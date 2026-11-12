# ARKS Sharks — show pack

AI talk show with Ahmed and Kamran in a Dubai studio. Vertical 9:16, 1080×1920, 24 fps, mixed to about -14 LUFS.

## Deliverables
| File | What it is |
|---|---|
| `trailer/ARKS_Sharks_trailer_9x16.mp4` | Trailer, 55 s: hook, logo slam, intro, rapid-fire news, funny bit, sign-off, end card |
| `intro/ARKS_Sharks_intro_9x16.mp4` | Fixed episode opener, 9.7 s: holographic shark over the Burj Khalifa, into the studio, logo and sound logo |
| `brand/arks_sharks_logo_shadow.png` | Logo with a transparent background and a soft shadow (for overlays) |
| `brand/arks_sharks_logo_v1.jpg` | Original logo on black |
| `trailer_script.md`, `episode01_script.md` | Scripts with sources |

## How it was made
1. **Characters and set:** Seedream 5.0 (BytePlus ModelArk). Studio and keyframes are in `trailer/keyframes/`.
2. **Dialogue:** each line recorded in Ahmed's and Kamran's own Cartesia voices (`sonic-3`), in `trailer/audio/`.
3. **Animation:** Seedance 2.0 reference-to-video at 720p, using keyframe and character references plus the
   Cartesia lines as reference audio for lip-sync. Clips are in `trailer/clips/`; prompts are in `trailer/prompts/`.
4. **Voice swap:** Seedance re-voices the dialogue, so each speaker's segment was passed through Cartesia's voice changer
   back into the real Ahmed and Kamran voices. Timing is unchanged, so the lip-sync holds
   (`trailer/audio/voice_swapped/`, `tools/vc_shot.py`).
5. **Voice clean-up** (`tools/clean_voice.py`): the animation audio is de-reverbed and denoised before conversion, then
   each converted track gets WPE de-reverb, RNNoise (voice model), gentle spectral denoise, de-click, EQ (mud cut,
   presence, air), de-ess and light levelling. It was tuned so quiet consonants survive: an earlier, harder setting
   swallowed the "Cl" in "Claude". Cleaned tracks are in `trailer/audio/voice_cleaned/`.
6. **Edit:** `tools/assemble.py` with `tools/trailer_plan.json`. It upscales to 1080×1920, adds word-timed captions with cyan
   keywords, headline tags, name tags, the logo slam and an end card, then mixes dialogue, SFX and music with
   side-chain ducking to -14 LUFS.
7. **Music and sound logo:** composed in code (`tools/music.py`, `tools/sting.py`), original and license-free.
   MoneyPrinterTurbo's bundled tracks were not used because their source is unclear (its README says they come
   from YouTube videos).

Skills used: ModelArk, OpenMontage (Seedance prompting, short-form, cinematic, sound design), and MoneyPrinterTurbo
(caption style only).

## Fixes made during review
- Shot 5: the model morphed Kamran's T-shirt into a shirt and tie mid-line. That moment is covered by an Ahmed reaction
  cutaway (`s5b_ahmed_react.mp4`).
- The brand name is pronounced most clearly when Seedance voices it from the quoted dialogue, which then goes
  through the voice changer.
