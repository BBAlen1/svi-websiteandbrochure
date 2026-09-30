# SVI Group website design previews

Every HTML file at the top level of this repo is a single, self-contained page. CSS, JS and images are all embedded, so each one works when downloaded and opened on its own. The only external request is Google Fonts (Be Vietnam Pro).

| File | What it is |
|---|---|
| `index.html` | Picker listing every design variant (start here) |
| `huong-a/hero-1.html` to `hero-5.html` | Direction A homepage, one per hero design. A small switcher in the bottom-right corner jumps between them |
| `huong-a/cong-ty-thanh-vien.html` | Direction A member companies page (draft content) |
| `huong-b/hero-1.html` to `hero-5.html` | Direction B (editorial, warm) homepage, one per hero design |
| `huong-b/cong-ty-thanh-vien.html` | Direction B member companies page (draft content) |

**Direction A: conservative institutional.** Navy, sans-serif, restrained; closer to CapitaLand or Keppel.
**Direction B: editorial and warm.** Cream, plum and copper, with a serif for headings (Noto Serif Display). It's laid out like a magazine, with numbered chapters, an interactive project map, and SVI's own vision, mission, values and motto from the company profile.

Links between pages only work when the folder structure is kept as it is here. `src/` holds the editable source and can be ignored when reviewing designs.

## Editing

Don't edit the top-level files by hand. They're generated from `src/` by running `python3 src/build.py` from the repo root:

- `src/huong-a/`, `src/huong-b/`: each direction's homepage template (`home.html`, with a `<!-- HERO -->` slot), its five hero designs (`heroes/`), and its member companies page
- `src/picker.html`: the picker page; the variant lists come from `DIRECTIONS` in `src/build.py`
- `src/css/heroes.css`: Direction A heroes; `src/css/huong-b.css`: Direction B skin, sections and heroes
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
| `src/img/huong-b/*` | Vietnamese profile, pp.6, 21, 22, 23, 26 | One image per business line, plus the riverside aerial for the arch hero. The wind turbine, port and Bitexco images look like stock photos licensed by the profile's designer; confirm they can be reused on the website |
| `src/huong-b/partials/map.svg` | Natural Earth (public domain), via the `world-atlas` package | Vietnam outline, projected and simplified. Hoàng Sa and Trường Sa are added by hand, because Natural Earth doesn't show them as part of Vietnam |
| `src/img/du-an/*` | Vietnamese profile, pp.3, 7, 10, 11, 12, 13, 14, 16, 18 | Cropped from the flattened page rasters and resized for tiles. Each has a WebP file plus a JPEG fallback |

All facts and figures are taken from the Vietnamese profile. Project status dates are left out on purpose.
