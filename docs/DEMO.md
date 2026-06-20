# Kajota Witness — 3-minute demo script

For recording a screencast you can paste into the 0G Arena submission form. Target: **3 minutes flat.** Each numbered beat below = ~20-30 seconds of screen time.

---

## Before you hit record

- [ ] `cd ~/Documents/kajota-witness && npm run start` — wait for `kajota-witness listening on http://localhost:4022`
- [ ] Open `http://localhost:4022/ui` in a fresh browser window
- [ ] Open a second tab to `https://storagescan-galileo.0g.ai` (you'll click into it mid-demo)
- [ ] Open a third tab to `https://chainscan-galileo.0g.ai/address/0x2f1D3a881cfbeA01Cf55f3cAd125aA32Bf8cEC94` (the WitnessAnchor contract page)
- [ ] Browser at ~125% zoom; window 1280×800
- [ ] Mute Slack/Discord/notifications
- [ ] Use Loom, OBS, or QuickTime (anything that captures system audio + mic)

---

## Script

### **00:00 – 00:25 — The problem (15s of footage, 25s of voiceover)**

**Show:** Kajota Coach in another tab, OR just the Witness UI's header.

**Say:**
> "In African micro-commerce, sellers chat with buyers across WhatsApp, Instagram, and direct DMs. When something goes wrong — wrong size shipped, partial order, pricing dispute — there's no record either side can prove. The platform owns the data, not the seller. And when escrow fires, there's no neutral way to decide who's right."

### **00:25 – 00:55 — The Memory layer (30s)**

**Show:** Witness UI at `/ui`. Point at the 3 (or 4) cards in the Memory panel.

**Say:**
> "Kajota Witness gives sellers cross-session memory they actually own. Every conversation is encrypted client-side and uploaded as a content-addressed blob to 0G Storage. Each card here is one chat. Each CID is real — let me click one."

**Action:** Click any chat's CID link → opens the 0G storagescan tx page in tab 2.

**Say:**
> "There it is on 0G Galileo. Permanent, content-addressed, verifiable by anyone — even if Kajota disappears."

### **00:55 – 01:20 — Seed a new chat live (25s)**

**Show:** Back to UI. Click `+ Seed a new conversation`. Paste the prepared messages.

**Pre-prepared seed payload to paste into the messages textarea:**
```
buyer: Hi, do you have the leather sandals in size 39?
seller: Yes, ₦6,000 with same-day Lagos delivery.
buyer: Can you do ₦5k?
seller: ₦5.5k flat — that's my final.
buyer: OK deal. Sending now.
```

**Say:**
> "Watch — I'll create a new conversation live. Topic: `sandals-haggling`. Seller and buyer agree at five-point-five-k. Hit 'Save to 0G'."

**Action:** Click Save. Wait ~20s for the upload spinner. The new card appears at the top of the Memory panel.

**Say:**
> "Encrypted, uploaded, indexed for retrieval — all in twenty seconds. Now there's evidence."

### **01:20 – 02:00 — File a dispute, convene the jury (40s)**

**Show:** The Court panel on the right.

**Pre-prepared dispute claim to paste into the claim textarea:**
```
The seller said ₦6,000 for the sandals and refused to give me any discount.
```

**Action:** Paste claim, click "Convene jury".

**Say:**
> "Now the buyer claims the seller wouldn't negotiate. We file the dispute. Witness does three things: pulls the most relevant chats from 0G as evidence, runs three LLM jurors in parallel — prosecutor, defender, neutral — and a judge model synthesizes the ruling. The jury sees the actual chat — not summary, not screenshot — the real decrypted blob."

**Action:** Wait ~40s for the verdict card to appear.

### **02:00 – 02:35 — The verdict (35s)**

**Show:** The verdict card. Read out the ruling badge at the top, scroll through the three juror arguments.

**Say:**
> "Verdict: release to seller, ninety percent confident. Look at the reasoning — the prosecutor, defender, and neutral analyst each cite the exact chat where the seller dropped from six-k to five-point-five. Their disagreement is on the record. The judge synthesizes."

**Action:** Scroll to the evidence section. Point at the CIDs.

**Say:**
> "Every piece of evidence the jury used is linked by its 0G CID. Anyone reading this verdict later can fetch the same blobs and re-run the deliberation themselves."

### **02:35 – 03:00 — On-chain anchor (25s)**

**Show:** The indigo "Verdict anchored on 0G Chain" badge.

**Action:** Click the on-chain tx link → opens chainscan tab.

**Say:**
> "And the verdict isn't just stored — it's anchored on 0G Chain. Our WitnessAnchor contract records the dispute ID, the verdict root hash, the ruling, and the confidence. The root on chain is byte-identical to the storage CID. No server trust required. If Kajota's backend went away tomorrow, the verdict still exists, still verifiable, still on chain."

**Action:** Briefly switch to the contract page (tab 3). Show the events tab.

**Say:**
> "Built end-to-end in 36 hours for 0G Zero Cup. Three real 0G surfaces — Storage, Chain transactions, and a deployed contract — each doing work the app can't run without."

---

## Things NOT to do on camera

- Don't open `.env` — even glancing at it on screen leaks the wallet PK
- Don't refresh the UI mid-demo (loses the verdict card state)
- Don't run the seed → dispute back-to-back too fast — the upload takes ~20s and the dispute takes ~40s; the spinner is the proof it's doing real work
- Don't apologize for latency — name it ("each upload is a real Galileo storage tx; this is what real settlement looks like")

## If something breaks during recording

- **Server crashes:** stop, restart `npm run start`, redo from the seed step (don't try to mid-stream recover)
- **Groq rate-limit:** wait 30s, retry the dispute (you'll see a 429 in the dispute card)
- **0G upload times out:** rare; redo the seed
- **No anchor badge:** check `.env` has `WITNESS_ANCHOR_ADDRESS=0x2f1D3a88…cEC94`

## Backup demo dispute prompts (if your first one verdicts weirdly)

> The seller agreed to 6 pairs but only sent 4.

> I paid ₦11k for trainers and they never arrived.

> The seller charged ₦14k but we agreed on ₦12k.

All three resolve cleanly against the seeded chats.

## Reference artifacts to mention on-camera

- WitnessAnchor contract: `0x2f1D3a881cfbeA01Cf55f3cAd125aA32Bf8cEC94`
- 0G Galileo (chainId 16602)
- Free testnet faucet: https://faucet.0g.ai

## What to caption / pin in the video description

```
Kajota Witness — encrypted seller memory + AI jury on 0G Galileo.
Built in 36 hours for 0G Zero Cup Round 1.

Repo: https://github.com/KaJota-inc/kajota-witness
Contract: https://chainscan-galileo.0g.ai/address/0x2f1D3a881cfbeA01Cf55f3cAd125aA32Bf8cEC94

Stack: Node + TypeScript + Fastify + 0G Storage SDK + Groq llama-3.3-70b-versatile
Three 0G surfaces, each load-bearing: Storage (blobs) + Chain txs + on-chain commitment.
```
