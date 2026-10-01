#!/usr/bin/env python3
"""Independently verify the A2A v1.0 JWS signature on https://emem.dev/.well-known/agent-card.json.
No emem code used: RFC 8785 JCS (rfc8785 pkg) + RFC 7515 detached JWS + Ed25519 (pynacl)."""
import json, base64, urllib.request, rfc8785, nacl.signing, sys
def b64d(s): return base64.urlsafe_b64decode(s + '=' * (-len(s) % 4))
def b64e(b): return base64.urlsafe_b64encode(b).rstrip(b'=')
card = json.load(urllib.request.urlopen('https://emem.dev/.well-known/agent-card.json'))
sigs = card.pop('signatures')
jwks = json.load(urllib.request.urlopen('https://emem.dev/.well-known/jwks.json'))
payload = rfc8785.dumps(card)
for s in sigs:
    hdr = json.loads(b64d(s['protected']))
    key = next(k for k in jwks['keys'] if k['kid'] == hdr['kid'])
    vk = nacl.signing.VerifyKey(b64d(key['x']))
    signing_input = s['protected'].encode() + b'.' + b64e(payload)
    try:
        vk.verify(signing_input, b64d(s['signature'])); ok = True
    except Exception as e:
        ok = False
    print('header', hdr); print('payload_bytes', len(payload), 'verify', ok)
    # tamper test
    card2 = dict(card); card2['version'] = card['version'] + 'x'
    si2 = s['protected'].encode() + b'.' + b64e(rfc8785.dumps(card2))
    try: vk.verify(si2, b64d(s['signature'])); print('tamper verify True (BAD)')
    except Exception: print('tamper verify False (expected)')
