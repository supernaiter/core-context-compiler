# Loop 03 Review

input:
- reports/ssi_all_context_framework/all_compressed_codex.md
- reports/ssi_all_context_framework/framework_from_all_compressed.md

previous_view:
- reports/ssi_10_loop_views/loops/loop_02_next_view.md

## 今回の見方

- 105件を「どの段階で情報不足を直しているか」で読み直す。
- 段階は、取得、発話モード差の吸収、解読の自由度、出力後の受け渡しと訂正、の 4 つに置く。

## 読み直し

### 1. 最初の段階は、取得の安定化で詰まる

事実:
- Adaptation of Tongue Ultrasound-Based Silent Speech Interfaces Using Spatial Transformer Networks は、4 話者・4 remounted sessions で STN+out が adaptation gap の 88% cross-speaker、92% cross-session を回復した。
- IR-UWB radar は upper/lower antenna 配置と lip alignment に依存し、raw/clutter-only では phoneme が 50% 未満まで落ちた。
- Multi-view lip 系は 30/45/60 度などの視点組合せで伸びるが、配置負担が増える。
- NasoVoce は whisper で vibration が弱く、極端雑音では vibration-only が勝つことがある。
- SilentSpeller は custom palate、KDE-SSI は 3 ch adhesive electrodes、Digital Voicing は face/jaw/throat EMG gear を要する。

推測:
- 多くの方式は、解読器より前に、入力の再現性で勝負が決まる。
- 取得段階の安定化が弱いと、後段の大きなモデルで埋めても限界が残る。

不明:
- 取得安定化だけでどこまで解けるかは、同一モデルでの治具比較が少なく不明である。

### 2. 次の段階は、silent と vocalized の差を埋めることにある

事実:
- Visual-Only Recognition of Normal, Whispered and Silent Speech は、matched digits 68.0/70.5/62.2%、matched phrases 69.7/70.8/64.4% で、normal->silent transfer は 59.7%、61.2% まで落ちた。
- Improving the Gap in Visual Speech Recognition Between Normal and Silent Speech Based on Metric Learning は AV Digits 10 phrases で best silent 9.97% WER を出し、silent data を倍にした baseline に近い結果を、normal-silent alignment で得た。
- Speech Reconstruction from Silent Tongue and Lip Articulation By Pseudo Target Generation and Domain Adversarial Training は、silent が vocalized に遅れ、training recipe 側の工夫が価値になっていた。
- Digital Voicing は vocalized/silent EMG mismatch を target transfer と CCA で吸収した。
- Cross-Modal Masking は laryngectomized adaptation が弱く、silent 側でも発話様式の違いが大きいことを示した。

推測:
- silent speech は単なる「音を消した通常発話」ではなく、別の運動様式として扱う必要がある。
- 中盤の本丸はモデルの大きさではなく、この発話モード差の扱いである。

不明:
- whisper、mimed、silent、post-laryngectomy を一つの連続体として扱えるかは不明である。

### 3. その次で、自由度を上げると誤りが跳ねる

事実:
- Digital Voicing は open vocabulary 9,828 words で WER がまだ高い。
- LipVoicer は strong guidance を外すと 21.4% から 86.2% へ崩れた。
- Acoustic sensing は unseen-sentence WER 8.1% でも、54 文の中での一般化に留まる。
- SilentSpeller は自由会話ではなく spelling へ切り、LipLearner は 30 commands へ切り、IR-UWB radar は 8 母音・11 子音・25 語・12 句に切っている。
- MEG imagined speech は 76 words、EEG imagined speech は 5 classes に留まる。

推測:
- 自由度を広げた時に足りない情報は、入力ではなく、言語候補の絞り込み側で爆発している。
- そのため、高自由度ほど後段の強い補完器に頼り、低自由度ほど前段の弱い信号でも成立しやすい。

不明:
- どの自由度から「修正可能な誤り」ではなく「会話不能な誤り」に変わるかは不明である。

### 4. 最後の段階で、受け渡しと訂正がある系だけが通信へ近づく

事実:
- SottoVoce は regenerated audio をそのまま smart speaker へ渡した。成功率は 65.0% でも、既存エコシステムと繋いだ点が大きい。
- SilentSpeller は push-to-talk と edit gestures を持ち、live entry 37 wpm 87% を示した。
- LipLearner は active learning と on-device incremental learning を持つ。
- WESPER は whisper を通常音声へ戻して既存 ASR へ繋ぐ。NasoVoce も Whisper Large-v2 と接続している。
- 2020 review は遅延目安を約 50 ms 理想、100 ms まで余地、200 ms は崩れやすいと整理していたが、SottoVoce は 2.61 s でまだ長い。

推測:
- 通信としての差は、認識器の前だけでなく、出力後にどう訂正し、どの既存機器へ渡せるかで決まる。
- SSI は単独モデルではなく、入出力と修正を含む系で見た方が現実に近い。

不明:
- どの訂正方法が最も負担が小さいかは、この束だけでは比較できない。

## 弱い結果と警告

事実:
- 4 段階のどこか一つを解いても、他段階の不足が残る例が多い。
- 取得が強くても open vocabulary で崩れ、生成が強くても guidance 依存が強く、受け渡しがあっても遅延や装着負担が残る。

推測:
- SSI の進歩は「最良論文を 1 本選ぶ」より、「どの段階をどの程度埋めたか」で見るべきである。
- 一見弱い論文でも、どの段階で失敗したかが明確なら価値が高い。

不明:
- 4 段階をまとめて測る共通ベンチマークはまだ見当たらない。

## このloopで残った問い

事実:
- 実用に近い系は、最後に受け渡しと訂正の仕組みを持っていた。

推測:
- 次は「誰がいつ誤りを直すか」で読むと、研究の価値がさらに通信寄りに整理できる。

不明:
- 誤り訂正を、ユーザー、装置自動補正、外部モデル、対話相手のどこへ置くのが最善かは、次の見方で詰める必要がある。
