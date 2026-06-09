# Loop 05 Compressed

## 前提

- 使った前の見方: `reports/ssi_10_loop_views/loops/loop_04_next_view.md`
- 入力: 105件の圧縮済みレビュー
- 弱点: 入力は 105件の圧縮済みレビューであり、原論文全文ではない

## 短い束

### 事実

- 借り物の主な種類
  - 狭い仕事: `LipLearner` 25-30 command、`SilentSpeller` 26 文字、radar 25 語・12 句。
  - 個人訓練: `Digital Voicing...`、`Improved Model...`、`KDE-SSI`、few-shot enrollment。
  - 固定装着: 超音波 headset、カスタム歯型、顔面電極、probe、radar 幾何。
  - 外部 prior: `LipVoicer` 21.4% -> 86.2%、`AKVSR` 46.1% -> 23.6%。
  - paired data: vocalized/silent transfer、pseudo target、normal-to-silent transfer。
  - 低音量入力: `NasoVoce`、`WESPER`、acoustic sensing。
- 軽い借り物は、スマホ、短い登録、既存 ASR 接続。
- 重い借り物は、専用装着、長時間個人学習、paired corpus。

### 推測

- 実用差はモダリティ差より、借り物の重さで説明しやすい。
- 次は、その借り物が時間の中でどこで壊れるかを見るべきである。

### 不明

- 先に外すべき借り物。
- 外部 prior が患者でも効くか。
