#!/usr/bin/env python3
"""Build the standalone preview files from src/.

Outputs (repo root), each a single self-contained HTML file:
  index.html                          picker listing every variant
  huong-a-1.html ... huong-a-5.html   Direction A homepage, one per hero design
  huong-a-cong-ty-thanh-vien.html     Direction A member companies page

CSS, JS, WebP images, SVG patterns and the favicon are inlined as data URIs, so
every file works when downloaded on its own. Only Google Fonts stays external.

Usage: python3 build.py
"""
import base64
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src"
MIME = {".webp": "image/webp", ".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml"}

# Direction A hero variants: (file suffix, short name, one-line description, recommended)
VARIANTS_A = [
    ("1", "Ánh sáng thương hiệu", "Các khối tam giác chiếu sáng dải đồng từ bìa bộ nhận diện, hoạt họa vector trôi chậm.", True),
    ("2", "Lưới lattice, vệt sáng quét", "Họa tiết lattice gốc của thương hiệu, một vệt sáng đồng quét qua khoảng 14 giây một lượt.", False),
    ("3", "Ảnh duotone trong khung", "Toàn cảnh Vinhomes Central Park hai tông navy và champagne, đặt trong khung nhỏ.", False),
    ("4", "Khảm ảnh dự án", "Sáu ô ảnh dự án nhỏ, lần lượt chuyển sang dự án khác theo nhịp lệch nhau.", False),
    ("5", "Toàn cảnh chuyển động chậm", "Ảnh toàn cảnh tối màu phía sau chữ, trượt và phóng chậm thay cho video.", False),
]


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
    html = html.replace('href="img/favicon.png"', f'href="{data_uri(SRC / "img" / "favicon.png")}"')
    leftovers = re.findall(r'(?:src|href|srcset)="((?:img|css|js)/[^"]+)"', html)
    if leftovers:
        raise SystemExit(f"{name}: unresolved local references {leftovers}")
    return html


def write(name: str, html: str) -> None:
    out = ROOT / name
    out.write_text(inline(html, name), encoding="utf-8")
    print(f"{name}: {out.stat().st_size / 1024:.0f} KB")


def switcher(current: str) -> str:
    links = "".join(
        f'<a href="huong-a-{n}.html"{CURRENT if n == current else ""} title="Hero {n}: {name}">{n}</a>'
        for n, name, _, _ in VARIANTS_A
    )
    return (
        '  <nav class="variant-switch" aria-label="Chọn phương án hero (chỉ dùng khi duyệt thiết kế)">'
        f'<a class="lbl" href="index.html" title="Tất cả phương án">Hướng A · Hero</a>{links}</nav>'
    )


CURRENT = ' aria-current="page"'


def build_direction_a() -> None:
    home = (SRC / "home.html").read_text(encoding="utf-8")
    lattice = (SRC / "heroes" / "lattice-symbol.html").read_text(encoding="utf-8")
    for n, _, _, _ in VARIANTS_A:
        page_name = f"huong-a-{n}.html"
        hero = (SRC / "heroes" / f"hero-{n}.html").read_text(encoding="utf-8")
        html = (
            home.replace("<!-- HERO -->", hero)
            .replace("<!-- LATTICE -->", lattice if n == "2" else "")
            .replace("<!-- SWITCHER -->", switcher(n))
            .replace("{{SELF}}", page_name)
            .replace("<title>SVI Group |", f"<title>Hướng A · Hero {n} | SVI Group |")
        )
        write(page_name, html)
    write("huong-a-cong-ty-thanh-vien.html", (SRC / "cong-ty-thanh-vien.html").read_text(encoding="utf-8"))


def build_picker() -> None:
    items = "\n".join(
        f"""        <li>
          <a class="pick" href="huong-a-{n}.html">
            <span class="pick__n">Hero {n}</span>
            <span class="pick__t">{name}{' <em>Đề xuất</em>' if rec else ''}</span>
            <span class="pick__d">{desc}</span>
          </a>
        </li>"""
        for n, name, desc, rec in VARIANTS_A
    )
    html = (SRC / "picker.html").read_text(encoding="utf-8").replace("<!-- VARIANTS_A -->", items)
    write("index.html", html)


if __name__ == "__main__":
    build_direction_a()
    build_picker()
