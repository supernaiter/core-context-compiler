# Audit: SSI review compression batch 27-53

- count: 27 reviews, indices 27-53 inclusive.
- source: `reports/ssi_all_context_framework/ssi-review.json` reviews[27:54].
- method: paper-compression-codex style compression of paper-like technical review material; paper metadata/list scaffolding, authors, URLs, DOIs, source paths, repeated tags, and duplicate limitation wording were removed.
- per-item target: roughly 120-220 tokens; longer entries kept extra numbers where the source had deployment-relevant metrics.
- source/output token ratio: measured after writing; see counts below.

## Possible Important Drops

- Some secondary baseline rows and ablation details were compressed to headline comparisons only.
- Full evidence confidence values and `evidence_kind`/`section_or_location` scaffolding were dropped except where the section implied a critical condition.
- Author lists, URLs, DOI/arXiv IDs, raw source paths, and duplicate tag vocabulary were dropped by design.
- Some subjective-study details were collapsed when participant/sample counts and headline results were preserved.

## Numbers, Names, And Constraints

- Preserved: all title/year/venue/slug identifiers; review trust; task/input/output modality; sensor/body-site where meaningful; headline datasets; headline metrics; major sample counts; real-time/latency values; deployment constraints.
- Preserved examples: LipLearner 0.8947 F1, 81.7%/98.8%, EER 6.75%, 422 ms; SilentSpeller 124 electrodes, 100 Hz, 37 wpm, 87%, 53 wpm, 91%; SSRNet CER 21.99% +/- 4.99%, 6.41%, 1.19%; SVTS dataset hours and GRID/LRW values; WESPER WER/CER values.
- Known compression risk: if a later analysis needs exact full baseline tables, use the source JSON/full text; this batch keeps decision-grade evidence, not full table reconstruction.

## Counts

- source_tokens_raw_json_reviews_27_53: 47931
- source_tokens_reviews_flat_rows_27_53: 17488
- output_tokens_compressed_md: 6184
- audit_tokens: 618
- output/source token ratio: 12.9% vs raw JSON; 35.4% vs `reviews_flat.tsv` judgment-material rows.
- source/output token ratio: 7.75:1 vs raw JSON; 2.83:1 vs `reviews_flat.tsv` judgment-material rows.
- numbers_names: headline numbers/proper names retained; source paths/authors/URLs intentionally omitted.
- serious_judgment_differences: none found in manual source-vs-output pass.
- status: pass for requested 27-item compression; weak result: average compressed tokens are about 229 per item including required labels/headings, slightly above the 120-220 guide because dense metric/deployment numbers were retained.
