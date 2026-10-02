# v13.3 release review — 2 October 2026

This review covers the issue #48 rewrite against its final tightening comment, the related editorial issues below, the rendered A0, and the generated companion pages. The original scientific measurements remain committed unchanged.

## Requirement coverage

| Issue | Resolution in this release |
|---|---|
| #48 | Retains the reading flow; leads with the complete observe–locate–record–handoff–resolve–check–continue mechanism. The human hero is “An Earth observation that survives an agent handoff.” Consolidates scope, moves research questions and detailed protocol material to methods, enlarges Berlin, groups token purposes, and prints three QR tasks. |
| #12 | Explicitly identifies the BLAKE3 input as the canonical record. The record/CID diagram and caption distinguish source pointers from source contents and batch attestation from raw-pixel signing. |
| #14 | Execution is a short reference-harness extension. Methods explicitly identify SAT-042 as a deterministic test harness with no spacecraft enrolled and state the value-digest gate's scope. |
| #20 | Berlin preserves native-grid sizes beside the products. Copy describes one lookup cell organising records, not a common native grid or automatic co-registration. |
| #23 | Actor/action copy carries the story: pass, resolve, check, recover, recompute and re-read. Each major mechanism states what the receiver can do with the cited record. |
| #24 | One plain-language hero appears above the technical explanation. The accepted programme title is retained separately. |
| #28 | The retained evidence-object diagram shows the exact record, its fields, source pointers, canonical bytes, CID and external batch attestation. The adjoining copy states what the token carries. |
| #30 | The complementary-layers panel retains STAC, openEO, PROV/C2PA, RAG and GeoGuard, with references in methods. |
| #37 | No internal version, defect scorecard, strike-through title or development chronology remains on the printed face. Build history remains in the repository. |
| #38 | The conclusion describes an addressable observation that another agent can recover and check. The bounded scientific scope is stated in the checks panel and experiment captions. |

## Scientific wording review

The displayed fact token contains a cell and record CID; product and observation time are fields in the record. “Lookup identity” and “content address” have distinct jobs. The CID is not described as a hash of raw imagery. The observation record names source files and read coordinates; the illustrated source has no embedded source-content hash. A batch attestation covers record addresses. Returning to the source tests the recorded measurement; it does not certify physical or semantic truth.

The positive system narrative does not broaden the evidence: the two-process handoff is identified as a program experiment, not a cross-host chat; tested client paths retain their counts and date; ChatGPT remains a publisher listing; execution remains a reference harness. Cross-host handoff (#43), wider integrations and new experiment work remain open.

## Validation

- `python poster/build_v13.py`: **17/17 PASS**, one A0 page, 649 running words, 662 tokens, 54 printed claim rows, 390 evidence rows rechecked and 402 figure numbers checked. All three printed QR codes decode from the PDF.
- Visual inspection: full poster preview and enlarged centre detail; phone landing and methods views. No clipping or overlap observed.
- Publication compression: the 300 dpi PNG is losslessly optimised with pyoxipng 9.1.1, level 3. Decoded RGB pixel hashes, dimensions and DPI match the original render exactly; the PDF is unchanged.
- Deterministic R1 rerun: verdicts and all non-timing results match the committed evidence. Original measurement files were retained; environment-specific rerun timing is not substituted into the poster.
- `python poster/build_site.py`: successful generation of the six routes and subset fonts.
- `node tools/site/test_site.mjs`: local layout, current hero and three primary CTAs, offline demo verdicts, no-JavaScript summary, methods/record content, zero writes to emem.dev, and all six QR payloads pass. **Full suite exits 1**: twelve live checks fail because external emem.dev/source fetches are unavailable in this workspace. The page reports “not checked”; no live success is inferred. Raw results and screenshots are in `docs/assets/screens/`.
- Python compilation, JavaScript syntax and source whitespace checks pass. Generated SVG whitespace is excluded from the whitespace check.

The release manifest records SHA-256 hashes of the PDF, previews, build report and browser results. The earlier signed board track is clearly archived at commit `e66c3ba`; it does not attest this revision.
