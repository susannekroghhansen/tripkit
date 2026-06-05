# Tripkit

**Pack smart, travel light.** A single-page web app that builds a packing list
tailored to your trip — travel style, who's coming (and pets), destination,
dates, activities and luggage — with live weather, a luggage-fit gauge, a
capsule-wardrobe coach, and country-aware reminders (entry authorisations,
plug types). Works offline and installs to your phone's home screen.

Everything lives in one `index.html` (HTML + CSS + JavaScript, no build step).
Your trips and lists are saved in the browser on your device — there is no
account and no server-side storage.

## Live site

https://tripkit.krogh-hansen.net

## Files

| File | What it is |
|------|------------|
| `index.html` | The whole app. |
| `manifest.json` | Makes it installable (name, icons, colours). |
| `sw.js` | Service worker — offline caching and update control. |
| `icons/` | App icons (192, 512, maskable, apple-touch). |
| `CNAME` | Tells GitHub Pages the custom domain. |
| `make_icons.py` | Regenerates the icons (needs Pillow). Not served. |

## Hosting

Served by **GitHub Pages** at the custom domain `tripkit.krogh-hansen.net`.
Push to the default branch and GitHub Pages redeploys automatically.

## Publishing an update

1. Edit `index.html` (or other files).
2. **Bump the cache version** in `sw.js`: change `const CACHE = "tripkit-v1"`
   to `"tripkit-v2"`, etc. This is what forces returning visitors to pick up
   the new version instead of an old cached copy.
3. Add an entry to the changelog below.
4. Commit with a clear message and push.

## Changelog

### v1 — 2026-06-05
- First hosted release as an installable PWA.
- Questionnaire, rules engine, per-person (Group/Family) and pet sections.
- Live weather with seasonal fallback; luggage-fit gauge with sized bags.
- Capsule coach, saved lists, section toggles, "your items win" de-duplication.
- Country-aware reminders: entry authorisations and plug/adapter types.
