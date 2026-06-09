# framework audit

- input_file: `reports/ssi_all_context_framework/all_compressed_codex.md`
- input_tokens: 24227
- token_counter: `.venv/bin/python` + `tiktoken` `cl100k_base`
- paper_count: 105
- coverage_check: 105件の圧縮レコード全体を読んだ
- output_tokens: 4930
- output_files:
  - `reports/ssi_all_context_framework/framework_from_all_compressed.md`
  - `reports/ssi_all_context_framework/framework_audit.md`

## 根拠が弱い見方

- 「実用化の近さ」は、圧縮資料内のreal-time/mobile/live/wearable/latency記述からの推測であり、実機比較ではない。
- 「LipLearner、SilentSpeller、NasoVoce、WESPER、スマホ音響が近い」は、完全無音性より運用条件を重く見た判断であり、SSIの定義を厳しく取ると順位が変わる。
- 「音声側の知識を借りる研究が伸びている」は、2022-2023年以降の圧縮レコードに目立つ傾向からの判断であり、全出版数の時系列統計ではない。
- 「患者価値はまだ直接証明が少ない」は、圧縮資料内で健常者データが多く見えることからの判断であり、各論文本文の被験者詳細までは再確認していない。
- 「強い研究」の分類は、分割・失敗条件・評価の豊富さを重く見た主観的整理であり、引用数や公式ベンチ順位ではない。

## 圧縮資料だけでは判断できないこと

- 各論文の正確な実験プロトコル、統計検定、除外基準、前処理、ハイパーパラメータ。
- 同一条件での方式間順位。
- 実際の音声サンプル品質、聞き取りやすさ、疲労感、装着感。
- 長期利用、日常環境、患者・失声者・喉頭摘出者での効果。
- ライセンス、データ公開状況、再現コードの有無。
- 最新の追試、撤回、後続研究での評価変更。
- セキュリティ、なりすまし、プライバシー、誤作動の実害。

## 既存手作りフレームを読んでいないこと

- 読んだ入力は `reports/ssi_all_context_framework/all_compressed_codex.md` のみ。
- `reports/ssi_all_context_framework` 配下の既存サイト、`compare`、`rubric`、`open-problems`、その他手作り分析フレームは読んでいない。
- そのため、この出力は既存フレームの要約や改稿ではなく、圧縮105件からの再整理である。
