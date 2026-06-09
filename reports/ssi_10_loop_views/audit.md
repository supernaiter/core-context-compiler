# SSI 10 Loop Audit

issue: #68
input: reports/ssi_all_context_framework/all_compressed_codex.md
input_papers: 105

required:
- 10 review files: pass
- 10 compressed files: pass
- 10 next_view files: pass
- loop_04 uses loop_03_next_view: pass
- loop_05 uses loop_04_next_view: pass
- loop_06 uses loop_05_next_view: pass
- loop_07 uses loop_06_next_view: pass
- loop_08 uses loop_07_next_view: pass
- loop_09 uses loop_08_next_view: pass
- loop_10 uses loop_09_next_view: pass
- stale provisional wording removed from loop_04 to loop_10: pass

token_counts_gpt4o_mini:
- review_total: 14149
- compressed_total: 5164
- next_view_total: 2502
- all_loop_files_total: 21815
- compressed_ratios_by_loop:
  - loop_01: 0.312
  - loop_02: 0.298
  - loop_03: 0.343
  - loop_04: 0.388
  - loop_05: 0.363
  - loop_06: 0.378
  - loop_07: 0.367
  - loop_08: 0.410
  - loop_09: 0.478
  - loop_10: 0.393

weak_result:
- This run satisfies the requested 10 review-view loops.
- It does not prove <=20% compression for the loop review files.
- It uses the existing 105-paper compressed review bundle, not original full papers.
- It does not include external latest-paper refresh.
