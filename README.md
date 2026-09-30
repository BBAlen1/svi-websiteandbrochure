# SVI Group homepage preview, Direction A (conservative institutional)

`index.html` and `cong-ty-thanh-vien.html` in this folder are single, self-contained files. CSS, JS and images are all embedded, so each one works when downloaded and opened on its own. The only external request is Google Fonts (Be Vietnam Pro). For the link between the two pages to work, keep both files in the same folder.

Don't edit those two files by hand. They're generated from `src/`:

- `src/index.html`, `src/cong-ty-thanh-vien.html`: the pages
- `src/css/site.css`: shared stylesheet
- `src/js/site.js`: mobile menu toggle, the only script
- `src/img/`: images, each as WebP plus a JPEG/PNG fallback

After changing anything in `src/`, run `python3 build.py` to regenerate the standalone files. The standalone files embed only the WebP images. This keeps the homepage at about 0.9 MB, but it means browsers from before 2020 won't show the images. The `src/` version keeps the JPEG/PNG fallbacks.

## Where the assets came from

All images come from the three supplied PDFs. There is no stock photography and nothing AI-generated.

| Asset | Source | Method |
|---|---|---|
| `src/img/logo/*` | Brand Identity PDF, p.2 | Vector page re-rendered at 1000 dpi on transparency, with the background shading, drop shadow and the Octopus Design watermark removed from the content stream. Horizontal lockup composed from the mark plus the wordmark, following the chairman business card on p.4 |
| `src/img/pattern-lattice-*.svg` | Brand Identity PDF, p.8 (envelope band) | Exact polygon geometry pulled from the PDF form object, recoloured. It repeats horizontally only, as on the stationery |
| `src/img/doi-tac/*` | Vietnamese profile, p.29 | Cropped from the flattened page raster (source logos are about 100 to 220px wide), converted to grayscale with the midtones darkened |
| `src/img/du-an/*` | Vietnamese profile, pp.3, 7, 10, 11, 12, 13, 14, 16, 18 | Cropped from the flattened page rasters and resized for tiles. Each has a WebP file plus a JPEG fallback |

All facts and figures are taken from the Vietnamese profile. Project status dates are left out on purpose.
