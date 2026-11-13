"""Package the ARKS Sharks Corporate Identity kit (folders + README) into one zip.
Run from the repo root:  python3 show/brand/ci/make_ci_kit.py
Output: show/_work/ARKS_Sharks_CI_Kit_v1/ and show/_work/ARKS_Sharks_CI_Kit_v1.zip"""
import json, shutil, struct, subprocess, zipfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]; CI = ROOT / "show/brand/ci"; KIT = ROOT / "show/_work/ARKS_Sharks_CI_Kit_v1"
if KIT.exists(): shutil.rmtree(KIT)
F = Path("/usr/share/fonts/opentype/inter")
def d(p): q = KIT / p; q.mkdir(parents=True, exist_ok=True); return q
def cp(src, dst): shutil.copy2(ROOT / src, dst)
def font(n, s): return ImageFont.truetype(str(F / n), s)
def run(*a): subprocess.run([str(x) for x in a], check=True)

PAL = [("Shark Cyan", "#00E5FF", "Signature accent: logo fin, caption key words, card borders, LED edges"),
       ("Deep Navy", "#081628", "Cards, panels, name tags"), ("Midnight", "#04080F", "Backgrounds, end cards, title cards"),
       ("Chrome", "#E9EDF0", "Wordmark, headline text, white type"), ("Neural Blue", "#2B4FBF", "LED walls, data graphics, gradients"),
       ("Neural Violet", "#8B5CF6", "LED node glow, secondary highlights"), ("Karak Amber", "#E39A3B", "Warm key light, karak tea, warm accents"),
       ("Mist", "#96B9CD", "Secondary text, source lines, small labels")]
WARD = [("Camel", "#C8875A", "Ahmed's blazer"), ("Jet", "#111214", "Ahmed's turtleneck"), ("Olive", "#4A5233", "Kamran's bomber"),
        ("Tee White", "#F4F4F2", "Kamran's T-shirt"), ("Charcoal", "#3A3D42", "Studio chairs, trousers")]
def rgb(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
def cmyk(h):
    r, g, b = [v / 255 for v in rgb(h)]; k = 1 - max(r, g, b)
    if k >= 1: return (0, 0, 0, 100)
    return tuple(round(100 * v) for v in ((1 - r - k) / (1 - k), (1 - g - k) / (1 - k), (1 - b - k) / (1 - k), k))

# 01 guidelines
cp("show/brand/ARKS_Sharks_CI_Guidelines_v1.pdf", d("01_Guidelines"))

# 02 logo
L = d("02_Logo")
cp("show/brand/arks_sharks_logo_alpha.png", L / "ARKS_Sharks_Logo_Transparent.png")
cp("show/brand/arks_sharks_logo_shadow.png", L / "ARKS_Sharks_Logo_Shadow_ForVideo.png")
cp("show/brand/arks_sharks_logo_v1.jpg", L / "ARKS_Sharks_Logo_OnBlack.jpg")
cp("show/brand/ci/assets/fin.png", L / "ARKS_Sharks_Fin_Icon_Transparent.png")
av = Image.open(ROOT / "show/brand/ci/assets/avatar.png"); av.save(L / "ARKS_Sharks_Avatar_600.png")
av.resize((1080, 1080), Image.LANCZOS).save(L / "ARKS_Sharks_Avatar_1080.png")

# 03 colours
C = d("03_Colours")
(C / "palette.json").write_text(json.dumps({"brand": [{"name": n, "hex": h, "rgb": rgb(h), "cmyk_approx": cmyk(h), "use": u} for n, h, u in PAL],
                                            "wardrobe": [{"name": n, "hex": h, "rgb": rgb(h), "use": u} for n, h, u in WARD],
                                            "forbidden": [{"name": "Red", "rule": "Never use red in set, graphics, logo or images"}]}, indent=1))
(C / "palette.css").write_text(":root {\n" + "".join(f"  --arks-{n.lower().replace(' ', '-')}: {h};  /* {u} */\n" for n, h, u in PAL + WARD) + "}\n")
(C / "palette.txt").write_text("ARKS Sharks colour palette (CMYK values are approximate; proof before print)\n\n" + "".join(
    f"{n:14s} {h}   RGB {rgb(h)}   CMYK {cmyk(h)}   {u}\n" for n, h, u in PAL) + "\nWardrobe locks\n" + "".join(
    f"{n:14s} {h}   RGB {rgb(h)}   {u}\n" for n, h, u in WARD) + "\nForbidden: red. Warm moments use Karak Amber.\n")
def ase(path, colours):  # Adobe Swatch Exchange (RGB, global swatches)
    blocks = b""
    for n, h, _ in colours:
        name = (n + "\0").encode("utf-16-be"); r, g, b = [v / 255 for v in rgb(h)]
        body = struct.pack(">H", len(n) + 1) + name + b"RGB " + struct.pack(">fff", r, g, b) + struct.pack(">H", 0)
        blocks += struct.pack(">HI", 0x0001, len(body)) + body
    path.write_bytes(b"ASEF" + struct.pack(">HHI", 1, 0, len(colours)) + blocks)
ase(C / "ARKS_Sharks_Palette.ase", PAL + WARD)
sheet = Image.new("RGB", (2000, 1000), (4, 8, 15)); dr = ImageDraw.Draw(sheet)
dr.text((60, 40), "ARKS SHARKS · COLOUR PALETTE", font=font("InterDisplay-Black.otf", 44), fill=(0, 229, 255))
for i, (n, h, u) in enumerate(PAL):
    x, y = 60 + (i % 4) * 480, 130 + (i // 4) * 400
    dr.rounded_rectangle((x, y, x + 440, y + 220), 18, fill=rgb(h), outline=(60, 80, 100), width=2)
    dr.text((x, y + 236), n, font=font("InterDisplay-Black.otf", 34), fill=(255, 255, 255))
    dr.text((x, y + 280), f"{h}  ·  RGB {', '.join(map(str, rgb(h)))}", font=font("Inter-Medium.otf", 22), fill=(0, 229, 255))
    dr.text((x, y + 312), "CMYK ≈ " + ", ".join(map(str, cmyk(h))), font=font("Inter-Medium.otf", 20), fill=(150, 185, 205))
sheet.save(C / "ARKS_Sharks_Palette.png")

# 04 typography
T = d("04_Typography")
for f in ["InterDisplay-Black.otf", "InterDisplay-ExtraBold.otf", "InterDisplay-Bold.otf", "Inter-Bold.otf", "Inter-SemiBold.otf", "Inter-Medium.otf", "Inter-Regular.otf"]:
    shutil.copy2(F / f, T / f)
shutil.copy2("/usr/share/doc/fonts-inter/copyright", T / "OFL_Inter_License.txt")
ts = Image.new("RGB", (2000, 1100), (4, 8, 15)); dr = ImageDraw.Draw(ts); y = 50
for label, fn, size, sample, col in [("CAPTIONS · Inter Display Black · 82 px", "InterDisplay-Black.otf", 82, "WE HUNT THE AI NEWS", (255, 255, 255)),
                                     ("HEADLINE TAG · Inter Display Black · 64 px on Shark Cyan", "InterDisplay-Black.otf", 64, "AI DRIVE-THRU FAIL", (0, 0, 0)),
                                     ("NAME TAG · Inter Display ExtraBold · 46 px", "InterDisplay-ExtraBold.otf", 46, "AHMED     KAMRAN", (255, 255, 255)),
                                     ("WIDGET HEADLINE · Inter Display Black · 40 px", "InterDisplay-Black.otf", 40, "LIVE SINCE 30 MARCH 2026", (0, 229, 255)),
                                     ("SOURCE LINE · Inter Medium · 23 px", "Inter-Medium.otf", 23, "Source: RTA · WAM, 30 March 2026", (150, 185, 205))]:
    dr.text((60, y), label, font=font("Inter-Bold.otf", 22), fill=(150, 185, 205)); y += 36
    f2 = font(fn, size)
    if "HEADLINE TAG" in label:
        w = dr.textlength(sample, font=f2); dr.rounded_rectangle((56, y - 6, 76 + w, y + size + 14), 10, fill=(0, 229, 255))
    if "CAPTIONS" in label:
        dr.text((60, y), sample, font=f2, fill=col, stroke_width=6, stroke_fill=(0, 0, 0))
    elif "NAME TAG" in label:
        dr.rounded_rectangle((56, y - 6, 300, y + size + 12), 8, fill=(8, 22, 40)); dr.rounded_rectangle((400, y - 6, 700, y + size + 12), 8, fill=(8, 22, 40))
        dr.text((70, y), "AHMED", font=f2, fill=col); dr.text((414, y), "KAMRAN", font=f2, fill=col)
    else:
        dr.text((66 if "HEADLINE" in label else 60, y), sample, font=f2, fill=col)
    y += size + 60
ts.save(T / "ARKS_Sharks_Type_Scale.png")

# 05 characters
for who in ("ahmed", "kamran"):
    D = d(f"05_Characters/{who.capitalize()}")
    cp(f"characters/{who}/{who}_master.jpg", D / f"{who.capitalize()}_Master_Design.jpg")
    cp(f"characters/{who}/{who}_expressions.jpg", D / f"{who.capitalize()}_Expression_Sheet.jpg")
cp("characters/00_cast_board.jpg", d("05_Characters") / "ARKS_Sharks_Cast_Board.jpg")
(KIT / "05_Characters/Character_Profiles.md").write_text("""# Character profiles

## Ahmed (host, seated left)
- **Persona:** warm, confident, cheeky; loves a punchline and a dramatic pause. Opens the show, sets up topics, asks the questions.
- **Face & hair:** round full face, light warm-tan skin, buzzed dark hair with a receding hairline, thick dark straight brows, brown eyes.
- **Beard:** full, neatly trimmed short black beard and moustache. **Build:** broad, stocky.
- **Wardrobe (locked):** camel-tan blazer worn open · black fine-knit turtleneck · charcoal trousers · white leather sneakers · silver watch on the left wrist.
- **Signature moves:** leans in to the camera · straightens his blazer lapels · points at the camera.
- **Voice:** his own cloned voice, UK English with his natural accent.

## Kamran (co-host, seated right)
- **Persona:** animated, quick, expressive hands; big laugh, wide-eyed disbelief. Brings the facts, numbers and the funny stories.
- **Face & hair:** full cheeks, olive-tan skin, dark wavy textured hair on top with short faded sides and a receding hairline, thick dark brows, brown eyes.
- **Beard:** full short dark beard and moustache with a salt-and-pepper grey patch on the chin. **Build:** medium, athletic.
- **Wardrobe (locked):** dark olive-green bomber jacket worn open · white crew-neck T-shirt · black jeans · white sneakers · black smartwatch.
- **Signature moves:** counts on his fingers · mimes the story with his hands · points and laughs.
- **Voice:** his own cloned voice, UK English with his natural accent.

## Always / never
- Always the same faces, outfits and seats; karak glasses on the table or in hand; mics beside them, never covering a mouth.
- Never: outfit changes mid-scene, ties, suits, sunglasses, red clothing, realistic photo versions, extra people on set.
""")

# 06 studio
S = d("06_Studio")
for src, dst in [("show/trailer/keyframes/talkshow_studio.jpg", "Studio_Main_Set.jpg"), ("show/trailer/keyframes/kf_two.jpg", "Framing_TwoShot.jpg"),
                 ("show/trailer/keyframes/kf_ahm.jpg", "Framing_CloseUp_Ahmed.jpg"), ("show/trailer/keyframes/kf_kam.jpg", "Framing_CloseUp_Kamran.jpg"),
                 ("show/brand/ci/assets/in_burj.jpg", "Opener_Exterior_Burj_Khalifa.jpg"), ("show/brand/ci/assets/in_dive.jpg", "Opener_Shark_Through_Window.jpg")]:
    cp(src, S / dst)

# 07 graphics
G = d("07_Graphics/Widget_Cards"); E = d("07_Graphics/Examples")
for i, name in enumerate(["Image_Card_Robotaxi", "Image_Card_Map", "Image_Card_App", "Stat_Card_25pc", "Ratio_Card_1in4", "Image_Card_Fun"], 1):
    cp(f"show/tests/conv20/widgets/cards/c{i}.png", G / f"Widget_{i}_{name}.png")
for src, dst in [("tr_hook", "Headline_Tag_and_Captions"), ("tr_logo", "Logo_Slam"), ("tr_names", "Name_Tags"), ("tr_tag", "Headline_Tag_CloseUp"),
                 ("tr_end", "End_Card"), ("cv_widget", "Widget_In_Frame"), ("cv_ratio", "Widget_Ratio_In_Frame")]:
    cp(f"show/brand/ci/assets/{src}.jpg", E / f"{dst}.jpg")
cp("show/brand/ci/assets/safezones.jpg", d("07_Graphics") / "Safe_Zones_9x16.jpg")

# 08 sound
SD = d("08_Sound"); W = ROOT / "show/_work/ci_sound"; W.mkdir(parents=True, exist_ok=True)
run("python3", ROOT / "show/tools/sting.py", W / "sting.wav", "5.2", "2.3")
run("ffmpeg", "-v", "error", "-y", "-i", W / "sting.wav", "-af", "loudnorm=I=-14:TP=-1.5", "-ar", "44100", SD / "ARKS_Sharks_Sound_Logo.wav")
run("python3", ROOT / "show/tools/music.py", W / "bed_trailer.wav", "40", "4.2", "36.5")
run("python3", ROOT / "show/tools/music.py", W / "bed_conv.wav", "60", "0", "59", "bed")
for src, dst in [("bed_trailer.wav", "ARKS_Sharks_Music_Trailer_Bed_40s.mp3"), ("bed_conv.wav", "ARKS_Sharks_Music_Conversation_Bed_60s.mp3")]:
    run("ffmpeg", "-v", "error", "-y", "-i", W / src, "-af", "loudnorm=I=-16:TP=-1.5", "-c:a", "libmp3lame", "-b:a", "256k", SD / dst)

# 09 video references
V = d("09_Video_References")
cp("show/final/ARKS_Sharks_Trailer_v1_APPROVED_9x16.mp4", V / "ARKS_Sharks_Trailer_v1_APPROVED_9x16.mp4")
cp("show/final/ARKS_Sharks_Episode_Intro_v1_9x16.mp4", V / "ARKS_Sharks_Brand_Film_TrailersOnly_9x16.mp4")
cp("show/final/ARKS_Sharks_Conversation_Test_Robotaxis_WithHook_9x16.mp4", V / "ARKS_Sharks_Hook_Example_9x16.mp4")

# 10 production
P = d("10_Production")
(P / "Identity_Prompts.txt").write_text("""Repeat these word for word in every image/video generation prompt.

Ahmed — round full face, buzzed receding dark hair, full short black beard, camel-tan blazer over a black turtleneck, silver watch
Kamran — dark wavy textured hair with short faded sides, full dark beard with a salt-and-pepper grey chin, olive-green bomber jacket over a white t-shirt, black smartwatch

Studio — a Dubai TV talk-show studio: charcoal-leather chairs on a raised circular platform with a glowing cyan edge, black podcast
microphones on boom arms (never covering mouths), a small round glowing white table with glass cups of golden karak tea, studio
spotlights on a black lighting truss, tall LED walls with blue-violet neural-network graphics, the Burj Khalifa at dusk through the
curved window.

Lighting — warm amber key light from front-left, cool cyan-violet rim light from the LED walls, light haze; teal-and-amber grade, no red tones.
Style — high-end 3D animated feature film, expressive cartoon acting, shallow depth of field, subtle film grain.
Negatives — no text, no subtitles, no captions, no logos, no watermark.
""")
(P / "Voices.txt").write_text("""Host voices (Cartesia, model sonic-3) — clones of the hosts' own voices. Use only for approved ARKS Sharks content.
Ahmed:  c1063679-503f-4961-b8ed-aab0ae1d924b
Kamran: f21c147a-0d3b-4b21-ab87-bedcb1374749
The API key is not included in this kit. It lives in the production environment's secret settings.
""")
shutil.copy2(ROOT / ".claude/skills/arks-sharks-video/SKILL.md", P / "Production_Recipe.md")

# README (markdown + PDF)
md = (CI / "README_CI_KIT.md").read_text(); (KIT / "README.md").write_text(md)
import markdown
body = markdown.markdown(md, extensions=["tables"])
css = """@page { size: A4; margin: 16mm 15mm } body { font-family: 'Inter', sans-serif; color: #111; font-size: 10.5pt; line-height: 1.45 }
h1 { font-family: 'Inter Display'; font-weight: 900; font-size: 24pt; color: #04080F; border-bottom: 4px solid #00E5FF; padding-bottom: 6px }
h2 { font-family: 'Inter Display'; font-weight: 800; color: #04080F; margin-top: 18px } h3 { font-family: 'Inter Display'; color: #0a6f80; margin: 14px 0 4px }
table { border-collapse: collapse; width: 100%; margin: 6px 0 } th, td { border: 1px solid #ccd; padding: 4px 7px; text-align: left; vertical-align: top; font-size: 9.5pt }
th { background: #081628; color: #fff } code { background: #eef6f8; padding: 0 3px; border-radius: 3px; font-size: 9pt } hr { border: 0; border-top: 1px solid #ccd }"""
html_path = KIT / "README.html"
html_path.write_text(f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{css}</style></head><body>"
                     f"<img src='{(ROOT / 'show/brand/arks_sharks_logo_v1.jpg').as_uri()}' style='width:220px; float:right; border-radius:8px'>{body}</body></html>")
run("node", "-e", """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+process.argv[1],{waitUntil:'networkidle'});await p.pdf({path:process.argv[2],format:'A4',printBackground:true,
margin:{top:'16mm',bottom:'16mm',left:'15mm',right:'15mm'}});await b.close();})();""", html_path, KIT / "README.pdf")
html_path.unlink()

# zip
zp = KIT.parent / "ARKS_Sharks_CI_Kit_v1.zip"
if zp.exists(): zp.unlink()
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for f in sorted(KIT.rglob("*")):
        if f.is_file(): z.write(f, Path(KIT.name) / f.relative_to(KIT))
n = sum(1 for f in KIT.rglob("*") if f.is_file())
print(f"kit: {KIT} ({n} files) -> {zp} {zp.stat().st_size / 1e6:.1f} MB")
