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
