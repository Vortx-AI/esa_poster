# Reproduce it: checks we ran ourselves against emem.dev

Run on 2026-09-29 from a clean container. The client used **no emem code**, only the
reference `blake3` and `cbor2` Python packages. Every result below can be re-run.

```sh
pip install blake3 cbor2
python verify_fact.py <emem:fact:...>
```

`verify_fact.py` does four things:

1. Fetches `GET https://emem.dev/v1/facts/<fact_cid>` with `Accept: application/cbor`.
2. Re-derives the CID with `base32-nopad-lower(BLAKE3-256(body))`.
3. Checks that the token's cell matches the cell inside the fact.
4. Changes the value by 0.1, re-encodes, and shows that the name no longer matches.

## Exhibit A: a real upstream drift, caught by addressing

The same place (Bengaluru, cell `defi.zb493.xuqA.zcb5f`), the same band
(`copdem30m.elevation_mean`), and three tokens. All three re-hash to their names today.

| token fact_cid (first 8 chars) | value | signed_at | upstream source | derivation |
|---|---|---|---|---|
| `yqbolgeo…` | **918.0 m** | 2026-05-28 | `open_meteo` (Copernicus DEM 90 m via Open-Meteo) | `open_meteo_copdem90m@1` |
| `tdwp3aax…` | **915.07 m** | 2026-08-17 | `copernicus.dem.30m.aws` (COG tile `N12_00_E077_00`) | `copernicus_dem_30m_aws_pixel@1` |
| `jzxzmvom…` | **915.07 m** | 2026-09-28 | same COG tile | same |

Full tokens:

```
emem:fact:defi.zb493.xuqA.zcb5f:yqbolgeoycqkvj3zkxukb4bjw4odhpwvfzqo3fbgwf4spk45zala   (918.0, May)
emem:fact:defi.zb493.xuqA.zcb5f:tdwp3aax6gqfkcdw4mah52fp7dxarelspo7gzte4eyrhpisafcjq   (915.07, Aug; the README flagship)
emem:fact:defi.zb493.xuqA.zcb5f:jzxzmvomshs6di3bkgponk6p3rgfk5nyvklekj6caegx6dwcuo5q   (915.07, Sep; live recall today)
```

Output for the May token:

```
bytes received : 509
token fact_cid : yqbolgeoycqkvj3zkxukb4bjw4odhpwvfzqo3fbgwf4spk45zala
re-derived cid : yqbolgeoycqkvj3zkxukb4bjw4odhpwvfzqo3fbgwf4spk45zala
cid matches    : True
cell matches   : True  (defi.zb493.xuqA.zcb5f)
observation    : copdem30m.elevation_mean = 918.0 m (tslot 0, signed 2026-05-28T19:54:32Z)
tampered value : 918.1 -> cid vines36lclftct32... matches=False
```

What this shows, stated precisely for the poster:

- An agent that kept the May token still gets **918.0**, and knows it came from a 90 m DEM
  via Open-Meteo. An agent that kept the sentence "elevation is about 918 m" cannot tell
  that the live answer moved, or why.
- **Two different CIDs carry the identical value 915.07.** The hashed body includes `signer`
  and `signed_at`. So a `fact_cid` names *one signed attestation*, not the physical
  observation behind it. The shared key across attestations is `(cell, band, tslot)`.
  Say this on the poster. A reviewer will find it.
- Where this came from: an external auditor first noticed the drift in August
  (`emem/docs/benchmarks.md:320-326`, `docs/collaboration-log.md:51883`). We re-verified it
  independently on 2026-09-29.

## Exhibit B: a wrong number is caught before it is repeated

```sh
T=emem:fact:defi.zb493.zezo.zcb35:nflpddk7zsncywguwjzk5koksseqfyx4jnngkuryrnd4aykqlpfq
curl -s -X POST https://emem.dev/v1/echo_verify -H 'content-type: application/json' \
  -d "{\"token\":\"$T\",\"claimed_value\":0.74}" | jq '{matches,drift}'
# -> {"matches": false, "drift": "wrong"}   (the signed value is 28.0 degC)
```

This fact is a met.no weather forecast, not EO. Use it only to demonstrate the mechanism.

## Exhibit C: a receipt verifies without trusting the server

```sh
curl -s -X POST https://emem.dev/v1/recall -H 'content-type: application/json' \
  -d '{"place":"Bengaluru","bands":["copdem30m.elevation_mean"]}' \
  | jq '{receipt: .receipt}' \
  | curl -s -X POST https://emem.dev/v1/verify_receipt -H 'content-type: application/json' --data-binary @- \
  | jq '{signature_valid, merkle_proof_valid, valid}'
# -> signature_valid: true, merkle_proof_valid: true, valid: true, preimage_version: 2
```

This call asks the server to verify. For a check that trusts nothing on the server, use the
offline verifiers: `pip install "ememdev[signing]"` then `verify_receipt_offline`, the
browser verifier at `https://emem.dev/verify`, or the `emem verify` CLI.

## Live-demo risk found today

`POST /v1/band_raster` (Sentinel-2 B04 over Lahaul) and `POST /v1/raster/resolve` on the
`web/index.html` example raster token both returned **HTTP 504 `compute_timeout`**
(40 s budget) on 2026-09-29, twice each.

Before the poster session:

- pre-warm the raster and cube examples;
- record their outputs;
- have an offline fallback. `cargo run -p emem-primitives --example satellite_downlink`
  needs no network.

Do not print a field token on the poster unless it resolved within the previous 24 hours.
