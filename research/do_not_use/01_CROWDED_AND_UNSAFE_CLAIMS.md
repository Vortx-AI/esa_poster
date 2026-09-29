# What we should NOT put in the poster

## 1. Do not claim "content addressing" as the invention

Generic content-derived identifiers are well established:
- IPFS CIDs are cryptographic content addresses.
- Nix supports content-addressed store objects and build outputs.

Sources:
- https://docs.ipfs.tech/concepts/content-addressing/
- https://releases.nixos.org/nix/nix-2.34.1/manual/store/store-object/content-address.html

**Bad:** "emem invents content-addressing for data."

**Better:** "emem applies content-derived identity to typed physical observations and makes those identities usable as cross-agent, independently verifiable world-state."

## 2. Do not claim "persistent memory for agents" as the invention

Persistent cross-session agent memory is an established category (Mem0, LangChain/LangGraph ecosystem and others).

Source:
- https://mem0.ai/
- https://www.langchain.com/blog/how-to-give-your-agent-memory

**Bad:** "Agents can remember across sessions."

**Better:** "A later session can resume from the same signed physical-world observation rather than from a model-generated summary of it."

The distinction is **what is remembered and how its identity is checked**.

## 3. Do not claim "provenance" as the invention

W3C PROV already defines interoperable concepts for entities, activities, agents, derivation, versioning and reproducibility.

Source:
- https://www.w3.org/TR/prov-overview/

Several posters at the event explicitly use provenance / auditability framing.

**Bad:** "emem adds provenance to EO."

**Better:** show that the **identifier itself binds the observation bytes**, while the receipt binds the served fact ids/query context and provenance travels with the observation.

## 4. Do not compete with STAC on discovery/cataloguing

STAC is already the de facto common structure for describing and discovering spatiotemporal assets.

Source:
- https://stacspec.org/en/

**Bad:** "One universal way for AI to find EO data."

**Better:** "After an observation is selected/derived, give the resulting physical-world state a stable, checkable identity that can move across agents."

STAC can be an upstream source, not an enemy.

## 5. Do not compete with COG on moving fewer bytes

COGs already support partial HTTP range access to raster imagery.

Source:
- https://cogeo.org/

**Bad:** "No need to move huge satellite files."

That wording implies emem invented efficient partial data movement.

**Better:** "The agent handoff can carry the address/derivation instead of re-serialising the evidence as prose; heavy artifacts remain separately retrievable/recomputable."

## 6. Do not claim lazy EO computation / build graphs are new by themselves

Google Earth Engine already serializes expression DAGs and executes lazily at result request time. Nix/Bazel-style systems make computation/build graphs and caching familiar systems ideas.

Source:
- https://developers.google.com/earth-engine/guides/deferred_execution
- https://developers.google.com/earth-engine/reference/rest/v1/Expression

**Bad:** "The first computation graph for Earth."

**Better:** "A content-addressed build-graph interpretation where the *outputs become portable signed world-state across agent trust boundaries*."

## 7. Avoid generic phrases crowded at the event

Do not headline:
- "Agentic geospatial intelligence"
- "AI assistant for Earth observation"
- "End-to-end EO agent"
- "Multi-agent EO framework"
- "Trustworthy EO AI"
- "EO data to decisions"
- "Semantic search for satellite imagery"
- "Provenance-first AI"
- "On-demand datacubes"

All are either present verbatim or very close to published poster titles:
https://agentic-eo.berlin/programme/posters/

## 8. Avoid "same truth"

Use:
- same signed bytes;
- same cited observation;
- same address;
- independently checkable evidence.

Do not use:
- "same truth";
- "guaranteed truth";
- "cryptographically true";
- "no hallucinations";
- "no drift" without qualification.

Signatures/content hashes prove integrity/co-reference, not objective accuracy.

## 9. Avoid overstating entity tokens

The strongest byte-identity guarantee is for `emem:fact:`.

Do not visually imply every token family means "same bytes everywhere." `emem:entity:` is a shared name/identity anchor with weaker semantics; `emem:cell:` is an address; field tokens bind derivations.

The poster should either:
- focus deeply on `emem:fact:`; or
- clearly annotate different token strengths.

## 10. Avoid putting roadmap claims in the shipped-mechanism diagram

Do not visually present as already solved:
- full numeric causal decomposition of change;
- general multi-hop `prove(goal)` planning;
- machine-checked formal proof of all protocol properties;
- universal artifact-typed observations;
- universal federation/read routing if not shipped in the version demonstrated.

Open work is valuable—label it as open work.

## 11. Avoid fake tokens and decorative cryptography

No:
- random hex strings;
- fake signatures;
- lock icons without mechanism;
- blockchain-looking networks;
- "verified" checkmarks unsupported by a real example.

Use one real observation and its real token.

## 12. Avoid robots, holograms and space wallpaper

These are instant "AI poster" tells:
- cute robots around a table;
- blue holographic Earth;
- giant satellite with meaningless data beams;
- neon agent icons;
- glowing cubes whose layers have no protocol meaning.

If a satellite appears, it should identify the source scene or onboard/airgap mechanism.

## 13. Avoid feature grids

Rows of:
"Observe / Tokenise / Share / Reason / Verify"
look like SaaS marketing and hide the invention.

Replace them with:
- one invariant;
- one handoff experiment;
- one long-horizon continuity experiment;
- one field/cube example;
- one honest limits box.

## 14. Avoid startup CTA language

No:
- "Book a demo"
- "Build with us"
- "Revolutionise your workflow"
- "The future of EO"
- "Game-changing intelligence"

Use:
- "Reproduce this"
- "Resolve this token"
- "Re-hash these bytes"
- "Verify this receipt"
- "Source / DOI"

Scientists should leave able to test the claim.
