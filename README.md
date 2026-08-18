# Platformday

In-person conferences for platform engineering, developer experience & infrastructure.


## Running locally

```sh
# if needed
make env
source env/bin/activate

make deps

# builds all years
make

# runs a small script to serve the pages with python
make serve
```

## Adding a new conference

1. Copy over the template (`_event_template`) to a new folder
    1. The name needs to follow the pattern `YYYY-location-qX`
    1. Let's say we add `2026-tokyo-q1`
1. Modify the `2026-tokyo-q1/metadata.yml` file:
    1. Update the location, time, date
    1. Update the `2026-tokyo-q1/_db/talks.csv` file
1. Update the venue info
    1. Modify the address in `2026-tokyo-q1/_templates/venue.html`
    1. Upload/copy the 3 venue photos to `2026-tokyo-q1/assets/images/venue`
1. Update the luma event
    1. Don't change the embeds in `2026-tokyo-q1/_templates/tickets.html`
    1. Change the `luma_evt` field in `home/metadata.yml`
1. Update the hero pictures
    1. Add the pictures to `photos`
    1. List the relevant ones in `2026-tokyo-q1/metadata.yml`
1. Add the conference to the home page
    1. Upload the splash screen
        1. Put it in `assets/images/events/platformday-2026-tokyo-q1.jpeg`
    1. Modify the `home/metadata.yml` file:
        1. Add a new item to the events list
        1. Make sure the url matches the format, e.g `2026-tokyo-q1`
        1. The `photo_url` card image doubles as the social link preview (og:image) for all of that event's pages; until it is uploaded, the build warns and falls back to the default hero photo

```yaml
events:

  - name: Platformday Tokyo 2026 Q1
    location: Tokyo, Japan
    photo_url: ./assets/images/events/platformday-2026-tokyo-q1.jpeg
    url: ./2026-tokyo-q1/
...
```

## Theme colours

Platformday uses an orange-on-black palette, shared with the PLATFORMday host
tiles on the sister sites (`--host-orange` in their `home/_templates/host.html`):

| Token | Value |
| --- | --- |
| `$theme-color-primary` | `#E2971D` (brand orange) |
| `$theme-color-secondary` | `#B45309` (burnt amber, buttons on white) |
| `$theme-bg-light` | `#FDF3E0` |
| `$theme-border-color` | `#F8DFAE` |

The palette lives in **two** SCSS trees that must be kept in sync:

- `_assets/template_v1/assets/scss/theme.scss` — used by event pages
- `home/template/assets/scss/theme.scss` — used by the home page

To change a colour, edit both `theme.scss` files and rebuild the CSS:

```sh
# event pages
cd _assets/template_v1/assets/scss
tail -n 1 ../css/theme.css > /tmp/tail.css          # preserve hand-written rules
sass --style=compressed --no-source-map theme.scss /tmp/new.css
cat /tmp/new.css /tmp/tail.css > ../css/theme.css

# home page (preserves the last TWO lines)
cd home/template/assets/scss
tail -n 2 ../css/theme.css > /tmp/tail.css
sass --style=compressed --no-source-map theme.scss /tmp/new.css
cat /tmp/new.css /tmp/tail.css > ../css/theme.css

# normalize fractional rgb() from modern dart-sass back to hex
python _build/normalize_css_colors.py \
  _assets/template_v1/assets/css/theme.css \
  home/template/assets/css/theme.css
```

Note that `theme.css` carries a small number of hand-written rules appended
*after* the compiled output — that is why the tail is preserved above rather
than simply overwriting the file.

## Home-page sponsor vs partner carousels

The main website's two logo carousels are categorized via `partners.yaml` at the
repo root (home page only - conference pages are unaffected):

- **Paying sponsor**: drop the logo file into `sponsors/` - it shows up in the
  home Sponsor carousel automatically.
- **Partner** (community meetup, media/non-sponsor org, sister conference, job
  board): drop the logo into `sponsors/` AND add its filename to the right list
  in `partners.yaml` - it shows up in the Partner carousel instead.
- **Duplicates**: if a company has more than one logo file, list the extra
  variants under `hidden_duplicates` so it only appears once on the home page.
