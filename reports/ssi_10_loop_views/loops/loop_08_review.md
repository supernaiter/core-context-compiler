# Loop 08 Review

## 前提

- 使った前の見方: `reports/ssi_10_loop_views/loops/loop_07_next_view.md`
- 入力: `reports/ssi_all_context_framework/all_compressed_codex.md` の 105件の圧縮済みレビュー
- 弱点: 入力は 105件の圧縮済みレビューであり、原論文全文ではない
- 今回の見方: 105件を、何が通信を止める停止条件かで読む

## レビュー

### 事実

- 語彙制限なしで止まりやすい。`Digital Voicing of Silent Speech` は open-vocabulary human WER 74.8、automatic WER 68.0。`An Improved Model for Voicing Silent Speech` も automatic WER 42.2%、human transcription 平均 32.3% にとどまる。`LipVoicer` は open vocabulary だが、ASR guidance を外すと WER 86.2% まで崩れる。
- 発話モード差でも止まりやすい。`TaL` は silent WER 43.114%、vocalized WER 17.309%。TaL80 は silent 69.84、modal 39.34。`Brain2Char` も通常 WER 7.0%-10.6% に対し silent/mimed 40%/67% だった。
- 未知話者や患者差でも止まりやすい。`Continuous Silent Speech Recognition using EEG` は cross-subject WER 92.55%。`Cross-Modal Masking...` は laryngectomized adaptation が弱い。`JapanEEG` は 1020 h と大きいが n=3 で decoding benchmark はまだ無い。
- 再装着や位置ずれでも止まる。STN adaptation が cross-session gap の 92% を回復したことは、remount が大きな停止条件であることを示す。radar は口元幾何、`KDE-SSI` は電極位置、超音波系は probe 固定に敏感である。
- 実時間でも止まる。`LipLearner` は約 422 ms で比較的近い。`WESPER` は realtime stack を持つ。`SottoVoce` は 2.61 s 総処理、`LipVoicer` は hundreds of inference steps で、ここで止まる。
- 実環境でも止まる。`NasoVoce` は 4 実環境記録を持つが、証拠の中心は合成雑音 -10 から 10 dB。映像系では severe head motion、non-frontal views、occlusion、camera noise が繰り返し限界として出る。`SilentSpeller` は walking 97.5%、seated 96.5% と比較的残るが、綴り入力である。
- 軽装着でも止まる。`SilentSpeller` のカスタム歯型、`SottoVoce` の超音波 probe、EEG/MEG/ECoG、顔面電極は持ち運びや日常装着の負担が大きい。
- 患者証拠でも止まる。価値の高い復元研究はあるが、健康被験者中心、少人数、短期、paired speech 不足が多い。

### 推測

- 一つの方式が全停止条件を同時に外す段階にはまだ来ていない。
- 近い路線は、完全無音を少し崩す、仕事を狭める、外部支援を使うことで、停止条件の数を減らしている。
- 分野を一列順位で読むより、どの停止条件を外したかで読む方が実態に近い。

### 不明

- 停止条件のうち、どれが実利用で最も支配的かを共通尺度で比べることはできない。
- 患者、長期利用、家庭内利用でどの停止条件が先に表に出るかは不明である。

### 警告

- 高い精度でも、語彙制約なし、未知話者、軽装着、実時間のどれかで止まるなら、日常通信としてはまだ弱い。
- 停止条件を明記しない比較は、近い路線と遠い路線を混同しやすい。

## 今回の結論

### 事実

- 105件では、停止条件は主に語彙制約なし、発話モード差、未知話者、再装着、実時間、実環境、軽装着、患者証拠に分かれていた。

### 推測

- 次は、同じ土俵で順位を付けず、どの停止条件を相手にしている路線かで分けて読むべきである。

### 不明

- 路線どうしで再利用できる改善がどこまであるかはまだ見えない。
