//! Local probe (not part of emem): does an enrolled device key reach the fact
//! store without a trace through the ungated `Storage::put_attestation`, which
//! is the method `POST /v1/attest_cbor` calls (emem-api-rest lib.rs ~20658),
//! while `POST /v1/attest` and `/v1/attest_traced` call `put_attestation_gated`?
//! Same key, same facts and same helpers as the SAT-042 example.
use std::sync::Arc;
use ed25519_dalek::SigningKey;
use emem_core::key::{AttesterKey, KeyEpoch};
use emem_fact::{Attestation, Derivation, Fact, PrimaryFact, RegistryCid, SchemaCid, Source};
use emem_storage::{MaterializingStorage, Storage};

const PROFILE: &str = "orbital.satellite.v1";
const BAND: &str = "indices.ndvi";

#[tokio::main(flavor = "current_thread")]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let storage = MaterializingStorage::ephemeral(
        Arc::new(emem_core::bands::DEFAULT.clone()),
        Arc::new(emem_core::FunctionRegistry::parse_default()?),
        Arc::new(emem_core::SourceRegistry::parse_default()?),
    )?;
    let gate = storage.trace_gate.clone().expect("trace gate");
    let registry_cid = RegistryCid::new(emem_core::manifest_cid(&*emem_core::bands::DEFAULT)?);
    let schema_cid = SchemaCid::new(emem_core::manifest_cid(&*emem_core::schema::DEFAULT)?);
    let mut secret = [0u8; 32];
    secret[..7].copy_from_slice(b"SAT-042");
    let sk = SigningKey::from_bytes(&secret);
    let pubkey = sk.verifying_key().to_bytes();
    let pubkey_b32 = data_encoding::BASE32_NOPAD.encode(&pubkey).to_lowercase();
    gate.enroll(&pubkey_b32, PROFILE)?;
    let cell = emem_codec::cell64_from_latlng(30.7901, 31.0007);
    let att = Attestation::build_and_sign_v1(
        vec![mk_fact(&cell, 0.6431, pubkey, &schema_cid)], vec![], registry_cid, schema_cid,
        &sk, KeyEpoch(0), "2026-07-26T09:41:00Z".into(), None,
    )?;
    println!("enrolled {pubkey_b32} under {PROFILE}");
    match storage.put_attestation_gated(&att, None).await {
        Ok((c, _)) => println!("put_attestation_gated, no trace: ADMITTED {} fact(s)", c.len()),
        Err(e) => println!("put_attestation_gated, no trace: REFUSED: {e}"),
    }
    match storage.put_attestation(&att).await {
        Ok(c) => println!("put_attestation (ungated), no trace: ADMITTED {} fact(s): {}", c.len(), c.iter().map(|x| x.as_str().to_string()).collect::<Vec<_>>().join(",")),
        Err(e) => println!("put_attestation (ungated), no trace: REFUSED: {e}"),
    }
    Ok(())
}

fn mk_fact(cell: &str, ndvi: f64, pubkey: [u8; 32], schema_cid: &SchemaCid) -> Fact {
    Fact::Primary(PrimaryFact {
        cell: cell.into(), band: BAND.into(), tslot: 12, value: ciborium::Value::Float(ndvi),
        unit: None, confidence: 0.98, uncertainty: None,
        sources: vec![Source { scheme: "operator.downlink".into(), id: "SAT-042/pass-1881".into(), cid: None, hash: None, captured_at: Some("2026-07-26T09:38:12Z".into()), url: None }],
        derivation: Derivation { fn_key: "ndvi@1".into(), args: None },
        privacy_class: "public".into(), schema_cid: schema_cid.clone(), signer: AttesterKey(pubkey),
        signed_at: "2026-07-26T09:41:00Z".into(), served_via: None,
    })
}
