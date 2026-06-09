---
name: document-compression-codex
description: Compress web pages, book chapters, technical manuals, case notes, lecture materials, papers, and other source documents with Codex judgment under a strict token budget. Use when preparing many documents for later domain learning, especially when the output must preserve decision material such as conditions, exceptions, failures, constraints, procedures, causality, warnings, exact numbers, units, tools, materials, and names. Includes tokenizer-guided final shortening and source-vs-output audit. Do not use for generic summarization.
---

# Document Compression Codex

Compress one source document into a reliable compact note for later reading or domain learning. Default gate:

- output tokens <= 20% of working source tokens
- required items retained = 100%
- important items retained >= 85%
- important numbers, units, names, materials, tools, and thresholds retained exactly = 100%
- serious judgment differences = 0

Scripts must not decide meaning. Scripts may count tokens or compare plain text only.

## Inputs

Use a file, pasted text, or extracted source as input. First build a working source by deleting low-value wrapper text with Codex judgment. Report both ratios when possible:

- ratio vs original input
- ratio vs working source

Delete by source type:

- web: navigation, ads, related links, duplicate calls to action, comments, SEO filler, author bio, cookie or subscription text
- book chapter: table of contents, index matter, publisher matter, repeated chapter framing, low-value footnotes, exercise answers unless they teach a rule
- manual: legal boilerplate, product marketing, repeated warnings, repeated UI steps, compatibility tables that do not affect the task
- case note: timestamps, signatures, duplicate logs, routine admin text, repeated symptom descriptions
- lecture material: agenda, learning-objective boilerplate, slide navigation, repeated recap text
- paper: metadata, title/authors, abstract, introduction, related work, references, acknowledgments when not needed for judgment

Keep source text that changes conditions, safety, failure interpretation, scope, or action.

## Workflow

1. Count tokens.
   - Prefer `scripts/count_tokens.py`.
   - Use the same tokenizer for source and output.
   - Set `target_tokens = floor(working_source_tokens * 0.20)`.

2. State what the document is useful for in one line.
   - This is not a summary headline.
   - It should name the practical judgment the source can improve.

3. Build the must-keep list before compressing.
   - Mark each item as `required`, `important`, or `optional`.
   - `required` items must all survive.
   - Keep items that affect a decision, action, diagnosis, design, safety call, or claim strength.

4. Must-keep item types:
   - conditions where the claim or method holds
   - exceptions and edge cases
   - failures, symptoms, traps, and warning signs
   - constraints, limits, prerequisites, and assumptions
   - procedures, sequence, mechanisms, and causal links
   - numbers, units, thresholds, settings, tolerances, dates, counts
   - materials, tools, machines, models, datasets, named methods
   - comparisons, baselines, alternatives, and exclusion tests
   - source scope: who, where, when, sample, domain, and setting
   - what to trust, ignore, test next, or avoid overclaiming

5. Build the exact-retention list.
   - Include important numbers with units, material names, tool names, machine names, settings, thresholds, tolerances, failure labels, warning labels, model names, source-specific terms, and proper names.
   - Exclude page numbers, citation numbers, decorative labels, and bibliographic years unless they affect judgment.

6. Compress into the fixed output shape.
   - Preserve meaning; do not add claims.
   - Use dense bullets or short labeled lines.
   - Remove background, repeated motivation, rhetorical transitions, long examples, low-value anecdotes, and duplicated explanations first.
   - Merge repeated setup/result/procedure lines.
   - Keep uncertainty and scope words such as `may`, `can`, `only`, `unless`, `in this setting`, `limited`, `not proven`, and `warning` when they affect judgment.

```text
what_it_is:
what_to_trust:
conditions:
procedure_or_mechanism:
numbers_and_settings:
failures_and_warnings:
limits:
source_scope:
```

7. Apply tokenizer-guided final shortening.
   - Count tokens before this pass.
   - Work sentence by sentence or bullet by bullet.
   - For replaceable phrases, write 2-5 same-meaning candidates and count with `scripts/count_tokens.py --text`.
   - Use the shortest candidate only when it preserves meaning, scope, uncertainty, polarity, causality, numbers, names, units, and warnings.
   - Prefer short active verbs: `is used to` -> `uses`, `is able to` -> `can`, `make it possible to` -> `enable`, `in order to` -> `to`, `due to the fact that` -> `because`.
   - Delete stop words only when meaning survives: filler adverbs, repeated subjects, empty `there is/are`, unnecessary `that`, and articles like `a`, `an`, `the`.
   - Trim prepositions and conjunctions only in compressed labels or telegraphic bullets where the relation stays clear.
   - Do not delete negation, hedges, comparators, time/scope markers, causal links, limitations, warnings, numbers, units, proper names, materials, tools, or method labels.
   - Count tokens after this pass and keep before/after counts for audit.

8. If output exceeds target tokens.
   - Remove optional items first.
   - Merge repeated conditions or procedure lines.
   - Shorten wording, not facts.
   - Remove background before failures, warnings, limits, settings, or sequence.
   - Never drop required items, exact-retention items, safety warnings, or scope limits to hit budget.

9. Audit against the source.
   - Count output tokens.
   - Check each required item is present.
   - Score important items as `kept/total`.
   - Check exact numbers, units, names, materials, tools, and thresholds.
   - Compare source and output answers to the judgment questions.

## Judgment Questions

1. What can this source help someone decide or do?
2. Under what conditions does it apply?
3. What sequence, mechanism, or causal link matters?
4. What failures, exceptions, warnings, or limits change the decision?
5. What should a reader trust, ignore, test next, or avoid overclaiming?

A serious judgment difference makes the reader take the wrong action, trust the wrong claim, miss a major condition or warning, choose the wrong method, misunderstand evidence strength, or repeat a known failure.

## Audit Report

Return or save:

```text
source_tokens:
working_source_tokens:
output_tokens:
token_ratio:
final_shortening_tokens_before:
final_shortening_tokens_after:
required_items:
important_items:
numbers_names_units:
warnings_limits:
serious_judgment_differences:
status:
weak_result:
```

Use `status: pass` only when all gates pass. If one gate fails, use `status: fail` and name the failed gate.

## Subagents

If subagents are available and the user allows or expects them, use two roles:

- compressor: create the compressed output from the source and must-keep list.
- auditor: compare source and output, then report missing required items, changed numbers/units/names, missing warnings/limits, token ratio, and judgment differences.

Do not give the auditor the intended answer beyond source, output, and gates.
