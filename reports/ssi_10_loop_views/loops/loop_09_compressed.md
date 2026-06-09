# Loop 09 Compressed

## 前提

- 使った前の見方: `reports/ssi_10_loop_views/loops/loop_08_next_view.md`
- 入力: 105件の圧縮済みレビュー
- 弱点: 入力は 105件の圧縮済みレビューであり、原論文全文ではない

## 短い束

### 事実

- 低音量路線
  - `NasoVoce`: 1000 held-out、-10 から 10 dB、50人 MUSHRA、4 実環境。
  - `WESPER`: 44.70/28.38 -> 26.68/12.70、13.75/5.47。
- 狭い課題路線
  - `LipLearner`: F1 0.8947、81.7% -> 98.8%、約422 ms。
  - `SilentSpeller`: 平均 37 wpm、最良 53 wpm、walking 97.5%。
  - `IR-UWB radar`: 25 words 88.95%、12 phrases 96.88%。
- 無音再生路線
  - `TaL`: silent 43.114%、vocalized 17.309%。
  - TaL80: silent 69.84、modal 39.34。
  - `AKVSR`: 46.1% -> 23.6%。
  - `LipVoicer`: guidance なし 86.2%。
- 患者復元路線
  - `Cross-Modal Masking...`: 最大 14 absolute points 改善、ただし laryngectomized adaptation は弱い。
  - `SottoVoce`: 成功率 65.0%、全体 2.61 s。
- 脳信号路線
  - `JapanEEG`: 1020 h、n=3。
  - MEG imagined speech: Recall@1 約9.1%。
  - EEG: 74.86%-84.22%、cross-subject 92.55%。
  - `Brain2Char`: silent/mimed 40%/67%。

### 推測

- 一列順位より、路線ごとに「何を一つ外したか」で見る方がよい。
- 次は、各路線で残る負担を誰が払っているかを見るべきである。

### 不明

- 路線間の将来収束。
- 共有できる改善の範囲。
