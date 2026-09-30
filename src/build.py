#!/usr/bin/env python3
"""Build the standalone preview files from src/.

Outputs, each a single self-contained HTML file:
  index.html                        picker listing every variant (repo root)
  huong-X/hero-1.html ... hero-5.html  homepage for direction X, one per hero design
  huong-X/cong-ty-thanh-vien.html   member companies page for direction X

CSS, JS, WebP images, SVG patterns and the favicon are inlined as data URIs, so
every file works when downloaded on its own. Only Google Fonts stays external.

Usage (from the repo root): python3 src/build.py
"""
import base64
import pathlib
import re

SRC = pathlib.Path(__file__).resolve().parent
ROOT = SRC.parent
MIME = {".webp": "image/webp", ".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml"}

# Hero variants per direction: (number, short name, one-line description, recommended)
DIRECTIONS = {
    "a": [
        ("1", "Ánh sáng thương hiệu", "Các khối tam giác chiếu sáng dải đồng từ bìa bộ nhận diện, hoạt họa vector trôi chậm.", True),
        ("2", "Lưới lattice, vệt sáng quét", "Họa tiết lattice gốc của thương hiệu, một vệt sáng đồng quét qua khoảng 14 giây một lượt.", False),
        ("3", "Ảnh duotone trong khung", "Toàn cảnh Vinhomes Central Park hai tông navy và champagne, đặt trong khung nhỏ.", False),
        ("4", "Khảm ảnh dự án", "Sáu ô ảnh dự án nhỏ, lần lượt chuyển sang dự án khác theo nhịp lệch nhau.", False),
        ("5", "Toàn cảnh chuyển động chậm", "Ảnh toàn cảnh tối màu phía sau chữ, trượt và phóng chậm thay cho video.", False),
    ],
    "b": [
        ("1", "Bình minh trên biển", "Bìa tạp chí: mặt trời đồng nhô lên trên đường chân trời, mặt biển lấp lánh.", True),
        ("2", "Khung vòm", "Ảnh bờ sông Sài Gòn trong khung vòm kiến trúc, trôi chậm.", False),
        ("3", "Dải phim dự án", "Dải ảnh dự án nhỏ chạy ngang liên tục dưới tiêu đề, dừng khi rê chuột.", False),
        ("4", "Mục lục năm lĩnh vực", "Năm lĩnh vực như mục lục tạp chí; rê chuột vào mục nào, ảnh lĩnh vực đó hiện ra.", False),
        ("5", "Tuyên ngôn", "Tôn chỉ của SVI Group hiện ra từng chữ trên nền tím nâu.", False),
    ],
}
# Direction A's lattice hero needs the lattice <symbol> injected once per page.
EXTRA_PARTIALS = {("a", "2"): "huong-a/heroes/lattice-symbol.html"}


def data_uri(path: pathlib.Path) -> str:
    return f"data:{MIME[path.suffix]};base64,{base64.b64encode(path.read_bytes()).decode()}"


def css(name: str) -> str:
    text = (SRC / "css" / name).read_text(encoding="utf-8")
    return re.sub(r'url\("\.\./(img/[^"]+)"\)', lambda m: f'url("{data_uri(SRC / m.group(1))}")', text)


def inline(html: str, name: str) -> str:
    """Inline stylesheets, script, favicon and <picture> images."""

    def picture(m: re.Match) -> str:
        webp, attrs = m.group(1), re.sub(r'\s*src="[^"]+"', "", m.group(2))
        return f'<img src="{data_uri(SRC / webp)}"{attrs}>'

    html = re.sub(
        r'<picture>\s*<source type="image/webp" srcset="([^"]+)">\s*<img([^>]*)>\s*</picture>', picture, html
    )
    html = re.sub(
        r'<link rel="stylesheet" href="css/([^"]+)">', lambda m: f"<style>\n{css(m.group(1))}</style>", html
    )
    html = html.replace(
        '<script src="js/site.js"></script>',
        f"<script>\n{(SRC / 'js' / 'site.js').read_text(encoding='utf-8')}</script>",
    )
    # url("img/...") inside inline <style> blocks (e.g. hero-only backgrounds)
    html = re.sub(r'url\("(img/[^"]+)"\)', lambda m: f'url("{data_uri(SRC / m.group(1))}")', html)
    html = html.replace('href="img/favicon.png"', f'href="{data_uri(SRC / "img" / "favicon.png")}"')
    leftovers = re.findall(r'(?:src|href|srcset)="((?:img|css|js)/[^"]+)"', html)
    if leftovers:
        raise SystemExit(f"{name}: unresolved local references {leftovers}")
    return html


def write(name: str, html: str) -> None:
    out = ROOT / name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(inline(html, name), encoding="utf-8")
    print(f"{name}: {out.stat().st_size / 1024:.0f} KB")


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
        )
        write(f"{folder}/hero-{n}.html", html)
    write(f"{folder}/cong-ty-thanh-vien.html", (SRC / folder / "cong-ty-thanh-vien.html").read_text(encoding="utf-8"))


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
