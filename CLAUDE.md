# Platformday — project overview for Claude Code

## What this is
A static site generator for the Platformday conference series (platform engineering,
developer experience, infrastructure). Each event is a separate folder
(e.g. `2026-london-q1/`). Python + Jinja2 renders HTML into a `static/` subfolder per event.

The repo was scaffolded from the `devopsnotdead` template and currently has
**no events yet** — only `_event_template/` and the home page.

## How to build

```bash
make env && source env/bin/activate
make deps
make            # builds home + every 20* event folder into ./static
make serve      # http://localhost:8080
```

Build one event:
```bash
cd 2026-london-q1
make generate
```

Output lands in `<event>/static/`, then the top-level Makefile assembles
everything into the root `static/` — that's the deployable folder
(GitHub Actions pushes it to the `gh-pages` branch).

## Folder structure

```
_event_template/        ← master template — changes here propagate to all events
  _build/generate.py    ← the build script
  _templates/           ← Jinja2 HTML templates
  metadata.yml          ← per-event config, copied and edited per event

_assets/template_v1/    ← shared CSS, JS, images for EVENT pages
home/template/          ← shared CSS, JS, images for the HOME page (separate copy!)

home/metadata.yml       ← single source of truth for the events list
home/_db/               ← testimonials.csv, ambassadors.csv
sponsorship.yaml        ← pricing tiers definition

photos/                 ← hero images (referenced as ../photos/... from events)
speakers/               ← speaker headshots
sponsors/               ← sponsor logos
ambassadors/            ← ambassador headshots
```

## The golden rule
**Always edit `_event_template/` first, then copy to all event folders.**

There are no event folders yet. Once there are, propagate with `sync.sh`:
```bash
find . -name "2026-*" -maxdepth 1 -exec ./sync.sh {} \;
```
`sync.sh` deliberately excludes `_db/`, `assets/`, `_templates/venue.html`
and `metadata.yml` — those are per-event.

## Theme / palette

Platformday's palette is orange on black, matching the brand logo and the
PLATFORMday swatch (`--host-orange: #E2971D`) on the sister sites' `/host` pages:

- `$theme-color-primary: #E2971D`
- `$theme-color-secondary: #B45309` (burnt amber — used where white text sits on it)
- `$theme-bg-light: #FDF3E0`
- `$theme-border-color: #F8DFAE`
- Primary-as-text spots use the darker `#BA7B12` for contrast on white.

**The palette is defined in two places that must stay in sync:**
`_assets/template_v1/assets/scss/theme.scss` (events) and
`home/template/assets/scss/theme.scss` (home).

`theme.css` is compiled SCSS **plus hand-written rules appended after** the
compiled output (1 extra line for `_assets`, 2 for `home/template`). Preserve
that tail when recompiling — see the "Theme colours" section of `README.md`
for the exact commands, and use `_build/normalize_css_colors.py` afterwards to
convert modern dart-sass's fractional `rgb()` output back to hex.

A handful of palette hexes are also inlined directly in templates
(`_event_template/_templates/index.html`, `home/_templates/index.html`,
`home/_templates/meetup_base.html`) — grep for the hex values when changing colours.

## Outstanding brand TODOs
- `photos/platformday-hero-*.jpg` are the generic template hero photos.
- `_event_template/_templates/sponsorship.html` uses a CSS gradient where the
  sister sites use a painted hero image (`../photos/<brand>-paint.png`), and its
  brand video element was removed. Both are marked with `TODO` comments.
- The audience stats in `sponsorship.html` are series-wide figures inherited from
  the template, not Platformday-specific.

## Sister repos
Same structure: `sreday`, `llmday`, `devopsnotdead` (all under `~/github/`, and
symlinked together in `~/github/trinity/`). Changes to shared templates or build
logic often need applying to all of them.

## Dependencies
```bash
pip install -r _build/requirements.txt   # jinja2, pyyaml, jinja-markdown, python-dateutil, Pillow
```
Building the CSS additionally needs `sass` on PATH (dart-sass).
