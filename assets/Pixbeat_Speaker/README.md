# Pixbeat speaker asset

Reference-built speaker model and standalone browser review, 30 October 2026.

**Repository upload status: incomplete.** This README is present, but GitHub rejected the binary upload commit. The GLB and viewer/source/reference package are not yet in this folder. The instructions and inventory below describe the prepared package, not files already available here. Use the private review link to inspect the existing model.

## View and download

Private owner-only review: https://files.instinct.com/4fn6vkgkckz2-your-speaker-in-3d

The link remains private. Public repository readers are not promised access. For local review, use the viewer below. The latest reusable model is `speaker-reference-v2.glb` (glTF 2.0 binary).

## Run the viewer

Requires Node.js 18 or newer.

```sh
npm install
npm run dev
```

Open the local address printed by Vite. `npm run build` creates a local production build; `npm run preview` previews it. This folder does not deploy a site. The viewer uses React and Canvas 2D, with drag rotation, three-axis controls, front/back/left/bottom presets, zoom and reset. `ui.tsx` contains standalone layout components. The download and viewer use the same generated mesh.

## Rebuild the model

```sh
python -m pip install -r requirements.txt
python generate_speaker.py
```

Python, Pillow and the DejaVu Sans Condensed TrueType font are required. The script currently expects `/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf`; adjust this path for your system. It regenerates the GLB, `model.json` and `modelDownload.ts`. The latter embeds the GLB for the viewer download. Vite reports a large JavaScript chunk because this review includes both mesh data and the base64 download; it is a review implementation, not an optimized room renderer.

## Model scope

- Body approximately 4.5 x 2.5 x 2.5 inches. Height excludes the fixed raised strap.
- Black shell, metallic-coloured trim, slatted grille, dial/knob, three buttons, strap/mounts, approximate ports, rear pattern, feet and blank underside label.
- Dial labels 00, 10 through 100 with radial ticks; previous/next marks and central power/M/play-pause-like group from close-ups.
- About 17,096 vertices and 22,000 triangles. GLB about 472 KB.

This is a stylised photo-reference model, not a scan or precision replica. Surface finishes, small strokes, ports, rear perforations and strap curvature are approximate. The marks appear dark on the surface, not physically recessed engraving. The central glyph is an approximation of visible strokes, not a claim about hardware function.

The model does not use photo textures. No reflected person or phone is baked into it. The original reflective dial close-up is intentionally not published. The underside reference has its certification label masked; published images have metadata stripped. Other reference files record the supplied shape/dimensions and button marks. `logo-reference.jpg` is source material only and is not integrated into the model.

## Interaction concept, not implemented

Speaker pickup/putdown and music remain future work. The proposed volume choices are Low / Medium / High, not continuous control based on the dial numerals. No music files, music licences, logo integration, table scene, room implementation or production deployment are included. The Edith Finch direction is parked. The planned immersive portfolio is laptop-only; this asset review is not a tested full-room performance target.

## Files

- `speaker-reference-v2.glb`: latest reusable model.
- `generate_speaker.py`, `requirements.txt`: procedural geometry/export source.
- `model.json`, `modelDownload.ts`: generated viewer data/download.
- `App.tsx`, `ui.tsx`, `main.tsx`, `style.css`, `index.html`, `package.json`, `package-lock.json`: standalone review source and dependencies.
- `model-preview.png`: model illustration.
- `reference-*.jpg`, `logo-reference.jpg`: source references, with the exclusions above.

Earlier superseded GLB versions, build output and dependency folders are not included. This folder contains the current asset work, not a replacement for the existing portfolio.
