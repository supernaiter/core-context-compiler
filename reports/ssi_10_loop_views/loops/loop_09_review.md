# Loop 09 Review

## 前提

- 使った前の見方: `reports/ssi_10_loop_views/loops/loop_08_next_view.md`
- 入力: `reports/ssi_all_context_framework/all_compressed_codex.md` の 105件の圧縮済みレビュー
- 弱点: 入力は 105件の圧縮済みレビューであり、原論文全文ではない
- 今回の見方: 105件を、どの停止条件を相手にしている路線かで分けて読む

## レビュー

### 事実

- 低音量入力で既存音声系へつなぐ路線がある。`NasoVoce` は 1000 held-out 項目、雑音 -10 から 10 dB、50人 MUSHRA、4 実環境記録を持つ。`WESPER` は whisper WER/CER 44.70/28.38 を 26.68/12.70 に下げ、HuBERT-base では 13.75/5.47 まで下げた。完全無音ではないが、実時間と接続性では先に進む。
- コマンド、綴り、短文入力を確実に通す路線がある。`LipLearner` は one-shot 25 command F1 0.8947、30 command accuracy 81.7% から 98.8%、約 422 ms。`SilentSpeller` は平均 37 wpm、最良 53 wpm、walking 97.5%、seated 96.5%。`IR-UWB radar` は 25 words 88.95%、12 phrases 96.88% である。
- 無音の映像や調音から音声や文字を再生する路線がある。`TaL` は silent 43.114%、vocalized 17.309%。TaL80 は silent 69.84、modal 39.34。`AKVSR` は LRS3 46.1% を 23.6% へ下げる。`LipVoicer` は guidance なしで 86.2% まで崩れる。研究の厚みはあるが停止条件も多い。
- 患者や失声者の復元を直接狙う路線がある。`Cross-Modal Masking...` は laryngeal と laryngectomized を含み、Whisper v3 WER を最大 14 absolute points 改善したが、laryngectomized adaptation は弱い。`SottoVoce` も支援方向を示すが、speaker-dependent で装置が重い。
- 脳信号など基礎研究の路線がある。`JapanEEG` は 1020 h と大きいが n=3。MEG imagined speech は Recall@1 約 9.1%。EEG continuous SSR は WER 74.86%-84.22%、cross-subject 92.55%。`Brain2Char` は通常 7.0%-10.6% でも silent/mimed 40%/67% である。
- 路線ごとに強い停止条件が違う。低音量路線は完全無音で止まり、綴りやコマンド路線は語彙制約なしで止まり、再生路線は発話モード差と外部補助依存で止まり、患者復元路線は患者証拠で止まり、脳信号路線は装置と一般化で止まる。

### 推測

- 105件を一列順位で比べるより、路線ごとに「何を一つ外したか」で見る方が正しい。
- 近い路線は、完全無音の純度を少し下げるか、課題を狭める代わりに、実時間や運用を取りに行っている。
- 遠い路線は停止条件が多いが、将来の大きい価値を持つため、低スコアでも切り捨てにくい。

### 不明

- 路線どうしで共有できる改善がどこまであるかは不明である。
- 低音量路線から完全無音路線へ、そのまま橋渡しできるかも分からない。

### 警告

- 同じ精度でも路線が違えば意味が違う。`LipLearner` の 98.8% と TaL の 43.114% は同じ物差しで読まない方がよい。
- 路線分けをしないと、実用に近い工夫と基礎研究の価値を同時に見失いやすい。

## 今回の結論

### 事実

- 105件は少なくとも五つの路線に分かれ、停止条件の種類も強さも違っていた。

### 推測

- 次は、各路線で残る負担を誰が払っているかを見るべきである。

### 不明

- 将来この五路線がどこまで収束するかはまだ見えない。
