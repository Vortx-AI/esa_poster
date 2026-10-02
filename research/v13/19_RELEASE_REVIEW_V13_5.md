# v13.5 release review

2 October 2026. The released poster restores community access and useful earlier demonstrations while preserving the central scientific experiments.

- PDF: one ISO A0 portrait page, 841 × 1189 mm nominal (PDF reports 840.99 × 1188.89 mm); inspected through both Chromium and Poppler renders.
- All 17 poster gates pass. No text below 14 pt; primary community names are 28 pt, actions 18–22 pt. Content clears the footer by 2.5 mm.
- 669 running words; 61 printed claim rows; 406 evidence rows rechecked.
- TRY IT, INSPECT and CONNECT & REPRODUCE QR codes decode to their expected payloads from the print render.
- Seven routes at both 390 px and 1440 px: 14 passing local layout checks, no page errors, no broken local images. External calls were blocked deliberately. The clipboard button preserved the exact example token at both widths; the link to methods opened correctly.
- Four saved reasoning-state hashes freshly reproduced; nine offline NDVI proof-bundle checks passed. The archived bundle groups eight records in a 38-character handle. The upstream 20-test Python result remains its original v13.4 run.
- ChatGPT's primary listing identifies emem and Vortx.ai. Dify and three workflow templates, GitHub MCP, MuleSoft Exchange and ClawHub returned 200. Connected ChatGPT resolve attempts returned connector errors and are not counted as successful host runs.
- PNG print proof: 9,933 × 14,042 pixels, 300 dpi. Lossless compression preserves decoded RGB and DPI exactly; 14,076,581 bytes became 11,421,748 bytes.
- PDF SHA-256: `33edb1f92b84db1786a2afb3729a3961e02a6788ee48b52c7af3a1a3df4de4e1`.

Evidence: `evidence/community/site_review.json`, `recovery_checks.json`, `listing_checks.json`, `chatgpt_plugin_check.json`; artifact manifest: `poster/release_v13.5.json`. The direct-listing archive retains selected identity fields and the full-response hashes rather than copying the entire provider pages.

The prior live-endpoint browser failures remain in their original report. Rust tests were not rerun. An address or signature does not establish source accuracy, correct reasoning, independent operation or future availability. The old signed poster track remains explicitly archived.

The full-width community band and the phone setup page were visually reviewed. The central experiments, formal equations, vector provenance and temporal example retain their scientific scope. Earlier seasonal, forest-screen and SAT-042 figures are copied unchanged into the methods gallery and labelled with their dates and limitations.

The branch is published through a pull request, preserving the reviewed Git tree. The existing Pages workflow deploys the generated static files; a final live check compares the PDF and public page bytes to this manifest and the committed files.
