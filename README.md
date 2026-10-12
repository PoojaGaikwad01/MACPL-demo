# MACPL Website — v2 (multipage)

Static site (HTML + CSS + vanilla JS). No build step, no dependencies.
Open `index.html` in a browser, or upload the whole folder to any web host.
To preview locally with working links: `python -m http.server 8000`, then open http://localhost:8000.

## Pages
| File | Content |
|---|---|
| `index.html` | Home: hero, key facts, short story, process and product-segment cards, quality and careers teasers |
| `about.html` | Our story, milestones, leadership (`#leadership`) |
| `processes.html` | Process tabs; `processes.html#bend` etc. opens a given process |
| `products.html` | Filterable product grid; `products.html?seg=earth` opens a given segment |
| `quality.html` | TPM parameters, quality policy, certifications |
| `group.html` | Group companies and values |
| `careers.html` | Who we hire, why MACPL, current openings (`#openings`) |
| `contact.html` | Contact details and enquiry form |

The header and footer are repeated in every page (no build step). When you change a menu link or footer link, change it in all eight files. The current page is marked with `aria-current="page"` on its menu link.

## Structure
- `*.html` — page markup and SEO meta (each page has its own title and description; schema.org data on Home and Contact)
- `assets/css/style.css` — brand tokens (top of file) and all styles
- `assets/js/main.js` — content data (processes, segments, products), mobile menu, home cards, process tabs, product filter, enquiry form
- `assets/images/` — logo mark, AI stand-in photos (`photos/`) and SVG illustrations
- `tools/gen_images.py` — regenerates the stand-in SVG illustrations

## Before launch
1. **Logo** — replace the header lockup with master AITG–MACPL artwork (brand manual p.12/20: never redraw the logo).
2. **Font** — the manual specifies Sansation. Add its licensed webfont with `@font-face` in style.css; it is already first in `--head`. Saira is the fallback.
3. **Photos** — products, processes, the About shop floor and the Careers team use AI-generated stand-in photos (`assets/images/photos/`, made with Figma AI). They are not MACPL's real parts or plants: replace them with real photography before launch (products & processes via `image:` paths in `main.js`, About/Careers via the inline `background-image` in `index.html`, `about.html` and `careers.html`). Earlier SVG illustrations are kept in `assets/images/processes|products|sections/` (regenerate with `python tools/gen_images.py .`). The two founder portraits are still placeholders and need real photos.
4. **Email** — replace `[sales email address]` in `contact.html` and `[careers email address]` in `careers.html`.
5. **Form** — add `data-endpoint="..."` on `<form id="enquiry">` in `contact.html` (Formspree, PHP mailer, etc.). Without it the form only shows the confirmation.
6. **Certifications** — fill the Certifications block in `quality.html`.
7. **Careers** — list current openings in `careers.html`, and check the role descriptions under "Who we hire".

## Brand rules applied
Blue #004282 (Pantone 287C), six sun hues #ED1B2F → #FFCC32, Trebuchet MS for body (electronic typeface), 60° diagonal from the "A", orange→blue footer bar. Reduced-motion preference is respected.
