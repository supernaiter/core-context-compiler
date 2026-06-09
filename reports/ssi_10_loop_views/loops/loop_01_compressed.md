# Loop 01 Compressed

source:
- reports/ssi_10_loop_views/loops/loop_01_review.md

## 束

事実:
- 105件を通信として読み直すと、近い実装は自由会話の完全無音復元ではなく、課題を狭めた系に集まる。
- LipLearner は 30 コマンドで one-shot 81.7%、five-shot 98.8%、約 422 ms。SilentSpeller は平均 37 wpm 87%、最良 53 wpm 91%。
- Acoustic sensing は 54 文で unseen-sentence WER 8.1% だが、文集合が小さい。
- NasoVoce と WESPER は低音量やささやきで open vocabulary 側へ寄るが、完全無音ではない。
- Digital Voicing は closed-vocabulary human WER 3.6% でも、open vocabulary は human 74.8%、automatic 68.0% と高い。
- SottoVoce は Alexa コマンド成功率 65.0%、総時間 2.61 s。LipVoicer は ASR guidance を外すと LRS3 WER が 21.4% から 86.2% へ悪化する。
- MEG imagined speech は Recall@1 約 9.1%、EEG imagined direct は 30.5% +/- 4.9%。IR-UWB radar は closed set で高いが配置依存が強い。
- 105件には Foley、音声分離、AV segmentation、環境音、telephony silent-call 判定など SSI 外や隣接の部品研究がかなり含まれる。
- 2020 review は遅延の目安を、理想約 50 ms、100 ms まで許容余地、200 ms は崩れやすいと整理していた。

推測:
- 今日使える線は「無音性の純度」より、「入力を狭める」「登録する」「低音量で逃がす」「既存音声系へ渡す」にある。
- 自然な音声を出す研究は、通信内容の正しさを外部モデルで補っている場合が多い。
- SSI 束というより、SSI 本体と部品棚を一緒に見ていると考えた方が実態に近い。

不明:
- コマンド、綴り、54 文、低音量 open vocabulary を同一条件で比べる横並びはない。
- 屋外、長時間、再装着、患者使用、対話中の訂正まで含めた実運用差はまだ見えにくい。

警告:
- 高精度でも closed set、speaker-dependent、lab、offline のことが多い。
- 音声が自然に聞こえることと、内容が正しく伝わることを混同しやすい。
