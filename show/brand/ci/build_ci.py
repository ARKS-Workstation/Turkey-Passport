"""Build the ARKS Sharks Corporate Identity guidelines (16:9 PDF) from repo assets.
Run from the repo root:  python3 show/brand/ci/build_ci.py
Writes show/brand/ci/ARKS_Sharks_CI_Guidelines.html and show/brand/ARKS_Sharks_CI_Guidelines_v1.pdf"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = "assets"
VERSION, DATE = "1.0", "November 2026"

PAL = [  # name, hex, rgb, role
    ("Shark Cyan", "#00E5FF", "0 · 229 · 255", "Signature accent: logo fin, caption keywords, card borders, LED edges"),
    ("Deep Navy", "#081628", "8 · 22 · 40", "Cards, panels, name tags"),
    ("Midnight", "#04080F", "4 · 8 · 15", "Backgrounds, end cards, title cards"),
    ("Chrome", "#E9EDF0", "233 · 237 · 240", "Wordmark, headline text, white type"),
    ("Neural Blue", "#2B4FBF", "43 · 79 · 191", "LED walls, data graphics, gradients"),
    ("Neural Violet", "#8B5CF6", "139 · 92 · 246", "LED node glow, secondary highlights"),
    ("Karak Amber", "#E39A3B", "227 · 154 · 59", "Warm key light, karak tea, warm accents"),
    ("Mist", "#96B9CD", "150 · 185 · 205", "Secondary text, source lines, small labels"),
]
WARDROBE = [("Camel", "#C8875A", "Ahmed's blazer"), ("Jet", "#111214", "Ahmed's turtleneck"), ("Olive", "#4A5233", "Kamran's bomber"),
            ("Tee White", "#F4F4F2", "Kamran's T-shirt"), ("Charcoal", "#3A3D42", "Studio chairs, trousers")]

CSS = """
@page { size: 1280px 720px; margin: 0 }
* { box-sizing: border-box }
body { margin: 0; background: #04080F; -webkit-print-color-adjust: exact; print-color-adjust: exact }
.page { width: 1280px; height: 720px; position: relative; overflow: hidden; page-break-after: always; background: #04080F; color: #E9EDF0;
        font-family: 'Inter', sans-serif }
.page:last-child { page-break-after: auto }
.hdr { position: absolute; top: 26px; left: 56px; right: 56px; display: flex; justify-content: space-between; align-items: center;
       font: 600 12px 'Inter'; letter-spacing: .2em; color: #96B9CD; text-transform: uppercase; z-index: 5 }
.hdr img { height: 22px; vertical-align: middle; margin-right: 10px }
.ftr { position: absolute; bottom: 22px; left: 56px; right: 56px; display: flex; justify-content: space-between; font: 500 11px 'Inter';
       color: #5D7385; letter-spacing: .08em; z-index: 5 }
.content { position: absolute; top: 70px; left: 56px; right: 56px; bottom: 56px }
.sec { font: 900 13px 'Inter Display'; color: #00E5FF; letter-spacing: .22em; text-transform: uppercase }
h1 { font: 900 50px/1.02 'Inter Display'; margin: 6px 0 16px; letter-spacing: -.01em; color: #fff }
h2 { font: 800 20px/1.2 'Inter Display'; color: #fff; margin: 0 0 8px }
h3 { font: 800 14px 'Inter Display'; color: #00E5FF; margin: 0 0 6px; letter-spacing: .14em; text-transform: uppercase }
p, li, td { font: 400 14px/1.5 'Inter'; color: #C8D6E0; margin: 0 0 8px }
ul { margin: 0; padding-left: 18px } li { margin: 0 0 4px }
b, strong { color: #fff; font-weight: 700 }
.cy { color: #00E5FF } .am { color: #E39A3B }
.card { background: #081628; border: 1px solid rgba(0,229,255,.32); border-radius: 14px; padding: 16px 18px }
.grid { display: grid; gap: 18px }
.g2 { grid-template-columns: 1fr 1fr } .g3 { grid-template-columns: 1fr 1fr 1fr } .g4 { grid-template-columns: repeat(4, 1fr) }
img.fill { width: 100%; height: 100%; object-fit: cover; border-radius: 12px; display: block }
.cap { font: 500 11px 'Inter'; color: #96B9CD; margin-top: 6px; letter-spacing: .03em }
table { border-collapse: collapse; width: 100% } td { padding: 5px 8px 5px 0; vertical-align: top; border-bottom: 1px solid rgba(150,185,205,.15) }
td.k { color: #96B9CD; font-weight: 600; width: 132px; font-size: 12.5px; letter-spacing: .04em; text-transform: uppercase }
.tag { display: inline-block; background: #00E5FF; color: #000; font: 900 12px 'Inter Display'; padding: 4px 10px; border-radius: 6px; letter-spacing: .06em }
.no { color: #ff6b6b } .yes { color: #00E5FF }
.mono { font-family: 'DejaVu Sans Mono', monospace; font-size: 12px; color: #C8D6E0 }
.big { font: 900 92px/0.95 'Inter Display'; color: #fff; letter-spacing: -.02em }
.swatch { border-radius: 12px; overflow: hidden; border: 1px solid rgba(255,255,255,.12) }
.swatch .c { height: 64px } .swatch .t { background: #081628; padding: 10px 12px }
.swatch .n { font: 800 15px 'Inter Display'; color: #fff } .swatch .h { font: 600 12px 'Inter'; color: #00E5FF; margin-top: 2px }
.swatch .r { font: 500 11px 'Inter'; color: #96B9CD } .swatch .u { font: 400 10.5px/1.3 'Inter'; color: #C8D6E0; margin-top: 4px; height: 30px }
.num { position: absolute; width: 28px; height: 28px; border-radius: 50%; background: #00E5FF; color: #000; font: 900 14px/28px 'Inter Display';
       text-align: center; box-shadow: 0 0 0 4px rgba(0,229,255,.25) }
.pill { display: inline-block; border: 1px solid rgba(0,229,255,.5); color: #00E5FF; font: 700 11px 'Inter'; padding: 3px 9px; border-radius: 99px;
        margin: 0 6px 6px 0; letter-spacing: .06em }
.bar { display: flex; height: 26px; border-radius: 8px; overflow: hidden; margin-top: 10px }
.tl { display: flex; height: 54px; border-radius: 10px; overflow: hidden; font: 700 11px/1.2 'Inter'; color: #000 }
.tl div { display: flex; align-items: center; justify-content: center; text-align: center; padding: 0 4px; border-right: 2px solid #04080F }
"""


def page(n, section, body, bg=None, chrome=True):
    style = f' style="background: {bg}"' if bg else ""
    hdr = (f'<div class="hdr"><div><img src="{A}/fin.png">ARKS Sharks · CI Guidelines</div><div>{section}</div></div>'
           f'<div class="ftr"><div>Version {VERSION} · {DATE}</div><div>{n:02d}</div></div>') if chrome else ""
    return f'<section class="page"{style}>{hdr}{body}</section>'


def spec_table(rows):
    return "<table>" + "".join(f'<tr><td class="k">{k}</td><td>{v}</td></tr>' for k, v in rows) + "</table>"


pages = []
# 01 cover
pages.append(page(1, "", f"""
<img src="{A}/in_burj.jpg" style="position:absolute; inset:0; width:100%; height:100%; object-fit:cover; object-position:50% 30%; filter:brightness(.45) saturate(1.1)">
<div style="position:absolute; inset:0; background:linear-gradient(90deg, rgba(4,8,15,.92) 0%, rgba(4,8,15,.55) 55%, rgba(4,8,15,.2) 100%)"></div>
<div style="position:absolute; left:80px; top:150px; width:640px">
  <img src="{A}/logo_shadow.png" style="width:560px; margin-left:-30px">
  <div class="sec" style="margin-top:18px">Corporate Identity Guidelines</div>
  <div style="font:900 40px/1.1 'Inter Display'; color:#fff; margin-top:8px">The show. The characters.<br>The studio.</div>
  <p style="margin-top:18px; font-size:15px">Everything needed to make ARKS Sharks look, sound and feel the same in every episode, trailer and post.</p>
  <div style="margin-top:22px"><span class="pill">VERSION {VERSION}</span><span class="pill">{DATE.upper()}</span><span class="pill">DUBAI</span></div>
</div>""", chrome=False))

# 02 contents
toc = ["The show", "Logo", "Logo do's & don'ts", "Colour", "Typography", "The characters", "Ahmed", "Kamran", "Character rules",
       "The studio", "Studio lighting & framing", "9:16 layout & safe zones", "On-screen graphics", "Motion & editing",
       "Sound identity", "Tone of voice & content rules", "Technical specs & asset index"]
items = "".join(f'<div style="display:flex; gap:16px; padding:9px 0; border-bottom:1px solid rgba(150,185,205,.15)">'
                f'<span class="cy" style="font:900 15px \'Inter Display\'; width:34px">{i + 1:02d}</span>'
                f'<span style="font:700 16px \'Inter Display\'; color:#fff; flex:1">{t}</span>'
                f'<span style="font:500 12px Inter; color:#5D7385">p. {i + 3}</span></div>' for i, t in enumerate(toc))
pages.append(page(2, "Contents", f"""<div class="content" style="display:grid; grid-template-columns: 380px 1fr; gap:60px">
<div><div class="sec">Contents</div><h1>What's<br>inside</h1>
<p>This book is the single source of truth for ARKS Sharks. When something isn't covered here, match the approved trailer
(<span class="mono">show/final/ARKS_Sharks_Trailer_v1_APPROVED_9x16.mp4</span>).</p>
<img src="{A}/avatar.png" style="width:150px; margin-top:20px"></div>
<div style="columns:2; column-gap:40px; margin-top:20px">{items}</div></div>"""))

# 03 the show
pages.append(page(3, "01 · The show", f"""<div class="content" style="display:grid; grid-template-columns: 1fr 300px; gap:40px">
<div><div class="sec">01 · The show</div><h1>Two friends.<br>One topic: <span class="cy">AI.</span></h1>
<p style="font-size:16px; max-width:640px"><b>ARKS Sharks</b> is a vertical talk show from a Dubai studio. Ahmed and Kamran chat like old friends
about the newest AI tools, what AI means for Dubai, and the funniest things AI has done. Every fact is sourced and shown on screen.</p>
<div style="font:900 26px 'Inter Display'; color:#fff; margin:18px 0 22px">“We hunt the AI news… <span class="cy">so you don't have to.</span>”</div>
<div class="grid g4">
 <div class="card"><h3>Friendly</h3><p>Two mates talking, never a lecture. Banter, laughs, karak on the table.</p></div>
 <div class="card"><h3>Smart</h3><p>Real, recent AI news explained in plain words, with what it means for you.</p></div>
 <div class="card"><h3>Funny</h3><p>A funny corner of real AI fails in every episode. We laugh with the tech, not at people.</p></div>
 <div class="card"><h3>Honest</h3><p>Every claim has a source on screen. AI-made pictures are labelled "Illustration".</p></div>
</div>
<h3 style="margin-top:22px">Episode structure</h3>
<div class="tl"><div style="flex:0.9; background:#00E5FF">Hook<br>2.5 s</div>
<div style="flex:2.2; background:#2B4FBF; color:#fff">What's new<br>in AI</div><div style="flex:1.6; background:#8B5CF6; color:#fff">AI in<br>Dubai</div>
<div style="flex:1.6; background:#E39A3B">Funny corner<br>AI fails</div><div style="flex:1; background:#E9EDF0">Tip &amp;<br>sign-off</div></div>
</div>
<div><img src="{A}/tr_names.jpg" class="fill" style="height:530px"><div class="cap">Ahmed (left) and Kamran (right) on set. Approved trailer.</div></div>
</div>"""))

# 04 logo
pages.append(page(4, "02 · Logo", f"""<div class="content">
<div class="sec">02 · Logo</div><h1>The ARKS Sharks mark</h1>
<div class="grid" style="grid-template-columns: 1.35fr 1fr; gap:30px">
 <div class="card" style="height:430px; display:flex; align-items:center; justify-content:center; background:#04080F; position:relative">
   <img src="{A}/logo.png" style="width:86%">
   <div style="position:absolute; inset:58px 44px; border:2px dashed rgba(0,229,255,.45); border-radius:6px"></div>
   <div class="cap" style="position:absolute; bottom:12px; left:18px">Dashed line = minimum clear space: the height of the letter "A" on every side.</div>
 </div>
 <div>
  <h3>Anatomy</h3>
  <p><b>Circuit fin.</b> A shark fin drawn from glowing circuit-board traces: the shark (sharp, hunting for news) built out of AI.</p>
  <p><b>Wave line.</b> The surface of the water. The fin cuts through it: news breaking the surface.</p>
  <p><b>Chrome wordmark.</b> "ARKS SHARKS" in a wide geometric sans with a chrome finish and a cyan edge.</p>
  <h3 style="margin-top:16px">Versions</h3>
  <div class="grid g3" style="gap:10px">
    <div class="card" style="padding:8px; text-align:center"><img src="{A}/logo_shadow.png" style="width:100%"><div class="cap">Full colour + shadow<br>(over video)</div></div>
    <div class="card" style="padding:8px; text-align:center; background:#04080F"><img src="{A}/logo.png" style="width:100%"><div class="cap">Full colour<br>(dark backgrounds)</div></div>
    <div class="card" style="padding:8px; text-align:center"><img src="{A}/avatar.png" style="width:66%"><div class="cap">Fin icon<br>(avatars, favicons)</div></div>
  </div>
  <p style="margin-top:12px"><b>Minimum size:</b> 320 px wide on a 1080 px frame. Fin icon: 48 px.</p>
 </div>
</div></div>"""))

# 05 logo dos and donts
mis = [("mis_stretch", "Don't stretch or squash"), ("mis_red", "Don't recolour, never red"), ("mis_busy", "Don't place on bright, busy video without the shadow version"),
       ("mis_rotate", "Don't rotate or tilt"), ("mis_split", "Don't separate the fin from the wordmark"), ("mis_faded", "Don't fade or use low contrast")]
tiles = "".join(f'<div><img src="{A}/{f}.jpg" class="fill" style="height:150px"><div class="cap"><span class="no">✕</span> {t}</div></div>' for f, t in mis)
pages.append(page(5, "03 · Logo do's & don'ts", f"""<div class="content">
<div class="sec">03 · Logo do's &amp; don'ts</div><h1>Keep the mark intact</h1>
<div class="grid" style="grid-template-columns: 330px 1fr; gap:28px">
 <div><h3><span class="yes">✓</span> Do</h3>
  <img src="{A}/tr_logo.jpg" class="fill" style="height:250px; object-position:50% 30%"><div class="cap">Logo slam over the studio, shadow version.</div>
  <ul style="margin-top:10px"><li>Use the shadow version over video and photos.</li><li>Keep it centred in the upper third of a 9:16 frame.</li>
  <li>Give it clear space: never touching captions, faces or widgets.</li></ul></div>
 <div class="grid g3" style="gap:14px">{tiles}</div>
</div></div>"""))

# 06 colour
sw = "".join(f'<div class="swatch"><div class="c" style="background:{h}"></div><div class="t"><div class="n">{n}</div><div class="h">{h}</div>'
             f'<div class="r">RGB {r}</div><div class="u">{u}</div></div></div>' for n, h, r, u in PAL)
ward = "".join(f'<div style="display:flex; align-items:center; gap:8px; margin-bottom:3px"><div style="width:20px; height:20px; border-radius:6px; background:{h}; border:1px solid rgba(255,255,255,.2)"></div>'
               f'<div style="font:600 12px Inter; color:#fff">{n} <span style="color:#96B9CD; font-weight:500">{h} · {u}</span></div></div>' for n, h, u in WARDROBE)
pages.append(page(6, "04 · Colour", f"""<div class="content">
<div class="sec">04 · Colour</div><h1 style="margin-bottom:10px; font-size:44px">Night-time Dubai, lit by AI</h1>
<div class="grid g4" style="gap:12px">{sw}</div>
<div class="grid" style="grid-template-columns: 1.3fr 1fr 0.9fr; gap:24px; margin-top:12px; align-items:start">
 <div><h3>Balance</h3><div class="bar"><div style="flex:55; background:#04080F; border:1px solid #233"></div><div style="flex:22; background:#081628"></div>
 <div style="flex:10; background:#00E5FF"></div><div style="flex:6; background:#2B4FBF"></div><div style="flex:4; background:#8B5CF6"></div><div style="flex:3; background:#E39A3B"></div></div>
 <div class="cap">Dark base (Midnight/Navy) about 75%, Shark Cyan about 10%, the rest as accents.</div></div>
 <div><h3>Wardrobe locks</h3>{ward}</div>
 <div class="card" style="border-color:rgba(255,107,107,.6)"><h3 style="color:#ff6b6b">No red</h3><p>Red is never used in the set, graphics, logo or images. Warm moments use <span class="am">Karak Amber</span> instead.</p></div>
</div></div>"""))

# 07 typography
pages.append(page(7, "05 · Typography", f"""<div class="content" style="display:grid; grid-template-columns: 1fr 300px; gap:36px">
<div><div class="sec">05 · Typography</div><h1>Inter Display &amp; Inter</h1>
<div style="font:900 64px/1 'Inter Display'; color:#fff">WE HUNT THE <span class="cy">AI</span> NEWS</div>
<div style="font:400 15px Inter; color:#96B9CD; margin:6px 0 16px">Inter Display Black · captions, headlines, titles · all caps on screen</div>
{spec_table([("Captions", "Inter Display Black · 82 px · all caps · white, 6 px black outline · key words in <span class='cy'>Shark Cyan</span> · max 3 words per chunk"),
             ("Headline tag", "Inter Display Black · 64 px · black on a Shark Cyan box · top of frame · e.g. <span class='tag'>AI DRIVE-THRU FAIL</span>"),
             ("Name tag", "Inter Display ExtraBold · 46 px · white on Deep Navy · under each host on first appearance"),
             ("Widget headline", "Inter Display Black · 40 px · first line Shark Cyan, second line white"),
             ("Widget header", "Inter Display Black · 30 px Shark Cyan topic + Inter Bold 22 px 'ARKS SHARKS'"),
             ("Source line", "Inter Medium · 23 px · Mist · always starts with 'Source:'"),
             ("End card", "Inter Display Black · 74 px · 'EPISODE 1' in cyan over 'COMING SOON' in white")])}
<p class="cap" style="margin-top:8px">Sizes are for a 1080 × 1920 frame. Fonts are free (SIL Open Font License) and installed with the build tools.</p></div>
<div><img src="{A}/tr_caption.jpg" class="fill" style="height:530px"><div class="cap">Captions and headline tag in the approved trailer.</div></div>
</div>"""))

# 08 characters overview
pages.append(page(8, "06 · The characters", f"""<div class="content" style="display:grid; grid-template-columns: 300px 300px 1fr; gap:26px">
<div><img src="{A}/ahmed_master.jpg" class="fill" style="height:560px"></div>
<div><img src="{A}/kamran_master.jpg" class="fill" style="height:560px"></div>
<div><div class="sec">06 · The characters</div><h1>Ahmed &amp;<br>Kamran</h1>
<p style="font-size:15px">Stylised 3D animated versions of the two real hosts, in a high-end animated-feature look: soft skin shading,
slightly larger heads and expressive eyes, clean shapes. They must always be recognisable as themselves.</p>
<div class="card" style="margin-top:10px"><h3>The duo</h3>
<p><b>Ahmed</b> is the host and anchor: curious, cheeky, sets up each topic and asks what the viewer is thinking.</p>
<p><b>Kamran</b> is the co-host and storyteller: animated, quick, brings the facts and the funniest stories.</p>
<p style="margin:0">Together: warm banter, real laughs, always on each other's side.</p></div>
<div style="margin-top:14px"><span class="pill">AHMED · SEATED LEFT</span><span class="pill">KAMRAN · SEATED RIGHT</span><span class="pill">UK ENGLISH</span></div>
</div></div>"""))


def char_page(n, sec, name, master, expr, rows, quote):
    return page(n, sec, f"""<div class="content" style="display:grid; grid-template-columns: 270px 1fr; gap:30px">
<div><img src="{A}/{master}" class="fill" style="height:560px"></div>
<div><div class="sec">{sec}</div><h1 style="margin-bottom:8px">{name}</h1>
<div style="font:800 17px 'Inter Display'; color:#00E5FF; margin-bottom:10px">{quote}</div>
<div class="grid" style="grid-template-columns: 1fr 380px; gap:22px">
<div>{spec_table(rows)}</div>
<div><img src="{A}/{expr}" class="fill" style="height:253px; object-fit:contain; background:#081628"><div class="cap">Expression sheet: neutral, speaking, laugh, surprised, thinking, pointing.</div></div>
</div></div></div>""")


pages.append(char_page(9, "07 · Ahmed", "Ahmed", "ahmed_master.jpg", "ahmed_expr.jpg", [
    ("Role", "Host. Opens the show, sets up topics, asks the questions."),
    ("Persona", "Warm, confident, cheeky. Loves a punchline and a dramatic pause."),
    ("Face & hair", "Round full face, light warm-tan skin, buzzed dark hair with a receding hairline, thick dark straight brows, brown eyes"),
    ("Beard", "Full, neatly trimmed short black beard and moustache"),
    ("Build", "Broad, stocky"),
    ("Wardrobe (locked)", "Camel-tan blazer worn open · black fine-knit turtleneck · charcoal trousers · white leather sneakers · silver watch, left wrist"),
    ("Seat", "Left chair, holding a glass of karak"),
    ("Signature moves", "Leans in to the camera · straightens his blazer lapels · points at camera"),
    ("Voice", "His own cloned voice (Cartesia), UK English with his natural accent"),
], "“Welcome to ARKS Sharks. I'm Ahmed.”"))
pages.append(char_page(10, "08 · Kamran", "Kamran", "kamran_master.jpg", "kamran_expr.jpg", [
    ("Role", "Co-host. Brings the facts, the numbers and the funny stories."),
    ("Persona", "Animated, quick, expressive hands. Big laugh, wide-eyed disbelief."),
    ("Face & hair", "Full cheeks, olive-tan skin, dark wavy textured hair on top, short faded sides, receding hairline, thick dark brows, brown eyes"),
    ("Beard", "Full short dark beard and moustache with a salt-and-pepper grey patch on the chin"),
    ("Build", "Medium, athletic"),
    ("Wardrobe (locked)", "Dark olive-green bomber jacket worn open · white crew-neck T-shirt · black jeans · white sneakers · black smartwatch"),
    ("Seat", "Right chair, holding a glass of karak"),
    ("Signature moves", "Counts on his fingers · mimes the story with his hands · points and laughs"),
    ("Voice", "His own cloned voice (Cartesia), UK English with his natural accent"),
], "“I'm Kamran. We hunt the AI news…”"))

# 11 character rules
pages.append(page(11, "09 · Character rules", f"""<div class="content" style="display:grid; grid-template-columns: 1fr 1fr 360px; gap:26px">
<div><div class="sec">09 · Character rules</div><h1>Always on-model</h1>
<h3><span class="yes">✓</span> Always</h3><ul>
<li>Same faces, hair, beards and outfits in every shot, using the master images as references.</li>
<li>Repeat the identity description word for word in every generation prompt (see page 19).</li>
<li>Ahmed sits left, Kamran sits right. Karak glasses on the table or in hand.</li>
<li>Podcast mics on boom arms beside them, never covering a mouth.</li>
<li>Natural, friendly acting: looking at each other while they chat, at the camera to open and close.</li></ul></div>
<div style="padding-top:96px"><h3><span class="no">✕</span> Never</h3><ul>
<li>No outfit changes mid-scene. No ties, suits or sunglasses. (The AI once gave Kamran a tie when he said "tie": cut around it.)</li>
<li>No extra people on set, no other characters wearing the hosts' outfits.</li>
<li>No red clothing or props.</li>
<li>No realistic photo versions: always the animated style.</li>
<li>Never put words in the hosts' mouths about real people or companies without a source.</li></ul></div>
<div><img src="{A}/kf_two.jpg" class="fill" style="height:560px"></div>
</div>"""))

# 12 studio
calls = [(50, 9, 1, "Lighting truss with spotlights"), (50, 33, 2, "Curved window, Burj Khalifa at dusk"), (93, 42, 3, "Neural-network LED walls"),
         (8, 54, 4, "Broadcast camera"), (27, 58, 5, "Charcoal leather swivel chairs"), (40, 54, 6, "Podcast mics on boom arms"),
         (53, 61, 7, "Round glowing table, karak glasses"), (50, 72, 8, "Raised circular platform, cyan edge")]
dots = "".join(f'<div class="num" style="left:calc({x}% - 14px); top:calc({y}% - 14px)">{k}</div>' for x, y, k, _ in calls)
legend = "".join(f'<div style="display:flex; gap:12px; align-items:center; margin-bottom:9px"><div class="num" style="position:static; flex:none">{k}</div>'
                 f'<div style="font:600 14px Inter; color:#fff">{t}</div></div>' for _, _, k, t in calls)
pages.append(page(12, "10 · The studio", f"""<div class="content" style="display:grid; grid-template-columns: 330px 1fr; gap:40px">
<div style="position:relative; height:586px"><img src="{A}/studio.jpg" class="fill" style="height:586px">{dots}</div>
<div><div class="sec">10 · The studio</div><h1>A broadcast studio<br>above Dubai</h1>
<p style="font-size:15px; max-width:620px">A real TV talk-show studio, never a living room, high above the city at dusk. It feels premium but relaxed:
two friends in comfortable chairs, karak on the table, the Burj Khalifa between them and AI glowing on the walls.</p>
<div class="grid g2" style="margin-top:14px"><div>{legend}</div>
<div class="card"><h3>Set rules</h3><ul><li>Time of day is always dusk: orange-pink to deep-blue sky.</li>
<li>Burj Khalifa visible between the hosts in wide shots.</li><li>LED walls show only abstract neural-network graphics, never text.</li>
<li>No logos or readable text inside the set; brand graphics are added in the edit.</li><li>No red anywhere.</li></ul></div></div>
</div></div>"""))

# 13 studio lighting & framing
pages.append(page(13, "11 · Studio lighting & framing", f"""<div class="content">
<div class="sec">11 · Studio lighting &amp; framing</div><h1 style="margin-bottom:14px">Teal and amber, always at dusk</h1>
<div class="grid" style="grid-template-columns: repeat(4, 1fr) 300px; gap:16px">
 <div><img src="{A}/kf_two.jpg" class="fill" style="height:400px"><div class="cap">Two-shot: the default conversation frame.</div></div>
 <div><img src="{A}/kf_ahm.jpg" class="fill" style="height:400px"><div class="cap">Close-up, Ahmed: punchlines, questions.</div></div>
 <div><img src="{A}/kf_kam.jpg" class="fill" style="height:400px"><div class="cap">Close-up, Kamran: reactions, stories.</div></div>
 <div><img src="{A}/in_dive.jpg" class="fill" style="height:400px"><div class="cap">Exterior: brand film and trailer titles only.</div></div>
 <div class="card">{spec_table([("Key light", "Warm amber, front-left"), ("Rim light", "Cool cyan-violet from the LED walls"), ("Atmosphere", "Light haze in the spotlight beams"),
                                ("Grade", "Teal and amber, rich but natural skin"), ("Lens", "Shallow depth of field, subtle film grain"), ("Camera", "Slow push-ins and gentle arcs; hard cuts between shots"),
                                ("Never", "Red tones, harsh flat light, daylight scenes")])}</div>
</div></div>"""))

# 14 layout & safe zones
pages.append(page(14, "12 · 9:16 layout & safe zones", f"""<div class="content" style="display:grid; grid-template-columns: 300px 1fr; gap:44px">
<div><img src="{A}/safezones.jpg" class="fill" style="height:534px; object-fit:contain"></div>
<div><div class="sec">12 · 9:16 layout &amp; safe zones</div><h1>Every frame has a place for everything</h1>
<div class="grid g2" style="gap:18px">
 <div class="card"><h3>Widget zone · top</h3><p>y 58–625 px, 800 px wide, centred. Topic cards live here. Faces must never be covered: frame the hosts lower when widgets are used.</p></div>
 <div class="card"><h3>Faces · middle</h3><p>y 660–1180 px. Keep clear of all graphics. Name tags go just below the faces on first appearance.</p></div>
 <div class="card"><h3>Captions · lower middle</h3><p>Baseline at about y 1450 px, inside 90 px side margins. One to three words at a time.</p></div>
 <div class="card"><h3>Platform UI · bottom</h3><p>The bottom 320 px is covered by TikTok, Reels and Shorts buttons. No text, logos or key action there.</p></div>
</div>
<p style="margin-top:14px">Universal safe area: <b>900 × 1400 px centred</b>. Headline tags sit at the very top (y ≈ 250 px) when no widget is showing.</p>
</div></div>"""))

# 15 on-screen graphics
pages.append(page(15, "13 · On-screen graphics", f"""<div class="content">
<div class="sec">13 · On-screen graphics</div><h1 style="margin-bottom:12px">The graphics system</h1>
<div class="grid" style="grid-template-columns: 1.15fr 1fr 1fr 0.62fr 0.62fr; gap:14px">
 <div><img src="{A}/card_image.png" style="width:100%"><div class="cap"><b>Topic widget, image card.</b> Header: fin + topic in cyan + "ARKS SHARKS". Image with an
 <span class="tag" style="font-size:9px; padding:1px 5px">ILLUSTRATION</span> tag when AI-made. Headline in two lines. Source line, always.</div></div>
 <div><img src="{A}/card_stat.png" style="width:100%"><div class="cap"><b>Stat card.</b> One big number, a progress bar, a two-line headline and the source.</div></div>
 <div><img src="{A}/card_ratio.png" style="width:100%"><div class="cap"><b>Ratio card.</b> "N in M" with icons; the highlighted one in Shark Cyan.</div></div>
 <div><img src="{A}/tr_hook.jpg" class="fill" style="height:330px"><div class="cap"><b>Headline tag + captions.</b></div></div>
 <div><img src="{A}/tr_end.jpg" class="fill" style="height:330px"><div class="cap"><b>End card.</b> Blurred studio, logo, episode line.</div></div>
</div>
<div class="grid g4" style="margin-top:14px; gap:14px">
 <div class="card"><h3>Widgets</h3><p>Change on every line of dialogue. Slide in 36 px and fade in over 0.3 s; fade out over 0.2 s.</p></div>
 <div class="card"><h3>Sources</h3><p>Every factual card shows "Source: …" with the outlet and date. Opinions and jokes don't need one.</p></div>
 <div class="card"><h3>Name tags</h3><p>White on Deep Navy, under each host for the first 4 seconds of a video.</p></div>
 <div class="card"><h3>Logo slam</h3><p>At the title moment: logo scales from 150% to 100% with a bass hit, holds about 2 s.</p></div>
</div></div>"""))

# 16 motion & editing
pages.append(page(16, "14 · Motion & editing", f"""<div class="content">
<div class="sec">14 · Motion &amp; editing</div><h1 style="margin-bottom:12px">Hook fast, then talk like friends</h1>
<div class="grid" style="grid-template-columns: 1fr 1fr 1fr 1.3fr; gap:16px">
 <div><img src="{A}/hook_frame.jpg" class="fill" style="height:300px"><div class="cap"><b>0–2.5 s: the hook.</b> Strongest line, headline tag, small logo, captions. No opener.</div></div>
 <div><img src="{A}/in_dive.jpg" class="fill" style="height:300px"><div class="cap">Brand film (trailers and promos only): the shark dives through the studio glass.</div></div>
 <div><img src="{A}/in_logo.jpg" class="fill" style="height:300px"><div class="cap">Brand film end: lights up, logo lands, sonic logo.</div></div>
 <div class="card"><h3>Editing rules</h3><ul>
 <li><b>Hook in the first 3 s</b>, with on-screen text from frame 1.</li><li>Trailers: a new cut every 2–4 s. Episodes: let conversations breathe.</li>
 <li><b>No opener.</b> Every video starts with a 2.5 s hook, then the sound-logo hit cuts into the conversation.</li><li>Hard cuts between shots; no flashy transitions.</li>
 <li>Captions on everything: most viewers watch muted.</li><li>Cover AI glitches (outfit morphs, odd hands) with a reaction cutaway.</li></ul></div>
</div>
<h3 style="margin-top:18px">Approved trailer structure (55 s)</h3>
<div class="tl"><div style="flex:7; background:#00E5FF">Hook · 7 s</div><div style="flex:5; background:#6CE6F5">Title · logo slam · 5 s</div>
<div style="flex:7.5; background:#2B4FBF; color:#fff">Who we are · 7.5 s</div><div style="flex:9.2; background:#8B5CF6; color:#fff">Rapid-fire news · 9 s</div>
<div style="flex:14; background:#E39A3B">Funny corner · 14 s</div><div style="flex:9; background:#E9EDF0">Sign-off · 9 s</div><div style="flex:3.2; background:#081628; color:#fff">End card</div></div>
</div>"""))

# 17 sound
pages.append(page(17, "15 · Sound identity", f"""<div class="content">
<div class="sec">15 · Sound identity</div><h1 style="margin-bottom:14px">Their real voices, clean and close</h1>
<div class="grid g3" style="gap:18px">
 <div class="card"><h3>Voices</h3><p>Always the hosts' <b>own cloned voices</b> (Cartesia), UK English with their natural accents. Never a stock voice.</p>
 <p>Lip-sync route: the animation is generated from the lines, then each speaker is converted back to his real voice so the timing matches the mouth.</p></div>
 <div class="card"><h3>Voice processing</h3><ul><li>De-reverb (WPE)</li><li>Neural noise removal (RNNoise, voice model)</li><li>Gentle spectral denoise</li>
 <li>De-click, de-ess</li><li>EQ: −2.5 dB at 220 Hz, +2.2 dB at 3.8 kHz, +1.5 dB air shelf</li><li>Light compression (2.2:1)</li></ul>
 <p class="cap">No noise gate: it swallows soft consonants.</p></div>
 <div class="card"><h3>Loudness</h3>{spec_table([("Master", "−14 LUFS integrated"), ("True peak", "≤ −1.5 dBTP"), ("Music bed", "18–20 dB under dialogue, side-chain ducked"), ("SFX", "6 dB under dialogue")])}</div>
</div>
<div class="grid g2" style="gap:18px; margin-top:16px">
 <div class="card"><h3>Sonic logo</h3><p>Low drone → riser → sub impact, then a bright three-note motif <b>A – E – A</b> with a shimmer tail. Plays as the hook cuts into the conversation, and on title slams.</p></div>
 <div class="card"><h3>Music</h3><p>Original, licence-free beds made for the show: 120 BPM cinematic electronic, chords Am – F – C – G. Trailer mode has the hook drone, riser and impacts; conversation mode is a soft groove.
 <b>Never</b> use tracks with unclear rights.</p></div>
</div></div>"""))

# 18 tone & content
pages.append(page(18, "16 · Tone of voice & content", f"""<div class="content">
<div class="sec">16 · Tone of voice &amp; content rules</div><h1 style="margin-bottom:12px">Sound like two mates who know their stuff</h1>
<div class="grid g3" style="gap:18px">
 <div class="card"><h3>Voice</h3><ul><li>UK English, short sentences, spoken not written.</li><li>Light Arabic flavour used naturally: <b>Yalla</b>, <b>Habibi</b>, <b>Wallah</b>, <b>Shukran</b>.</li>
 <li>Questions and reactions between the hosts keep it a conversation.</li><li>Explain jargon in one breath ("agentic AI: AI that actually does tasks for you").</li></ul></div>
 <div class="card"><h3>Content rules</h3><ul><li>Every fact is real, recent and sourced; the source appears on screen.</li><li>AI-made pictures carry the "ILLUSTRATION" tag.</li>
 <li>Funny corner: real, documented AI fails only.</li><li>Kind humour: laugh at the tech, never at people.</li><li>No claims about real people's experiences unless they're true.</li></ul></div>
 <div class="card"><h3>Say it like this</h3>
 <p><span class="yes">✓</span> “Mate, you already can! Umm Suqeim and Jumeirah, since March.”</p>
 <p><span class="no">✕</span> “Commercial autonomous mobility services have been deployed in select districts.”</p>
 <p><span class="yes">✓</span> “Treat AI like a brilliant intern: fast, helpful, but check its work.”</p>
 <p><span class="no">✕</span> “AI will replace everyone by next year.” (unsourced hype)</p></div>
</div>
<div class="card" style="margin-top:16px"><h3>Sign-off &amp; catchphrases</h3><p>“We hunt the AI news… so you don't have to.” · “New features. Funny fails. Real talk.” · “ARKS Sharks! Yalla… dive in!”</p></div>
</div>"""))

# 19 specs & assets
pages.append(page(19, "17 · Technical specs & asset index", f"""<div class="content">
<div class="sec">17 · Technical specs &amp; asset index</div><h1 style="margin-bottom:12px">Make it the same way every time</h1>
<div class="grid" style="grid-template-columns: 1fr 1.25fr; gap:24px">
 <div class="card">{spec_table([("Format", "9:16 vertical, 1080 × 1920, 24 fps"), ("Video", "H.264, CRF 20, yuv420p, fast-start"), ("Audio", "AAC 192 kbps, 44.1 kHz stereo, −14 LUFS"),
   ("Generation", "Seedance 2.0 reference-to-video, 720p, upscaled to 1080p; Seedream 5.0 for stills"), ("Voices", "Cartesia sonic-3 · Ahmed c1063679-503f… · Kamran f21c147a-0d3b…"),
   ("Recipe", "<span class='mono'>.claude/skills/arks-sharks-video/SKILL.md</span>"), ("Tools", "<span class='mono'>show/tools/</span> (generation, voice swap, clean-up, widgets, assembly, finalise)")])}</div>
 <div class="card">{spec_table([("Logo", "<span class='mono'>show/brand/arks_sharks_logo_*.png / .jpg</span>"), ("Characters", "<span class='mono'>characters/ahmed/, characters/kamran/</span> (masters, expressions)"),
   ("Studio", "<span class='mono'>show/trailer/keyframes/talkshow_studio.jpg, kf_two/kf_ahm/kf_kam.jpg</span>"), ("Approved trailer", "<span class='mono'>show/final/ARKS_Sharks_Trailer_v1_APPROVED_9x16.mp4</span>"),
   ("Hook", "<span class='mono'>show/tools/hook.py</span> (2.5 s, no opener). Brand film for trailers: <span class='mono'>show/final/ARKS_Sharks_Episode_Intro_v1_9x16.mp4</span>"), ("Widget style", "<span class='mono'>show/tools/widgets.py</span> + example cards in <span class='mono'>show/tests/conv20/</span>"),
   ("Prompts", "<span class='mono'>show/trailer/prompts/</span> (identity strings, set, lighting)"), ("This book", "<span class='mono'>show/brand/ci/build_ci.py</span> rebuilds it")])}</div>
</div>
<p class="cap" style="margin-top:12px">Identity strings for generation: <b>Ahmed</b>: round full face, buzzed receding dark hair, full short black beard, camel-tan blazer over a black turtleneck, silver watch.
<b>Kamran</b>: dark wavy textured hair with short faded sides, full dark beard with a salt-and-pepper grey chin, olive-green bomber jacket over a white t-shirt, black smartwatch.</p>
</div>"""))

# 20 back cover
pages.append(page(20, "", f"""
<img src="{A}/studio.jpg" style="position:absolute; inset:-20px; width:calc(100% + 40px); height:calc(100% + 40px); object-fit:cover; object-position:50% 45%; filter:blur(8px) brightness(.32)">
<div style="position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center">
<img src="{A}/logo_shadow.png" style="width:620px">
<div style="font:900 30px 'Inter Display'; color:#fff; margin-top:16px">We hunt the AI news… <span class="cy">so you don't have to.</span></div>
<div class="sec" style="margin-top:20px">Dubai · {DATE}</div></div>""", chrome=False))

html = f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>ARKS Sharks CI Guidelines</title><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
out_html = HERE / "ARKS_Sharks_CI_Guidelines.html"; out_html.write_text(html)
out_pdf = HERE.parent / f"ARKS_Sharks_CI_Guidelines_v{VERSION.split('.')[0]}.pdf"
import os, subprocess
prev = os.environ.get("CI_PREVIEW_DIR")  # optional: also save PNG previews of every page
subprocess.run(["node", str(HERE / "render_pdf.js"), str(out_html), str(out_pdf)] + ([prev] if prev else []), check=True)
print("pdf:", out_pdf, f"{out_pdf.stat().st_size / 1e6:.1f} MB", "| pages:", len(pages))
