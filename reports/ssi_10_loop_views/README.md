# SSI 10 review-view refinement loops

issue: #68
input: reports/ssi_all_context_framework/all_compressed_codex.md
base_view: reports/ssi_all_context_framework/framework_from_all_compressed.md
loops: 10
files:
- review: 10
- compressed: 10
- next_view: 10
status: verified
weak:
- input is 105 compressed expert-review records, not original full paper PDFs.
- loop outputs are Codex-derived readings, not externally rechecked literature review.
- compressed loop files are shorter than reviews, but not all are <=20% of review tokens.
