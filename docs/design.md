# Engineering atlas

This profile pairs technical editorial typography with abstract terrain: a reference to Kathmandu and an invitation to follow a feature through a system. The contour artwork is illustrative, not a geographic map. Project illustrations explain source structure; none are product screenshots.

## Design system

- Canvas: `#0D1117`; surface: `#161B22`; text: `#E6EDF3`.
- Blue `#58A6FF` identifies structure; cyan `#39C5CF` identifies flow.
- Light variants use `#F6F8FA`, `#FFFFFF`, and dark ink with darker accents.
- System sans-serif typography keeps identity and descriptions legible. JetBrains Mono with Consolas/monospace fallbacks carries terminal labels.
- Hero and KPI assets have dedicated mobile compositions. Project artwork is supported by normal Markdown descriptions and links, which reflow at narrow widths.
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

The GIF is 600 × 260, 40 frames at 140 ms per frame, with a 48-color palette. It appears inside an opt-in disclosure; a static PNG is selected for reduced-motion preferences where the renderer supports that media query. A direct static link remains available. The hero has restrained CSS motion and a reduced-motion rule; static rendering retains all essential information. SVG animation support depends on the image renderer and is not required to read the profile.

## Verification

```bash
python3 scripts/test_update_stats.py
python3 scripts/test_render_assets.py
git diff --check
```

Tests cover public-only collection, pagination, API caps, failed updates preserving existing files, SVG validity, escaping, empty language data, count labels, and reduced-motion styles. The charts and dashboard expose exact data in a linked JSON snapshot for readers who cannot use the visuals.

Public repository references were checked against GitHub APIs and source files. No unverified live demos, metrics, production claims, or private repository information are included. Third-party Python packages are unnecessary for the normal dashboard workflow; Pillow is only an optional artwork-generation tool.
