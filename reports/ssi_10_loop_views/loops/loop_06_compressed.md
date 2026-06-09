# Loop 06 Compressed

## 前提

- 使った前の見方: `reports/ssi_10_loop_views/loops/loop_05_next_view.md`
- 入力: 105件の圧縮済みレビュー
- 弱点: 入力は 105件の圧縮済みレビューであり、原論文全文ではない

## 短い束

### 事実

- 長期・反復使用の証拠は少ない。多くは single speaker、same session、offline。
- 再装着ずれは大きい。超音波 STN は cross-session gap 92%、cross-speaker gap 88% を回復した。
- `SilentSpeller` は live まで進むが、歯型と 1-2 時間訓練が重い。
- `LipLearner` は約422 ms と live study が強いが、訂正負担と語彙制限なし未解決が残る。
- `NasoVoce` と `WESPER` は維持しやすいが、完全無音ではない。
- `SottoVoce` は接続先が良いが、成功率 65.0%、全体 2.61 s で遅い。
- acoustic sensing は unseen-sentence WER 8.1% が強いが、54 sentences 設計の外は未確認。
- TaL80 69.84、`Digital Voicing...` 74.8、EEG 92.55 は、反復以前に通信性能が弱い。

### 推測

- 実用を止めるのは、精度より保守の重さであることが多い。
- 次は、壊れた時にどう戻すかを見るべきである。

### 不明

- 数週間から数か月の維持コスト。
- 訂正込みの実効速度の横比較。
