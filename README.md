# MACPL Website — Homepage v1

Static site (HTML + CSS + vanilla JS). No build step, no dependencies.
Open `index.html` in a browser, or upload the whole folder to any web host.

## Structure
- `index.html` — page markup and SEO meta / schema.org data
- `assets/css/style.css` — brand tokens (top of file) and all styles
- `assets/js/main.js` — mobile menu, process tabs, product filter, enquiry form
- `assets/images/` — put photos here

## Before launch
1. **Logo** — replace the header lockup with master AITG–MACPL artwork (brand manual p.12/20: never redraw the logo).
2. **Font** — the manual specifies Sansation. Add its licensed webfont with `@font-face` in style.css; it is already first in `--head`. Saira is the fallback.
3. **Photos** — swap `.ph` placeholders for real images. Products & processes: set `image:` paths in `main.js`.
4. **Email** — replace `[sales email address]` in the Contact section.
5. **Form** — add `data-endpoint="..."` on `<form id="enquiry">` (Formspree, PHP mailer, etc.). Without it the form only shows the confirmation.
6. **Certifications** — fill the Certifications tile in the Quality section.

## Brand rules applied
Blue #004282 (Pantone 287C), six sun hues #ED1B2F → #FFCC32, Trebuchet MS for body (electronic typeface), 60° diagonal from the "A", orange→blue footer bar. Reduced-motion preference is respected.
