# From the interface down

This profile follows one path from a user interaction to application logic and the system underneath. Abstract contour lines reference Kathmandu without pretending to be a geographic map. The terminal, project diagrams, charts, and architecture share the same surfaces, blue structural lines, and cyan flow accents. Project illustrations explain source structure; none are product screenshots.

## Design system

- Canvas: `#0D1117`; surface: `#161B22`; text: `#E6EDF3`.
- Blue `#58A6FF` identifies structure; cyan `#39C5CF` identifies flow.
- Light variants use `#F6F8FA`, `#FFFFFF`, and dark ink with darker accents.
- System sans-serif typography keeps identity and descriptions legible. JetBrains Mono with Consolas/monospace fallbacks carries terminal labels.
- The desktop hero is 960 × 330; the phone composition is 360 × 330. The name remains prominent in both layouts.
- Hero, KPI, project, architecture, and chart assets have dedicated mobile compositions. Normal Markdown carries the project descriptions, technology lists, and source links.
- The flagship Code Shell cover has a taller terminal diagram. Other covers show different source structures: invoice-to-fields processing, storefront/API boundaries, and GTK/daemon/runtime/Wine layers.
- KPI graphics use four cards on desktop and two columns on phones. Numbers are snapshots, with no invented trend indicators.
- The activity chart uses scaled daily bars on desktop and labeled seven-day groups on phones. Grouping preserves all returned events. Language shares use the same data in both layouts.
- The repository creation-year chart is available in a disclosure to keep the primary project gallery and charts prominent.
- GitHub-compatible `picture`, `source`, `img`, links, and `details` provide presentation without scripts, custom page styles, or HTML layout tables.

## Source and regeneration

`scripts/render_assets.py` contains the small SVG renderer and static artwork. It uses the Python standard library. Rebuild artwork and render the saved dashboard snapshot:

```bash
python3 scripts/render_assets.py
```

The GitHub API collector, metric definitions, failure behavior, and weekly schedule are documented in [dashboard.md](dashboard.md). The old contribution snake workflow has been replaced by this public-data pipeline; its output branch is no longer referenced.

The original OCR animation is an illustration of `easy-invoice/backend/invoices/views.py`. It uses no stock media, invoice documents, or third-party artwork. To regenerate it, install Pillow in a virtual environment and run:

```bash
python3 scripts/build_animation.py
```

The GIF is 600 × 260, 40 frames at 140 ms per frame, with a 48-color palette. It appears inside an opt-in disclosure; a static PNG is selected for reduced-motion preferences where the renderer supports that media query. A direct static link remains available. Hero motion finishes within four seconds: one signal trace and two slow cursor pulses. Reduced-motion preferences disable both. Static rendering retains all essential information. SVG animation support depends on the image renderer and is not required to read the profile. Other SVGs are static.

## Verification

```bash
python3 scripts/test_update_stats.py
python3 scripts/test_render_assets.py
git diff --check
```

Tests cover public-only collection, pagination, API caps, failed updates preserving existing files, SVG validity, escaping, empty language data, count labels, reduced-motion styles, mobile event grouping at date boundaries, and creation-year totals excluding forks. The charts and dashboard expose exact data in a linked JSON snapshot for readers who cannot use the visuals.

Public repository references were checked against GitHub APIs and source files. No unverified live demos, metrics, production claims, or private repository information are included. Third-party Python packages are unnecessary for the normal dashboard workflow; Pillow is only an optional artwork-generation tool.
