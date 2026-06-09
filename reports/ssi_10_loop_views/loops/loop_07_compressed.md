# Loop 07 Compressed

## 前提

- 使った前の見方: `reports/ssi_10_loop_views/loops/loop_06_next_view.md`
- 入力: 105件の圧縮済みレビュー
- 弱点: 入力は 105件の圧縮済みレビューであり、原論文全文ではない

## 短い束

### 事実

- 戻し方が見える例
  - `LipLearner`: 81.7% -> 98.8%、few-shot enrollment、active learning。
  - `SilentSpeller`: 平均 37 wpm、最良 53 wpm、push-to-talk と edit gestures。
  - `NasoVoce` と `WESPER`: low-volume や whisper へ逃げられる。
  - `SottoVoce`: smart speaker へ渡せるが、成功率 65.0%、全体 2.61 s。
- 戻し方が見えにくい例
  - `AKVSR`、`LipVoicer`、speech unit 系は外部モデル補正が中心。
  - TaL80 69.84、EEG 92.55、`Brain2Char` 40%/67% のような苦しい系では復帰手順が薄い。

### 推測

- 実用差は最高精度より、失敗を小さく閉じられるかで分かれる。
- 次は、何が通信を止める停止条件なのかで読むべきである。

### 不明

- 最も安全で短い復帰設計。
- 患者でも同じ戻し方が使えるか。
