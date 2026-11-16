#!/usr/bin/env python3
"""NoBaCor Installationsordner – technische Variante.
Maße aus Druckvorlage 'Aktenordner 2-Loch 350 A4' (WIRmachenDRUCK):
Datenformat 673 x 351 mm, Endformat 637 x 315 mm, 18 mm Umschlag, 3 mm Sicherheitsabstand.
Alle Koordinaten in mm (Datenformat, Ursprung oben links)."""
import sys

W, H = 673, 351
T0X, T1X, T0Y, T1Y = 18, 655, 18, 333          # Endformat
# Falzlinien (außen, von links): Rückdeckel | Gelenk | Rücken | Gelenk | Titelseite
F_BACK, F_SP0, F_SP1, F_FRONT = 302, 310, 363, 371
RIVET = (232, 292)                               # Nietenbereich Hebelmechanik (Rückdeckel)
POCKET = (318.5, 88, 354.5, 224)                 # Rückentasche 30x130 (Außenkontur)

GRAPHITE = "#1F2A30"; STEEL = "#56656C"; MID = "#8A979D"; HAIR = "#B7C2C7"
BG = "#EEF1F2"; WHITE = "#FFFFFF"
BLUE = "#1E6DE8"; GREEN = "#12812C"; COPPER = "#B65D20"
HEAD = "Outfit, Hanken Grotesk, Arial, sans-serif"
BODY = "Hanken Grotesk, Arial, sans-serif"

BARS = [(-38.80, -6.5, 4.7, 13), (-30.25, -10.5, 4.7, 21), (-21.70, -17, 4.7, 34),
        (-13.15, -24, 5.2, 48), (-4.10, -13.5, 4.7, 27), (4.45, -30, 5.4, 60),
        (13.70, -18, 4.7, 36), (22.25, -10.5, 4.7, 21), (30.80, -5.5, 4.7, 11)]


def signet(cx, cy, s, fill=None, stroke=None, sw=0.3):
    """Signet (Frequenzsignal) – zentriert auf cx/cy, Breite ~83*s mm."""
    st = f'fill="{fill}"' if fill else f'fill="none" stroke="{stroke}" stroke-width="{sw/s:.3f}"'
    o = [f'<g transform="translate({cx:.2f} {cy:.2f}) scale({s})" {st}>']
    for x, y, w, h in BARS:
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w/2:.2f}"/>')
    o.append('<circle cx="40.2" cy="6" r="3.8"/></g>')
    return "".join(o)


def t(x, y, s, size, fam=BODY, w=400, fill=GRAPHITE, anchor="start", ls=0, extra=""):
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{fam}" font-size="{size}" font-weight="{w}" '
            f'fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}" {extra}>{s}</text>')


def line(x1, y1, x2, y2, c=GRAPHITE, w=0.25, extra=""):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{c}" stroke-width="{w}" {extra}/>'


def rect(x, y, w, h, fill="none", stroke=None, sw=0.25, extra=""):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}"{s} {extra}/>'


def crosses(x0, y0, x1, y1, step=10, c=HAIR, skip=None):
    """Technisches Kreuzraster (wie Zeichenpapier)."""
    o = ['<g stroke="%s" stroke-width="0.15">' % c]
    y = y0
    while y <= y1 + 0.01:
        x = x0
        while x <= x1 + 0.01:
            if not (skip and skip(x, y)):
                o.append(f'<path d="M{x-0.8:.1f} {y:.1f}h1.6M{x:.1f} {y-0.8:.1f}v1.6"/>')
            x += step
        y += step
    o.append("</g>")
    return "".join(o)


def corner_marks(x0, y0, x1, y1, L=4, c=GRAPHITE, w=0.35):
    p = (f"M{x0} {y0+L}V{y0}H{x0+L} M{x1-L} {y0}H{x1}V{y0+L} "
         f"M{x1} {y1-L}V{y1}H{x1-L} M{x0+L} {y1}H{x0}V{y1-L}")
    return f'<path d="{p}" fill="none" stroke="{c}" stroke-width="{w}"/>'


def brand_ticks(x, y, L=12, h=0.9, gap=1.2):
    """Dezente Markenfarben-Kennung: drei kurze Segmente."""
    return "".join(rect(x + i * (L + gap), y, L, h, fill=c) for i, c in enumerate([BLUE, GREEN, COPPER]))


def ruler(x0, y0, length=200):
    o = ['<g stroke="%s" stroke-width="0.14">' % GRAPHITE]
    for mm in range(length + 1):
        L = 3.2 if mm % 10 == 0 else (2.0 if mm % 5 == 0 else 1.1)
        o.append(f'<path d="M{x0+mm} {y0}v{L}"/>')
    o.append("</g>")
    for mm in range(0, length + 1, 10):
        o.append(t(x0 + mm, y0 + 5.6, str(mm), 1.7, w=500, fill=STEEL, anchor="middle"))
    o.append(t(x0 + length + 2.5, y0 + 2.2, "mm", 1.7, w=500, fill=STEEL))
    return "".join(o)


def arrow(x, y, d, c=GRAPHITE, s=1.6):
    pts = {"r": f"{x-s},{y-s*0.6} {x},{y} {x-s},{y+s*0.6}", "l": f"{x+s},{y-s*0.6} {x},{y} {x+s},{y+s*0.6}",
           "u": f"{x-s*0.6},{y+s} {x},{y} {x+s*0.6},{y+s}", "d": f"{x-s*0.6},{y-s} {x},{y} {x+s*0.6},{y-s}"}[d]
    return f'<polygon points="{pts}" fill="{c}"/>'


def valve(x, y, vertical=False, s=2.2):
    if vertical:
        p = f"M{x-s} {y-s}L{x+s} {y+s}L{x-s} {y+s}L{x+s} {y-s}Z"
    else:
        p = f"M{x-s} {y-s}L{x+s} {y+s}L{x+s} {y-s}L{x-s} {y+s}Z"
    return f'<path d="{p}" fill="{BG}" stroke="{GRAPHITE}" stroke-width="0.3"/>'


def tag(x, y, s, anchor="middle"):
    return t(x, y, s, 1.9, w=600, fill=STEEL, anchor=anchor, ls=0.25)


def schematic(ox, oy):
    """Vereinfachtes Fließschema eines Kühlkreislaufs (illustrativ)."""
    g = [f'<g id="Fliessschema" transform="translate({ox} {oy}) scale(1.08)">']
    P = dict(stroke=GRAPHITE)
    # Leitungen
    g.append(f'<path d="M24 62 H150 V54 M164 28 V18 H24 V29" fill="none" stroke="{GRAPHITE}" stroke-width="0.45"/>')
    g.append(f'<path d="M14 54 V62 H24" fill="none" stroke="{GRAPHITE}" stroke-width="0.45"/>')
    # Kühlturm
    g.append(f'<path d="M6 54 L10 30 H32 L36 54 Z" fill="{WHITE}" stroke="{GRAPHITE}" stroke-width="0.4"/>')
    g.append(f'<path d="M12 36 H30 M11 42 H31 M10 48 H32" stroke="{HAIR}" stroke-width="0.3"/>')
    g.append(f'<ellipse cx="21" cy="30" rx="7" ry="1.6" fill="{WHITE}" stroke="{GRAPHITE}" stroke-width="0.35"/>')
    g.append(tag(3, 42, "KT-01", anchor="end") + t(21, 70, "KÜHLTURM", 1.8, w=500, fill=MID, anchor="middle", ls=0.3))
    # Pumpe
    g.append(f'<circle cx="52" cy="62" r="4.2" fill="{WHITE}" stroke="{GRAPHITE}" stroke-width="0.4"/>')
    g.append(f'<path d="M49.4 59 L56 62 L49.4 65" fill="none" stroke="{GRAPHITE}" stroke-width="0.35"/>')
    g.append(tag(52, 55.5) if False else tag(52, 55.6, "P-01") + t(52, 70, "PUMPE", 1.8, w=500, fill=MID, anchor="middle", ls=0.3))
    g.append(valve(70, 62))
    # NoBaCor Einheit
    g.append(rect(82, 55, 34, 14, fill=WHITE, stroke=BLUE, sw=0.55))
    g.append(signet(90.5, 62, 0.085, fill=BLUE))
    g.append(t(97, 63.3, "NoBaCor", 3.1, fam=HEAD, w=600, fill=GRAPHITE))
    g.append(t(99, 52.6, "NBC-01", 1.9, w=600, fill=BLUE, anchor="middle", ls=0.25))
    g.append(valve(128, 62))
    # Wärmetauscher
    g.append(rect(150, 28, 14, 26, fill=WHITE, stroke=GRAPHITE, sw=0.4))
    g.append(f'<path d="M150 33 L164 37 L150 41 L164 45 L150 49" fill="none" stroke="{GRAPHITE}" stroke-width="0.3"/>')
    g.append(tag(147, 33, "WT-01", anchor="end") + t(147, 37.5, "WÄRMETAUSCHER", 1.8, w=500, fill=MID, anchor="end", ls=0.3))
    # Messstelle
    g.append(f'<circle cx="140" cy="18" r="2.6" fill="{WHITE}" stroke="{GRAPHITE}" stroke-width="0.35"/>')
    g.append(t(140, 18.7, "TI", 1.6, w=700, anchor="middle"))
    g.append(line(140, 15.4, 140, 11.5, w=0.25) + tag(140, 10, "TI-01"))
    # Flussrichtung
    for x in (40, 100, 172):
        pass
    g.append(arrow(40, 62, "r") + arrow(140 - 10, 62, "r") + arrow(164, 23, "u") + arrow(80, 18, "l") + arrow(24, 26.5, "d") if False else "")
    g.append(arrow(40, 62, "r") + arrow(142, 62, "r") + arrow(164, 23, "u") + arrow(80, 18, "l"))
    # Legende
    g.append(t(0, 80, "VORLAUF / RÜCKLAUF – SCHEMATISCHE DARSTELLUNG", 1.7, w=600, fill=MID, ls=0.35))
    g.append("</g>")
    return "".join(g)


def field(x, y, w, h, label, hint=""):
    o = [rect(x, y, w, h, fill=WHITE, stroke=GRAPHITE, sw=0.3)]
    o.append(t(x + 1.8, y + 3.6, label, 2.1, w=700, fill=STEEL, ls=0.3))
    if hint:
        o.append(t(x + w - 1.8, y + 3.6, hint, 1.8, w=500, fill=MID, anchor="end", ls=0.2))
    return "".join(o)


def seal(cx, cy, top, main, bottom, main_size=4.2, extra=""):
    """Technische Siegel-Platzhalter (monochrom) – vor Druck gegen Original-Logos tauschen."""
    o = [f'<g class="Auszeichnung_Platzhalter">']
    o.append(f'<circle cx="{cx}" cy="{cy}" r="15" fill="{WHITE}" stroke="{GRAPHITE}" stroke-width="0.45"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="13" fill="none" stroke="{HAIR}" stroke-width="0.25" stroke-dasharray="0.6 0.6"/>')
    o.append(t(cx, cy - 6.2, top, 1.75, w=700, fill=STEEL, anchor="middle", ls=0.35))
    for i, m in enumerate(main):
        o.append(t(cx, cy + 0.6 + i * (main_size + 0.6) - (len(main) - 1) * (main_size + 0.6) / 2 + main_size * 0.35,
                   m, main_size, fam=HEAD, w=600, fill=GRAPHITE, anchor="middle"))
    o.append(t(cx, cy + 9.3, bottom, 1.75, w=700, fill=STEEL, anchor="middle", ls=0.35))
    o.append(extra)
    o.append("</g>")
    return "".join(o)


def awards(x0, x1, y0, y1):
    """Leiste mit vier Auszeichnungen."""
    o = ['<g id="Auszeichnungen">']
    o.append(rect(x0, y0, x1 - x0, 6.5, fill=GRAPHITE))
    o.append(t(x0 + 3, y0 + 4.5, "AUSZEICHNUNGEN &amp; QUALITÄT", 2.4, w=700, fill=WHITE, ls=0.6))
    o.append(rect(x0, y0, x1 - x0, y1 - y0, stroke=GRAPHITE, sw=0.5))
    cw = (x1 - x0) / 4
    cy = y0 + 6.5 + (y1 - y0 - 6.5) / 2
    for i in range(1, 4):
        o.append(line(x0 + i * cw, y0 + 6.5, x0 + i * cw, y1, w=0.25))
    flag = "".join(rect(x0 + cw * 3.5 - 6 + k * 4, cy + 11.4 - 9.3 - 7.6, 4, 0.9, fill=c)
                   for k, c in enumerate(["#000000", "#DD0000", "#FFCE00"]))
    o.append(seal(x0 + cw * 0.5, cy, "GERMAN", ["INNOVATION", "AWARD"], "WINNER 2021", main_size=3.1))
    o.append(seal(x0 + cw * 1.5, cy, "GREEN PRODUCT", ["AWARD"], "FINALIST 2025", main_size=4.4))
    o.append(seal(x0 + cw * 2.5, cy, "ISO", ["9001"], "ZERTIFIZIERT", main_size=6.4))
    o.append(seal(x0 + cw * 3.5, cy, "", ["MADE IN", "GERMANY"], "", main_size=3.6, extra=flag))
    o.append("</g>")
    return "".join(o)


def icon(kind, x, y, s=12):
    """Linien-Icons für USPs (x/y = linke obere Ecke, s = Kantenlänge)."""
    o = [rect(x, y, s, s, fill=GRAPHITE)]
    st = f'fill="none" stroke="{WHITE}" stroke-width="0.55" stroke-linejoin="round" stroke-linecap="round"'
    k = s / 12
    g = f'<g transform="translate({x} {y}) scale({k})">'
    if kind == "energy":
        g += f'<path d="M6.8 2.2 L3.6 6.6 H6 L5.2 9.8 L8.4 5.4 H6 Z" {st}/>'
    elif kind == "chem":
        g += f'<path d="M4.8 2.4 H7.2 M5.2 2.4 V5 L2.9 9.1 Q2.6 9.8 3.4 9.8 H8.6 Q9.4 9.8 9.1 9.1 L6.8 5 V2.4" {st}/>'
        g += f'<path d="M3.9 7.6 H8.1" {st}/><line x1="4.2" y1="7.6" x2="3.2" y2="9.5" stroke="none"/>'
        g += f'<path d="M7.4 1.2 L9.6 3.4 M9.6 1.2 L7.4 3.4" {st}/>'
    elif kind == "safe":
        g += f'<path d="M6 1.8 L9.4 3.1 V6 Q9.4 8.9 6 10.3 Q2.6 8.9 2.6 6 V3.1 Z" {st}/>'
        g += f'<path d="M4.5 6.1 L5.6 7.2 L7.7 4.9" {st}/>'
    g += "</g>"
    o.append(g)
    return "".join(o)


def outside(guides=False):
    o = []
    o.append(f'<g id="01_Hintergrund">{rect(0, 0, W, H, fill=BG)}')
    o.append(crosses(28, 28, 296, 323, skip=lambda x, y: RIVET[0] - 2 < x < RIVET[1] + 2))
    o.append(crosses(381, 28, 655, 323))
    # Rücken + Gelenke in Graphit, 3 mm über die Falz hinaus (Falztoleranz)
    o.append(rect(F_BACK - 3, 0, (F_FRONT + 3) - (F_BACK - 3), H, fill=GRAPHITE))
    o.append("</g>")

    # ---------- TITELSEITE ----------
    fx0, fx1, fy0, fy1 = 432, 645, 28, 323
    o.append('<g id="02_Titelseite">')
    o.append(rect(fx0, fy0, fx1 - fx0, fy1 - fy0, fill=WHITE, stroke=GRAPHITE, sw=0.35))
    o.append(corner_marks(fx0 - 3, fy0 - 3, fx1 + 3, fy1 + 3))
    o.append(ruler(fx0 + 5, fy0))
    # Logo + Claim
    o.append(signet(fx0 + 17, 51, 0.17, fill=BLUE))
    o.append(t(fx0 + 27, 55.2, "NoBaCor", 11.5, fam=HEAD, w=500, fill=GRAPHITE, ls=-0.1))
    o.append(t(fx0 + 8.6, 68.5, "NO BACTERIA.  NO CORROSION.", 3.3, w=700, fill=GRAPHITE, ls=0.55))
    o.append(t(fx0 + 8.6, 73.8, "IN COOLING SYSTEMS.", 2.6, w=600, fill=MID, ls=0.8))
    o.append(line(fx0 + 8, 82, fx1 - 8, 82, w=0.25))
    o.append(brand_ticks(fx0 + 8, 81.55, L=10, h=0.9, gap=0))
    # Titel
    o.append(t(fx0 + 8, 106, "INSTALLATIONSORDNER", 15.2, fam=HEAD, w=600, fill=GRAPHITE, ls=0.2))
    o.append(t(fx0 + 8.6, 118, "Technische Dokumentation", 6.2, w=400, fill=STEEL))
    o.append(t(fx0 + 8.6, 127, "INSTALLATION  ·  INBETRIEBNAHME  ·  WARTUNG  ·  NACHWEISE", 2.4, w=600, fill=MID, ls=0.55))
    o.append(line(fx0 + 8, 136, fx1 - 8, 136, c=HAIR, w=0.25))
    # Fließschema
    o.append(schematic(fx0 + 22, 148))
    # Auszeichnungen
    o.append(awards(fx0, fx1, 262, fy1))
    o.append("</g>")

    # ---------- RÜCKEN ----------
    cx = (F_SP0 + F_SP1) / 2
    o.append('<g id="03_Ruecken">')
    o.append(signet(cx, 44, 0.36, fill=WHITE))
    o.append(t(cx, 72, "NoBaCor", 8.2, fam=HEAD, w=500, fill=WHITE, anchor="middle"))
    o.append(brand_ticks(cx - 13.2, 78, L=8, h=0.8, gap=1.2))
    px0, py0, px1, py1 = POCKET
    o.append(rect(px0, py0, px1 - px0, py1 - py0, fill="#2B373E", stroke="#4A5960", sw=0.3))
    o.append(t(cx, 278, "INSTALLATIONSORDNER", 5.6, fam=HEAD, w=600, fill=WHITE, anchor="middle", ls=0.35,
               extra=f'transform="rotate(-90 {cx} 278)" dominant-baseline="middle"'))
    o.append(line(F_SP0 + 6, 320, F_SP1 - 6, 320, c="#4A5960", w=0.3))
    o.append(t(cx, 326.0, "nobacor.com", 2.4, w=500, fill="#9FB0B7", anchor="middle", ls=0.2))
    o.append("</g>")

    # ---------- RÜCKDECKEL: USPs ----------
    bx0, bx1, by0, by1 = 28, 222, 28, 323
    o.append('<g id="04_Rueckdeckel_USP">')
    o.append(rect(bx0, by0, bx1 - bx0, by1 - by0, fill=WHITE, stroke=GRAPHITE, sw=0.35))
    o.append(corner_marks(bx0 - 3, by0 - 3, bx1 + 3, by1 + 3))
    o.append(t(bx0 + 10, 50, "IHRE VORTEILE MIT NOBACOR", 2.6, w=700, fill=STEEL, ls=0.6))
    o.append(t(bx0 + 10, 71, "Warum NoBaCor?", 10, fam=HEAD, w=600, fill=GRAPHITE))
    o.append(signet(bx1 - 32, 64, 0.29, stroke=GRAPHITE, sw=0.3))
    o.append(line(bx0 + 10, 92, bx1 - 10, 92, w=0.25))
    o.append(brand_ticks(bx0 + 10, 91.55, L=10, h=0.9, gap=0))
    usps = [("energy", "Geringerer Energieverbrauch", "Lower energy consumption"),
            ("chem", "Weniger Chemikalien zur Wasserbehandlung", "Less treatment chemicals"),
            ("safe", "Höhere Prozesssicherheit", "Higher process reliability")]
    uy = 104
    for i, (k, de, en) in enumerate(usps):
        y = uy + i * 30
        o.append(icon(k, bx0 + 10, y, 14))
        o.append(t(bx0 + 30, y + 3.6, f"{i+1:02d}", 2.4, w=700, fill=BLUE, ls=0.4))
        o.append(t(bx0 + 30, y + 10, de, 5.4, fam=HEAD, w=600, fill=GRAPHITE))
        o.append(t(bx0 + 30, y + 15.6, en.upper(), 2.3, w=600, fill=MID, ls=0.5))
        if i < 2:
            o.append(line(bx0 + 30, y + 22.5, bx1 - 10, y + 22.5, c=HAIR, w=0.25))
    # Claim-Band
    o.append(rect(bx0 + 10, 202, bx1 - bx0 - 20, 22, fill=GRAPHITE))
    o.append(t(bx0 + 16, 212.2, "NO BACTERIA.  NO CORROSION.", 4.2, fam=HEAD, w=600, fill=WHITE, ls=0.5))
    o.append(t(bx0 + 16, 218.6, "IN COOLING SYSTEMS.", 2.4, w=600, fill="#9FB0B7", ls=0.8))
    o.append(signet(bx1 - 26, 213, 0.12, fill=WHITE))
    # Hinweis
    o.append(rect(bx0 + 10, 236, 1.2, 22, fill=BLUE))
    o.append(t(bx0 + 15, 240, "HINWEIS ZUR AUFBEWAHRUNG", 2.3, w=700, fill=GRAPHITE, ls=0.5))
    for i, s in enumerate(["Dieser Ordner enthält die technische Dokumentation Ihrer NoBaCor-Anlage.",
                           "Bitte vollständig und griffbereit in der Nähe der Anlage aufbewahren."]):
        o.append(t(bx0 + 15, 247 + i * 5.5, s, 3.1, w=400, fill=STEEL))
    # Kontakt
    ky = 270
    o.append(line(bx0 + 10, ky, bx1 - 10, ky, w=0.25))
    o.append(signet(bx0 + 20, ky + 20, 0.15, fill=BLUE))
    o.append(t(bx0 + 30, ky + 23.5, "NoBaCor", 8.5, fam=HEAD, w=500, fill=GRAPHITE))
    kx = bx0 + 112
    for i, (k, v) in enumerate([("WEB", "nobacor.com"), ("TEL", "+49 9191 960 910 0"),
                                ("ADRESSE", "Pfaffensee 3"), ("", "91301 Forchheim")]):
        o.append(t(kx, ky + 11 + i * 6, k, 2.0, w=700, fill=MID, ls=0.4))
        o.append(t(kx + 18, ky + 11 + i * 6, v, 3.3, w=500, fill=GRAPHITE))
    o.append("</g>")

    if guides:
        o.append(guide_layer_outside())
    return "".join(o)


def guide_layer_outside():
    g = ['<g id="99_Hilfslinien_NICHT_DRUCKEN" fill="none" stroke-width="0.3">']
    g.append(rect(T0X, T0Y, T1X - T0X, T1Y - T0Y, stroke="#E6007E"))
    g.append(rect(21, 21, 631, 309, stroke="#2D6CDF", extra='stroke-dasharray="2 1"'))
    for x in (F_BACK, F_SP0, F_SP1, F_FRONT):
        g.append(line(x, 0, x, H, c="#00AEEF", w=0.3))
    g.append(rect(RIVET[0], 0, RIVET[1] - RIVET[0], H, fill="#E6007E", extra='fill-opacity="0.15"'))
    g.append(rect(POCKET[0], POCKET[1], POCKET[2] - POCKET[0], POCKET[3] - POCKET[1], stroke="#E6007E", extra='stroke-dasharray="1.5 1"'))
    for y in (124, 203):
        g.append(rect(381, y, 42, 22, fill="#E6007E", extra='fill-opacity="0.15"'))
    g.append(t(262, 12, "NIETEN HEBELMECHANIK", 3, w=700, fill="#E6007E", anchor="middle"))
    g.append(t(402, 120, "RADOÖSEN", 2.6, w=700, fill="#E6007E", anchor="middle"))
    g.append("</g>")
    return "".join(g)


def inside(guides=False):
    o = [f'<g id="01_Hintergrund_innen">{rect(0, 0, W, H, fill=BG)}']
    o.append(crosses(28, 28, 646, 323))
    o.append("</g>")
    # Innenseite links = Innenseite Titelseite (Taschen: CD, Dreieck, Visitenkarte)
    o.append('<g id="02_Innen_links">')
    sx0, sy0 = 190, 30
    o.append(rect(sx0, sy0, 98, 58, fill=WHITE, stroke=GRAPHITE, sw=0.35))
    o.append(rect(sx0, sy0, 98, 6.5, fill=GRAPHITE))
    o.append(t(sx0 + 3, sy0 + 4.5, "SERVICE-KONTAKT", 2.4, w=700, fill=WHITE, ls=0.6))
    o.append(signet(sx0 + 12, sy0 + 19, 0.12, fill=BLUE))
    o.append(t(sx0 + 19.5, sy0 + 21.6, "NoBaCor", 6.4, fam=HEAD, w=500))
    for i, (k, v) in enumerate([("TEL", "+49 9191 960 910 0"), ("WEB", "nobacor.com"),
                                ("ADRESSE", "Pfaffensee 3 · 91301 Forchheim")]):
        o.append(t(sx0 + 5, sy0 + 34 + i * 6.5, k, 2.0, w=700, fill=MID, ls=0.4))
        o.append(t(sx0 + 22, sy0 + 34 + i * 6.5, v, 3.2, w=500))
    o.append(t(sx0, sy0 + 66, "Visitenkarte Ihres Ansprechpartners: Tasche unten links.", 2.6, w=400, fill=STEEL))
    o.append("</g>")
    # Innenseite rechts = Innenseite Rückdeckel (Mechanik bei x ≈ 384–444)
    o.append('<g id="03_Innen_rechts_Register">')
    rx0, rx1, ry0 = 460, 645, 30
    o.append(rect(rx0, ry0, rx1 - rx0, 7.5, fill=GRAPHITE))
    o.append(t(rx0 + 3, ry0 + 5.2, "INHALT / REGISTER", 2.8, w=700, fill=WHITE, ls=0.6))
    items = ["Anlagenübersicht und Fließschema", "Montage- und Installationsprotokoll",
             "Inbetriebnahmeprotokoll", "Betriebsanleitung", "Wartungsplan und Wartungsnachweise",
             "Datenblätter und Zertifikate", "Wasseranalysen und Messprotokolle",
             "Ersatzteile und Zubehör", "Schulungsnachweise", "Korrespondenz und Sonstiges"]
    rh = 12.4
    for i, s in enumerate(items):
        y = ry0 + 7.5 + i * rh
        o.append(rect(rx0, y, rx1 - rx0, rh, fill=WHITE, stroke=GRAPHITE, sw=0.25))
        o.append(rect(rx0, y, 14, rh, fill="#E3E8EA", stroke=GRAPHITE, sw=0.25))
        o.append(t(rx0 + 7, y + rh / 2 + 1.6, f"{i+1:02d}", 4.2, fam=HEAD, w=600, anchor="middle"))
        o.append(t(rx0 + 19, y + rh / 2 + 1.3, s, 3.7, w=500))
    o.append("</g>")
    if guides:
        g = ['<g id="99_Hilfslinien_NICHT_DRUCKEN" fill="none" stroke-width="0.3">']
        g.append(rect(T0X, T0Y, T1X - T0X, T1Y - T0Y, stroke="#E6007E"))
        g.append(rect(38, 42, 140, 121, stroke="#E6007E", extra='stroke-dasharray="1.5 1"'))
        g.append(rect(38, 253, 100, 60, stroke="#E6007E", extra='stroke-dasharray="1.5 1"'))
        g.append(f'<path d="M22 111 L238 333" stroke="#E6007E" stroke-dasharray="1.5 1"/>')
        g.append(rect(380, 112, 68, 146, fill="#E6007E", extra='fill-opacity="0.12"'))
        for x in (F_BACK, F_SP0, F_SP1, F_FRONT):
            g.append(line(x, 0, x, H, c="#00AEEF", w=0.3))
        g.append("</g>")
        o.append("".join(g))
    return "".join(o)


def doc(body, title):
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" '
            f'viewBox="0 0 {W} {H}"><title>{title}</title>{body}</svg>\n')


def spine_label():
    """Rückenschild-Einleger 29 x 129 mm für Rückentasche 30 x 130 mm."""
    w, h = 29, 129
    o = [rect(0, 0, w, h, fill=WHITE)]
    o.append(rect(0, 0, w, 17, fill=GRAPHITE))
    o.append(signet(w / 2, 6.2, 0.13, fill=WHITE))
    o.append(t(w / 2, 14.6, "NoBaCor", 3.6, fam=HEAD, w=500, fill=WHITE, anchor="middle"))
    o.append(t(w / 2, 72, "INSTALLATIONSORDNER", 4.4, fam=HEAD, w=600, fill=GRAPHITE, anchor="middle", ls=0.3,
               extra=f'transform="rotate(-90 {w/2} 72)" dominant-baseline="middle"'))
    o.append(rect(0, h - 12, w, 12, fill=BG))
    o.append(brand_ticks(w / 2 - 9, h - 8, L=6, h=0.7, gap=0))
    o.append(t(w / 2, h - 3.5, "NO BACTERIA. NO CORROSION.", 1.45, w=700, fill=STEEL, anchor="middle", ls=0.15))
    return "".join(o), w, h


def spine_sheet():
    body, w, h = spine_label()
    o = [rect(0, 0, 210, 297, fill=WHITE)]
    o.append(t(15, 14, "NoBaCor Rückenschilder – 29 × 129 mm für Rückentasche 30 × 130 mm – an den Schnittmarken ausschneiden",
               2.6, w=500, fill=STEEL))
    for r in range(2):
        for c in range(6):
            x, y = 15 + c * 31, 22 + r * 136
            o.append(f'<g transform="translate({x} {y})">{body}</g>')
            for (a, b) in ((x, y), (x + w, y), (x, y + h), (x + w, y + h)):
                o.append(line(a - 1.5, b, a + 1.5, b, c="#999", w=0.15) + line(a, b - 1.5, a, b + 1.5, c="#999", w=0.15))
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 210 297">{"".join(o)}</svg>\n'


if __name__ == "__main__":
    out = sys.argv[1]
    open(f"{out}/aussen.svg", "w").write(doc(outside(), "NoBaCor Installationsordner – Außen"))
    open(f"{out}/innen.svg", "w").write(doc(inside(), "NoBaCor Installationsordner – Innen"))
    open(f"{out}/aussen_kontrolle.svg", "w").write(doc(outside(True), "Außen mit Hilfslinien"))
    open(f"{out}/innen_kontrolle.svg", "w").write(doc(inside(True), "Innen mit Hilfslinien"))
    open(f"{out}/rueckenschilder_A4.svg", "w").write(spine_sheet())
