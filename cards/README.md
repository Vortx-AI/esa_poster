# emem visiting cards

Two personalisations of the approved encode/decode design. The small `em` encoder on the satellite sends the same globe token to three distinct `em` decoders. Contact details and headlines are typeset independently of the illustrations.

## Print files

- [Avijeet Singh](output/emem-card-avijeet-singh.pdf) - avijeet@vortx.ai
- [Jaya](output/emem-card-jaya.pdf) - jaya@vortx.ai
- [Side-by-side preview](output/emem-cards-preview.png)

Each PDF has two pages: front first, reverse second. Both are upright in the same orientation. The reverse is identical for both people.

| Property | Value |
|---|---|
| Finished card | 85 x 55 mm, landscape |
| Bleed | 3 mm on every edge |
| PDF media size | 91 x 61 mm |
| TrimBox | 3 mm inset from every media edge |
| Text | Live vector text with embedded IBM Plex Sans fonts |
| Smallest contact text | 8.5 pt |
| Artwork | More than 300 ppi at placed size |
| Colour | RGB master for printer-managed conversion |

Print at 100%, with no fit-to-page scaling. The printer should impose the two pages for duplex alignment using the TrimBox. Crop marks are omitted so they cannot enter the bleed. The globe is illustrative brand artwork, not a scientific map. For a press requiring CMYK or PDF/X, convert using that printer's paper/press profile; these masters do not claim PDF/X certification. A plain white matte stock preserves the intended background.

## Edit and rebuild

Change names or emails in `content.json`; copy is limited to the wording already present in the user's approved reference. Reuse the existing repository's IBM Plex Sans fonts under `poster/fonts/plex-full/`.

```bash
python -m pip install -r cards/requirements.txt
python cards/build_cards.py
```

The build uses the committed artwork and makes no network calls. It checks page dimensions, exact text, embedded text fonts, text margins, minimum type size and image resolution; then renders the trimmed cards to PNG. `output/preflight.json` records the final checks and PDF hashes.

## Design sources

The artwork was refined with the built-in image-generation tool from the user's latest encode/decode card references. The final generation prompts are in `art-direction.md`. The generated artwork is committed as fixed input; names, email addresses, headline copy and website remain editable vector text. No third-party AI logos or extra promotional copy were added.
