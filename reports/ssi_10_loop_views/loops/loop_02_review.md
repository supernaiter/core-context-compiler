# Loop 02 Review

input:
- reports/ssi_all_context_framework/all_compressed_codex.md
- reports/ssi_all_context_framework/framework_from_all_compressed.md

previous_view:
- reports/ssi_10_loop_views/loops/loop_01_next_view.md

## 今回の見方

- 105件を「誰が負担を払っているか」で読み直す。
- 負担は、ユーザー、装置、学習、環境、外部モデル、課題制限に分ける。

## 読み直し

### 1. 近い実装は、負担をユーザーへ少し戻して成立している

事実:
- LipLearner は few-shot 登録と user correction を使う。30 コマンドで five-shot 98.8% まで上がる一方、似たコマンド混同と active learning 負担が残る。
- SilentSpeller は 1-2 h の user-dependent training、custom dental impression、B/P と D/T/Z の混同、punctuation と capitalization なしという制約がある。それでも平均 37 wpm 87%、最良 53 wpm 91% を出す。
- SottoVoce は話者ごとに約 500 commands を集める speaker-dependent 設計で、超音波プローブと表示撮像の負担が大きい。
- Digital Voicing は substantial subject-specific data と facial EMG gear を要する。
- Acoustic sensing も 54 文という狭い文設計に課題制限の負担を置いている。

推測:
- 実用に近い系は、完全自動化を諦めて、登録、綴り、少数コマンド、訓練時間といった形でユーザーに一部の負担を払ってもらっている。
- その代わり、外部環境やモデルの不確実性を減らしている。

不明:
- 多くのユーザーが受け入れる登録時間の上限が何分か、何日かは、この束だけでは分からない。
- 入力の手間と会話速度の交換条件も未整理である。

### 2. 遠い方式は、装置と環境の負担が重い

事実:
- Ultrasound 系は probe fixing headset、再装着、角度ずれ、表示撮像などの負担が何度も出る。STN adaptation は 4 話者・4 remounted sessions で adaptation gap の 88-92% を埋めたが、そもそも supervised adaptation が必要である。
- IR-UWB radar は upper/lower antenna geometry が効き、歯や距離で舌情報が欠ける。
- Multi-view lip-to-speech は 30/45/60/90 度など複数カメラ配置が前提になりやすい。
- MEG は 157 ch、EEG は 64 ch や 128 ch 級で、装置負担が日常利用から遠い。
- Brain2Char や ECoG 系は科学的には強いが、侵襲性や機器制約が大きい。

推測:
- 装置負担が重い方式は、少し性能が良くても、通信路としては実装順が下がる。
- 超音波やレーダーで見えている課題は、モデル不足より、位置合わせと再装着の課題であることが多い。

不明:
- 軽量化や固定治具の改善で、どこまで装置負担が減るかは束だけでは読めない。
- 多視点カメラや高密度脳計測が、低コスト版へ縮む速度も不明である。

### 3. 生成系は、負担を外部モデルと事前学習へ押し出している

事実:
- AKVSR は HuBERT/CPC/wav2vec2 の audio memory を使い、LRS3 WER を 46.1% から 29.1%、条件によって 23.6% まで下げた。
- Let There Be Sound は HuBERT-large layer 12 と 200 clusters を使い、GRID WER 17.07% を出した。
- LipVoicer は lip-reader text と ASR classifier guidance に強く依存し、guidance を外すと LRS3 WER 21.4% から 86.2% へ崩れる。
- Intelligible Lip-to-Speech with Speech Units は text ラベルなしでも unit supervision を使い、LRS3 WER 29.8% を得た。
- VCVTS、VisualTTS、automatic voice-over、large-scale audio pretraining も、情報不足を外部表現で埋める方向に並ぶ。

推測:
- これらは「口や筋電だけで全部読む」より、「外部の音声知識で欠損を埋める」設計である。
- 性能改善の多くは、本体入力が良くなったというより、補完器が強くなった結果かもしれない。

不明:
- どこまでが妥当な補完で、どこからが思い込みになるかは、同一条件の評価が足りない。
- text guidance や strong LM の注入が、誤り時にどの程度危険かも十分に測られていない。

### 4. 課題制限は弱さではなく、負担の置き場所である

事実:
- LipLearner は command sets、SilentSpeller は spelling、KDE-SSI は 26 NATO words、IR-UWB radar は 8 母音・11 子音・25 語・12 句、visual-only normal/whispered/silent は digits と fixed phrases、imagined EEG は 5 classes、MEG は 76 poem content words だった。
- Digital Voicing の open vocabulary は 9,828 words でも WER が高い。open vocabulary 化と高精度は同時には進んでいない。
- WESPER と NasoVoce は open vocabulary に近いが、無音ではなく低音量・ささやきへ負担を置いている。

推測:
- 課題制限は逃げではなく、負担配分の決定である。
- 実際には、「語彙を狭める」「入力作法を変える」「低音量へ逃がす」のどれかで、通信として成立する側へ寄せている。

不明:
- どの制限が最も受け入れられやすいかは、用途別に違いそうだが、束だけでは分けきれない。

## 弱い結果と警告

事実:
- 多くの論文は負担を明示せず、性能だけを先に出す。
- だが limits を読み直すと、装着、登録、再学習、センサー配置、合成雑音、lab capture、offline 推論が繰り返し現れる。

推測:
- SSI の差は精度差より、負担の隠し方の差である。
- そのため、headline 数値だけで近さを決めると危ない。

不明:
- 負担を定量化する共通表は、この束にはない。

## このloopで残った問い

事実:
- 負担は一箇所ではなく、取得、変換、補完、操作に分散している。

推測:
- 次は「どの段階で情報不足を直しているか」で読むと、負担と失敗の移動が見えやすい。

不明:
- 段階の切り方は、取得、発話モード変換、解読自由度、出力後の訂正、の 4 つがよさそうだが、次で確かめる必要がある。
