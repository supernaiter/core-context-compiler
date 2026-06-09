---
name: paper-compression-codex
description: Compress academic papers or paper-like technical documents with Codex judgment when the user needs an output within a strict token budget, especially targets like at most 20% of source tokens while preserving important methods, data, results, limits, numbers, and names. Use for per-paper compression, paper body shortening after metadata/section stripping, tokenizer-guided final wording reduction, and audits of token ratio, retained important items, exact numeric/proper-name retention, and serious judgment differences. Do not use for generic summarization.
---

# Paper Compression Codex

Use Codex judgment to compress one paper under a hard token budget. The default gate is:

- output tokens <= 20% of source tokens
- important items retained >= 85%
- important numbers and proper names retained exactly = 100%
- serious judgment differences = 0

Do not let scripts decide what paper content to remove. Scripts may count tokens or compare plain text only.

## Inputs

Use the user's file or pasted text as the source. If the input is a raw paper with title, authors, abstract, references, boilerplate, or metadata, first create a working source by deleting those formal parts with Codex judgment. Report both ratios when possible:

- ratio vs original input
- ratio vs working source

If the user already provides a stripped body, treat it as the source.

## Workflow

1. Count source tokens.
   - Prefer `scripts/count_tokens.py` from this skill.
   - Use the same tokenizer for source and output.
   - Set `target_tokens = floor(source_tokens * 0.20)`.

2. Build the must-keep list before compressing.
   - Read the source once.
   - List only items needed to understand or judge the paper.
   - Mark each item as `required`, `important`, or `optional`.
   - Keep `required` items out of the 85% score; they must all survive.

3. Must-keep item types:
   - problem or research question
   - main claim or contribution
   - method, algorithm, mechanism, or design
   - data, corpus, participants, materials, or sample
   - experimental setup, conditions, baselines, comparisons
   - metrics and evaluation method
   - main results and negative results
   - ablations, sensitivity checks, or robustness checks
   - limitations, assumptions, failures, and threats to validity
   - scope where the claim does and does not apply
   - definitions, notation, named variants, datasets, systems, and benchmarks

4. Build the exact-retention list.
   - Include important numbers with units, percentages, counts, settings, thresholds, dates, table labels, figure labels, model names, dataset names, method names, named metrics, and paper-specific terms.
   - Exclude page numbers, citation numbers, reference list details, and purely bibliographic years unless they affect the paper's claim.

5. Compress.
   - Use dense bullets or short paragraphs.
   - Preserve the paper's meaning; do not add claims.
   - Keep exact names and numbers unchanged.
   - Remove background, repeated motivation, citation scaffolding, long examples, rhetorical transitions, and duplicated explanations first.
   - Replace repeated prose with one precise statement when the evidence is still clear.
   - Keep uncertainty words such as "may", "can", "in this setting", "on this dataset", "preliminary", and "limitation" when they affect judgment.

6. Apply the final token-shortening pass.
   - Count tokens before this pass.
   - Work sentence by sentence or bullet by bullet.
   - For each replaceable phrase, write 2-5 same-meaning candidates and count them with `scripts/count_tokens.py --text`.
   - Use the shortest candidate only when it preserves meaning, scope, uncertainty, polarity, numbers, names, units, and limits.
   - Prefer short active verbs: `is used to` -> `uses`, `is able to` -> `can`, `make it possible to` -> `enable`, `in order to` -> `to`, `due to the fact that` -> `because`.
   - Delete stop words only when meaning survives: filler adverbs, repeated subjects, empty `there is/are`, unnecessary `that`, and articles like `a`, `an`, `the`.
   - Trim prepositions and conjunctions only in compressed labels or telegraphic bullets where the relation stays clear.
   - Choose fewer-token equivalents for the same meaning; verify with the tokenizer instead of guessing from character length.
   - Do not delete negation, hedges, modals, comparators, time/scope markers, causal links, limitations, warnings, proper names, numbers, units, or dataset/method labels.
   - Count tokens after this pass and keep the before/after counts for the audit.

7. If output exceeds target tokens.
   - Remove optional items first.
   - Merge repeated setup/result bullets.
   - Shorten wording, not facts.
   - Remove non-actionable future work before methods, results, or limits.
   - Never drop a required item, important number, or important name to hit the budget.

8. Audit against the source.
   - Count output tokens.
   - Check each required item is present.
   - Score important items as `kept/total`.
   - Check important numbers and proper names exactly.
   - Answer the judgment questions from source and output, then compare.

## Judgment Questions

Use these questions for the serious judgment difference check:

1. What did the paper actually do?
2. What evidence supports the main claim?
3. Under what data, setting, or assumptions does the claim hold?
4. What are the main weaknesses, failures, or limits?
5. What should a researcher or builder trust, ignore, or test next?

A serious judgment difference is any answer from the compressed text that would make a reader trust the wrong claim, miss a major limit, pick the wrong method, misunderstand the evidence strength, or repeat a known failure.

## Pass Report

Return or save a short audit with this shape:

```text
source_tokens:
target_tokens:
output_tokens:
token_ratio:
final_shortening_tokens_before:
final_shortening_tokens_after:
required_items:
important_items:
important_item_retention:
numbers_names:
serious_judgment_differences:
status:
weak_result:
```

Use `status: pass` only when all gates pass. If one gate fails, use `status: fail` and name the failed gate.

## Subagents

If subagents are available and the user allows or expects them, use two roles:

- compressor: create the first compressed output from the source and must-keep list.
- auditor: compare source and output, then report missing required items, changed numbers/names, token ratio, and judgment differences.

Do not give the auditor the intended answer beyond the source, output, and gates.
