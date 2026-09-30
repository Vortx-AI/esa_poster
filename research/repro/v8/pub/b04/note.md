---
after: sth 2566579 3abso6lcewa5rvuipzsekwsvnhvkswvwf2e3uf7bkzb3z6uq22tq 2026-09-30T13:02:55Z
emem: pointer.v1
spec: mlxrdcys43hao7cz554s46bp7a
source: https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/43/S/FS/2026/9/S2A_43SFS_20260925_1_L2A/B04.tif
bytes: 232853854
etag: not exposed
kind: cloud-optimised GeoTIFF
chunks: 292 of 292 hashed
root: 6qneyijgknf4v4kcd64yghrvmgq6zcbsqzwu6nwvnzfylsqtfniq
hash: blake3-256 of each chunk's bytes
order: defaults, then by blake3(label without type or shape)
place: 32.93339,76.65684
bbox: 76.0638,32.4294,77.2564,33.4349
---

# B04.tif

> cloud-optimised GeoTIFF at sentinel-cogs.s3.us-west-2.amazonaws.com, 232.9 MB.

- 10980×10980 px, 16-bit unsigned, deflate with horizontal differencing tiles of 1024×1024
- 5 levels (10980, 5490, 2745, 1373, 687 px wide), 291 tiles in all
- EPSG:32643
- 10 m per pixel
- nodata 0
- centre 32.93339, 76.65684; bounds 76.0638, 32.4294, 77.2564, 33.4349 (west, south, east, north)
- 292 of 292 chunks hashed; more can be hashed later, in a fixed order, without re-reading these

## Place

- centre cell defi.zb576.zb56d.yAyO (emem:cell, about 10 m across)
- copdem30m.elevation_mean 4537.3 m: emem:fact:defi.zb576.zb56d.yAyO:g6uqzjegd6iyi6nkufutovyz5h5kuh6thzuxfufpcvx7ohkmtmkq
- indices.ndvi 0.0428: emem:fact:defi.zb576.zb56d.yAyO:ex6vvw7eaigx3bob5y2nstpoxztcuclrr7du3b2wut2n7zm4brua
- poster pixel 32.57126,77.03448 (Keylong, Lahaul): level 0 tile 8,9, column 9098 row 9443 of 10980; B04 reads 900 here. Earth Search subtracts the L2A offset (earthsearch:boa_offset_applied), so Planetary Computer's copy of the same scene reads 1900
- with B08 2502 at the same pixel (B08.tif beside this file), NDVI (2502 - 900) / (2502 + 900) = 0.4708994708994709, the value emem signed: emem:fact:defi.zb572.xoso.zb1ec:oj5ceccile62uvm6hedpuk67cjt2pqc7z33mtsyuffgakxbxmyaa

## Chunks

| what | url (· is the source) | offset | length | blake3 | stats |
|---|---|---|---|---|---|
| header and tile tables | · | 0 | 3562 | mq6yoyw6gsqf75alrquc5wgias7tmwshflypgappkmzxnspwn3yq |  |
| level 0 tile 0,0 | · | 59970075 | 1424017 | ee67gvqjbemd5ehb3tkym2l5peowtdwndxz25l7ymsh3canmx2aa | mean 3513 · sd 1763 · min 924 · max 16100 |
| level 0 tile 1,0 | · | 61394092 | 1435006 | egv5vjhg4jclxaimujm4yhvus6aupjmjyhei224b36hezjms33ua | mean 2594 · sd 1892 · min 577 · max 16960 |
| level 0 tile 2,0 | · | 62829098 | 1532810 | zl2aske33snjexu5j3ktvbdoeevmimghkf32enftjnl5aiyqxmqa | mean 2817 · sd 2521 · min 516 · max 16900 |
| level 0 tile 3,0 | · | 64361908 | 1580863 | 4vj33vqz3eglujtbnrrfe6isl7z6bvnhtvcgkv7c7m2skr5sslhq | mean 2286 · sd 1617 · min 1 · max 16760 |
| level 0 tile 4,0 | · | 65942771 | 1667007 | z6jotoynnjmoc5qurupzhwtvmhcwdxtmh2ej5bsdusumvoiol2va | mean 3625 · sd 2630 · min 1 · max 16870 · 100% valid |
| level 0 tile 5,0 | · | 67609778 | 1670864 | ti5izvaa7swq4fzpqtpipltw37qiqlakni3nlp5fquupqur36rma | mean 4539 · sd 3042 · min 1 · max 16690 · 100% valid |
| level 0 tile 6,0 | · | 69280642 | 1646979 | w2l6d5ww5yijmlh3eorbtrormkll5asr7r7cph7tzct3mbic2rdq | mean 2999 · sd 2071 · min 1 · max 16800 · 100% valid |
| level 0 tile 7,0 | · | 70927621 | 1572426 | xobzj4nt3ooidf4wbice2722c6xwodmjlb5evderrs2o5yykitpa | mean 1908 · sd 700.4 · min 1 · max 16780 |
| level 0 tile 8,0 | · | 72500047 | 1502683 | mnesvz25vhgjhaza6ycd5ovtrkqjuhx7n7sunm6kifolfm2z3mxa | mean 1382 · sd 473.6 · min 1 · max 10670 |
| level 0 tile 9,0 | · | 74002730 | 1556612 | zvzwc2j4exsx4iitrmep4mjo7fnb7zoxid6wmkbp4vaj5onl6fua | mean 1706 · sd 1391 · min 1 · max 15130 · 100% valid |
| level 0 tile 10,0 | · | 75559342 | 1151794 | npfljjnk377j2aehbrxdl552rc7esi4o5qny5jowjbvciwwj33vq | mean 1505 · sd 491.6 · min 1 · max 10840 · 72% valid |
| level 0 tile 0,1 | · | 76711136 | 1459450 | v37adgpuqgi3w6s5tz3yg3mavrthppme4ekb7ys4k43cmtkrxbzq | mean 1760 · sd 1266 · min 15 · max 9708 |
| level 0 tile 1,1 | · | 78170586 | 1550612 | ld6z5qp2qt66teehriprx5dqf4fokzrjk7mcxytp4ixmebir27tq | mean 1963 · sd 2054 · min 1 · max 17050 · 100% valid |
| level 0 tile 2,1 | · | 79721198 | 1636532 | h2jwyi4wmwbotk3ehxzjkvbi6b3q3wkb4li2mqnso7hm56aktpka | mean 3513 · sd 2834 · min 1 · max 16850 · 100% valid |
| level 0 tile 3,1 | · | 81357730 | 1632571 | yvrp43isyyx2uglmw5d2pjkxf4qwkqo22ynam26of2e75slsvvva | mean 2935 · sd 2894 · min 1 · max 16950 · 100% valid |
| level 0 tile 4,1 | · | 82990301 | 1606770 | nuu2ciwrohsarho5qrwaqfro42fjrrumvwmrl2fnu6ppx4oe6ulq | mean 2350 · sd 2091 · min 1 · max 16890 · 100% valid |
| level 0 tile 5,1 | · | 84597071 | 1659928 | dm7pagtpptvlvwz6wcuxpdq2r6amkwwh4yqxqlml46jrzwitydtq | mean 3848 · sd 2710 · min 1 · max 16560 |
| level 0 tile 6,1 | · | 86256999 | 1663436 | r2k3rcy4h2jiesoilf434yddlzdsumghnlmccb6nz2zu4te3b7nq | mean 4132 · sd 2802 · min 1 · max 16650 · 100% valid |
| level 0 tile 7,1 | · | 87920435 | 1607993 | jhrxrrewql4gjcj6bxp2l7r7i5eqobadmcrlbclmujy2p2e27nfq | mean 2398 · sd 1525 · min 1 · max 16690 · 100% valid |
| level 0 tile 8,1 | · | 89528428 | 1567644 | 2pxumnnjjeftbmbumomjuw2b5gslttluhtnhyji5nza46m7br3ea | mean 1645 · sd 660.4 · min 1 · max 13680 · 100% valid |
| level 0 tile 9,1 | · | 91096072 | 1532610 | lr3vwbrw4lepn4utvmw2xc4nn6nn2lm7ubc4cu7i6wkjnbuwbw2a | mean 1668 · sd 1107 · min 1 · max 15610 · 100% valid |
| level 0 tile 10,1 | · | 92628682 | 1180404 | zrzmllztiept245kbm2f3jmr2sdcjt2xqxhqyyff2b2csln2oxpq | mean 1597 · sd 572.9 · min 1 · max 10410 · 72% valid |
| level 0 tile 0,2 | · | 93809086 | 1566300 | pnyhsrgo42syzal6yttt6m4fkg6aeqp7qk5cdezzmi33eoed4krq | mean 2597 · sd 2539 · min 1 · max 16920 |
| level 0 tile 1,2 | · | 95375386 | 1557702 | hq3lwhnnz3jamr54rnqrp46qw6btl2m345btzmc7x4m7yqxi6flq | mean 892.6 · sd 1172 · min 1 · max 17390 · 100% valid |
| level 0 tile 2,2 | · | 96933088 | 1581571 | 7emsufxgge5mtt5xv2h6kvopftftge43idfnnhovnvu44zgtxrka | mean 1922 · sd 2281 · min 1 · max 17260 · 100% valid |
| level 0 tile 3,2 | · | 98514659 | 1552967 | vtxkoqqydlzmrzbkgli2mrph4sqkzung6egzqjdneschoh5kruqq | mean 1949 · sd 1985 · min 1 · max 16910 |
| level 0 tile 4,2 | · | 100067626 | 1601362 | iv7cihbp2qctvh3edfbinvomyakaha5um5jpz5nzpxigq2dnioja | mean 2954 · sd 2414 · min 1 · max 16770 |
| level 0 tile 5,2 | · | 101668988 | 1608534 | xqrlp2oz2newssmhm5awhcktqgx3rbj3e3x4mgn7x4qvhc5wqj4q | mean 2940 · sd 2100 · min 49 · max 16690 |
| level 0 tile 6,2 | · | 103277522 | 1687620 | e7hhcwaps23bsuuykmduc7sp7sjkbo7mmk34m7y4qpxxh35omw5a | mean 4785 · sd 3079 · min 1 · max 16650 · 100% valid |
| level 0 tile 7,2 | · | 104965142 | 1629654 | ucezbojochuntsaqwqv5yaymkwpctnjduxxqwogu3776zr3k4ejq | mean 2816 · sd 1905 · min 1 · max 16690 · 100% valid |
| level 0 tile 8,2 | · | 106594796 | 1594854 | oz554loiadef2p3dd2okph5pc7w4afqj2yd5mjgefwna6irppu2q | mean 2002 · sd 1261 · min 1 · max 16590 · 100% valid |
| level 0 tile 9,2 | · | 108189650 | 1545658 | 3s4wyencbc424vxwmercmvjjeor7deazyifclawflctjtbroytta | mean 1570 · sd 969.2 · min 1 · max 13190 · 100% valid |
| level 0 tile 10,2 | · | 109735308 | 1155333 | 24rd3dapdlzl2rydsv5dijhsq76uyv3cj5biayietpgipotzhj5q | mean 1615 · sd 512 · min 1 · max 9663 · 72% valid |
| level 0 tile 0,3 | · | 110890641 | 1543445 | 6t4zkgkeuwiq5gp73iu2xm6nj64qgyi2vwogtvmewdknow44e5ma | mean 2180 · sd 2701 · min 1 · max 17440 · 100% valid |
| level 0 tile 1,3 | · | 112434086 | 1556909 | 45cs4faib7bmjsxrvtzuce5j46sjmfjqqxzjfpzmgftlwdnnncpa | mean 1670 · sd 2160 · min 1 · max 17290 · 100% valid |
| level 0 tile 2,3 | · | 113990995 | 1537878 | kn3pnal6lk5km5y5seurxdrdpifhuoarkj5ynb24b6hpsltrs3ha | mean 1070 · sd 1492 · min 1 · max 17170 · 100% valid |
| level 0 tile 3,3 | · | 115528873 | 1513357 | rtll6h4eo6zskn4puk2faztjonqbgh7mbtg6mlyb2mp3ceqvn5rq | mean 1170 · sd 810.4 · min 10 · max 16820 |
| level 0 tile 4,3 | · | 117042230 | 1606864 | gxsbyva6hlc2aygdd6ssnikcdczkdvubo4uq3kedcs4hx7dbb7sa | mean 2858 · sd 2413 · min 1 · max 16950 |
| level 0 tile 5,3 | · | 118649094 | 1576896 | 4mlxseonxpelygbdiohlj6gzn7k6gwlu34aqrqpxvsfymlxl5uoa | mean 2152 · sd 1900 · min 1 · max 16850 · 100% valid |
| level 0 tile 6,3 | · | 120225990 | 1632707 | zsk75rau7rslyocs5zbvsss6zfh76k5f4dfsnn5khqh6wr4oy4bq | mean 2847 · sd 2310 · min 1 · max 16910 · 100% valid |
| level 0 tile 7,3 | · | 121858697 | 1674087 | 4qt6urvdmdewzf3tocgl43ekj5kd4qhkc4vefci66i33bk7yvoya | mean 4702 · sd 2974 · min 1 · max 16410 · 100% valid |
| level 0 tile 8,3 | · | 123532784 | 1640592 | lqtjjxwre7bo2unkxn7s3xnrpfhy56vbpxdlf6avbwhzrdrgolra | mean 3264 · sd 2299 · min 1 · max 16590 · 100% valid |
| level 0 tile 9,3 | · | 125173376 | 1555150 | dkb3rscitttmj27xfxewhenvlyyfckokrn5zfssov2nvaoec67mq | mean 1862 · sd 1123 · min 1 · max 13850 · 100% valid |
| level 0 tile 10,3 | · | 126728526 | 1140582 | 2cuseaj2bprve6upuartm3rqxgt4njqbwkxozweetbbhckvrwl2a | mean 1640 · sd 549.5 · min 1 · max 13520 · 72% valid |
| level 0 tile 0,4 | · | 127869108 | 1552404 | qyikz5coi3o4wrcfq35vwxcj4tdwkegztddy42htj4ntqnnttgbq | mean 3473 · sd 3489 · min 1 · max 17200 |
| level 0 tile 1,4 | · | 129421512 | 1577866 | l43vf5a7rofxn3t2wrr4xph53iffnqpv6bf735i5fjkmymqfnsvq | mean 3409 · sd 3062 · min 1 · max 16900 · 100% valid |
| level 0 tile 2,4 | · | 130999378 | 1562899 | yndrgoaib6pkxwa4zbhhw5yb3ssfk2ld4nuyorjy3wrdght6oybq | mean 1575 · sd 1704 · min 1 · max 17200 · 100% valid |
| level 0 tile 3,4 | · | 132562277 | 1526660 | qiulszwo57c4qywzvlk5rwy4be6hnrinsoi6yhlfyy4desp6m3uq | mean 787.3 · sd 533 · min 1 · max 16840 · 100% valid |
| level 0 tile 4,4 | · | 134088937 | 1537015 | 5iqtvzfenaaz7iyawh3rokvwektvbl5pzk7phaznqh3fo3inlrka | mean 1162 · sd 1334 · min 1 · max 16980 · 100% valid |
| level 0 tile 5,4 | · | 135625952 | 1555284 | 2czyhmxbulim7cwn52qxqsiwptb42enc4fivugc7zwtgwgnkfo5q | mean 1419 · sd 1192 · min 1 · max 16900 · 100% valid |
| level 0 tile 6,4 | · | 137181236 | 1587558 | vpqt2peixpd6rqd45wxth2lz5cndp7g5rheqdbviivxhxfipc33a | mean 2126 · sd 1433 · min 1 · max 16820 · 100% valid |
| level 0 tile 7,4 | · | 138768794 | 1613584 | fgcqlnttfiqgtxfpzx7wxzuazqj7zwkwvd4m7xyojirhih5ypsoq | mean 2331 · sd 1820 · min 1 · max 16730 · 100% valid |
| level 0 tile 8,4 | · | 140382378 | 1647216 | uczqsj2lqmqvsb44hf2zonejkdz25lcgkt5x7ipb5cfcpnrisuua | mean 2915 · sd 2195 · min 1 · max 16760 · 100% valid |
| level 0 tile 9,4 | · | 142029594 | 1619351 | akt4edf3wlsrun57zxa5b46vqmqedagp32szctbta3sbtld7ulaa | mean 2542 · sd 1865 · min 1 · max 16800 · 100% valid |
| level 0 tile 10,4 | · | 143648945 | 1034203 | riamhe2rttoelsd32unayfng35r2txiguo6chpxmywkcrtfdkqvq | mean 2099 · sd 1551 · min 1 · max 16250 · 65% valid |
| level 0 tile 0,5 | · | 144683148 | 1514412 | fbcqoow2ssgmla6celozi7evskcfj2ahhke2lz2cjrdcx6n2nwga | mean 1846 · sd 2809 · min 1 · max 17900 · 100% valid |
| level 0 tile 1,5 | · | 146197560 | 1517395 | m5tn6ltm46bu77p4sgvvsm5a2hkcb2fuixkpkxqje2v4v6dqydua | mean 1888 · sd 2827 · min 1 · max 17860 · 100% valid |
| level 0 tile 2,5 | · | 147714955 | 1574773 | nzggp6utuu2xcv3nzpohm7w7geitbcjkwfvo6yie66g5gzvzcwlq | mean 2758 · sd 3034 · min 1 · max 17040 · 100% valid |
| level 0 tile 3,5 | · | 149289728 | 1532884 | rmtglmujirxn6de64mj4ks7mbvtvqs5lqhf36lft6glmsfj2anuq | mean 719.6 · sd 846.2 · min 1 · max 17010 · 100% valid |
| level 0 tile 4,5 | · | 150822612 | 1544525 | 5baf7bumjz2xjrjs2hgp4464c6hmhnwb6vi4672tfdvlmvl36njq | mean 1167 · sd 1131 · min 1 · max 16950 · 100% valid |
| level 0 tile 5,5 | · | 152367137 | 1583576 | bc2ol56fui5yn47te4mbqsuacvjmltakuoaxilzjpzxf7nd2oanq | mean 2074 · sd 2207 · min 1 · max 16870 |
| level 0 tile 6,5 | · | 153950713 | 1609801 | p4kmoya5pe4ydrivksfq74omokhjmexxcmdiwmbofuncaceiqmva | mean 2796 · sd 2389 · min 1 · max 16440 · 100% valid |
| level 0 tile 7,5 | · | 155560514 | 1576514 | gdv6hkvvrx6vln3bdnfhq7fxvqgxzbr4qfwndltuq6y7p3h3sr5q | mean 1763 · sd 1101 · min 1 · max 16800 · 100% valid |
| level 0 tile 8,5 | · | 157137028 | 1615423 | c6vn5cmanpfu25qvx7ai3x4prpnou7247ai6xkusfvq6pjy7asbq | mean 2837 · sd 2102 · min 1 · max 16640 · 100% valid |
| level 0 tile 9,5 | · | 158752451 | 1579749 | ldkb4gswwtwgylvz2zxrm53mcrxvg2ewj5dyild7xdmfw3nrdu5q | mean 2331 · sd 2256 · min 1 · max 16890 · 100% valid |
| level 0 tile 10,5 | · | 160332200 | 676214 | eljfzyfx7d3a7ya4ints3f25bv6fyfffaa2jnmajnh4iebfitd3q | mean 2306 · sd 2165 · min 1 · max 16510 · 42% valid |
| level 0 tile 0,6 | · | 161008414 | 1507929 | em7ehm5g6ozick73zyt3owk5v6d6aldewogihkarsfibyco67hca | mean 801 · sd 1459 · min 1 · max 17860 · 100% valid |
| level 0 tile 1,6 | · | 162516343 | 1514945 | yhhnzp7oe7jdz6s7ra2ifzsaluybrwfnigaqtfwg3kb2dzksw3ca | mean 2495 · sd 3303 · min 1 · max 17890 · 100% valid |
| level 0 tile 2,6 | · | 164031288 | 1570761 | s7uctlvniizalkj5pbo3asfr2t7lztk4zgmxhhdqwhjsjn74tjia | mean 2902 · sd 3324 · min 1 · max 16960 · 100% valid |
| level 0 tile 3,6 | · | 165602049 | 1559605 | mttlfubdrcfm7uomhmduemg6tdhjltq2652dvfyfq247b6nmo26q | mean 924.9 · sd 1058 · min 1 · max 16740 · 100% valid |
| level 0 tile 4,6 | · | 167161654 | 1602527 | q2jd3mkhmml7vmiirdat7wczk5ahihmckn4bu3hmoz2fpwwpz3eq | mean 1947 · sd 2343 · min 1 · max 16960 · 100% valid |
| level 0 tile 5,6 | · | 168764181 | 1572057 | bglo4ahn7fp7jlcj2dllg36sjpyznunswdow3ortcudzykcw75va | mean 1684 · sd 1524 · min 1 · max 16960 · 100% valid |
| level 0 tile 6,6 | · | 170336238 | 1573302 | m6t7qimt3ke2hss2nya3bu2kza7nypq5bn452mqpimczti54q3ia | mean 1360 · sd 973.4 · min 1 · max 16820 · 100% valid |
| level 0 tile 7,6 | · | 171909540 | 1630925 | 2tan53tckiynfys4ffkjs3aiaz3gl6cx574cydqgicebhuerhlgq | mean 2554 · sd 1915 · min 1 · max 16540 · 100% valid |
| level 0 tile 8,6 | · | 173540465 | 1653841 | hu3a2csvt3blojrkp2yave6glnvifgsgbna7o3tadushpb4xs7iq | mean 3983 · sd 2766 · min 1 · max 16670 |
| level 0 tile 9,6 | · | 175194306 | 1599007 | 3afgswnzzcji3ik4lu7ktvbh5w7atfltqdknbltssm53fjcsoqxa | mean 2051 · sd 1683 · min 1 · max 16740 · 100% valid |
| level 0 tile 10,6 | · | 176793313 | 303626 | d7anqvhes7ii6yrkufhae57ketpen5c6am5rtaxens2gtwdcsr7q | mean 1608 · sd 1009 · min 1 · max 16960 · 18% valid |
| level 0 tile 0,7 | · | 177096939 | 1512616 | dmj5amoaeocfkyls4qtmtnooxjzeup6nmfnogeuogcveax3uosra | mean 944.5 · sd 1340 · min 1 · max 17680 · 100% valid |
| level 0 tile 1,7 | · | 178609555 | 1490285 | 3qbwueccf7gqfbadwav73ezp53mknnc32bwedk6o6tf3ilru6zvq | mean 1067 · sd 1811 · min 1 · max 17940 · 100% valid |
| level 0 tile 2,7 | · | 180099840 | 1516388 | ycmbjzlnvu2hl7exj2kblqtdfzvrgsegc4paevk5h2ozbz7hgkpa | mean 1775 · sd 2819 · min 1 · max 17600 · 100% valid |
| level 0 tile 3,7 | · | 181616228 | 1533944 | ym7khntyn3n4fhja36oitddh64xmoqhzrojb4mevh3mzqjm7wuda | mean 909.9 · sd 956.4 · min 1 · max 16950 · 100% valid |
| level 0 tile 4,7 | · | 183150172 | 1554890 | lyw4miocyzhmhboij7j4vsojgnesmd2gvqnma65rpg56gneavuaq | mean 1003 · sd 1113 · min 1 · max 16980 · 100% valid |
| level 0 tile 5,7 | · | 184705062 | 1549788 | qjiqytvofo2ta4uclrz6ue7w6ilker37radqgzmxxrktrhspahna | mean 932.5 · sd 439 · min 1 · max 6021 · 100% valid |
| level 0 tile 6,7 | · | 186254850 | 1576942 | w3wdam6kawhlscgbpeedbqbr53n6kjdxhbxyle4b76durmqnifvq | mean 1842 · sd 1918 · min 1 · max 16930 · 100% valid |
| level 0 tile 7,7 | · | 187831792 | 1604146 | x4e7uw65wxqluj4ljmj4ksddehrymckaoyhos5auu2koq3fnibuq | mean 2011 · sd 2140 · min 1 · max 16850 · 100% valid |
| level 0 tile 8,7 | · | 189435938 | 1657988 | mppdz27beex64asj3jbd2rpl3s7fxzoriaco6zs3cbs2qzaepbaq | mean 3709 · sd 2876 · min 1 · max 16710 · 100% valid |
| level 0 tile 9,7 | · | 191093926 | 1545984 | 24gvhnsugrrmau6lnbvyv4qa7wnmgxfde7ajhou2c2axgi24mmoq | mean 2999 · sd 2510 · min 1 · max 16560 · 94% valid |
| level 0 tile 10,7 | · | 192639910 | 21813 | y473dttg3og6t5pafw23nyzsl2jcjcdp4dhui65ctbmwnvx53vda | mean 1281 · sd 478.9 · min 1 · max 3892 · 1% valid |
| level 0 tile 0,8 | · | 192661723 | 1547819 | hq7htdzsd7gtu4x7cm2xnladekb2dl3fomsuz5f7i6hll2ilyjya | mean 1863 · sd 2382 · min 20 · max 14250 |
| level 0 tile 1,8 | · | 194209542 | 1565218 | ii3gqxqgzeslpaksvbf62wns6k3mlz3ee3t4eeqm55yztl3euwga | mean 3788 · sd 3485 · min 1 · max 17650 · 100% valid |
| level 0 tile 2,8 | · | 195774760 | 1538201 | od6ecwrmr4qtj4brh43gnddyaytujf5uv4ozqfwsud4veopgykma | mean 3967 · sd 3999 · min 1 · max 17210 · 100% valid |
| level 0 tile 3,8 | · | 197312961 | 1572653 | ix2bqh53gag4ravz2ka7ahpitolpihfmfp7oajfk4s477liz7wpq | mean 2185 · sd 2677 · min 1 · max 17020 · 100% valid |
| level 0 tile 4,8 | · | 198885614 | 1571212 | nmysdunz7nxerj7d7rbrq4jhlvcz7qjwfzfdmonp7fbjhpietb5a | mean 1599 · sd 2468 · min 1 · max 17100 · 100% valid |
| level 0 tile 5,8 | · | 200456826 | 1576196 | v5kff2a3gckefcpywxeqnjdrumr4djf5kl52f2oek5if3hll4tbq | mean 1241 · sd 1415 · min 1 · max 16970 · 100% valid |
| level 0 tile 6,8 | · | 202033022 | 1564547 | svkkrpk2vgbfgesjimqw6g5zcwiillup4jdw2aogzctjny3lthwq | mean 1132 · sd 873.6 · min 1 · max 16670 · 100% valid |
| level 0 tile 7,8 | · | 203597569 | 1528928 | ar7rqxppjf44op65jteq7hbidvnp3ox2fu77dxmbc72mniopfiga | mean 1092 · sd 625.5 · min 1 · max 13320 · 100% valid |
| level 0 tile 8,8 | · | 205126497 | 1549400 | nnhdlurc7aylqa6np7h472pvuj3ghcxkpfxlc7wzequn5stspyja | mean 1697 · sd 1821 · min 1 · max 16870 · 100% valid |
| level 0 tile 9,8 | · | 206675897 | 1157035 | 74on5sftcgv3yb3zeyoyj7zd7jafv4xqp7przbjqdpvcmoccboha | mean 2496 · sd 2464 · min 1 · max 16940 · 72% valid |
| level 0 tile 10,8 | · | 232847689 | 2055 | 3vwob6iobzfvwj3kwziu7ynoc2s67hmz2inqhbgzojv7zslcsa4q | no valid values |
| level 0 tile 0,9 | · | 207832932 | 1565734 | hbmgdhmwpsexlnzsmol6bqk4ohtasf3vdcv23r5ih5yamraww7ua | mean 1924 · sd 2179 · min 1 · max 18210 · 100% valid |
| level 0 tile 1,9 | · | 209398666 | 1542715 | 5quqhqh5qw3zeexxqyagd3kjaiknhrjlsecuo7x4ot22pqrptvra | mean 1408 · sd 1926 · min 1 · max 17620 · 100% valid |
| level 0 tile 2,9 | · | 210941381 | 1521913 | y6p5geghtsn2g3ivykk27jsdcma2ousalf57m3cx6v5krlioscta | mean 1712 · sd 2536 · min 1 · max 17890 · 100% valid |
| level 0 tile 3,9 | · | 212463294 | 1476077 | t2brdjs2k6ls2k624aqgoenovoedwuagoqgfrmysxseqno4tjnga | mean 1061 · sd 1987 · min 1 · max 15670 · 100% valid |
| level 0 tile 4,9 | · | 213939371 | 1532904 | ynwyucfm4fvx6lldkgabb2srg3m532ettsxw33wfc3xzgxvlzxkq | mean 1344 · sd 1935 · min 1 · max 17090 · 100% valid |
| level 0 tile 5,9 | · | 215472275 | 1622500 | ljhx5dzs3g4jopg3v3h3shu4uedtd4gunn5ghfz3ke6pfspi5okq | mean 2242 · sd 2703 · min 1 · max 16830 · 100% valid |
| level 0 tile 6,9 | · | 217094775 | 1588760 | bl6tsofjsnhlkjhlxkmpzflrxy23kpvs4dfi5t3pehbdyyo7fxqq | mean 1831 · sd 2167 · min 1 · max 16860 · 100% valid |
| level 0 tile 7,9 | · | 218683535 | 1583490 | wfm7pml4mf45qzdjgdlddc4ls2epsd5qk7lsths7eiulos6ifz2a | mean 1702 · sd 1829 · min 1 · max 16870 · 100% valid |
| level 0 tile 8,9 | · | 220267025 | 1549684 | 3yywqm3oqlpr7jmyzdahzpypaziqr4fueh7n572ia4k5ovsgjntq | mean 1101 · sd 523.2 · min 1 · max 17310 · 100% valid |
| level 0 tile 9,9 | · | 221816709 | 773481 | 76ftmsinttofn2qz3w3yoaci5z7foot2ofzbkgjrd75fjqn3dzyq | mean 993.6 · sd 362.3 · min 1 · max 16070 · 49% valid |
| level 0 tile 10,9 | · | 232849744 | 2055 | 3vwob6iobzfvwj3kwziu7ynoc2s67hmz2inqhbgzojv7zslcsa4q | no valid values |
| level 0 tile 0,10 | · | 222590190 | 1090654 | 5zso33t4vwmodnrvbkhx6o6ids35ewzanukdreyulztywbwj2i3a | mean 3408 · sd 4062 · min 1 · max 18150 · 72% valid |
| level 0 tile 1,10 | · | 223680844 | 1089593 | lzv7h5h4cmr6fcjxw7lcu7yovgahil5vzgoym2qx4fiwudvho7gq | mean 657.6 · sd 482.2 · min 4 · max 10280 · 72% valid |
| level 0 tile 2,10 | · | 224770437 | 1099491 | kvn2pm27wisvgxzw6ckpyke36jffevy2bg35tb5spcilgwhzrgoa | mean 618.7 · sd 362 · min 1 · max 8013 · 72% valid |
| level 0 tile 3,10 | · | 225869928 | 1099086 | qnav35p3rzsbdawf6qqg6t7pdnjurbvxnfdnytl5jeliqjkze2oa | mean 619 · sd 409.8 · min 1 · max 5332 · 72% valid |
| level 0 tile 4,10 | · | 226969014 | 1073925 | wgfu5w6dqjuoge2i6jt2aywondfdvexhmsqxxprs7swte4lbivxq | mean 663.6 · sd 965.2 · min 1 · max 15780 · 72% valid |
| level 0 tile 5,10 | · | 228042939 | 1054261 | dbxfrjglub6fnxswsysxrn5d2rnfpcqugvjtcixumv22dmfbgxka | mean 427.7 · sd 348.2 · min 1 · max 5044 · 72% valid |
| level 0 tile 6,10 | · | 229097200 | 1094426 | rbcwfhjq5asnscxry2fiinyudwohryth6yesoa3w5ie7zmndjkhq | mean 922.9 · sd 1063 · min 1 · max 16910 · 72% valid |
| level 0 tile 7,10 | · | 230191626 | 1161556 | hllo3oojl5w64bdmm4of5ly53fdutrep45pufrheoipsetvqq66a | mean 1805 · sd 2094 · min 1 · max 16930 · 72% valid |
| level 0 tile 8,10 | · | 231353182 | 1145693 | bo46ti7rnlkqkktr4f6vf3vtgso5qfgczfvae4t6ogwhmtr2i7cq | mean 1388 · sd 1499 · min 1 · max 16790 · 72% valid |
| level 0 tile 9,10 | · | 232498875 | 348814 | nl4tojpq7oddn7fqw7t3fyvxts7msnsbhxcgmggj2bgiqxvmvbgq | mean 1503 · sd 1608 · min 1 · max 16950 · 21% valid |
| level 0 tile 10,10 | · | 232851799 | 2055 | 3vwob6iobzfvwj3kwziu7ynoc2s67hmz2inqhbgzojv7zslcsa4q | no valid values |
| level 1 tile 0,0 | · | 15117637 | 382358 | takhq562iap747qhozwuappz6laciy77k4if2ehjoyl5pclexeaa | mean 3513 · sd 1761 · min 946 · max 15870 |
| level 1 tile 1,0 | · | 15499995 | 379166 | 6yrvtlfirym4vvdykewflfzre4sy7svzxuy3d6l4t35eeban2ktq | mean 2594 · sd 1889 · min 596 · max 16960 |
| level 1 tile 2,0 | · | 15879161 | 400236 | y6ivrpkwhg7wedvp3hy2t7ahqhoz6vjy3q2befjybw63lhfmx2cq | mean 2817 · sd 2512 · min 528 · max 16900 |
| level 1 tile 3,0 | · | 16279397 | 410199 | s5eudi6zsvk2evm3kk37q3xlhhu3kcbykqipkgwmxpkitcw7d2ga | mean 2286 · sd 1602 · min 2 · max 16760 |
| level 1 tile 4,0 | · | 16689596 | 430138 | gnm6tbabxchrcxpdbqw34p4lqr3r4fetcxkojf5erewc2p3k3asa | mean 3625 · sd 2602 · min 1 · max 16870 |
| level 1 tile 5,0 | · | 17119734 | 430956 | 2uymslqgnugv2f6uuxwrcemfay2zdinhfxuaskgvuu7oygr6mfaa | mean 4539 · sd 3015 · min 1 · max 16480 |
| level 1 tile 6,0 | · | 17550690 | 424296 | dpjra5637dmfzp4vfaquwbpri34jnapnevutadppewdl7bjjb6ua | mean 2999 · sd 2039 · min 1 · max 16800 |
| level 1 tile 7,0 | · | 17974986 | 405413 | dscv2tmkn7vcmndu6v6w5vqwccm6hg2x676iclhqobfni4vflcfq | mean 1908 · sd 666.7 · min 4 · max 15980 |
| level 1 tile 8,0 | · | 18380399 | 388158 | ka7d7idgesqnyqepkxi4ayvmldj2r7wgzgteazraqmzkqkithl4q | mean 1382 · sd 461.2 · min 94 · max 9429 |
| level 1 tile 9,0 | · | 18768557 | 403749 | lkdqnydydfsou2pj5btkauzkcnqq2zpc3td6aq37j6ctdlp7igkq | mean 1706 · sd 1377 · min 1 · max 13440 |
| level 1 tile 10,0 | · | 19172306 | 297461 | ulpgxjfsozpo3jhv347m2gz55gz4qfbeubothrv4sdzsayjaulca | mean 1506 · sd 466.2 · min 1 · max 8707 · 72% valid |
| level 1 tile 0,1 | · | 19469767 | 382458 | hpqmer3kifz2bbbkszchfodgb52jlnck4zvrz6f522o7ujpee5na | mean 1760 · sd 1263 · min 24 · max 9606 |
| level 1 tile 1,1 | · | 19852225 | 402465 | 6dqbqyd77gppccpjh4oa5mfc3255zytiqhqiormn6xztb52fvmka | mean 1963 · sd 2045 · min 1 · max 17050 |
| level 1 tile 2,1 | · | 20254690 | 424196 | girkvahm5xydikuoo6kychrm363qhfc3bmll4zllnyvnwfvjf7ka | mean 3513 · sd 2814 · min 1 · max 16840 |
| level 1 tile 3,1 | · | 20678886 | 422923 | lhubuguseaxy22ugozm3mntpcs2pqdoifb3gvhenhnchyodggx2q | mean 2935 · sd 2872 · min 1 · max 16950 |
| level 1 tile 4,1 | · | 21101809 | 415524 | zhwvtaxvh5qwv53ezr5iyzdocxpxlnj6zbxz7634fcbtxaikheea | mean 2350 · sd 2072 · min 1 · max 16890 |
| level 1 tile 5,1 | · | 21517333 | 428350 | umkgf6pi7axombuiqopg3dzdmyy4aaiqgohjoku2yaqvlipzu3gq | mean 3848 · sd 2683 · min 1 · max 16500 |
| level 1 tile 6,1 | · | 21945683 | 429264 | zpacq5fko2cgorbp7pp2fmhvp7lvyuyrw4fa7ueawyews2csa7sa | mean 4132 · sd 2773 · min 1 · max 16520 |
| level 1 tile 7,1 | · | 22374947 | 414955 | 7upneapy5jvtcuuvonhpu5xib3giis7e6fj22z555ho52xvbz76q | mean 2399 · sd 1497 · min 1 · max 16350 |
| level 1 tile 8,1 | · | 22789902 | 404543 | pfehaqld4wjfmapmtdctizudzryb5dhego35vjfaxu34vyjuz73a | mean 1645 · sd 634.2 · min 1 · max 11730 |
| level 1 tile 9,1 | · | 23194445 | 397098 | sqos5mkgwudrlqfkrw3pplvzx42n3c6rhyuxtybrb6e4lbojk6aa | mean 1668 · sd 1096 · min 1 · max 14200 |
| level 1 tile 10,1 | · | 23591543 | 303434 | w6wgqvxoajg3ckrfd6ubl7dhhyi7o6pfjnxs6d62747csqir6gmq | mean 1597 · sd 538.2 · min 1 · max 8743 · 72% valid |
| level 1 tile 0,2 | · | 23894977 | 407566 | vl7gnj3dypb4j2qphwdaxwau2chr7bsz5mb4yg36ripiyfdpvu2q | mean 2598 · sd 2529 · min 2 · max 16910 |
| level 1 tile 1,2 | · | 24302543 | 399622 | v3fe4zx2if7abzwyp2ayqb5mukyi2ou47ktgjdqxoecfttpwllda | mean 892.7 · sd 1161 · min 1 · max 17380 |
| level 1 tile 2,2 | · | 24702165 | 409541 | n44vs3lu3dinie4abb7mkzl56conxhyi24cg3ay3cjniaipp7pya | mean 1923 · sd 2270 · min 1 · max 17260 |
| level 1 tile 3,2 | · | 25111706 | 401143 | nylvu5cl5nsup26yhienxnl3izcywvf7ltuxw6s7g72tjyhhlzma | mean 1949 · sd 1970 · min 6 · max 16900 |
| level 1 tile 4,2 | · | 25512849 | 414610 | lo5lb27up7327zonnzqndq7vmmu3udsmk4r6y6gz7xanz4l7ubwq | mean 2954 · sd 2398 · min 1 · max 16770 |
| level 1 tile 5,2 | · | 25927459 | 414800 | wl3c3jfp44axshq6yymvjzhwndyva2mhdnu7aldhxfhgy6nslv4a | mean 2940 · sd 2076 · min 79 · max 16490 |
| level 1 tile 6,2 | · | 26342259 | 435840 | vdviedozszchqsfme6y6hzp6orxvox5jzvrrnpzemfnnh5nix43q | mean 4785 · sd 3046 · min 1 · max 16640 |
| level 1 tile 7,2 | · | 26778099 | 420332 | 2sjcm6xz5lesq7qzbvlhjp7gtw5sgflbvsigivzwjrtj4ph6jdnq | mean 2816 · sd 1878 · min 1 · max 16690 |
| level 1 tile 8,2 | · | 27198431 | 411731 | 2vqga35x5f5ciizvm2pvfhxsyxr4nxj6qq26uecuo4vs7atvimdq | mean 2002 · sd 1237 · min 1 · max 14860 |
| level 1 tile 9,2 | · | 27610162 | 399417 | bdmjaocmocnnxmsv53ana3bamstszfblvcc34iha2otfo3cihucq | mean 1570 · sd 954.6 · min 1 · max 12690 |
| level 1 tile 10,2 | · | 28009579 | 298329 | u6gjnmztebunq2ejv3ghtmn7l7g2yy6aw5qc3owbjx2zhzlp4ziq | mean 1616 · sd 487.1 · min 1 · max 8626 · 72% valid |
| level 1 tile 0,3 | · | 28307908 | 401694 | fn3g6iup4kximu2zz5jo24dg63zvqkwwgf77lhin2mtnl6fze3ya | mean 2180 · sd 2696 · min 1 · max 17440 |
| level 1 tile 1,3 | · | 28709602 | 404921 | h3m6b2tzfpshby4jayukec2jp3lwreqo3w2pmdijc6fqcbayo7da | mean 1670 · sd 2151 · min 1 · max 17280 |
| level 1 tile 2,3 | · | 29114523 | 396620 | y7ddggbsxu6vo4hxn4rvuwkzlmztf7esef265vuxtrhcup3m47ha | mean 1070 · sd 1484 · min 1 · max 17170 |
| level 1 tile 3,3 | · | 29511143 | 390000 | nvfccwvhjsonc4psqyzwvy4ni2cqapaewqn3jlom3dkjlrcolluq | mean 1170 · sd 798.1 · min 23 · max 16800 |
| level 1 tile 4,3 | · | 29901143 | 416116 | tsohcpe6cs2do6z76wntbmimf6cztovkgaif2ltamhsg3qg3vara | mean 2858 · sd 2394 · min 7 · max 16950 |
| level 1 tile 5,3 | · | 30317259 | 407461 | 2xzs2oh5glafugsofybnpj7g4eau5x35qztmwnfp5zjhoa5tuhnq | mean 2152 · sd 1882 · min 1 · max 16830 |
| level 1 tile 6,3 | · | 30724720 | 421149 | 5vfrvz7p7dwmxfarj56jk2zztpykjbv37bhgnroo3n5x3cuz7keq | mean 2847 · sd 2280 · min 1 · max 16900 |
| level 1 tile 7,3 | · | 31145869 | 433788 | rj6wrhwqolw4yhoeoludgcph2pfltqioncwrghcnjelqgwzyy2qq | mean 4702 · sd 2941 · min 1 · max 16410 |
| level 1 tile 8,3 | · | 31579657 | 423728 | vnohd3w3ewdigslbkvludi6bfrkja5ojeluw52t7tenyabhguiva | mean 3264 · sd 2272 · min 1 · max 16570 |
| level 1 tile 9,3 | · | 32003385 | 402666 | fbixrcwf6lab4gebvz35ohq7qwj5rfwefbtuy2rpbxrcc27aarrq | mean 1862 · sd 1107 · min 1 · max 13030 |
| level 1 tile 10,3 | · | 32406051 | 294688 | 2wkityin4p3lydq4afxpvlrnmh5lnkq7qn5ilhflhnue64rdz46q | mean 1641 · sd 529.9 · min 1 · max 10390 · 72% valid |
| level 1 tile 0,4 | · | 32700739 | 412301 | l6seapuldqtsxzf5vj32gqywns2k6rkllal67khzidv7tevadwsq | mean 3473 · sd 3484 · min 12 · max 17190 |
| level 1 tile 1,4 | · | 33113040 | 416642 | v3s6pin4ihlrgc5jrsjkvzvbfsfgjtiirsgmvuvbxor2lbpsg52q | mean 3409 · sd 3054 · min 1 · max 16710 |
| level 1 tile 2,4 | · | 33529682 | 405291 | adea7rtylxwyldtlnd7oe5ohghjjwvyt55rdmz7vthwnx2fnkbtq | mean 1575 · sd 1692 · min 1 · max 17190 |
| level 1 tile 3,4 | · | 33934973 | 392236 | uww3t2uqxxp7r7vvwp7pzrv6dpsgofl7367ntkm35cgtrp4rq5mq | mean 787.4 · sd 517.8 · min 1 · max 16830 |
| level 1 tile 4,4 | · | 34327209 | 397090 | z4khql42atp5r3phn52inrdgqvdo5wdj4m3mh27abvjilqnlzdtq | mean 1162 · sd 1326 · min 1 · max 16980 |
| level 1 tile 5,4 | · | 34724299 | 401627 | 6fjstsp4dpfrtuyt5d2vbjgsb5k3gvigo5k5gj4uc5cs3tmrnb6q | mean 1419 · sd 1178 · min 1 · max 16900 |
| level 1 tile 6,4 | · | 35125926 | 411138 | 5cywwiyyl6im7gsfbson66e2z6zh5tdavpthm7l5xex5dcxepv7q | mean 2126 · sd 1414 · min 1 · max 16810 |
| level 1 tile 7,4 | · | 35537064 | 417397 | k5uaczpqythx4zrivwdzgm645puljtqntoouelsaidnlgzg4owfq | mean 2331 · sd 1790 · min 1 · max 16730 |
| level 1 tile 8,4 | · | 35954461 | 425386 | dbjvsuyzsdbziqiw2ggeutsuv2zdzyp2tko3nm7msfpkzumvq4aa | mean 2915 · sd 2159 · min 1 · max 16450 |
| level 1 tile 9,4 | · | 36379847 | 418142 | zno5wvrscd4sz363uiedqq5qvzlefgpohwxc7rajpt3m47dp6s3q | mean 2542 · sd 1838 · min 1 · max 16800 |
| level 1 tile 10,4 | · | 36797989 | 267676 | vjhaydbopqbnsect7xo725mokum6ae7klwctnvfpaumkzkkiqhqa | mean 2099 · sd 1532 · min 1 · max 15340 · 65% valid |
| level 1 tile 0,5 | · | 37065665 | 396331 | s6i24h5opqaajprix5s2optgkb2jq6yemqzrbjgrshwdik2swlsa | mean 1846 · sd 2805 · min 1 · max 17880 |
| level 1 tile 1,5 | · | 37461996 | 398210 | kxposy45iwtghsoakj472nyhdmnylk77zgx3gw33nxi643ie2tca | mean 1888 · sd 2823 · min 1 · max 17860 |
| level 1 tile 2,5 | · | 37860206 | 414172 | zcofswio63kovt2isg4vnwpg3oxaiy5jtobnt4v4wz2cmxp5c4ka | mean 2758 · sd 3024 · min 1 · max 17040 |
| level 1 tile 3,5 | · | 38274378 | 394466 | irs2zqonj2dhx4vq2xgzvpxi7kcamgzpbqmxkrncehme33t7sfwq | mean 719.7 · sd 832.4 · min 1 · max 17010 |
| level 1 tile 4,5 | · | 38668844 | 399582 | yfpadajrdodf7jzcavdabqqnyve7256t267e5alsswtukz2efonq | mean 1167 · sd 1112 · min 1 · max 16950 |
| level 1 tile 5,5 | · | 39068426 | 409763 | q5kezgm3shtmiw7mx5tzkonaj36jnsaxzj2dtvje5pksfya7jgpa | mean 2074 · sd 2189 · min 1 · max 16870 |
| level 1 tile 6,5 | · | 39478189 | 416451 | jvlr2tq2uaircir3oxzf4daqir2y5noydah5p675f3ctl6gukyaa | mean 2796 · sd 2366 · min 1 · max 16050 |
| level 1 tile 7,5 | · | 39894640 | 406627 | 2sboeub6jtquejmxxhperub7pujl2ifspsvwm4u437nx7ewecfuq | mean 1763 · sd 1080 · min 1 · max 16800 |
| level 1 tile 8,5 | · | 40301267 | 418210 | p6ruremnsfmglquagv3ekfwfsi4ubc5znfaqljcznwp77ed24d5q | mean 2837 · sd 2076 · min 1 · max 16470 |
| level 1 tile 9,5 | · | 40719477 | 409270 | ofdu3uim36qw6fmkhrkulwmnbm7zapsbpv4pla27cpltpxwcofia | mean 2332 · sd 2233 · min 1 · max 16600 |
| level 1 tile 10,5 | · | 41128747 | 175684 | figndeqybmef3rhan7fa2kkqyfpkwppfqks3xzmm5jlkcj6sp36a | mean 2306 · sd 2143 · min 1 · max 16510 · 42% valid |
| level 1 tile 0,6 | · | 41304431 | 387928 | 73rxtesbxsndqthhrh5l4yfon2xau6u6use73vtjkfkfzrnloplq | mean 801.1 · sd 1453 · min 1 · max 17860 |
| level 1 tile 1,6 | · | 41692359 | 400229 | ds57yhrbuqamlp444xm7ztqzsajovvsbyojwk7jv2qxer4qihkza | mean 2495 · sd 3299 · min 1 · max 17880 |
| level 1 tile 2,6 | · | 42092588 | 413708 | g44uuhkasvxxens2m5sssozb6u6emi6nepvya5ptxaxrbzrkwbfa | mean 2903 · sd 3313 · min 1 · max 16950 |
| level 1 tile 3,6 | · | 42506296 | 401324 | t6hg5cdfcumacdd2dfubgrhdzfclhjepscfp2tosoyagihm7y5ja | mean 925 · sd 1025 · min 1 · max 16740 |
| level 1 tile 4,6 | · | 42907620 | 414542 | em4gjzdpsn5johmxshfglx5a6m5ciufcd32m6235ia34aydilp2a | mean 1947 · sd 2315 · min 1 · max 16900 |
| level 1 tile 5,6 | · | 43322162 | 406140 | vkgkbb4didh27rpiz7xwual6ucdpwsmjkxgyfdj7mhrok4jaonpq | mean 1684 · sd 1504 · min 1 · max 16740 |
| level 1 tile 6,6 | · | 43728302 | 404790 | 4tznpulpt6lbjwmc5zgelacney7opj5cccf5nq35bczm6rkxwbeq | mean 1360 · sd 953.4 · min 1 · max 16320 |
| level 1 tile 7,6 | · | 44133092 | 420703 | lojnx3wnhqg2ehjfelvjonxhtz7zu5s4fjlanpw5yd4wbpw554ma | mean 2554 · sd 1887 · min 1 · max 16310 |
| level 1 tile 8,6 | · | 44553795 | 428808 | j4crcr25qdwyilcvgggudryekb3l4wrocg6xluqujabzvimudjpq | mean 3983 · sd 2738 · min 1 · max 16310 |
| level 1 tile 9,6 | · | 44982603 | 412580 | kp36uqawouoztbxd2ivmm6gjfeayfwav6s6a75xw42iqth6s7k5a | mean 2052 · sd 1656 · min 1 · max 16420 |
| level 1 tile 10,6 | · | 45395183 | 79008 | lxuh3kqpfifi3xhpljy4r34eicfcb7qnlgsen33dleraqd3u3npq | mean 1608 · sd 974.7 · min 7 · max 16960 · 18% valid |
| level 1 tile 0,7 | · | 45474191 | 391336 | phfumyjqp52xlkg5ax7uqbl7cdwwpiwct2avz7hhnornkl6nebda | mean 944.6 · sd 1334 · min 1 · max 17130 |
| level 1 tile 1,7 | · | 45865527 | 387822 | djh56icb44ll6ezgvzynjzoz2t5slplkj7lxmximxpe4kpignneq | mean 1067 · sd 1806 · min 1 · max 17860 |
| level 1 tile 2,7 | · | 46253349 | 398699 | jzpwrfexrnyv7flw6e5biuk33nkahtnyz46do4qrhjqvm54lvdva | mean 1775 · sd 2813 · min 1 · max 17580 |
| level 1 tile 3,7 | · | 46652048 | 396846 | inil6r4syisd4qv72n7libxdldgnzcpsmb3urfo5st2vgqjnxb3q | mean 910 · sd 939.3 · min 1 · max 16950 |
| level 1 tile 4,7 | · | 47048894 | 401856 | x3nt5rl4zskd62qgyf4ea3e2tijnoulgd6tls2bjcc3eoee7ajzq | mean 1004 · sd 1096 · min 1 · max 16980 |
| level 1 tile 5,7 | · | 47450750 | 397664 | jnszbhdv4xeoqy34liijyiwxkiayepgkrszqahvpp3f5dmgsbfeq | mean 932.6 · sd 419 · min 1 · max 5494 |
| level 1 tile 6,7 | · | 47848414 | 407208 | 7wwdczegxvbvo67aur3ixi3icnw6telf3qbflxohhzdr7tpxajfq | mean 1842 · sd 1899 · min 1 · max 16930 |
| level 1 tile 7,7 | · | 48255622 | 414400 | 544y5ghlmgqzpc6c66lyjgph4cpdbgdth7ex7xg3tiv3drqa2ida | mean 2012 · sd 2111 · min 1 · max 16850 |
| level 1 tile 8,7 | · | 48670022 | 429181 | 6a5xe3ait6cqb73yryiylio2zrzh577f5n4wyugqogvln537a45a | mean 3709 · sd 2844 · min 1 · max 16310 |
| level 1 tile 9,7 | · | 49099203 | 400323 | vnu2hb5fqnhqjjejfvybyuaheq4ajv7txgcyhkevnfhbjw36qstq | mean 3000 · sd 2485 · min 1 · max 16280 · 94% valid |
| level 1 tile 10,7 | · | 49499526 | 6145 | o33lyf3tw4jsknyn7exbrpx57h2mw635mhhjwoyxwwnkbpeg36mq | mean 1281 · sd 435.6 · min 9 · max 3585 · 1% valid |
| level 1 tile 0,8 | · | 49505671 | 405419 | kgteutdfe3emabixpoiyumcyaku64hy73k3knql43skmpznem3lq | mean 1863 · sd 2377 · min 29 · max 14180 |
| level 1 tile 1,8 | · | 49911090 | 416800 | dajbetm4che2lmprr3qyzotixugpchcmsuzmkzrwehrwgbigxa3a | mean 3788 · sd 3480 · min 1 · max 17210 |
| level 1 tile 2,8 | · | 50327890 | 411710 | xyjp3ar65vvefdfzziky6q6irzyajh66vqpp54qlnzfo3fi7jy2q | mean 3967 · sd 3995 · min 1 · max 16950 |
| level 1 tile 3,8 | · | 50739600 | 412064 | bahycsm27mztmrshm3dwijj3ao3tfr57gdl77nsfito7porlmmfa | mean 2186 · sd 2659 · min 1 · max 17020 |
| level 1 tile 4,8 | · | 51151664 | 408868 | bnl4scozfpw2y3yb3hutkgvxfw6lms5hlxgmhkot4g4sm454sgpq | mean 1599 · sd 2437 · min 1 · max 17100 |
| level 1 tile 5,8 | · | 51560532 | 407183 | lrwppmjb7hdpqxdgtadobxpkmky65l5bo2fear3ps56yklywxkjq | mean 1241 · sd 1376 · min 1 · max 16940 |
| level 1 tile 6,8 | · | 51967715 | 402112 | alfxm6p3jd7eshhelib7lyw6hsoarbvygvcvn3a2vvl6xl63vukq | mean 1132 · sd 849.7 · min 1 · max 16510 |
| level 1 tile 7,8 | · | 52369827 | 394907 | eocloy3osti7p6tdqkvtbywzxqzsaps5m25lqmax5uzrpq7uah7a | mean 1092 · sd 607.1 · min 1 · max 12520 |
| level 1 tile 8,8 | · | 52764734 | 401750 | y3alq3nmpeo36gqbbabjkyalmwhohhzvgegsfa6fbbn5xqcsbizq | mean 1698 · sd 1805 · min 1 · max 16740 |
| level 1 tile 9,8 | · | 53166484 | 301888 | 726eivyegkrumjubva2u4adq3c2ij6kwgcvnsarhi3r442ugkwea | mean 2496 · sd 2444 · min 1 · max 16940 · 72% valid |
| level 1 tile 10,8 | · | 53468372 | 531 | q6vavplqzaqde7mjqbudgqoeoftse5lvkoemdzauzqdxunq3jrva | no valid values |
| level 1 tile 0,9 | · | 53468903 | 410048 | baoowypwpmsil2nioieepbrjnwreep7itf3cvlbdh5ilq6246pkq | mean 1924 · sd 2172 · min 1 · max 18200 |
| level 1 tile 1,9 | · | 53878951 | 401944 | wrzognhhbbvzxipm2vkftdkwld46ckzynvqcln6vilz4wophsveq | mean 1408 · sd 1919 · min 1 · max 17620 |
| level 1 tile 2,9 | · | 54280895 | 399377 | 5fwu73s4cyyad7ttbyfdk4wzahrlrgj2f3wgu6uqrrnamgqghjfq | mean 1712 · sd 2530 · min 1 · max 17880 |
| level 1 tile 3,9 | · | 54680272 | 385105 | sjqbtseqx44tgjpqemgskousl7ujsdounxm5aarhbnaqrhzm5hxa | mean 1061 · sd 1984 · min 1 · max 15340 |
| level 1 tile 4,9 | · | 55065377 | 399593 | fitcplpnl6dupvhk4zcuzs2dplfzm6rywyrsf6bgonv6qofw2zcq | mean 1344 · sd 1917 · min 1 · max 17090 |
| level 1 tile 5,9 | · | 55464970 | 419913 | uosuwlp7t56chn6m7nchnfdsxo7bwqvvv3a7uljyfls3kkdd3fxq | mean 2242 · sd 2672 · min 1 · max 16820 |
| level 1 tile 6,9 | · | 55884883 | 411324 | yf5fzjtmv7kcz3mjb2edfdqn5d43eixdhrrlyajziuextkcyawla | mean 1831 · sd 2137 · min 1 · max 16840 |
| level 1 tile 7,9 | · | 56296207 | 410268 | 5swfpke6ihmfj7w434wfmx3ku6jr7h4kqhxr7aon47m5yopbbdbq | mean 1702 · sd 1802 · min 1 · max 16810 |
| level 1 tile 8,9 | · | 56706475 | 399645 | swxtvwnfiidbpp74x6njnvyrwseves3pns42jrdmrkc3nhy4eibq | mean 1101 · sd 498.9 · min 1 · max 16150 |
| level 1 tile 9,9 | · | 57106120 | 199051 | xiuqwdb4h7dv66efl6ho752fdukf3xxqlpefeocl6xlzkxkwgggq | mean 993.7 · sd 342.5 · min 1 · max 11510 · 49% valid |
| level 1 tile 10,9 | · | 57305171 | 531 | q6vavplqzaqde7mjqbudgqoeoftse5lvkoemdzauzqdxunq3jrva | no valid values |
| level 1 tile 0,10 | · | 57305702 | 291486 | sd3jck5srqkpahzoncngvz27lvvwrkgs7zizv2y3wr3kpasqxftq | mean 3408 · sd 4060 · min 1 · max 18110 · 72% valid |
| level 1 tile 1,10 | · | 57597188 | 279721 | jaw5z6zyns5inumnkcmkz253iaexqi57pubv5sg7kzgtj5ate7ja | mean 657.7 · sd 472 · min 16 · max 10200 · 72% valid |
| level 1 tile 2,10 | · | 57876909 | 281678 | kutm2j5fmwyzfogvn3dp4gzlqsqfcjgvlymcecwbqvmbjlburtoa | mean 618.8 · sd 346.3 · min 1 · max 6953 · 72% valid |
| level 1 tile 3,10 | · | 58158587 | 282938 | gldhkharijlp56mitvthpw2ukecdqoxngczlqu45afs6gnbxfcaq | mean 619.1 · sd 394.1 · min 1 · max 4306 · 72% valid |
| level 1 tile 4,10 | · | 58441525 | 278622 | o4hap5pdqyfop2z6focb3ar2c2lsbhjps6ubsyss6tsibcxbeyva | mean 663.7 · sd 959.7 · min 1 · max 15340 · 72% valid |
| level 1 tile 5,10 | · | 58720147 | 275632 | 73qyqdxl7522pjvulyrgkxgdhpe52776yzynwl4mguq4abhyresq | mean 427.8 · sd 337.2 · min 1 · max 4531 · 72% valid |
| level 1 tile 6,10 | · | 58995779 | 284798 | toklaauie7ir4gio6tcdziunynmmzgncjjpvh4yd4wny73lbhvma | mean 923 · sd 1038 · min 1 · max 16910 · 72% valid |
| level 1 tile 7,10 | · | 59280577 | 300892 | 3dzduvognxhh6peletrefzwvb22gl7hbd3qg376v6fml7yjvrzuq | mean 1805 · sd 2056 · min 1 · max 16670 · 72% valid |
| level 1 tile 8,10 | · | 59581469 | 297166 | 5mco7tned4dgrrh3st664xybxknatqukvsyrwrobfaagxjs3ml4a | mean 1388 · sd 1466 · min 1 · max 16780 · 72% valid |
| level 1 tile 9,10 | · | 59878635 | 90909 | aoii2ikthbks7bbhyrfshe4nchnptv7d4mvgh7avhq77nvatxg6a | mean 1503 · sd 1568 · min 1 · max 16940 · 21% valid |
| level 1 tile 10,10 | · | 59969544 | 531 | q6vavplqzaqde7mjqbudgqoeoftse5lvkoemdzauzqdxunq3jrva | no valid values |
| level 2 tile 0,0 | · | 3618668 | 403074 | 753gum3eh2e5sgvraiyjba2lo6imd2vtpurzai26gb2fhx7ltbjq | mean 2457 · sd 1879 · min 1 · max 17040 |
| level 2 tile 1,0 | · | 4021742 | 426590 | lnggglz453i3xx5xp3yy3w7iz2lzbvbvgvgk4adod62su2q6jzwq | mean 2888 · sd 2503 · min 1 · max 16950 |
| level 2 tile 2,0 | · | 4448332 | 435764 | ueche6yg76ve7wjeuhshpl5f5euoft4ydergb6fcpgtomue2aezq | mean 3591 · sd 2682 · min 1 · max 16880 |
| level 2 tile 3,0 | · | 4884096 | 427100 | t5ywsuoopxzavjwoytm55ktswmgba5dxcn2qni3w424rtlnxbh2q | mean 2860 · sd 2030 · min 1 · max 16420 |
| level 2 tile 4,0 | · | 5311196 | 404945 | pgstggkrspesokncugwnovppomp76phi33o2omtwi6mmdrhzczca | mean 1600 · sd 944.7 · min 1 · max 12680 |
| level 2 tile 5,0 | · | 5716141 | 154266 | glmzsokp443lyalx3bikaiwactjx525ldlu6ncybsb72w3dyx5jq | mean 1551 · sd 449.9 · min 1 · max 7752 · 36% valid |
| level 2 tile 0,1 | · | 5870407 | 414846 | dx6i57iqmwukqwgfv5n6fuh4ghqalrq7fn5277tpmngaxxfghpuq | mean 1835 · sd 2288 · min 1 · max 17430 |
| level 2 tile 1,1 | · | 6285253 | 407455 | zxmrivqppd6r6url63glp2bteb3rj3o4tjyot6vmmn7knqjvkfbq | mean 1528 · sd 1747 · min 1 · max 17240 |
| level 2 tile 2,1 | · | 6692708 | 423956 | iqjvegxsjoreiewmfen7jb3xcse6wi3jcfi6wv3trv3h2r35rwsq | mean 2726 · sd 2184 · min 1 · max 16940 |
| level 2 tile 3,1 | · | 7116664 | 437610 | zlkj6u7gah2m2ga4sxj3mx4zroapw3yalkz5a3kmppwvvvg2jxgq | mean 3788 · sd 2696 · min 1 · max 16840 |
| level 2 tile 4,1 | · | 7554274 | 417163 | pirnazlx6ql5umvcgopdhai264yr4zfmtlvtmgxrzh3dmg6w5ola | mean 2175 · sd 1583 · min 1 · max 16440 |
| level 2 tile 5,1 | · | 7971437 | 152817 | zhdpj7wammfg3pobq4uoumq7d5ggffgmuz6illpfysuctopeqs3a | mean 1628 · sd 468.2 · min 2 · max 8944 · 36% valid |
| level 2 tile 0,2 | · | 8124254 | 420220 | y5khmgiwxsrxklmioa7mztuk2q2axrus2zmwsqx3kgpikhtlc3zq | mean 2654 · sd 3139 · min 1 · max 17850 |
| level 2 tile 1,2 | · | 8544474 | 411291 | n2iphjjyb6mvytjig5ntk4fjrir7t4i527fdfggudfukrkwsyllq | mean 1460 · sd 1961 · min 1 · max 17180 |
| level 2 tile 2,2 | · | 8955765 | 409654 | l5cbkrhnc6mnlyoerqyj6itnexbzuhlive267ccdzlnxs7afspeq | mean 1456 · sd 1531 · min 1 · max 16980 |
| level 2 tile 3,2 | · | 9365419 | 420991 | hsd63cg7tok7xbqmwtghdofoeey6i2shtrhc2mbhi5aodw5x3d4a | mean 2254 · sd 1724 · min 1 · max 16800 |
| level 2 tile 4,2 | · | 9786410 | 426402 | tliwiqya2rcoyy3gora2llgf4ztxf5m5kwauutl4zkijohotyvla | mean 2657 · sd 2040 · min 1 · max 16440 |
| level 2 tile 5,2 | · | 10212812 | 115469 | yzamqv5jv57mjnc7goagj7xca6vuiff4ztfj3xzie73pay3cqbnq | mean 2179 · sd 1760 · min 1 · max 14100 · 27% valid |
| level 2 tile 0,3 | · | 10328281 | 403334 | izdmmflsmqowufouoaz7m4xkvnnfssq4aljmi6qn2xfmquvyslka | mean 1327 · sd 2218 · min 1 · max 17790 |
| level 2 tile 1,3 | · | 10731615 | 414363 | c2xcig3h72hg4wlsbo7hwlznlgr6o7ytzmf2wwx6rnqrvvck4o6q | mean 1628 · sd 2400 · min 1 · max 17400 |
| level 2 tile 2,3 | · | 11145978 | 412360 | zr5kp7uxvgwudpwdlqwiv6i7jmkorsdb655s73tglqdsna5eakya | mean 1392 · sd 1524 · min 1 · max 16970 |
| level 2 tile 3,3 | · | 11558338 | 419394 | 7mivwojquagsjz62ywh4n3rwipkeycy4mwszfu4wc5fwm3sy5jqa | mean 1942 · sd 1777 · min 1 · max 16840 |
| level 2 tile 4,3 | · | 11977732 | 426895 | ybdfdxdko24fsvzp2ospdz6asep6rvywvgdhdyfdg33imjdk6kaq | mean 3188 · sd 2536 · min 1 · max 16300 · 99% valid |
| level 2 tile 5,3 | · | 12404627 | 23057 | fvytulo67mcqpxpsv5dvaz7ddi3y6vwlrnaeg5v5xlgdbwfpyx2a | mean 1590 · sd 889.6 · min 43 · max 14420 · 5% valid |
| level 2 tile 0,4 | · | 12427684 | 423150 | bhaznos6wzftqecsk7kg67ga46iogdssyiztxoc77n7p4uucg3bq | mean 2246 · sd 2700 · min 1 · max 18190 |
| level 2 tile 1,4 | · | 12850834 | 415940 | de5qc7ydvysdbasp3vpwtewphlxwsdhrkaxv5gfjt46uimeveeda | mean 2232 · sd 3066 · min 1 · max 17670 |
| level 2 tile 2,4 | · | 13266774 | 419557 | mup7oickgghstx3vymo7nxeiwponojijjriapokuxdd2ozc67ofq | mean 1607 · sd 2141 · min 1 · max 17090 |
| level 2 tile 3,4 | · | 13686331 | 412255 | smxlooknzs2kqz7ycb7b3nfwkibvsm2t5gywtdhb3hmrpdtfm5eq | mean 1439 · sd 1483 · min 1 · max 16690 |
| level 2 tile 4,4 | · | 14098586 | 333382 | vjfvb2vt5bojr4a5rmjlakt4ix2q6kcx7ttd77o6rjpaa547majq | mean 1582 · sd 1630 · min 1 · max 16740 · 80% valid |
| level 2 tile 5,4 | · | 14431968 | 531 | q6vavplqzaqde7mjqbudgqoeoftse5lvkoemdzauzqdxunq3jrva | no valid values |
| level 2 tile 0,5 | · | 14432499 | 147906 | ipowvmfjjdiamy3fxqqqkntriqayvscqdp74ykzkpxsdve5s7faq | mean 2033 · sd 3194 · min 1 · max 18100 · 36% valid |
| level 2 tile 1,5 | · | 14580405 | 142795 | 2566qsj6buf7apmhhdvcuw457gfrtthvclngodzjucn2njqghpea | mean 619.1 · sd 345.4 · min 1 · max 3891 · 36% valid |
| level 2 tile 2,5 | · | 14723200 | 142227 | 7gnip3wjnuckcgmscmm7n36y6tr3uqui6w3s5u3nr46ti5fshxva | mean 545.9 · sd 717.4 · min 1 · max 14980 · 36% valid |
| level 2 tile 3,5 | · | 14865427 | 150661 | z5qi66i3h7l45cpqllk2ugipxvgjap7ki5mvqoxgc6vk5mlplnva | mean 1364 · sd 1629 · min 1 · max 16310 · 36% valid |
| level 2 tile 4,5 | · | 15016088 | 101018 | o5aonkhfec4cb7k33sijbaqlozzuktkj65wi3cw3ou44zy77nvka | mean 1413 · sd 1424 · min 1 · max 16320 · 23% valid |
| level 2 tile 5,5 | · | 15117106 | 531 | q6vavplqzaqde7mjqbudgqoeoftse5lvkoemdzauzqdxunq3jrva | no valid values |
| level 3 tile 0,0 | · | 737919 | 416306 | hrpqqooejglihrspg7taijnu3a2tq6hsgxgyx6ylkqvksfmijzxq | mean 2179 · sd 2115 · min 1 · max 17060 |
| level 3 tile 1,0 | · | 1154225 | 432190 | vbuwsrivutg3v7sgzgflxkwys5dsyu4jq2lg3b5wl26vfsnd4y7q | mean 3241 · sd 2319 · min 2 · max 16860 |
| level 3 tile 2,0 | · | 1586415 | 280261 | 4vqwig6m5gsoc7ts2dljt55r6r7nybzr74uamzqctr3gq7o4mzcq | mean 1809 · sd 1095 · min 50 · max 14000 · 68% valid |
| level 3 tile 0,1 | · | 1866676 | 415022 | odcd3ncxfmppoqrdjqnfsiq4y2w7xiqmpqsuq545d7asci74lqoq | mean 1768 · sd 2461 · min 1 · max 17370 |
| level 3 tile 1,1 | · | 2281698 | 411142 | y5c64srg3zg77hvobzn32xmeli7rfcgsrjrwab5hwrf55l6j5vmq | mean 1761 · sd 1576 · min 1 · max 16960 |
| level 3 tile 2,1 | · | 2692840 | 251132 | e4bxu4ac533m6r26ve3vj5mioa6gpykn5wuwdxre6gadmspt7rqq | mean 2804 · sd 2120 · min 1 · max 15990 · 58% valid |
| level 3 tile 0,2 | · | 2943972 | 284966 | gfny674gxjb2skqj7iynizmughuwsebuozphvtzy72zdhu3lk2ea | mean 1997 · sd 2735 · min 1 · max 18030 · 68% valid |
| level 3 tile 1,2 | · | 3228938 | 278943 | dolib7vlthxendxipkehhlia2bn2ylraqlknb4t7qeuiodiqg2ba | mean 1372 · sd 1614 · min 1 · max 17060 · 68% valid |
| level 3 tile 2,2 | · | 3507881 | 110787 | wyemn2lmlhobu2cjiu6o26227bpicnl4qcjpz67xy67urt7zl47q | mean 1544 · sd 1485 · min 1 · max 15990 · 26% valid |
| level 4 tile 0,0 | · | 3562 | 423765 | nwnsrmvfjkxxdqmnh2cdio3ymdsfv7dhmy5nq5xvxar7emtfmuya | mean 2238 · sd 2118 · min 2 · max 16970 |
| level 4 tile 1,0 | · | 427327 | 137067 | jw2koroa6doktwwv2ogmvz33dodu62vs3vzlhial7pot2ob5vema | mean 2263 · sd 1606 · min 102 · max 11010 · 32% valid |
| level 4 tile 0,1 | · | 564394 | 143728 | uzpc5yuibd4j4o4a2ncz5t4dngcjn3uljn54c23ze3lmuy2crrda | mean 1684 · sd 2167 · min 2 · max 17050 · 34% valid |
| level 4 tile 1,1 | · | 708122 | 29797 | si2rxl5mq6luiwns47cwqm6x63osqsrnqsjk3kqhhapempc6stna | mean 1543 · sd 1375 · min 12 · max 12910 · 7% valid |
