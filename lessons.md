2026-06-04T09:11:46+09:00 | v1 gate can run end-to-end while still failing quantitative release criteria; keep run success separate from release pass.
2026-06-04T09:19:10+09:00 | Source-id-only verification plus query-conditioned loadout can pass score-per-token without proving absolute token inversion.
2026-06-04T10:02:46+09:00 | CLI console scripts need setuptools package-dir when package code lives under src/.
2026-06-06T10:11:11+09:00 | If ruff hangs in uninterruptible state, record the incomplete verification explicitly instead of claiming a pass.
2026-06-06T10:52:46+09:00 | Before running ruff again, inspect and clear any existing uninterruptible ruff processes when the OS allows it.
2026-06-06T13:56:27+09:00 | If pytest hangs without a test summary for several minutes, terminate it and record verification as incomplete.
2026-06-06T15:02:47+09:00 | Run long verification with an explicit timeout and record timeout as incomplete, not failed.
2026-06-06T15:32:53+09:00 | Context edit history needs two layers: Git for batch versioning and context_audit.jsonl for individual rule reasons.
2026-06-06T16:44:00+09:00 | Core policy should make decision impact and baseline subtraction admission criteria, not after-the-fact compression preferences.
2026-06-06T19:28:02+09:00 | If Python import or pytest hangs before a summary, record the hang as incomplete verification and use py_compile plus diff checks as fallback evidence.
2026-06-06T20:31:23+09:00 | Enforce Policy v2 at both admission and runtime output boundaries so direct renderer calls cannot bypass core eligibility.
2026-06-06T22:25:08+09:00 | Treat centrality or placement effect as a required core-context admission field; decision impact alone does not prove worldview value.
2026-06-07T01:31:31+09:00 | When uv pytest hangs, retry target tests with PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 using .venv/bin/python before marking pytest incomplete.
2026-06-07T02:37:34+09:00 | Do not claim ruff verification when ruff enters STAT UE; record PID and use py_compile plus pytest as fallback evidence.
2026-06-07T03:47:59+09:00 | If targeted pytest hangs after a prior pass, add a direct PYTHONPATH smoke assertion for the changed behavior and record the pytest rerun as incomplete.
2026-06-07T04:49:04+09:00 | If uv run ruff hangs during package build, record it separately from direct ruff UE and keep pytest plus py_compile evidence explicit.
2026-06-07T07:18:00+09:00 | Keep audit-only CLI imports lazy so context-audit workflows do not pay heavy evaluation imports.
2026-06-08T00:00:00+09:00 | Paper stripping can remove known sections by headings, but cannot reliably separate introduction from body when no later section boundary exists; prefer heading-bounded deletion and keep this limitation explicit.
2026-06-08T08:59:00+09:00 | For arXiv smoke, count source fetch success separately from source usability; latex-heavy source archives should fall through to ar5iv HTML or PDF when the existing stripper empties them.
2026-06-09T12:08:03+09:00 | R2'c lossless final output can be larger than source text and the guard can corrupt paper terms such as KDE-SSI -> DE-SSI; do not treat "lossless" as safe without direct diff checks.
2026-06-09T12:48:20+09:00 | Subagent compression audits can be optimistic; verify exact missing numbers/names manually before claiming a 20% paper-compression pass.
2026-06-09T14:57:18+09:00 | Always rerun the repo token counter on subagent compression outputs; the first SottoVoce subagent audit claimed 762 tokens but the actual count was 1130 before correction.
2026-06-09T15:09:35+09:00 | Token-shortening passes can silently drop caveats; the SottoVoce audit first lost "difference unclear", so final shortening needs a source-vs-output judgment audit.
2026-06-09T15:55:09+09:00 | Generic document compression must preserve concrete symptom combinations; BTA audits failed until pressure/chip/pad/runout/material-inclusion traps were restored.
2026-06-10T13:53:29+09:00 | For persona/chatbot work, cleaned chats and speakerless text exports can destroy style evidence; use raw current_node JSON paths and keep user/assistant roles explicit.
2026-06-10T13:53:29+09:00 | In this workspace, uv console scripts may miss src on sys.path; verify CLI with PYTHONPATH=src when the editable install path is not loaded.
2026-06-10T18:51:39+09:00 | A chatbot scaffold is not a distillation-loop validation; reproduce the same loop artifacts and explicitly mark whether the loop was human-scored or only profile-derived.
2026-06-10T18:51:39+09:00 | When posting GitHub comments containing backticks, use --body-file with a quoted heredoc so the shell does not execute command substitutions.
2026-06-10T19:01:25+09:00 | Do not recast a requested distillation process into persona/style axes; preserve the source-review/compress/next-view process unless the user explicitly asks for customization.
2026-06-10T19:05:42+09:00 | For chat-history distillation, the chatbot is only an evaluation shell; the context must be distilled source knowledge, not voice or phrasing imitation.
2026-06-11T13:59:25+0900 | For personal chat distillation, keep the generated final view as route/proof/evaluation control; topic interests and persona/style imitation must be explicit removals, not outputs.
2026-06-11T16:23:10+0900 | Do not treat personal chat distillation as assistant response routing; the primary object is the user's knowledge, interests, beliefs, evaluation axes, worldview, and open questions.
2026-06-11T16:52:28+0900 | A distillation profile can exist while the chat UI still ignores it; prompt construction needs explicit v2 field coverage and a separate local-model-gateway health check.
2026-06-11T17:25:52+0900 | Codex app-server is not OpenAI-compatible HTTP; for a local browser chat UI, codex exec is the fastest working Codex-backed generation bridge.
2026-06-17T14:55:00+0900 | Domain distillation reports should preserve rankable performance tables; later route/view refinement must not erase the early comparison layer.
2026-06-17T15:30:00+0900 | arXiv refresh can find missing relevant papers older than the top latest paper; mark query-bound, metadata-only additions clearly until full-text review and ranking are done.
2026-06-17T18:10:00+0900 | Do not use a page-level subset of SSI views as if it were the full distillation view catalog; individual paper reviews must trace back to the complete A/B/C/D view set.
2026-06-17T22:12:00+0900 | In full-history SSI loops, adding every prior line reference to every record can increase tokens; keep shared history in the view and only record minimal continuity refs.
2026-06-17T22:35:00+0900 | Latest-only compact loops can preserve token budget but lose semantic fields; full-history loops preserve source continuity and warnings but need shared history moved to view-level to control tokens.
2026-06-18T06:31:58+0900 | Corpus distillation needs two separate outputs: model-reading text without JSON/trace metadata, and audit/source maps for citation; mixing them leaves large token waste even after semantic compression.
