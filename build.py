#!/usr/bin/env python3
"""Build single-file pages from src/.

Each page in src/ loads its CSS, JS and images from sibling folders, so it breaks
when the .html is downloaded on its own. This inlines everything (CSS, JS, WebP
images, SVG patterns, favicon) as data URIs and writes standalone copies next to
this script. Only Google Fonts stays external.

Usage: python3 build.py
"""
import base64
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src"
PAGES = ["index.html", "cong-ty-thanh-vien.html", "hero-options.html"]
MIME = {".webp": "image/webp", ".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml"}


def data_uri(path: pathlib.Path) -> str:
    return f"data:{MIME[path.suffix]};base64,{base64.b64encode(path.read_bytes()).decode()}"


def inline_css() -> str:
    css = (SRC / "css" / "site.css").read_text(encoding="utf-8")
    return re.sub(
        r'url\("\.\./(img/[^"]+)"\)',
        lambda m: f'url("{data_uri(SRC / m.group(1))}")',
        css,
    )


def build(page: str) -> None:
    html = (SRC / page).read_text(encoding="utf-8")

    # <picture><source webp><img fallback></picture>  ->  <img src="data:image/webp">
    def picture(m: re.Match) -> str:
        webp, img_attrs = m.group(1), m.group(2)
        img_attrs = re.sub(r'\s*src="[^"]+"', "", img_attrs)
        return f'<img src="{data_uri(SRC / webp)}"{img_attrs}>'

    html, n = re.subn(
        r'<picture>\s*<source type="image/webp" srcset="([^"]+)">\s*<img([^>]*)>\s*</picture>',
        picture,
        html,
    )

    html = html.replace('<link rel="stylesheet" href="css/site.css">', f"<style>\n{inline_css()}</style>")
    html = html.replace(
        '<script src="js/site.js"></script>',
        f"<script>\n{(SRC / 'js' / 'site.js').read_text(encoding='utf-8')}</script>",
    )
    html = html.replace('href="img/favicon.png"', f'href="{data_uri(SRC / "img" / "favicon.png")}"')

    leftovers = re.findall(r'(?:src|href|srcset)="((?:img|css|js)/[^"]+)"', html)
    if leftovers:
        raise SystemExit(f"{page}: unresolved local references {leftovers}")

    out = ROOT / page
    out.write_text(html, encoding="utf-8")
    print(f"{page}: {n} images inlined, {out.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    for p in PAGES:
        build(p)
