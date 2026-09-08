# PLATFORMday

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

  - name: PLATFORMday Tokyo 2026 Q1
    location: Tokyo, Japan
    photo_url: ./assets/images/events/platformday-2026-tokyo-q1.jpeg
    url: ./2026-tokyo-q1/
...
```

## Theme colours

PLATFORMday uses an orange-on-black palette, shared with the PLATFORMday host
tiles on the sister sites (`--host-orange` in their `home/_templates/host.html`):

| Token | Value |
| --- | --- |
| `$theme-color-primary` | `#E2971D` (brand orange) |
| `$theme-color-secondary` | `#B45309` (burnt amber, buttons on white) |
| `$theme-bg-light` | `#FDF3E0` |
| `$theme-border-color` | `#F8DFAE` |

The palette lives in ONE SCSS tree, shared by the home page and the event pages
(the home page used to have its own copy under `home/template/assets`; removed 2026-09-08):

- `_assets/template_v1/assets/scss/theme.scss` -> compiled to `_assets/template_v1/assets/css/theme.css`

`theme.css` = compiled SCSS (the first 12 lines: Bootstrap/DevConf banners + two long compiled lines)
**plus hand-written rules appended after it** (line 13 onwards: hero social pill, hero CTA row,
button colours, header/schedule tweaks, home hover effects). To change a colour, edit `theme.scss`,
recompile, and keep the hand-written tail:

```sh
cd _assets/template_v1/assets/scss
tail -n +13 ../css/theme.css > /tmp/tail.css          # hand-written rules, keep them
sass --style=compressed --no-source-map theme.scss /tmp/new.css
cat /tmp/new.css /tmp/tail.css > ../css/theme.css

# normalize fractional rgb() from modern dart-sass back to hex
python _build/normalize_css_colors.py _assets/template_v1/assets/css/theme.css
```

Check `head -12 ../css/theme.css` still ends with the compiled `*/body{...}` line before relying on
`tail -n +13`; if the compiled banner ever changes length, adjust the line number.

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

## Sponsor lead form

The home page `#sponsor` section has an "Email us" expandable form under the Calendly widget
(`home/_templates/index.html`). It posts JSON to a Google Apps Script web app whose source lives in
`_build/lead-form.gs` (kept in the llmday repo; one deployment serves all brands); the script emails `hello@platformday.com` **and** the sponsor in one message
(from `mark@llmday.com`) so the thread is open for both sides immediately.

- The deployed `/exec` URL lives in `home/metadata.yml` -> `lead_form_url`. When it is empty the form
  falls back to a prefilled `mailto:` link, so the UI can ship before the script is deployed.
- Deploy / re-deploy steps are in the header comment of `_build/lead-form.gs` (kept in the llmday repo; one deployment serves all brands) (Web app, Execute as: Me,
  Who has access: Anyone). Editing the script needs a new deployment *version*; the URL stays the same.
- Same deployment can serve sreday/platformday: the form sends `brand`, the script maps it to inbox + alias.
- The email lists `Form sent from: <page URL>` (home page -> `https://platformday.com/`, event page -> its folder URL).
- Event pages (event index + talk pages) use the same form as the "Become A Sponsor" pill via
  `_event_template/_templates/_lead_form.html` (propagated into every `20*/_templates/`); the event build
  reads `lead_form_url` from `home/metadata.yml`. That partial is a deliberate COPY of the home-page block in
  `home/_templates/index.html` (label, pill colour, card border and navbar hash differ) - when changing fields
  or copy, edit both, then propagate the partial to all event folders.
- Brand colours come from the single `.lead-scope { --lead-accent ... }` line at the top of each form block;
  the rest of the block/partial is byte-identical to llmday's. Sync from llmday when the form changes.
