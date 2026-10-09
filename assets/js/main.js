/* MACPL website — interactions (no dependencies) */
(function () {
  'use strict';
  var HUES = ['#ED1B2F', '#F15A31', '#F47932', '#F79433', '#FBB034', '#FFCC32'];

  /* ---- Content: edit here ---- */
  var PROCESSES = [
    { id: 'cut', name: 'Plasma cutting', body: 'CNC plasma cutting turns plate into accurate blanks for frames, links and brackets, ready for forming and welding with minimal rework.', tags: ['CNC profile cutting', 'Plate blanks', 'Heavy fabrication'], image: 'assets/images/photos/processes/plasma-cutting.jpg', video: 'https://www.youtube.com/watch?v=vPwjm4bx5XY' },
    { id: 'bend', name: 'Tube bending', body: 'A CNC cold tube bender and a robotic hot-bending cell each run more than 2,000 parts a day. Bending well takes metallurgy as much as machinery, and we have both.', tags: ['CNC cold bending', 'Robotic hot bending', '2,000+ parts/day each'], image: 'assets/images/photos/processes/tube-bending.jpg', video: 'https://www.youtube.com/watch?v=7Ba8KVW0Pok' },
    { id: 'weld', name: 'Welding', body: 'Skilled welders and robotic cells hold process parameters tight, so every joint on a steering column or fork is as strong as the design demands.', tags: ['Robotic welding', 'MIG / TIG', 'Fixture-controlled'], image: 'assets/images/photos/processes/welding.jpg', video: '' },
    { id: 'heat', name: 'Heat treatment', body: 'We design and build our own furnaces. Strictly controlled parameters give the exact microstructure needed, stress-relieved and normalised, batch after batch.', tags: ['In-house furnaces', 'Stress relieving', 'Normalising'], image: 'assets/images/photos/processes/heat-treatment.jpg', video: 'https://www.youtube.com/watch?v=NaewbxKqvD0' },
    { id: 'cast', name: 'Aluminium casting', body: 'Gravity die casting with alloy made in-house, which cuts material cost substantially. Tight process control delivers castings without blow holes.', tags: ['Gravity die casting', 'In-house alloy', 'Zero blow-hole target'], image: 'assets/images/photos/processes/aluminium-casting.jpg', video: 'https://www.youtube.com/watch?v=sTr3GobQtg8' },
    { id: 'coat', name: 'Surface finish', body: 'Surface treatment and powder coating protect parts such as under-bracket assemblies against corrosion and wear in the field.', tags: ['Pre-treatment', 'Powder coating', 'Corrosion protection'], image: 'assets/images/photos/processes/surface-finish.jpg', video: '' }
  ];

  var SEGMENTS = [
    { id: 'all', label: 'All products' },
    { id: 'two', label: 'Two-wheeler & EV' },
    { id: 'three', label: 'Three-wheeler & EV' },
    { id: 'earth', label: 'Earth-moving' },
    { id: 'agri', label: 'Agriculture' }
  ];

  /* image: path like 'assets/images/products/bucket-link.jpg' — leave '' for placeholder */
  var PRODUCTS = [
    { seg: 'two', segment: 'Two-wheeler', name: 'Under-bracket assembly', note: 'Powder-coated, for motorcycle front suspension forks.', image: 'assets/images/photos/products/under-bracket.jpg' },
    { seg: 'two', segment: 'Two-wheeler EV', name: 'Telescopic suspension fork, Ø30 mm', note: 'For electric two-wheelers, disc-brake version.', image: 'assets/images/photos/products/fork-2w-disc.jpg' },
    { seg: 'two', segment: 'Two-wheeler EV', name: 'Telescopic suspension fork, Ø30 mm', note: 'For electric two-wheelers, drum-brake version.', image: 'assets/images/photos/products/fork-2w-drum.jpg' },
    { seg: 'three', segment: 'Three-wheeler', name: 'Steering column, cargo', note: 'For three-wheel cargo vehicles.', image: 'assets/images/photos/products/steering-column-cargo.jpg' },
    { seg: 'three', segment: 'Three-wheeler', name: 'Steering column, passenger', note: 'For three-wheel passenger vehicles.', image: 'assets/images/photos/products/steering-column-passenger.jpg' },
    { seg: 'three', segment: 'Three-wheeler', name: 'Front fork, cargo', note: 'For three-wheel cargo vehicles.', image: 'assets/images/photos/products/front-fork-cargo.jpg' },
    { seg: 'three', segment: 'Three-wheeler EV', name: 'Telescopic suspension fork, Ø41 mm', note: 'Rated for a 700 kg transport payload.', image: 'assets/images/photos/products/fork-3w-41.jpg' },
    { seg: 'three', segment: 'Three-wheeler EV', name: 'Telescopic suspension fork, Ø30 mm', note: 'Rated for a 680 kg transport payload.', image: 'assets/images/photos/products/fork-3w-30.jpg' },
    { seg: 'earth', segment: 'Earth-moving', name: 'Bucket link', note: 'For excavators.', image: 'assets/images/photos/products/bucket-link.jpg' },
    { seg: 'earth', segment: 'Earth-moving', name: 'Link arm', note: 'For excavators.', image: 'assets/images/photos/products/link-arm.jpg' },
    { seg: 'earth', segment: 'Earth-moving', name: 'Dozer blade', note: 'For excavators.', image: 'assets/images/photos/products/dozer-blade.jpg' },
    { seg: 'earth', segment: 'Earth-moving', name: 'Engine frame', note: 'For excavators.', image: 'assets/images/photos/products/engine-frame.jpg' },
    { seg: 'earth', segment: 'Earth-moving', name: 'Rear chassis frame', note: 'For vibrating compactors.', image: 'assets/images/photos/products/rear-chassis-frame.jpg' },
    { seg: 'earth', segment: 'Earth-moving', name: 'Star plate', note: 'For crawler frames.', image: 'assets/images/photos/products/star-plate.jpg' },
    { seg: 'agri', segment: 'Agriculture', name: 'Front axle assembly', note: 'For tractors.', image: 'assets/images/photos/products/front-axle.jpg' }
  ];

  function el(tag, attrs, children) {
    var n = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === 'text') n.textContent = attrs[k];
      else if (k === 'class') n.className = attrs[k];
      else n.setAttribute(k, attrs[k]);
    });
    (children || []).forEach(function (c) { if (c) n.appendChild(c); });
    return n;
  }

  /* ---- Mobile menu ---- */
  var menuBtn = document.querySelector('.menu-btn');
  var nav = document.getElementById('site-nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { nav.classList.remove('open'); menuBtn.setAttribute('aria-expanded', 'false'); }
    });
  }

  /* ---- Processes tabs ---- */
  var tabList = document.getElementById('proc-tabs');
  var panel = document.getElementById('proc-panel');
  if (tabList && panel) {
    var tabs = PROCESSES.map(function (p, i) {
      var b = el('button', { class: 'tab', role: 'tab', id: 'tab-' + p.id, 'aria-controls': 'proc-panel', 'aria-selected': 'false', tabindex: '-1', text: p.name });
      b.addEventListener('click', function () { select(i, false); });
      tabList.appendChild(b);
      return b;
    });
    tabList.addEventListener('keydown', function (e) {
      var cur = tabs.indexOf(document.activeElement);
      if (cur < 0) return;
      var next = null;
      if (e.key === 'ArrowDown' || e.key === 'ArrowRight') next = (cur + 1) % tabs.length;
      if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') next = (cur - 1 + tabs.length) % tabs.length;
      if (e.key === 'Home') next = 0;
      if (e.key === 'End') next = tabs.length - 1;
      if (next !== null) { e.preventDefault(); select(next, true); }
    });
    function select(i, focus) {
      var p = PROCESSES[i];
      tabs.forEach(function (t, j) {
        t.setAttribute('aria-selected', j === i ? 'true' : 'false');
        t.setAttribute('tabindex', j === i ? '0' : '-1');
      });
      if (focus) tabs[i].focus();
      panel.setAttribute('aria-labelledby', 'tab-' + p.id);
      var media = el('div', { class: 'ph proc-media' }, [el('span', { class: 'ph-label', text: '[Process photo: ' + p.name + ']' })]);
      if (p.image) { media.style.backgroundImage = 'url(' + p.image + ')'; media.innerHTML = ''; media.setAttribute('role', 'img'); media.setAttribute('aria-label', p.name + ' photo'); }
      var text = el('div', { class: 'proc-text' }, [
        (function () { var h = el('div', { class: 'hue-bar' }); h.style.background = HUES[i]; return h; })(),
        el('h3', { text: p.name }),
        el('p', { text: p.body }),
        el('div', { class: 'tags' }, p.tags.map(function (t) { return el('span', { text: t }); })),
        p.video ? el('a', { href: p.video, target: '_blank', rel: 'noopener', text: 'Watch the ' + p.name.toLowerCase() + ' video' }) : null
      ]);
      panel.innerHTML = '';
      panel.appendChild(text);
      panel.appendChild(media);
      panel.classList.remove('anim-in'); void panel.offsetWidth; panel.classList.add('anim-in');
    }
    select(1, false);
  }

  /* ---- Product filter ---- */
  var filters = document.getElementById('filters');
  var grid = document.getElementById('product-grid');
  var count = document.getElementById('product-count');
  if (filters && grid) {
    var pills = SEGMENTS.map(function (s) {
      var b = el('button', { class: 'pill', 'aria-pressed': 'false', text: s.label });
      b.addEventListener('click', function () { render(s.id); });
      filters.appendChild(b);
      return b;
    });
    function render(seg) {
      pills.forEach(function (b, i) { b.setAttribute('aria-pressed', SEGMENTS[i].id === seg ? 'true' : 'false'); });
      var list = PRODUCTS.filter(function (p) { return seg === 'all' || p.seg === seg; });
      grid.innerHTML = '';
      list.forEach(function (p) {
        var media;
        if (p.image) media = el('img', { src: p.image, alt: p.name, loading: 'lazy', style: 'aspect-ratio:4/3;object-fit:cover;width:100%' });
        else media = el('div', { class: 'ph' }, [el('span', { class: 'ph-label', text: '[Product photo]' })]);
        grid.appendChild(el('article', { class: 'product anim-in' }, [
          media,
          el('div', { class: 'meta' }, [
            el('div', { class: 'seg', text: p.segment }),
            el('h3', { text: p.name }),
            el('p', { text: p.note })
          ])
        ]));
      });
      count.textContent = 'Showing ' + list.length + ' of ' + PRODUCTS.length + ' products';
    }
    render('all');
  }

  /* ---- Enquiry form ----
     Front-end validation only. Connect to your mail service / backend:
     set data-endpoint on the form to a URL that accepts POST (e.g. Formspree, a PHP mailer). */
  var form = document.getElementById('enquiry');
  var sent = document.getElementById('sent');
  if (form && sent) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      ['f-name', 'f-mail', 'f-msg'].forEach(function (id) {
        var f = document.getElementById(id);
        var err = document.getElementById(id + '-err');
        var bad = !f.value.trim() || (f.type === 'email' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.value));
        f.setAttribute('aria-invalid', bad ? 'true' : 'false');
        err.textContent = bad ? (f.type === 'email' ? 'Enter a valid email, like name@company.com.' : 'This field is required.') : '';
        if (bad && ok) { f.focus(); ok = false; }
      });
      if (!ok) return;
      var endpoint = form.getAttribute('data-endpoint');
      var done = function () { form.hidden = true; sent.hidden = false; sent.querySelector('h3').focus(); };
      if (endpoint) {
        fetch(endpoint, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
          .then(function (r) { if (!r.ok) throw new Error(); done(); })
          .catch(function () { document.getElementById('form-status').textContent = 'Your enquiry could not be sent. Call +91 240 6625613 or try again.'; });
      } else { done(); }
    });
    document.getElementById('send-another').addEventListener('click', function () {
      form.reset(); form.hidden = false; sent.hidden = true; document.getElementById('f-name').focus();
    });
  }

  var y = document.getElementById('year'); if (y) y.textContent = new Date().getFullYear();
})();
