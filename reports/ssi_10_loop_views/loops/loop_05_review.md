# Loop 05 Review

## 前提

- 使った前の見方: `reports/ssi_10_loop_views/loops/loop_04_next_view.md`
- 入力: `reports/ssi_all_context_framework/all_compressed_codex.md` の 105件の圧縮済みレビュー
- 弱点: 入力は 105件の圧縮済みレビューであり、原論文全文ではない
- 今回の見方: 105件を「誤りを直すために何を借りているか」で読む

## レビュー

### 事実

- 語彙や仕事を狭めて借りる例が多い。`LipLearner` は 25-30 command、`SilentSpeller` は 26 文字と空白、`IR-UWB Radar-Based Contactless Silent Speech Recognition...` は 8 母音・11 子音・25 語・12 句、`Visual-Only Recognition of Normal, Whispered and Silent Speech` は digits と固定句だった。高い数値はこの制約込みで出ている。
- 話者ごとの訓練や登録を借りる例も多い。`Digital Voicing of Silent Speech` は subject-specific data を強く使い、`An Improved Model for Voicing Silent Speech` は 1 話者 19 時間、`Knowledge Distilled Ensemble Model for sEMG-based Silent Speech Interface` は 5 人 26 NATO 語、`LipLearner` も few-shot enrollment を前提にしている。
- 固定装着を借りる例も目立つ。超音波系は probe-fixing headset 前提が多く、STN adaptation が cross-session gap の 92% を回復したこと自体が位置ずれの重さを示す。`SilentSpeller` はカスタム歯型、`SottoVoce` は 3.5 MHz convex probe、radar は口元幾何、`KDE-SSI` は顔面電極に強く依存する。
- 外部の speech/text prior を借りる研究は厚い。`LipVoicer` は lip-reader と ASR guidance、`AKVSR` は audio memory、`RobustL2S` と `Intelligible Lip-to-Speech with Speech Units` は speech SSL、voice-over 系は text script や speaker embedding を借りる。
- vocalized data や paired audio を教師に借りる研究も多い。`Digital Voicing...` は vocalized/silent target transfer、pseudo target 系は DTW pseudo acoustic target、metric learning 系は normal data から silent data へ寄せている。silent だけで閉じた学習は少ない。
- 完全無音そのものを少し崩して借りる例もある。`NasoVoce` と `WESPER` は low-volume や whisper を使う。`End-to-end Silent Speech Recognition with Acoustic Sensing` は inaudible acoustic probing に寄る。完全無音の純度は下がるが、実装の近さは上がる。
- 借り物の軽重には差がある。スマホ前面カメラ、短い登録、既存 ASR 接続は比較的軽い。カスタム口腔内装置、長時間個人学習、固定超音波、paired vocalized corpus は重い。

### 推測

- SSI の実用差は、唇、筋電、超音波といったモダリティ差より、借り物の重さで説明しやすい。
- 近い方式は何かを借りていても借り先が安い。遠い方式は結果が面白くても借り先が高い。
- speaker-independent と書かれていても、重い事前学習や curated benchmark を強く借りていれば、現場導入が軽いとは限らない。

### 不明

- 語彙制約、固定装着、paired audio、話者訓練のどれを先に外すべきかは方式ごとに違う。
- 外部 prior が患者音声や崩れた silent articulation に同じように効くかは不明である。

### 警告

- script 付き voice-over や reference speech 付き生成系は、音声が自然でも SSI の読み取り力そのものとは限らない。
- 借り物を隠したまま精度だけ比べると、実用の近さを見誤る。

## 今回の結論

### 事実

- 105件の多くは、語彙制約、個人訓練、固定装着、外部 prior、paired data、低音量入力のどれかを強く借りていた。

### 推測

- 次に見るべき差は、その借り物が時間の経過でどこから壊れるかである。

### 不明

- 毎日使うと最初に壊れる借り物が何かは、まだはっきりしない。
