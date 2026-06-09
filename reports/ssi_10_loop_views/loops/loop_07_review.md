# Loop 07 Review

## 前提

- 使った前の見方: `reports/ssi_10_loop_views/loops/loop_06_next_view.md`
- 入力: `reports/ssi_all_context_framework/all_compressed_codex.md` の 105件の圧縮済みレビュー
- 弱点: 入力は 105件の圧縮済みレビューであり、原論文全文ではない
- 今回の見方: 105件を、壊れた時にどう戻すかで読む

## レビュー

### 事実

- 明示的な戻し方を持つ例は少ない。圧縮束で user correction や edit gesture がはっきり書かれているのは `LipLearner` と `SilentSpeller` のような一部に限られる。
- `LipLearner` は few-shot enrollment と active learning を持ち、30 command accuracy が one-shot 81.7% から five-shot 98.8% に上がる。これは失敗後に再登録で戻す設計である。
- `SilentSpeller` は live push-to-talk と edit gestures を持ち、平均 37 wpm・87%、best 53 wpm・91% を出した。誤りを全文やり直しではなく、綴りと編集で小さく戻す発想である。
- `NasoVoce` と `WESPER` は完全無音が崩れた時に、low-volume や whisper の経路で既存 ASR へ逃げられる。これは SSI そのものの解決ではないが、通信を止めにくい。
- `SottoVoce` は regenerated audio を smart speaker に渡すので運用上の逃げ道はあるが、成功率 65.0%、Google STT WER 33.56%、2.61 s 総処理で戻し方が速いとは言えない。
- `AKVSR`、`LipVoicer`、`RobustL2S`、speech unit 系は、誤りの多くをユーザーの前に外部モデルで吸収する設計だが、信頼度表示、拒否、部分修正の報告は圧縮束であまり見えない。
- 超音波 STN、cross-modal masking、metric learning は入力側のずれを先に直すが、失敗後の運用手順より、事前のモデル補正に重心がある。
- 苦しい路線ほど戻し方の情報が薄い。TaL80 silent WER 69.84、EEG cross-subject WER 92.55、`Brain2Char` silent/mimed 40%/67% のような例では、誤認識後の安全な停止や復帰方法は読み取れない。

### 推測

- 実用差は最高精度より、失敗を小さく閉じられるかで分かれる。
- 低音量系、綴り系、コマンド系が近く見えるのは、完全正解だからではなく、壊れても短く戻せるからである可能性が高い。
- 生成系や復元系は見栄えが強くても、戻し方が設計されていないと日常利用では弱い。

### 不明

- confidence、reject、partial edit、handoff を含めた最良の復帰設計は不明である。
- 患者や初学者でも同じ戻し方が使えるかは分からない。
- 誤作動が危険な場面で、どの路線が最も安全に止まれるかも不明である。

### 警告

- 戻し方が書かれていない高スコアは、実利用では予想以上に脆い可能性がある。
- 低音量への逃げ道は実用上は強いが、完全無音 SSI の到達度とは分けて扱う必要がある。

## 今回の結論

### 事実

- 戻し方が明示されている研究は少なく、明示されていても綴り、再登録、既存 ASR への逃げ道に偏っている。

### 推測

- 次は、そもそも何が通信を止める停止条件なのかで読むべきである。

### 不明

- どの停止条件を先に外すと復帰コストが最も下がるかはまだ粗い。
