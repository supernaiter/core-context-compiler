# Audit: SSI review compression batch 54-79

- range: reviews[54:80] / index 54-79
- count: 26
- output_file: reports/ssi_all_context_framework/compressed/batch_54_79.md
- tokenizer: gpt-4o-mini via `.venv/bin/python`

## token ratio

- source_raw_json_tokens: 48133
- source_selected_json_tokens: 34876
- source_reviews_flat_tsv_tokens: 14411
- output_tokens: 5559
- ratio_raw_json_to_output: 8.7:1 / output 11.6%
- ratio_selected_json_to_output: 6.3:1 / output 15.9%
- ratio_reviews_flat_tsv_to_output: 2.6:1 / output 38.6%
- note: reviews_flat.tsv は判断材料だけの既圧縮入力なので、20% gate ではなく 120-220 tokens/paper 目安との整合を優先した。
- final_shortening_tokens_before: 7049
- final_shortening_tokens_after: 5559
- per_item: average 214 tokens; long title/slug papers can exceed 220 by tokenizer, but evidence body was shortened.

## retained

- title/year/slug: all 26 retained.
- venue: retained once globally because all 26 are `arXiv / imported corpus page`.
- trust: all 26 retained.
- task/input/output/body site/sensor: retained when present in source; blank or out-of-scope cases kept as domain labels rather than invented fields.
- core metrics/numbers: retained for WER, PER, CER, MSE, MCD, R2, STOI/ESTOI/PESQ, SI-SNRi/SDRi, VAD/F1/AUC, latency, sample counts, participant counts, dataset splits, JND settings, and headline percentage changes.
- conditions: retained dataset names and evaluation modes including USC-TIMIT, USC-EMO-MRI, TaL1/TaL80, GRID, TAL1, MUSDB18, NTT EMA, UXTD/UPX, VoiceBank-DEMAND, DEMAND, AudioSet, MUSIC, ESC-10/ESC-50.
- limits: retained technical, evaluation, deployment, and scope limits, especially one-speaker/small-vocabulary/offline/no-real-time/no-deployment/out-of-SSI constraints.

## possibly dropped

- authors, URLs, DOI, evidence source paths, section labels, evidence confidence values, tags, and repeated bibliographic scaffolding.
- duplicate restatements of the same limitation across technical/evaluation/deployment/scope fields.
- some secondary metric lists for out-of-scope audio papers after the main metric set was preserved.
- some exact hardware brand/model wording where it did not change the judgment, except key ultrasound/EMA/acoustic/EEG/rtMRI identifiers.
- long background contrast prose and canon-before language when delta/change_view preserved the decision-relevant contrast.

## numbers_names_constraints

- exact numeric retention: pass for decision-critical values checked during final pass.
- proper-name retention: pass for title, slug, dataset names, method names, and main model names.
- constraints retention: pass for single-speaker, speaker-dependent, closed-vocabulary, no-cross-session, no-real-time, lab-bound, out-of-SSI, and review-only constraints.
- serious_judgment_differences: none detected.
- weak_result: ratio vs reviews_flat.tsv is above 20% because the TSV is already stripped judgment material; output still matches the requested per-paper compression target closely.
