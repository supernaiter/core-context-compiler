# Loop 06 Review

## 前提

- 使った前の見方: `reports/ssi_10_loop_views/loops/loop_05_next_view.md`
- 入力: `reports/ssi_all_context_framework/all_compressed_codex.md` の 105件の圧縮済みレビュー
- 弱点: 入力は 105件の圧縮済みレビューであり、原論文全文ではない
- 今回の見方: 105件を、借り物が時間の中でどこから壊れるかで読む

## レビュー

### 事実

- 長期や反復使用の直接証拠は少ない。多くの超音波、sEMG、lip-to-speech 論文は single speaker、same session、read speech、offline 評価で止まる。
- 再装着ずれは大きい。STN adaptation が cross-session gap の 92%、cross-speaker gap の 88% を回復したことは、適応前に大きく崩れることを示す。
- 反復利用に最も近い例でも維持コストが重い。`SilentSpeller` は walking 97.5%、seated 96.5%、live seven-user 平均 37 wpm・87%、best 53 wpm・91% を出すが、カスタム歯型と 1-2 時間訓練が要る。
- `LipLearner` は 11 人・7 条件・9625 clips と 16 人 live study を持ち、約 422 ms まで詰めたが、similar commands の混同、active learning、user correction burden、語彙制限なし未解決が残る。
- `NasoVoce` は 1000 held-out 項目、雑音 -10 から 10 dB、4 実環境記録を持つが、主証拠は synthetic noise で、fusion は fully streaming ではない。whisper 時は vibration も弱い。
- `WESPER` は realtime stack を持ち、whisper WER/CER を大きく下げるが、完全無音ではない。維持しやすさは高いが、SSI の中心課題からは少し外れる。
- `SottoVoce` は smart speaker 接続の逃げ道がある一方、3.68 s clip に対し 2.61 s 総処理、成功率 65.0% で、日常会話の速度には届かない。
- `End-to-end Silent Speech Recognition with Acoustic Sensing` は unseen-sentence WER 8.1% が強いが、54 sentences の設計内であり、常時利用、電力、野外ノイズ、広い語彙の継続使用は不明である。
- 長く使う以前に弱い路線もある。TaL80 silent WER 69.84、`Digital Voicing...` open-vocabulary human WER 74.8、EEG cross-subject WER 92.55、`Brain2Char` silent/mimed 40%/67% は、初回の通信としてすでに厳しい。
- 患者側の継続証拠も薄い。`Cross-Modal Masking...` は laryngectomized adaptation の弱さと paired audible speech 欠如を自ら書いている。

### 推測

- 毎日使う場面で先に壊れるのは、精度表より、再装着、再学習、疲労、遅延、手入れの方である可能性が高い。
- 少し精度が低くても、壊れた時に別経路へ逃げられる系の方が長く残りやすい。
- 分野の次の差は、「一回うまくいくか」ではなく、「やさしく壊れるか」にある。

### 不明

- 1週間、1か月、半年の再学習コスト、衛生、電池、社会的受容はほぼ不明である。
- 訂正ループ込みの実効速度を方式横断で比べられる資料は不足している。

### 警告

- same session や random split の高スコアを、そのまま継続使用の証拠として扱わない方がよい。
- 低い結果は弱さの証拠であると同時に、どこから壊れるかを教える重要な警報でもある。

## 今回の結論

### 事実

- 継続使用を直接測った研究は少なく、あるとしても装着、訓練、訂正、遅延の重さを残している。

### 推測

- 次は、壊れた時にどう戻すかまで含めた運用で読むべきである。

### 不明

- どの方式が最もやさしく壊れ、最も短く戻せるかは未確定である。
