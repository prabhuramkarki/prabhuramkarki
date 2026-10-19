# Engineering console

The profile uses three connected references: terminal precision for the identity, a console dashboard for public data, and compact repository cards for the work. Charcoal surfaces, emerald signals, cyan structural lines, restrained gradients, and isometric nodes connect the graphics. These are original SVG compositions, not application screenshots or claims of production telemetry.

## Design system

- Dark canvas `#090F17`, panel `#0E1924`, elevated surface `#162B3A`, foreground `#E5EDF5`.
- Emerald `#1BE0AC` carries emphasis and data. Cyan `#65C9F3` carries structure and technology labels.
- Light variants use `#F4F8FC`, white, ink `#14293B`, and darker accents. Text colors meet a 4.5:1 contrast ratio on every defined surface.
- System sans-serif display text sits beside JetBrains Mono, Consolas, and monospace terminal labels. No font downloads are required.
- Terminal window bars, a fine grid, gradient panels, and cube motifs form the common visual vocabulary. SVG filters are confined to small decorative node highlights.
- The desktop hero is 960 × 390; the phone hero is 360 × 374. Name, role, stack, and location remain static and readable.
- Project images are individually linked and placed in a native HTML paragraph. Each uses 48% of the available content width, keeping two cards per row in a 2 × 2 gallery. Text links and expanded implementation notes provide readable alternatives to the smaller card text on phones. There are no CSS layout dependencies or HTML layout tables.
- Card summaries, technologies, and project status remain visible. Expanded notes preserve implementation details, contributions, and source links; adjacent text links provide an alternative to the image links.
- The dashboard follows the gallery. It combines four KPIs, a public-event plot, and language byte shares in a single console. On phones the panels stack. Full chart breakdowns are available in a disclosure.
- Architecture uses isometric nodes and explicit connections. The map is labeled conceptual; it is not an observed deployment or live service map.
- All graphics have dark/light and desktop/phone variants. The variants come from one renderer, rather than separately maintained artwork.

## Source and regeneration

`scripts/render_assets.py` is the SVG renderer. It uses only Python's standard library. Rebuild static artwork and the saved public dashboard snapshot:

```bash
python3 scripts/render_assets.py
```

The collector and weekly workflow are described in [dashboard.md](dashboard.md). Dashboard updates generate all chart variants from one validated public-data snapshot. The image palette and layout do not change the metric definitions. Event areas use straight segments between actual returned daily counts; no synthetic or smoothed activity is introduced. Repository stars, latency, service health, growth trends, and uptime are not invented for visual effect.

The OCR animation is an original illustration of `easy-invoice/backend/invoices/views.py`, using the same dark palette. It contains no stock media or invoice documents. To rebuild it, install Pillow in a virtual environment and run:

```bash
python3 scripts/build_animation.py
```

The 600 × 260 GIF has 40 frames at 140 ms per frame with a 48-color palette. It is opt-in through a disclosure, with a static PNG for reduced-motion preferences and a direct static link. Hero motion ends within four seconds. Reduced-motion preferences disable the trace and cursor animation. No essential information depends on animation support.

## Verification

```bash
python3 -m unittest discover -s scripts -p 'test_*.py'
git diff --check
```

Tests cover public-only collection, pagination, API caps, safe failure behavior, SVG validity, escaping, absent language data, mobile grouping, archive totals, contrast, and truthful combined-console values. Browser checks cover responsive card flow, image loading, text bounds, and reduced motion. GitHub Markdown API checks confirm sanitizer acceptance; they do not substitute for checking the published profile.

All project descriptions use public source and documentation. No unverified application footage, performance results, or private repository data is included. Normal dashboard updates require no third-party Python packages; Pillow is only used for the optional animation build.
