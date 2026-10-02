// One evidence sequence, shared by the browser and its accessible transcript.
export function tourSteps({ V, blake3, receive, rec, fact, bundle, M }) {
  const refused = receive({kind:'ref', token:bundle.token, bytes:M.m3});
  const genuine = receive({kind:'ref', token:bundle.token, bytes:fact});
  if (refused.verdict !== 'REFUSED' || refused.layer !== 'L0' || !genuine.checked) throw new Error('tour receiver check failed');
  const reference = `emem:fact:${V.parseToken(bundle.token).cell}:${V.b32e(blake3(fact))}`;
  if (reference !== bundle.token) throw new Error('reference differs from the saved record');
  return [
    {title:'Observe', text:`Keylong NDVI ${rec.value}; Sentinel-2 L2A, 25 Sep 2026. One saved observation.`},
    {title:'Construct the reference', text:reference},
    {title:'Mutate the value', text:`0.4708994708994709 → 0.47089947089947093. Change byte ${M.off+7}; keep the original token.`},
    {title:'Resolve and re-hash', text:`Expected record: ${V.parseToken(bundle.token).cid}\nReceived bytes: ${V.b32e(blake3(M.m3))}\nThe content identifiers differ.`},
    {title:'Refuse the changed record', text:V.verdictLine(refused), verdict:refused.verdict},
    {title:'Resolve the genuine reference', text:`${V.verdictLine(genuine)}\nExact value: ${rec.value}. Record integrity, declared identity and derivation checked; source accuracy is inherited.`, verdict:genuine.verdict},
  ];
}
