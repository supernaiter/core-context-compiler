# 全圧縮資料から作ったSSIの見方

## 1. 何を読んだか

- input: `reports/ssi_all_context_framework/all_compressed_codex.md`
- 範囲: 2014-2026年の105件
- 読み方: 既存の比較サイト、ルーブリック、未解決問題、手作りフレームは読まず、この圧縮ファイルだけから見た
- 含まれるもの: 中核SSI、低音量・囁き入力、唇映像からの音声生成、超音波・EMG・EEG・ECoG・EPG・レーダー、音声強調やFoleyなどの隣接研究

## 2. 全体を見て最初に感じること

事実:
- 105件の中には、SSIそのものではない資料がかなり混ざっている。
- 実用に近いものは、完全な無音よりも、唇コマンド、囁き、低音量、スマホ音響、EPG spelling のようにタスクを狭めている。
- 音声復元として強い論文でも、多くは speaker-dependent、閉語彙、制御環境、オフライン評価に寄っている。
- 2022-2023年以降は、SSL単位、HuBERT/AV-HuBERT、音声事前学習、lip-reader guidance、メモリ橋渡しのように、音声側の大規模表現を借りる研究が増えている。
- EEG/MEGの非侵襲脳信号は、現時点の圧縮資料では実用SSIより基礎研究に近い。

推測:
- 分野の実用化は「自然な発話をそのまま復元する」方向だけでは遅く、「入力作法を変える」「語彙を狭める」「既存ASR/TTS/スマートスピーカーへ接続する」方向が先に進みそう。
- センサーの新規性より、毎回ずれる装着、個人差、発話モード差、評価条件差をどう扱うかが実用差になりそう。
- 研究として強いものと、製品に近いものは一致しない。研究としてはTaL系や大規模LRS系が強く、製品に近いのはLipLearner、SilentSpeller、NasoVoce、WESPER、スマホ音響系に見える。

不明:
- 同じデータ・同じ分割・同じASR・同じ遅延条件で横比較した順位は、この圧縮資料だけでは作れない。
- 患者、失声者、喉頭摘出者で本当に使えるかは、ほとんどの資料で不明。
- 長期装着、汗、疲労、食事、会話相手、屋外、照明、姿勢、再装着後の劣化は、圧縮資料だけでは十分に判断できない。

## 3. 新しい見方 12個

### 1. 完全無音より先に来る入力

- 何を見るか: 完全な無音だけでなく、囁き、低音量、唇コマンド、スマホ音響、鼻パッド、EPG spelling を同じ実用候補として見る。
- なぜ重要か: 実用価値は「無音の純度」ではなく、今の機器で低負担に使えるかで決まるため。
- 根拠: NasoVoce、WESPER、LipLearner、SilentSpeller、End-to-End Silent Speech Recognition with Acoustic Sensing。
- 間違いやすい点: 完全無音でないからSSIではない、と早く捨てること。逆に、囁きや低音量を完全無音の証拠として扱うこと。

### 2. タスクを狭めるほど実用に近い

- 何を見るか: 開語彙会話、文章、コマンド、keyword spotting、spelling、固定句のどれを狙っているか。
- なぜ重要か: 高い数値の多くは、狭い語彙・固定句・登録済みコマンドで出ている。
- 根拠: LipLearner、SilentSpeller、IR-UWB radar、textile strain sensor、KDE-SSI、visual-only normal/whispered/silent speech、Silent Speech Challenge更新。
- 間違いやすい点: 30コマンドの高精度を、自由会話復元の進歩と同じ意味に読むこと。

### 3. 話者依存がまだ中心

- 何を見るか: speaker-dependent、seen speaker、unseen speaker、cross-subject、cross-session、remount の扱い。
- なぜ重要か: SSIは身体信号なので、話者差・装着差がそのまま性能差になる。
- 根拠: Digital Voicing of Silent Speech、Improved Model for Voicing Silent Speech、ultrasound系、GRID系VTS、TaL80、STN ultrasound adaptation、KDE-SSI。
- 間違いやすい点: 同じ被験者内の高性能を、初回利用者にもそのまま出る性能と読むこと。

### 4. 発話モード差が本丸

- 何を見るか: vocalized、silent、whispered、normal の差を明示しているか。
- なぜ重要か: 無音発話は、音を消した通常発話ではなく、動きの速度・範囲・癖が変わる。
- 根拠: Silent versus modal multi-speaker speech recognition、Visual-only normal/whispered/silent speech、normal-silent metric learning、Digital Voicing、pseudo target generation/domain adversarial training。
- 間違いやすい点: 有声音データで学んだモデルの結果を、無音発話にも移せると仮定すること。

### 5. センサー配置がモデル性能を決める

- 何を見るか: 電極位置、プローブ固定、カメラ角度、鼻パッド、レーダーアンテナ、歯科装置、再装着の影響。
- なぜ重要か: モデル改良より、入力の見え方が変わるだけで性能が崩れる資料が多い。
- 根拠: ultrasound STN adaptation、IR-UWB radar、SottoVoce、SilentSpeller、NasoVoce、multi-view lip-to-speech、sEMG系。
- 間違いやすい点: 論文のセンサー配置を、日常装着でも再現できると考えること。

### 6. 音声側の知識を借りる研究が伸びている

- 何を見るか: HuBERT、AV-HuBERT、wav2vec2、speech units、lip-reader、ASR guidance、TTS/vocoder、音声事前学習をどう使うか。
- なぜ重要か: 唇や筋電だけでは欠ける音韻・韻律・声質を、音声モデルが補っている。
- 根拠: AKVSR、RobustL2S、LipVoicer、Intelligible Lip-to-Speech with Speech Units、large-scale audio pretraining、VCVTS、VisualTTS、voice-over with discrete units。
- 間違いやすい点: 生成が自然に聞こえることを、入力から正しく読めたことと混同すること。

### 7. 出力は音声か文字かで別の分野になる

- 何を見るか: 文字認識、音声復元、コマンド認識、spelling、音声強調、TTS同期のどれか。
- なぜ重要か: WER、PESQ、STOI、MOS、成功率、wpm は同じ目盛りで比べられない。
- 根拠: Brain2Char、EEG continuous SSR、SottoVoce、EMA2S、SilentSpeller、LipLearner、Vocoder-based speech synthesis、VisualTTS。
- 間違いやすい点: 音声が自然な研究を、意思伝達精度が高い研究とみなすこと。

### 8. 評価指標が目的を隠す

- 何を見るか: WER/CER/PER、PESQ/STOI/ESTOI/MCD/MOS、成功率、latency、RTF、wpm、EERが何を測っているか。
- なぜ重要か: SSIの目的は通信だが、多くの研究は音質、同期、分類精度、客観距離だけを測っている。
- 根拠: ultrasound MSE中心研究、VTSのPESQ/STOI/MOS、SottoVoceのスマートスピーカー成功率、SilentSpellerのwpm、LipLearnerの実アプリ精度。
- 間違いやすい点: MSE改善やPESQ改善を、使える会話速度や誤解の少なさへ直結させること。

### 9. 実用化の近さは性能より運用条件で決まる

- 何を見るか: リアルタイム、モバイル、装着負担、登録データ量、再学習、ユーザー修正、騒音・照明・動き。
- なぜ重要か: 実験室の精度が低くても、日常で動く条件が揃う研究の方が先に使われる可能性がある。
- 根拠: LipLearner、SilentSpeller、WESPER、NasoVoce、SottoVoce、FastLTS、SVTS。
- 間違いやすい点: ベンチマーク性能だけで近さを判断すること。

### 10. 患者価値はまだ直接証明が少ない

- 何を見るか: 喉頭摘出、失声、麻痺、 aphasia、臨床ユーザー、長期使用の有無。
- なぜ重要か: SSIの強い社会的目的は音声障害支援だが、健常者・研究室データが大半に見える。
- 根拠: Cross-modal masking with laryngectomized speakers、aphasia fluency、SSI restoration review、SottoVoce、Brain2Char。
- 間違いやすい点: 健常者の無音模倣で出た性能を、臨床復元性能と読むこと。

### 11. 隣接研究は部品として読む

- 何を見るか: Foley、音声分離、音声強調、AV segmentation、環境音分類、music generation、TTS pause のような資料をSSI性能から分ける。
- なぜ重要か: これらはセンサー融合、同期、評価、生成、活動検出の部品にはなるが、SSIの証拠ではない。
- 根拠: Diff-Foley、SonicVisionLM、audio-visual segmentation、target speech extraction、Demucs、environmental sound classification、SA-SDR、JNDQ。
- 間違いやすい点: 「silent」「audio-visual」「speech」という単語だけでSSI研究として扱うこと。

### 12. 強い研究は失敗条件まで見せている

- 何を見るか: unseen speaker、cross-session、silent vs modal、field/noise、ablation、negative control、weak result を出しているか。
- なぜ重要か: SSIは簡単な設定では動いてしまうので、失敗条件を出す研究ほど次の判断に使える。
- 根拠: TaL80 silent WERの高さ、EEG WERの高さ、Brain2Char silent/mimed劣化、STN adaptationの回復率、NasoVoceの極端騒音、LipVoicerのguidance依存。
- 間違いやすい点: 弱い数値の研究を低価値と決めること。失敗が具体的なら、分野地図としては強い。

## 4. SSI分野の地図

### 入力別

- 唇・顔映像: 研究量が多い。大規模データとSSLの恩恵が大きい。弱点は曖昧性、視点、照明、遮蔽、声質・韻律。
- 超音波舌画像: 舌を直接見るため調音情報が強い。弱点はプローブ固定、再装着、単一話者、装着負担。
- sEMG/顔面筋電: 完全無音に近く、音声復元の可能性がある。弱点は電極位置、話者依存、日常装着。
- EPG/口腔内センサー: spelling では実用に近い。弱点は歯科カスタム、発話自然性、子音混同。
- スマホ音響・鼻パッド・囁き: 近い製品形に寄る。弱点は完全無音ではないこと、環境雑音、プライバシー。
- レーダー・接触レス: 非接触が魅力。弱点は語彙が狭く、センサー幾何に強く依存。
- EEG/MEG/ECoG/rtMRI: 科学的には重要。非侵襲脳信号は性能が遠く、ECoGやrtMRIは機器・侵襲性で日常利用から遠い。

### 出力別

- 文字: 実用判断がしやすい。WER/CER/wpmで通信性能を見られる。
- 音声復元: 既存音声システムへ接続しやすい。生成品質と内容正確性を分けて見る必要がある。
- コマンド: MVPに近い。語彙が狭いので高精度でも過大評価しない。
- spelling: 自然発話ではないが、入力として強い。速度、誤り修正、装着負担を重視する。
- 同期TTS/voice-over/Foley: SSIそのものではなく、生成・同期部品として読む。

### 評価別

- 強い評価: unseen speaker、cross-session、silent-only、real-time、live user task、latency、wpm、field condition、ablationがある。
- 中くらいの評価: held-out sentence、objective metrics、MOS、benchmark WER。
- 弱い評価: single speaker、closed set、random split、MSEだけ、qualitativeだけ、合成ノイズだけ、デモだけ。
- 注意が必要な評価: lip-readerやASR guidanceを使う生成は、入力復元と外部補完を分ける必要がある。

### 実用化の近さ別

- 近い: LipLearner、SilentSpeller、NasoVoce、WESPER、スマホ音響SSI。
- 条件付きで近い: SottoVoce、sEMG音声復元、multi-view/large-scale VTS、ultrasound adaptation。
- 研究段階: ultrasound単一話者回帰、EMG speaker-dependent復元、TaL系speaker-independent研究、visual speech large-scale研究。
- 遠い: EEG/MEG imagined speech、rtMRI、ECoGの一般利用、Foley/音声分離などSSI外の隣接研究。

### 研究としての強さ別

- 強い中核研究: TaL系、Digital Voicing、SilentSpeller、LipLearner、SottoVoce、SVTS、LipVoicer、AKVSR、Brain2Char、STN ultrasound adaptation。
- 強いが隣接: WESPER、NasoVoce、audio-visual speech enhancement/separation、target speech extraction、JNDQ。
- 弱いが残す価値がある: EEG continuous SSR、MEG imagined speech、レーダー初期研究、textile strain sensor。失敗条件や狭い成功条件が分野理解に効く。
- SSI証拠としては弱い: Foley、music separation、environmental sound、telephony dead-air、relay power control。

## 5. 研究を見る時の質問リスト

- 入力は本当に無音か、囁き・低音量・通常音声・音声付き映像を使っていないか。
- 出力は文字か、音声か、コマンドか、spellingか。
- 語彙は開いているか、固定句か、コマンドか、数字か。
- 話者依存か、未知話者か、未知セッションか、再装着後か。
- silent、modal、whispered、normal を分けて測っているか。
- 患者・失声者・喉頭摘出者で試しているか。
- 実時間、遅延、RTF、オンデバイス、電力、装着時間があるか。
- モデルの成功はセンサーの固定条件に依存していないか。
- lip-reader、ASR、TTS、vocoder、language model がどの程度答えを補っているか。
- 評価指標は通信の成功を測っているか、音質だけか。
- 人間評価は何人で、何サンプルで、何を聞かせたか。
- 失敗例、混同、弱い条件、negative control が出ているか。
- 既存デバイスや既存音声エコシステムにつながるか。
- 登録データ量とキャリブレーション時間は現実的か。
- プライバシー、なりすまし、テキスト注入、誤作動の危険を扱っているか。

## 6. 今後の資料圧縮で必ず残すべき情報

- 入力モダリティ、センサー名、位置、チャンネル数、サンプリング条件。
- 出力形式: 文字、音声、コマンド、spelling、同期TTSなど。
- 被験者数、患者/健常者、性別・言語・話者条件。
- 語彙サイズ、文数、発話モード、silent/modal/whispered/normal の区別。
- 分割: speaker-dependent、speaker-independent、cross-session、cross-device、unseen sentence。
- 主要数値: WER/CER/PER、PESQ/STOI/ESTOI/MOS、wpm、成功率、latency、RTF。
- 実用条件: real-time、mobile、on-device、wearable、再装着、歩行、騒音、照明、屋外。
- 外部補助: lip-reader、ASR、LM、TTS、vocoder、pretraining、reference speech、text script。
- 失敗条件: 混同、未知話者、無音発話差、装着ずれ、遅延、電力、ユーザー負担。
- その資料をSSI中核、低音量隣接、生成部品、評価部品、SSI外のどれとして読むべきか。

## 7. 10回ループするなら、次の1回で見方がどう変わりそうか

推測:
- 次の1回では、各研究を「通信として使える」「音声を作れる」「身体信号を読める」「部品として使える」「SSI外」に分ける見方がより強くなりそう。
- その次に、実用化の近さはベンチマーク順位ではなく、登録時間、装着負担、遅延、語彙、誤り修正で決める方向に寄りそう。
- さらに回すと、SSIを単一分野ではなく、入力作法を設計する分野、身体信号を読む分野、音声生成で補う分野、評価を整える分野に分けて見る可能性が高い。

弱い点:
- 今回は圧縮資料だけを読んでいるため、各論文の細部や最新追試は未確認。
- 105件の中でSSI外資料が多く、地図の境界は圧縮文の記述に依存している。

## 8. 結論

事実:
- SSIは「無音から自然会話を復元する単線の競争」ではない。
- 実際には、唇、舌、筋電、口腔内、低音量、脳信号、生成音声、既存ASR/TTSをどう組み合わせるかの分野になっている。
- 強い数値の多くは、話者依存、閉語彙、制御環境、オフライン評価に支えられている。

推測:
- 短期で動くSSIは、完全無音の自由会話ではなく、狭いタスク、ユーザー登録、低負担デバイス、既存音声エコシステム接続から出る。
- 研究として次に重要なのは、モデル構造の小差より、発話モード差、装着ずれ、未知話者、実時間、誤り修正、患者データを正面から測ること。

不明:
- 圧縮資料だけでは、どの方式が同一条件で最強かは決められない。
- 長期日常使用と臨床価値は、まだ十分に読めない。
