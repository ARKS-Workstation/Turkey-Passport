"""Render ARKS Sharks side-widget cards (transparent PNG, 960 px wide) from a JSON spec.
Card kinds: image (with label + source), stat (big number + bar), ratio (N-in-M car icons).
Usage: widgets.py SPEC.json OUTDIR"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
F = "/usr/share/fonts/opentype/inter/"
def font(name, size): return ImageFont.truetype(F + name, size)
CY, WHITE, MUTED, NAVY = (0, 229, 255), (255, 255, 255), (150, 185, 205), (8, 22, 40)
W, IMW, IMH, PAD = 960, 920, 430, 20
LOGO = Path(__file__).resolve().parents[1] / "brand" / "arks_sharks_logo_alpha.png"
def fin_icon(h):
    lg = Image.open(LOGO).convert("RGBA"); fin = lg.crop((int(lg.width * .28), 0, int(lg.width * .72), int(lg.height * .62)))
    return fin.resize((int(fin.width * h / fin.height), h), Image.LANCZOS)
def rounded(im, r):
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, *im.size), r, fill=255); im = im.convert("RGBA"); im.putalpha(m); return im
def text_lines(d, xy, lines, f, fill, accent_first=False, gap=8):
    x, y = xy
    for k, ln in enumerate(lines):
        d.text((x, y), ln, font=f, fill=CY if (accent_first and k == 0) else fill); y += f.size + gap
    return y
def car(d, x, y, s, col):
    d.rounded_rectangle((x, y + .35 * s, x + 1.9 * s, y + .8 * s), int(.15 * s), fill=col)
    d.polygon([(x + .35 * s, y + .38 * s), (x + .6 * s, y + .05 * s), (x + 1.35 * s, y + .05 * s), (x + 1.6 * s, y + .38 * s)], fill=col)
    d.polygon([(x + .5 * s, y + .36 * s), (x + .68 * s, y + .14 * s), (x + 1.27 * s, y + .14 * s), (x + 1.45 * s, y + .36 * s)], fill=NAVY + (255,))
    for cx in (.45, 1.45): d.ellipse((x + cx * s - .2 * s, y + .62 * s, x + cx * s + .2 * s, y + 1.02 * s), fill=(20, 30, 45, 255), outline=col, width=max(2, int(.05 * s)))
def panel(kind, c):
    p = Image.new("RGBA", (IMW, IMH), (0, 0, 0, 0))
    if kind == "image":
        im = ImageOps.fit(Image.open(c["image"]).convert("RGB"), (IMW, IMH), Image.LANCZOS, centering=(0.5, c.get("focus_y", 0.5)))
        p = rounded(im, 20)
        if c.get("illustration", True):
            d = ImageDraw.Draw(p); f = font("Inter-Bold.otf", 20); t = "ILLUSTRATION"; tw = d.textlength(t, font=f)
            d.rounded_rectangle((IMW - tw - 34, IMH - 44, IMW - 12, IMH - 12), 8, fill=(0, 0, 0, 150)); d.text((IMW - tw - 23, IMH - 40), t, font=f, fill=(220, 235, 245))
        return p
    bg = Image.new("RGBA", (IMW, IMH), (0, 0, 0, 0)); d = ImageDraw.Draw(bg)
    for yy in range(IMH):  # vertical navy-to-teal gradient
        t = yy / IMH; d.line([(0, yy), (IMW, yy)], fill=(int(6 + 4 * t), int(28 + 30 * t), int(52 + 30 * t), 255))
    bg = rounded(bg, 20); d = ImageDraw.Draw(bg)
    if kind == "stat":
        big = font("InterDisplay-Black.otf", 230); txt = c["value"]; tw = d.textlength(txt, font=big)
        glow = Image.new("RGBA", bg.size, (0, 0, 0, 0)); ImageDraw.Draw(glow).text(((IMW - tw) / 2, 40), txt, font=big, fill=CY + (200,))
        bg = Image.alpha_composite(bg, glow.filter(ImageFilter.GaussianBlur(18))); d = ImageDraw.Draw(bg)
        d.text(((IMW - tw) / 2, 40), txt, font=big, fill=WHITE)
        frac = c.get("fraction", 0.25); x0, x1, yb = 90, IMW - 90, 340
        d.rounded_rectangle((x0, yb, x1, yb + 34), 17, fill=(30, 55, 80, 255)); d.rounded_rectangle((x0, yb, x0 + (x1 - x0) * frac, yb + 34), 17, fill=CY + (255,))
        f = font("Inter-Bold.otf", 26); d.text((x0, yb + 44), c.get("bar_left", "TODAY"), font=f, fill=MUTED); t = c.get("bar_right", "2030"); d.text((x1 - d.textlength(t, font=f), yb + 44), t, font=f, fill=MUTED)
    elif kind == "ratio":
        n, m = c.get("n", 1), c.get("m", 4); s = 92; gapx = 34; total = m * 1.9 * s + (m - 1) * gapx; x = (IMW - total) / 2
        big = font("InterDisplay-Black.otf", 96); t = c["value"]; d.text(((IMW - d.textlength(t, font=big)) / 2, 30), t, font=big, fill=WHITE)
        for k in range(m):
            col = CY + (255,) if k < n else (70, 95, 120, 255)
            car(d, x + k * (1.9 * s + gapx), 200, s, col)
    return bg
def card(c, out):
    lines = c["label"].split("\n"); fl = font("InterDisplay-Black.otf", 40); fs = font("Inter-Medium.otf", 23)
    H = 70 + IMH + 22 + len(lines) * 48 + 44
    base = Image.new("RGBA", (W + 40, H + 40), (0, 0, 0, 0))
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((20, 26, W + 20, H + 26), 30, fill=(0, 0, 0, 150))
    glow = Image.new("RGBA", base.size, (0, 0, 0, 0)); ImageDraw.Draw(glow).rounded_rectangle((20, 20, W + 20, H + 20), 30, outline=CY + (160,), width=6)
    base = Image.alpha_composite(base, sh.filter(ImageFilter.GaussianBlur(14))); base = Image.alpha_composite(base, glow.filter(ImageFilter.GaussianBlur(8)))
    body = Image.new("RGBA", (W, H), NAVY + (225,)); body = rounded(body, 30); body.putalpha(Image.eval(body.split()[3], lambda v: min(v, 225)))
    d = ImageDraw.Draw(body); d.rounded_rectangle((0, 0, W - 1, H - 1), 30, outline=CY + (210,), width=3)
    ic = fin_icon(44); body.alpha_composite(ic, (PAD, 13))
    ft = font("InterDisplay-Black.otf", 30); d.text((PAD + ic.width + 12, 18), c.get("topic", "AI IN DUBAI"), font=ft, fill=CY)
    fb = font("Inter-Bold.otf", 22); t = "ARKS SHARKS"; d.text((W - PAD - d.textlength(t, font=fb), 24), t, font=fb, fill=(200, 220, 235))
    body.alpha_composite(panel(c.get("kind", "image"), c), (PAD, 70))
    y = text_lines(d, (PAD + 4, 70 + IMH + 16), lines, fl, WHITE, accent_first=c.get("accent_first", True))
    if c.get("source"): d.text((PAD + 4, y + 2), c["source"], font=fs, fill=MUTED)
    base.alpha_composite(body, (20, 20)); base.save(out); return base.size
spec = json.load(open(sys.argv[1])); outdir = Path(sys.argv[2]); outdir.mkdir(parents=True, exist_ok=True)
for c in spec["cards"]:
    print(c["id"], card(c, outdir / f"{c['id']}.png"))
