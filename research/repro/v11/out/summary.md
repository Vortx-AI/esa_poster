# Mutation suite: summary

16 in-scope mutations, one control (G0), one out-of-scope case (M17, entity).
Whole suite 0.0536 s; one full verification (level I) 1.207 ms, offline.

| level | representation | in-scope applicable | acted on corrupted evidence | decision flipped | genuine refused |
|---|---|---|---|---|---|
| A | prose | 15 | 15 (M1, M2, M3, M4, M5, M6, M8, M9, M10, M11, M12, M13, M14, M15, M16) | M2, M8, M12, M13, M14, M15 | no |
| B | structured | 15 | 15 (M1, M2, M3, M4, M5, M6, M8, M9, M10, M11, M12, M13, M14, M15, M16) | M2, M8, M12, M13, M14, M15 | no |
| C | opaque id | 16 | 13 (M3, M4, M5, M6, M8, M9, M10, M11, M12, M13, M14, M15, M16) | M8, M12, M13, M14, M15 | no |
| D | content hash | 16 | 12 (M4, M5, M6, M8, M9, M10, M11, M12, M13, M14, M15, M16) | M8, M12, M13, M14, M15 | no |
| E | + binding | 16 | 9 (M8, M9, M10, M11, M12, M13, M14, M15, M16) | M8, M12, M13, M14, M15 | no |
| F | + signature | 16 | 3 (M14, M15, M16) | M14, M15 | no |
| G | + log | 16 | 2 (M14, M15) | M14, M15 | no |
| H | + recompute | 16 | 1 (M15) | M15 | no |
| I | + source re-read | 16 | 0 (none) | none | no |

First level at which B is protected (refused or unaffected):

- M1 (stated value moved by 1 ULP): C
- M2 (stated value rounded to "0.47"): C
- M3 (1 ULP changed inside the served bytes; token kept): D
- M4 (record cited for another cell): E
- M5 (an older record handed over as the current answer): E
- M6 (a record for another band handed over): E
- M7 (token miscopied by one character): C
- M8 (value changed to 0.45, re-encoded and re-hashed): F
- M9 (cell changed inside the record, re-hashed): F
- M10 (tslot changed to look current, re-hashed): F
- M11 (source scene id changed, re-hashed): F
- M12 (derivation offset changed, value recomputed, re-hashed): F
- M13 (value 0.45, signed and logged under the forger's own key): F
- M14 (value (0.46) disagrees with the signed DNs; signed and logged): H
- M15 (DNs read from the pixel 10 m south; signed and logged): I
- M16 (a second signed version shown only to B (not in the log)): G
- M17 (same record; A meant a different physical entity): never

Leave-one-out (all six checks minus one): mutations that get through

- without D (content hash): none
- without E (binding): M4, M5, M6
- without F (signature): M9, M10, M11, M12
- without G (log): M16
- without H (recompute): M14
- without I (source re-read): M15

Notes

- The source check (I) compares the signed DNs with the committed 25 Sep COG window; it does not
  follow a forged scene id to another scene, so M11 is caught here by the signature, not by the re-read.
- The signature check recomputes the batch root from the fact hashes, so it subsumes the content hash.
  The hash earns its place by being checkable alone, offline, without the attestation.
- T2 rows use a TEST key the verifier is told to trust; nothing is signed with emem's key.
