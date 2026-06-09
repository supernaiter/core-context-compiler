# Loop 02 Compressed

source:
- reports/ssi_10_loop_views/loops/loop_02_review.md

## 束

事実:
- 近い実装は、ユーザー負担を少し戻して成立している。LipLearner は few-shot 登録と user correction、SilentSpeller は custom palate と 1-2 h training、SottoVoce は話者ごと約 500 commands、Digital Voicing は subject-specific data を要する。
- 遠い方式は、装置と環境の負担が重い。Ultrasound は probe fixing と remount adaptation、radar は geometry 依存、multi-view video は複数視点、MEG/EEG は高密度装置が前提である。
- 生成系は、外部モデル負担が大きい。AKVSR は audio memory、Let There Be Sound は HuBERT 200 clusters、LipVoicer は lip-reader と ASR guidance、speech-unit 系は音声事前学習で欠損を埋める。
- 課題制限は負担の置き場所である。30 commands、26 letters、54 sentences、8 vowels/11 consonants/25 words/12 phrases、5 classes、76 words のように、多くは自由度を減らしている。
- open vocabulary 側へ寄ると、Digital Voicing human WER 74.8% / automatic 68.0% のように急に厳しくなる。WESPER と NasoVoce は open vocabulary 側だが、低音量・ささやきへ逃がしている。

推測:
- SSI の実用差は「どれだけ当たるか」より、「負担を誰に払わせたか」で読みやすい。
- 良い系は、ユーザー、装置、モデル、環境、課題のどれか一つを極端に重くせず、分散している。

不明:
- 受け入れ可能な登録時間、装着負担、再学習頻度、語彙制限の上限は分からない。
- 外部モデルの補完がどこから危険になるかも未整理である。

警告:
- 性能値はしばしば隠れた負担を隠す。
- limits を読まないと、lab 条件や外部知識依存を見落とす。
