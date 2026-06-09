# Loop 04 Compressed

## 前提

- 使った前の見方: `reports/ssi_10_loop_views/loops/loop_03_next_view.md`
- 入力: 105件の圧縮済みレビュー
- 弱点: 入力は 105件の圧縮済みレビューであり、原論文全文ではない

## 短い束

### 事実

- 誤りを先に直す例
  - 超音波 STN: cross-speaker gap 88%、cross-session gap 92% を回復。
  - cross-modal masking: Whisper v3 WER を最大 14 absolute points 改善。
- 外部モデルが後で直す例
  - `LipVoicer`: ASR guidance あり 21.4%、なし 86.2%。
  - `AKVSR`: LRS3 WER 46.1% -> 23.6%。
- ユーザーや周辺系が最後に直す例
  - `LipLearner`: 81.7% -> 98.8%、約422 ms、active learning と user correction burden が残る。
  - `SilentSpeller`: 平均 37 wpm、最良 53 wpm、edit gesture あり。
  - `SottoVoce`: 成功率 65.0%、Google STT WER 33.56%、全体 2.61 s。
- 直し切れない例
  - `TaL`: silent 43.114%、vocalized 17.309%。
  - TaL80: silent 69.84、modal 39.34。
  - EEG: 74.86%-84.22%、cross-subject 92.55%。
  - `Brain2Char`: silent/mimed 40%/67%。

### 推測

- SSI の差は、誰がどこで誤りを直すかでかなり説明できる。
- 次は、その訂正のために何を借りているかを見る方がよい。

### 不明

- 最も疲れにくい訂正契約。
- 患者で同じ契約が成り立つか。
