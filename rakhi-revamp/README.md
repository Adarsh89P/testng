# Rakhi Das — portfolio revamp

`site/` is the complete website. Copy its contents into the root of the
`rakhi-das-portfolio` GitHub Pages repository, replacing the old files, and it is live.
`previews/` holds single-file previews and screenshots for review only; do not deploy it.

## What's in `site/`

| Path | What it is |
|---|---|
| `index.html`, `assets/home.css`, `assets/home.js` | Homepage with the interactive sun/moon sky hero |
| `case-studies/*.html`, `case.css`, `case.js` | The four case studies (Healthcare, Yoga, Malta Taxi, Banking) |
| `404.html` | Not-found page; GitHub Pages serves it automatically |
| `public/` | Case-study images (PNG/JPG with WebP alongside) |
| `assets/` | Homepage images, résumé PDF, social-share images, touch icon |
| `robots.txt`, `sitemap.xml`, `.nojekyll` | Search and GitHub Pages housekeeping |

## Hero photos

The homepage hero is a real photo of Key Monastery with the Langza Buddha cut out of a second
photo and placed on the left. Both are from Unsplash (Unsplash License: free for commercial use,
no attribution required):
- Key Monastery: https://images.unsplash.com/photo-1723575409854-b8bd40109081
- Langza Buddha: https://images.unsplash.com/photo-1746036837163-4050ff8743fc

`assets/sky-mask.png` is the traced skyline; the sun, moon and stars are clipped to it.

## Deploying

1. In the portfolio repo, delete the old `index.html`, `css/`, `js/`, `case-studies/` and `public/` (keep `.git`).
2. Copy everything from `site/` (including the hidden `.nojekyll`) into the repo root.
3. Commit and push to the branch GitHub Pages publishes from.

All links are relative, so the site also works from any other host or folder.
Two things assume the current address, `https://rakhidas25.github.io/rakhi-das-portfolio/`:
the canonical/social-share URLs in each page's `<head>` plus `robots.txt` and `sitemap.xml`,
and the two links in `404.html`. Update those if the address changes (for example on Vercel).

## Editing

- Homepage text lives in `site/index.html`.
- The four case studies share one template. Their content lives in `tools/build_case_studies.py`
  (the `CONTENT` block); edit it there and run `python3 tools/build_case_studies.py` to rebuild
  `site/case-studies/*.html`. Keep each page to about a three-minute read.
- Previewing a time of day on the homepage: `index.html?t=21` (night), `?t=17.3` (golden hour).
- Day/night choice is remembered across pages (`localStorage` key `rk-theme`).

## Checks run before handoff

- axe-core (WCAG 2 A/AA + best practice) on all six pages, light and dark: no violations.
- Every internal link and `#anchor` resolves.
- No console errors; no horizontal scroll at 390px and 1440px.

## Open content items for Rakhi

- Malta Taxi: research method, map/fare/tour screens, any measured results.
- Banking: context and problem detail from the deck, onboarding screen exports, app typeface, delivery scale.
- LinkedIn: the old case studies linked `rakhi-das-19a03b1b4`, the homepage `rakhi-das-183381158`. The new site uses the latter everywhere; confirm it.
