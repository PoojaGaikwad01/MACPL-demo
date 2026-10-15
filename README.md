# MACPL Website — v2 (multipage)

Static site (HTML + CSS + vanilla JS). No build step, no dependencies.
Open `index.html` in a browser, or upload the whole folder to any web host.
To preview locally with working links: `python -m http.server 8000`, then open http://localhost:8000.

## Pages
| File | Content |
|---|---|
| `index.html` | Home: hero with photo, key facts, vision and tagline, process and product-segment cards, enquiry band |
| `about.html` | Left sub-menu tabs, one section shown at a time (`about.html#values` etc.): Overview, Vision, Values, Management, Strengths, Policies, Financials |
| `processes.html` | Process tabs (the Home cards open a given process) |
| `products.html` | Product gallery grouped by segment, with filter (the Home cards open a given segment) |
| `quality.html` | TPM parameters, quality policy, ISO certifications, integrated management policy |
| `news.html` | News and events (ISO 9001 / 14001 / OHSAS 18001 certification) |
| `group.html` | Brand essence, the rising sun, the visionary, group companies |
| `careers.html` | Working at MACPL, who we hire and openings, online application form |
| `contact.html` | Contact details (English and Marathi), map and enquiry form |
| `sitemap.html` | Every page and section |
| `search.html` | Site search results (`search.html?q=...`), searched in the browser |

## Shared header and footer
The header and footer are repeated in every page (no build step). Edit them in `tools/sync_layout.py`, then run `python tools/sync_layout.py` from the site root to write them into all pages. It also marks the current page with `aria-current="page"` and writes the font links into each `<head>`. New pages must be added to `PAGES` (and `NAV`, if they belong in the menu).

## Structure
- `*.html` — page markup and SEO meta (each page has its own title and description; schema.org data on Home and Contact)
- `assets/css/style.css` — brand tokens (top of file) and all styles
- `assets/js/main.js` — content data (processes, segments, products, search index), mobile menu, home cards, process tabs, product gallery, forms, About sub-menu, site search
- `assets/fonts/` — Sansation 400/700 (corporate typeface, SIL Open Font License, from Fontsource)
- `assets/images/` — AITG–MACPL logo (`macpl-logo.png`), white-background version (`macpl-logo-white.png`), favicon cut from it (`favicon.png`), AI stand-in photos (`photos/`) and SVG illustrations
- `tools/sync_layout.py` — writes the shared header, footer and font links into every page
- `tools/gen_images.py` — regenerates the stand-in SVG illustrations

## Before launch
1. **Logo** — the header and footer use `assets/images/macpl-logo-white.png`, the white-background version of the AITG–MACPL lockup (blue lettering, sun unchanged), generated from the original `macpl-logo.png` (419×58 px, on brand blue). The footer shows it on a white panel. On desktop it shows at its full 58 px height, above the manual's 55 px digital minimum (p.15). On phones it has to shrink to fit (about 40 px tall at 390 px wide), and the PNG is soft on high-density screens: replace it with the SVG master artwork from the brand custodian at the same path, and regenerate `favicon.png` from it (manual p.12/20: never redraw the logo).
2. **Photos** — products, processes, the About shop floor and the Careers team use AI-generated stand-in photos (`assets/images/photos/`). They are not MACPL's real parts or plants: replace them with real photography before launch (products & processes via `image:` paths in `main.js`, About/Careers via the inline `background-image` in `index.html` and `careers.html`). The two founder portraits are still placeholders. The ISO news article on the current site has photos: add them to `news.html`.
3. **Email** — replace `[sales email address]` in `contact.html` and `[careers email address]` in `careers.html`.
4. **Forms** — add `data-endpoint="..."` on `<form id="enquiry">` in `contact.html` and on `<form id="apply-form">` in `careers.html` (Formspree, PHP mailer, etc.; the application form sends a file upload). Without it the forms only show the confirmation.
5. **Social links** — the footer strip has a slot for "Follow us on" (manual p.35). Add the official profile links in `tools/sync_layout.py` once confirmed.
6. **Certifications** — the site states ISO 9001, ISO 14001 and OHSAS 18001 as on the current site. OHSAS 18001 was replaced by ISO 45001 in 2021: confirm the current certificates and add download links in `quality.html`.
7. **Group companies** — `group.html` merges the current site's list with the brand manual's (Dhruv Coatings, Umasons Steel Fab). Confirm the list and add each company's division logo if wanted.
8. **Careers** — list current openings in `careers.html`.
9. **Marathi** — the company name and address appear in Devanagari (Noto Sans Devanagari on screen; the manual's Shree-Dev-1097 is for print). A full Marathi version of the site needs a translator.

## Brand rules applied (AITG Brand Identity Guidelines)
- Colours: blue #004282 (Pantone 287C) and the six sun hues #ED1B2F → #FFCC32 only; text in Black 80% / 70%. Text on the sun hues is near-black for contrast.
- Type: Sansation for headings (corporate typeface), Trebuchet MS for body (electronic typeface).
- Logo: master PNG only, never redrawn; minimum 55 px tall on desktop; on brand blue with a white logotype.
- Visual language: circle cut by a 60° diagonal (Group page), orange crescent and curved edge on page heroes (layout p.24), orange→blue diagonal bars, slash separators in the menu, orange icon discs in the footer.
- Content: vision statement, six values with their word-marks, "Honest Business With Honest Relationships", the rising sun's meaning, the group's visionary.
- Pages are kept short (minimum scroll): inner-page headers share one fixed height (250 px).
- Page addresses stay plain (`about.html`, never `about.html#management`): tabs switch in place, and links that open a given tab use `data-open` (kept for one page load in sessionStorage).
- Reduced-motion preference is respected.
