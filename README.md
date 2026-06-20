# Kajota Witness

**Encrypted seller memory + AI jury for African micro-commerce disputes — all on 0G Galileo.**

A standalone Fastify service that gives Kajota Coach (a sales-assistant agent for African sellers) cross-session memory that the seller actually owns, and an AI jury that pulls those exact conversations from 0G Storage as evidence when a Mesh escrow dispute fires.

Built for [0G Zero Cup 2026 — Round 1](https://0g.ai/arena/zero-cup).

---

## Demo loop

```
seed 3 conversations → file a dispute → jury deliberates → verdict on chain
                                                              │
                                                              ▼
                                             https://storagescan-galileo.0g.ai/tx/<cid>
```

A buyer claims they ordered 6 wedding heels but only got 4. The system:

1. **Pulls evidence** — embedding search over the seller's prior chats; top‑K decrypted from 0G.
2. **Convenes a jury** — three LLM jurors (prosecutor / defender / neutral) argue in parallel, then a judge model issues a ruling.
3. **Writes the verdict** — encrypted, content-addressed, anchored on 0G with its own root hash.

Total time per dispute: **~22 seconds** (5.8s evidence + 1.6s jury + 14.9s verdict-write). Cost: **$0** (Groq free tier + 0G testnet).

---

## Why 0G actually does work (per Zero Cup rules)

> *"0G has to do real work in your app. If it runs the same without it, that's a bolt-on and it doesn't qualify."*

Witness has **no fallback storage layer**. Conversations have nowhere to live but 0G. Verdicts have nowhere to anchor but 0G. The seller's "I own my data" promise resolves to a 0G CID — there is no Postgres mirror to swap in, no S3 hedge, no IPFS fallback.

| 0G surface | Used for | Removing it |
|---|---|---|
| 0G Storage (`@0gfoundation/0g-storage-ts-sdk` v1.2.10) | Encrypted chat blobs + verdict blobs, content-addressed | App can't store memory or verdicts — system is dead |
| 0G Galileo chain (chainId 16602) | Settlement layer for storage transactions, root-hash anchoring | No way to prove the blob existed at a given time |

---

## Architecture

```
┌─────────────────┐    POST /memory     ┌─────────────────┐
│  Kajota Coach   │ ─────────────────►  │   Witness API   │
│  (demo client)  │   ChatBlob          │   (Fastify)     │
└─────────────────┘                     └────────┬────────┘
                                                 │
                              encrypt (AES-GCM)  │  embed (all-MiniLM-L6-v2)
                                                 ▼
                                        ┌─────────────────┐
                                        │  0G Storage     │  ← root hash returned
                                        │   (Galileo)     │  ← indexed locally
                                        └─────────────────┘
                                                 │
                                                 │ POST /dispute fires
                                                 ▼
┌──────────────────┐  evidence (decrypted)  ┌────────────────────┐
│  3-LLM jury      │ ◄──────────────────────│  Top-K retrieval   │
│  (Groq /         │  ────────────────────► │  by cosine sim     │
│   llama-3.3-70b) │  verdict synthesis     └────────────────────┘
└────────┬─────────┘
         │ encrypt → upload
         ▼
┌─────────────────┐
│  0G Storage     │  ← verdict root hash anchored
│  (verdict blob) │  ← evidence CIDs cited inside
└─────────────────┘
```

---

## Stack

| Layer | Choice | Why |
|---|---|---|
| Runtime | Node 22 + TypeScript | 0G SDK is TS-only |
| Server | Fastify 5 | Smallest competent server |
| 0G | `@0gfoundation/0g-storage-ts-sdk` | Official, indexed via Galileo Turbo |
| Crypto | `crypto` (Node built-in) | AES-256-GCM envelope |
| Embeddings | `@xenova/transformers` (all-MiniLM-L6-v2, 384 dims) | Runs in-process; no external embed API |
| Vector index | JSON file + cosine top-K | Hackathon scale; trivially replaceable |
| LLM | Groq `llama-3.3-70b-versatile` (OpenAI-compatible API) | ~1.5s for 4 calls; free tier |
| UI | Static HTML + Tailwind CDN + vanilla JS | No build step; 1 file |

---

## Quick start

```sh
git clone https://github.com/KaJota-inc/kajota-witness.git
cd kajota-witness
npm install
cp .env.example .env
# Edit .env: WITNESS_DEPLOYER_PK + GROQ_API_KEY
```

`.env` needs:

```ini
# 0G Galileo testnet
ZG_RPC_URL=https://evmrpc-testnet.0g.ai
ZG_INDEXER_URL=https://indexer-storage-testnet-turbo.0g.ai

# Wallet with testnet 0G — drip at https://faucet.0g.ai (0.1 0G/day)
WITNESS_DEPLOYER_PK=0x...

# Free tier at https://console.groq.com/keys
GROQ_API_KEY=gsk_...

PORT=4022
```

Then:

```sh
npm run hello         # round-trip a blob through 0G (de-risk SDK)
npx tsx src/probe-llm.ts   # 1-call Groq ping (de-risk LLM)
npx tsx src/test-memory.ts # seed 3 chats + run 3 retrieval queries
npx tsx src/test-jury.ts   # full 3-dispute jury smoke test
npm run start         # boot Fastify server
# open http://localhost:4022/ui
```

---

## API

| Route | Body / Query | Returns |
|---|---|---|
| `GET /` | — | Service banner + route list |
| `GET /health` | — | `{ok, ts}` |
| `GET /ui` | — | Static HTML demo page |
| `POST /memory` | `ChatBlob` | `WriteResult` — `{cid, txHash, storageScanUrl, chainScanUrl, summary}` |
| `GET /memory` | `?kind=chat\|verdict&sellerId=...` | `{entries: EntrySummary[]}` (sorted desc by ts) |
| `POST /evidence/query` | `{query, sellerId?, k?}` | `{query, count, hits[]}` — top-K with decrypted blobs |
| `POST /dispute` | `{sellerId, buyerId?, claim, evidenceQuery?, k?}` | `{verdict, evidence, onChain, timings}` |

---

## File map

```
src/
├── hello.ts                # SDK round-trip de-risk
├── probe-llm.ts            # Groq auth probe
├── server.ts               # Fastify routes
├── test-memory.ts          # 3-chat seed + retrieval smoke test
├── test-jury.ts            # 3-dispute end-to-end smoke test
├── lib/
│   ├── crypto.ts           # AES-256-GCM envelope (newKey/encrypt/decrypt/pack/unpack)
│   ├── embed.ts            # @xenova/transformers wrapper
│   ├── index-store.ts      # JSON file-backed embedding index
│   ├── jury.ts             # 3-juror + judge deliberation pipeline
│   ├── memory.ts           # MemoryService: writeChat / queryEvidence / writeVerdict / listEntries
│   └── og.ts               # 0G SDK wrapper: uploadBytes / downloadBytes
└── ui/
    └── index.html          # Single-page demo UI
```

---

## What's not in scope (yet)

- **Coach client patch** — Coach already exists ([KaJota-inc/kajota-coach](https://github.com/KaJota-inc/kajota-coach)) but for this round Witness is demoed via seeded chats. A 30-line client patch in Coach is the trivial next step.
- **Mesh escrow on-chain anchor** — verdict root hash is stored on 0G; the final step is anchoring it to the existing Mesh escrow contract on Mantle/Ethereum Sepolia for actual fund release. Architecturally clean, deferred for time.
- **Hybrid retrieval** — small MiniLM model + short chats sometimes misses on lexical edge cases (e.g. "shipping" vs "delivered"). Top-K=3 mitigates for the jury, but a BM25 + embedding hybrid is the proper fix.

---

## License

MIT.

---

## Repo conventions

Built start-to-finish during the Zero Cup tournament window — no pre-existing code. Submitted Mon Jun 22, 2026 to https://0g.ai/arena/zero-cup.

Co-author trail and milestone-by-milestone progress are in the commit history.
