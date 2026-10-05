# SVI Group website design previews

There are two copies of every page, built from the same source:

- **Hosted pages** (repo root: `index.html`, `huong-a/`, `huong-b/`, `huong-c/`). Use these for the GitHub Pages link. Images are separate files in `assets/`, so they load as you scroll, and the browser caches them as you move between variants. They also work when you open them from a downloaded copy of the whole repo.
- **Single-file downloads** (`tai-ve/`, "downloads"). These are the same pages with everything embedded, so one `.html` file works on its own when downloaded. They're slower to load (1 to 1.7 MB each), so only use them for sending a file.

| File | What it is |
|---|---|
| `index.html` | Picker listing every design variant (start here) |
| `huong-a/hero-1.html` to `hero-5.html` | Direction A homepage, one per hero design. A small switcher in the bottom-right corner jumps between them |
| `huong-a/cong-ty-thanh-vien.html` | Direction A member companies page (draft content) |
| `huong-b/hero-1.html` to `hero-5.html` | Direction B (editorial, warm) homepage, one per hero design |
| `huong-b/cong-ty-thanh-vien.html` | Direction B member companies page (draft content) |
| `huong-c/hero-1.html` to `hero-5.html` | Direction C (bold, modern) homepage, one per hero design |
| `huong-c/cong-ty-thanh-vien.html` | Direction C member companies page (draft content) |

Measured on a throttled mobile 4G connection (1.6 Mbps, 150 ms latency, 4× slower CPU), a hosted homepage paints in 0.5 to 1 s and finishes loading in 1.2 to 3.1 s.

**Direction A: conservative institutional.** Navy, sans-serif, restrained; closer to CapitaLand or Keppel.
**Direction B: editorial and warm.** Cream, plum and copper, with a serif for headings (Noto Serif Display). It's laid out like a magazine, with numbered chapters, an interactive project map, and SVI's own vision, mission, values and motto from the company profile.
**Direction C: bold and modern.** Dark throughout, oversized Unbounded headings, copper gradients, stronger motion. Partner logos run as a moving wall, projects sit in a tile grid, a bar chart compares investment across ongoing projects, and SVI's motto lights up word by word as you scroll.

Links between pages only work when the folder structure is kept as it is here. `src/` holds the editable source and can be ignored when reviewing designs.

## Editing

Don't edit the built pages by hand. Both copies are generated from `src/` by running `python3 src/build.py` from the repo root:

- `src/huong-a/`, `src/huong-b/`, `src/huong-c/`: each direction's homepage template (`home.html`, with a `<!-- HERO -->` slot), its five hero designs (`heroes/`), and its member companies page
- `src/picker.html`: the picker page; the variant lists come from `DIRECTIONS` in `src/build.py`
- `src/css/heroes.css`: Direction A heroes; `src/css/huong-a.css`: Direction A section styles (business line cards, vision band, project filter, member cards); `src/css/huong-b.css`: Direction B skin, sections and heroes; `src/css/huong-c.css`: Direction C skin, sections and heroes
- Typography: the English company name uses Audiowide, the typeface of "SOUTHERN VISION" in the logo (identified from the brand identity PDF). Audiowide has no Vietnamese characters, so Vietnamese text stays in Be Vietnam Pro (and Noto Serif Display in Direction B). The logo's "INVESTMENT" line is set in Eurostile, a paid font, so it isn't used on the site
- `src/css/site.css`, `src/js/site.js`: shared styles, the mobile menu, and the scroll animations
- `src/img/`: images, each as WebP plus a JPEG/PNG fallback. The built files embed only the WebP versions, so browsers from before 2020 won't show the images

All motion (hero entrance, scroll reveals, icon drawing, hero animations) switches off automatically when the viewer's device asks for reduced motion.

## Where the assets came from

All images come from the three supplied PDFs. There is no stock photography and nothing AI-generated.

| Asset | Source | Method |
|---|---|---|
| `src/img/logo/*` | Brand Identity PDF, p.2 | Vector page re-rendered at 1000 dpi on transparency, with the background shading, drop shadow and the Octopus Design watermark removed from the content stream. Horizontal lockup composed from the mark plus the wordmark, following the chairman business card on p.4 |
| `src/img/pattern-lattice-*.svg` | Brand Identity PDF, p.8 (envelope band) | Exact polygon geometry pulled from the PDF form object, recoloured. It repeats horizontally only, as on the stationery |
| `src/img/doi-tac/*` | Vietnamese profile, p.29 | Cropped from the flattened page raster (source logos are about 100 to 220px wide), converted to grayscale with the midtones darkened |
| `src/img/hero2/*` | Brand Identity PDF p.2 (logo mark); Vietnamese profile pp.3, 10, 11, 12, 13, 14, 18 | Large logo mark for hero A4, and portrait crops of project renders for the B heroes |
| `src/img/huong-b/*` | Vietnamese profile, pp.6, 21, 22, 23, 26 | One image per business line, plus the riverside aerial for the arch hero. The wind turbine, port and Bitexco images look like stock photos licensed by the profile's designer; confirm they can be reused on the website |
| `src/huong-b/partials/map.svg` | Natural Earth (public domain), via the `world-atlas` package | Vietnam outline, projected and simplified. Hoàng Sa and Trường Sa are added by hand, because Natural Earth doesn't show them as part of Vietnam |
| `src/img/huong-c/toan-canh-song.*` | Vietnamese profile, p.6 | Full riverside aerial (2400 px wide, the highest-resolution image in the profile) for hero C2 |
| `src/huong-c/partials/mark.svg` | Brand Identity PDF, p.2 | The S mark rebuilt as true vectors: 16 triangle shapes and the metallic gradient read directly from the PDF's drawing instructions, so it stays sharp at any size |
| `src/img/du-an/*` | Vietnamese profile, pp.3, 7, 10, 11, 12, 13, 14, 16, 18 | Cropped from the flattened page rasters and resized for tiles. Each has a WebP file plus a JPEG fallback |

All facts and figures are taken from the Vietnamese profile. Project status dates are left out on purpose.
