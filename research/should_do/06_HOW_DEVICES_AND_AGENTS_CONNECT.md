# How devices and agents actually "connect and talk" through emem

Snapshot: 2026-09-29. Evidence paths are relative to the emem repo.

## The precise mechanism, in three sentences

Two parties that never shared a database or a model, and that do not trust each other, still
agree on *which* evidence they mean:

1. They compute the **same place name** deterministically (`cell64`).
2. They exchange a **name derived from the evidence bytes** (`fact_cid`).
3. Each checks, **offline**, a signature from the responder's public key.

> "No peer is trusted to be honest, only to be checkable." (`docs/federation.md:95-96`)

This is the "devices talk" story. What travels is a *checkable reference*, not a file and not
a sentence.

## Two kinds of agreement: keep them separate on the poster

| question | mechanism | strength |
|---|---|---|
| "Did you send me the bytes you named?" | `fact_cid` = BLAKE3 of the served bytes | cryptographic, byte-identical |
| "Are we talking about the same place/thing?" | `cell64` (deterministic); `emem:entity:` (shared name via attested aliases) | deterministic address / social anchor |
| "Did two independent sensors see the same thing?" | not the CID. Both write to the same `(cell, band, tslot)` key; `/v1/memory_contradictions` scores the disagreement | **measured disagreement, never averaged away** |

**Why the third row matters:** `signer` and `signed_at` are inside the hash. So two devices that
each observe 915.07 m mint **different** CIDs. We saw this live. The CID does not make
independent observations converge. It makes each one *re-servable and re-checkable by anyone*.

- `docs/federation.md:39-43` overstates this point. Do not copy its wording.

## What works today (SHIPPED)

| capability | evidence | how to show it |
|---|---|---|
| Handoff between two robots from different vendors: different phrasing, one entity, offline `VALID`; **3 lines, 206 characters**; no shared backend | `examples/fleet-memory/README.md:16-47` (run 2026-07-13) | `python3 examples/fleet-memory/fleet_memory.py` |
| Air-gapped node `emem-airgap`: a scratch image with no networking crate, for amd64 and arm64, that signs custody records | `crates/emem-airgap/README.md:1-60`; decoder image 1.9 MB | `crates/emem-airgap/quickstart.sh` (docker only) |
| OS-trace sidecar `emem-encode`: tracefs and thermal data become a signed `emem.os_trace.v1`; the verifier has 16 named rejects; a one-event edit gives `chain_broken seq 2` | `crates/emem-airgap/README.md:135-157`; `docs/plans/encoder-substrates.md:88-110` | `/v1/trace_verify` |
| Satellite downlink walkthrough: `orbital.satellite.v1`, 8 layers; a forged 4th fact is refused with `chain broken at seq 3` | `examples/satellite-downlink/README.md:1-31` | `cargo run -p emem-primitives --example satellite_downlink` (offline, deterministic) |
| Signing at the edge on a third-party detector: **0.167% of a 40 ms frame**, 399/399 verified | `docs/roadmap.md:94-97` | print the number |
| Federation phase 0: emem.dev and geo.qa witness each other's log heads every 15 min | `docs/federation.md:312-368` | `/v1/log/witnesses` |
| Agent surface: MCP with 18 core tools and 114 in total, plus REST; one install line | `README.md:68,434` | `claude mcp add --transport http emem https://emem.dev/mcp` |

## What is NOT working yet (do not draw it as shipped)

| capability | status | evidence |
|---|---|---|
| Hardware-attested device enrolment (Jetson, TPM, TDX, SEV-SNP) | **every enrolment is refused**; all anchors are provisional | `docs/robots.md:249-253`; `README.md:503` |
| Enrolled devices on emem.dev | **1**, a software-only Linux host; no public trace binds a fact yet | `plugins/emem/skills/emem-device-traces/SKILL.md` |
| Anything running in orbit | **nothing**. The satellite example is a simulation. "Encoders in orbit" in diagram 31 means the satellite *sensors*. | `docs/diagrams/31-*.svg` |
| Orin NX streaming | a simulation: fixed key and clocks, Sentinel-2 crops used as frames | `crates/emem-primitives/examples/orin_stream.rs:22-28` |
| Read federation, write sharding, quorum reads | **design** | `docs/federation.md:3`; `docs/roadmap.md:28` |
| Substrate profiles | 18 published, **1 active** (`earth.satellite.v0`) | `README.md:550` |
| ROS 2 client | does not exist (HTTP only) | `examples/fleet-memory/README.md:52-53` |
| Sleep-time refiner writing to a default responder | refused; unattested writes are blocked | `docs/sleep-agent.md:18-27` |

## Poster recommendation

- **Main panel:** agents connecting across *trust boundaries*. This means model ↔ model,
  session ↔ session and vendor ↔ vendor. It is shipped and measured.
- **Device and orbit:** a small side panel titled
  *"Same primitive, at the edge (simulated today)"*. Show:
  - the signing overhead of 0.167% of a 40 ms frame;
  - the forged-fact refusal (`chain broken at seq 3`);
  - the air-gap custody record.
  Label hardware attestation as **open work**.
- **Why not headline "encode in orbit":** two neighbouring posters (ESA Φ-lab's onboard VLMs;
  Tor Vergata's space–ground–cloud work) own real onboard results. We would lose that
  comparison. We win on the thing they do not have: **evidence that survives the handoff**.

## The agent skills: how an agent uses emem, step by step

Skills live in `plugins/emem/skills/`, 19 in total. These five make the poster's case:

| skill | what the agent does | why an agent "loves" it |
|---|---|---|
| `emem-long-horizon-memory` | `emem_memory_create` → the first call is refused and the refusal names the digest → the agent signs it and resends; later `emem_memory_view` / `str_replace` against the base `file_cid` | a checkpoint of tokens and CIDs that verifies after a context reset |
| `emem-multi-agent-handoff` | `/v1/memory_bundle` (≤256 facts) → one 38-character handle → the receiver resolves and runs `verify_note.py` (body MATCH, signature VALID) | the receiver never needs the sender's prompt, model or honesty |
| `emem-referential-drift` | `/v1/memory_token/resolve`, then `/v1/echo_verify` before stating a number | catches a wrong number before it is repeated (0.74 → `drift:"wrong"`, verified live) |
| `emem-field-tokens` | `/v1/band_raster` / `band_cube` → re-hash the `f32` grid → `/v1/raster/resolve {spot_check}` | the model receives *a field*, not a sentence about a field |
| `emem-verify-before-publish` | `/v1/guard/verdict` on the draft → `PROV_SIG`, `PROV_BYTES`, `PROV_DRIFT`, `PROV_VALUE`, `CLAIM_UNGROUNDED` | an allow/deny gate before a claim leaves the agent. Known gap: the band is not yet matched to the sentence |
