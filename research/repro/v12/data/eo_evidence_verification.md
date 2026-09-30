# EO evidence pack: verification record

Pulled from live https://emem.dev (emem 2.4.2) between 2026-09-30T18:54:57.023Z and 2026-09-30T19:25:57.683Z UTC. Every raw response is in `eo_evidence_raw.zip`; `raw/index.json` gives the request, HTTP status and query time for each file.

## Result

- Facts kept: 780. Facts verified: 780. Facts dropped: 0.
- Case 1, one Berlin cell `defi.zb655.yaka.pUxe`: 25 facts (20 readings, 5 signed absences).
- Case 2, Keylong field cell `defi.zb572.xoso.zb1ec`: 155 Sentinel-2 NDVI facts, 2022-01-27 to 2026-09-25 (14 before 2025, 141 in 2025 and 2026).
- Case 3, Rondonia: 100 grid cells x 6 bands = 600 facts.
- No fact failed any check, so nothing was dropped.

## Method

The verifier is `verify_lib.py`. It uses only `blake3`, `cbor2` and `pynacl` and imports no emem code. Rules come from `GET /v1/verifier_spec` (saved as `raw/meta/v1_verifier_spec`). The network is used only to fetch bytes. Every check runs locally.

Pinned key: `777er3yihgifqmv5hmc2wwmyszgddzderzhsx6rex4yoakwomvka`. The same key is published in `/.well-known/emem.json`, `/.well-known/jwks.json`, `/.well-known/did.json` (`#responder`) and `/v1/health`, and all four agree. This ties the key to whoever controls emem.dev. No independent party vouches for it.

For each fact:

1. Fetch the signed CBOR body with `GET /v1/facts/{cid}` (`accept: application/cbor`).
2. Recompute `fact_cid` as base32(BLAKE3-256(bytes)) and compare. Check that the body names the expected cell, the expected band and the pinned signer. Check that the JSON recall values equal the CBOR body.
3. Resolve `emem:fact:<cell>:<cid>` with `POST /v1/memory_token/resolve`. Check the receipt's Ed25519 signature over the v2 receipt preimage. Check that the receipt binds this cid and cell, and that the receipt's batch Merkle path leads from BLAKE3(fact bytes) to its root.
4. Find the attestation entry in the transparency log. The API has no cid-to-leaf index, so the verifier bisects on entry timestamps and then scans. Then check the entry hash, that the exact fact bytes appear in the entry, the recomputed batch root, and the attestation Ed25519 signature by the pinned key. Also check that the entry's batch root equals the receipt's root.
5. Check RFC 6962 inclusion of the entry under a signed tree head from `/v1/log/inclusion`, then flip one bit of the leaf and confirm the proof rejects it.
6. Recompute the value where the signed derivation carries its inputs. NDVI is recomputed from the signed B08 and B04 DNs and the BOA offset. S2 reflectance comes from DN and offset, and S1 VV dB from the signed linear gamma0. For absences, reason_cid is recomputed from the reason text. Every recompute is bit-identical. For raster reads (DEM, WorldCover, CCI, GSW, Hansen, GFC2020, TMF, CAMS, MODIS, DMSP, Overture), no recompute was attempted. Those values are bound by the cid, the signatures and the log, but they were not re-read from the upstream raster.

Log heads: 4 signed tree heads were used. Each one is proven consistent with the final head (tree size 2571756, signed 2026-09-30T19:25:56Z) by an RFC 6962 consistency proof:

| first tree size | signed at | STH signature | consistent with final |
|---|---|---|---|
| 2570212 | 2026-09-30T19:01:18Z | pass | pass |
| 2571336 | 2026-09-30T19:10:54Z | pass | pass |
| 2571654 | 2026-09-30T19:13:43Z | pass | pass |

## Check totals (all 780 facts)

| check | pass | fail | not applicable |
|---|---|---|---|
| resolve_http_200 | 780 | 0 | 0 |
| cid_recomputed | 780 | 0 | 0 |
| cell_bound | 780 | 0 | 0 |
| band_bound | 780 | 0 | 0 |
| signer_is_pinned_key | 780 | 0 | 0 |
| json_matches_cbor | 625 | 0 | 155 |
| receipt_sig_valid | 780 | 0 | 0 |
| receipt_binds_fact | 780 | 0 | 0 |
| receipt_merkle_path_valid | 780 | 0 | 0 |
| log_entry_located | 780 | 0 | 0 |
| entry_hash_matches | 780 | 0 | 0 |
| fact_bytes_in_entry | 780 | 0 | 0 |
| batch_root_recomputed | 780 | 0 | 0 |
| attestation_attester_pinned | 780 | 0 | 0 |
| attestation_sig_valid | 780 | 0 | 0 |
| entry_root_eq_receipt_root | 780 | 0 | 0 |
| log_inclusion_valid | 780 | 0 | 0 |
| log_inclusion_rejects_flipped_leaf | 780 | 0 | 0 |
| trajectory_value_matches | 155 | 0 | 625 |
| recompute | 266 | 0 | 514 |

`json_matches_cbor` does not apply to trajectory points, because the trajectory JSON carries only value and cid. Those points instead use `trajectory_value_matches`, which checks that the trajectory value is bit-identical to the CBOR body.

## Requested but not signed

These instruments were requested at the Berlin cell. None returned a fact, so none appears in the pack.

| band requested | HTTP | outcome | queried at (UTC) |
|---|---|---|---|
| era5.t2m | 200 | no fact; upstream_error, retryable: era5 hourly.temperature_2m[18] missing or null | 2026-09-30T18:57:23.627Z |
| era5.precip | 200 | no fact; upstream_error, retryable: era5 hourly.precipitation[18] missing or null | 2026-09-30T18:57:23.862Z |
| tropomi.s5p.no2 | 400 | band_not_in_registry | 2026-09-30T18:57:28.361Z |
| tropomi.no2 | 400 | band_not_in_registry | 2026-09-30T18:57:28.650Z |
| s5p.no2 | 400 | band_not_in_registry | 2026-09-30T18:57:28.929Z |
| dynamic_world.label | 400 | band_not_in_registry | 2026-09-30T18:57:29.206Z |
| dynamic_world.v1 | 400 | band_not_in_registry | 2026-09-30T18:57:29.486Z |
| openet.et | 400 | band_not_in_registry | 2026-09-30T18:57:29.766Z |
| viirs.dnb.monthly | 400 | band_not_in_registry | 2026-09-30T18:57:30.196Z |
| viirs.dnb | 400 | band_not_in_registry | 2026-09-30T18:57:30.296Z |

Sentinel-5P TROPOMI, Dynamic World, OpenET and VIIRS DNB appear in `/v1/sources`, but no band for them is wired on the live responder. ERA5 retried with explicit time slots also returned upstream_error.

## Provenance classes

The class comes from `band_metadata.provenance.class` in the recall response. Where that field is absent (trajectory and resolve paths), the class for the Keylong NDVI facts is taken from the `indices` slot in `GET /v1/bands`. `modis.lst_day_8day` and `firms.active_fires` have no manifest entry. A live recall filtered with `provenance=[unclassified]` returned both, which confirms the fail-safe `unclassified` class. The emem manifest classes WorldCover, CCI biomass, JRC GSW, Hansen, JRC GFC2020 and CAMS as `model_output`.

## Case notes

- Keylong backfill: 119 newly materialized, 7 already cached, 29 scenes signed as unusable at the pixel (cloud or mask). Of the 155 points, 27 come from Element84 COGs that carry no BOA offset; their NDVI recomputes with offset 0. Platforms: S2A 21, S2B 69, S2C 65.
- Rondonia grid: 10 x 10 nodes, 9.700 to 9.760 S, 63.000 to 63.060 W, about 740 m apart. Each node is one cell of about 10 m, so these are point samples, not plot polygons. The pack is not a Due Diligence Statement.
- EUDR rule used: flag when JRC GFC2020 marks forest in 2020 and Hansen marks loss after 2020. Categories: not_forest_2020_no_hansen_loss 43, forest_2020_no_later_loss 33, cleared_2001_2020 20, eudr_flag_forest_2020_loss_after_2020 3, loss_after_2020_on_gfc2020_non_forest 1.
  - flag: row 2 col 7 (-9.713333, -63.013333), cell `defi.zb391.taza.zcc31`, loss year 2023, tree cover 2000 100 %, CCI biomass 2022 208 t/ha, NDVI 0.433; loss fact `6rtcbfumrzhac2a32vkoixocgtel7ws5bxnra2omnrjv5apyfnea`
  - flag: row 4 col 8 (-9.726667, -63.006667), cell `defi.zb391.nota.zcc7f`, loss year 2024, tree cover 2000 86 %, CCI biomass 2022 231 t/ha, NDVI 0.682; loss fact `oiu5g7xg2hnokz25sjoxagm42m7wodcb6xemhxrmokpol4vtu2va`
  - flag: row 8 col 8 (-9.753333, -63.006667), cell `defi.zb391.bOyE.zcc7f`, loss year 2024, tree cover 2000 49 %, CCI biomass 2022 118 t/ha, NDVI 0.655; loss fact `kvy4a65jlaqcy3mgbpfoz7vnabnhiknvgoxydaweim4gvftwk53q`
  - maps disagree: row 7 col 3, cell `defi.zb391.fisO.zcafa`, Hansen loss 2023, GFC2020 forest 0, JRC TMF deforestation year 1984. Not flagged under the rule.

## Per-fact record

`eo_evidence_per_fact_checks.csv` lists every fact with every check. The lines below give case, band, fact_cid, log leaf and verdict.

```
berlin    cams.no2                           r5kr6sgs2yrgihnalmjnzjdbez2tsarijxwbltnxqdeelukkra7a leaf=1453722 PASS
berlin    cams.no2                           jvwhwgm6gu6irtd26rsfkkeg6hw72amealfuxdepxam7fpnlf4za leaf=2570186 PASS
berlin    copdem30m.elevation_mean           sdu3gfiu4hioukhphatvgoir52dwju7eukdwosfkxt4ndopahz4a leaf=2570170 PASS
berlin    esa_cci_biomass.agb_t_per_ha_2022  keebyc7rs63obeuiprdromm5spnlokjs7zbsywmkt6vfumqrwtta leaf=2570185 PASS
berlin    esa_worldcover.lc_2021             xicg6usfctfgarydipb5evusbfl7ew2gmb6waoqy3lputi4cbztq leaf=2570179 PASS
berlin    hansen.loss_year                   fdtciergf7zniv2q2f3jxhgp33rfe5pwzrgh3wst4gv4l264izza leaf=2570183 PASS
berlin    hansen.tree_cover_2000             x4kpkygflp35lsynav3dnmybaclt46ayqb34akrrnzst3qrgrjbq leaf=2570182 PASS
berlin    indices.ndvi                       5iixkdp2auwva4hwul5wgzsikccovzu6xgbnji5y2app66ares2a leaf=527813 PASS
berlin    indices.ndvi                       y2k2tic2smuobi5hcwfvaq2p2apk3lpwekaggboyawum3tzqjw7a leaf=2570176 PASS
berlin    jrc_gfc2020.forest_2020            oog2b4aykebescspshijuxiwuq3dfxdjp47yd4vwxy4pqdnlmwcq leaf=2570188 PASS
berlin    modis.lst_day_8day                 yqhihmuyozdm2urlpk5nxzkoozct65y6shsysttouoy27ddklhnq leaf=2570193 PASS
berlin    modis.ndvi_mean                    ty77ne73kyexhf43qyoabvxzcu65yveqwm3nhbkc7de3cdpzn6cq leaf=2570190 PASS
berlin    nightlights.dmsp_ols_avg_dn        2ozugc3sy2cskemheusdzm6ks7dtcfu6lcbcgjdc4x7m3jo7qeya leaf=2570194 PASS
berlin    overture.buildings.count           czehax3d3djwpkfrawqdj4b6o7xvkbrugnco6qbin73mo4hofu2a leaf=1453714 PASS
berlin    s2.B04                             x4jh23askylgrdbtlecius3gmqcyhgyxupsb2dozgpwtavkytqua leaf=2570175 PASS
berlin    s2.B08                             wtqd64payr37jhzyk624ii4gc6k4in5q7kpr7tabob5lah4yquta leaf=2570177 PASS
berlin    sentinel1_raw                      zts3wqlnhexgxsrpakbwuvo3yqim3ty53slvuijyxmyfm7bvifua leaf=1453728 PASS
berlin    sentinel1_raw                      2x2enxej23rl4hpkycidwmy3brqfrhghqiucrrwzf6o76a53lyjq leaf=2570178 PASS
berlin    surface_water.occurrence           hohgux3n36e7bjsekaii5f7m4wfxkwpy22666w322s7ey4uqt72q leaf=2570180 PASS
berlin    surface_water.recurrence           dkcztut32o2ajs2ehillrurbjcyvuzim4qatmtizaewviutvibtq leaf=2570181 PASS
berlin    chirps.precip_daily_mm             bkaovfadmyjwyj6ggx5kct6j4y2cbig2rfwio24cji7cv7ek4kiq leaf=2570184 PASS
berlin    firms.active_fires                 k2ykb2dshtzcfamtdrwd6peav4tct3gh4wc4pmhnhcvu27wvu6ma leaf=2570191 PASS
berlin    jrc_tmf.deforestation_year         w7t2hxc7yvumi6ck75m3fmq5rv4o4qwgzjy3y5zq5xodbx6exudq leaf=2570187 PASS
berlin    soilgrids.phh2o_0_30cm             msqj4t54fro7aj7hb333racgmaohxjqgxwd57jz47jzymqvyjowa leaf=2570189 PASS
berlin    soilgrids.soc_0_30cm               mkwinv556gemukzvucnj3em3s3bhspp7lct3pmrwv63yeztl6a3q leaf=2570192 PASS
keylong   indices.ndvi                       2dpnuf4eqjgmacmwq5hqoofpcslmsmehtui2mnul5x6pbh2ttnwq leaf=546488 PASS
keylong   indices.ndvi                       av3yiinq7ss65rp2zq5sez47fepcu2kgcbw6kdvwbmryhols3ecq leaf=546495 PASS
keylong   indices.ndvi                       ambveemg22gb6sxg43zmyotgzkl2bdv42y4od64nvlj63qfjwisa leaf=546499 PASS
keylong   indices.ndvi                       r47ns5s7yboyn5l2qmwstpw7z2fwvjgxb5zqowe76g2dkhbxdagq leaf=546500 PASS
keylong   indices.ndvi                       pawwouui324b5ohyalaehuzk3pe5th7wn2tz2mfeepe35izzq7yq leaf=546502 PASS
keylong   indices.ndvi                       pdggyrzguuwuy3hhaslof2hkdmwupzmdap3e53yw7zsksja7xaxq leaf=546504 PASS
keylong   indices.ndvi                       6bixwohsocr7ml4jrjga6zq2i3d4v4ir73z2wbhie7qzovzoadsq leaf=546506 PASS
keylong   indices.ndvi                       gxatpd7rxcybtcqkguejubt5uu2mlzpjjjzgpuekugoxdxricisa leaf=546511 PASS
keylong   indices.ndvi                       abq3ohgxtkhefaluiitasxj2x7g22xatcqgudn44z2vbnpqqp66a leaf=546516 PASS
keylong   indices.ndvi                       w2aiub3fjkrkh4cezwsktlne3z2l7zciwtxl6tfpqjl3kf5g3osa leaf=546518 PASS
keylong   indices.ndvi                       zgtxa5b3sz6sqqcuvqped63m2thrjfnsd5turq4uracpki3wstsa leaf=546525 PASS
keylong   indices.ndvi                       uvpcasbwhfjyg7pwp2ad7hjrtvgzk4hfq7vg5wc7hhinzc35krva leaf=546527 PASS
keylong   indices.ndvi                       jtqrz5afacn7qejs4m2gbzep3rxmddza7d6vbcy7mpnv2sbtlhmq leaf=546529 PASS
keylong   indices.ndvi                       qwli4ej4zdadwr3cyvmpz5qpttleko44ydh3kqvbfab25dkk5dua leaf=546535 PASS
keylong   indices.ndvi                       qinwnmwkyifxztpojlfqpjjrobifnwmaltezctp7gwvyh23eugja leaf=546536 PASS
keylong   indices.ndvi                       dhesyu6hlocjrkkjs6mgus7scl2qle43tpeu5zfiw66ozw4nv3bq leaf=546537 PASS
keylong   indices.ndvi                       l5bhccee7b4vt277nsnldnz3euxil26clvpytlx2clghhpfg4oyq leaf=546539 PASS
keylong   indices.ndvi                       52rd5swgxsqrh4okxjjjvauuvgag6wqa37xwdx3n6oqferl3bh5a leaf=546548 PASS
keylong   indices.ndvi                       odzwxq7gymlpn7lniohjifgc64lntae3pxka2m236y456d3ehura leaf=546551 PASS
keylong   indices.ndvi                       egnix55xnlwnutvaiyp6wmrpfiastichsswkkalc7qebnmrqwffq leaf=2571160 PASS
keylong   indices.ndvi                       dccco5g67rt5lexvlrnt5pqrojo3b3s4cxdn62j6vfrtqw67uuza leaf=2571161 PASS
keylong   indices.ndvi                       ul74ppkfjsd5wrvitzestifoqemvd3jym5f6au32c34rlbpbwdna leaf=2571162 PASS
keylong   indices.ndvi                       5lo7yvchfdx3svyhgvdcs4ua4m23x6pic4eaj375bywnwmdywghq leaf=2571163 PASS
keylong   indices.ndvi                       ilhnucuw3ezipljhofawuxccdvnpcpwozl6xb5sfrcsccmijsqxq leaf=2571164 PASS
keylong   indices.ndvi                       wonip2v36xyhrtwl5t4hrhel7o34lh3w3qnbbg5jofvdpgopmxaq leaf=2571165 PASS
keylong   indices.ndvi                       wvsktgghwbbfawlvk3tmnxb5cvex2gckx4cuxnc6xjuthhpqyhza leaf=2571166 PASS
keylong   indices.ndvi                       57gxhasa46rj2gugpzfq3jbyx6mca34gl3bqa2w3aarfmohoi42q leaf=2571167 PASS
keylong   indices.ndvi                       bdersdzw5n54bydv7vqj46oo6ogvlrcsamwxhzxtekkx7rf4k75a leaf=2571168 PASS
keylong   indices.ndvi                       2xxrfa6bkt3lt2p2yhzawkk5mradps6kw3rjdm35gsovpmlt7y3a leaf=2571169 PASS
keylong   indices.ndvi                       vwrsgykste3v2cpkbdf6nmd3h77shkpmbbkpdraqi4dlxtie56aq leaf=2571170 PASS
keylong   indices.ndvi                       3uqyffbwcw2mnpv4wjtuxszzx4ah6bdr6642sz6e23hx4qjehxrq leaf=2571171 PASS
keylong   indices.ndvi                       ztnusdzumedrb6nfmyxbpzq3wn5nrdq7rwqlxwbi26wqasu63nha leaf=2571172 PASS
keylong   indices.ndvi                       4euht427es2uruob2lmxssceoqg6f3ltq4soelirhzxmqf2e34vq leaf=2571173 PASS
keylong   indices.ndvi                       akdmtpziqibykoi7cn6xlkeeojeyakodjcls5wtifmg6aem4d3zq leaf=2571174 PASS
keylong   indices.ndvi                       2l5ta6hkuvvlhnjkphkctjlxht66f3sa3oxwgfv2dvjjcstyzhca leaf=2571175 PASS
keylong   indices.ndvi                       sh35c7qbddanlwx62k42eaizps4l7vsyob32kbprrurbm4z2kr4q leaf=2571176 PASS
keylong   indices.ndvi                       cijznct4colahrrjg335rvcloevj3uxr246joddzkvy7gzyo2wya leaf=2571177 PASS
keylong   indices.ndvi                       zgklv5c6t2vyw4urhkn4y5g6qjnfcd7v6a5be7prjc7rx4y6b7tq leaf=2571178 PASS
keylong   indices.ndvi                       bkfpa7dnxtg3g64twxe4y4zlwmjlen7nyedxotm5fbyitwllftjq leaf=2571179 PASS
keylong   indices.ndvi                       zabwh3mxvxby2mgkyz7apjfrpfz4a3w6g33xjrcnkv27jyvcwxhq leaf=2571180 PASS
keylong   indices.ndvi                       bqtkdup7yzun2icuc3wdgxy2ncshldouyzy7vhxybqi7lnxol2ca leaf=2571181 PASS
keylong   indices.ndvi                       iai54v4dnvwaklgyopolulskuu2wyifsi4pxivyjhrup73uvnroa leaf=2571182 PASS
keylong   indices.ndvi                       j4ez6ll5yokybeqhl6mbz7r5uqcssuwqoaemx5rvi4hsgkx5nlra leaf=2571183 PASS
keylong   indices.ndvi                       m4ymsv465gddpeiszrqbcjqglumsvyjotjxaccik6zlcyymvotra leaf=2571184 PASS
keylong   indices.ndvi                       3esge77p6esdllhlj7hjkgezgxf7x7nguxckd5fyfa5lawhmsxsq leaf=2571185 PASS
keylong   indices.ndvi                       2qhftyky3ga7lf32b7yknfw6zi7js26y63gujmjpd6touipcttna leaf=2571186 PASS
keylong   indices.ndvi                       r26hi43g3vpdjyavsyri3ofuv7ewyfrlibbxjuaub54izpqxrz6q leaf=2571187 PASS
keylong   indices.ndvi                       bs7s5a43vq4lb57x4y4pnwl3w3qa4vbrhsnmmqukstlduvm2swxa leaf=2571188 PASS
keylong   indices.ndvi                       7r4vbsvkw7zsx6jy5qp2oqhy5e5ppdgbinperu2c76tllzir3enq leaf=2571189 PASS
keylong   indices.ndvi                       j57vasawosbg7kmjs3zuzynr7t3izbcu5ycwtvubpct2ykqll7qq leaf=2571190 PASS
keylong   indices.ndvi                       u63sp2h7nzmcr2nxuavww554auiimcgvv7odojlee2yd7xn3vola leaf=2571191 PASS
keylong   indices.ndvi                       cesimadglabj6fa6isv6e6imhctyy2djoyhng63ptsuoyqe7heda leaf=2571192 PASS
keylong   indices.ndvi                       npphkevfdzgqucd2sdhhuasl2v2v6yfkitbapjen2faxnhvbpplq leaf=2571193 PASS
keylong   indices.ndvi                       vv2q2wquhpiay45mksjbhpft4pi4vb6gzbhj4glntugeph2c3zsa leaf=2571194 PASS
keylong   indices.ndvi                       egp4mm5tmuzqfgg22ngjcrzwwbai5lyhtk6ulbew7tgtookiyw3a leaf=2571195 PASS
keylong   indices.ndvi                       zrcqs2vx5qsqq3mswnflojcq5trtp3xl2me5dmvkwdn7ukym3qpa leaf=2571196 PASS
keylong   indices.ndvi                       7uwcb5xibwcmjl3cgr75hiktc7krgtqgynmufovguc55wc2if7za leaf=2571197 PASS
keylong   indices.ndvi                       lsrqzf43ypizelqqnltsu3jfinhmfxab4ntzpfvaacsltre473bq leaf=2571198 PASS
keylong   indices.ndvi                       frzmuzkpnmhsaxvvlsot6v5s7qtoezoxbmm25e3cmxeefwlp7dka leaf=2571199 PASS
keylong   indices.ndvi                       v6cqz7cv7mutitdgaep24tnqrhdyjyomuqxeyqtm7dblvg5zhljq leaf=2571200 PASS
keylong   indices.ndvi                       rc2mpyysxiq4arbkgsmswhpikgcw6mfd5ivktup45wr3jvvcnvma leaf=2571201 PASS
keylong   indices.ndvi                       w55qck5rvqti2xu6w37skelvqns4qzuo3bvgp3o5kf4dxfbof2pq leaf=2571202 PASS
keylong   indices.ndvi                       35hjsdebqzb2g7ddbt6f2mlx4nqcua2mnxueol7c5q54x4nkp3pa leaf=2571203 PASS
keylong   indices.ndvi                       5ahk2vf2offgfv6ws5brm73aoscn2qrtwysk2nnfkgmwcqduzmjq leaf=2571204 PASS
keylong   indices.ndvi                       mpjwi6462r5t6vwcybr6iwrsvlraouh74hhok2o6edke5vz5iuiq leaf=2571205 PASS
keylong   indices.ndvi                       ucvd5nbad7jtn5jb5lhtbyejtcktk4hdo3do4lha2syztem7zfma leaf=2571206 PASS
keylong   indices.ndvi                       cpwbtjzcgsmmd2ifwonm2et6t3bwzoeavx3qsyd6r4yygktepkba leaf=2571207 PASS
keylong   indices.ndvi                       tzxpxrx5aurqvhmgtldjhn4ttuvcrhzxz6dbjvf6t54jz63frddq leaf=2571208 PASS
keylong   indices.ndvi                       pitvauymasymskralidx3cuwqyjc4zsktpvspmzezozo5277vjna leaf=2571209 PASS
keylong   indices.ndvi                       6wjavzwctok2n3qye5ft77fxbpbsagtshrbxwzh6dx6cmis66r7a leaf=2571210 PASS
keylong   indices.ndvi                       tomipqiog5o2djk2xylv6onlfv4zoruyaf2flebbyfd3o64ldgja leaf=2571211 PASS
keylong   indices.ndvi                       t7nc2mpwsps6lzo5fd442lynok64nrucjr4x2jtefjqda6y6hpwa leaf=2571212 PASS
keylong   indices.ndvi                       fal3ndhgdh4ecws6nxluyqsajat6ghff3whmemni5mbwxhkhma4q leaf=2557548 PASS
keylong   indices.ndvi                       gl3cepxngl6kouadxnw4g4uvapunkenv7dccq5gamgyej5wkvbiq leaf=2571213 PASS
keylong   indices.ndvi                       ppqhsnziipnlfb2otd6lvgrcrvoca2d4kshsbndhty5rozvmpbfa leaf=2571214 PASS
keylong   indices.ndvi                       olqj3po6jo7a6do5yt7joa35gx7v3ot4uc55mwx7vmjudhznvesq leaf=2571215 PASS
keylong   indices.ndvi                       ws76b5b4egsxj6odagleis7n4begblgxufgietlbkdhbyfxbwvaa leaf=2571216 PASS
keylong   indices.ndvi                       qncg5ycemsejbnocf6l63lefqqt63ap7noij6vqnboaokuldmsla leaf=2571217 PASS
keylong   indices.ndvi                       5euwulti6u3ukkgjdkastydr4wrdup2lzsezfzii43phqk276mma leaf=2571218 PASS
keylong   indices.ndvi                       4n2lhps42quim36wlithjaapnshyzpu3jvfpxpmqm7tctd5sengq leaf=2571219 PASS
keylong   indices.ndvi                       2za5oyziyghdh3i3csxmqqblheicoyx47jeckv6bx4tp2yjbt6ua leaf=2571220 PASS
keylong   indices.ndvi                       sbtopiujz2vajuftxtveqbusbulvtj5lk3kechp5wyhsuhlkoglq leaf=2571221 PASS
keylong   indices.ndvi                       34k4wmxefoex4l43qcacrnitbx6kzmuqtczrnkhqtyorgp7n5zma leaf=2571222 PASS
keylong   indices.ndvi                       ke4chyv5goi5eqt3xsyy27fvkmzf4cmighlgdlslperytamkcx3a leaf=2571223 PASS
keylong   indices.ndvi                       zkcprs6akmwmviqisjtpa7ld5axm3i2iyolxcax5pccyo5umayuq leaf=2571224 PASS
keylong   indices.ndvi                       l7jwqsxjtbpqbg5r6t4rv36mbiil5zb6xbsypsnjmhdk4cizujsa leaf=2571225 PASS
keylong   indices.ndvi                       t4fioklxfzhgqvslbecbk5ww2b4gfsfq5cpe7noxpfqeqnmjxgpq leaf=2571226 PASS
keylong   indices.ndvi                       pbcx2oo2q4o7cvd2qwrxa73te2ub2r7pvmbvmrrbud56kjizdpqq leaf=2571227 PASS
keylong   indices.ndvi                       5x7nizwkcju5je2swp6kal724njh5ksyweworaxu2g7mv26q5nua leaf=2571228 PASS
keylong   indices.ndvi                       kga4lairaavbqikovpmzlqbh3cjjbbsky5od3hr4477nxyvaiz4a leaf=2571229 PASS
keylong   indices.ndvi                       jbe7arunsjvd2vqpnkjo54qy2co2hcrvzqmatkyqu23ldhxgedhq leaf=2571230 PASS
keylong   indices.ndvi                       abexsf72hhujdaarr4pgskp5afrc2beckpkzfotxxwtufkcun56a leaf=2571231 PASS
keylong   indices.ndvi                       hlpsryqjr3kz42fqzzwucrdilf2uwo5ld6bnnufdluie5zingr2q leaf=2571232 PASS
keylong   indices.ndvi                       hy7ao3bt5apxyhk5a6h2jhsmsjheo726s2wzburobqiricd35jyq leaf=2571233 PASS
keylong   indices.ndvi                       gad7jb3d5y3eavsw5rafcpa5ulelwyhwvlcgqybghpwyz3c3aaya leaf=2571234 PASS
keylong   indices.ndvi                       bg6ra6md5f7fo5mb4hm3scpgssaly6z6sk4a6czweciegdns4ijq leaf=2571235 PASS
keylong   indices.ndvi                       or6diopgrw57bozl4appslnzutqu2bdw5dw5q5tpp2dz2zibepva leaf=2571236 PASS
keylong   indices.ndvi                       5wn5azfvmdcpwxuqaqzanmko2aec35tyvd2hr5qcq3apay6b5yla leaf=2571237 PASS
keylong   indices.ndvi                       o6n2wpooii4t3wrlaqykow42t2cdn3dngjcp6arifr6t7drolema leaf=2571238 PASS
keylong   indices.ndvi                       ezobstlti3rk2yfqxcb3z6tp6lmwf45jndenfirpdscgnb6qny6q leaf=2571239 PASS
keylong   indices.ndvi                       snzym7yecqbnacabc7ackhoa253zlcrdtn6auybwrbkf7kboasdq leaf=2571240 PASS
keylong   indices.ndvi                       4qj3l4mgh7ch5kvxmkqspjdl6y42oqhm42khh3gostccpixkbz5q leaf=546552 PASS
keylong   indices.ndvi                       aeg2w2m3d3am2nmfnugytlw5dc6ciwzderx66w3i4khodvdoxnoq leaf=546557 PASS
keylong   indices.ndvi                       sb5xeaw2s2i4jnlyawuabc7di3tgm5zh24ihc73nvch3le3do3ba leaf=546558 PASS
keylong   indices.ndvi                       kxd7jgts5wcidgkszlgeycv3ry7npdxd3ullcad3xht26ncqcexa leaf=546563 PASS
keylong   indices.ndvi                       27wcyyi4zvzgybvqzzdtese5ra5zsrj3jasy2fdvla5pyvsgmspq leaf=546566 PASS
keylong   indices.ndvi                       2etdpvwibg6dge3jleoy4lfe53kqphdr2c5rh7rraiuc7pqidadq leaf=2570200 PASS
keylong   indices.ndvi                       bkucgr5rwx5acphqiirnc6rtep5ek4lociginq5u7t6zy57webaa leaf=2570201 PASS
keylong   indices.ndvi                       j63cro5dm4gz5x37elekkjybszofnqesvgvrglrviy7rrydbf2wq leaf=2570202 PASS
keylong   indices.ndvi                       wv576wzhb2v7iujztrtwcjhaz7cfi4aez4mrkr6ospc5alroxgrq leaf=2570203 PASS
keylong   indices.ndvi                       4gql6tueamshkghdo65nk24fexpvpvgwagx3lejgrwb4jy7tujqa leaf=2570204 PASS
keylong   indices.ndvi                       ocd56xlsoke6lo3nwboz4qja7rzzzvmmr4ao2nyjhgzqq6azmyfa leaf=2570205 PASS
keylong   indices.ndvi                       7uq76ubexqxbr3bxmhkcaxifyzm2ow4uethyevp4lhrhb6jpp3ma leaf=2571241 PASS
keylong   indices.ndvi                       dlud4jknjinqt4hx7k2coly6nua7u6m3qkxszdfqvt7e37w5tcsq leaf=2571242 PASS
keylong   indices.ndvi                       vdph4ykmfomrl2i34ylyxta5r3frbykcezekeahzk2pcjxttlgfq leaf=2571266 PASS
keylong   indices.ndvi                       2kxurmof36zg3tpmgdyythscbv4bhmrjz6riir7g3jvsvchdcxfq leaf=2571272 PASS
keylong   indices.ndvi                       z4zj4bpkxzfybw5xhjfbgyofvzw5m4syz5d5m6dq4vht63zjp2xq leaf=2571273 PASS
keylong   indices.ndvi                       fcwwby5vtdsdwn72driweqf3qq3p2evu4n57tpl3yetseiyaznvq leaf=2571274 PASS
keylong   indices.ndvi                       t5g2jdhml5mhkcoxy2gkklwfodbyvhaiwctth5g3ibvfo3op5bgq leaf=2571275 PASS
keylong   indices.ndvi                       erqkxhj4uyvkzm5igjmcqrq6njwydmtqyauquiroosejqzflltyq leaf=2571276 PASS
keylong   indices.ndvi                       gwehadlpntvbpxiqfoxsasozgd5mot3oavld6w75gv2vy7jz7cza leaf=2571277 PASS
keylong   indices.ndvi                       awc3pf5j7sktr6yp6hap6j67d6wquhozu5ytgcffrzgvx2nybjhq leaf=2571278 PASS
keylong   indices.ndvi                       c3i7cpimlhmyhizegrtnvkrn6rcrzdxwpbkhyvmeigjkyozhikna leaf=2571279 PASS
keylong   indices.ndvi                       midyz3lybrxv4e5ocnoa7uc3j3beiocmffceomik7e52lv4nekva leaf=2571280 PASS
keylong   indices.ndvi                       u25ma7zuzvtd23jh7hwt5ifgjxsk2kxjyoc2tzdcfge5wrcaixua leaf=2571281 PASS
keylong   indices.ndvi                       diipckxlcin3effvx3hdwijyra73snkdlko4jcui5kx7ilsl4y4q leaf=2571282 PASS
keylong   indices.ndvi                       slmpt7etbr5v7wgx6efyxhlllhvnxo2wn6qsotokexysulrsljiq leaf=2571283 PASS
keylong   indices.ndvi                       tmlx4snnc72av5v5pg3iijue5dkb5n7knveolnm5zfha2rymkmna leaf=2571284 PASS
keylong   indices.ndvi                       quvnbidqicvoozshjw4pmhszyxzvbdmfdydr244gwvgv32soa7aa leaf=2571285 PASS
keylong   indices.ndvi                       zyorgfe2qdejbuxqvkf7zz37vmn57phndoiszy77tv6haoabxb7q leaf=2571286 PASS
keylong   indices.ndvi                       nh25ek6yx3sktt2iirfpvik53vivulghaomodra3ovmi7ti7dgmq leaf=572871 PASS
keylong   indices.ndvi                       svwyrpjrwzbdclvgxfmivn5xbonji222git7bpzqnyzirltf34bq leaf=2571287 PASS
keylong   indices.ndvi                       qqw3jqwr4llqdwucp3cdkgvg6x6nvgsemzitotxs6bae6766gxtq leaf=2571288 PASS
keylong   indices.ndvi                       v7usyptgbm6x3ejgtw7jvur4i6e6exfeorpw2izfqnpytzebl5qa leaf=540131 PASS
keylong   indices.ndvi                       vwjdyfds62ur7angwwumo54g34hv4duxtklbp46smfd3bklgiwxq leaf=2571289 PASS
keylong   indices.ndvi                       jwkqm6ehelmzrwupfwyq2oqotiarexr5bdrt4xbl3znuynhurqxq leaf=568755 PASS
keylong   indices.ndvi                       xbqqfk5r7celr2oj36asofnmzr5eevdmd67ifofbnesgjs7j7eeq leaf=2571290 PASS
keylong   indices.ndvi                       gh6vvnznsmmfka4psdq4x2lfzxhr6644btygxzurqjy7jiwyrr5a leaf=2571291 PASS
keylong   indices.ndvi                       2oeo5ezs4gmhtibjtvlkkg4db37rftlcqurkiq2nszhshta65jha leaf=2571292 PASS
keylong   indices.ndvi                       jgn4hsc2ytbfs2buio3bgkpctdyqds4d3rgdghlxsqfzuxd54vca leaf=2571293 PASS
keylong   indices.ndvi                       7kuu6y2hlqn3kdakaw5xe6gfwumybnhm3qvjibya6fqu5zxgagca leaf=2571294 PASS
keylong   indices.ndvi                       hs5acthlfiqizgoaa4kocuqruh4uxyz5t52ipeyo2ubyaliuqmtq leaf=2571295 PASS
keylong   indices.ndvi                       rdrznvrcep7ethpxa7z5sk3nls4b3rfclogzqsmnbu3cgsj6whna leaf=2571296 PASS
keylong   indices.ndvi                       dcugypdubcfxmqeqq4rdxrjjdwqsmgbhvicyli3bdilzojsq2qua leaf=2571297 PASS
keylong   indices.ndvi                       j46c36kfbkzrryu2i3zkqymucn5o5w6d4uziznx6gn4fuid355cq leaf=2571298 PASS
keylong   indices.ndvi                       ducjgy6qxr767gmfeki2oqp6e5kllzx4i3dwmzz3fvu5fl6rhu5q leaf=2571299 PASS
keylong   indices.ndvi                       cv72gvry64pqn2ccnyk5aqq2uenwlleg64h2vyirzr4b6x4akhwq leaf=2571300 PASS
keylong   indices.ndvi                       ccdlbl2ektx3btds7rpzp65ziugiw2pkyyw3ka3hqqvvhkpohe3q leaf=2571301 PASS
keylong   indices.ndvi                       fmqfudqtqdyb67wp2gvy6fnaujv3ndlezwf3o5amause3wqnyd6q leaf=2571302 PASS
keylong   indices.ndvi                       k4244lyhbp6knqv43e4dn6qrkkxu3b7k65etg4u23ado4ylbgd5a leaf=2571303 PASS
keylong   indices.ndvi                       ytck2qynqptfchmrvxejzwsej3dhpz4omdecouidq46ul46orkia leaf=2571304 PASS
keylong   indices.ndvi                       6t22dgsbuzhh5b4bmjt7ejg3bfod3o377zvimz5iqkrezchsf7wq leaf=2571305 PASS
keylong   indices.ndvi                       ucu3v57ibm2kbx2gtrvlzkcm65kqqnx3sgo7avdbghan6hxhrk6a leaf=2571306 PASS
keylong   indices.ndvi                       kxjvfwpa7grmfhkxoxufq5xjltq2s5syer2rzdx7odbnrxhnjzkq leaf=2356353 PASS
keylong   indices.ndvi                       oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa leaf=2457078 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  og2rbjgbfa3s65egor7xsb3msrv6rt47ebcp5qfdbqsn7n7sofla leaf=2571340 PASS
rondonia  hansen.loss_year                   ewjl7b37rk5f57huailutozkyou2akxesrzeejwp7fnj5lvrokrq leaf=2571339 PASS
rondonia  hansen.tree_cover_2000             3enn4wsyabcnjblgmauqcedfm7q276p44aykab7rvkt2hophzb6q leaf=2571339 PASS
rondonia  indices.ndvi                       46jjubzumxmsv5ze52z6mmf7mkusm5ik3mbikptpfhjvvtud4ckq leaf=2571346 PASS
rondonia  jrc_gfc2020.forest_2020            ieontr754lh3ndg3sslaaef4bqqrqigwlm3z44i4ubqkxmvachyq leaf=2571344 PASS
rondonia  jrc_tmf.deforestation_year         c2p6pdwyc4rwjgbfps535pqu4kkqurl3ygljaedhejc5xfvpdbaa leaf=2571344 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  vpn3c2dbtpgk424k5pidfvfxfapzveplcyghiwoztxdv6lxjrctq leaf=2571357 PASS
rondonia  hansen.loss_year                   vecm6m72hij74a6m7it36awog7fglsp55epglvuz4bil45x45xta leaf=2571357 PASS
rondonia  hansen.tree_cover_2000             3rt3i27hslxjlycba7axwkfx434qe5qw34oqyevk4scfhiicysea leaf=2571357 PASS
rondonia  indices.ndvi                       kt4bu4sot45l7sjbmv2d42w7t4kdchr76uyjyeuyua266cxpbq2q leaf=2571359 PASS
rondonia  jrc_gfc2020.forest_2020            xshquukgogesckbvasw7bu523tgjly5e3riqdkwspr56shyxwbxq leaf=2571357 PASS
rondonia  jrc_tmf.deforestation_year         5si5emjasgri36qhbwadcccpngbcbe4knigggoudg4d72y73hlha leaf=2571357 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  ahskueyqcm63nwobyjja5mgainpbx6lb2cwt5lhuwtcry2qypxfq leaf=2571356 PASS
rondonia  hansen.loss_year                   nowavx3jo3jz6a2sgvcrrtb2znrd2jm4gndm2kt6ttotalnvfu5a leaf=2571355 PASS
rondonia  hansen.tree_cover_2000             ana3hzqku4xo5677btktnmgrlzi4fhfhsxynfhzucnxiznjornnq leaf=2571356 PASS
rondonia  indices.ndvi                       dgvpkff2gg6xjmqogrvp2s2i4wsug27gr5gudrqpuwynwntraqeq leaf=2571358 PASS
rondonia  jrc_gfc2020.forest_2020            nsakm6tddt32dnx5i3hulmw44wtn6bknp2dde45ryebxxo6nbsma leaf=2571356 PASS
rondonia  jrc_tmf.deforestation_year         usrgh2bni4oajit7y2hafqcqatbfwfvhnidvadfwidbv3xlcielq leaf=2571356 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  qvfwvfnqmhu5km4rexyzxw2iypxuk3kdjscx6orlbt7rwnt7jwoa leaf=2571361 PASS
rondonia  hansen.loss_year                   hjajrjremz52sj27ji5ejtsn5aiuc2ui5oxucgnlviyla7hvodmq leaf=2571360 PASS
rondonia  hansen.tree_cover_2000             a65bnyz2hdv5b375jzgwcmez53yj62s74vg2cfpo3arrw3mz5f2q leaf=2571361 PASS
rondonia  indices.ndvi                       xfgvo7pelynuuuyc6wb5p5zjzpo5cxfpge5cab5sfttq3kcwghta leaf=2571362 PASS
rondonia  jrc_gfc2020.forest_2020            zf46bfzj4rwjb44z7vhk2umxqyfo52vnjkm3voj34ck55ukougyq leaf=2571361 PASS
rondonia  jrc_tmf.deforestation_year         5dhfv5kamjbc3uug6d4azvdr4qnoekov26wgoxdzuomjyy7f5vcq leaf=2571361 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  econcjhp5kbbw3m2trubq6hef4dz22umf3l6ingjxm52z674ih3q leaf=2571342 PASS
rondonia  hansen.loss_year                   rcilayfswfqgr42f2shlg3jb6wygimn4dg42gtjwylyhmbgdoe7q leaf=2571342 PASS
rondonia  hansen.tree_cover_2000             nce757ccuaz3bshlvthbntk36pos5vgo53ggeib2pwexnpyhwpga leaf=2571342 PASS
rondonia  indices.ndvi                       hms3tz76ueasn2x4gc6rahwm7cjfi3alyforcizghs5afwyal66q leaf=2571347 PASS
rondonia  jrc_gfc2020.forest_2020            f6yzm3awmizrf7rd7pgye3kma6ynp323flezoylkbiaf7mgh2lsa leaf=2571344 PASS
rondonia  jrc_tmf.deforestation_year         seh5ly3qa4ltktcevdiesycaiwwdktmdfy4z67wmrvtnbxvmj3ba leaf=2571344 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  zonl4a6mj3eirfl7q5rdp4wwkkfhofzffsnjng34pfmpe7i2eroa leaf=2571344 PASS
rondonia  hansen.loss_year                   rxf4uhegdkbtaiuafh4thv6w5dhf6cpesmw23e4epfkasxrwqfra leaf=2571343 PASS
rondonia  hansen.tree_cover_2000             qpfvtqopdxqvuqexy6diilzw2d5efh436nikkjueu3l5udbz4qrq leaf=2571343 PASS
rondonia  indices.ndvi                       hrnfmzlez4tuulavbdzfz6bo63pww2xeiamykuvtg7bvjozkl6aa leaf=2571348 PASS
rondonia  jrc_gfc2020.forest_2020            na6xmbre7s3xyv3glpdkxouimenfvutn656dvivi7golp5knuzba leaf=2571344 PASS
rondonia  jrc_tmf.deforestation_year         pewgasb6xdm6d6wz6bilmxjon4fv6wnion44kj755gqa2xgrf4vq leaf=2571345 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  srj5bsp4obzdzqyr22grg4c2hb5spzd7fpn62lg3gxj3e7zwlh3a leaf=2571342 PASS
rondonia  hansen.loss_year                   gwqjctcptr54dqcgaqg5cj3526mpnbf5imb7xaxks5xlo6sdq3jq leaf=2571341 PASS
rondonia  hansen.tree_cover_2000             nald6aeb7vivhcrfeqfubb5imqmhncvf6torh364a4mdohk3lpha leaf=2571342 PASS
rondonia  indices.ndvi                       b32kjvg2cx3vybpnz7cqy2gamlsdqzswmf4r623xg7rc6qfabz2q leaf=2571349 PASS
rondonia  jrc_gfc2020.forest_2020            em2zkl42apqrefwllp7thfe4nptbc4wo6hvkhk3t7km5gcb4gtzq leaf=2571344 PASS
rondonia  jrc_tmf.deforestation_year         z5hqerhd3c32f3zl6u36vs237j25fmzmqexplunaucjal2zkfwgq leaf=2571344 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  jrmavd6qypfrm37mws47cln7soueku3jvaif3mriit5jacce5ckq leaf=2571352 PASS
rondonia  hansen.loss_year                   b7nvgyc2f75iel7pkguar7xtsoqs3zqlgnw6rahbd4k22ap7fj5a leaf=2571352 PASS
rondonia  hansen.tree_cover_2000             xtncnkrgqyysvdknc2jjvlldghi7dy7pwtbasn5qk3tl5662wxsa leaf=2571352 PASS
rondonia  indices.ndvi                       emyu4ym7t4kzzucyh3gzhk64bl6o5m7vnhe6q2ikwkvmcweenpsa leaf=2571354 PASS
rondonia  jrc_gfc2020.forest_2020            gkotjwttls5j6mg5z6wuxgmel2j4wifdkvv5hmh452yr45sm2rbq leaf=2571352 PASS
rondonia  jrc_tmf.deforestation_year         z5nwtbj3zc6dh6t2ogn5hbk43fumg72ks26j2ostijhh2flbhbra leaf=2571352 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  sjq2e5td5vzcgkddwumozalxy57ieyxprd4gdh36ppnhkstxyxzq leaf=2571351 PASS
rondonia  hansen.loss_year                   r2cswumblmdfqskj3xl2gb4m6ywpiuexzfb3s5mcdkljojnaiy7q leaf=2571350 PASS
rondonia  hansen.tree_cover_2000             4lbkrjq2twrhbbnq5ggapuue4pmyyrxu5knn2focvtwx2z66yi7q leaf=2571351 PASS
rondonia  indices.ndvi                       nwbevpkxcw5vmy7hyas3y7zsw7k4xok65yuxdbfeoksimxeewvlq leaf=2571353 PASS
rondonia  jrc_gfc2020.forest_2020            jyt6wlpvsmsv2vq6gijeazc2qe6jd6qburhlmye4zfgju2mmjfva leaf=2571351 PASS
rondonia  jrc_tmf.deforestation_year         nzp6il2lyc5tsiibllmink6llqazvnalt5z2q7szzzub5ufhnyoq leaf=2571351 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  tl3wjuh26ru4jz6nnl2cwctlnhrnv3seyqpbjzbx425qz43yjqgq leaf=2571364 PASS
rondonia  hansen.loss_year                   x277fzuko7ujpz4nsttlxy2ufzruvzjukur5rbcbyvhgiexrh5oq leaf=2571363 PASS
rondonia  hansen.tree_cover_2000             5lm4jdmyqhin625ifggkgy72gglghfgrjif5iqwibfk3mvgslh3q leaf=2571364 PASS
rondonia  indices.ndvi                       3bd5padsxsz7uiabrokiblwbf7fx33ntqhnpvhaa4cikk65tkizq leaf=2571377 PASS
rondonia  jrc_gfc2020.forest_2020            3ltbm5tscx7favmkivq7p7yysjhn2h2d3t3hnd6enkspdjy2trma leaf=2571364 PASS
rondonia  jrc_tmf.deforestation_year         owb67cqdjxkakrjwojvwnjmt7nmhihmx4zjsilvsq46gzi44uglq leaf=2571364 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  tunwbgndl3jjf543bpzdv6prgxmyvq5owo3uuxmu3nafmvkyipta leaf=2571373 PASS
rondonia  hansen.loss_year                   cpkqhhwzswdhl5hoozby5yuxlxrgjz722ctm72lw42swvorjbosq leaf=2571367 PASS
rondonia  hansen.tree_cover_2000             vnzk64uy3abbmso6nts4icen6ncj7shzlbjgvgoebqm6urx6qhxa leaf=2571369 PASS
rondonia  indices.ndvi                       lo7wo3exksqr6637j2mvgfclqsg6uzaundbk6g5mx3m3z4bc2gea leaf=2571370 PASS
rondonia  jrc_gfc2020.forest_2020            cwm25ck4dlyajei2iorkapnhhcexeaek3qlzuofk3a7x5vuyptia leaf=2571371 PASS
rondonia  jrc_tmf.deforestation_year         wtkxxg4mj6klzslwu3pfztlftrqlah3ucoqmk6fta7cusuibpyia leaf=2571365 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  qqxveujtvdn2vlzexof3fpoytj72qsrs2wcfbrya4k5c2ic3h3gq leaf=2571374 PASS
rondonia  hansen.loss_year                   g57fp5emeksub56o62y62t6ddi3dot6e5t2nsriinwiw3bvcovqq leaf=2571368 PASS
rondonia  hansen.tree_cover_2000             fhgfswe5ibx7joxh74nr4sjv3idly5kkwqasxjuwg7iz5kpvnxkq leaf=2571369 PASS
rondonia  indices.ndvi                       tehjd22y7d6ax6nsun2krfqbygemhavryuataharoeh2igv7f4yq leaf=2571372 PASS
rondonia  jrc_gfc2020.forest_2020            xw4gag4lvaxonznk2f6kvuh2i7kefotqbixcyn2ahi64xtnk5j3q leaf=2571371 PASS
rondonia  jrc_tmf.deforestation_year         klw63cqmmg5r3mh6qqzvc7a2jihkfbupsjq456ttuh3yauzg5o5q leaf=2571366 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  2ju52fbwwdxom5qu3r266xtb5lukrg4hoeekj4fwo2qsbnaqhtkq leaf=2571376 PASS
rondonia  hansen.loss_year                   kj7d2ffto2up6iiqfad7hjefspa4hn6bk2cgggxwvdiy4rbwo2sq leaf=2571375 PASS
rondonia  hansen.tree_cover_2000             lvg2xsowrgxqv2psx6nr3tlewaywmb36q5lby5orqmseaiww77ja leaf=2571376 PASS
rondonia  indices.ndvi                       mua7hyhwrwcxuddau33s2rv4apdy6p3562dgogoso47w3okhi6ra leaf=2571379 PASS
rondonia  jrc_gfc2020.forest_2020            3yuils223uoz6lokkifoouxqiyfdczblzyb6luvejhkt5k3ajxmq leaf=2571376 PASS
rondonia  jrc_tmf.deforestation_year         72f3rasu6yp4iaxhkpr5wub5dsqrzsoznd6nmsjqezjlvjdxbslq leaf=2571376 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  vowq7bk5fhv6hjkv54dni6eamqqwppzxfwbzsxvroxikyw26t45q leaf=2571378 PASS
rondonia  hansen.loss_year                   yn46244b7adpkebrdm4qokkbflrdca4hkrw2f7z5t7vtdkqspnlq leaf=2571379 PASS
rondonia  hansen.tree_cover_2000             hywigl24uwrestkraccpyoj5qor52e2da5wmz35sltkvectt6bgq leaf=2571378 PASS
rondonia  indices.ndvi                       bdmwfvhi65b4j7mg66moichpvnj2mugqh446edlqnhl2fzdwkbsa leaf=2571380 PASS
rondonia  jrc_gfc2020.forest_2020            7vgimzgyprjhczu2qadxj5z3ljx6ohiif7s7jcknpmce5besoxga leaf=2571379 PASS
rondonia  jrc_tmf.deforestation_year         f26xis7o34hnhqrtyttrpejvq7gvvswr3juwjy3alofz4ynic6oa leaf=2571379 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  foemgasxknlivtn664cw4j5xwjf5h2ffvhrsuzcym3yfvmrwemba leaf=2571382 PASS
rondonia  hansen.loss_year                   uoggbvknpu25gwm2ickpcivmzh77f64hzqwqyy46vtnqpedr4zda leaf=2571381 PASS
rondonia  hansen.tree_cover_2000             fl627tdmlvqjktqiz5ifjnhmm57qupba6dt2nyjelrtpo7smjf2a leaf=2571382 PASS
rondonia  indices.ndvi                       lojedzos7zqqz3oresfxru6rcco2k4henh5jzu2bzi6mckkx2ewq leaf=2571387 PASS
rondonia  jrc_gfc2020.forest_2020            bhytijzemi255mpzdnaquqfxya7si2gwd4s2u4pg3ow5lca2rlba leaf=2571382 PASS
rondonia  jrc_tmf.deforestation_year         jfa4brcf732suuzgrh54bs7chdracc4kvvwxutv6hnebpeugp77q leaf=2571382 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  htyvbeqol3bfyxudkacrwskg54sp5yrkagoiw5ong2w7yaxilxyq leaf=2571384 PASS
rondonia  hansen.loss_year                   ghb6xtq66ntrfaq42eiwpu7l37mjqxnqjef5wjzg477p53tsjmzq leaf=2571383 PASS
rondonia  hansen.tree_cover_2000             xbtgeqakaszsokcm6e2ym5rpcru7uufihzouv6y76yjayrub3m2a leaf=2571384 PASS
rondonia  indices.ndvi                       opapqxbwgsnv5i346nhjcfpv3ikhda6tc66czjnkjsea4b4i3qwq leaf=2571388 PASS
rondonia  jrc_gfc2020.forest_2020            2nuowz3zr6jpeofcksskkxm3lzoygshjh5xeuo3i4fvur6e5kfqq leaf=2571384 PASS
rondonia  jrc_tmf.deforestation_year         yd74gibypdlofjdqwnbsjki5e7wxamlemobhjop6it57qquazlrq leaf=2571384 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  lwktsfk4dxpgfkysxaqjlrfjfif4v4qf3jjcjztkqwzunqneg6qa leaf=2571386 PASS
rondonia  hansen.loss_year                   xepxmtspmehedqn3qimjxruxzutsumxi2yksmpev6tuga2k4iykq leaf=2571385 PASS
rondonia  hansen.tree_cover_2000             vt6no3mj2vzdzzh54oqb5blop5wg3zpwalxgp6fbjqduak3qtqma leaf=2571386 PASS
rondonia  indices.ndvi                       44xu4luoqjcj3hob5utsssyl24pmsclw63ll2ywu4ljwtwpescca leaf=2571389 PASS
rondonia  jrc_gfc2020.forest_2020            gkzjslfwene26cojjielh3hfn33qa3mcmnufqpe7wlwoy27gfycq leaf=2571386 PASS
rondonia  jrc_tmf.deforestation_year         qn7is6s4zs2g744cod2oh3nz5sjgjsto3qe5l35koq7ujefcjvcq leaf=2571386 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  rigis3s2rwvizndyvvcj2azhtrq5q4sk3w5jxeufy3ljk3tobpaa leaf=2571391 PASS
rondonia  hansen.loss_year                   qrhwll47aqobrptjyiv4ppzcunpcfts7yvktpmmlmphqupln6oqa leaf=2571390 PASS
rondonia  hansen.tree_cover_2000             bzedp34rpjdrijizqkyytgcpzlkyl2qkbydyn567yf55lbq36uoq leaf=2571391 PASS
rondonia  indices.ndvi                       fqgfr6idhvutdhavmcf5x77ukxobqslubm4hcm4rh2etriipj3dq leaf=2571392 PASS
rondonia  jrc_gfc2020.forest_2020            sehi3gwpgjvomphwwzc45iyreeacdunwuzpkgmprsywuyripgubq leaf=2571391 PASS
rondonia  jrc_tmf.deforestation_year         gcq3pvo4vsbl2m46mcjjeqfhumykylgn44r4njbliyvt2mztyd5q leaf=2571391 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  umxkh7zxh7hjkpxtu4ootagm4j2zm3lxcv3jnemto46ziovssyca leaf=2571394 PASS
rondonia  hansen.loss_year                   uaz322iflxvcgtoq7lnbu4uijltyqnrinthmguuth4cjm56kzvxa leaf=2571393 PASS
rondonia  hansen.tree_cover_2000             suvqrv32ff5xlforyyuagnnb6jifnhhv2tvmty6uvmixbh35tc2q leaf=2571393 PASS
rondonia  indices.ndvi                       jwn6q25jkdijkaie6sbivzd6yalmc4hvsvzhgozxcmshsw3tgqha leaf=2571395 PASS
rondonia  jrc_gfc2020.forest_2020            b2ojqgzpdsh7rfkkpmky5dezddfahv4blgmzgufii367gqzsyc2q leaf=2571394 PASS
rondonia  jrc_tmf.deforestation_year         3gplafjocsj2vwvsf4ttui4mrhahwvnoa36vmt33pc7bmnekgqsq leaf=2571394 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  7pyuxm3zx7ayhzq4vmbvvalxz32d25kwljz7n64ukhyinph3ie5q leaf=2571397 PASS
rondonia  hansen.loss_year                   ae2qyvigyco2smc7nhum274c3kw7mvx57blwrx2hyfrqbkmgf3vq leaf=2571396 PASS
rondonia  hansen.tree_cover_2000             nohcg6tyghh32cjolsa22upfnpj2hsbaeyonuud4j67hzilhkuhq leaf=2571397 PASS
rondonia  indices.ndvi                       poxix62jznwpkw36xns7c3qdqhiw26bh44zpkhnicpoj6mxx2nwq leaf=2571400 PASS
rondonia  jrc_gfc2020.forest_2020            sqcv6xujofsteecqfb34blgtpgcbhzbw5mb4lfx5sxgkktsayk3a leaf=2571397 PASS
rondonia  jrc_tmf.deforestation_year         cj3hksmvqhfw2jfulfuleeit5m7n5gxqgqww42ffr52bfv7mwpba leaf=2571397 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  7aw6qddnfry77bpifo57st5of2dkuu6snocif3sozarxvwimcz6q leaf=2571409 PASS
rondonia  hansen.loss_year                   ep6quxxm4iwwk2rxz57visqehj2qlb4ckj2q23d6cfy5wcgs5lfq leaf=2571399 PASS
rondonia  hansen.tree_cover_2000             lwxjm6wdhuurduh2jtfvzr34bzi5kpmbfcyj23loge6yqopxgi6a leaf=2571404 PASS
rondonia  indices.ndvi                       hgwee4o5myleawbqdjq5cf5sxnnq3fhyilea4a2pzvlodcr5ne6a leaf=2571406 PASS
rondonia  jrc_gfc2020.forest_2020            vxxxclbhpomx6srdew4elww22apis3cjncuutxxwamhuk3u2ldaa leaf=2571401 PASS
rondonia  jrc_tmf.deforestation_year         yjkg64db3kobczf2uvxyilr4jiiydx4mcbkikuaojbswyordorxq leaf=2571398 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  yafir5azleoxjvt4ks4fj4q2knnk4pziiw4fkuzozb4hx7xjtf3q leaf=2571410 PASS
rondonia  hansen.loss_year                   wtcjeshg2dosypzdf6flgax5qntbvt3bdfiaoib2f6vyfkn452iq leaf=2571402 PASS
rondonia  hansen.tree_cover_2000             plsov5butqmp32kjwxaglwamgctn3oc6qkep7he5fhfd3e5kehhq leaf=2571405 PASS
rondonia  indices.ndvi                       4me6jux5hpl4bbsceian2462jlosdsscvcfrhj3dtz7irrgmqb2q leaf=2571408 PASS
rondonia  jrc_gfc2020.forest_2020            g4t5z7c3b7n4r35vuteyw77srujg2gfmpuiqhinme23mei2yxviq leaf=2571403 PASS
rondonia  jrc_tmf.deforestation_year         fhwj5hfjckkmwhbhhkfptbdp6ozwn4xmntknwooxikvstnfbutfq leaf=2571403 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  rdy7cqrbbcelyr5kyfbcfmpfi3coe5nazlxknow6bccztrktzyva leaf=2571410 PASS
rondonia  hansen.loss_year                   kheenmazdn7viswiupgv4g5z3idtyptkb3chqdcreqnw7hkj4rkq leaf=2571407 PASS
rondonia  hansen.tree_cover_2000             57p6soerqwcmfl5o776ajo6pcdngwl4i7wuvugklybxmxlrbigsq leaf=2571408 PASS
rondonia  indices.ndvi                       jsmmxrkmulfr4z75ombutfe4zhzye5cweo2bbrnx7wrgntilzk6a leaf=2571411 PASS
rondonia  jrc_gfc2020.forest_2020            ejqpmnk6klihnob2yucyq7qtdvilujcpaej33bhqregsetrubvta leaf=2571408 PASS
rondonia  jrc_tmf.deforestation_year         4462asx6kskngn355uarw6akv7fbx3kafn4qkvghlliz54uyezqq leaf=2571408 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  ersfaqtm6mb3omgrmq2adefbbso2havj64dldrhdun3oc4tl4poa leaf=2571413 PASS
rondonia  hansen.loss_year                   6p4jipy7sql3b7bjoi3wlhfcq2sxmvh5mxtivft5oxiqv735rj4a leaf=2571412 PASS
rondonia  hansen.tree_cover_2000             ww4sz6ism7cdzfoa4u5kxlevexpv7gcl3nad7ak6ojbvhvusxxhq leaf=2571413 PASS
rondonia  indices.ndvi                       rmsf66ivkf5ejilfudc35ybhtfjzdvjevaycie72vnhtrdmtoh2a leaf=2571416 PASS
rondonia  jrc_gfc2020.forest_2020            nuxjxmffnf33nsjhk2ngfzu2spyt2j2faje5i36apthzyenxleua leaf=2571413 PASS
rondonia  jrc_tmf.deforestation_year         xxijsbaszz74zta2lxsupdayfkf5yv2sw5rnmomaxj74u2x4zjza leaf=2571413 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  qhaafhao25oynntwrx6was7i5z6njqpwh2hfq2s2gws5xvmxy6za leaf=2571415 PASS
rondonia  hansen.loss_year                   m4so2tac6vpxx3qayjja7dqcych4fjzkisu2zdw2wxvqebxzl52a leaf=2571414 PASS
rondonia  hansen.tree_cover_2000             3ugrpcvh5hmp45w4cpmtn6dhxyag3gabngihxy46warvett322lq leaf=2571415 PASS
rondonia  indices.ndvi                       nhzkjrtv2hzvpjrk3aicpvw24clk7vwvumea7hv5kc3qykbcv43q leaf=2571417 PASS
rondonia  jrc_gfc2020.forest_2020            76yjntkwdnvg756w343e5dro7u3gozsjpf5d3vcp4q6ubkokgnaa leaf=2571415 PASS
rondonia  jrc_tmf.deforestation_year         u6ocg3hlnblzy3fqrjj2ncffuszlctj7eo4mocgkfrjqxemejkqa leaf=2571415 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  eltbsilbly7ipgin5dua3lnax3ahbteqn7f7j2c2tcfuz6wmdx7a leaf=2571418 PASS
rondonia  hansen.loss_year                   2jw6atk42msyntevlqofrikl7zyqtgxttqcmv2o5qxwzjupaeexa leaf=2571418 PASS
rondonia  hansen.tree_cover_2000             vcztdomo623mpbrimasiymv2rnsdaa5jfcgzti7cjbxm4k4kwppq leaf=2571418 PASS
rondonia  indices.ndvi                       grpsrijheocoszblcsvc3alrwbwxp7fryfqjthhm5atnmuo2e3nq leaf=2571419 PASS
rondonia  jrc_gfc2020.forest_2020            dzveu7tbhyi7gagjlchbiqji2wwvociafyip7om2gyjrxunxgdpa leaf=2571418 PASS
rondonia  jrc_tmf.deforestation_year         dbwrmg63z4hr673wpcimrspm433q67fzytdptt63st2unzbih52a leaf=2571418 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  t67npsucg3ua2ghyoqmlh7ipfgu22aw5uwmtqmoxyz2cnm7oo6iq leaf=2571421 PASS
rondonia  hansen.loss_year                   jqkvrvtn5dtic3nq5jxbdd444hx6y3e22vorapts7sehajtvz2aq leaf=2571420 PASS
rondonia  hansen.tree_cover_2000             td52qcpoxz7476haopdfofcpwx2bd2wxd5nuk65dehpw2x6e3s4q leaf=2571421 PASS
rondonia  indices.ndvi                       ugxbxfcm2tpspnissvf5fuitwgw3gwclicu4wfciqoyezbgh4ikq leaf=2571424 PASS
rondonia  jrc_gfc2020.forest_2020            e3w2r5e7jg6in7ybnkop54xcb5rmu5mxkxy2pfvooneudi42wbpa leaf=2571421 PASS
rondonia  jrc_tmf.deforestation_year         s2mirbpz3fvqtynojsdjtmf3erfx7cu7746sdic5kfutkcperxnq leaf=2571421 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  yc5qjlghl6mwy5kmqggtma64yro6gfjg4poocqsawqwd24wh5uoq leaf=2571423 PASS
rondonia  hansen.loss_year                   6rtcbfumrzhac2a32vkoixocgtel7ws5bxnra2omnrjv5apyfnea leaf=2571422 PASS
rondonia  hansen.tree_cover_2000             iv6mhn5veoaoglxzs6mda62gjjiiadn2cjibfidkqz565oaipqiq leaf=2571423 PASS
rondonia  indices.ndvi                       ojbthm4vcir7q5j3t62hcmbdnxffnvejfn5yzqiwsrbunq32dnsq leaf=2571427 PASS
rondonia  jrc_gfc2020.forest_2020            ncupl5ptbfrz5kgis4swtfrvleqwcln4xvbpjxjaul3ocz3hznoq leaf=2571423 PASS
rondonia  jrc_tmf.deforestation_year         sw4zpem3spflpjnxetuxi6b63u62fghu7s6kufnludfzopd5n6sq leaf=2571423 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  irvogimaszmdiu4vr47dsfen7xifzcjvdqxwylfhikkpgr3zhfqa leaf=2571426 PASS
rondonia  hansen.loss_year                   xpif5ivpa4izsvxwessj6aiowuktfekqitvhm7um2dxdseukjrka leaf=2571425 PASS
rondonia  hansen.tree_cover_2000             4nreu5jsnozgt5n6k6nghjgltjypkdqx2tuqffep4lex5a25jy4q leaf=2571426 PASS
rondonia  indices.ndvi                       27ekymgqw3svs2wir3v6vuohg7icsoxpdsbqgech2j6avybsr3qa leaf=2571428 PASS
rondonia  jrc_gfc2020.forest_2020            5n32bg35wqx4q6y2f2c2khd5jsle7badtuigbj7zmqnujrgew4xq leaf=2571426 PASS
rondonia  jrc_tmf.deforestation_year         hp47zurwkdkbmwlkaoskyebjkiexfdsklaqdoic53ysflzbvgkzq leaf=2571426 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  zvgz6ylcpruhg4fpmokbjl7iq2imiold5n4abszekkhfzwg6osja leaf=2571430 PASS
rondonia  hansen.loss_year                   qadpelgfynuivp27muu4ufgsdmyfdtyixuhtmjooxlyjlu6yleea leaf=2571429 PASS
rondonia  hansen.tree_cover_2000             o64bic3mlp5uf4s5py6slkqoyzyu5gdzkvqa2tsbxrin7dzmk6za leaf=2571430 PASS
rondonia  indices.ndvi                       flhphmesq365cefwmcuh645tu4xdemlntwumkxnbnszivcl5ii5a leaf=2571431 PASS
rondonia  jrc_gfc2020.forest_2020            lvyq4i5ix64yfjujmijk3cx5cersimnc27abhhe22bmaz4kldpsq leaf=2571430 PASS
rondonia  jrc_tmf.deforestation_year         a6bl7ivaoslkno5qkyxmlapa2rfeavmv3a7ynlvdth2l6oulpkyq leaf=2571430 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  bpkgfsezj6gqehe3iscqmqyg7u4avlinosshhiziy26oxmwcucja leaf=2571444 PASS
rondonia  hansen.loss_year                   kifwqeisc7d4o2df7nlajbpcxx4ltcmdgvet3w4u5rvbib2ub3na leaf=2571433 PASS
rondonia  hansen.tree_cover_2000             52gkwq5sbazdzlot53jgptvmyliucoum4aptwb4tfomqqbtg7iyq leaf=2571434 PASS
rondonia  indices.ndvi                       wzy66iajmigtkzzt2ho5uipysxpfkyvf3b6i7jcd6tv4oh7wgpca leaf=2571439 PASS
rondonia  jrc_gfc2020.forest_2020            yoedhv6ql2htjlwndh5trlfgjg5uz7nhb2yhyxw6xskmbib4vy6a leaf=2571437 PASS
rondonia  jrc_tmf.deforestation_year         4all5jfp4tyrlltjhfbbjs64noksn6nzjzxiap6ctlmvtdxdm4xq leaf=2571432 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  twvzpycv5e2xmiuzzex74xezr2oovdjy45ildcmo3hmls7m3ch2q leaf=2571445 PASS
rondonia  hansen.loss_year                   ehfhvcxj7pq22o4i7vaeixf2acls6y3g455kz5baknicfjtcgo4q leaf=2571435 PASS
rondonia  hansen.tree_cover_2000             k2ofmapef4sd376cg4f4twb6rhxaq4dlb7zjdkvt4u3dgrsh77bq leaf=2571436 PASS
rondonia  indices.ndvi                       tmcqqgwfcj7czvdq62kcmtxq77pxlgsu7pgxzed3fyqusm2rhzfq leaf=2571440 PASS
rondonia  jrc_gfc2020.forest_2020            tbmo2faxip3ebh2e5v7kenltuovw4psgda3bsvbfbo4cqqp5ub7q leaf=2571438 PASS
rondonia  jrc_tmf.deforestation_year         jfxu2g4zhcclcpyewormwvs4gb3fsucpsq2pj4tlnek64kn3ae5a leaf=2571436 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  n3lvuorzhnjlwhdxeeavuva5lgrhjcoy4xce3ju7craut7fmqyma leaf=2571445 PASS
rondonia  hansen.loss_year                   ixiafmsvlbloth5zrwjk6f7yluqpwsu2yj75ocllf3fswhuqxy2q leaf=2571442 PASS
rondonia  hansen.tree_cover_2000             k2gotkfhs2mhqbzvp3m4uq5cwcsakzoj3w3n4vtohyiqlrhimwea leaf=2571441 PASS
rondonia  indices.ndvi                       5fdrpz4qdlgg6t7x6i5jpapphmeuahxktdksqpqceh4w5dcmyirq leaf=2571443 PASS
rondonia  jrc_gfc2020.forest_2020            krkgh44oqppz63f3ygrurh7fp7pa7y33teyjw45e3xvyrykl2r2a leaf=2571442 PASS
rondonia  jrc_tmf.deforestation_year         h2jrvu4omtyserqvzsaek3xfzgldusspzm5ch3lq5wv7o2ru7ghq leaf=2571442 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  wlo35mawnmsce6ahwwu26xvrt7mjbzauzb62jwkxszerjr3izcza leaf=2571447 PASS
rondonia  hansen.loss_year                   a6gez2ij7r64umqnfobthf5altwx7ulsdksq7wbe6yym5nzn74kq leaf=2571446 PASS
rondonia  hansen.tree_cover_2000             o2vta22dvl26hgndnrjzznh2nbwi2pfxthw2hgdwq3kppfddcewq leaf=2571447 PASS
rondonia  indices.ndvi                       kob3dc6rv5ihkb4qgq6pdt4qpv4lutfrkctdtovnf4rtax7qnb5a leaf=2571450 PASS
rondonia  jrc_gfc2020.forest_2020            5oeoe65bz3eahxctubdyvji7std4y2cfdcicqmajdu5hxbeafgpa leaf=2571447 PASS
rondonia  jrc_tmf.deforestation_year         rbsd44snyhoxyossaqeepqv4dpraa6x6zz44i5ul6pglhps7fnwa leaf=2571447 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  gjkvbzn6t5b2hdewx4jlz4grpwzzhnfd3llnl64iqd33242aytia leaf=2571449 PASS
rondonia  hansen.loss_year                   5y5lbdnehgcl6pdyxjf2dwgw7udjl4bk2wnpnr2umddjejfpdaiq leaf=2571449 PASS
rondonia  hansen.tree_cover_2000             6pkjqr53zos2qa4sfdbjzeg5cliksatsbj4anlrrq2ch6jcaltva leaf=2571449 PASS
rondonia  indices.ndvi                       qalqtxjmgtvtum3sukumkjfh5bis55snrefd26a4eqvgvzqrsxnq leaf=2571452 PASS
rondonia  jrc_gfc2020.forest_2020            xhphheoy7ul7iw4ni6n6xubqmdauh4mlksubp2an65ki6ig2bp7q leaf=2571449 PASS
rondonia  jrc_tmf.deforestation_year         aohow24536cnckyemnjgycs7qcasklgxnjjamzn3wpof2ijwbsoq leaf=2571449 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  jemaxs46aw5ycyfwjpjsvuhniffownzfnbujpnmll2pvgsbcalrq leaf=2571448 PASS
rondonia  hansen.loss_year                   3nztysvi5cuclzgxitraapx4fhbj4wf7exf62okkva7lmvmobeia leaf=2571448 PASS
rondonia  hansen.tree_cover_2000             yu6cuyw3iem2olxsuphkykz5k2slqirmsu6nbkmpc5kgohdfsrta leaf=2571448 PASS
rondonia  indices.ndvi                       2hs6g43b33c57nsjhsicpeazj74btoapd6r72f76mpiwfsnhjjga leaf=2571451 PASS
rondonia  jrc_gfc2020.forest_2020            uwsmbvp3oqc7m6bg5wvb5h45n5ds7vjk3ome7qew7zzeukl66ayq leaf=2571448 PASS
rondonia  jrc_tmf.deforestation_year         ro56exrydddwwbgyqtofu3aiptqre63zkyqghgtamtnjrnos6hpq leaf=2571448 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  jebyux6zbelskusxwslsfmy736zvbbjar2bhrx62nsbh2c6orfxq leaf=2571454 PASS
rondonia  hansen.loss_year                   e3zoxibd4hl5ugsoytcxselzengcysrcbgtmrtddprlfyhgjdyxq leaf=2571453 PASS
rondonia  hansen.tree_cover_2000             olfrof7ygneds34obgo2x7xfmjsbvhrn73xbjs4n22pbzf3r5b3q leaf=2571454 PASS
rondonia  indices.ndvi                       ads2skuge332pkqekspsp7kgx5ibrboa57cwn5lvp4ucyrgf4q5a leaf=2571457 PASS
rondonia  jrc_gfc2020.forest_2020            eklsm5v6fpmknltr6alr4b44dqtw47gpwu3lfcfw64g2zuwkokya leaf=2571454 PASS
rondonia  jrc_tmf.deforestation_year         loctok5gwdxcdcgekj7qbtaii2gisilbgn6f5fvw44y7xokfc7na leaf=2571454 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  aimwrvl4iu4zwi6p5we4mgnpxa2o7dwidheu4s7eohlhuwa67ttq leaf=2571456 PASS
rondonia  hansen.loss_year                   nbgpcuci2e4oncfdmjaspcji42rpj3hfwaegfhiqhfsdrkcbl6uq leaf=2571455 PASS
rondonia  hansen.tree_cover_2000             oaqmqcjwr3qqxjvedovr7rv242h4dypzkbqqisf3dcvoqr4dwt7q leaf=2571456 PASS
rondonia  indices.ndvi                       3sb3f34a3uwssu27a3xpxxgtzaa2v2tw42lzkjm3ffx3jeu43pca leaf=2571467 PASS
rondonia  jrc_gfc2020.forest_2020            hgdbrvf5obifcia6ecu5n7xaczzmm2hiim66eoovpempwcjojuja leaf=2571456 PASS
rondonia  jrc_tmf.deforestation_year         pquru4o5vsr4tpqhq3hgaghowh5ohm2usdcmsqs2l4zr4z5q4eqq leaf=2571456 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  c3iqggiqnmgr3ibp2zhcn2g5xmrajkt55irlscklrgkvleryldka leaf=2571459 PASS
rondonia  hansen.loss_year                   kn46iqzeqimgrpdostmful63vjpdluh6qap56qjm32aqeje3mrca leaf=2571458 PASS
rondonia  hansen.tree_cover_2000             dthjawupc32rgeszrjjzwt57o74iriigovikn2blw5vswom6kipa leaf=2571459 PASS
rondonia  indices.ndvi                       jitic2ubamd3daog3fijfm7h34sj5hncwizq6in35xw3uchxbvuq leaf=2571466 PASS
rondonia  jrc_gfc2020.forest_2020            gqfxyaxqqipqvp7j6xse74h24brurk7sap425jak3gk52m23rp6a leaf=2571459 PASS
rondonia  jrc_tmf.deforestation_year         gbybdnmdeuxzlbcev4jkggxgixgrat3yuziq3p4smguuw22gbrma leaf=2571459 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  dbtf5uuzvlp6nm6fm7lxce7nvhiztfqkdtpjb46ncbxf53uwmhwq leaf=2571461 PASS
rondonia  hansen.loss_year                   dh7zdv5qxuuwvgjmm3jbte4tdn3yoowt3wyvw5w3coijjlcqx4ga leaf=2571460 PASS
rondonia  hansen.tree_cover_2000             efixbdhqs5md6wqokcsrfnzjb6hreqeh554lrfkrq2hwxgrrfg5a leaf=2571461 PASS
rondonia  indices.ndvi                       lnagjxajiwpjstbg5l6lrjkkd4u5wgwyoeh3a7xjsydtx6ek464q leaf=2571462 PASS
rondonia  jrc_gfc2020.forest_2020            hydgw5i2v3u4vllxc3wdj2b7zkpofeo5n4y5lt57eg5v7vhfycqq leaf=2571461 PASS
rondonia  jrc_tmf.deforestation_year         kjjpzddo63x32qil5jhzxaojt7hyzmdcfzkyrq6r7cyaae5mhxua leaf=2571461 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  d4grgzqwnupj6rexhuynfs44t6szuxnrgwql36gv4y5rlc6b3zla leaf=2571470 PASS
rondonia  hansen.loss_year                   adm3dojsoivlpygymfasggx2nbh23b4rhjmprqr543yvnrytkxfq leaf=2571464 PASS
rondonia  hansen.tree_cover_2000             xpqyrgz22ynnjv7tqmeqizezuctcysxg7efshi5bchqhs2fj4hza leaf=2571465 PASS
rondonia  indices.ndvi                       u3co3kkdpmxn3ss7fy2wta7elok4blxoqx52wgyo2nrjxt7dsj3a leaf=2571468 PASS
rondonia  jrc_gfc2020.forest_2020            pjmu72mtv3kewf4nz4l2n7cjayqadsffrjndei3ruc6ak7pj5gha leaf=2571469 PASS
rondonia  jrc_tmf.deforestation_year         dfqbnrjyqbjy4o6w225wxn5icinuhmih6o73jx52nrffybczztdq leaf=2571463 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  daawcwtufjkbf3parxhdiaglbfb6awefgwglz33boh72aw2neqpq leaf=2571472 PASS
rondonia  hansen.loss_year                   pdsoilf63azih4dafsdqpczwy6dv5vgpufqho4jfhpyafftu4rgq leaf=2571471 PASS
rondonia  hansen.tree_cover_2000             hrbywyk2p7sek7ixjcq4tgdnopkrldwxe7aimufhwbhs3todq55q leaf=2571472 PASS
rondonia  indices.ndvi                       njbxbrabnmbgflz7ulcm6xot5tugk62csydwjncyjmdopmrdsorq leaf=2571476 PASS
rondonia  jrc_gfc2020.forest_2020            hmdas2wcxnylvdwensor6sinsfyt2u2fnmmesdwx3lq2jj54xmrq leaf=2571472 PASS
rondonia  jrc_tmf.deforestation_year         yjkmghj23alqixadkcn3lc7l7jnuktzgdl5atxtcoy6zt2eqcrqq leaf=2571472 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  icqdrqiln24tge4ct4odmm5s2gghk7tqoemk4gdke3gwglvhppua leaf=2571473 PASS
rondonia  hansen.loss_year                   ty5wwf6wefgwmdgcwjtm5dbfrni547ecdx2zwgl4ja4emf5fym4a leaf=2571473 PASS
rondonia  hansen.tree_cover_2000             5urewdxapwuf5usdizqa7h4j7glac47xdjtdtiiyefdagbdslkfq leaf=2571473 PASS
rondonia  indices.ndvi                       lkzva5owxrfgh3h3lrsc6dxze37pi3ndwbkovqoph2uuua2dw3xq leaf=2571477 PASS
rondonia  jrc_gfc2020.forest_2020            mfpp6czygtbfauqqiipcvbvt7ctrfxnrf45cix57w3vmkbjwsjkq leaf=2571473 PASS
rondonia  jrc_tmf.deforestation_year         jyui3ufi3eeeje355r6ses5so6dhoezq5ldkdkmqdvhxn37fvc7q leaf=2571473 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  fueyv7fceqfck5cf5puswt72636vjwv4upkuubrsgnoex57yxt2q leaf=2571475 PASS
rondonia  hansen.loss_year                   4bygxjiwgc4gbb4htumuyleml3h4mk5e5e4cibblbbh2lprbsliq leaf=2571474 PASS
rondonia  hansen.tree_cover_2000             guvmi6fqno5sit46l7lhkmfrdhfuks2rfmxvqsrpap5qwsbfgvca leaf=2571475 PASS
rondonia  indices.ndvi                       a7hmnoo7krcjfuqphksgyqte3ufngflehihe35pbjifmucxewywq leaf=2571478 PASS
rondonia  jrc_gfc2020.forest_2020            zl5pjekyh2urv4rn7pfbkgbdl7idfcab6yyggnb6ih7fhrk3qb6a leaf=2571475 PASS
rondonia  jrc_tmf.deforestation_year         kfqkfga33zyzwcve3py34yw2t6w7s7xdaohmvuyzvxekscfrktoa leaf=2571475 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  hc5gxdeedmsseel3gcdaexa6ntsx5lwublghb4y3ovkxr64dcf5a leaf=2571480 PASS
rondonia  hansen.loss_year                   6q6gyueok33se7r743eb24p6fgdk4cgwi3pdxfzkwpmsjsjkyybq leaf=2571479 PASS
rondonia  hansen.tree_cover_2000             feyc2uwmnxil2wc3glnh3k53rcgkqjgg34ox2wdfsjzjod2a5m5q leaf=2571480 PASS
rondonia  indices.ndvi                       z5dmmkmn5hc477a5cvvd3xtvc3mvd6zqe6klgeccgq6u7voo5i5q leaf=2571485 PASS
rondonia  jrc_gfc2020.forest_2020            2xvjaecv6jr6bk6u3ewnkruxqpqzui65obi3zbunvfuzwzbhmvba leaf=2571480 PASS
rondonia  jrc_tmf.deforestation_year         2ufkyxydrify2n6fdzqoqx5nnqhqwioztof2mdi76yukmmgfs5rq leaf=2571480 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  knnr2fwegmaz3a733ayz3ir5u7f4mnrx6eu5tbmvzx62a77dgfsa leaf=2571482 PASS
rondonia  hansen.loss_year                   vp26v5vqn5fzvm5672zlmswrfe7tb6sa4nbr6tcsq7y6hr72u3ca leaf=2571481 PASS
rondonia  hansen.tree_cover_2000             2ltobikwfgdnixs2w7alczzovlmcff2mrtzrxb6tdk2ujan2resq leaf=2571482 PASS
rondonia  indices.ndvi                       43mlzhdpkyc2egaunw35jwjptxofuwa7s7wzwvhytthkela5myia leaf=2571486 PASS
rondonia  jrc_gfc2020.forest_2020            oc3vr5mvedqr2osud36jczqu7jearkxsixfxqjsmtmesddvtxawq leaf=2571482 PASS
rondonia  jrc_tmf.deforestation_year         x6y443otfcboobll6v6niuvnbb2xtzfudmjpndxst5242jlwcooa leaf=2571482 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  hwbno47nwzpo7otlnfi5oknyge5wwt4gdskcfku53psdkb72f2pa leaf=2571484 PASS
rondonia  hansen.loss_year                   pd7j7rsmuxgddjtlgdgukbrti4xkpkjvm7gifqeqwdl5p74s7ppq leaf=2571484 PASS
rondonia  hansen.tree_cover_2000             sk24sapd7rooljjyw776kafxfacrpjxuclbiyogl7badysqkzmjq leaf=2571483 PASS
rondonia  indices.ndvi                       cte2sb5qouigekix4a2hxlfriljhswkdlt4lqrq324duunxconpa leaf=2571487 PASS
rondonia  jrc_gfc2020.forest_2020            qmpzawwawfbtbwvso2nlyia4xazzmzyeq3fdo3it4ywtw4gh2m6a leaf=2571484 PASS
rondonia  jrc_tmf.deforestation_year         bdo7jqph3y6romv2oe4n7wysxmiqfavkhu7fehy3xork3lwhfoaq leaf=2571484 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  xxuhqjctj55dcsc3d4ftojywra63heodyrebwwf5k2elp2cvebfa leaf=2571489 PASS
rondonia  hansen.loss_year                   m47mjq2mhe5as6uhu6c3h7pqzdr6s3vxlujoxwd4rq37xbpbcroq leaf=2571489 PASS
rondonia  hansen.tree_cover_2000             qx2bh2icixqypfxxqu36ddm5zqlf332se44uuyv43pxkqy46k32a leaf=2571488 PASS
rondonia  indices.ndvi                       5xtiyge6fmjkkkkhgmwicfgqgdseyolpyke2ghr7vzc5vabzczka leaf=2571490 PASS
rondonia  jrc_gfc2020.forest_2020            b4cuwsun4yumux4jwsrslxi3ifsrn6u4q3yza3kyx7ido5axb66q leaf=2571489 PASS
rondonia  jrc_tmf.deforestation_year         tlcjqes4v7reypwclqflz4cgljjtyzqyrhu2pp7lnj2pklxclaca leaf=2571489 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  3mg6htc2gefqy5bndqmpo6cdhyzucmg6olu43emwtgoese3ya73q leaf=2571492 PASS
rondonia  hansen.loss_year                   oiu5g7xg2hnokz25sjoxagm42m7wodcb6xemhxrmokpol4vtu2va leaf=2571491 PASS
rondonia  hansen.tree_cover_2000             wnvi7ze7ang6esfx5krspj67xrdzstavtara7hrs5ol4c73zdlsq leaf=2571492 PASS
rondonia  indices.ndvi                       2zmm2wnhjwxjmtjiutauasmnhnaxl67qxchmqdxo7pv4u737jbuq leaf=2571495 PASS
rondonia  jrc_gfc2020.forest_2020            v6dyr5msnzspzl3ltoondbzjyux5n7zpcxel2ulxdrnnevr5ekra leaf=2571492 PASS
rondonia  jrc_tmf.deforestation_year         kctwxvywmkvss3th4p5nvi4ataymfa737jxl3b2zogrenhcp473a leaf=2571492 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  tdsv42dvik2wrf6otilf3kvycfwcgvvvsqikriar2mpqplmtpvna leaf=2571494 PASS
rondonia  hansen.loss_year                   q6kdudkgxrg72ta63pskifdxrkziddfycejuoucdrgtu3dlsmk2a leaf=2571493 PASS
rondonia  hansen.tree_cover_2000             3pxiboodvwa3zs6o2rd3genkn7jq3adnea4zuglagncq7dgyk7cq leaf=2571494 PASS
rondonia  indices.ndvi                       t6yg2vqjq77utekoeu4k4zgtvsxyak4v5fykmp737whmgeijjmyq leaf=2571496 PASS
rondonia  jrc_gfc2020.forest_2020            y7nnrsdpfpjw55sfbktnygl3wlqth6o27a2ot5zt63irj2u4fcxa leaf=2571494 PASS
rondonia  jrc_tmf.deforestation_year         qmwqx5hrdv2x67zgnrc5kkyrjijxsr2q5lycfuvi6flr2jjvadbq leaf=2571494 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  wacnge5ydniydxr4zsfnlrtsvwmwupnpwyytywxxj6s6mm4rxyma leaf=2571507 PASS
rondonia  hansen.loss_year                   a6macpsgaicvwa3h2cgu5og5v3o7bxn4uoaw4oqmliepqydghcwa leaf=2571499 PASS
rondonia  hansen.tree_cover_2000             wmf2hxuq55hoedek6wktqqxcla56ousy3d4swd5wf3rixq4xevbq leaf=2571501 PASS
rondonia  indices.ndvi                       mc6lbth2ib6zqp2rnddhiynfhu2nubs42isvmilm57m276kga2pa leaf=2571506 PASS
rondonia  jrc_gfc2020.forest_2020            5l33xj5yyqp2brqjy7lhscomthb56uetlzqg3v3xocvbj4ho7mxq leaf=2571504 PASS
rondonia  jrc_tmf.deforestation_year         4l7knygsgxqqyj4gltz42afq5xg4i4hlzpyjo3u7f2yivbkuelga leaf=2571497 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  nw5goivq2nbrenpix623va33oylnp36pooqr5dkbnlsgj3ggpsmq leaf=2571508 PASS
rondonia  hansen.loss_year                   knuau4ll7gshtjelnammwpgvvaf55ptgmqrekrvud4ltnkyuovda leaf=2571500 PASS
rondonia  hansen.tree_cover_2000             rqlviuwmyno4snrzxwqd3vmqwjyxz2fevmhmzb3gyd2u3372iwza leaf=2571502 PASS
rondonia  indices.ndvi                       7uuoavx6f5siwahat5fgiaui54i4curzohabbzggf7ozpwcw4ada leaf=2571503 PASS
rondonia  jrc_gfc2020.forest_2020            gocyqwywegnjwiukutn6tvkzhitsc5jqmcn246wydspzondtp6eq leaf=2571505 PASS
rondonia  jrc_tmf.deforestation_year         7jpolcaypc6dzlutp2547u252vx7ggztophwknqxhlbkbntnnodq leaf=2571498 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  vrc56bjtw4i23uifpy6hufcex3fno5gbdx7myvt74bj7tqxlgdza leaf=2571510 PASS
rondonia  hansen.loss_year                   bfswv7ai73kvb7idqzzyj5khn3qj62qec4bjpb5ugnyup7d6ghgq leaf=2571509 PASS
rondonia  hansen.tree_cover_2000             fmbrzckqvcyqtb4tumyex7b7fdlbbw7zn542cblk2qs3wwakpnpa leaf=2571510 PASS
rondonia  indices.ndvi                       w2kpqsuakrgvk2jzda6aydeckw4lmzhlhuytamld2pqflxx6dnba leaf=2571513 PASS
rondonia  jrc_gfc2020.forest_2020            km6kj2sioyhrjkuj2izrhiyyr7qubpsi43yqfop5xknqa65cx5ma leaf=2571510 PASS
rondonia  jrc_tmf.deforestation_year         wdp67i2zcykswa7ycszovgvvi3st7ue6kzauh6oz7mk7kjx4klya leaf=2571510 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  ybbppwdp3tyjv3kkq5vrar7y5gdtuuh6t6hn7cci7mklydqbmg4q leaf=2571511 PASS
rondonia  hansen.loss_year                   wdox5xhmiyycbswepfuow245vq2mlgkz4w4mbkqvqniqggrqnycq leaf=2571511 PASS
rondonia  hansen.tree_cover_2000             7wjzbfhyo5c5av2so3xlopdqslyzna4w6dxk3fxlgvdhqicdi4wq leaf=2571511 PASS
rondonia  indices.ndvi                       tjgky3yrifqv7ia3eiz3bb4jqarkfvkily3rgzc3irlb4a4meepa leaf=2571512 PASS
rondonia  jrc_gfc2020.forest_2020            m43suphldxmbbpz6gwu4rm2szaecelrbpw43bdswo7fvkb422jda leaf=2571511 PASS
rondonia  jrc_tmf.deforestation_year         cfqnt7vtpyzdv5nararmsu7vlk5xec3cdafmsfmr73ll7xqk2oza leaf=2571511 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  zg4y3i5jkad6z4wvewehr5hsvsdb22stsboqqasyl2mksct6ljpq leaf=2571515 PASS
rondonia  hansen.loss_year                   zmsfuvgecw4ll5e2yg5nizofceqgnub6mudlruuxwxyzsaupxfya leaf=2571514 PASS
rondonia  hansen.tree_cover_2000             khf6squ56donqj7unl55mnwvyyxjtu4rwtkwrmciou2zjullqwpq leaf=2571515 PASS
rondonia  indices.ndvi                       jw62hfca4joeaulz2ho7ermpq24intayrrks7vtkhso2lffbqoha leaf=2571517 PASS
rondonia  jrc_gfc2020.forest_2020            r5zhps3xfsrcxxmkrzdz3433ymaob2znlzfealuykjwbhddzfzaq leaf=2571515 PASS
rondonia  jrc_tmf.deforestation_year         nvw5bdthbmeleyeuroyclvi66g44qvipcpce7637lvbrfkfcziwq leaf=2571515 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  4iaqz4meaxllmmbqckrmuvevlfrk3scwnfoi42xag24iqme24stq leaf=2571516 PASS
rondonia  hansen.loss_year                   s7gdnidt3cf3p2hbzh3hsaf2amqhlw2nwnjcbxqmewkzzvgj4wda leaf=2571516 PASS
rondonia  hansen.tree_cover_2000             j5osvjtzvitw2g4qlw23cqz6jnf5n5dtrbnn2eed6rgbc7utvnta leaf=2571516 PASS
rondonia  indices.ndvi                       3p2k3z6crnwsxj3oqgp5b7c4rhkifcy3wpsqjlj4tq4lhvpbenzq leaf=2571518 PASS
rondonia  jrc_gfc2020.forest_2020            mbiqwr76cjgluy2dydipwehziwuy7yxt3onq6xql2ngscsbq6gxa leaf=2571516 PASS
rondonia  jrc_tmf.deforestation_year         g44yrfw7qbgxvwbe3vmjnlwfsl5pgp35tmilpaz5d7scwdabfq2q leaf=2571516 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  npilod6yilhitiphnhjsiism3syu5b4m2dmcjxb2bh6w7sw4y6pa leaf=2571520 PASS
rondonia  hansen.loss_year                   n427537pgse5namingpeosnx2g4n4tpwwovpkojtbftxhhwgijqa leaf=2571520 PASS
rondonia  hansen.tree_cover_2000             pwrui2gbixsnejmfr2e2tgipvnei3pzui4ty4sswpbdepq6og2ea leaf=2571520 PASS
rondonia  indices.ndvi                       hrodl3qgm5g2evfrww7afnjrxszjrrny2acfizb3lsmgblym3fra leaf=2571522 PASS
rondonia  jrc_gfc2020.forest_2020            d22pile3ww7r72v7f75si2b7pwi6ppyifege3tumj6gatvvceuha leaf=2571520 PASS
rondonia  jrc_tmf.deforestation_year         5f37foomuo4feks4xgaw4q75ltptxrrtgcjx4xaslyk4j27jblea leaf=2571520 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  z7xe5dvxgzxwdmvrblsz4ygcnoxox454z7kls7flj3aiwjikdcpq leaf=2571520 PASS
rondonia  hansen.loss_year                   q3nxl3abq7242ir4ylpvnyfxxetmyqed37limo2hzmwjnrnz5goa leaf=2571519 PASS
rondonia  hansen.tree_cover_2000             jbjlmttdm5722pxu6dj2apgtfwl3mbsrgcr3rb5rdhjiodulbdcq leaf=2571520 PASS
rondonia  indices.ndvi                       7su27tgq3ilnra75i5jp5i5pss3gai47znar346i2sdq6s4xouiq leaf=2571521 PASS
rondonia  jrc_gfc2020.forest_2020            xjb6h4l7q2dxdnkveqbhej666a6iemqaphdvi6ovl2cvssyivnbq leaf=2571520 PASS
rondonia  jrc_tmf.deforestation_year         rombn6plvdj3l7nf4nvpeqk42yohwwrxbtzj4dzjltlblbcoyhqa leaf=2571520 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  ksah6gizcpae3sac45zvdfqowv2szurr6qwtyjq6dvwxaq4axezq leaf=2571524 PASS
rondonia  hansen.loss_year                   3fgewqpo46ghk2v7l467ayxmlfluvnnzvwpskx36rqjnvvgtqy6a leaf=2571523 PASS
rondonia  hansen.tree_cover_2000             uiodopteiwmom4yjfcvup7sfr3s2uvdte3pyzniokt5bqb53ddya leaf=2571524 PASS
rondonia  indices.ndvi                       i73cdiaer7mdttxql67lt5wr76gukr4kwryooeqkjiggg7knegjq leaf=2571525 PASS
rondonia  jrc_gfc2020.forest_2020            rt5hxa4mkz773kfyj6lo33hewtxyc6ewbeqf43wc24lyz6zrck6a leaf=2571524 PASS
rondonia  jrc_tmf.deforestation_year         jjfvvaigdtqngcy6flx24i5xtybataeqw462mfpbaslzkewj3xka leaf=2571524 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  xa27of5vcnifp7yhc6tm335z37ufs6bmjrryogfflzux4cejnala leaf=2571524 PASS
rondonia  hansen.loss_year                   lvctugeue7zfef2k2kwedt5cd7cpf6qe4rzpftdcze3dvly7cjiq leaf=2571524 PASS
rondonia  hansen.tree_cover_2000             wjhqgo3v6sy5o32jztmzwwmcjmc3q2trpv2ptmecalekpaqxaj2a leaf=2571524 PASS
rondonia  indices.ndvi                       inlf3geolzvxkcyrbmfrxfvqf7lsxnn3l2k2kkoqhtpryrxcsipq leaf=2571526 PASS
rondonia  jrc_gfc2020.forest_2020            dxbjohvk5azpvzcebz6s7g6kthoxrr4yz22ms6ddl3uynj44bowa leaf=2571524 PASS
rondonia  jrc_tmf.deforestation_year         r46s2hhubkhkmjjxc2b22ht6pkopfknnsqgzfro4k3jkmzykwyqa leaf=2571524 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  cdmvqsn6gbjcmx6ytpfuk33wnb472ihjvtppxabuqy6nn4mk7ccq leaf=2571535 PASS
rondonia  hansen.loss_year                   qplyxp6mabr4ukuiwknnlrmuzpzcoyuvbmqpuuhx7cbc3zl5baoa leaf=2571531 PASS
rondonia  hansen.tree_cover_2000             jhrqvkq44aoaez2uon2eoxqc7rbnxwbzb3rr6sfzrooa34jsqbga leaf=2571529 PASS
rondonia  indices.ndvi                       io7me2uoxqwlnbhj7x2wk3trgyywurov54ly7gl36ljof464wkyq leaf=2571537 PASS
rondonia  jrc_gfc2020.forest_2020            yv3fczehkjvrf25ihi7cl566lds5625q4jby4i36ybkmls6daxtq leaf=2571534 PASS
rondonia  jrc_tmf.deforestation_year         jsyp7ksgyywatqtapvzit4aytwwun6j4i5byntzv5rog7j43a5va leaf=2571527 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  if26qxphhei5s7khgcaqjev424f44ralnb5u3avrzxprtdee25sq leaf=2571536 PASS
rondonia  hansen.loss_year                   bksloehpgkeud2yrz44i3y6hpeou5iod4nctprqzvaisb4fdwvka leaf=2571532 PASS
rondonia  hansen.tree_cover_2000             umozb52xkltdmhgjah7dbbju4dg3jvnpijxcl5imig6b4t2nx3sa leaf=2571530 PASS
rondonia  indices.ndvi                       g253wuvn7ujt47sghpb4nepmfq7zvajznyrzm7hcbuvq4vsetr7q leaf=2571533 PASS
rondonia  jrc_gfc2020.forest_2020            ca6pfqxl6bujaolvgmhfiwsuxtr2u4c6vv2f3netomsehrcpkaca leaf=2571534 PASS
rondonia  jrc_tmf.deforestation_year         isvgvltmvlgz3uwwfmqugauukmbyyat7drgxiqy6aaag2iadwnrq leaf=2571528 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  t7mgalco7xknuszqermmjgh4tbafm3iq3o5y26gzeruvqby4kvia leaf=2571539 PASS
rondonia  hansen.loss_year                   nksyeajox6rc3fclfdgdfdxmwcnnfzvo6v57ryktnpia5lccekpq leaf=2571538 PASS
rondonia  hansen.tree_cover_2000             blri4o3kbfsu343kumlcyxmz3gfojft5b7yrfcbevpuamvaqb6xq leaf=2571539 PASS
rondonia  indices.ndvi                       2n2y2ybigciobhjks7b6fagrqas3jfapwjv35wd26mwc74wwhrxa leaf=2571541 PASS
rondonia  jrc_gfc2020.forest_2020            iit6vml64euvmotc75gfecj2b5yuy7ztz4xxmiymm2kxk6xp3fga leaf=2571539 PASS
rondonia  jrc_tmf.deforestation_year         vol64wmn2q5ckgaplmfzegmi5tzynymksbfhvrzc4otj7xbq7obq leaf=2571539 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  wd7u2v5fnatshounxx3pswoyygzwvz42sqo3dgecsqanyf2r3v7a leaf=2571539 PASS
rondonia  hansen.loss_year                   ettw5njk76z7m24xu3iakcoz2prb43yr2nuudvkhccfoufebnvza leaf=2571539 PASS
rondonia  hansen.tree_cover_2000             lnb56aidrivjpdv4vqvwgtvmmjjxujeawqe5nhpip2hy4urmajdq leaf=2571539 PASS
rondonia  indices.ndvi                       gfj2spxel5tazkqgplpe35alf2xgen72tl3uxgdf3fk5dnh2itdq leaf=2571540 PASS
rondonia  jrc_gfc2020.forest_2020            myvbgoxb6feeburx33icakbytvj7deag2bvpxdn7rzc4ri6bbvya leaf=2571539 PASS
rondonia  jrc_tmf.deforestation_year         ups3vxxpipkhxhqlj35us4rvesyayg5jypgoox7rwddkunjliayq leaf=2571539 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  yicg2pzhp6qembupt55sil7wzucblzqtkm6iyeg5mrddmsq7yjma leaf=2571544 PASS
rondonia  hansen.loss_year                   zjxe6nv62zvna2sh6kpr4h3lagcapachvfimfczfo7u63kgdy3xa leaf=2571544 PASS
rondonia  hansen.tree_cover_2000             ddb5r56vyi2wlcpgd5leeuh6r4rcwnefhsktq6o2a3orln5cx2za leaf=2571544 PASS
rondonia  indices.ndvi                       bxkau4vop2usxr3dvowkcwte46wtrci4q2al7pcksvdhalz72hwq leaf=2571546 PASS
rondonia  jrc_gfc2020.forest_2020            axr5jvxsswx6s6fcbefdz6adpngpwq4hd4n5t5amponhybj7esla leaf=2571544 PASS
rondonia  jrc_tmf.deforestation_year         rubi22rfupooevmmbe4nzoyurdeda7rs5jelmoztwbvaf3iklwka leaf=2571544 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  ueucf3gnhd6wld3lnf5wn63fjmakafav5l3smzzsp7n2sdh23mfa leaf=2571543 PASS
rondonia  hansen.loss_year                   uwflm3z35jeiqgthwsh46lcy45hf6ggiqwsz24ktbjgkvnv5k2ka leaf=2571542 PASS
rondonia  hansen.tree_cover_2000             yg6cdvehf5x6a5qr7xvsifzvcca5iaaqcfdgen2bpkaws3wzu4oq leaf=2571543 PASS
rondonia  indices.ndvi                       a67mkfgjvqd4nablswu2vomtmnbiyo3cphpp7g2hkrcde5wsbw5a leaf=2571545 PASS
rondonia  jrc_gfc2020.forest_2020            6f6a52nvbh5aqgp6ydr753rhh2lhvupw72bbnre2wo5ddujc57fa leaf=2571543 PASS
rondonia  jrc_tmf.deforestation_year         afcry7bfi3vo4imhbqflq6hdhtiuhesu4aqmv342majrb53wsqyq leaf=2571543 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  gzp47sljyv6es6govbeiqcdlikyaa36tqivqd34amscaf7i7l4lq leaf=2571548 PASS
rondonia  hansen.loss_year                   7pkh3rsr6kxnvn7mmzr7b7xh5thfj6nz267e2723dgn6ervyksta leaf=2571547 PASS
rondonia  hansen.tree_cover_2000             b4sh4mh3afcly6aohggpp4tknyp3hdx4ywiisubvqzmfx4js3ahq leaf=2571548 PASS
rondonia  indices.ndvi                       p2lybugmw5t35kp5fihn3kkfzwqz2gtoz5hfnuqrlmgy3yyhotea leaf=2571551 PASS
rondonia  jrc_gfc2020.forest_2020            3jzaho4hvl5m4ozvklizcwqxjvz22eqoeld6akgkfb3om7ddxdla leaf=2571548 PASS
rondonia  jrc_tmf.deforestation_year         v46vlr3zobstaiepohhbffme6cvqjx2ubduwim3wsos2kx7qkypa leaf=2571548 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  tkvpbqe5kyojfq2kgkmhxn7by4su7snr56dtrlsrli4xltimn4xa leaf=2571550 PASS
rondonia  hansen.loss_year                   z644t6kfjalvjo5uin3tn5p2jwbqymst6wpxay6xj7ysxppjtota leaf=2571549 PASS
rondonia  hansen.tree_cover_2000             src6yaw3a4aga7tldgglfaqm6c3pcyuftsgkl5z4nz6r2zmscdgq leaf=2571550 PASS
rondonia  indices.ndvi                       eqbgcy64iej56inbyie7pdsw6jvlmuk2qf4spkf5usknowk3vjva leaf=2571552 PASS
rondonia  jrc_gfc2020.forest_2020            aisc3mnspscdg3jijht5joq5un5q3p2ytp46fsnmhyc2a62b7dba leaf=2571550 PASS
rondonia  jrc_tmf.deforestation_year         gzyotelmfkn7xj62gq2zxp23lm55sm2sxoptwqniw2ltr6jovqea leaf=2571549 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  jyt6kr43lybf54fubtfqwfxwtgwoxi6ctjg3rrvvx7yw3lsiclsa leaf=2571554 PASS
rondonia  hansen.loss_year                   6pidorrwl66kjqv4pub4ozu7gh6gjwf6wqt7fkclrk6kb5v2fidq leaf=2571553 PASS
rondonia  hansen.tree_cover_2000             lptpoqb3fd4dm4nfwrmgfidfvubdvhqip4pzurjsamt44pgrc4cq leaf=2571554 PASS
rondonia  indices.ndvi                       zokmbqxipnjcyx2ewc7kv26il4bu7goswsb4zdtxgbky5g5tfulq leaf=2571557 PASS
rondonia  jrc_gfc2020.forest_2020            vsqdi42qxmmwt464icn6amby7tkhpuv4ks5hjdqainz2csw2u6qq leaf=2571554 PASS
rondonia  jrc_tmf.deforestation_year         s4eamvmb2ph2va44f3gthrljw5bdlxwhp6zmrizhznqywcfyvmeq leaf=2571554 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  jkvwxg4e2mjbtdevgzhdziqg7mby465gfb3gz5wmr76q7quiwnoq leaf=2571556 PASS
rondonia  hansen.loss_year                   rhta5h6rtcqxygv7c34bvdnp4h6zq2ieikqpazfeptopuja5oirq leaf=2571556 PASS
rondonia  hansen.tree_cover_2000             y4sdgu4mi5utfuvapuhu3jshjclxsxtp5dptcgtvll67lx53hgja leaf=2571555 PASS
rondonia  indices.ndvi                       4hhy33ny2x5wzd6qamveqfj7w5wmeixhtghyfangjnae42v77j7a leaf=2571558 PASS
rondonia  jrc_gfc2020.forest_2020            wh6xdo2x2ddxjcj6ygqoe6pcxu74zpmy46i3lcn37nlfxyprn5fa leaf=2571556 PASS
rondonia  jrc_tmf.deforestation_year         jd4ab7cbm5cma3pd7cq6wtpcsydebhwbnwxcopd3psrdguq2k3dq leaf=2571556 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  aczapwu4p7w7ce3hcyhuv3gwuhassili3bf4tv3udav4z64b2ypa leaf=2571566 PASS
rondonia  hansen.loss_year                   3wuciemtzfpabdt3kudazfuyehwognv6macbdgtpr53e6s4s4lxq leaf=2571560 PASS
rondonia  hansen.tree_cover_2000             prmo3djcmckw5f6txbpdwuba4o6qeoq552tqxculawhr45x4gsrq leaf=2571561 PASS
rondonia  indices.ndvi                       zoc7g2uldvzbyj4asbdslp2ifaeuscr6si2ns4726533pgnowpyq leaf=2571568 PASS
rondonia  jrc_gfc2020.forest_2020            et2ffhilkr4xurscyjeggbj2a3i2by4wtq4dqdwgfjik5cy6ffca leaf=2571564 PASS
rondonia  jrc_tmf.deforestation_year         6odyskw43ikp3nkwq5b5pjl3sojo5pfwqbeshso26dxr62ag6zra leaf=2571559 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  a3qw2wogjj7n3cau5idyjeusjd2ekdhnh6e46ybb4urrbe3saqfq leaf=2571567 PASS
rondonia  hansen.loss_year                   yv3pmulfc66caem2d4gwpvj5pcijngiudqdvpssx2lo2ypnpospq leaf=2571562 PASS
rondonia  hansen.tree_cover_2000             5p3d6eth4bof3mg2bkj7chx627yzzzri5c6ofsjtdxad3pzm2hnq leaf=2571563 PASS
rondonia  indices.ndvi                       dooxwkl6lzav2lqvjw7ncxeu2ekbnzlaj7c4d5yyxf5wllcyvhqa leaf=2571569 PASS
rondonia  jrc_gfc2020.forest_2020            grcroj62hxdvizkjr4ntgd3rcnk2cip23rykwirkb4t7fx4t3sga leaf=2571565 PASS
rondonia  jrc_tmf.deforestation_year         qmkpf2fizmwr6i47qcku6qmhidqxkh2kwj5ffezzi2q42nspi54q leaf=2571563 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  bpb2eztfshod2qs6jsqyvby5irggbeianrybprcpnoqf62wyqz5a leaf=2571571 PASS
rondonia  hansen.loss_year                   gta2xpufwlhqcjimn6uswk7hel5fb276p5tpkwgzxvnamhb5dhda leaf=2571571 PASS
rondonia  hansen.tree_cover_2000             tb3dkvmov62ehxrbdkv4ervp7nmwlucjxpi6gjxemuyf5uwtigua leaf=2571570 PASS
rondonia  indices.ndvi                       tdsxm4lnkiwh75adnkqfssy6me62jeiqpdyvk5udrp5d4jwmivqq leaf=2571574 PASS
rondonia  jrc_gfc2020.forest_2020            p23oobvjv4u7n5nxrhy65km6z6ycw4qq4dvawxbbclmalcupjrsa leaf=2571570 PASS
rondonia  jrc_tmf.deforestation_year         3mz43gwinylmalte6k6bbzzespkey3hulbmxfz27gdtcwcef4oma leaf=2571571 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  qglaglvrdiqvpkfi3befuhdetpgn76pwx7tan6x2nhaivu5mtctq leaf=2571573 PASS
rondonia  hansen.loss_year                   b4mj5qzb2tgesqaz3i6sstjcauu7uqrxi5xgfgortdsi4hgv5uwa leaf=2571573 PASS
rondonia  hansen.tree_cover_2000             kys36aoctypx25izjkkdity6v3zl6w5ddh262p3v4sgljcbr4ziq leaf=2571572 PASS
rondonia  indices.ndvi                       i6jfrkjdawiijcmt4c7dc7lladcqp4zf4sebxake3zlpr53jmunq leaf=2571575 PASS
rondonia  jrc_gfc2020.forest_2020            e43znmglzppu5e62l6nn44sppctyzzxcb2xdvdlwvypk4ndzex7q leaf=2571573 PASS
rondonia  jrc_tmf.deforestation_year         cv2d27od2cuqv2yahs3ttsv2x6n6367mypdvfweqdcwg7e4cu7ba leaf=2571573 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  cutzvcnnzvp3g6xqfuxmnn6aplfnkd7w3643l6laaibqmfvn5pnq leaf=2571577 PASS
rondonia  hansen.loss_year                   5z4g2wccxfsie5qda6fqjpx4bgyzqtwjtz2hdlk5t3xvbmffcnoa leaf=2571576 PASS
rondonia  hansen.tree_cover_2000             vdlczleapoq56wh2h2gtibdcsi44lxdm6p43oaqxwcmpzzu7y5ra leaf=2571577 PASS
rondonia  indices.ndvi                       hjtesrc4xderhf5gmt376apskrwhlfaumobxnpyysw6whojxwucq leaf=2571578 PASS
rondonia  jrc_gfc2020.forest_2020            cmkuuazfxcsympqolqkqj7xzctcksty2znspzeekeyjo2vbt5pzq leaf=2571577 PASS
rondonia  jrc_tmf.deforestation_year         pzxxut7klezgo3izjqty5unz7fxwozwtwrp3mpk6kduo7x4ifvqq leaf=2571577 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  5cqul2lqdtofnd6tavf7i3xfiavash5rgnw2zvbxanayui3oepgq leaf=2571580 PASS
rondonia  hansen.loss_year                   ok4duknhk24onos3h2l22qb5ckb2svspgcisrry2lmnnb6qdmmvq leaf=2571579 PASS
rondonia  hansen.tree_cover_2000             qpzv7o52whjibfmqbus7v2kxmjduoaungo463pa2wfuhnhqsfjxq leaf=2571580 PASS
rondonia  indices.ndvi                       bkomquwxaik5bcfq5utzbsiriws7jbmvu27g4h2wmgoivsagokda leaf=2571581 PASS
rondonia  jrc_gfc2020.forest_2020            6ruqjvc5zcxg3d65kkkg5r6qowgarsarx4wupuzyhyccmuk5bbrq leaf=2571580 PASS
rondonia  jrc_tmf.deforestation_year         d5vsug7ew44d4tow6gkhcsrholamgqk4ufaa7xhdpr5ke6kurasq leaf=2571580 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  f2hncpdce5jj5ydizubdak7mytsh6boinqnizfwheh53vsq7xlba leaf=2571583 PASS
rondonia  hansen.loss_year                   feovuzvsyxvle6rry6w4gjz6vilaprwqoccrkl37uhqzpapuriia leaf=2571582 PASS
rondonia  hansen.tree_cover_2000             ddrpe27dtzt7ponxdxrehu66prkqiemiypxklkqyzlxprss3nh2a leaf=2571583 PASS
rondonia  indices.ndvi                       kksvicnihray2n3imp7evye5i25zv3iupvetpbj7wmi6g55siavq leaf=2571584 PASS
rondonia  jrc_gfc2020.forest_2020            5v6sjvaovw6pvmcnpljxyto6f6g6xx5qvaiaftozx74o2la7iyka leaf=2571583 PASS
rondonia  jrc_tmf.deforestation_year         dospps7zdizqsb335ckckhre72iemvo36x7wx5kopfi2cjm7hzaa leaf=2571583 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  pz2gfie5sw3pokj5rijmlle6voaskjxu6d5oh7aqw44g2yxj3jpq leaf=2571586 PASS
rondonia  hansen.loss_year                   dibwxbzjxdym722iqwu4b2m3rndizocryu4gf22suspdf6thtaya leaf=2571585 PASS
rondonia  hansen.tree_cover_2000             e3aodiwdkcq3ingvqfwzk72hmsckqaoa7cxqkynhcjzqvbvlz3iq leaf=2571586 PASS
rondonia  indices.ndvi                       5iwtd3diyjfpx33zr2lcszozncc52np6p3utvh5pvyqiippuwzta leaf=2571587 PASS
rondonia  jrc_gfc2020.forest_2020            xtgcxyhn6tigrgyaa526adq5yx3zomfenotalk4xadet3uxxvnoq leaf=2571586 PASS
rondonia  jrc_tmf.deforestation_year         d3q7qehkewgiammyuiln6hmuyites3kq5xtflcaldp2b2upgrgaa leaf=2571586 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  ke5iw42yrmavirh775c2oqr7tq6zzdzekfkalmhb6c6ewtxx74eq leaf=2571589 PASS
rondonia  hansen.loss_year                   e6y4ta3zp2mtcp5yhk2pboswqiego53wtm6k5q73lt36lihpfscq leaf=2571588 PASS
rondonia  hansen.tree_cover_2000             6epg63qkuwlb4egfs3hstsez6wwygx5ehqbc7npv7mati5pfsuda leaf=2571589 PASS
rondonia  indices.ndvi                       bixnvsxwx6qfsyripiaodrp3extd3n6grwlja524mar6cfdibbpq leaf=2571593 PASS
rondonia  jrc_gfc2020.forest_2020            nihoz2jkhlmygl4fj76nbpmqp4ej6r3y5s554svbgrdleqij4ala leaf=2571589 PASS
rondonia  jrc_tmf.deforestation_year         wiaxxtszenjpkeh75ovis6y4ybluwscp2itx44hqbqhszrukbqha leaf=2571589 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  an47cqs6ytl6mhyz3ojahiaecjpn5ehkoc5abmu42mps26ucahmq leaf=2571591 PASS
rondonia  hansen.loss_year                   6hjwpfz3yhchwa43lgtsaowbb2hmwsipcbz3lxsip3uzrn6t5icq leaf=2571590 PASS
rondonia  hansen.tree_cover_2000             257yu2ekapuhckvnhvpefr4nwaovqscpzq3epp77xjis7u73b3jq leaf=2571591 PASS
rondonia  indices.ndvi                       p7pxyygoygbrcjm74jjx7i7abdmy4aukzmxnqvqjd3kxze22gfra leaf=2571592 PASS
rondonia  jrc_gfc2020.forest_2020            7vm6hbw7327m2xjbquaahloiq67jb2fnl7wtzqbkz5lg6lhqt3dq leaf=2571591 PASS
rondonia  jrc_tmf.deforestation_year         otit4viks7f2o255nhcmtksknjodfinsin67g7cxoltavzx5npmq leaf=2571591 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  yd7mdbabip6lzjaarbjehlhhadjpx2rdfi7mxb5blalhn6ddojaa leaf=2571602 PASS
rondonia  hansen.loss_year                   gyqvjzgm5w5oijvs5725t7s7glj6be3dylo46gjxcmqw5d7bvt4q leaf=2571596 PASS
rondonia  hansen.tree_cover_2000             c3mpgoyvgosgkr52nyytsvbx3hhfjygbp4ph3flfy22sglynrpqa leaf=2571597 PASS
rondonia  indices.ndvi                       emecgeteou66xggkh4mrvvsdbx3ybkz4lfq6ujvql4a4h3ejqsxa leaf=2571598 PASS
rondonia  jrc_gfc2020.forest_2020            at25erzu6v42nvcy42cjppisz3za6kshhhs5wsswjyx6oyfwjrqq leaf=2571600 PASS
rondonia  jrc_tmf.deforestation_year         c4pbhxknzia4mehxjfbtuagnurr77rgz3vxt2m3ps3qn5oat4a3q leaf=2571594 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  qq6t3a26tdpjshuesfhferhm6vjrf6qcqsujm3rw5qz27t6xue5a leaf=2571603 PASS
rondonia  hansen.loss_year                   6o7iichz22gdlb2odsrnn5fsgfreirgidyvfthpdith3yzerdhxq leaf=2571596 PASS
rondonia  hansen.tree_cover_2000             sczcqfpkh3kdhke7uemeqkafop6qwi5zxeuyo5y2mkpknmtvzpcq leaf=2571597 PASS
rondonia  indices.ndvi                       vxsyxeeq3fijkizfgl6lajsgnrloofrzys7if7no22hy66r5cnla leaf=2571599 PASS
rondonia  jrc_gfc2020.forest_2020            iy4cm2qzy2dgd3onysxbr46lndo6mkbykgbvovz4z54fpdzmc3xq leaf=2571601 PASS
rondonia  jrc_tmf.deforestation_year         xqftyynk5qsq4xxeea7wudrrss7j7ikaszaoyweodeognvnu4rma leaf=2571595 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  l6xq3niif4jkggfb5sh5tz5jzztu4k5aniyrvdqq3p5tk7ylwmqq leaf=2571606 PASS
rondonia  hansen.loss_year                   lsfxfyfqcaox2vpfs6lz3oce2iyawcy7pe3w4sd4d2ic5l6c5aua leaf=2571606 PASS
rondonia  hansen.tree_cover_2000             wxeilahrgzid55qpyn6s45rufkmnmnmt6nyjakpbu6qvijgw6sza leaf=2571606 PASS
rondonia  indices.ndvi                       747ldyg7hu47dj4sz4csjk5euhabasoc4nj3qqdbnvqd45wn2via leaf=2571608 PASS
rondonia  jrc_gfc2020.forest_2020            rwmi7jwogzwzdvydnrphsuztvtv7clgxn5xolyxrkhefrujpqrda leaf=2571606 PASS
rondonia  jrc_tmf.deforestation_year         m4wjdtdwlm37pskfja67yvbng7spkbphbmndm2le4hwhsmqgmqfa leaf=2571606 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  ziiwtht3roi7gyx536j57qmgajc7fosutdzwakjafdgbtpkmnvpq leaf=2571605 PASS
rondonia  hansen.loss_year                   mqmb2c72s2xcpycsod6ywhvhdivyslivcsa63palpnrzkwsvblva leaf=2571604 PASS
rondonia  hansen.tree_cover_2000             h3jzpraomf3xumetuf3iysh6qasftoq2ccu4f5mk4vv27sq3jg3a leaf=2571605 PASS
rondonia  indices.ndvi                       ptqhxqq4r6ktgnbojg7yvoqxzbtnyroalabtbjs2rhfuax5hmtnq leaf=2571607 PASS
rondonia  jrc_gfc2020.forest_2020            aeoypbva3mpgyiges6v3ldjx7xltsl66u6npeveisdif6l2trmyq leaf=2571605 PASS
rondonia  jrc_tmf.deforestation_year         yoof3medqchfvvx6rs7dnxfndworjllsv3noyapemt3p553gaxcq leaf=2571605 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  b5mfbttug3vn3mt7bhza523334v2f6psgyuvjrxsfcf7mcjinjlq leaf=2571611 PASS
rondonia  hansen.loss_year                   iq6fatdkyt3bpcgtcyjkfpkvtbre6uax65eg3jo3mfduw4clo6wq leaf=2571611 PASS
rondonia  hansen.tree_cover_2000             oxpy6zmfwzv5yqfxyqbz6dnttbxmkztf3mtzmwwbmdtcfvyjedwa leaf=2571611 PASS
rondonia  indices.ndvi                       nwmllitawcecsa5mwci4cdq2xrigwozhos6cdg3gff6fuq6zphxa leaf=2571613 PASS
rondonia  jrc_gfc2020.forest_2020            seim7l3oi7v6gibiln2rfovprrue3iovleg3qcaijnngyxzedsla leaf=2571611 PASS
rondonia  jrc_tmf.deforestation_year         b5itx6isb4fq5wstc7cei5a7igcuqrvvohwjqyoyu5jh464oh6wa leaf=2571611 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  7tvr77sfalgnwj3d3pgggjn6b74n234wkbsepm2jbarn4v4cos4q leaf=2571610 PASS
rondonia  hansen.loss_year                   bf26jddv7sbym25dz2yosdlwj44ycq64rauesymx7icfeli6r5wq leaf=2571609 PASS
rondonia  hansen.tree_cover_2000             q7xepchgzeaywgdledzczvpul5iyunvx5lhhjs4i6ztyasw5qnjq leaf=2571610 PASS
rondonia  indices.ndvi                       vsmxkv3ccaxrhdgssiixdrrb2rizdx5hgf6klgtrthj7hcp26nla leaf=2571612 PASS
rondonia  jrc_gfc2020.forest_2020            oghvtthrpkzdxn6oxpcwiebz2riaaefxrh3sblmuvleazcwrhmsq leaf=2571610 PASS
rondonia  jrc_tmf.deforestation_year         3l2laxv7sch6wh57n5vfpzviodienc7vw2megwpvfojiwkv3ejzq leaf=2571610 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  ne4dhdynyigk2p53nzyvx4iejyxqzco2nmi5kiohdnkznfjzawta leaf=2571615 PASS
rondonia  hansen.loss_year                   cpist2iypn443z3nvweh763nxu6y5fcgzuwbnmhacrw4hgarsmpa leaf=2571614 PASS
rondonia  hansen.tree_cover_2000             6vkb35u6mk452hn6ovwc4knnzb4pul27why5x5umspofx74qdata leaf=2571615 PASS
rondonia  indices.ndvi                       mbq77gbg5oraqupa2pjrtqm2pazfmdt7lbojfuvkkjmex7dzqnjq leaf=2571619 PASS
rondonia  jrc_gfc2020.forest_2020            hwodysyumhas33kprfypazj26vukbbl3ocwii46uxybhjwkryhkq leaf=2571615 PASS
rondonia  jrc_tmf.deforestation_year         ixlyzjevahl272tly76mjiyvrlmbd6m4yvgra47cabcbhfdwd4gq leaf=2571615 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  jlixgye6oirh4qmptwsx7bgwagqwofaeaforzdckeszx7fttkrsq leaf=2571617 PASS
rondonia  hansen.loss_year                   mko7kms7if6yharh4oxhykuvagcywyiqzl32u4nyh5qj3gmmm7ca leaf=2571616 PASS
rondonia  hansen.tree_cover_2000             2zz2rwhs5st5qebollpdvnae4x57j5jt53rv5tmtzifrfxd4rnrq leaf=2571617 PASS
rondonia  indices.ndvi                       d5yf5viouea5hecaob565binp6rb5aanwiz5aammvgfme4ktupvq leaf=2571618 PASS
rondonia  jrc_gfc2020.forest_2020            daqf3r3snymz7mnzrchglarg2kzempj6gf4qctwc4czfh3thsf6a leaf=2571617 PASS
rondonia  jrc_tmf.deforestation_year         jg7eljd4sg25mgbab2frgncjq52zgtvziis57c3wazyrh5gb4ijq leaf=2571617 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  oaivjmf62bn6xjk3tovrf4cjgsutprs6p3lgr3jarvgsfsn6asiq leaf=2571621 PASS
rondonia  hansen.loss_year                   kvy4a65jlaqcy3mgbpfoz7vnabnhiknvgoxydaweim4gvftwk53q leaf=2571620 PASS
rondonia  hansen.tree_cover_2000             5ntg423i66fcmaip52at5ydxv3bqbddhus4oiy3f45p64vp6w73a leaf=2571621 PASS
rondonia  indices.ndvi                       2ytb7t6mpmhkh6j44yyobi7miclzelwypvwqqnv2jbocl6mvpupq leaf=2571623 PASS
rondonia  jrc_gfc2020.forest_2020            vtzio2wculzysclmccj6kc6zu6tfkvxfl64bbk4n45vgfcdrgupa leaf=2571621 PASS
rondonia  jrc_tmf.deforestation_year         cewwpdfyylrvf54xsoq4fidzif62cb2nnnxzsxg3ynomakfo6yoa leaf=2571621 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  wrnah7z6x5emr23e4k2atx6pznwvxbk56r4pw73xm6d2zcgs22ua leaf=2571621 PASS
rondonia  hansen.loss_year                   rvepn4apmebjcgkq5rzatk43tanw554ydk5ttjjgtod7paahcnpq leaf=2571621 PASS
rondonia  hansen.tree_cover_2000             s4r7x2gs6o4x754a2i5brye77cvbku2i3ctnmznr4dtk2drxsanq leaf=2571621 PASS
rondonia  indices.ndvi                       uh65hixixd5y5b7nxccjafkaljpas32trsx27sx3ss5ity4hpyga leaf=2571622 PASS
rondonia  jrc_gfc2020.forest_2020            6flyukpazglygtd4wf3j3n7sawgrcuz7vadgrlibwt4h6ozzjz2a leaf=2571621 PASS
rondonia  jrc_tmf.deforestation_year         ctexnhtru63uzdis66dt7x6eu4255tzdts7cvzzv3xptn7sca33a leaf=2571621 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  xfecbkvep4zm4usglh6qkw6a4cylxtsmrwggv7rh55ycwnhs34cq leaf=2571625 PASS
rondonia  hansen.loss_year                   jodlzxnv7diyvkx344il4ywp24a3xb472a3sbucobdjvsbkw25xq leaf=2571625 PASS
rondonia  hansen.tree_cover_2000             c4ompiifwpao6g7rtdlkh72ukthmw34dkg7gi3xe2el7jh7ag2aq leaf=2571625 PASS
rondonia  indices.ndvi                       yoq475kp7or4dultt7bfgk2gfiwl443lx7odkmkk2if6at7vu4vq leaf=2571628 PASS
rondonia  jrc_gfc2020.forest_2020            xzet2fg52xelmma74fovchhpwtmpyjmpadnq7eyrjsj4kpgyxnca leaf=2571629 PASS
rondonia  jrc_tmf.deforestation_year         og6sexyqchkilxww2l6lt6orgjnh6xbuekdeszaetiivtrdoaidq leaf=2571624 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  caqrv4wouxpnu3wefwcipw44ir2f45tuig625vnvpexupwxgwuxa leaf=2571627 PASS
rondonia  hansen.loss_year                   pmpvaq2zus3hiqcoamtsquqwms4lvq3m5wocrl67sbyphtzt2xbq leaf=2571626 PASS
rondonia  hansen.tree_cover_2000             7udzlvryhjwwil5fsjvr6dbiadzwzymmwjkxqqsi7auufif5lvfa leaf=2571627 PASS
rondonia  indices.ndvi                       qn2kpubekn5tyabkyy6yliiyhefupzrxxmopdodnws4slsbhjsrq leaf=2571630 PASS
rondonia  jrc_gfc2020.forest_2020            6btj26qegcbnbzwk64xujkdtdf4uv7vytzitmyh5lfyzm6cdbfha leaf=2571629 PASS
rondonia  jrc_tmf.deforestation_year         w5splbchvr2plykvnd53g5h3mdkuoi2i7dgkzquqfv4mxh5pq7vq leaf=2571627 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  ajnzrlyuophhh6qvodbgzzlavfz4nkhzcqhe553jzxjnp37bv5ua leaf=2571632 PASS
rondonia  hansen.loss_year                   mhquag7cycmhjr2c6cvjqbwb2wslibinembqfsiteohuid3lti7a leaf=2571631 PASS
rondonia  hansen.tree_cover_2000             3nv2wb5mqfsis7om5ea4rzc5m6iql2c6sfbbsskscq2vnzf3vz2q leaf=2571632 PASS
rondonia  indices.ndvi                       o7sdluy5aqmafhsyv72lwyik5nq6wvnd4q3ffzhelwy4pcx4uxna leaf=2571636 PASS
rondonia  jrc_gfc2020.forest_2020            e4a6whsuyzznfpj7tub4rpgl63oa43y7qfcv5w7dputoof52pf6a leaf=2571632 PASS
rondonia  jrc_tmf.deforestation_year         5fiklkueul5kwkz6xhou4b6b5nvwlzicctydg4zdwg6ha22ryrla leaf=2571632 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  do72j2fkbxchrvfxj36lzoyeoe62dazpruyhvchz2c7etdylmyiq leaf=2571634 PASS
rondonia  hansen.loss_year                   hyveelbp3qypdgwpgeup4ky3p7s36rl3u54x4ixbml64eesblvrq leaf=2571633 PASS
rondonia  hansen.tree_cover_2000             kzgysmizyceq7mnpetjht5jlg4h25oij4wva2rbjl7soinsvpbja leaf=2571633 PASS
rondonia  indices.ndvi                       go3hhezfrizsazgkgc7miysf65d2mqusd33xdylfluedti4aggbq leaf=2571635 PASS
rondonia  jrc_gfc2020.forest_2020            dtkceyp3trqscqlwczirx3b4fb3njwydnhzasgxyrwo5pzls2u6q leaf=2571634 PASS
rondonia  jrc_tmf.deforestation_year         jvc7c3q3cmvrqi2ratu7ae4gys3jdmib4qclpybyembi6bdf4yfq leaf=2571634 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  3w7ms7ylbgyxqkgke5t2qlneq2tstb3lgo2witbngiktgx3lawgq leaf=2571638 PASS
rondonia  hansen.loss_year                   5mmi5fjedctlyimajc5zylaywqf63oe6f745dhjdqguhnw47ii6a leaf=2571637 PASS
rondonia  hansen.tree_cover_2000             ysk27hkraqojpbxp5uztifi3cevfgoops7l4cx6opc2bkrwhqfnq leaf=2571638 PASS
rondonia  indices.ndvi                       xhhdtdm5jiipdnahzfp7ejg6eflrhn4ahmkajdxfpejja7labzeq leaf=2571640 PASS
rondonia  jrc_gfc2020.forest_2020            tkf6lda4kq6puggdvbb6w7qm2nfesfrawgrh5s6imjhv27s4ve4q leaf=2571638 PASS
rondonia  jrc_tmf.deforestation_year         a6bqqcwuk5gnydukqsxvjad24clqrpvmklphh5bifdyzbclojn6q leaf=2571638 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  5atot2njdqspi2gihmujkq6hajxtxyv3nwcdswaqecaooco2gi4q leaf=2571639 PASS
rondonia  hansen.loss_year                   rudaorvl2magvml5njm2izuvrowb6pzebku4vlqbjox4kxj5yina leaf=2571639 PASS
rondonia  hansen.tree_cover_2000             iqgcje2st5vlso4eqwoyly5sht3rfdtxonunrxtsefzsaxz2in4a leaf=2571639 PASS
rondonia  indices.ndvi                       2xk6yoy5m5eacdfh7qrrw36urmm44el7y2nmeby6c2rs3jsupcgq leaf=2571641 PASS
rondonia  jrc_gfc2020.forest_2020            2dwym6fqrwjkbqx5xscddtcqvifc2pn33cjtqkh3jxiz7moyq63a leaf=2571639 PASS
rondonia  jrc_tmf.deforestation_year         i7fm2pp6fow6x7brixhjotm3jlmj3jmtclctdy5mvhryqp7nh7aa leaf=2571639 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  ee5a3l5ebvm2kzaluqjjaju2lntn4sgd6kodqkgihmhzlxeuwkza leaf=2571643 PASS
rondonia  hansen.loss_year                   dv5nubz2ww5glvhh4bdbgncu24qcnse4tuyefkstbpdjpttfx2yq leaf=2571642 PASS
rondonia  hansen.tree_cover_2000             dumr2dbbyohijjofdp423tg6uyozie42rjldh77dexkmuv2u6dia leaf=2571643 PASS
rondonia  indices.ndvi                       uhge3fpecdpurf6bhij2ilptzf662bbyvdrdj4svpmovzvyh4tsq leaf=2571646 PASS
rondonia  jrc_gfc2020.forest_2020            hs73an2mtdyhtetkh5x3an2pqfzt6yls73iuhvtgmpoubli42f4a leaf=2571643 PASS
rondonia  jrc_tmf.deforestation_year         ltwpw22wvdv2y4nmws4plortnjztetbe6juy5sxgxo7tolwkwo3q leaf=2571643 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  u65dubtysegqrikhmglsnvdhdolmsxeom23l7isnh666xb5woara leaf=2571645 PASS
rondonia  hansen.loss_year                   kxkfshotmppgbe74pqqysuqshev6j4bob3ufzvxv6uizdyq472la leaf=2571644 PASS
rondonia  hansen.tree_cover_2000             ml4zmgfzgbxzrerbft3ry7x7uoea3ohy2unengfbnm4wtk4js7ia leaf=2571645 PASS
rondonia  indices.ndvi                       beuvzw5xagx44qchwfdpj4cg7l2eo65aqasuzfao7pvdg3n2ptgq leaf=2571647 PASS
rondonia  jrc_gfc2020.forest_2020            yusoiklhzx6wn6v25chc4yrgtyvqgic7e642vcnga733rjzzvlda leaf=2571645 PASS
rondonia  jrc_tmf.deforestation_year         ncof4mnveciq3flf3vhewsraouix5sjten6u7avya3jbjdzzrxta leaf=2571644 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  v7uiyaf4x54yemx5grmcajvteccbql445y74h3vcbe3y2zgducqa leaf=2571649 PASS
rondonia  hansen.loss_year                   3jijxczhqef2yyh3ou3cpvwlmdeaprqvo6vetigsf4e7ije6ps3a leaf=2571648 PASS
rondonia  hansen.tree_cover_2000             v6vs3ubwuaabltmrtxff7gbdc3qoe7v32gmsdwplt2rzu323ukaa leaf=2571648 PASS
rondonia  indices.ndvi                       br5ltkf53h2ufz42323g5qow6i53adlviba2mtd6ywwvoebstkaa leaf=2571650 PASS
rondonia  jrc_gfc2020.forest_2020            5xtcrfmmnxj7vmy2pblgfqkaownmb7vyv2vzn22eng54nhg4yhaq leaf=2571649 PASS
rondonia  jrc_tmf.deforestation_year         mv6jtv4lsp3tpnoqe3h7clvyti35s3sxdgu2awcfgswa63pks4qq leaf=2571649 PASS
rondonia  esa_cci_biomass.agb_t_per_ha_2022  3hjmlskk4qw4vlvijeg5b73gdzxb35m5b626kan7cpfc4bhelsoq leaf=2571652 PASS
rondonia  hansen.loss_year                   mqjalsfsoniehgbgokhgi6ryckkucxbghrw3fjtpw47zqqef5tqq leaf=2571652 PASS
rondonia  hansen.tree_cover_2000             sgnpvruuztd3ns2immun2lwvwg6me5x22r6jf3iudje7a22b4nbq leaf=2571651 PASS
rondonia  indices.ndvi                       l4irnnnyjgcffel7grqypsaaev7szswpgs3eutwa3wggjzjgyoja leaf=2571653 PASS
rondonia  jrc_gfc2020.forest_2020            zvefrwyiysagwlmer6fyvipzeydymztf2pmvklcgcukya5z3k5vq leaf=2571652 PASS
rondonia  jrc_tmf.deforestation_year         2f5jmsl7jhrklnupwbpankvj67kt6suhbrncvxcwchsngxrbopha leaf=2571652 PASS
```