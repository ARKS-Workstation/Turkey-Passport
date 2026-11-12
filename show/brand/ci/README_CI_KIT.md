# ARKS Sharks: Corporate Identity Kit v1.0

**Two friends. One topic: AI.** A vertical talk show from a Dubai studio with Ahmed and Kamran.
*"We hunt the AI news… so you don't have to."*

This kit holds everything needed to make ARKS Sharks look, sound and feel the same everywhere: episodes,
trailers, social posts, thumbnails and print. Start with **`01_Guidelines/ARKS_Sharks_CI_Guidelines_v1.pdf`**.
It is the full 20-page brand book, and this README is the quick version.

Version 1.0 · November 2026 · Dubai

---

## What's in the box

| Folder | Contents |
|---|---|
| `01_Guidelines/` | The full brand book (PDF, 20 pages) |
| `02_Logo/` | Logo with transparent background, logo with soft shadow (for use over video), logo on black, fin icon, round avatar (600 px and 1080 px) |
| `03_Colours/` | Palette sheet (PNG), Adobe swatch file (`.ase`), CSS variables, JSON, plain-text list with HEX / RGB / approximate CMYK |
| `04_Typography/` | Inter Display and Inter font files plus their licence (SIL Open Font License 1.1) and a type-scale sheet |
| `05_Characters/` | Ahmed and Kamran: master designs, expression sheets, cast board, character profiles |
| `06_Studio/` | The talk-show studio, the three standard camera framings, the exterior and opener frames |
| `07_Graphics/` | Topic widget cards (image, stat and ratio styles), examples of captions, headline tags, name tags, logo slam, end card, and the 9:16 safe-zone diagram |
| `08_Sound/` | Sound logo (WAV), trailer music bed and conversation music bed (MP3), all original and licence-free |
| `09_Video_References/` | Approved trailer (55 s) and the fixed episode opener (9.7 s) |
| `10_Production/` | Character identity prompts, voice details and the production recipe |

---

## The rules on one page

### Logo
- Use the **shadow version** over video or photos and the plain version on dark backgrounds.
- Clear space: the height of the letter "A" on every side. Minimum width: 320 px on a 1080 px frame. Fin icon: 48 px minimum.
- **Never** stretch, rotate, recolour (never red), fade it, or separate the fin from the wordmark.

### Colours
| Name | HEX | Use |
|---|---|---|
| Shark Cyan | `#00E5FF` | Signature accent: logo fin, caption key words, card borders |
| Deep Navy | `#081628` | Cards, panels, name tags |
| Midnight | `#04080F` | Backgrounds, end cards |
| Chrome | `#E9EDF0` | Wordmark, white type |
| Neural Blue | `#2B4FBF` | LED walls, data graphics |
| Neural Violet | `#8B5CF6` | LED glow, secondary highlights |
| Karak Amber | `#E39A3B` | Warm light, warm accents |
| Mist | `#96B9CD` | Secondary text, source lines |

Dark base (Midnight and Navy) about 75%, Shark Cyan about 10%, the rest accents. **No red, ever.**

### Typography
- **Inter Display Black** for captions, headlines and titles (all caps on screen).
- **Inter Display ExtraBold** for name tags. **Inter Medium/Bold** for body text and source lines.
- On a 1080 × 1920 frame: captions 82 px (white, 6 px black outline, key words in Shark Cyan, max 3 words);
  headline tag 64 px (black on cyan); name tag 46 px; widget headline 40 px; source line 23 px.

### Characters
| | Ahmed | Kamran |
|---|---|---|
| Role | Host: opens, sets up topics, asks the questions | Co-host: facts, numbers, the funny stories |
| Look | Round face, buzzed receding dark hair, full short black beard | Wavy textured hair with faded sides, full beard with a grey chin |
| Outfit (locked) | Camel blazer, black turtleneck, charcoal trousers, white sneakers, silver watch | Olive bomber, white T-shirt, black jeans, white sneakers, black smartwatch |
| Seat | Left | Right |

Always on-model: same faces, outfits and seats. No ties, no suits, no red. Mics never cover a mouth.

### Studio
A broadcast talk-show studio above Dubai at **dusk**, never a living room. It has a lighting truss, the Burj Khalifa through a
curved window, neural-network LED walls, a raised round platform with a cyan edge, charcoal chairs, podcast mics on
booms, and a round glowing table with karak. The grade is teal and amber; key light warm from the front-left, rim light cyan-violet.

### On-screen graphics (9:16)
- **Widget zone:** top of frame (y 58–625 px, 800 px wide). Topic cards change on every line.
  Every factual card shows **"Source: …"** and AI-made pictures carry an **ILLUSTRATION** tag.
- **Faces:** keep y 660–1180 px clear. **Captions:** around y 1450 px. **Bottom 320 px:** platform buttons, keep it empty.

### Sound
- The hosts' **own voices** only (cloned with their consent), UK English with their natural accents.
- Sound logo: drone, riser, impact, then the three-note motif **A–E–A**.
- Master at **−14 LUFS**, true peak ≤ −1.5 dBTP. Music sits 18–20 dB under the dialogue.

### Tone
UK English, short and spoken, light Arabic flavour (*Yalla, Habibi, Wallah, Shukran*). Two mates who know their stuff:
sourced facts, kind humour (laugh at the tech, never at people).

---

## Specs
- Video: 9:16, 1080 × 1920, 24 fps, H.264 (CRF 20), AAC 192 kbps at 44.1 kHz.
- Thumbnails and posts: use the shadow logo, the cast or studio art, and Shark Cyan type on Midnight.

## Credits and licences
- **Fonts:** Inter and Inter Display © The Inter Project Authors, SIL Open Font License 1.1 (see `04_Typography/OFL_Inter_License.txt`).
- **Music and sound logo:** original compositions made for ARKS Sharks; free to use in all ARKS Sharks content.
- **Images and video:** AI-generated for ARKS Sharks (characters, studio, logo and widget illustrations).
- **Voices:** clones of the hosts' own voices. Use them only for ARKS Sharks content approved by Ahmed and Kamran.

Questions or new assets: keep this kit and the brand book in sync. The source files and build scripts live in the
show's repository under `show/brand/`.
