---
name: arks-sharks-video
description: Make an ARKS Sharks trailer, episode or short (Ahmed and Kamran, AI talk show, Dubai studio, 9:16) using the approved pipeline that produced show/final/ARKS_Sharks_Trailer_v1_APPROVED_9x16.mp4. Use for any new ARKS Sharks video, segment or re-edit.
---

# ARKS Sharks video recipe

The approved reference is `show/final/ARKS_Sharks_Trailer_v1_APPROVED_9x16.mp4`. Match its look, sound and pacing.
All tools are in `show/tools/` and run from the repository root.

## Before generating (owner's rules)
- **Ask before starting paid generation.** Show the script and shot list first; send a short sample to hear when
  changing anything about the voices.
- The set is a **broadcast studio**, never a living room: `show/trailer/keyframes/talkshow_studio.jpg`.
- **No red** in visuals. Palette: teal, cyan, violet, amber.
- 9:16, UK English with the hosts' own (Arabic-accented) voices. Show name **ARKS Sharks**; topic AI; Dubai.
- Every claim in a script is sourced (see `show/episode01_script.md`).

## Assets
- Cast: `characters/ahmed/ahmed_master.jpg`, `characters/kamran/kamran_master.jpg` (plus expression sheets).
  Keyframes: `show/trailer/keyframes/kf_two.jpg`, `kf_kam.jpg`, `kf_ahm.jpg`.
- Identity strings (repeat verbatim in every Seedance prompt):
  - Ahmed — round full face, buzzed receding dark hair, full short black beard, camel-tan blazer over a black turtleneck, silver watch
  - Kamran — dark wavy textured hair with short faded sides, full dark beard with a salt-and-pepper grey chin, olive-green bomber jacket over a white t-shirt, black smartwatch
- Logo: `show/brand/arks_sharks_logo_shadow.png`. Episode opener: `show/final/ARKS_Sharks_Episode_Intro_v1_9x16.mp4`
  (put it at the start of every episode).
- Voices (Cartesia, `sonic-3`): Ahmed `c1063679-503f-4961-b8ed-aab0ae1d924b`, Kamran `f21c147a-0d3b-4b21-ab87-bedcb1374749`.
  The Cartesia key is a network secret on this cloud environment: send `X-API-Key: proxy-injected` and the proxy fills it in.

## Pipeline
1. **Lines:** `python3 show/tools/tts2.py VOICE_ID "text" out.wav EMOTION SPEED` for each line. Check with Cartesia
   STT. In TTS text write "A.I." and "Chat G P T".
2. **Keyframes (new framings only):** `show/tools/gen.py PROMPT.txt --refs master1 master2 studio --size 1440x2560 --out kf.jpg`
   (Seedream 5.0, about 15K tokens).
3. **Shots:** `show/tools/seed.py PROMPT.txt --model dreamina-seedance-2-0-260128 --images KEYFRAME MASTER... --audios LINE1.wav LINE2.wav --duration N --out clip.mp4`
   - 720p, 9:16, reference-to-video, `generate_audio` on, at most 3 audio references and 15 s each, 4–15 s duration.
   - Prompt shape: see `show/trailer/prompts/p_s3.txt`. Use quoted dialogue, `— his voice is audio reference N`,
     setting, lighting (no red), style, "Audio: only the voices…", negatives.
   - Cost is about 21,700 tokens per second of video. Run shots in parallel.
   - **Review the contact sheet.** Watch for outfit morphs (for example, Kamran grew a tie when he said "tie").
     Cover them with a reaction cutaway (`p_s5b.txt`, 4 s, `--no-audio`).
   - Seedance 2.5 is not activated on this ModelArk account.
4. **Voice swap:** `VC_PRECLEAN=1 python3 show/tools/vc_shot.py clip.mp4 OUTPREFIX "VOICE|line" ...` (in speaking order).
   It de-reverbs and denoises the clip audio, splits it by speaker and converts each segment to the real voice with
   Cartesia's voice changer, keeping the timing (lip-sync).
5. **Clean-up:** `python3 show/tools/clean_voice.py OUTPREFIX_dialogue.wav OUTPREFIX_clean.wav`. This runs WPE de-reverb,
   RNNoise (`models/bd.rnnn`), gentle spectral denoise, de-click, EQ and de-ess. Do not add a gate: it swallowed the
   "Cl" in "Claude".
6. **Edit:** copy `show/tools/trailer_plan.json`, then `python3 show/tools/assemble.py PLAN.json out.mp4`. That gives
   1080×1920 upscale, word-timed captions (cyan key words), headline tags, name tags, logo slam, end card, music
   bed (`music.py`, original) with side-chain ducking.
7. **Deliver:** `python3 show/tools/finalize.py out.mp4 show/final/NAME.mp4`. That sets -14 LUFS and encodes CRF 20.
   Check frames and transcribe the final audio, then commit and push.

## Don't
- Don't use MoneyPrinterTurbo's bundled songs: their copyright is unclear. Use `music.py` / `sting.py`.
- Don't fit clean Cartesia takes to the lips. Tested: they land about 0.4 s off. The owner chose the voice-swap route (A).
- Don't put readable text inside generated video. All text goes in as overlays in `assemble.py`.
