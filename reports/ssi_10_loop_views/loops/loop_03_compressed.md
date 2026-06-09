# Loop 03 Compressed

source:
- reports/ssi_10_loop_views/loops/loop_03_review.md

## 束

事実:
- 第1段階の取得で多くが詰まる。Ultrasound STN+out は remount/cross-speaker gap の 88-92% を回復したが supervised adaptation が要る。IR-UWB radar は geometry 依存が強く、raw/clutter-only phoneme は 50% 未満。NasoVoce は whisper で vibration が弱い。
- 第2段階の発話モード差も大きい。Visual-only normal/whispered/silent は matched 68.0/70.5/62.2%、69.7/70.8/64.4%、normal->silent 59.7%、61.2%。Digital Voicing や pseudo target generation はこの差を埋めるための工夫だった。Cross-Modal Masking でも laryngectomized 適応は弱い。
- 第3段階で自由度を上げると誤りが跳ねる。Digital Voicing open vocabulary は高 WER、LipVoicer は guidance なしで 86.2%、Acoustic sensing は 54 文、SilentSpeller は spelling、LipLearner は 30 commands へ切って成立していた。
- 第4段階で受け渡しと訂正がある系だけが通信へ近づく。SottoVoce は smart speaker 接続、SilentSpeller は edit gestures、LipLearner は active learning、WESPER/NasoVoce は既存 ASR/TTS 接続がある。
- 2020 review の遅延目安は約 50 ms 理想、100 ms まで余地、200 ms は崩れやすい。SottoVoce 2.61 s はこの点でまだ重い。

推測:
- SSI の不足は前段から後段へ移動する。前段で取り切れない情報を、モード変換、言語補完、受け渡し後の訂正で埋めている。
- 実用差は「どの段階をどこまで埋めたか」で見るのがよい。

不明:
- 4 段階を同時に測る共通ベンチマークは見当たらない。
- どの誤りを誰が直すのが最も現実的かは未整理である。

警告:
- 単一段階の改善を、通信全体の改善と読まない方がよい。
- guidance や ecosystem 接続は強いが、同時に依存も増やす。
