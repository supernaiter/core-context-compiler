# Loop 03 Next View

source:
- reports/ssi_10_loop_views/loops/loop_03_compressed.md

## 次の見方

- 次は 105件を「誰がいつ誤りを直すか」で読む。
- 修正主体は、ユーザー、装置の自動補正、外部モデル、既存サービス、対話相手に分ける。

事実:
- 取得誤差は STN adaptation や sensor fusion が直していた。
- 発話モード差は metric learning、target transfer、domain adaptation が直していた。
- 自由度不足は speech units、ASR guidance、audio memory が直していた。
- 実用寄りの系は、edit gesture、active learning、smart speaker 接続、ASR/TTS 接続で最後の取りこぼしを直していた。

推測:
- SSI の差は、精度より「誤り訂正の契約」をどこへ置いたかで見える可能性が高い。
- 次のloopでは、誤りを機械が先に直す方式と、人が後で直す方式の差が中心になる。

不明:
- どの修正契約が最も速く、疲れにくく、誤解が少ないかは、この束だけではまだ決められない。
