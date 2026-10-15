/* MACPL website — interactions (no dependencies) */
(function () {
  'use strict';
  var HUES = ['#ED1B2F', '#F15A31', '#F47932', '#F79433', '#FBB034', '#FFCC32'];

  /* ---- Content: edit here ---- */
  var PROCESSES = [
    { id: 'cut', name: 'Plasma cutting', body: 'CNC plasma cutting turns plate into accurate blanks for frames, links and brackets, ready for forming and welding with minimal rework.', tags: ['CNC profile cutting', 'Plate blanks', 'Heavy fabrication'], image: 'assets/images/photos/processes/plasma-cutting.jpg', video: 'https://www.youtube.com/watch?v=vPwjm4bx5XY' },
    { id: 'bend', name: 'Tube bending', body: 'Tube bending is a cluster of sub-processes, run on induction heating machines, hydraulic presses, a CNC cold tube bender and a robotic hot-bending cell. Both cold and hot bending run efficiently, each line at more than 2,000 parts a day. In the robotic cell, the robot does everything from picking up the raw tube, through homing, resistance heating and the first and second bends, to placing the bent part in the tray.', tags: ['Induction heating', 'CNC cold bending', 'Robotic hot bending', '2,000+ parts/day each'], image: 'assets/images/photos/processes/tube-bending.jpg', video: 'https://www.youtube.com/watch?v=7Ba8KVW0Pok' },
    { id: 'weld', name: 'Welding', body: 'Skilled welders and robotic cells hold process parameters tight, so every joint on a steering column or fork is as strong as the design demands.', tags: ['Robotic welding', 'MIG / TIG', 'Fixture-controlled'], image: 'assets/images/photos/processes/welding.jpg', video: '' },
    { id: 'heat', name: 'Heat treatment', body: 'We design and build our own furnaces. Strictly controlled parameters give the exact microstructure needed, stress-relieved and normalised, batch after batch.', tags: ['In-house furnaces', 'Stress relieving', 'Normalising'], image: 'assets/images/photos/processes/heat-treatment.jpg', video: 'https://www.youtube.com/watch?v=NaewbxKqvD0' },
    { id: 'cast', name: 'Aluminium casting', body: 'Gravity die casting with alloy made in-house, which cuts material cost substantially. Tight process control delivers castings without blow holes.', tags: ['Gravity die casting', 'In-house alloy', 'Zero blow-hole target'], image: 'assets/images/photos/processes/aluminium-casting.jpg', video: 'https://www.youtube.com/watch?v=sTr3GobQtg8' },
    { id: 'coat', name: 'Surface finish', body: 'Surface treatment and powder coating protect parts such as under-bracket assemblies against corrosion and wear in the field.', tags: ['Pre-treatment', 'Powder coating', 'Corrosion protection'], image: 'assets/images/photos/processes/surface-finish.jpg', video: '' }
  ];

  var SEGMENTS = [
    { id: 'all', label: 'All products' },
    { id: 'two', label: 'Two-wheeler & EV', heading: 'Components for two-wheelers and EVs', note: 'Under-bracket assemblies and telescopic suspension forks for motorcycles and electric two-wheelers.', image: 'assets/images/photos/products/fork-2w-disc.jpg' },
    { id: 'three', label: 'Three-wheeler & EV', heading: 'Components for three-wheelers and EVs', note: 'Steering columns, front forks and suspension forks for passenger and cargo three-wheelers.', image: 'assets/images/photos/products/steering-column-cargo.jpg' },
    { id: 'earth', label: 'Earth-moving', heading: 'Components for earth-moving equipment', note: 'Bucket links, link arms, dozer blades and heavy frames for excavators and compactors.', image: 'assets/images/photos/products/bucket-link.jpg' },
    { id: 'agri', label: 'Agriculture', heading: 'Components for agriculture equipment', note: 'Front axle assemblies for tractors.', image: 'assets/images/photos/products/front-axle.jpg' }
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
    var fromHash = function () {
      var id = location.hash.slice(1);
      for (var i = 0; i < PROCESSES.length; i++) if (PROCESSES[i].id === id) return i;
      return -1;
    };
    var start = fromHash();
    select(start < 0 ? 1 : start, false);
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { history.replaceState(null, '', '#' + PROCESSES[i].id); });
    });
    window.addEventListener('hashchange', function () { var i = fromHash(); if (i >= 0) select(i, false); });
  }

  /* ---- Home: process cards ---- */
  var procCards = document.getElementById('proc-cards');
  if (procCards) {
    PROCESSES.forEach(function (p, i) {
      var bar = el('div', { class: 'hue-bar' }); bar.style.background = HUES[i];
      procCards.appendChild(el('a', { class: 'card', href: 'processes.html#' + p.id }, [
        el('img', { src: p.image, alt: '', loading: 'lazy' }),
        el('div', { class: 'meta' }, [
          bar,
          el('h3', { text: p.name }),
          el('p', { text: p.body.split('. ')[0].replace(/\.?$/, '.') }),
          el('span', { class: 'more', text: 'Explore process' })
        ])
      ]));
    });
  }

  /* ---- Home: product segment cards ---- */
  var segCards = document.getElementById('segment-cards');
  if (segCards) {
    SEGMENTS.filter(function (s) { return s.id !== 'all'; }).forEach(function (s) {
      var n = PRODUCTS.filter(function (p) { return p.seg === s.id; }).length;
      segCards.appendChild(el('a', { class: 'card', href: 'products.html?seg=' + s.id }, [
        el('img', { src: s.image, alt: '', loading: 'lazy' }),
        el('div', { class: 'meta' }, [
          el('div', { class: 'seg', text: n + (n === 1 ? ' product' : ' products') }),
          el('h3', { text: s.label }),
          el('p', { text: s.note }),
          el('span', { class: 'more', text: 'View products' })
        ])
      ]));
    });
  }

  /* ---- Product filter ---- */
  var filters = document.getElementById('filters');
  var grid = document.getElementById('product-grid');
  var count = document.getElementById('product-count');
  if (filters && grid) {
    var pills = SEGMENTS.map(function (s) {
      var b = el('button', { class: 'tab', 'aria-pressed': 'false', text: s.label });
      b.addEventListener('click', function () {
        render(s.id);
        history.replaceState(null, '', s.id === 'all' ? location.pathname : '?seg=' + s.id);
      });
      filters.appendChild(b);
      return b;
    });
    function render(seg) {
      pills.forEach(function (b, i) { b.setAttribute('aria-pressed', SEGMENTS[i].id === seg ? 'true' : 'false'); });
      var list = PRODUCTS.filter(function (p) { return seg === 'all' || p.seg === seg; });
      grid.innerHTML = '';
      /* Product gallery: one heading per segment, as on the current site */
      SEGMENTS.filter(function (s) { return s.id !== 'all' && (seg === 'all' || s.id === seg); }).forEach(function (s) {
        var cards = el('div', { class: 'grid-products' });
        list.filter(function (p) { return p.seg === s.id; }).forEach(function (p) {
          var media;
          if (p.image) media = el('img', { src: p.image, alt: p.name, loading: 'lazy', style: 'aspect-ratio:1/1;object-fit:cover;width:100%' });
          else media = el('div', { class: 'ph' }, [el('span', { class: 'ph-label', text: '[Product photo]' })]);
          cards.appendChild(el('article', { class: 'product anim-in' }, [
            media,
            el('div', { class: 'meta' }, [
              el('div', { class: 'seg', text: p.segment }),
              el('h3', { text: p.name }),
              el('p', { text: p.note })
            ])
          ]));
        });
        grid.appendChild(el('h3', { class: 'seg-head', text: s.heading }));
        grid.appendChild(cards);
      });
      count.textContent = 'Showing ' + list.length + ' of ' + PRODUCTS.length + ' products';
    }
    var q = /[?&]seg=([a-z]+)/.exec(location.search);
    render(q && SEGMENTS.some(function (s) { return s.id === q[1]; }) ? q[1] : 'all');
  }

  /* ---- Forms (enquiry, job application) ----
     Front-end validation only. Connect to your mail service / backend:
     set data-endpoint on the form to a URL that accepts POST (e.g. Formspree, a PHP mailer). */
  Array.prototype.forEach.call(document.querySelectorAll('form.js-form'), function (form) {
    var sent = document.getElementById(form.getAttribute('data-sent'));
    var status = form.querySelector('.form-status');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      Array.prototype.forEach.call(form.querySelectorAll('[required]'), function (f) {
        var err = document.getElementById(f.id + '-err');
        var bad = !f.value.trim() || (f.type === 'email' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.value));
        f.setAttribute('aria-invalid', bad ? 'true' : 'false');
        if (err) err.textContent = bad ? (f.type === 'email' ? 'Enter a valid email, like name@company.com.' : 'This field is required.') : '';
        if (bad && ok) { f.focus(); ok = false; }
      });
      if (!ok) return;
      var endpoint = form.getAttribute('data-endpoint');
      var done = function () { form.hidden = true; sent.hidden = false; sent.querySelector('h3').focus(); };
      if (endpoint) {
        fetch(endpoint, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
          .then(function (r) { if (!r.ok) throw new Error(); done(); })
          .catch(function () { status.textContent = 'This could not be sent. Call +91 240 6625613 or try again.'; });
      } else { done(); }
    });
    var again = sent && sent.querySelector('.js-again');
    if (again) again.addEventListener('click', function () {
      form.reset(); form.hidden = false; sent.hidden = true; form.querySelector('input').focus();
    });
  });

  /* ---- About: the sub-menu shows one section at a time (about.html#values etc.) ---- */
  var tabbed = document.querySelector('.tabbed');
  var subLinks = document.querySelectorAll('.subnav a');
  if (tabbed && subLinks.length) {
    var panels = Array.prototype.slice.call(tabbed.children);
    var show = function (id) {
      if (!panels.some(function (p) { return p.dataset.tab === id; })) id = panels[0].dataset.tab;
      panels.forEach(function (p) { p.classList.toggle('on', p.dataset.tab === id); });
      Array.prototype.forEach.call(subLinks, function (a) {
        if (a.getAttribute('href') === '#' + id) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
      });
    };
    Array.prototype.forEach.call(subLinks, function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        var id = a.getAttribute('href').slice(1);
        history.replaceState(null, '', '#' + id);
        show(id);
      });
    });
    window.addEventListener('hashchange', function () { show(location.hash.slice(1)); });
    show(location.hash.slice(1));
  }

  /* ---- Site search (search.html?q=...) ---- */
  var PAGES = [
    { url: 'index.html', title: 'Home', text: 'Building capacities, building assets. Mass manufacturing from part manufacturing to complete assemblies. Customized, durable and critical auto components.' },
    { url: 'about.html#overview', title: 'About MACPL', text: 'Complex, technically challenging auto components for vehicle safety. Started in 1997 by Ram Bhogale and Ajit Soundalgekar to make steering columns for scooters and three-wheelers.' },
    { url: 'about.html#vision', title: 'Vision', text: 'To be a well respected innovative group that is most preferred as a partner in progress globally.' },
    { url: 'about.html#values', title: 'Values', text: 'Integrity, commitment, compassion, passion, innovation, proud of roots. The six values of the rising sun.' },
    { url: 'about.html#management', title: 'Management', text: 'Ram Bhogale, Chairman. Ajit Soundalgekar, Managing Director. Plant heads Anant Adhav, Vivek Deshpande, Avinash Kude. Leadership.' },
    { url: 'about.html#strengths', title: 'Strengths', text: 'Fast development, mass manufacturing, in-house design of fixtures, tooling and furnaces, robotic cells, in-house alloy, TPM, SAP, USD 10 million in assets. Infrastructure.' },
    { url: 'about.html#financials', title: 'Financials', text: 'Annual return 2021–22 and CSR policy documents (PDF).' },
    { url: 'quality.html', title: 'Quality', text: 'Total Productive Maintenance (TPM), six parameters: product, quality, cost, delivery, safety, morale. Quality policy. ISO 9001, ISO 14001 and OHSAS 18001 certification with TUV Nord. Integrated management policy.' },
    { url: 'news.html', title: 'News and events', text: 'MACPL now with ISO 9001, ISO 14001 and OHSAS 18001 certification. TUV Nord auditors.' },
    { url: 'group.html', title: 'The Group', text: 'Applied Innovation & Technology Group (AITG). The rising sun identity, brand essence, the visionary Nanasaheb Bhogale: knowledge is the ultimate quest. Group companies: Umasons, Dhruv Coatings, Bhogale Automotive, Preci Fab, Technocraft Toolings, iInvent Labs. Honest business with honest relationships.' },
    { url: 'careers.html', title: 'Careers', text: 'Working at MACPL. Jobs, apply online with your resume. Engineers, welders, quality inspectors, operators. Current openings.' },
    { url: 'contact.html', title: 'Contact us', text: 'E-63, MIDC Waluj, Aurangabad 431136. Phone, enquiry, request a quote, map and directions.' }
  ];
  var resultsList = document.getElementById('search-results');
  if (resultsList) {
    var index = PAGES.slice();
    PROCESSES.forEach(function (p) { index.push({ url: 'processes.html#' + p.id, title: p.name, text: 'Process. ' + p.body + ' ' + p.tags.join(', ') }); });
    PRODUCTS.forEach(function (p) { index.push({ url: 'products.html?seg=' + p.seg, title: p.name, text: p.segment + ' product. ' + p.note }); });
    var qm = /[?&]q=([^&]*)/.exec(location.search);
    var query = qm ? decodeURIComponent(qm[1].replace(/\+/g, ' ')).trim() : '';
    var qInput = document.getElementById('q-page'); if (qInput) qInput.value = query;
    var summary = document.getElementById('search-summary');
    if (query) {
      var terms = query.toLowerCase().split(/\s+/);
      var hits = index.filter(function (r) {
        var hay = (r.title + ' ' + r.text).toLowerCase();
        return terms.every(function (t) { return hay.indexOf(t) >= 0; });
      });
      summary.textContent = hits.length
        ? hits.length + (hits.length === 1 ? ' result' : ' results') + ' for “' + query + '”'
        : 'No results for “' + query + '”. Try a product, process or page name.';
      hits.forEach(function (r) {
        resultsList.appendChild(el('li', null, [el('a', { href: r.url }, [
          el('b', { text: r.title }),
          el('span', { text: r.text.length > 160 ? r.text.slice(0, 157) + '…' : r.text })
        ])]));
      });
    }
  }

  var y = document.getElementById('year'); if (y) y.textContent = new Date().getFullYear();
})();
