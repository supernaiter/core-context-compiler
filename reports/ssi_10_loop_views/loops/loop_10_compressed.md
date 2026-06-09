# Loop 10 Compressed

## 前提

- 使った前の見方: `reports/ssi_10_loop_views/loops/loop_09_next_view.md`
- 入力: 105件の圧縮済みレビュー
- 弱点: 入力は 105件の圧縮済みレビューであり、原論文全文ではない

## 短い束

### 事実

- 低音量路線は、周辺の既存音声系が主な負担を払う。
  - `NasoVoce`: 1000 held-out、-10 から 10 dB、50人 MUSHRA、4 実環境。
  - `WESPER`: 44.70/28.38 -> 26.68/12.70、13.75/5.47。
- 狭い課題路線は、ユーザーと装置が主な負担を払う。
  - `LipLearner`: 81.7% -> 98.8%、約422 ms。
  - `SilentSpeller`: 平均 37 wpm、最良 53 wpm、walking 97.5%。
  - radar: 25 words 88.95%、12 phrases 96.88%。
- 無音再生路線は、モデルと装置が主な負担を払う。
  - `AKVSR`: 46.1% -> 23.6%。
  - `LipVoicer`: guidance なし 86.2%。
  - `TaL`: silent 43.114%、vocalized 17.309%。
  - `SottoVoce`: 成功率 65.0%、全体 2.61 s。
- 患者復元路線は、ユーザーと装置の負担が重く、直接証拠が薄い。
  - `Cross-Modal Masking...`: 最大 14 absolute points 改善、ただし laryngectomized adaptation は弱い。
- 脳信号路線は、装置と研究側の負担が極めて重い。
  - `JapanEEG`: 1020 h、n=3。
  - MEG imagined speech: Recall@1 約9.1%。
  - EEG: cross-subject 92.55%。
  - `Brain2Char`: silent/mimed 40%/67%。

### 推測

- 今後は global rank より、「どの路線で」「どの停止条件を」「誰の負担で外したか」を見る方がよい。

### 不明

- 将来の収束形。
- 長期日常利用で残る路線。
