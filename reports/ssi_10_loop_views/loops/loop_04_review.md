# Loop 04 Review

## 前提

- 使った前の見方: `reports/ssi_10_loop_views/loops/loop_03_next_view.md`
- 入力: `reports/ssi_all_context_framework/all_compressed_codex.md` の 105件の圧縮済みレビュー
- 弱点: 入力は 105件の圧縮済みレビューであり、原論文全文ではない
- 今回の見方: 105件を「誰がいつ誤りを直すか」で読む

## レビュー

### 事実

- 装置や前処理が先に誤りを直す例がある。`Adaptation of Tongue Ultrasound-Based Silent Speech Interfaces Using Spatial Transformer Networks` は STN+out で cross-speaker gap の 88%、cross-session gap の 92% を回復した。`Cross-Modal Masking for Robust Silent Speech Synthesis Using sEMG and Lipreading` は multimodal masking で Whisper v3 WER を最大 14 absolute points 改善した。
- 発話モード差をモデル側で直す例も多い。`Improving the Gap in Visual Speech Recognition Between Normal and Silent Speech Based on Metric Learning` は normal と silent の分布差を寄せる。`Speech Reconstruction from Silent and Vocalized Articulatory Data Using Pseudo Targets and Domain Adversarial Training` は DTW pseudo target と domain adversarial 学習で silent と vocalized のずれを埋めようとしていた。
- 外部モデルが後段で誤りを直す例はさらに強い。`LipVoicer` は ASR guidance ありで LRS3 WER 21.4% だが、外すと 86.2% まで悪化した。`AKVSR` は LRS3 baseline WER 46.1% を 23.6% まで下げた。speech unit、audio memory、lip-reader は読み取り不足の穴埋めとして働いている。
- ユーザーが最後に誤りを直す例もある。`LipLearner` は 30 command accuracy が one-shot 81.7%、five-shot 98.8%、遅延は約 422 ms だが、active learning と user correction burden が残る。`SilentSpeller` は live seven-user で平均 37 wpm・87%、最良 53 wpm・91% を出したが、綴り入力と edit gesture を使い、修正をユーザーが引き受ける。
- 周辺の既存サービスに渡して誤りを小さくする例もある。`SottoVoce` は regenerated audio を smart speaker に渡し、Network1+2 で成功率 65.0%、Google STT WER 33.56%、3.68 s clip に対し 2.61 s 総処理だった。`NasoVoce` と `WESPER` は低音量や囁き入力を使って既存 ASR へ寄せている。
- それでも直し切れない路線は残る。`TaL` は silent WER 43.114%、vocalized WER 17.309%。TaL80 は silent WER 69.84、modal 39.34。`Continuous Silent Speech Recognition using EEG` は WER 74.86%-84.22%、cross-subject 92.55%。`Brain2Char` は silent/mimed で 40%/67% まで落ちる。

### 推測

- SSI の進み方は、入力を一度で正しく読むことより、どこかで誤りを直せる契約を作ることに近い。
- 実用に近い系は、誤りを早い段階で全部なくすより、外部モデル、ユーザー、既存サービスに分散して直している。
- 見栄えのよい音声生成は、内容理解そのものの強さではなく、後段の補助の強さで押し上がっている場合がある。

### 不明

- 装置の自動補正、外部モデル、ユーザー修正のうち、どの契約が最も速く、疲れにくく、誤解が少ないかは決められない。
- 患者や喉頭摘出者で同じ訂正契約が成立するかは不明である。
- 誤りを早く直すほど privacy や安全性が上がるかどうかも、この束だけでは読めない。

### 警告

- 音声が自然でも内容が合っているとは限らない。とくに `LipVoicer` のように外部 guidance が強い系は、音の自然さと意味の正確さを分けて読む必要がある。
- 低い WER や高い MOS があっても、誰が誤りを直した結果かを書き分けないと実用判断を誤る。

## 今回の結論

### 事実

- 105件では、誤り訂正の担い手は装置、モデル、ユーザー、既存サービスに分かれていた。

### 推測

- 次に見るべき差は、どの誤りを直したかより、そのために何を借りているかである。

### 不明

- 借り物の中で、どれが最も外しやすく、どれが本質的に必要かはまだ見えない。
