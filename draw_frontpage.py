#!/usr/bin/env python3
"""Draw the 21 November 2026 front page: 65 verified stories, 7 regions.
Original design, drawn with PIL. Output: entry.png (1024x1024, <=1 MiB)."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024
PAPER = (248, 244, 233)
INK = (22, 22, 22)
GREY = (96, 92, 84)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# (label, glyph tag) -- every label verified from 21 Nov 2026 reporting.
SA = ("SOUTH ASIA / INDIA", (200, 90, 23), [
    ("Cyclone Akvan weakens after landfall; 4.4 lakh evacuated", "storm"),
    ("1,452 babies delivered in shelters as Akvan hits Odisha", "storm"),
    ("Nikhil Gupta gets 235 months in US court over Pannun plot", "court"),
    ("ICJ Myanmar verdict: Rohingya hope for return; Myanmar objects", "court"),
    ("India 'takes note' of Trump-Xi-Putin summit in Shenzhen", "globe"),
    ("Congress offers 4-point delimitation formula; INDIA bloc on board", "dot"),
    ("NIA asks UAE to probe flydubai co-pilot's India links", "plane"),
    ("Bangladesh hit by fresh arson amid political unrest", "flame"),
    ("Pakistan cuts petrol Re1 to Rs322; diesel up Rs2 to Rs357", "chart"),
    ("Kohat operation kills 3 terrorists, incl. Police Lines chief", "dot"),
    ("Manipur spurious liquor kills 13; 300+ in hospital", "dot"),
    ("Teen held for selling 4,000 Agniveers' data on dark web", "chip"),
    ("Adani Defence fires four anti-tank missiles at Pokhran", "rocket"),
    ("India-Portugal sign 5-year trade, defence, energy roadmap", "globe"),
    ("India-France condemn Pahalgam and Red Fort terror attacks", "globe"),
])
ME = ("MIDDLE EAST", (11, 114, 133), [
    ("Yemen: Saudi-attributed strikes kill 41, incl. 11 children", "flame"),
    ("Basra gas pipeline blast kills 8, injures 30+ in Iraq", "flame"),
    ("Oil tanker hits sea mine off Hormuz, catches fire", "bolt"),
    ("IRGC says it downed a US Predator drone over Qeshm", "plane"),
    ("Bahrain intercepts Iranian attacks; sirens, fire at facility", "bolt"),
    ("Iran vows to break US blockade; power rationing from Sunday", "bolt"),
    ("Israeli strike kills 3 in Gaza City's Tel al-Hawa", "flame"),
    ("Houthi senior commander killed in Taiz", "dot"),
    ("Iran FM: any US deal must protect national interests", "globe"),
    ("Trump claims US control over Strait of Hormuz", "globe"),
])
US = ("US / AMERICAS", (31, 78, 121), [
    ("FBI probes suspected hack of NCIC criminal database", "chip"),
    ("Trump defends Putin ties; no NATO-like Ukraine guarantees", "globe"),
    ("US, China, Russia agree talks to stop nuclear spread", "globe"),
    ("Trump threatens ban on US firms building AI centres abroad", "chip"),
    ("Nvidia board: no plans to bring back Jensen Huang", "chip"),
    ("Measles case in Virginia child, 0-4, amid rising infections", "dot"),
    ("Earthquake rattles Peru; tremors mapped across region", "quake"),
    ("SpaceX Dragon leaves ISS; splashdown off California", "rocket"),
    ("Brazil storm kills 1 in Tupancireta, Rio Grande do Sul", "storm"),
])
EU = ("EUROPE", (91, 75, 158), [
    ("EU-UK seal deals on food trade, carbon markets, youth", "globe"),
    ("Tusk: incidents as Russian strikes hit Ukraine again", "bolt"),
    ("Court: BYD Fangchengbao Ti7 copies Defender design", "court"),
    ("French court jails 3 police for beating a Black man", "court"),
    ("Protests sweep Europe; Italy strike halts transport", "dot"),
    ("Austria Foreign Ministry website hacked; contacts leaked", "chip"),
    ("EU proposes Big Tech tax to fund next budget", "chart"),
    ("Drones attack Russian cargo ship in Gulf of Finland", "plane"),
])
EAP = ("EAST ASIA / PACIFIC / AFRICA", (46, 125, 50), [
    ("QUAD summit in Manila: Trump, Modi, Takaichi, Albanese", "globe"),
    ("Indonesia fire losses could hit $30bn, research warns", "flame"),
    ("Minibus-train crash in Simalungun kills 1, injures several", "dot"),
    ("Cummins keeps Cricket Australia's 'unanimous support'", "ball"),
    ("China AI fire system mistakes photo for blaze, sprays water", "chip"),
    ("Magnitude 5.8 quake strikes Qinghai, China", "quake"),
])
BUS = ("BUSINESS / TECH / SCIENCE", (146, 110, 12), [
    ("Nasdaq -5.28%, wiping out all of 2026's gains", "chart"),
    ("Nasdaq 100 nears bear market; S&P 500 in correction", "chart"),
    ("Chip crash: Nvidia -14%, AMD, Broadcom, Micron slide", "chip"),
    ("Anthropic -8.5% a day after its blockbuster IPO debut", "chart"),
    ("CLAIM: Claude helped prove the Riemann Hypothesis", "dot"),
    ("Apple reportedly building an AI agent to write code", "chip"),
    ("Lenovo revenue +48% to a quarterly record", "chart"),
    ("Broadcom patches critical vCenter flaw", "chip"),
    ("NASA halts Perseverance and Mars Odyssey science", "rocket"),
])
SPORT = ("SPORT / CULTURE", (178, 24, 10), [
    ("KL Rahul: first Indian opener with Test tons in all SENA lands", "ball"),
    ("F1 Las Vegas GP: Free Practice 3 sets the grid order", "car"),
    ("Alcaraz beats Cobolli; faces Shelton in Turin semi-final", "ball"),
    ("Bengaluru FC 2-0 Mumbai City, go top of the ISL", "ball"),
    ("India women beat Malaysia 4-1 in Asian Champions Trophy", "ball"),
    ("Australia edge England in the 1st T20", "ball"),
    ("Hunger Games prequel takes $21m in Thursday previews", "film"),
    ("Giri-Firouzja share the spoils, 2-2, in Total Chess blitz", "dot"),
])

LEFT = [SA, ME]
RIGHT = [US, EU, EAP]
BOTTOM = [BUS, SPORT]
TOTAL = sum(len(s[2]) for s in LEFT + RIGHT + BOTTOM)


def trunc(draw, text, fnt, max_w):
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    while text and draw.textlength(text + "...", font=fnt) > max_w:
        text = text[:-1]
    return text + "..."


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def glyph(d, cx, cy, kind, color):
    """Tiny 14x14 drawn icon centred at (cx, cy)."""
    s = 6
    if kind == "dot":
        d.polygon([(cx, cy - s), (cx + s, cy), (cx, cy + s), (cx - s, cy)], fill=color)
    elif kind == "storm":
        for r in (2, 4, 6):
            d.arc([cx - r, cy - r, cx + r, cy + r], 200, 20, fill=color, width=2)
        d.ellipse([cx - 1, cy - 1, cx + 1, cy + 1], fill=color)
    elif kind == "court":
        d.rectangle([cx - 6, cy - 5, cx + 6, cy - 4], fill=color)
        for x in (-4, 0, 4):
            d.rectangle([cx + x - 1, cy - 3, cx + x + 1, cy + 4], fill=color)
        d.rectangle([cx - 6, cy + 5, cx + 6, cy + 6], fill=color)
    elif kind == "rocket":
        d.polygon([(cx, cy - 6), (cx + 4, cy + 2), (cx, cy + 6), (cx - 4, cy + 2)], fill=color)
        d.polygon([(cx - 2, cy + 4), (cx, cy + 8), (cx + 2, cy + 4)], fill=(230, 120, 40))
    elif kind == "ball":
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], outline=color, width=2)
        d.line([cx - 5, cy, cx + 5, cy], fill=color, width=1)
        d.line([cx, cy - 5, cx, cy + 5], fill=color, width=1)
    elif kind == "chart":
        d.line([(cx - 6, cy + 4), (cx - 2, cy - 1), (cx + 1, cy + 2), (cx + 6, cy - 5)],
               fill=color, width=2)
        d.polygon([(cx + 6, cy - 5), (cx + 3, cy - 5), (cx + 6, cy - 2)], fill=color)
    elif kind == "quake":
        d.line([(cx - 6, cy), (cx - 3, cy - 5), (cx, cy + 4), (cx + 3, cy - 5),
                (cx + 6, cy)], fill=color, width=2)
    elif kind == "plane":
        d.polygon([(cx - 6, cy + 2), (cx + 6, cy - 3), (cx + 2, cy + 3), (cx - 2, cy + 5)],
                  fill=color)
    elif kind == "chip":
        d.rectangle([cx - 4, cy - 4, cx + 4, cy + 4], outline=color, width=2)
        for x in (-2, 2):
            d.line([cx + x, cy - 6, cx + x, cy + 6], fill=color, width=1)
        d.rectangle([cx - 1, cy - 1, cx + 1, cy + 1], fill=color)
    elif kind == "flame":
        d.polygon([(cx, cy - 6), (cx + 4, cy + 1), (cx + 2, cy + 6),
                   (cx - 2, cy + 6), (cx - 4, cy + 1)], fill=color)
    elif kind == "bolt":
        d.polygon([(cx + 1, cy - 6), (cx - 3, cy + 1), (cx, cy + 1),
                   (cx - 1, cy + 6), (cx + 3, cy - 1), (cx, cy - 1)], fill=color)
    elif kind == "globe":
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], outline=color, width=2)
        d.ellipse([cx - 2, cy - 5, cx + 2, cy + 5], outline=color, width=1)
        d.line([cx - 5, cy, cx + 5, cy], fill=color, width=1)
    elif kind == "car":
        d.rectangle([cx - 6, cy - 2, cx + 6, cy + 2], fill=color)
        d.polygon([(cx - 3, cy - 2), (cx - 1, cy - 5), (cx + 3, cy - 5), (cx + 5, cy - 2)],
                  fill=color)
        d.ellipse([cx - 5, cy + 1, cx - 1, cy + 5], fill=INK)
        d.ellipse([cx + 1, cy + 1, cx + 5, cy + 5], fill=INK)
    elif kind == "film":
        d.rectangle([cx - 6, cy - 5, cx + 6, cy + 5], outline=color, width=2)
        d.line([cx - 6, cy - 1, cx + 6, cy - 1], fill=color, width=1)
        for x in (-3, 0, 3):
            d.line([cx + x, cy - 5, cx + x + 2, cy - 1], fill=color, width=1)
    else:
        d.polygon([(cx, cy - 5), (cx + 5, cy), (cx, cy + 5), (cx - 5, cy)], fill=color)


def draw_lead_scene(d, x0, y0, x1, y1):
    """Sunset Vice-City style skyline panel for the GTA 6 lead."""
    top = (255, 122, 61)
    mid = (193, 59, 122)
    bot = (59, 42, 107)
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0)
        c = lerp(top, mid, t * 1.6) if t < 0.62 else lerp(mid, bot, (t - 0.62) / 0.38)
        d.line([(x0, y), (x1, y)], fill=c)
    # sun
    d.ellipse([x1 - 118, y0 + 16, x1 - 48, y0 + 86], fill=(255, 214, 130))
    d.ellipse([x1 - 108, y0 + 26, x1 - 58, y0 + 76], fill=(255, 236, 180))
    # skyline silhouettes
    import random
    rnd = random.Random(21)
    base = y1 - 52
    bx = x0 + 8
    while bx < x1 - 20:
        bw = rnd.randint(22, 46)
        bh = rnd.randint(34, 96)
        d.rectangle([bx, base - bh, bx + bw, base], fill=(28, 18, 54))
        for wy in range(base - bh + 8, base - 6, 12):
            for wx in range(bx + 5, bx + bw - 4, 10):
                if rnd.random() < 0.5:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 210, 120))
        bx += bw + 4
    # road + sports car
    d.rectangle([x0, y1 - 34, x1, y1], fill=(24, 16, 46))
    d.line([(x0, y1 - 17), (x1, y1 - 17)], fill=(255, 210, 120), width=2)
    cx, cy = x0 + 300, y1 - 26
    d.polygon([(cx - 58, cy + 4), (cx - 46, cy - 8), (cx - 12, cy - 14),
               (cx + 28, cy - 12), (cx + 56, cy + 4)], fill=(96, 62, 150))
    d.ellipse([cx - 44, cy - 2, cx - 24, cy + 8], fill=(8, 6, 18))
    d.ellipse([cx + 24, cy - 2, cx + 44, cy + 8], fill=(8, 6, 18))
    # big VI numeral
    f_vi = font(SERIF_B, 92)
    d.text((x0 + 18, y0 + 8), "VI", font=f_vi, fill=(255, 255, 255))
    d.text((x0 + 20, y0 + 100), "LEONIDA", font=font(SANS_B, 15),
           fill=(255, 214, 130))


def section(d, x, y, w, title, color, items, body_fnt, bold_fnt, head_fnt):
    """Draw one region section at (x, y); return y after it."""
    d.rounded_rectangle([x, y, x + w, y + 21], radius=4, fill=color)
    d.text((x + 8, y + 4), title, font=head_fnt, fill=(255, 255, 255))
    d.text((x + w - 8, y + 4), str(len(items)), font=head_fnt,
           fill=(255, 255, 255), anchor="ra")
    y += 21
    for label, tag in items:
        yy = y + 2
        glyph(d, x + 8, yy + 6, tag, color)
        fnt = bold_fnt if label.startswith("Nasdaq -5.28") else body_fnt
        txt = trunc(d, label, fnt, w - 24)
        d.text((x + 22, yy), txt, font=fnt, fill=INK)
        y += 16
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    f_title = font(SERIF_B, 46)
    f_date = font(SANS_B, 15)
    f_count = font(SANS_B, 13)
    f_head = font(SERIF_B, 33)
    f_sub = font(SANS, 14)
    f_small = font(SANS, 12)
    f_body = font(SANS, 13)
    f_bold = font(SANS_B, 13)
    f_sect = font(SANS_B, 13)
    f_foot = font(SANS, 10)

    # --- masthead ---
    title = "THE WORLD IN ONE DAY"
    d.text((W // 2, 12), title, font=f_title, fill=INK, anchor="ma")
    d.line([(14, 82), (1010, 82)], fill=INK, width=2)
    d.text((14, 88), "SATURDAY 21 NOVEMBER 2026", font=f_date, fill=INK)
    d.text((1010, 89), "%d STORIES  ·  7 REGIONS  ·  ONE DAY" % TOTAL,
           font=f_count, fill=GREY, anchor="ra")

    # --- lead: scene left, headline right ---
    sx0, sy0, sx1, sy1 = 14, 114, 560, 300
    draw_lead_scene(d, sx0, sy0, sx1, sy1)
    tx = 576
    for i, (line, color) in enumerate([
            ("GTA 6 EARNS $3.8BN", (178, 24, 10)),
            ("ON DAY ONE", (178, 24, 10)),
            ("BIGGEST LAUNCH EVER", INK)]):
        size = 33
        while size > 24 and d.textlength(line, font=font(SERIF_B, size)) > 434:
            size -= 1
        d.text((tx, 118 + i * 34), line, font=font(SERIF_B, size), fill=color)
    d.text((tx, 232), "Bigger than any film, album or game in", font=f_sub, fill=INK)
    d.text((tx, 250), "history. The wait is over - and the", font=f_sub, fill=INK)
    d.text((tx, 268), "numbers are in.", font=f_sub, fill=INK)
    d.text((tx, 292), "PC scam alert: $200 malware kits, fake downloads.",
           font=f_small, fill=GREY)

    # --- COP31 strip ---
    d.rounded_rectangle([14, 308, 1010, 340], radius=5, fill=(11, 79, 92))
    d.text((28, 316),
           "COP31 STALLS INTO OVERTIME  —  no deal in Antalya; fossil-fuel wording cut",
           font=font(SANS_B, 15), fill=(255, 255, 255))

    # --- body: two columns, then a full-width bottom band ---
    col_w = 489
    y = 348
    ly = y
    for title, color, items in LEFT:
        ly = section(d, 14, ly, col_w, title, color, items, f_body, f_bold, f_sect)
        ly += 8
    ry = y
    for title, color, items in RIGHT:
        ry = section(d, 521, ry, col_w, title, color, items, f_body, f_bold, f_sect)
        ry += 8
    by = max(ly, ry) + 4
    bx = section(d, 14, by, col_w, BUS[0], BUS[1], BUS[2], f_body, f_bold, f_sect)
    section(d, 521, by, col_w, SPORT[0], SPORT[1], SPORT[2], f_body, f_bold, f_sect)
    end_y = max(bx, by + 21 + 8 * 16)

    # --- footer ---
    d.line([(14, end_y + 8), (1010, end_y + 8)], fill=GREY, width=1)
    d.text((14, end_y + 12),
           "Stories as reported on 21 November 2026  ·  The Hindu · WION · Al Jazeera · "
           "Business Standard · NYT",
           font=f_foot, fill=GREY)
    print("layout end_y:", end_y, "total stories:", TOTAL)
    assert end_y + 26 <= H, "layout overflow"

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
