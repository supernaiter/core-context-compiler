# Audit: SSI Review Compression Batch 00-26

- range: reviews[0:27] / index 0-26
- count: 27
- output: reports/ssi_all_context_framework/compressed/batch_00_26.md
- source_used:
  - reports/ssi_all_context_framework/ssi-review.json
  - reports/ssi_all_context_framework/reviews_flat.tsv
- tokenizer: gpt-4o-mini via paper-compression-codex count_tokens.py

## Token Ratio

- source_tokens_json_reviews_0_26: 56921
- source_tokens_reviews_flat_rows_0_26: 22105
- output_tokens_compressed: 7059
- source/output_json: 8.06:1
- output/source_json: 12.40%
- source/output_flat: 3.13:1
- output/source_flat: 31.93%
- per_item_body_tokens_excluding_title_id_trust: min 171 / max 221 / avg 201
- per_item_total_tokens_including_title_id_trust: min 219 / max 288 / avg 261
- weak_result: full item totals exceed 220 for many entries because required titles, long slugs, venue, and trust are retained; judgment body is within the intended 120-220 range except index 21 at 221.

## Retention Check

- title/year/venue/slug: kept for all 27.
- required fields: every item keeps trust, did, evidence, conditions, limits, changes_view.
- core judgment: expert_true_value, delta_from_canon, position_in_field, task, modality, sensor/body site, output, metrics/evaluation, limits, and field-position implications were retained as compressed claims.
- numbers/names retained: high-priority numeric results, dataset sizes, participant counts, sensor names, model names, dataset names, and key metrics were preserved where present.
- scaffolding dropped: authors, URLs, DOI/arXiv links, repeated tags, long expert_take prose, canon background when redundant, evidence_source paths, source_ref, section locations, and repeated limitations.

## Possible Important Loss

- Full confidence intervals and some table-level metric variants were omitted when the review only needed the decision-relevant best or representative numbers.
- Some secondary ablation details were collapsed, especially for AKVSR, AV2A, LipVoicer, speech-unit L2S, and audio pretraining.
- Exact p-values, null-test details, and per-architecture mapping scores in the MEG zero-shot paper were not kept.
- Some subjective-test protocol details were shortened when counts and metrics were preserved.
- Deployment limits were merged across technical/evaluation/deployment/scope categories, so the original category boundaries are less explicit.

## Numbers / Names / Constraints

- Preserved examples: 1020 h, 955 GB, 17 subjects, 76 words, 157-channel MEG, -10 to 10 dB, 50 evaluators, FERASEC accuracies, gauge factor 317, 10,000 cycles, 21.5%/41.7% WER improvements, LRS2/LRS3 WERs, GRID/TCD-TIMIT/LRW metrics, STN 75-76%/88%/92%/87%, GRID 33 speakers, AV Digits 39 speakers, 6.66% VER, 9.97% WER.
- Preserved proper names: ReSSInt, JapanEEG, OpenNeuro/BIDS, g.Pangolin, g.SCARABEO, eego sports, Whisper Large-v2/v3, HuBERT, Wav2Vec2, BERT, AV-HuBERT, FERASEC, BITalino MuscleBIT, MusicVAE, Diff-Foley, CAVP, Unit HiFi-GAN, SyncNet, Dlib.
- Preserved constraints: closed vocabulary, n=3, n=5, 10 phrases, 20-word max, no real-time/mobile, no open vocabulary, no in-the-wild, no speaker-independent proof, simulation-only, benchmark-only, single-speaker Chem, GRID constrained grammar, controlled read-speech or controlled ultrasound sessions.
- serious_judgment_differences: none found in manual audit; compressed text should not make a reader trust a deployment, generalization, or SSI relevance claim stronger than the source supports.

## Status

- status: pass_with_note
- note: Meets assigned count/range and retains decision material. Per-item total token counts are above 220 for many entries only because required metadata scaffolding is counted; compressed judgment bodies stay near target.
