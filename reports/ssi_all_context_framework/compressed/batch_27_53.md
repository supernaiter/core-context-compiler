# SSI review compression batch 27-53

### 27. Conditional Generation of Audio from Video via Foley Analogies (2023)
- id: conditional-generation-of-audio-from-video-via-foley-analogies
- trust: high; venue: arXiv / imported corpus page.
- did: Controlled Foley generation, not SSI: video plus exemplar audio -> soundtrack. Main move is analogy conditioning, self-supervised pairing, and sync-model re-ranking.
- evidence: Greatest Hits re-rank: 44.0% material, 66.7% action, 25.3% onset-count, 54.3 AP sync. AMT 376 participants prefer re-rank over base 54.3% material, 53.8% sync.
- conditions: Quantitative Greatest Hits; CountixAV/wild transfer qualitative.
- limits: Offline sound-design tool; timing fragile; sampling/re-ranking matter; onset transfer can still win simple onset sync.
- changes_view: Adds controllable neural Foley evidence, not silent-speech capability.

### 28. Speech Reconstruction from Silent Tongue and Lip Articulation By Pseudo Target Generation and Domain Adversarial Training (2023)
- id: speech-reconstruction-from-silent-tongue-and-lip-articulation-by-pseudo-target-generation-and-domain-adversarial-training
- trust: high; venue: arXiv / imported corpus page.
- did: Core SSI speech reconstruction: ultrasound tongue + lip video -> speech audio. Adds DTW pseudo acoustic targets, domain adversarial features, and iterative retraining for silent/vocalized mismatch.
- evidence: TaL: 81 English speakers, 1212 paired utterances, speaker-independent. Silent MCD 3.935 dB, STOI 0.517, WER 43.114%, MOS 3.330; vocalized WER 17.309%; about 15 WER-point and 0.34 MOS silent gain over TaLNet.
- conditions: MCD/STOI/WER via ASR, MOS, ablations.
- limits: No true silent acoustic target; pseudo-label alignment noise; silent lags vocalized; some speakers excluded; no real-time/deployment study.
- changes_view: Training recipe is the value, not just decoder architecture.

### 29. WESPER: Zero-shot and Realtime Whisper to Normal Voice Conversion for Whisper-based Speech Interactions (2023)
- id: wesper-zero-shot-and-realtime-whisper-to-normal-voice-conversion-for-whisper-based-speech-interactions
- trust: high; venue: CHI '23.
- did: Whispered microphone speech -> normal voice, zero-shot/realtime. Uses speech-to-unit and unit-to-speech modules learned from unpaired whisper/normal data.
- evidence: wTIMIT Google ASR: whisper WER/CER 44.70/28.38 -> WESPER 26.68/12.70. HuBERT-base with Librispeech+wTIMIT reaches 13.75/5.47. MOS/MUSHRA/ASR evaluation.
- conditions: Discreet audible whisper, non-autoregressive real-time stack.
- limits: Not fully silent; no silent-articulation benchmark or broad public-use robustness.
- changes_view: Low-friction whispered interaction adjacent to SSI, not core SSI.

### 30. Duration-aware pause insertion using pre-trained language model for multi-speaker text-to-speech (2023)
- id: duration-aware-pause-insertion-using-pre-trained-language-model-for-multi-speaker-text-to-speech
- trust: high; venue: arXiv / imported corpus page.
- did: Text -> TTS pause labels. BERT+BiLSTM with speaker embeddings predicts respiratory pauses and brief/medium/long punctuation pauses.
- evidence: LibriTTS: over 400,000 sentences, more than 2,000 speakers, MFA alignment. RPI respiratory 0.569 precision, 0.272 recall, F0.5 0.467. CPI respiratory 0.575/0.261/F0.5 0.463; punctuation 0.848 precision, 0.996 recall, F2 0.962. A/B: 30 listeners, 277 utterances, FastSpeech2+HiFi-GAN.
- conditions: English audiobook TTS rhythm metrics and preference tests.
- limits: Needs aligned text/audio and speaker embeddings; thresholds open; no silent articulation, SSI, conversational, or multilingual test.
- changes_view: TTS phrasing advance only adjacent to SSI synthesis.

### 31. LipLearner: Customizable Silent Speech Interactions on Mobile Devices (2023)
- id: liplearner-customizable-silent-speech-interactions-on-mobile-devices
- trust: high; venue: arXiv / imported corpus page.
- did: Smartphone front-camera lip video -> commands. Combines few-shot command enrollment, Voice2Lip, visual keyword spotting, on-device incremental learning, and real-time mobile use.
- evidence: One-shot 25-command F1 0.8947. App 30-command accuracy: one-shot 81.7%, five-shot 98.8%; keyword spotting EER 6.75%; latency about 422 ms. Uses LRW pretraining, 11 participants/7 conditions/9625 clips, plus 16-participant live study.
- conditions: Cross-condition, keyword spotting, registration, recognition; mainly frontal lips and command sets.
- limits: Visible lips required; similar commands confuse; active learning/user correction burden; open vocabulary and unseen environments unresolved.
- changes_view: Strong commodity-mobile SSI system evidence.

### 32. Towards Neural Decoding of Imagined Speech based on Spoken Speech (2022)
- id: towards-neural-decoding-of-imagined-speech-based-on-spoken-speech
- trust: medium-high; venue: arXiv / imported corpus page.
- did: 64-channel EEG imagined-speech label decoding using spoken-speech transfer; visual imagery is negative control.
- evidence: 7 subjects, 5 classes, 10-fold within-subject CV, CSP+SVM. Imagined direct 30.5% +/- 4.9% vs spoken-transfer 26.8% +/- 2.0% (p=0.0983). Visual imagery direct 31.8% +/- 4.1% vs transfer 26.3% +/- 2.4% (p=0.022).
- conditions: Offline small-vocabulary EEG, Kruskal-Wallis/bootstrap tests.
- limits: No deep model, online BCI, cross-subject split, latency, assistive study, or scalable vocabulary.
- changes_view: Interesting imagined-speech transfer baseline, not practical SSI.

### 33. Breaking the trade-off in personalized speech enhancement with cross-task knowledge distillation (2022)
- id: breaking-the-trade-off-in-personalized-speech-enhancement-with-cross-task-knowledge-distillation
- trust: high; venue: arXiv / imported corpus page.
- did: Causal personalized speech enhancement from mixed audio plus target-speaker conditioning. pVAD distillation down-weights inactive-target frames.
- evidence: TS1/TS2/TS3 with WER, DEL, DNSMOS, STOI, TSOS, leakage energy. S1 keeps over-suppression near B1 while improving TS3 leakage 46.5 dB -> 148.5 dB; TS2 WER 16.8 -> 17.8, TSOS 0.45 -> 0.37.
- conditions: Acoustic PSE scenario simulations.
- limits: No silent modality, interface, or SSI deployment; scenario-specific evidence.
- changes_view: Useful PSE trade-off control, outside SSI.

### 34. Movement Detection of Tongue and Related Body Parts Using IR-UWB Radar (2022)
- id: movement-detection-of-tongue-and-related-body-parts-using-ir-uwb-radar
- trust: high; venue: arXiv / imported corpus page.
- did: IR-UWB radar at chin -> binary tongue-motion labels. Hardware: radar module, LNA board, sinuous antennas, dielectric lens; envelope features + five-state left-to-right GMM-HMM.
- evidence: 4 participants, 2 tongue states, 20 repetitions/state. Leave-one-out vs CLEAN+MD-DTW gives 100%, 90%, 90%, 90% accuracy.
- conditions: Stationary lab, manual trial boundaries.
- limits: No continuous speech, unseen-user split, vocabulary recognition, or complete radar SSI.
- changes_view: Real narrow contactless tongue sensing; not speech decoding.

### 35. Lip-to-Speech Synthesis for Arbitrary Speakers in the Wild (2022)
- id: lip-to-speech-synthesis-for-arbitrary-speakers-in-the-wild
- trust: high; venue: arXiv / imported corpus page.
- did: Silent lip video -> speech audio for arbitrary speakers; emphasizes speaker conditioning and distributional modeling.
- evidence: GRID/TCD-TIMIT plus LRW/LRS2; metrics PESQ, STOI, SED, FDSD, KDSD, LSE-C/D, human ratings, fine-tuning curves. LRS2 uses thousands of speakers, about 59k vocabulary. Table 3 LRS2: 1.273 FDSD, 0.2 KDSD, 2.507 LSE-C, 8.155 LSE-D.
- conditions: Benchmark/human evaluation; 5 h adaptation can nearly match 20 h single-speaker model.
- limits: Severe head motion, non-frontal views, and lip ambiguity still cause wrong words; human study only 15 LRS2 samples/20 raters; no live latency/camera-noise deployment.
- changes_view: Meaningful move toward arbitrary in-the-wild lip-to-speech.

### 36. An Anchor-Free Detector for Continuous Speech Keyword Spotting (2022)
- id: an-anchor-free-detector-for-continuous-speech-keyword-spotting
- trust: high; venue: arXiv / imported corpus page.
- did: Continuous acoustic KWS as 1D detection. AF-KWS uses heatmap, length, offset heads and an unknown class for non-keywords, silence, noise.
- evidence: LibriTop-20: AP@5 0.952, AP@75 0.886, mAP 0.860, FRR@5 0.140, FRR@25 0.049, RTF 0.031, ahead of adapted classifiers; also CMAK-7.
- conditions: AP/mAP/FRR/RTF benchmarks on continuous microphone audio.
- limits: Audio KWS only; no SSI modality or interaction deployment.
- changes_view: Important formulation lesson: continuous KWS behaves like detection.

### 37. FastLTS: Non-Autoregressive End-to-End Unconstrained Lip-to-Speech Synthesis (2022)
- id: fastlts-non-autoregressive-end-to-end-unconstrained-lip-to-speech-synthesis
- trust: high; venue: arXiv / imported corpus page.
- did: Talking-face video -> waveform audio with non-autoregressive parallel decoder and GAN vocoder; removes main-path spectrogram bottleneck.
- evidence: Lip2Wav corpus 5 speakers/3 evaluated; GRID adaptation 3 speakers. GRID MOS: quality 3.59, intelligibility 3.68, naturalness 3.73 vs Lip2Wav 3.27/3.47/3.54. Waveform acceleration 19.76x at 3-second input.
- conditions: MOS, GRID PESQ, mel/waveform speed.
- limits: Offline windows, few evaluated speakers, no in-the-wild user study or conversational latency.
- changes_view: Strong latency/system gain, not new sensing.

### 38. Improved Processing of Ultrasound Tongue Videos by Combining ConvLSTM and 3D Convolutional Networks (2022)
- id: improved-processing-of-ultrasound-tongue-videos-by-combining-convlstm-and-3d-convolutional-networks
- trust: high; venue: arXiv / imported corpus page.
- did: 82 fps ultrasound tongue video -> mel-spectrogram -> WaveGlow speech. 3D-CNN+ConvLSTM replaces heavier upper temporal layers; hardware is Articulate Instruments Micro probe/headset plus ATR 3350 mic.
- evidence: One female Hungarian speaker, 438 sentences split 310/41/87. Best hybrid MSE about 0.276, mean R2 about 0.73, beating 3D-CNN and 3D-CNN+BiLSTM.
- conditions: Objective offline mel regression on train/dev/test.
- limits: Single speaker/language; no perceptual intelligibility, cross-speaker, robustness, or real-time test; specialized ultrasound.
- changes_view: Efficient SSI architecture evidence with narrow scope.

### 39. VisageSynTalk: Unseen Speaker Video-to-Speech Synthesis via Speech-Visage Feature Selection (2022)
- id: visagesyntalk-unseen-speaker-video-to-speech-synthesis-via-speech-visage-feature-selection
- trust: high; venue: arXiv / imported corpus page.
- did: Video -> speech for unseen speakers by separating speech content from visage/identity style using multi-head feature-selection masks and style-conditioned synthesis.
- evidence: GRID, TCD-TIMIT volunteer, LRW; unseen splits; LRW has 17,580 clustered speaker identities. Unseen GRID STOI/ESTOI/PESQ 0.567/0.308/1.373; unseen TCD-TIMIT 0.478/0.217/1.410. GRID MOS 20 samples/16 raters: 2.96 naturalness, 3.35 intelligibility, 3.34 voice match.
- conditions: Offline benchmarks, MOS, EER disentanglement probe.
- limits: Far from natural speech; needs clean aligned cropped face video; no camera-noise, pose, occlusion, real-time, or in-wild test.
- changes_view: Content-style split is operational, not decorative.

### 40. Silence is Sweeter Than Speech: Self-Supervised Model Using Silence to Store Speaker Information (2022)
- id: silence-is-sweeter-than-speech-self-supervised-model-using-silence-to-store-speaker-information
- trust: high; venue: arXiv / imported corpus page.
- did: SSL speech probing: silence fragments carry speaker information. Utterances split into 10 fragments with learned SID weights.
- evidence: High-silence last fragment contributes most. Across HuBERT variants and wav2vec2, silence improves SID/ASV. Adding 1/10 waveform silence raises HuBERT SID 0.807 -> 0.824 and HuBERT-Large 0.890 -> 0.892 on VoxCeleb; silence ratio below 5% reduces SID 30-50%.
- conditions: Fixed upstream SSL, linear speaker-ID probes, no upstream finetuning.
- limits: Model/data-specific; causal mechanism unproven; modest larger-model effects; no content decoding, SSI modality, or deployment.
- changes_view: Representation insight, not SSI system evidence.

### 41. SVTS: Scalable Video-to-Speech Synthesis (2022)
- id: svts-scalable-video-to-speech-synthesis
- trust: high; venue: arXiv / imported corpus page.
- did: Scalable lip-video -> speech: ResNet18+conformer video-to-spectrogram predictor plus pretrained Parallel WaveGAN.
- evidence: GRID 27 h, LRW about 150 h, LRS3 312 h, LRS3+VoxCeleb2 over 1,500 h. GRID seen PESQ/STOI/ESTOI/WER 1.97/0.705/0.523/2.36%; GRID unseen 1.40/0.588/0.318/17.85%; LRW unseen 1.49/0.649/0.483/13.4%. Vocoder about 54.7 clips/sec on GRID with RTX 2080 Ti.
- conditions: Benchmark metrics, loss/vocoder ablations; LRS3 WER omitted because ASR unreliable.
- limits: Needs curated aligned lip video; unseen/unconstrained fidelity weak; no user/deployment validation.
- changes_view: Foundational data-scaling baseline for VTS.

### 42. Listen only to me! How well can target speech extraction handle false alarms? (2022)
- id: listen-only-to-me-how-well-can-target-speech-extraction-handle-false-alarms
- trust: high; venue: arXiv / imported corpus page.
- did: Target speech extraction from mixture + enrollment speech, centered on inactive-speaker false alarms; verification-based handling beats direct zero-output training.
- evidence: LibriMix: 13,900 Train-100k, 50,800 Train-360k, 3,000 validation, 3,000 test. At 10 s enrollment, TSE-V(360): 13.6 dB SDRi before detection, 1.7% fail rate, 6.3% EER, 7.1% fail-and-miss.
- conditions: SDRi, fail rate, EER, attenuation, enrollment sweeps.
- limits: SpeakerBeam/LibriMix acoustic benchmark; TSE-V needs extra verification and 15-20 s enrollment for about 5% EER; no silent modality.
- changes_view: Strong TSE failure analysis, outside SSI.

### 43. Multi-modality Associative Bridging through Memory: Speech Sound Recollected from Face Video (2022)
- id: multi-modality-associative-bridging-through-memory-speech-sound-recollected-from-face-video
- trust: high; venue: arXiv / imported corpus page.
- did: Audio-visual memory bridge lets visual-only inference borrow audio structure for lip reading and face-video speech reconstruction.
- evidence: LRW/LRW-1000 word accuracy 85.4/50.82, ahead of listed prior work. Speaker-dependent GRID subjects 1,2,4,29: STOI 0.738, ESTOI 0.579, PESQ 1.984. Human ratings included; best subjective scores use extra WaveNet vocoder.
- conditions: LRW/LRW-1000 word benchmarks plus GRID reconstruction.
- limits: Paired audio-video supervision and benchmark preprocessing; no speaker-independent reconstruction, live deployment, or uncontrolled capture.
- changes_view: Memory bridge does real work, especially on LRW-1000.

### 44. VCVTS: Multi-speaker Video-to-Speech synthesis via cross-modal knowledge transfer from voice conversion (2022)
- id: vcvts-multi-speaker-video-to-speech-synthesis-via-cross-modal-knowledge-transfer-from-voice-conversion
- trust: high; venue: arXiv / imported corpus page.
- did: Silent lip video plus reference speech -> multi-speaker VTS. Transfers voice-conversion content units, speaker encoder, pitch predictor, decoder, and Lip2Ind.
- evidence: GRID seen/unseen, LRW; metrics PESQ, STOI, ESTOI, MCD, F0-RMSE, MOS naturalness/similarity. Unseen GRID with Griffin-Lim: PESQ 1.417, STOI 0.582, ESTOI 0.330, MOS naturalness 3.25, MOS speaker similarity 2.66.
- conditions: Offline objective/subjective benchmarks with reference speech for speaker control.
- limits: Large seen/unseen gap; vocoder-dependent quality; complex reference-speech system; no interactive SSI validation.
- changes_view: Clear cross-modal transfer advance for multi-speaker VTS.

### 45. Supervised and Self-supervised Pretraining Based COVID-19 Detection Using Acoustic Breathing/Cough/Speech Signals (2022)
- id: supervised-and-self-supervised-pretraining-based-covid-19-detection-using-acoustic-breathing-cough-speech-signals
- trust: high; venue: ICASSP 2022.
- did: Respiratory/audio COVID-19 classifier from breathing, cough, speech using BiLSTM with supervised/self-supervised pretraining and ensembles.
- evidence: DiCOVA-ICASSP 2022/Coswara; 5-fold CV plus blind test. Track-1 ensemble: 86.72 test AUC, 80.05 validation AUC; abstract reports 88.44% AUC on blind fusion track.
- conditions: ROC-AUC medical audio challenge.
- limits: No silent articulation, speech interface, SSI hardware, or deployment path.
- changes_view: Out of SSI scope despite acoustic modeling.

### 46. VisualTTS: TTS with Accurate Lip-Speech Synchronization for Automatic Voice Over (2022)
- id: visualtts-tts-with-accurate-lip-speech-synchronization-for-automatic-voice-over
- trust: high; venue: arXiv / imported corpus page.
- did: Text script + silent lip video -> synchronized TTS for automatic voice-over. Adds textual-visual attention and visual fusion during acoustic decoding.
- evidence: GRID: 33 speakers, 900 train/100 test each, 24 kHz audio, 25 Hz lip video. LSE-C 5.87 higher better, LSE-D 8.45 lower better, FD 5.92 lower better. MOS 4.17+/-0.06 from 12 listeners.
- conditions: Objective sync metrics and MOS/preference on scripted paired text/video.
- limits: Needs matching script and prerecorded video; fixed GRID grammar/vocabulary; no spontaneous, unseen-speaker, real-time, or mobile test.
- changes_view: Dubbing sync advance, not silent-video speech decoding.

### 47. Sequence-to-Sequence Voice Reconstruction for Silent Speech in a Tonal Language (2022)
- id: sequence-to-sequence-voice-reconstruction-for-silent-speech-in-a-tonal-language
- trust: high; venue: arXiv / imported corpus page.
- did: Mandarin facial sEMG -> speech audio. Five Ag/AgCl channels at 2000 Hz near nose/mouth/chin/neck. SSRNet uses DTW duration extraction, length regulation, toneme loss, vocal-sEMG reconstruction, Parallel WaveGAN.
- evidence: Six Mandarin speakers, AISHELL-3 read sentences, about 5.79 h silent speech, 8:1:1 split. ASR CER 21.99% +/- 4.99% vs baseline 46.62%; subjective CER 6.41% average, best 1.19%, baseline 39.76%; MCD/STOI/naturalness with 10 listeners.
- conditions: Speaker-dependent controlled read speech.
- limits: No cross-speaker/environment, mobile/walking, latency, or real-time test; fixed electrodes and limited vocabulary/coverage.
- changes_view: Important tonal SSI result: duration and toneme supervision matter.

### 48. SilentSpeller: Towards mobile, hands-free, silent speech text entry using electropalatography (2022)
- id: silentspeller
- trust: high; venue: CHI '22.
- did: Silent spelling text entry using SmartPalate electropalatography: 124 capacitive electrodes, 100 Hz, tongue-palate contact, HMM triletter states, 16 PCA eigen-palate features, 26 letters plus space.
- evidence: 2328 isolated words/1164 unique: about 97% character, 92% word. Unseen 100 words: 94.5%/85.5%. Walking vs seated: 97.5% vs 96.5% character. Live seven-user entry: 37 wpm at 87% average; best 53 wpm at 91%.
- conditions: 10-fold CV, unseen-word reserve, walking/seated phrases, live push-to-talk/edit gestures; tuning mainly two users.
- limits: Custom dental impression; obtrusive wired/partial wireless hardware; 1-2 h user-dependent training; user-independent about 55%; B/P and D/T/Z confusions; no punctuation/capitalization.
- changes_view: Major SSI reframing: less natural, more usable for mobile text entry.

### 49. SA-SDR: A novel loss function for separation of meeting style data (2021)
- id: sa-sdr-a-novel-loss-function-for-separation-of-meeting-style-data
- trust: high; venue: arXiv / imported corpus page.
- did: Speech-separation loss for meeting audio with silent targets. Source-aggregated SDR computes one global SDR over all outputs instead of channel-wise averages.
- evidence: WSJ0-2mix BSSEval SDR 18.0 with SA-SDR vs 17.8 A-SDR. Meeting-style data: 19.8 BSSEval SDR and 16.1 SA-SDR; SA-tSDR reaches 17.9 SA-SDR. Also WER, attenuation ratio, VAER.
- conditions: Offline acoustic separation benchmarks.
- limits: No silent-speech modality, SSI system, or human-facing deployment.
- changes_view: Objective-design lesson for silence in meetings, not SSI.

### 50. Advances and Challenges in Deep Lip Reading (2021)
- id: advances-and-challenges-in-deep-lip-reading
- trust: high; venue: arXiv / imported corpus page.
- did: Survey of deep visual speech recognition datasets, modules, data challenges, evaluation criteria, and open problems.
- evidence: Synthesizes controlled vs in-the-wild datasets and notes controlled sets transfer poorly to real conditions. Metrics reviewed: word accuracy, sentence accuracy, error-rate family, BLEU.
- conditions: Literature review for lip reading and SSI-adjacent context.
- limits: No original model, benchmark, experiment, or deployment evidence.
- changes_view: Orientation source only; do not treat as system performance evidence.

### 51. Sub-word Level Lip Reading With Visual Attention (2021)
- id: sub-word-level-lip-reading-with-visual-attention
- trust: high; venue: arXiv / imported corpus page.
- did: Silent video -> text lip reading with visual transformer pooling, WordPiece decoding, and AVA ActiveSpeaker transfer.
- evidence: LRS2/LRS3 WER: public-data 28.9/40.6; extended training 22.6/30.7. Ablation: WordPiece improves LRS2 41.0 -> 37.2; VTP further to 30.9.
- conditions: Offline benchmark WER and visual speech detection transfer.
- limits: Camera/video-quality and benchmark-corpus dependence; no live dictation, on-device latency, privacy, or real-world robustness study.
- changes_view: Strong visual speech recognition, adjacent not articulatory SSI.

### 52. Speech Synthesis from Text and Ultrasound Tongue Image-based Articulatory Input (2021)
- id: speech-synthesis-from-text-and-ultrasound-tongue-image-based-articulatory-input
- trust: high; venue: arXiv / imported corpus page.
- did: DNN-TTS with text plus ultrasound tongue-image features from Articulate Instruments Micro probe/headset.
- evidence: 8-speaker dev/test with MCD, BAP, F0-RMSE, F0-CORR, F0-VUV, probe-misalignment analysis. Text+ultrasound lowest MCD for all 8 speakers: 03mn 5.442 vs 5.652 text-only; 06fe 5.236 vs 5.447; ultrasound-only 7.153 and 7.050.
- conditions: Speaker-dependent offline synthesis metrics.
- limits: Best system needs text; ultrasound-only weak; limited data, speaker dependence, probe misalignment, no listening tests, probe headset.
- changes_view: Articulatory side info helps TTS; not standalone SSI.

### 53. Sparsely Overlapped Speech Training in the Time Domain: Joint Learning of Target Speech Separation and Personal VAD Benefits (2021)
- id: sparsely-overlapped-speech-training-in-the-time-domain-joint-learning-of-target-speech-separation-and-personal-vad-benefits
- trust: high; venue: arXiv / imported corpus page.
- did: Target speech separation with personal VAD for sparse-overlap audio. Weighted SI-SNR and pVAD treat target absence and sparse overlap explicitly.
- evidence: VoiceFilter-style fully overlapped plus SparseLibri2Mix clean/noisy. Gains: 1.73 dB SDR fully overlapped, 4.17 dB average SDR clean sparse, 0.9 dB noisy sparse. Early VAD branch reduces RTF 0.61 -> 0.47 with SDR cost.
- conditions: Offline synthetic/semi-synthetic acoustic benchmarks with target-speaker embeddings.
- limits: Standard audio separation, not silent/articulatory input; no SSI hardware, user study, or silent communication loop.
- changes_view: Credible sparse-overlap/activity engineering, outside SSI.
