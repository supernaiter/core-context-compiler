# Loop 08 Compressed

## 前提

- 使った前の見方: `reports/ssi_10_loop_views/loops/loop_07_next_view.md`
- 入力: 105件の圧縮済みレビュー
- 弱点: 入力は 105件の圧縮済みレビューであり、原論文全文ではない

## 短い束

### 事実

- 語彙制約なしで止まる
  - `Digital Voicing...`: human 74.8、automatic 68.0。
  - `Improved Model...`: automatic 42.2%、human 平均 32.3%。
  - `LipVoicer`: guidance なし 86.2%。
- 発話モード差で止まる
  - `TaL`: silent 43.114%、vocalized 17.309%。
  - TaL80: silent 69.84、modal 39.34。
  - `Brain2Char`: silent/mimed 40%/67%。
- 未知話者や患者差で止まる
  - EEG cross-subject 92.55%。
  - `Cross-Modal Masking...`: laryngectomized adaptation が弱い。
  - `JapanEEG`: 1020 h、n=3。
- 再装着や実時間で止まる
  - STN remount 回復 92%。
  - `LipLearner` 約422 ms。
  - `SottoVoce` 2.61 s。
- 実環境や軽装着で止まる
  - `NasoVoce` は合成雑音中心。
  - `SilentSpeller` は walking 97.5% だが歯型が重い。

### 推測

- 一つの方式が全停止条件を同時に外す段階にはまだ来ていない。
- 次は、どの停止条件を相手にしている路線かで分けて読むべきである。

### 不明

- 最も支配的な停止条件。
- 路線どうしで再利用できる改善。
