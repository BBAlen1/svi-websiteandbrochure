#!/usr/bin/env python3
"""Generate src/hero-options.html: five hero treatments for Direction A, side by side.

Header and hero copy are taken from src/index.html so the options stay in sync.
Run from svi-direction-a/:  python3 tools/gen_hero_options.py && python3 build.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

src = (SRC / "index.html").read_text(encoding="utf-8")
lat = re.search(r' d="([^"]+)"', (SRC / "img/pattern-lattice-copper.svg").read_text()).group(1)
head = src.split('<a class="skip-link"')[0]
head = head.replace(
    "<title>SVI Group | Công ty Cổ phần Đầu tư Tầm Nhìn Phương Nam</title>",
    "<title>Phương án hero | SVI Group</title>",
).replace('<meta name="theme-color"', '<meta name="robots" content="noindex">\n  <meta name="theme-color"')
header = re.search(r"(  <header class=\"site-header\">.*?</header>)", src, re.S).group(1)
header = header.replace('href="#', 'href="index.html#')

LAZY = ' loading="lazy"'


def pic(name, alt, cls="", w=1444, h=576, eager=False):
    lazy = "" if eager else LAZY
    return (f'<picture><source type="image/webp" srcset="img/{name}.webp">'
            f'<img class="{cls}" src="img/{name}.jpg" width="{w}" height="{h}" alt="{alt}"{lazy}></picture>')


LINES = """<nav class="hero__lines" aria-label="Năm lĩnh vực hoạt động">
          <p class="hero__lines-title">Năm lĩnh vực hoạt động</p>
          <ol>
            <li><a href="index.html#linh-vuc-1"><span class="num">01</span>Bất Động Sản</a></li>
            <li><a href="index.html#linh-vuc-2"><span class="num">02</span>Dịch Vụ Ăn Uống và Giải Trí</a></li>
            <li><a href="index.html#linh-vuc-3"><span class="num">03</span>Tài Chính - Công Nghệ</a></li>
            <li><a href="index.html#linh-vuc-4"><span class="num">04</span>Năng Lượng và Môi Trường</a></li>
            <li><a href="index.html#linh-vuc-5"><span class="num">05</span>Thương Mại - Xuất Nhập Khẩu</a></li>
          </ol>
        </nav>"""


def text(hid):
    return f"""<div class="hero__text">
          <p class="eyebrow">SVI Group</p>
          <h1 id="{hid}">
            <span class="hero__kicker">Công ty Cổ phần Đầu tư</span>
            Tầm Nhìn Phương Nam
            <span class="en" lang="en">Southern Vision Investment Corporation</span>
          </h1>
          <span class="rule-copper" aria-hidden="true"></span>
          <p class="hero__lead">Nhà đầu tư đa ngành với trọng tâm là đầu tư và kinh doanh bất động sản, kế thừa kinh nghiệm và đội ngũ của Công ty Tân Liên Phát, chủ đầu tư ban đầu của dự án Khu phức hợp Tân Cảng Sài Gòn (Vinhomes Central Park).</p>
          <div class="hero__actions">
            <a class="link-arrow" href="index.html#du-an">Danh mục dự án</a>
            <a class="link-arrow" href="index.html#lien-he">Liên hệ hợp tác</a>
          </div>
        </div>"""


def label(n, name, what, pro, con, verdict):
    return f"""  <div class="opt-label">
    <div class="wrap">
      <p class="opt-label__n">Phương án {n}</p>
      <h2 class="opt-label__t">{name}</h2>
      <p class="opt-label__what">{what}</p>
      <dl class="opt-label__pc">
        <div><dt>Ưu điểm</dt><dd>{pro}</dd></div>
        <div><dt>Hạn chế</dt><dd>{con}</dd></div>
        <div><dt>Đánh giá</dt><dd>{verdict}</dd></div>
      </dl>
    </div>
  </div>"""


# 1. Brand light peaks: recreates the cover of the brand identity book
def peak(i, ax, ay, s):
    lx, ly = ax - 230 * s, ay + 660 * s
    mx, my = ax - 120 * s, ay + 720 * s
    rx, ry = ax + 460 * s, ay + 400 * s
    return f"""<g class="peak peak--{i}">
        <polygon points="{ax},{ay} {rx:.0f},{ry:.0f} {mx:.0f},{my:.0f}" fill="url(#pk-shade)"/>
        <polygon class="peak__lit" points="{ax},{ay} {mx:.0f},{my:.0f} {lx:.0f},{ly:.0f}" fill="url(#pk-lit)"/>
      </g>"""


BEAMS = f"""<svg class="beams" viewBox="0 0 1440 820" preserveAspectRatio="xMaxYMid slice" aria-hidden="true" focusable="false">
      <defs>
        <linearGradient id="pk-lit" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="#F0A56A" stop-opacity=".95"/>
          <stop offset=".25" stop-color="#C8834F" stop-opacity=".55"/>
          <stop offset="1" stop-color="#C8834F" stop-opacity="0"/>
        </linearGradient>
        <linearGradient id="pk-shade" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stop-color="#8A6A5A" stop-opacity=".55"/>
          <stop offset=".45" stop-color="#3A3F5C" stop-opacity=".35"/>
          <stop offset="1" stop-color="#252C45" stop-opacity="0"/>
        </linearGradient>
      </defs>
      {peak(1, 1130, 60, 1.0)}
      {peak(2, 1360, 330, .8)}
      {peak(3, 860, 250, .62)}
    </svg>"""

# 2. Lattice: the real brand band, stacked into a field
rows = "".join(f'<use href="#band" x="{x}" y="{y * 43.94:.2f}"/>' for y in range(14) for x in (0, 303.01, 606.02))
LATTICE_SYM = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">'
               f'<symbol id="band" viewBox="0 0 303.01 43.94" width="303.01" height="43.94" overflow="visible"><path d="{lat}"/></symbol></svg>')


def lattice(cls):
    return f'<svg class="{cls}" viewBox="0 0 909 615" preserveAspectRatio="xMinYMin slice" aria-hidden="true" focusable="false">{rows}</svg>'


# 4. Mosaic tiles
tiles = [("mui-cu-hin", "landmark-81"), ("dong-hai-plaza", "vinh-hoa-emerald"), ("hung-vuong-symphony", "nha-o-xa-hoi"),
         ("van-phong", "cape-pearl-thanh-da"), ("dong-tranh", "mui-cu-hin"), ("nha-o-xa-hoi", "dong-hai-plaza")]
names = {"mui-cu-hin": "Mũi Cù Hin", "landmark-81": "Landmark 81", "dong-hai-plaza": "Đông Hải Plaza",
         "vinh-hoa-emerald": "Vịnh Hòa Emerald", "hung-vuong-symphony": "Hùng Vương Symphony",
         "nha-o-xa-hoi": "Nhà ở xã hội", "van-phong": "Vân Phong", "cape-pearl-thanh-da": "Cape Pearl Thanh Đa",
         "dong-tranh": "Đồng Tranh"}
MOSAIC = '<ul class="mosaic" aria-label="Hình ảnh dự án">' + "".join(
    f'<li style="--d:{i * 1.6:.1f}s"><figure>{pic("du-an/" + a, "", w=640, h=480)}<figcaption>{names[a]}</figcaption></figure>'
    f'<figure class="alt" aria-hidden="true">{pic("du-an/" + b, "", w=640, h=480)}<figcaption>{names[b]}</figcaption></figure></li>'
    for i, (a, b) in enumerate(tiles)) + "</ul>"

opts = []
opts.append(label(
    1, "Ánh sáng thương hiệu (hoạt họa SVG)",
    "Dựng lại hình ảnh chủ đạo trên trang bìa Brand Identity: các khối tam giác được chiếu sáng bằng dải đồng. Vẽ hoàn toàn bằng vector, trôi rất chậm và ánh sáng “thở”.",
    "Đúng hình ảnh thương hiệu, sắc nét trên mọi màn hình, dung lượng gần như bằng 0, không phụ thuộc ảnh độ phân giải thấp.",
    "Trừu tượng: người xem chưa thấy dự án nào. Hình ảnh thuộc bộ nhận diện chưa xác nhận đã thanh toán bản quyền.",
    "<strong>Đề xuất số 1.</strong> Khớp định hướng thể chế, không có rủi ro về chất lượng ảnh.") + f"""
  <section class="hero hero--beams on-dark" aria-labelledby="h1a">
    {BEAMS}
    <div class="wrap hero__grid">
        {text("h1a")}
        {LINES}
    </div>
    <div class="lattice-band lattice-band--copper" aria-hidden="true"></div>
  </section>""")

opts.append(label(
    2, "Lưới lattice với vệt sáng quét",
    "Họa tiết lattice gốc của thương hiệu phủ nửa phải hero ở độ mờ thấp; một vệt sáng đồng quét chéo qua rất chậm (khoảng 14 giây một lượt).",
    "Rất tiết chế, đúng tinh thần “nghiêm túc, lâu đời”; dùng đúng hình học trích từ PDF.",
    "Kín đáo tới mức nhiều người không nhận ra có chuyển động; vẫn không có hình ảnh dự án.",
    "Tốt nếu CEO thấy phương án 1 quá “trình diễn”.") + f"""
  <section class="hero hero--lattice on-dark" aria-labelledby="h1b">
    <div class="lat-wrap" aria-hidden="true">{lattice("lat lat--base")}{lattice("lat lat--glow")}</div>
    <div class="wrap hero__grid">
        {text("h1b")}
        {LINES}
    </div>
  </section>""")

opts.append(label(
    3, "Ảnh hero duotone trong khung",
    "Ảnh toàn cảnh Vinhomes Central Park chuyển sang hai tông navy và champagne, đặt trong khung cố định phía trên danh sách lĩnh vực.",
    "Có hình ảnh thật, của dự án mạnh nhất. Duotone che được nhiễu JPEG; ảnh nguồn 1444px đủ nét cho khung khoảng 560px.",
    "Đây là phối cảnh của Vingroup và Landmark 81 là biểu tượng của Vingroup: đặt ở đầu trang dễ khiến người xem hiểu đây hoàn toàn là dự án của SVI.",
    "<strong>Đề xuất số 2</strong>, nếu CEO muốn có ảnh thật ngay màn hình đầu.") + f"""
  <section class="hero hero--duotone on-dark" aria-labelledby="h1c">
    <div class="wrap hero__grid">
        {text("h1c")}
        <div class="hero__side">
          <figure class="duo">
            {pic("hero/vcp-duotone", "Toàn cảnh Khu đô thị Vinhomes Central Park bên sông Sài Gòn", eager=True)}
            <figcaption>Vinhomes Central Park · 43,91 ha</figcaption>
          </figure>
          {LINES}
        </div>
    </div>
    <div class="lattice-band lattice-band--copper" aria-hidden="true"></div>
  </section>""")

opts.append(label(
    4, "Khảm ảnh dự án, chuyển cảnh chậm",
    "Sáu ô ảnh nhỏ các dự án; mỗi ô lần lượt hòa sang ảnh dự án khác theo nhịp lệch nhau, tên dự án hiện ở góc ô.",
    "Cho thấy độ rộng danh mục ngay màn hình đầu; ô nhỏ (khoảng 180px) nên ảnh độ phân giải thấp không bị soi.",
    "Nhiều chuyển động hơn, bắt đầu giống site bất động sản bán lẻ; nặng nhất (12 ảnh).",
    "Dùng được, nhưng lệch khỏi tinh thần tiết chế của hướng A.") + f"""
  <section class="hero hero--mosaic on-dark" aria-labelledby="h1d">
    <div class="wrap hero__grid">
        {text("h1d")}
        <div class="hero__side">
          {MOSAIC}
          {LINES}
        </div>
    </div>
    <div class="lattice-band lattice-band--copper" aria-hidden="true"></div>
  </section>""")

opts.append(label(
    5, "Toàn cảnh chuyển động chậm (thay cho video)",
    "Ảnh toàn cảnh phủ nửa phải hero, tối đi và hòa vào nền navy, trượt và phóng rất chậm kiểu Ken Burns. Đây là mức gần “video” nhất có thể làm với tài liệu hiện có.",
    "Cảm giác điện ảnh, có chiều sâu, không cần quay phim.",
    "Ảnh phải phóng to nên mềm trên màn hình retina, đúng điều brief muốn tránh. Video thật cần footage flycam dự án (xin chủ đầu tư hoặc thuê quay), hiện chưa có.",
    "Không đề xuất cho tới khi có footage thật.") + f"""
  <section class="hero hero--pan on-dark" aria-labelledby="h1e">
    <div class="pan" aria-hidden="true">{pic("hero/vcp-pano", "", "pan__img")}</div>
    <div class="wrap hero__grid">
        {text("h1e")}
        {LINES}
    </div>
  </section>""")

STYLE = (ROOT / "tools" / "hero-options.css").read_text(encoding="utf-8")

page = head.replace('<link rel="stylesheet" href="css/site.css">',
                    '<link rel="stylesheet" href="css/site.css">\n  <style>\n' + STYLE + "  </style>") + f"""<a class="skip-link" href="#noi-dung">Bỏ qua điều hướng</a>
  {LATTICE_SYM}
{header}
  <main id="noi-dung">
  <section class="opt-intro">
    <div class="wrap">
      <p class="eyebrow">Hướng A · Bản so sánh</p>
      <h1>Năm phương án cho phần hero</h1>
      <p>Mỗi phương án là một hero hoàn chỉnh, chạy thật trong trình duyệt. Tất cả chỉ dùng tài sản trích từ bộ nhận diện và hồ sơ năng lực, không có ảnh stock hay ảnh AI. Chuyển động tự tắt nếu thiết bị bật chế độ giảm chuyển động.</p>
    </div>
  </section>
{chr(10).join(opts)}
  </main>
  <script src="js/site.js"></script>
</body>
</html>
"""
(SRC / "hero-options.html").write_text(page, encoding="utf-8")
print("wrote src/hero-options.html", len(page))
