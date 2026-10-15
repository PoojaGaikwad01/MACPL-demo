"""Write the shared header, footer and font links into every page.

The site has no build step, so the header and footer are repeated in each
HTML file. Edit them here, then run from the site root:

    python tools/sync_layout.py
"""
import re
from pathlib import Path

PAGES = ['index', 'about', 'processes', 'products', 'quality', 'news',
         'group', 'careers', 'contact', 'sitemap', 'search']
NAV = [('index', 'Home'), ('about', 'About'), ('processes', 'Processes'),
       ('products', 'Products'), ('quality', 'Quality'), ('news', 'News'),
       ('group', 'The Group'), ('careers', 'Careers'), ('contact', 'Contact')]

SEARCH_ICON = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
               'stroke-width="2.4" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg>')

FONTS = ('<link rel="preload" href="assets/fonts/sansation-latin-700.woff2" as="font" type="font/woff2" crossorigin>\n'
         '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;600&amp;display=swap">\n')


def search_form(suffix):
    return (f'<form class="search" action="search.html" role="search">'
            f'<label class="sr" for="q{suffix}">Search the site</label>'
            f'<input id="q{suffix}" name="q" type="search" placeholder="Search">'
            f'<button type="submit" aria-label="Search">{SEARCH_ICON}</button></form>')


def header(page):
    current = ' aria-current="page"'
    links = '\n'.join(
        f'      <a class="navlink" href="{p}.html"{current if p == page else ""}>{label}</a>'
        for p, label in NAV)
    return f'''<header class="site-header">
  <div class="masthead">
    <div class="wrap">
      <a class="brand" href="index.html">
        <!-- AITG–MACPL logo: replace with the master artwork (SVG) from the brand custodian; never redraw it (manual p.12) -->
        <img class="brand-logo" src="assets/images/macpl-logo.png" width="419" height="58" alt="AITG Marathwada Auto Compo Pvt Ltd, home">
      </a>
      {search_form('')}
      <button class="menu-btn" aria-label="Open menu" aria-expanded="false" aria-controls="site-nav">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
      </button>
    </div>
  </div>
  <div class="navbar">
    <div class="wrap">
    <nav id="site-nav" class="nav" aria-label="Main">
{links}
      <a class="btn btn-sun nav-cta" href="contact.html">Request a quote</a>
      {search_form('-m')}
    </nav>
    </div>
  </div>
</header>'''


FOOTER = '''<footer class="site-footer">
  <div class="foot-strip">
    <div class="wrap">
      <a class="fs-contact" href="contact.html"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="5" width="18" height="14"/><path d="m3 6 9 7 9-7"/></svg>Contact us</a>
      <a class="fs-map" href="sitemap.html"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="9" y="3" width="6" height="5"/><rect x="2" y="16" width="6" height="5"/><rect x="16" y="16" width="6" height="5"/><path d="M12 8v4M5 16v-4h14v4"/></svg>Sitemap</a>
      <p class="fs-tag">Honest Business With Honest Relationships</p>
      <!-- "Follow us on" (manual p.35): add official social profile links here once confirmed -->
    </div>
  </div>
  <div class="wrap foot">
    <div class="foot-about">
      <a class="brand" href="index.html">
        <img class="brand-logo" src="assets/images/macpl-logo.png" width="419" height="58" alt="AITG Marathwada Auto Compo Pvt Ltd, home">
      </a>
      <p class="mr" lang="mr">मराठवाडा ऑटो कॉम्पो प्रायव्हेट लिमिटेड</p>
      <p>Customized, durable and critical auto components. A company of Applied Innovation &amp; Technology Group.</p>
      <ul class="foot-contact">
        <li><span class="ico"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M12 22s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg></span><span>E-63, MIDC Waluj, Aurangabad 431136, Maharashtra, India</span></li>
        <li><span class="ico"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg></span><span><a href="tel:+912406625613">+91 240 6625613</a> / <a href="tel:+912406625614">4</a></span></li>
      </ul>
    </div>
    <div class="col"><h2>Company</h2><a href="about.html">About</a><a href="about.html#management">Management</a><a href="group.html">The Group</a><a href="news.html">News</a><a href="careers.html">Careers</a></div>
    <div class="col"><h2>Capability</h2><a href="processes.html">Processes</a><a href="products.html">Products</a><a href="quality.html">Quality</a><a href="contact.html">Contact</a></div>
    <div class="col"><h2>Documents</h2><a href="https://www.macpl-aitg.co/images/financials/MACPL-Annual-Return-2021-2022.pdf">Annual return 2021–22 <em>PDF</em></a><a href="https://www.macpl-aitg.co/images/financials/MACPL-CSR-Policy-2022.pdf">CSR policy <em>PDF</em></a><a href="sitemap.html">Sitemap</a></div>
  </div>
  <div class="wrap legal">
    <span>© <span id="year">2026</span> Marathwada Auto Compo Pvt. Ltd. All rights reserved.</span>
    <span>CIN U29130MH1988PTC046951</span>
    <a class="to-top" href="#" aria-label="Back to top" title="Back to top"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg></a>
  </div>
</footer>'''


def main():
    root = Path(__file__).resolve().parent.parent
    for page in PAGES:
        path = root / f'{page}.html'
        html = path.read_text(encoding='utf-8')
        html = re.sub(r'<header class="site-header">.*?</header>', lambda m: header(page), html, count=1, flags=re.S)
        html = re.sub(r'<footer class="site-footer">.*?</footer>', lambda m: FOOTER, html, count=1, flags=re.S)
        # fonts: everything between the favicon link and the stylesheet link
        html = re.sub(r'(<link rel="icon"[^>]*>\n).*?(<link rel="stylesheet" href="assets/css/style.css">)',
                      lambda m: m.group(1) + FONTS + m.group(2), html, count=1, flags=re.S)
        path.write_text(html, encoding='utf-8', newline='\n')
        print('updated', path.name)


if __name__ == '__main__':
    main()
