#!/usr/bin/env python3
"""Build the preview pages from src/.

Two outputs from the same source:

  Hosted (repo root, for GitHub Pages): fast
    index.html, huong-X/hero-1..5.html, huong-X/cong-ty-thanh-vien.html
    Images are separate files in assets/, lazy-loaded and cached across pages.

  Downloadable (tai-ve/): one self-contained file per page
    Same pages with CSS, JS and WebP images embedded as data URIs, so each file
    works when downloaded and opened on its own.

Only Google Fonts stays external in both.

Usage (from the repo root): python3 src/build.py
"""
import base64
import pathlib
import re
import shutil

from PIL import Image

SRC = pathlib.Path(__file__).resolve().parent
ROOT = SRC.parent
MIME = {".webp": "image/webp", ".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml"}

# Hero variants per direction: (number, short name, one-line description, recommended)
DIRECTIONS = {
    "a": [
        ("1", "Dải ảnh dự án", "Hai cột ảnh dự án trôi chậm ngược chiều nhau, dừng khi rê chuột.", False),
        ("2", "Lưới lattice, vệt sáng quét", "Họa tiết lattice gốc của thương hiệu, một vệt sáng đồng quét qua khoảng 14 giây một lượt.", True),
        ("3", "Toàn cảnh chuyển động chậm", "Ảnh toàn cảnh tối màu phía sau chữ, trượt và phóng chậm thay cho video.", False),
        ("4", "Biểu tượng thương hiệu", "Logo chữ S khối đồng lơ lửng, có vệt sáng lướt qua.", False),
        ("5", "Bức tường danh mục", "Lưới ảnh dự án tối màu phía sau chữ, lần lượt từng ô sáng lên.", False),
    ],
    "b": [
        ("1", "Xấp ảnh dự án", "Các ảnh dự án in như ảnh chụp, lần lượt được rút ra khỏi xấp.", False),
        ("2", "Lật trang tạp chí", "Ảnh dự án khổ dọc lần lượt hiện ra như lật trang, có số thứ tự.", False),
        ("3", "Dải phim dự án", "Dải ảnh dự án nhỏ chạy ngang liên tục dưới tiêu đề, dừng khi rê chuột.", True),
        ("4", "Năm lĩnh vực mở rộng", "Năm dải ảnh lĩnh vực, lần lượt mở rộng; rê chuột để chọn.", False),
        ("5", "Bộ ba khổ dọc", "Ba ảnh dự án khổ dọc so le, ảnh trôi chậm lên xuống bên trong khung.", False),
    ],
    "c": [
        ("1", "Chữ chuyển động", "Tên năm lĩnh vực chạy ngang thành hai dải chữ cỡ lớn, viền và đồng.", False),
        ("2", "Toàn cảnh mở rộng", "Ảnh bờ sông Sài Gòn trong khung bo góc, mở rộng ra toàn màn hình khi cuộn trang.", False),
        ("3", "Biểu tượng lắp ghép", "Logo chữ S dựng lại bằng vector từ bộ nhận diện; từng mảnh tam giác bay vào ghép thành hình.", True),
        ("4", "Lĩnh vực xoay vòng", "Dòng “Đầu tư vào…” lần lượt đổi tên năm lĩnh vực, kèm ảnh tương ứng.", False),
        ("5", "Mặt phẳng dự án 3D", "Các cột ảnh dự án trên mặt phẳng nghiêng phối cảnh, trôi chậm phía sau chữ.", False),
    ],
}
# Direction A's lattice hero needs the lattice <symbol> injected once per page.
EXTRA_PARTIALS = {("a", "2"): "huong-a/heroes/lattice-symbol.html"}


def data_uri(path: pathlib.Path) -> str:
    return f"data:{MIME[path.suffix]};base64,{base64.b64encode(path.read_bytes()).decode()}"


# Images with a smaller phone variant (file "<name>-<w>.webp"): full width, small width.
RESPONSIVE = {"img/huong-c/toan-canh-song.webp": 1200, "img/hero/vcp-pano.webp": 800}

# Audiowide only sets the English company name, so request just those glyphs.
AUDIOWIDE = ('<link href="https://fonts.googleapis.com/css2?family=Audiowide&amp;text='
             'SouthernVisionInvestmentCorporationSOUTHERNVISIONINVESTMENTCORPORATION%20&amp;display=swap" rel="stylesheet">')


def fonts(html: str) -> str:
    if "family=Audiowide" not in html:
        return html
    html = html.replace("&amp;family=Audiowide", "")
    return re.sub(r'(<link href="https://fonts\.googleapis\.com/css2\?family=Be[^>]+>)', lambda m: m.group(1) + "\n  " + AUDIOWIDE, html, count=1)


def prioritise_hero(html: str) -> str:
    """The hero's first image is the likely largest paint: load it eagerly at high priority."""
    i = html.find('id="gioi-thieu"')
    if i < 0:
        return html
    j = html.find("</section>", i)
    hero = html[i:j].replace(' loading="lazy"', "")
    hero = re.sub(r"<img ", '<img fetchpriority="high" ', hero, count=1)
    return html[:i] + hero + html[j:]


def lazy_async(html: str) -> str:
    return html.replace(' loading="lazy"', ' loading="lazy" decoding="async"')


def css(name: str, url) -> str:
    text = (SRC / "css" / name).read_text(encoding="utf-8")
    return re.sub(r'url\("\.\./(img/[^"]+)"\)', lambda m: f'url("{url(m.group(1))}")', text)


def common(html: str, url) -> str:
    html = re.sub(r'<link rel="stylesheet" href="css/([^"]+)">', lambda m: f"<style>\n{css(m.group(1), url)}</style>", html)
    html = html.replace('<script src="js/site.js"></script>',
                        f"<script>\n{(SRC / 'js' / 'site.js').read_text(encoding='utf-8')}</script>")
    return lazy_async(prioritise_hero(fonts(html)))


def standalone(html: str, name: str) -> str:
    """Everything embedded (WebP only), so the single file works when downloaded."""
    def picture(m: re.Match) -> str:
        webp, attrs = m.group(1), re.sub(r'\s*src="[^"]+"', "", m.group(2))
        return f'<img src="{data_uri(SRC / webp)}"{attrs}>'
    html = re.sub(r'<picture>\s*<source type="image/webp" srcset="([^"]+)">\s*<img([^>]*)>\s*</picture>', picture, html)
    html = common(html, lambda p: data_uri(SRC / p))
    html = re.sub(r'url\("(img/[^"]+)"\)', lambda m: f'url("{data_uri(SRC / m.group(1))}")', html)
    html = html.replace('href="img/favicon.png"', f'href="{data_uri(SRC / "img" / "favicon.png")}"')
    left = re.findall(r'(?:src|href|srcset)="((?:img|css|js)/[^"]+)"', html)
    if left:
        raise SystemExit(f"{name}: unresolved local references {left}")
    return html


USED: set = set()


def hosted(html: str, name: str) -> str:
    """Images as separate cached files under assets/, loaded lazily below the fold."""
    prefix = "../" * name.count("/")
    def url(p: str) -> str:
        USED.add(p)
        return f"{prefix}assets/{p}"
    def source(m: re.Match) -> str:
        p = m.group(1)
        if p in RESPONSIVE:
            w = RESPONSIVE[p]; small = p.replace(".webp", f"-{w}.webp")
            full = Image.open(SRC / p).width
            return f'<source type="image/webp" srcset="{url(small)} {w}w, {url(p)} {full}w" sizes="100vw">'
        return f'<source type="image/webp" srcset="{url(p)}">'
    html = re.sub(r'<source type="image/webp" srcset="(img/[^"]+)">', source, html)
    html = common(html, url)
    html = re.sub(r'((?:src|href)=")(img/[^"]+)"', lambda m: f'{m.group(1)}{url(m.group(2))}"', html)
    html = re.sub(r'url\("(img/[^"]+)"\)', lambda m: f'url("{url(m.group(1))}")', html)
    return html


def write(name: str, html: str) -> None:
    for out, body in ((ROOT / name, hosted(html, name)), (ROOT / "tai-ve" / name, standalone(html, name))):
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(body, encoding="utf-8")
    print(f"{name}: hosted {(ROOT / name).stat().st_size / 1024:.0f} KB, standalone {(ROOT / 'tai-ve' / name).stat().st_size / 1024:.0f} KB")


def copy_assets() -> None:
    dest = ROOT / "assets"
    if dest.exists():
        shutil.rmtree(dest)
    for p in sorted(USED):
        (dest / p).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SRC / p, dest / p)
        if p.endswith(".webp"):  # <picture> fallback
            for ext in (".jpg", ".png"):
                fb = SRC / p.replace(".webp", ext)
                if fb.exists():
                    shutil.copy2(fb, dest / p.replace(".webp", ext))
    size = sum(f.stat().st_size for f in dest.rglob("*") if f.is_file())
    print(f"assets/: {len(USED)} images referenced, {size / 1024:.0f} KB on disk")


def switcher(d: str, current: str) -> str:
    links = "".join(
        f'<a href="hero-{n}.html"{CURRENT if n == current else ""} title="Hero {n}: {name}">{n}</a>'
        for n, name, _, _ in DIRECTIONS[d]
    )
    return (
        '  <nav class="variant-switch" aria-label="Chọn phương án hero (chỉ dùng khi duyệt thiết kế)">'
        f'<a class="lbl" href="../index.html" title="Tất cả phương án">Hướng {d.upper()} · Hero</a>{links}</nav>'
    )


CURRENT = ' aria-current="page"'


def build_direction(d: str) -> None:
    folder = f"huong-{d}"
    home = (SRC / folder / "home.html").read_text(encoding="utf-8")
    for n, _, _, _ in DIRECTIONS[d]:
        hero = (SRC / folder / "heroes" / f"hero-{n}.html").read_text(encoding="utf-8")
        extra = EXTRA_PARTIALS.get((d, n))
        html = (
            home.replace("<!-- HERO -->", hero)
            .replace("<!-- LATTICE -->", (SRC / extra).read_text(encoding="utf-8") if extra else "")
            .replace("<!-- SWITCHER -->", switcher(d, n))
            .replace("{{SELF}}", f"hero-{n}.html")
            .replace("<title>SVI Group |", f"<title>Hướng {d.upper()} · Hero {n} | SVI Group |")
            .replace("Bản xem trước thiết kế · Hướng A", f"Bản xem trước thiết kế · Hướng {d.upper()}")
        )
        write(f"{folder}/hero-{n}.html", html)
    member = (SRC / folder / "cong-ty-thanh-vien.html").read_text(encoding="utf-8")
    write(f"{folder}/cong-ty-thanh-vien.html", member.replace("Bản xem trước thiết kế · Hướng A", f"Bản xem trước thiết kế · Hướng {d.upper()}"))


def build_picker() -> None:
    html = (SRC / "picker.html").read_text(encoding="utf-8")
    for d, variants in DIRECTIONS.items():
        items = "\n".join(
            f"""        <li>
          <a class="pick" href="huong-{d}/hero-{n}.html">
            <span class="pick__n">Hero {n}</span>
            <span class="pick__t">{name}{' <em>Đề xuất</em>' if rec else ''}</span>
            <span class="pick__d">{desc}</span>
          </a>
        </li>"""
            for n, name, desc, rec in variants
        )
        html = html.replace(f"<!-- VARIANTS_{d.upper()} -->", items)
    write("index.html", html)


if __name__ == "__main__":
    for d in DIRECTIONS:
        build_direction(d)
    build_picker()
    copy_assets()
