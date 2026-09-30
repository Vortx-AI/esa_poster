# Satellite execution traces in emem: what is true

Audit for the ESA/BIFOLD poster (Poster Session 1, 19 Oct 2026). emem code at `04b40c56c97d1c2809ca05003dc2b7d6de450758` (github.com/Vortx-AI/emem, main). Live checks against https://emem.dev on 2026-09-30 between 2026-09-30T19:03:50Z and 2026-09-30T19:05:21Z UTC. Raw evidence: `trace_live_state.json`, `sat042_run_stdout.txt`, `emem_trace_tests.txt`.

## 1. Verdict

"Satellite execution traces" is **true as an implemented and tested protocol**, shown end to end in a deterministic reference spacecraft run (SAT-042). It is **not true as a live capability** on emem.dev.

- No satellite is enrolled. The live roster has 1 device: a Linux host (`generic.linux-host`, profile `host.counters.v1`, assurance `operator_endorsed`).
- `orbital.satellite.v1` is `candidate`. In code, candidate means "the ingest path is not open yet" (`crates/emem-core/src/substrates.rs:299-305`).
- All 17 hardware platforms are `candidate`. Every hardware trust anchor is provisional. The only effective anchor is `operator.vortx.v1` on `generic.linux-host`.
- No live band carries the `attested_execution` provenance class (0 of 43 bands, bands_cid `mesoyti3qcs22pftcq27ljwcf3ifktnkqid4euqxyskhea5rpgra`). A recall filtered to `attested_execution` returns 0 facts. No fact in the live memory is attributed to a device trace.
- What is live is the verifier and the resolver. The public trace token resolves, re-verifies to `admit`, and a one-field edit is rejected.

The phrase can go in the title only in a qualified form (Section 7). The bare phrase implies satellites write to emem today, and a reviewer can refute that with one GET.

## 2. What "satellite execution traces" means in code

A device writes under a substrate profile. For every device-borne profile, admission is `os_trace_required`. The write must carry an `emem.os_trace.v1` record: device identity, a hash-chained list of OS trace segments (one per required layer), the digests of the outputs the device emitted, and an ed25519 device signature over all of it (`crates/emem-trace/src/schema.rs`).

`orbital.satellite.v1` (`crates/emem-core/data/substrates-v0.json:53`) requires 8 layers: syscall, scheduler, memory, sensor_bus, signal, energy, thermal, storage. Its provenance class is `attested_execution`. `earth.satellite.v0` (line 7) is the only `active` profile. It is admitted by recomputability from free public archives and serves as the drift anchor.

The satellite here is a manufacturer's own constellation writing its own data (CHANGELOG 1.3.0, lines 894-896). ESA or USGS missions are not tracing anything into emem. Public-archive EO enters through `earth.satellite.v0`, with no device trace.

## 3. Implemented and tested

| Mechanism | Where | Evidence |
|---|---|---|
| Trace schema, canonical CBOR, BLAKE3 CIDs, domain-separated signing preimage | `crates/emem-trace/src/schema.rs` | unit + round-trip tests pass |
| Verifier collects every failure: profile mismatch, missing layer, chain broken, clock non-monotonic, output unbound, signature invalid | `crates/emem-trace/src/verify.rs:164-321` (reasons at 177, 205, 235, 239, 276, 300) | `rewritten_segment_is_caught_at_every_escalation`, `dropped_layer_is_missing_coverage`, `unbound_payload_is_rejected_even_with_a_sound_trace`, `wrong_key_cannot_speak_for_the_device` |
| Archive substrate never admits device output | verify.rs, trace_gate.rs | `archive_substrate_never_admits_device_output`, `enrollment_refuses_the_archive_profile` |
| Enrolment evidence (RFC 9334 shape) and its verifier; provisional anchors admit nothing | `crates/emem-trace/src/enroll.rs` | `shipped_platforms_admit_nothing_because_anchors_are_provisional`, `attested_enrollment_is_refused_while_anchors_are_provisional` |
| Drift-anchor score: 0.5 at 3 sigma, 0.75 at 9 sigma; verdicts consistent / tension / contradicted | `crates/emem-trace/src/drift.rs:50-56` | `pinned_points`, `verdict_thresholds` |
| `emem:trace:` and `emem:attestation:` tokens | `crates/emem-trace/src/token.rs` | `round_trip`, `rejects_malformed` |
| Write-path gate: enrolled key must present a binding trace; every fact's payload digest must be in the trace outputs; trace encodings must be registered and able to capture the claimed layer; per-device stream must chain | `crates/emem-storage/src/trace_gate.rs:392` (`check`), `:539` (`persist`); `crates/emem-storage/src/lib.rs:913` (`put_attestation_gated`) | `enrolled_device_needs_a_binding_trace`, `trace_naming_an_unregistered_encoding_is_refused`, `device_trace_stream_must_chain`, `derivative_facts_are_not_a_side_door` |
| Committed conformance vectors (admit, chain broken, output unbound, archive refused) | `spec/test_vectors/os_trace/` | `committed_vectors_replay` |

Test counts on this machine (aarch64-apple-darwin, rustc 1.98.1):

- `cargo test -p emem-trace --locked` (2026-09-30T19:02:08Z to 2026-09-30T19:02:42Z UTC): **22 passed, 0 failed, 1 ignored** (a release-only timing test).
- `cargo test -p emem-storage --lib` filtered to the gate, enrolment and fact-plane tests (2026-09-30T19:15:42Z to 2026-09-30T19:17:15Z UTC): **23 passed, 0 failed**. 38 other emem-storage lib tests were filtered out.

## 4. Live on emem.dev (2026-09-30, UTC)

| Check | Time | Result |
|---|---|---|
| `GET /v1/devices` | 2026-09-30T19:03:50Z | 1 device; key `r6c3xpbetvl7soyf3eani7knij74gth6bjizqjkrdfyl2ycqcdna`, `generic.linux-host`, `host.counters.v1`, `operator_endorsed`, 1 trace; listing is opt-in |
| `GET /v1/device_platforms` | 2026-09-30T19:03:51Z | manifest_cid `gi6lw3ekbpd7soeperslxjgeljl6c3h7q6ngdcykfp2yucpcbsya`; 17 platforms, all `candidate`; no hardware anchor is effective |
| Satellite-serving platforms | same | `tpm2.host`, `intel.tdx`, `amd.sev-snp`, `arm.psa-l2`, `arm.psa-l3`, `caliptra.rot`; none has a non-provisional anchor |
| `GET /v1/trace_encodings` | 2026-09-30T19:03:53Z | manifest_cid `fmyxah55fjr2vfzmktjdghutg37g2qdt2zmu7ub2dtgtpn64otga`; 8 encodings; only `ros2.bag.v2` captures sensor_bus or signal, and no satellite-serving platform recognises it |
| `GET /v1/substrates` | 2026-09-30T19:03:54Z | manifest_cid `oqaxnlorhlsy72pm4wnkjupr2ul252bz3snjjzmgdof6jmse2dqa`; 18 profiles; `earth.satellite.v0` is the only `active` one; `orbital.satellite.v1` is `candidate`, `os_trace_required`, `attested_execution` |
| `GET /v1/bands` | 2026-09-30T19:04:51Z | bands_cid `mesoyti3qcs22pftcq27ljwcf3ifktnkqid4euqxyskhea5rpgra`; 43 bands, 1792 dims; classes model_output 23, deterministic_index 7, direct_sensor 6, human_curated 5, unclassified 2; 0 with `attested_execution` |
| `POST /v1/recall` Nile Delta, `indices.ndvi`, provenance `attested_execution` | 2026-09-30T19:05:03Z | HTTP 400: the filter excludes every requested band |
| `POST /v1/recall` Nile Delta, provenance `attested_execution`, any band | 2026-09-30T19:05:21Z | HTTP 200, 0 facts |
| `POST /v1/trace_resolve` `emem:trace:mxyer5c2oxn4ud3xqbtnaxcxhdv4kkxiu67q32inbwxgpa7r3s6a` | 2026-09-30T19:04:20Z | resolved; trace_cid `mxyer5c2oxn4ud3xqbtnaxcxhdv4kkxiu67q32inbwxgpa7r3s6a`; `host.counters.v1` on `Debian GNU/Linux 13 (trixie)`, kernel `6.17.0-1017-aws`; 4 `linux.ftrace.v1` segments (scheduler, memory, storage, network); 0 outputs |
| `POST /v1/trace_verify` original | 2026-09-30T19:04:34Z | `admit`, no reasons |
| same, segment 1 `event_count` + 1 | 2026-09-30T19:04:35Z | `reject`: `chain_broken` at seq 2 |
| same, `window_end_ns` + 1 | 2026-09-30T19:04:37Z | `reject`: `signature_invalid` |
| original, verified against `orbital.satellite.v1` | 2026-09-30T19:04:38Z | `reject`: `profile_mismatch` plus 5 missing layers (syscall, sensor_bus, signal, energy, thermal) |
| original, with a claimed payload digest not in the outputs | 2026-09-30T19:04:40Z | `reject`: `output_unbound` |

The live public trace is a Linux host's counters. It is not a satellite trace. It shows the verifier works on a real device record, and that the same record cannot pass as a satellite.

## 5. Not live today

- A satellite enrolled on emem.dev, or any fact written under `orbital.satellite.v1`.
- Hardware-attested enrolment for any platform. Every hardware anchor is provisional, and the code refuses attested enrolment by name (CHANGELOG 1.4.0, lines 749-753).
- A trace encoding that a satellite-serving platform recognises for the sensor_bus and signal layers. A real spacecraft trace could not meet `orbital.satellite.v1` against today's registries, even with operator enrolment.
- A band whose facts carry `attested_execution`. Provenance class is assigned per band (`provenance_for_band`, `crates/emem-api-rest/src/lib.rs:37955`), and no band has that class. No read path uses `trace_for_fact` to label a fact as device-attested.

## 6. SAT-042 reference run

How it was run. `cargo run -p emem-primitives --example satellite_downlink` was not run as such. emem-primitives pulls 497 crates (lance, datafusion, two arrow versions, ort, tokenizers). The example never calls them, and they do not fit in this machine's free disk (3.6 GB when checked). Instead the example source (sha256 `073469b6…4529`) was compiled in a local harness crate. The harness uses the same emem crates at the same commit, with a lock that is a strict subset of emem's Cargo.lock (no version changes). One import line differs: `emem_primitives::memory_bundle` is compiled from the same source file via `#[path]`. `orin_stream` compiled unmodified. Both ran twice with byte-identical stdout, exit 0, empty stderr (2026-09-30T19:14:15Z to 2026-09-30T19:14:16Z UTC).

Key outputs (verbatim, from `sat042_run_stdout.txt`):

1. Enrolment: spacecraft key `mwndc7zcesxqvw7bgxmbff3trktrynx3edprmwtzodv6qt45vqvq` under `orbital.satellite.v1`, 8 required layers.
2. Write without a trace: refused. "writes require the device's OS execution trace and none was presented".
3. One unemitted fact added to a sound batch: refused. Payload digest `cyzwaknc3wznnmpjc52er4sy4kxqkeq6ysflubbmahrxassy4jlq` "is not bound in the trace's emitted outputs".
4. Admitted: 3 facts under one verified trace.
   - `emem:fact:defi.zb55e.natI.tUpu:ol4ugzp4rmkc7nodxgfnm3bucamdbell6anysvt5syqlwhmzjtia`
   - `emem:fact:defi.zb55e.nadU.tUra:wndl3zwt4b27q2ufzpwc6oxwqx7a2t3ysd3evwzjnewvz5wphefa`
   - `emem:fact:defi.zb55e.mUgI.tUsE:asue5jcmxpwiur3ajfj7xil5u7uz7bvh4rrxbcqswkvjeop2lbhq`
   - `emem:trace:3arfrney6ieeugzekzqfufwoayvqj3edhc6fbwaqzhydxn2hbogq`
   - `emem:bundle:sfxaann374s7omyhfhbavl3qne`
5. Drift-anchor scores against anchor NDVI 0.6402 ± 0.02: device 0.6431 scores 0.05, consistent; device 0.6512 scores 0.15, consistent; device 0.2103 scores 0.88, contradicted.
6. Tamper: segment 2 rewritten after signing. Verifier: "reject: chain broken at seq 3".

What the run is and is not. It is a deterministic simulation that exercises the real gate and verifier code. The enrolment is operator-asserted (`gate.enroll`, `satellite_downlink.rs:80`), not hardware-attested. Segment log digests are BLAKE3 hashes of fixed strings (`segment()`, line 257), not captured kernel logs. The drift anchor is a fixed pair `(0.6402, 0.02)` (line 198), not a live recomputation from Sentinel-2. The tamper edits `segments[2].log_digest` (line 215).

`orin_stream` (Jetson Orin NX, `robot.fleet.v1`) shows the same boundary. Attested enrolment is refused because `nvidia.jetson-orin` has no effective anchor. It then enrols operator-asserted, chains 4 traced frames, refuses a dropped frame, and re-verifies all 4 tokens. Its own strings contain em dashes, so do not paste that output onto the board.

## 7. Findings the board depends on

1. **Ungated write path.** `POST /v1/attest_cbor` (`crates/emem-api-rest/src/lib.rs:20643`, call at `:20658`) calls `Storage::put_attestation`, not `put_attestation_gated`. `put_attestation` admits an enrolled key "by enrolment" without a trace (`crates/emem-storage/src/lib.rs:1005-1020`). `/v1/attest` (`:20519`) and `/v1/attest_traced` (`:20570`) use the gated path. A local probe with the SAT-042 key confirms this at storage level. The gated call refused the untraced write. The ungated call admitted it as fact `ol4ugzp4…` (`sat042_run_stdout.txt`, gate_path_probe section). This does not change today's live state, because no device is enrolled for writes that take an address. It does mean "every enrolled-device write carries a verified trace" is not yet an invariant of the code. Do not print that sentence until the CBOR route goes through the gate. This should be filed as an emem issue.
2. **A signature is not a measurement.** The code says so itself. The `attested_execution` caution in `crates/emem-core/src/bands.rs:227` reads "A genuine but miscalibrated or spoofed sensor still produces a signed trace". It tells readers to corroborate against the drift anchor. This matches esa_poster issue #7 (separate derivation integrity from semantic correctness), and panel c of the figure shows it.
3. **The live public trace is not a satellite.** Any board text that shows `emem:trace:mxyer5c2…` must call it a Linux host trace.

## 8. Title

Current: "EMEM: A Content-Addressed, Verifiable Earth-Memory Protocol for AI Agents ~~over Foundation-Model Embeddings~~".

Options that stay true:

1. **"EMEM: A Content-Addressed, Verifiable Earth-Memory Protocol for AI Agents, with Signed Execution Traces"** (recommended). True live: `/v1/trace_verify` and `/v1/trace_resolve` work on a real signed device trace today.
2. **"EMEM: A Content-Addressed, Verifiable Earth-Memory Protocol for AI Agents, with Execution Traces Proven on a Reference Satellite Pass"**. True as implemented and tested. "Reference" names the SAT-042 simulation.
3. **"EMEM: A Content-Addressed, Verifiable Earth-Memory Protocol for AI Agents and Trace-Gated Device Data"**. True in code and tests (the gate and its tests). Weaker live: the only live device trace carries no outputs, and finding 1 must be fixed first.

Do not use: "Satellite Execution Traces" unqualified, "satellites that write to emem", or "hardware-attested".

## 9. Scope statements a poster can print

Each is true against code and live state on 2026-09-30. The last one describes the profile rule. Keep it to that wording while finding 1 is open.


- The trace verifier is live. emem.dev re-checks any signed execution trace and names each broken link.
- In the SAT-042 reference pass, a write with no trace and a fact the trace never emitted were both refused.
- Rewrite one log segment and the chain breaks at the next sequence number. The verifier says where.
- A signed trace proves what ran, not that the sensor was right. A drift anchor scores the claim.
- SAT-042 is a deterministic reference spacecraft: fixed key, clocks, capture digests and anchor value.
- Public Earth observation enters by recomputation from open archives. Device profiles require a signed execution trace.

## 10. Figure

`sat042_panel.png` (300 dpi) and `sat042_panel.svg` (glyphs as paths). Every value is parsed from the captured run stdout (`fig_sat042.py`). The two fixed inputs, the anchor sigma and the tampered segment index, come from the example source (lines 198 and 215), and the footer states that the values are deterministic. Palette and IBM Plex fonts match poster v11. The figure contains no em dashes or en dashes.
