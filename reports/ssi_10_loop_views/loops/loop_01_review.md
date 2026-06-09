# Loop 01 Review

input:
- reports/ssi_all_context_framework/all_compressed_codex.md
- reports/ssi_all_context_framework/framework_from_all_compressed.md

previous_view:
- reports/ssi_all_context_framework/framework_from_all_compressed.md

## 今回の見方

- 105件を「通信として今日どこまで使えるか」という見方で読み直す。
- 評価の中心は、自然さではなく、実際に相手へ意図を通せるかに置く。

## 読み直し

### 1. すぐ通信に使える線は、完全無音の自由会話ではない

事実:
- LipLearner はスマホ前面カメラで 30 コマンドを扱い、one-shot 81.7%、five-shot 98.8%、遅延は約 422 ms だった。11人・7条件・9,625 クリップと、16人の実地試験がある。
- SilentSpeller は 124 電極 EPG で 26 文字と空白を扱い、約 97% 文字、92% 単語、未知 100 単語でも 94.5% 文字、85.5% 単語、7人 live で平均 37 wpm 87%、最良 53 wpm 91% だった。
- End-to-end Silent Speech Recognition with Acoustic Sensing は、音が聞こえないスマホ型音響センシングで 54 文を扱い、domain-dependent WER 2.6%、domain-independent 平均 8.4%、unseen-sentence 8.1% を出した。
- NasoVoce は鼻パッドで低音量発話を拾い、1,000 held-out items と -10 から 10 dB の合成雑音で評価した。WESPER はささやき音声を通常音声へ変換し、Google ASR の WER/CER を 44.70/28.38 から 26.68/12.70 へ下げた。
- これらは高性能でも、コマンド、綴り、54 文、低音量音声のように入力や課題を狭めている。

推測:
- 105件を通信として見ると、近いのは「自由会話を完全無音で復元する線」ではなく、「課題を狭める」「登録する」「低音量で逃がす」線である。
- 実用の早さは、SSI の純度より、使い始めの負担と誤り修正のしやすさで決まっている。

不明:
- 30 コマンド、26 文字、54 文、低音量 open vocabulary を同じ条件で比べた表は、この束だけでは作れない。
- 屋外、長時間装着、汗、再装着、会話相手ありの条件でどこまで保つかは、多くの実装で不明である。

### 2. 自然な音声復元の線は、まだ通信の完成品ではない

事実:
- Digital Voicing of Silent Speech は顔・顎・喉の EMG から音声を作り、closed-vocabulary の human WER 3.6% を出したが、open vocabulary では human WER 74.8%、automatic WER 68.0% までしか下がっていない。
- SottoVoce は顎下超音波から音声を再生し、Google STT WER を 41.03% から 33.56% に下げ、4 種 Alexa コマンド成功率は 65.0%、総時間は 2.61 s だった。
- Let There Be Sound は GRID で WER 17.07%、LipVoicer は LRS3 で ASR guidance あり 21.4%、なし 86.2% だった。Intelligible Lip-to-Speech with Speech Units は LRS3 WER 29.8% で、音声 unit を使うと multi-task 65.8% より大きく良かった。
- Cross-Modal Masking は 8 ch sEMG と lip video を組み合わせ、Whisper v3 WER を最大 14 absolute points 改善したが、喉頭摘出者への適応は弱いままだった。

推測:
- 音声が聞けることと、内容が正しく伝わることは別である。
- 生成研究の強みは「欠けた情報をそれらしく埋めること」だが、通信としては、その埋め方が外していないかを別に見ないと危ない。

不明:
- 人が聞いて誤解なく意思決定できる水準と、ASR の WER の関係は、この束だけでは統一して読めない。
- 話者が違う時、長文になった時、雑音や姿勢変化が入った時に、どこから急に崩れるかは十分に出ていない。

### 3. 脳信号や接触レス信号は、通信路というより「信号がある」証明に近い

事実:
- Zero-Shot Imagined Speech Decoding via Imagined-to-Listened MEG Mapping は 157 ch MEG、17人、76 語で Recall@1 が約 9.1% だった。
- Towards Neural Decoding of Imagined Speech based on Spoken Speech は 64 ch EEG、7人、5 クラスで imagined direct 30.5% +/- 4.9% だった。
- Continuous Silent Speech Recognition using EEG は review 束でも高い WER 側にあり、非侵襲脳信号は実用 SSI より基礎研究に近い。
- IR-UWB radar は 20人、8 母音・11 子音・25 語・12 句で、upper radar が 86.47%、81.59%、88.95%、96.88% だったが、closed set で配置依存が強い。

推測:
- これらは「何か読める」ことの証拠としては重要だが、「今日使う通信路」としてはまだ遠い。
- 研究価値は低くないが、運用条件の重さが性能値を打ち消している。

不明:
- 非侵襲脳信号が、低負担の装着で open vocabulary まで伸びる見込みは、この束だけでは読めない。
- 接触レス方式が日常姿勢や距離ずれにどれだけ弱いかも、十分に比較されていない。

### 4. 105件には、SSI本体ではなく部品研究がかなり混ざっている

事実:
- SonicVisionLM、Diff-Foley、audio-visual segmentation、target speech extraction、speech enhancement、environmental sound、telephony silent-call 判定などは、入力も出力も SSI の通信そのものではない。
- ただし、時間合わせ、雑音耐性、音声 unit、話者条件付け、評価指標、無音区間の扱いは、SSI に流用できる部品として何度も現れる。
- Surveys も多く、2020 review は理想遅延約 50 ms、100 ms までは許容余地、200 ms は通信を崩すと整理していた。

推測:
- この 105 件束は、SSI 単独の勝ち筋一覧ではなく、SSI 周辺を含む「使える部品の棚」に近い。
- そのため、見かけの件数よりも、中核の通信実験が少ないことを意識しないと判断を誤る。

不明:
- どの部品が本当に SSI 本体へ効くのかは、同一条件の統合実験が少なく、まだ整理不足である。

## 弱い結果と警告

事実:
- open vocabulary の完全無音通信で強い数値は少ない。
- speaker-dependent、closed set、lab 条件、offline 評価がまだ中心である。
- patient や laryngectomized を含む研究はあるが、強い数値より制約の記述が目立つ。

推測:
- この束を通信中心で読むと、「研究として強い」と「今日使える」はかなりずれる。
- 近い実装ほど、完全無音性より、狭い課題と運用の工夫に寄っている。

不明:
- このずれが 2026 年以降にどこまで縮むかは不明である。

## このloopで残った問い

事実:
- 使える系は、登録、語彙制限、低音量、既存音声系への接続を使っている。

推測:
- 次は「どこで性能を稼いだか」より、「誰がどの負担を払っているか」で読むと、実用差がさらにはっきりする。

不明:
- 負担の内訳を、ユーザー、装置、学習、環境、外部モデルにどう切るのが一番読みやすいかは、次の見方で試す必要がある。
