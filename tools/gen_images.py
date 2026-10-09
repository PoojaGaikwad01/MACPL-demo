"""Generate on-brand SVG illustrations for the MACPL site placeholders.
Usage: python gen_images.py <site_root>
"""
import math, os, random, sys

ROOT = sys.argv[1]
BLUE, NAVY = '#004282', '#0a2f5c'
BG = '#eaf0f6'
S1, S2, S3, S4 = '#e4eaf2', '#bccadb', '#8ea0b8', '#5b6e88'
H = ['#ED1B2F', '#F15A31', '#F47932', '#F79433', '#FBB034', '#FFCC32']
OW = 3  # outline width


def f(v):
    return ('%.1f' % v).rstrip('0').rstrip('.')


def pts(p):
    return ' '.join(f(x) + ',' + f(y) for x, y in p)


def stripes(w, h, corner='br'):
    """Six sun-hue bars on the brand 60 degree diagonal."""
    out, hh, k = [], 70, 70 / math.tan(math.radians(60))
    x0 = w - 200 if corner == 'br' else 30
    for i, c in enumerate(H):
        x = x0 + i * 22
        out.append('<polygon points="%s" fill="%s"/>' % (pts([(x, h), (x + 16, h), (x + 16 + k, h - hh), (x + k, h - hh)]), c))
    return ''.join(out)


def frame(w, h, title, body, corner='br', bg=BG, defs=''):
    grid = ''.join('<path d="M%d 0V%d"/>' % (x, h) for x in range(40, w, 40)) + \
           ''.join('<path d="M0 %dH%d"/>' % (y, w) for y in range(40, h, 40))
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img">'
            '<title>%s</title><defs>%s</defs><rect width="%d" height="%d" fill="%s"/>'
            '<g stroke="%s" stroke-width="1" opacity=".06">%s</g>%s%s</svg>'
            % (w, h, w, h, title, defs, w, h, bg, BLUE, grid, body, stripes(w, h, corner) if corner else ''))


def shadow(cx, cy, rx, ry=None):
    return '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" opacity=".1"/>' % (f(cx), f(cy), f(rx), f(ry or rx * .12), NAVY)


def tube(d, w, base=S3, hi=S1):
    """Round tube along a path: outline, body, specular streak."""
    s = 'fill="none" stroke-linecap="round" stroke-linejoin="round"'
    return ('<path d="%s" %s stroke="%s" stroke-width="%s"/>' % (d, s, NAVY, f(w + 2 * OW)) +
            '<path d="%s" %s stroke="%s" stroke-width="%s"/>' % (d, s, base, f(w)) +
            '<path d="%s" %s stroke="%s" stroke-width="%s" opacity=".85" transform="translate(%s %s)"/>'
            % (d, s, hi, f(w * .22), f(-w * .18), f(-w * .18)))


def line(x1, y1, x2, y2, w, color, cap='round', extra=''):
    return '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s" stroke-linecap="%s" %s/>' % (
        f(x1), f(y1), f(x2), f(y2), color, f(w), cap, extra)


def union(shapes, fill, dx=0, dy=0, outline=NAVY):
    """Draw the union of shapes with one clean outline (outlines first, fills on top)."""
    def el(s, color, grow):
        k = s[0]
        if k == 'c':
            _, cx, cy, r = s
            return '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(cx + dx), f(cy + dy), f(r + grow), color)
        if k == 'l':
            _, x1, y1, x2, y2, w = s
            return line(x1 + dx, y1 + dy, x2 + dx, y2 + dy, w + 2 * grow, color)
        if k == 'p':
            p = [(x + dx, y + dy) for x, y in s[1]]
            st = ' stroke="%s" stroke-width="%s" stroke-linejoin="round"' % (color, f(2 * grow)) if grow else ''
            return '<polygon points="%s" fill="%s"%s/>' % (pts(p), color, st)
        if k == 'd':
            st = ' stroke="%s" stroke-width="%s" stroke-linejoin="round"' % (color, f(2 * grow)) if grow else ''
            return '<path d="%s" fill="%s" transform="translate(%s %s)"%s/>' % (s[1], color, f(dx), f(dy), st)
    return ''.join(el(s, outline, OW) for s in shapes) + ''.join(el(s, fill, 0) for s in shapes)


def solid(shapes, top=S2, side=S4, depth=(0, 18)):
    """Extruded plate: side (shifted) union, then top union."""
    return union(shapes, side, *depth) + union(shapes, top)


def bush(cx, cy, r, ring=S1):
    return ('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="%d"/>' % (f(cx), f(cy), f(r), ring, NAVY, OW) +
            '<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="2"/>' % (f(cx), f(cy), f(r * .58), '#3d4f68', NAVY))


def glow(cx, cy, r):
    return ('<circle cx="%s" cy="%s" r="%s" fill="%s" opacity=".25"/>' % (f(cx), f(cy), f(r * 2.2), H[5]) +
            '<circle cx="%s" cy="%s" r="%s" fill="%s" opacity=".55"/>' % (f(cx), f(cy), f(r * 1.1), H[4]) +
            '<circle cx="%s" cy="%s" r="%s" fill="#fff"/>' % (f(cx), f(cy), f(r * .45)))


def sparks(cx, cy, n=14, seed=1, spread=(200, 340), ln=(20, 60)):
    rnd, out = random.Random(seed), []
    for i in range(n):
        a = math.radians(rnd.uniform(*spread))
        r0, r1 = rnd.uniform(8, 18), rnd.uniform(*ln)
        out.append(line(cx + r0 * math.cos(a), cy - r0 * math.sin(a), cx + r1 * math.cos(a), cy - r1 * math.sin(a),
                        rnd.choice([2, 2.5, 3]), rnd.choice(H[1:])))
    return ''.join(out)


def arm(points, w=34, color=H[2]):
    """Industrial robot: base, orange links, joints."""
    (bx, by), rest = points[0], points[1:]
    o = '<rect x="%s" y="%s" width="%s" height="%s" rx="6" fill="%s" stroke="%s" stroke-width="%d"/>' % (
        f(bx - 42), f(by), 84, 26, NAVY, NAVY, OW)
    o += '<path d="M%s %s h64 l-8 -40 h-48z" fill="%s" stroke="%s" stroke-width="%d" stroke-linejoin="round"/>' % (
        f(bx - 32), f(by), H[2], NAVY, OW)
    chain = [(bx, by - 40)] + rest[:-1]
    for (x1, y1), (x2, y2) in zip(chain, chain[1:]):
        o += line(x1, y1, x2, y2, w + 2 * OW, NAVY) + line(x1, y1, x2, y2, w, color)
        o += line(x1, y1, x2, y2, w * .2, H[4], extra='opacity=".7" transform="translate(-4 -4)"')
    (x1, y1), (x2, y2) = rest[-2], rest[-1]
    o += line(x1, y1, x2, y2, 16, NAVY) + line(x1, y1, x2, y2, 10, S3)
    for x, y in chain:
        o += '<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="%d"/>' % (f(x), f(y), f(w * .62), S4, NAVY, OW)
        o += '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(x), f(y), f(w * .22), S1)
    return o


def save(rel, svg):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write(svg)
    print(rel, len(svg))


# ---------------------------------------------------------------- processes (800x600, left 16% clipped)
def proc_cut():
    b = shadow(500, 520, 290)
    b += solid([('p', [(240, 430), (560, 345), (770, 430), (450, 520)])], top=S2, side=S4, depth=(0, 16))
    cut = [(390, 432), (480, 405), (575, 430), (540, 455), (450, 474)]
    b += '<polyline points="%s" fill="none" stroke="%s" stroke-width="4" stroke-linejoin="round"/>' % (pts(cut[:3]), NAVY)
    b += '<polyline points="%s" fill="none" stroke="%s" stroke-width="3" stroke-dasharray="9 7"/>' % (pts(cut[2:] + [cut[0]]), H[2])
    b += '<rect x="230" y="70" width="560" height="34" fill="%s" stroke="%s" stroke-width="3"/>' % (BLUE, NAVY)
    b += '<rect x="520" y="90" width="110" height="60" rx="6" fill="%s" stroke="%s" stroke-width="3"/>' % (NAVY, NAVY)
    b += '<rect x="551" y="146" width="48" height="190" rx="6" fill="%s" stroke="%s" stroke-width="3"/>' % (S2, NAVY)
    b += '<rect x="551" y="200" width="48" height="26" fill="%s"/>' % H[2]
    b += '<polygon points="560,336 590,336 583,372 567,372" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % (S4, NAVY)
    b += '<path d="M600 120 C690 120 700 40 790 40" fill="none" stroke="%s" stroke-width="10" stroke-linecap="round"/>' % NAVY
    b += '<polygon points="571,372 579,372 584,428 566,428" fill="%s"/>' % H[5]
    b += glow(575, 430, 16) + sparks(575, 432, 18, 3, (190, 350), (24, 80))
    return frame(800, 600, 'Plasma cutting illustration', b)


def proc_bend():
    cx, cy = 430, 330
    b = shadow(470, 540, 300)
    b += '<circle cx="%d" cy="%d" r="152" fill="%s" stroke="%s" stroke-width="3"/>' % (cx, cy, S2, NAVY)
    b += '<circle cx="%d" cy="%d" r="120" fill="none" stroke="%s" stroke-width="12"/>' % (cx, cy, S4)
    for a in range(0, 360, 90):
        r = math.radians(a + 45)
        b += '<circle cx="%s" cy="%s" r="9" fill="%s"/>' % (f(cx + 78 * math.cos(r)), f(cy + 78 * math.sin(r)), NAVY)
    b += '<circle cx="%d" cy="%d" r="40" fill="%s" stroke="%s" stroke-width="3"/><circle cx="%d" cy="%d" r="14" fill="%s"/>' % (cx, cy, S3, NAVY, cx, cy, NAVY)
    b += '<rect x="540" y="226" width="200" height="44" rx="4" fill="%s" stroke="%s" stroke-width="3"/>' % (BLUE, NAVY)
    b += tube('M790 210 L430 210 A120 120 0 0 0 345 415 L440 510', 34)
    b += '<rect x="-62" y="-22" width="124" height="44" rx="4" fill="%s" stroke="%s" stroke-width="3" transform="translate(362 488) rotate(45)"/>' % (BLUE, NAVY)
    b += '<path d="M270 238 A185 185 0 0 0 270 422" fill="none" stroke="%s" stroke-width="6" stroke-linecap="round"/>' % H[2]
    b += '<polygon points="279,438 261,427 279,417" fill="%s"/>' % H[2]
    return frame(800, 600, 'Tube bending illustration', b)


def proc_weld():
    b = shadow(470, 520, 300)
    b += solid([('p', [(240, 440), (520, 370), (760, 440), (480, 515)])], top=S2, side=S4, depth=(0, 16))
    b += '<ellipse cx="480" cy="300" rx="34" ry="11" fill="%s" stroke="%s" stroke-width="3"/>' % (S4, NAVY)
    b += '<path d="M446 300 V432 A34 11 0 0 0 514 432 V300" fill="%s" stroke="%s" stroke-width="3"/>' % (S3, NAVY)
    b += '<rect x="456" y="304" width="9" height="126" fill="%s" opacity=".85"/>' % S1
    b += '<path d="M446 432 A34 11 0 0 0 488 443" fill="none" stroke="%s" stroke-width="8" stroke-linecap="round"/>' % H[3]
    b += '<path d="M488 443 A34 11 0 0 0 514 432" fill="none" stroke="%s" stroke-width="3" stroke-dasharray="5 5"/>' % NAVY
    b += arm([(690, 360), (650, 190), (560, 220), (500, 430)])
    b += glow(497, 440, 14) + sparks(497, 442, 18, 7, (180, 360), (20, 70))
    return frame(800, 600, 'Robotic welding illustration', b)


def proc_heat():
    defs = ('<radialGradient id="g" cx=".5" cy=".6" r=".7"><stop offset="0" stop-color="#FFE9A6"/>'
            '<stop offset=".35" stop-color="%s"/><stop offset=".75" stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient>' % (H[4], H[1], H[0]))
    b = shadow(520, 505, 290)
    b += '<rect x="600" y="50" width="44" height="80" fill="%s" stroke="%s" stroke-width="3"/>' % (S4, NAVY)
    b += '<polygon points="300,130 340,105 770,105 730,130" fill="#2a5d94" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % NAVY
    b += '<polygon points="730,130 770,105 770,465 730,490" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % (NAVY, NAVY)
    b += '<rect x="300" y="130" width="430" height="360" fill="%s" stroke="%s" stroke-width="3"/>' % (BLUE, NAVY)
    b += '<rect x="340" y="205" width="280" height="245" rx="6" fill="url(#g)" stroke="%s" stroke-width="4"/>' % NAVY
    b += '<rect x="330" y="140" width="300" height="52" rx="4" fill="%s" stroke="%s" stroke-width="3"/>' % (S3, NAVY)
    for x in (345, 615):
        b += '<rect x="%d" y="40" width="10" height="100" fill="%s"/>' % (x - 5, NAVY)
    b += '<rect x="370" y="410" width="220" height="16" fill="%s"/>' % NAVY
    for x in (395, 455, 515):
        b += '<path d="M%d 408 V340 a22 22 0 0 1 44 0 V408" fill="none" stroke="#b4451b" stroke-width="13" stroke-linecap="round"/>' % x
    b += '<rect x="645" y="210" width="66" height="130" rx="4" fill="%s" stroke="%s" stroke-width="2"/>' % (NAVY, '#2a5d94')
    b += '<circle cx="678" cy="248" r="20" fill="#fff" stroke="%s" stroke-width="3"/>' % S3
    b += line(678, 248, 691, 236, 3, H[0])
    b += '<circle cx="664" cy="300" r="7" fill="%s"/><circle cx="692" cy="300" r="7" fill="%s"/>' % (H[5], H[0])
    for i, x in enumerate((420, 480, 540)):
        b += '<path d="M%d 95 q-12 -15 0 -30 t0 -30" fill="none" stroke="%s" stroke-width="5" stroke-linecap="round" opacity=".8"/>' % (x, H[3 + i % 2])
    return frame(800, 600, 'Heat treatment furnace illustration', b, defs=defs)


def proc_cast():
    b = shadow(500, 515, 300)
    b += '<rect x="330" y="482" width="320" height="26" rx="4" fill="%s" stroke="%s" stroke-width="3"/>' % (NAVY, NAVY)
    b += '<rect x="360" y="330" width="122" height="152" fill="%s" stroke="%s" stroke-width="3"/>' % (S3, NAVY)
    b += '<rect x="486" y="330" width="122" height="152" fill="%s" stroke="%s" stroke-width="3"/>' % (S2, NAVY)
    b += '<polygon points="456,330 512,330 494,352 474,352" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % (H[2], NAVY)
    for y in (360, 450):
        b += '<rect x="606" y="%d" width="22" height="16" fill="%s" stroke="%s" stroke-width="2"/>' % (y, S4, NAVY)
    b += '<path d="M424 192 C452 222 482 262 484 336" fill="none" stroke="%s" stroke-width="13" stroke-linecap="round"/>' % H[2]
    b += '<path d="M424 192 C452 222 482 262 484 336" fill="none" stroke="%s" stroke-width="4" stroke-linecap="round"/>' % H[5]
    b += glow(484, 336, 13)
    b += ('<g transform="translate(330 170) rotate(35)">'
          '<line x1="-88" y1="-14" x2="-210" y2="-34" stroke="%s" stroke-width="20" stroke-linecap="round"/>'
          '<line x1="-88" y1="-14" x2="-210" y2="-34" stroke="%s" stroke-width="14" stroke-linecap="round"/>'
          '<path d="M-92 -40 L96 -40 L72 50 Q0 78 -72 50 Z" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>'
          '<rect x="-92" y="-48" width="188" height="14" rx="4" fill="%s" stroke="%s" stroke-width="3"/>'
          '<rect x="-80" y="-36" width="164" height="10" fill="%s"/></g>') % (NAVY, S4, S4, NAVY, S3, NAVY, H[3])
    b += '<circle cx="705" cy="440" r="56" fill="%s" stroke="%s" stroke-width="3"/>' % (S1, NAVY)
    for a in range(0, 360, 72):
        r = math.radians(a - 90)
        b += '<circle cx="%s" cy="%s" r="13" fill="%s" stroke="%s" stroke-width="2"/>' % (f(705 + 34 * math.cos(r)), f(440 + 34 * math.sin(r)), S4, NAVY)
    b += '<circle cx="705" cy="440" r="12" fill="%s" stroke="%s" stroke-width="2"/>' % (S3, NAVY)
    return frame(800, 600, 'Aluminium gravity die casting illustration', b)


def clamp_shape(cx, top):
    return [('l', cx - 92, top + 34, cx + 92, top + 34, 64), ('c', cx, top + 44, 40)]


def proc_coat():
    defs = '<linearGradient id="g" x1="0" x2="1"><stop offset=".45" stop-color="%s"/><stop offset=".62" stop-color="%s"/></linearGradient>' % (S2, BLUE)
    b = line(130, 110, 800, 110, 10, NAVY)
    for x in (270, 500):
        b += line(x, 110, x, 220, 4, NAVY) + '<path d="M%d 220 q0 12 -10 12" fill="none" stroke="%s" stroke-width="4"/>' % (x, NAVY)
        b += '<circle cx="%d" cy="110" r="9" fill="%s" stroke="%s" stroke-width="3"/>' % (x, S3, NAVY)
    b += union(clamp_shape(270, 230), BLUE)
    b += union(clamp_shape(500, 230), 'url(#g)')
    for cx in (270, 500):
        for x in (cx - 80, cx, cx + 80):
            b += '<circle cx="%d" cy="%d" r="15" fill="%s" stroke="%s" stroke-width="3"/>' % (x, 266 if x != cx else 274, BG, NAVY)
    rnd = random.Random(5)
    b += '<polygon points="651,368 545,238 545,342" fill="%s" opacity=".12"/>' % BLUE
    for _ in range(70):
        t = rnd.random() ** .7
        x = 651 - 106 * t
        y = 368 - (130 - (rnd.random()) * 104) * t
        b += '<circle cx="%s" cy="%s" r="%s" fill="%s" opacity=".7"/>' % (f(x), f(y), f(rnd.uniform(1.5, 3.5)), BLUE)
    b += ('<g transform="translate(740 400) rotate(20)">'
          '<rect x="-84" y="-9" width="104" height="18" fill="%s" stroke="%s" stroke-width="3"/>'
          '<rect x="-98" y="-6" width="16" height="12" fill="%s"/>'
          '<rect x="0" y="-24" width="66" height="38" rx="6" fill="%s" stroke="%s" stroke-width="3"/>'
          '<polygon points="18,14 50,14 62,84 32,84" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>'
          '<rect x="8" y="14" width="10" height="26" rx="3" fill="%s"/></g>') % (S3, NAVY, NAVY, BLUE, NAVY, NAVY, NAVY, H[2])
    b += '<path d="M727 485 C720 540 790 530 800 580" fill="none" stroke="%s" stroke-width="10" stroke-linecap="round"/>' % NAVY
    return frame(800, 600, 'Powder coating illustration', b, defs=defs)


# ---------------------------------------------------------------- products (800x600)
def p_under_bracket():
    b = shadow(400, 510, 280)
    b += tube('M400 300 L400 470', 46)
    sh = [('l', 230, 300, 570, 300, 120), ('c', 230, 300, 66), ('c', 570, 300, 66)]
    b += solid(sh, top='#3b4f69', side='#1f2e42', depth=(0, 22))
    for x in (230, 570):
        b += bush(x, 300, 42)
    b += bush(400, 300, 24)
    for x, s in ((164, 1), (636, -1)):
        b += line(x, 300, x + s * 22, 300, 5, NAVY)
        b += '<rect x="%d" y="262" width="14" height="22" rx="3" fill="%s" stroke="%s" stroke-width="2"/>' % (x + s * 6 - 7, S2, NAVY)
    return frame(800, 600, 'Under-bracket assembly illustration', b)


def p_fork_side(kind):
    A, T, off = (300, 470), (450, 70), (78, -18)
    pt = lambda t, o=(0, 0): (A[0] + t * (T[0] - A[0]) + o[0], A[1] + t * (T[1] - A[1]) + o[1])

    def leg(o, dim=False):
        (x0, y0), (x1, y1), (x2, y2) = pt(0, o), pt(.5, o), pt(1, o)
        s = tube('M%s %s L%s %s' % (f(pt(.42, o)[0]), f(pt(.42, o)[1]), f(x2), f(y2)), 30, S1, '#fff')
        s += tube('M%s %s L%s %s' % (f(x0), f(y0), f(x1), f(y1)), 48, '#4a5a70' if not dim else '#6c7c93', S3)
        s += '<circle cx="%s" cy="%s" r="26" fill="%s" stroke="%s" stroke-width="3"/><circle cx="%s" cy="%s" r="10" fill="%s"/>' % (
            f(x0), f(y0), S3, NAVY, f(x0), f(y0), NAVY)
        return s
    b = shadow(380, 530, 260)
    b += leg(off, True)
    ax, ay = A[0] + off[0] / 2, A[1] + off[1] / 2
    if kind == 'disc':
        b += '<circle cx="%s" cy="%s" r="112" fill="%s" stroke="%s" stroke-width="3"/>' % (f(ax), f(ay), S2, NAVY)
        b += '<circle cx="%s" cy="%s" r="72" fill="%s" stroke="%s" stroke-width="3"/>' % (f(ax), f(ay), BG, NAVY)
        for a in range(0, 360, 30):
            r = math.radians(a)
            b += '<circle cx="%s" cy="%s" r="6" fill="%s"/>' % (f(ax + 92 * math.cos(r)), f(ay + 92 * math.sin(r)), S4)
        for a in range(0, 360, 72):
            r = math.radians(a)
            b += line(ax, ay, ax + 72 * math.cos(r), ay + 72 * math.sin(r), 14, S3)
        b += '<rect x="-30" y="-42" width="60" height="84" rx="12" fill="%s" stroke="%s" stroke-width="3" transform="translate(%s %s) rotate(-30)"/>' % (
            H[0], NAVY, f(ax + 70), f(ay - 74))
    else:
        b += '<circle cx="%s" cy="%s" r="84" fill="%s" stroke="%s" stroke-width="3"/>' % (f(ax), f(ay), S3, NAVY)
        b += '<circle cx="%s" cy="%s" r="62" fill="%s" stroke="%s" stroke-width="3"/>' % (f(ax), f(ay), S2, NAVY)
        for a in range(0, 360, 20):
            r = math.radians(a)
            b += line(ax + 64 * math.cos(r), ay + 64 * math.sin(r), ax + 80 * math.cos(r), ay + 80 * math.sin(r), 4, S4)
        b += line(ax, ay, ax + 150, ay - 40, 20, NAVY) + line(ax, ay, ax + 150, ay - 40, 14, S4)
    b += leg((0, 0))
    sx, sy = pt(.86, (off[0] / 2, off[1] / 2))
    b += tube('M%s %s L%s %s' % (f(sx), f(sy), f(sx + 20), f(sy - 100)), 26, S3)
    for t in (.78, .97):
        (x1, y1), (x2, y2) = pt(t, (-16, 4)), pt(t, (off[0] + 16, off[1] - 4))
        b += line(x1, y1, x2, y2, 36, NAVY) + line(x1, y1, x2, y2, 30, '#3b4f69')
    return frame(800, 600, 'Telescopic suspension fork illustration, %s brake' % kind, b)


def p_fork_front(slider, stanchion):
    b = shadow(400, 535, 250)
    xs = (300, 500)
    b += '<rect x="330" y="452" width="140" height="78" rx="12" fill="%s" stroke="%s" stroke-width="3"/>' % (S3, NAVY)
    for y in (470, 492, 514):
        b += line(342, y, 458, y, 3, S4)
    b += line(276, 491, 524, 491, 10, NAVY)
    for x in xs:
        b += tube('M%d 70 L%d 300' % (x, x), stanchion, S1, '#fff')
        b += tube('M%d 280 L%d 480' % (x, x), slider, '#4a5a70', S3)
        b += '<circle cx="%d" cy="491" r="%s" fill="%s" stroke="%s" stroke-width="3"/>' % (x, f(slider * .5), S3, NAVY)
        b += '<circle cx="%d" cy="491" r="9" fill="%s"/>' % (x, NAVY)
    b += tube('M400 40 L400 170', 30, S3)
    for y in (90, 160):
        b += union([('l', 270, y, 530, y, 34)], '#3b4f69')
        for x in xs:
            b += '<circle cx="%d" cy="%d" r="7" fill="%s"/>' % (x, y, S1)
    return frame(800, 600, 'Telescopic suspension fork illustration', b)


def p_steering(kind):
    b = shadow(420, 520, 260)
    if kind == 'cargo':
        d = 'M300 90 L370 340 Q384 392 432 414 L590 478'
        b += tube(d, 42)
        bands = [((318, 152), (336, 216)), ((346, 258), (362, 314))]
        b += solid([('p', [(560, 440), (650, 476), (632, 528), (540, 494)])], top=S2, side=S4, depth=(0, 14))
        b += bush(598, 486, 18)
    else:
        b += tube('M300 90 L500 470', 42)
        bands = [((334, 156), (366, 216)), ((390, 262), (422, 322))]
        b += solid([('c', 500, 470, 62)], top=S2, side=S4, depth=(0, 14))
        b += '<circle cx="500" cy="470" r="28" fill="%s" stroke="%s" stroke-width="3"/>' % (S3, NAVY)
        for a in range(0, 360, 60):
            r = math.radians(a)
            b += '<circle cx="%s" cy="%s" r="7" fill="%s"/>' % (f(500 + 46 * math.cos(r)), f(470 + 46 * math.sin(r)), NAVY)
    for (x1, y1), (x2, y2) in bands:
        b += line(x1, y1, x2, y2, 66, NAVY, 'butt') + line(x1, y1, x2, y2, 60, S4, 'butt') + line(x1, y1, x2, y2, 8, S2, 'butt', 'transform="translate(-16 4)"')
    b += '<g transform="translate(300 90) rotate(-16)">' + solid([('l', -80, 0, 80, 0, 46)], top=BLUE, side=NAVY, depth=(0, 12))
    b += bush(-56, 0, 14) + bush(56, 0, 14) + '</g>'
    return frame(800, 600, 'Steering column illustration, %s' % kind, b)


def p_front_fork_cargo():
    b = shadow(400, 525, 230)
    b += tube('M400 40 L400 200', 44)
    for x0, x1 in ((322, 302), (478, 498)):
        b += tube('M%d 230 Q%d 360 %d 470' % (x0, x0 - (x0 - x1) * 3, x1), 40, S3)
    b += solid([('l', 300, 220, 500, 220, 54)], top=BLUE, side=NAVY, depth=(0, 12))
    for x in (302, 498):
        b += solid([('c', x, 482, 32)], top=S2, side=S4, depth=(0, 10)) + bush(x, 482, 14)
    b += line(334, 482, 466, 482, 8, NAVY, extra='stroke-dasharray="10 8"')
    return frame(800, 600, 'Three-wheeler cargo front fork illustration', b)


def p_bucket_link():
    b = shadow(410, 500, 290)
    sh = [('l', 250, 340, 560, 270, 112), ('c', 250, 340, 88), ('c', 560, 270, 88)]
    b += solid(sh, top=S2, side=S4, depth=(0, 28))
    b += bush(250, 340, 46) + bush(560, 270, 46)
    b += '<path d="M330 330 L480 296" stroke="%s" stroke-width="3" opacity=".7"/>' % S3
    return frame(800, 600, 'Excavator bucket link illustration', b)


def p_link_arm():
    b = shadow(400, 500, 290)
    c = [(190, 390), (330, 262), (480, 232), (620, 300)]
    sh = [('l', x1, y1, x2, y2, 84) for (x1, y1), (x2, y2) in zip(c, c[1:])]
    sh += [('c', 190, 390, 70), ('c', 620, 300, 70), ('c', 480, 232, 56)]
    b += solid(sh, top=S2, side=S4, depth=(0, 26))
    b += bush(190, 390, 36) + bush(620, 300, 36) + bush(480, 232, 26)
    return frame(800, 600, 'Excavator link arm illustration', b)


def p_dozer():
    defs = '<linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset=".55" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>' % (S3, S1, S2)
    b = shadow(420, 500, 300)
    b += line(470, 330, 740, 470, 46, NAVY) + line(470, 330, 740, 470, 40, S4)
    b += '<path d="M160 160 L640 120 Q600 270 650 400 L190 432 Q130 300 160 160 Z" fill="url(#g)" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % NAVY
    b += '<path d="M160 160 L640 120" stroke="%s" stroke-width="16" stroke-linecap="round"/>' % S4
    b += '<polygon points="190,432 650,400 654,428 194,462" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % ('#3b4f69', NAVY)
    for i in range(1, 9):
        x, y = 190 + i * 51, 432 - i * 3.6 + 15
        b += '<circle cx="%s" cy="%s" r="5" fill="%s"/>' % (f(x), f(y), S1)
    b += '<path d="M160 160 Q130 300 190 432 L176 436 Q114 300 146 162 Z" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % (S4, NAVY)
    return frame(800, 600, 'Dozer blade illustration', b, defs=defs)


def iso(x, y, z, k=1.15, c=(400, 330)):
    return (c[0] + (x - y) * .866 * k, c[1] + (x + y) * .5 * k - z * k)


def beam(p1, p2, w=26, color=S3):
    (x1, y1), (x2, y2) = p1, p2
    return line(x1, y1, x2, y2, w + 6, NAVY, 'square') + line(x1, y1, x2, y2, w, color, 'square') + \
        line(x1, y1, x2, y2, w * .28, S1, 'butt', 'transform="translate(0 %s)"' % f(-w * .28))


def p_engine_frame():
    X, Y = 170, 110
    b = shadow(400, 470, 300)
    P = lambda x, y, z=0: iso(x, y, z)
    b += beam(P(-X, -Y), P(X, -Y)) + beam(P(-X, -Y), P(-X, Y))
    for x in (-60, 60):
        b += beam(P(x, -Y), P(x, Y), 22, S2)
    for x in (-60, 60):
        for y in (-40, 40):
            (px, py) = P(x, y)
            b += '<rect x="%s" y="%s" width="30" height="40" fill="%s" stroke="%s" stroke-width="3"/>' % (f(px - 15), f(py - 40), BLUE, NAVY)
            b += '<ellipse cx="%s" cy="%s" rx="17" ry="8" fill="%s" stroke="%s" stroke-width="3"/>' % (f(px), f(py - 40), H[2], NAVY)
    b += beam(P(X, -Y), P(X, Y)) + beam(P(-X, Y), P(X, Y))
    for x, y in ((-X, Y), (X, Y), (X, -Y)):
        (px, py) = P(x, y)
        b += '<circle cx="%s" cy="%s" r="9" fill="%s" stroke="%s" stroke-width="2"/>' % (f(px), f(py), S1, NAVY)
    return frame(800, 600, 'Excavator engine frame illustration', b)


def p_chassis():
    d = 'M120 200 L690 200 L690 360 L600 360 A110 110 0 0 0 380 360 L120 360 Z'
    b = shadow(420, 470, 300)
    b += union([('d', d)], S3, 70, -50)
    for x, y in ((120, 200), (690, 200), (120, 360), (690, 360)):
        b += line(x, y, x + 70, y - 50, 22, NAVY) + line(x, y, x + 70, y - 50, 16, S4)
    b += solid([('d', d)], top=S2, side=S4, depth=(0, 16))
    for x in (170, 250):
        b += bush(x, 290, 18)
    b += bush(650, 290, 24)
    b += '<path d="M600 360 A110 110 0 0 0 380 360" fill="none" stroke="%s" stroke-width="10" opacity=".8"/>' % H[2]
    return frame(800, 600, 'Vibrating compactor rear chassis frame illustration', b)


def p_star_plate():
    cx, cy = 400, 285
    b = shadow(400, 500, 250)
    sh = [('c', cx, cy, 96)]
    ends = []
    for i in range(5):
        a = math.radians(-90 + i * 72)
        ex, ey = cx + 175 * math.cos(a), cy + 175 * math.sin(a)
        ends.append((ex, ey))
        sh += [('l', cx, cy, ex, ey, 74), ('c', ex, ey, 46)]
    b += solid(sh, top=S2, side=S4, depth=(0, 24))
    for ex, ey in ends:
        b += bush(ex, ey, 20)
    b += bush(cx, cy, 40)
    for i in range(6):
        a = math.radians(i * 60)
        b += '<circle cx="%s" cy="%s" r="7" fill="%s"/>' % (f(cx + 66 * math.cos(a)), f(cy + 66 * math.sin(a)), NAVY)
    return frame(800, 600, 'Crawler frame star plate illustration', b)


def p_axle():
    b = shadow(400, 500, 330)
    b += line(220, 400, 580, 400, 20, NAVY) + line(220, 400, 580, 400, 14, S4)
    for x, s in ((200, 1), (600, -1)):
        b += line(x, 330, x + s * 20, 400, 16, NAVY) + line(x, 330, x + s * 20, 400, 10, S3)
        b += '<circle cx="%d" cy="400" r="13" fill="%s" stroke="%s" stroke-width="3"/>' % (x + s * 20, S2, NAVY)
    b += solid([('p', [(220, 278), (580, 278), (610, 318), (190, 318)])], top=BLUE, side=NAVY, depth=(0, 14))
    b += solid([('c', 400, 300, 50)], top=BLUE, side=NAVY, depth=(0, 14)) + bush(400, 300, 24)
    for x, s in ((180, -1), (620, 1)):
        b += '<rect x="%d" y="250" width="40" height="110" rx="8" fill="%s" stroke="%s" stroke-width="3"/>' % (x - 20, S3, NAVY)
        b += line(x + s * 20, 305, x + s * 70, 305, 30, NAVY, 'butt') + line(x + s * 20, 305, x + s * 70, 305, 24, S2, 'butt')
        hx = x + s * 80
        b += '<rect x="%d" y="225" width="26" height="160" rx="8" fill="%s" stroke="%s" stroke-width="3"/>' % (hx - 13, S2, NAVY)
        for y in (250, 280, 330, 360):
            b += '<circle cx="%d" cy="%d" r="5" fill="%s"/>' % (hx, y, NAVY)
    return frame(800, 600, 'Tractor front axle assembly illustration', b)


# ---------------------------------------------------------------- sections
def s_shop_floor():
    W, Hh = 800, 700
    defs = ('<pattern id="mesh" width="18" height="18" patternUnits="userSpaceOnUse">'
            '<path d="M0 0L18 18M18 0L0 18" stroke="%s" stroke-width="1.2" opacity=".6"/></pattern>' % S3)
    b = '<rect width="800" height="300" fill="#dbe4ee"/>'
    for x in range(30, 800, 130):
        b += '<rect x="%d" y="40" width="100" height="70" fill="#f7f9fc" stroke="%s" stroke-width="3"/>' % (x, S2)
    b += '<polygon points="0,300 800,300 800,700 0,700" fill="#cdd8e4"/>'
    vx, vy = 400, 200
    for x in range(-600, 1500, 140):
        t = (700 - 300) / (700 - vy)
        b += line(x, 700, x + (vx - x) * t, 300, 2, S3, 'butt', 'opacity=".7"')
    for y in (360, 450, 570):
        b += line(0, y, 800, y, 2, S3, 'butt', 'opacity=".5"')
    b += '<polygon points="40,640 470,640 430,600 70,600" fill="%s" opacity=".55"/>' % H[5]
    b += '<rect x="40" y="170" width="520" height="200" fill="url(#mesh)" stroke="%s" stroke-width="3"/>' % S3
    for x in (40, 213, 386, 560):
        b += '<rect x="%d" y="160" width="10" height="214" fill="%s"/>' % (x - 5, NAVY)
    b += line(140, 0, 140, 60, 3, NAVY) + line(460, 0, 460, 60, 3, NAVY)
    b += '<path d="M110 60 h60 l-12 18 h-36z M430 60 h60 l-12 18 h-36z" fill="%s"/>' % NAVY
    b += arm([(500, 420), (540, 270), (440, 300), (380, 470)], 28)
    b += '<polygon points="170,500 420,462 520,510 270,556" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % (S3, NAVY)
    b += '<polygon points="170,500 270,556 270,580 170,524" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % (S4, NAVY)
    b += '<polygon points="270,556 520,510 520,534 270,580" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % (NAVY, NAVY)
    for x, y in ((180, 528), (262, 584), (512, 536)):
        b += line(x, y, x, y + 70, 12, NAVY, 'butt')
    b += tube('M260 500 L400 478 L440 498', 18, S2)
    b += tube('M300 520 L360 470', 18, S2)
    b += arm([(150, 520), (130, 340), (270, 360), (330, 470)], 30)
    b += glow(370, 482, 11) + sparks(370, 484, 14, 11, (160, 380), (16, 50))
    return frame(W, Hh, 'Robotic welding cell on the shop floor, illustration', b, corner='bl', bg='#dbe4ee', defs=defs)


def person(x, base, h, suit, skin, vest=None):
    hd = h * .075
    o = ''
    for dx in (-1, 1):
        o += line(x + dx * h * .06, base - h * .46, x + dx * h * .07, base - h * .02, h * .095, NAVY)
    o += '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="3"/>' % (
        f(x - h * .14), f(base - h * .83), f(h * .28), f(h * .42), f(h * .07), suit, NAVY)
    if vest:
        o += '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (f(x - h * .13), f(base - h * .7), f(h * .26), f(h * .05), vest)
        o += '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (f(x - h * .13), f(base - h * .58), f(h * .26), f(h * .05), vest)
    for dx in (-1, 1):
        o += line(x + dx * h * .15, base - h * .78, x + dx * h * .19, base - h * .5, h * .07, suit)
    o += '<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="3"/>' % (f(x), f(base - h * .9), f(hd), skin, NAVY)
    o += '<path d="M%s %s a%s %s 0 0 1 %s 0 z" fill="%s" stroke="%s" stroke-width="3"/>' % (
        f(x - hd * 1.15), f(base - h * .92), f(hd * 1.15), f(hd * 1.15), f(hd * 2.3), H[5], NAVY)
    o += line(x - hd * 1.45, base - h * .92, x + hd * 1.45, base - h * .92, 5, NAVY)
    return o


def s_team():
    W, Hh = 800, 560
    b = '<rect width="800" height="330" fill="#d6e0eb"/><rect y="330" width="800" height="230" fill="#c6d2df"/>'
    b += '<rect x="260" y="150" width="200" height="180" fill="%s" opacity=".7"/>' % S2
    b += '<rect x="470" y="110" width="280" height="220" fill="%s" opacity=".6"/>' % S3
    b += '<circle cx="610" cy="220" r="70" fill="none" stroke="%s" stroke-width="16" opacity=".6"/>' % S4
    b += line(180, 40, 800, 40, 14, NAVY, 'butt', 'opacity=".5"')
    for x in range(260, 800, 120):
        b += '<rect x="%d" y="60" width="80" height="50" fill="#f7f9fc" opacity=".8"/>' % x
    b += shadow(520, 505, 300, 18)
    crew = [(310, 470, BLUE, '#a8714d', None), (405, 500, NAVY, '#d7a27c', H[2]), (500, 480, BLUE, '#8d5a3b', None),
            (595, 495, '#2a5d94', '#c58c64', H[2]), (690, 470, NAVY, '#e0b08c', None)]
    for x, h, suit, skin, vest in crew:
        b += person(x, 505, h * .78 + 20, suit, skin, vest)
    return frame(W, Hh, 'Production team at Unit 2, illustration', b, corner=None, bg='#d6e0eb')


JOBS = {
    'assets/images/processes/plasma-cutting.svg': proc_cut,
    'assets/images/processes/tube-bending.svg': proc_bend,
    'assets/images/processes/welding.svg': proc_weld,
    'assets/images/processes/heat-treatment.svg': proc_heat,
    'assets/images/processes/aluminium-casting.svg': proc_cast,
    'assets/images/processes/surface-finish.svg': proc_coat,
    'assets/images/products/under-bracket.svg': p_under_bracket,
    'assets/images/products/fork-2w-disc.svg': lambda: p_fork_side('disc'),
    'assets/images/products/fork-2w-drum.svg': lambda: p_fork_side('drum'),
    'assets/images/products/steering-column-cargo.svg': lambda: p_steering('cargo'),
    'assets/images/products/steering-column-passenger.svg': lambda: p_steering('passenger'),
    'assets/images/products/front-fork-cargo.svg': p_front_fork_cargo,
    'assets/images/products/fork-3w-41.svg': lambda: p_fork_front(58, 40),
    'assets/images/products/fork-3w-30.svg': lambda: p_fork_front(46, 30),
    'assets/images/products/bucket-link.svg': p_bucket_link,
    'assets/images/products/link-arm.svg': p_link_arm,
    'assets/images/products/dozer-blade.svg': p_dozer,
    'assets/images/products/engine-frame.svg': p_engine_frame,
    'assets/images/products/rear-chassis-frame.svg': p_chassis,
    'assets/images/products/star-plate.svg': p_star_plate,
    'assets/images/products/front-axle.svg': p_axle,
    'assets/images/sections/shop-floor.svg': s_shop_floor,
    'assets/images/sections/team.svg': s_team,
}

for rel, fn in JOBS.items():
    save(rel, fn())
