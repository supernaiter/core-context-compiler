# SSI review compression batch 54-79

- venue: arXiv / imported corpus page for all entries

### 54. Silent Speech and Emotion Recognition from Vocal Tract Shape Dynamics in Real-Time MRI (2021)
- id: silent-speech-and-emotion-recognition-from-vocal-tract-shape-dynamics-in-real-time-mri
- trust: high; real sentence-level rtMRI result, but lab-only.
- did: rtMRI vocal-tract video to text; lip/oral/palate/throat/tongue sensing; USC-EMO-MRI emotion/gender geometry.
- evidence: USC-TIMIT unseen phrases-with-LM: 40.6 PER, 39.4 CER, 42.1 WER; older baselines: 58% VCV error, 57% phoneme error.
- conditions: Offline USC-TIMIT recognition plus USC-EMO-MRI articulatory analysis.
- limits: MRI is large/immobile; no latency, deployable hardware, accessibility trial, or day-use path.
- changes_view: Extends rtMRI toward sentence recognition, but keeps it as research instrumentation, not practical SSI.

### 55. Neural Speaker Embeddings for Ultrasound-based Silent Speech Interfaces (2021)
- id: neural-speaker-embeddings-for-ultrasound-based-silent-speech-interfaces
- trust: high for embeddings; weaker for synthesis gain.
- did: X-vectors from tongue ultrasound condition ultrasound-to-spectrum synthesis; Micro 64x842@82 fps resized 64x128; tongue to speech audio.
- evidence: Speaker error: 1.96% on 50-speaker dev with 164 frames / 2 sec; 0.70% on held-out 31. Synthesis MSE: single 0.265; 31-speaker no x-vector 0.669; x-vector 0.653; MCD 3.12.
- conditions: Recognition generalizes embeddings; synthesis train/dev/test share the same 31 speakers.
- limits: Marginal synthesis gain; no speaker-independent SSI, probe-shift, cross-session, live, or deployment test.
- changes_view: Ultrasound carries speaker identity; naive embedding injection does not solve multi-speaker SSI.

### 56. An Improved Model for Voicing Silent Speech (2021)
- id: an-improved-model-for-voicing-silent-speech
- trust: high; strong speaker-dependent facial EMG reconstruction.
- did: Learns convolutional EMG features, uses Transformer layers, and adds auxiliary phoneme loss for face EMG to speech audio.
- evidence: Automatic WER improves from 68.0% to 42.2%; human transcription averages 32.3% WER. Ablations worsen to 45.2%, 46.0%, and 51.7%.
- conditions: One English speaker, 19 hours silent/vocalized EMG; open-vocabulary automatic WER plus 40 human-rated samples by two raters.
- limits: No cross-speaker/session, wearable, mobility, recalibration, or real-world test; voicing distinctions remain hard.
- changes_view: Learned features + Transformer + phoneme loss matter, but only within one-speaker lab data.

### 57. Voice Activity Detection for Ultrasound-based Silent Speech Interfaces using Convolutional Neural Networks (2021)
- id: voice-activity-detection-for-ultrasound-based-silent-speech-interfaces-using-convolutional-neural-networks
- trust: high for narrow preprocessing claim.
- did: CNN separates ultrasound tongue-image speech/silence labels and tests silence removal before ultrasound SSI reconstruction.
- evidence: VAD reaches 0.852 accuracy, 0.9 F1, 0.859 ROC AUC. Conv3D+BiLSTM SSI with silence removed gives test MCD 3.05 versus 3.12 with 180 ms silence retained.
- conditions: Single-speaker TaL1; speech-derived labels; downstream reconstruction comparison.
- limits: No cross-speaker, live, probe-shift, silence-style, or new-user robustness.
- changes_view: Ultrasound VAD works and slightly helps reconstruction; not a general SSI result.

### 58. Speaker disentanglement in video-to-speech conversion (2021)
- id: speaker-disentanglement-in-video-to-speech-conversion
- trust: high for GRID-style controllable video-to-speech.
- did: Silent lip video to speech audio with explicit speaker ID/embedding and adversarial removal of speaker identity from visual features.
- evidence: GRID: 34,000 samples, 34 speakers, 52 words. Unseen control: normalized rev-grad WER 38.9%, EER 11.9%; speaker-independent linear WER 42.7%, EER 7.3%. Speaker-dependent baseline WER 17.8%, STOI ~0.468, PESQ ~1.85, MCD ~32 dB.
- conditions: WER/EER/STOI/PESQ/MCD plus listening tests; unseen speakers use synthetic pairings.
- limits: Closed vocabulary/read grammar; no open-vocabulary or spontaneous speech; intelligibility/speaker-control trade-off.
- changes_view: Makes voice control explicit, but remains GRID-bound.

### 59. Improving Neural Silent Speech Interface Models by Adversarial Training (2021)
- id: improving-neural-silent-speech-interface-models-by-adversarial-training
- trust: high for objective training comparison.
- did: Adds Patch-GAN adversarial loss to MSE-trained 3D CNN ultrasound-to-mel-spectrogram mapping; under-chin Articulate Instruments Micro probe; tongue to speech audio.
- evidence: GAN training gives consistent slight gains over MSE-only on MSE, R2, STOI, ESTOI, PESQ, SI-SDR, SDR, PMSQE, and MCD.
- conditions: Single-speaker Hungarian female 438 sentences; TAL1 English 1015 train / 50 dev / 24 test; held-out objective metrics only.
- limits: No listening tests, multi-speaker/speaker-independent, real-time, or deployment evidence; improvement is modest.
- changes_view: Adversarial loss is a useful refinement, not a major architecture shift.

### 60. 3D Convolutional Neural Networks for Ultrasound-Based Silent Speech Interfaces (2021)
- id: 3d-convolutional-neural-networks-for-ultrasound-based-silent-speech-interfaces
- trust: high for speaker-dependent ultrasound regression.
- did: Compact (2+1)D 3D CNN maps tongue ultrasound video to 13 LSP vocoder coefficients; Micro 2-4 MHz, 64-element transducer, 82 fps.
- evidence: One Hungarian female, 438 sentences split 310/41/87. Best 5-frame stride s=6 (~300 ms): MSE 0.315, R2 0.683; 2D CNN 0.366/0.633; CNN+LSTM 0.336/0.661.
- conditions: Objective FCN/2D/3D/CNN+LSTM comparison; no F0 estimate.
- limits: Single-speaker read-aloud data; no listening, intelligibility, silent-articulation, real-time, or probe-shift test.
- changes_view: 3D temporal convolution beats recurrent baseline efficiently, but remains pre-deployment.

### 61. HTMD-Net: A Hybrid Masking-Denoising Approach to Time-Domain Monaural Singing Voice Separation (2021)
- id: htmd-net-a-hybrid-masking-denoising-approach-to-time-domain-monaural-singing-voice-separation
- trust: medium-high; good audio separation, out of SSI.
- did: Serial latent masking + denoising with skip connections/deep supervision for monaural singing voice separation.
- evidence: MUSDB18: 100 train / 50 test at 22.05 kHz mono. Median SDR 5.16 dB, SIR 10.24 dB, SAR 8.53 dB; VAD 84.7%. Wilcoxon/McNemar: Conv-TasNet-like SDR, better silent-segment handling, Wave-U-Net worse.
- conditions: Objective SDR/SIR/SAR plus PES/VAD; no subjective listening.
- limits: Music-only; no speech restoration, SSI, deployment, or cross-domain adaptation.
- changes_view: Silent-segment handling in source separation is a distractor, not silent speech progress.

### 62. Silent versus modal multi-speaker speech recognition from ultrasound and video (2021)
- id: silent-versus-modal-multi-speaker-speech-recognition-from-ultrasound-and-video
- trust: high; core multi-speaker SSI recognition.
- did: Recognizes modal/silent/whispered speech from ultrasound tongue imaging plus lip video; analyzes articulatory space/rate; output text.
- evidence: TaL1: six sessions, one professional speaker; TaL80: +81 native English speakers. TaL80 silent WER 77.79 to 69.84 with fMLLR + unsupervised adaptation; modal raw WER 39.34. TaL1 silent WER 52.64 to 37.94.
- conditions: WER by speaking mode plus syllable-rate and convex-hull analysis.
- limits: Silent WER still high; controlled capture and adaptation required; no live interface/user task.
- changes_view: Main value is mismatch diagnosis: silent speech is slower, smaller in articulatory space, and harder than modal.

### 63. EMA2S: An End-to-End Multimodal Articulatory-to-Speech System (2021)
- id: ema2s-an-end-to-end-multimodal-articulatory-to-speech-system
- trust: high; strong lab EMA synthesis baseline.
- did: EMA on lips, jaws, tongue, velum to waveform via Parallel WaveGAN and joint spectrogram/mel/deep-feature loss.
- evidence: NTT EMA: 3 speakers, 354 utterances each, 304/50 train/test. EMA2S vs baseline: MCD 7.176/7.815, PESQ 1.350/1.279, STOI 0.716/0.696, CCR 0.868/0.818. A/B: 10 participants, 15 questions, 83% vs 17%.
- conditions: Objective metrics, ASR CCR, subjective A/B, and reduced-sensor ablation.
- limits: Small lab corpus; no cross-speaker generalization; EMA remains intrusive even with four sensors.
- changes_view: Neural vocoder + joint loss improves naturalness, but hardware blocks practical SSI.

### 64. Convolutional Neural Network-Based Age Estimation Using B-Mode Ultrasound Tongue Image (2021)
- id: convolutional-neural-network-based-age-estimation-using-b-mode-ultrasound-tongue-image
- trust: high for narrow exploratory regression.
- did: CNN estimates child age from B-mode ultrasound tongue images; output age labels.
- evidence: UXTD typically developing children: validation MSE 2.03 with random rotation versus mean-age baseline 3.64. UPX validation MSE 4.87 versus baseline 5.35.
- conditions: Two UltraSuite child cohorts; validation-set regression only.
- limits: Small child-only, low-SNR data; no external validation, interface, runtime, deployment, or direct silent-speech task.
- changes_view: Tongue ultrasound contains age signal, but this is adjacent articulatory analysis, not SSI.

### 65. End-to-end Silent Speech Recognition with Acoustic Sensing (2020)
- id: end-to-end-silent-speech-recognition-with-acoustic-sensing
- trust: high; real mobile-compatible SSI contribution.
- did: Inaudible smartphone-like speaker/mic acoustics capture silent lip movement via reflected phase features; output text; 54 sentences.
- evidence: WER: 2.6% domain-dependent, 8.4% domain-independent average, 8.1% unseen-sentence. Leave-one-sentence-out over 54 sentences has worst Top-10 WER 18.2%; includes CTC comparison.
- conditions: Collected dataset with domain-dependent, domain-independent, and unseen-sentence splits.
- limits: Small corpus/vocabulary; unseen split remains inside 54-sentence design; latency, power, always-on robustness, field noise, broad vocabulary unresolved.
- changes_view: Commodity acoustic sensing can exceed memorization, but proof is narrow.

### 66. Speech Prediction in Silent Videos using Variational Autoencoders (2020)
- id: speech-prediction-in-silent-videos-using-variational-autoencoders
- trust: high; meaningful ambiguity modeling.
- did: VAE maps silent lip video to multiple plausible speech-audio outputs via latent z.
- evidence: GRID metrics: STOI 0.724, ESTOI 0.540, PESQ 1.932; trails Lip2Wav STOI by 0.007 but leads on ESTOI/PESQ. Varying z demonstrates diverse plausible waveforms.
- conditions: GRID benchmark, objective metrics, qualitative comparison, diversity sampling.
- limits: Griffin-Lim waveform recovery from mel spectrograms; no open-world, speaker-independent deployment, real-time, or in-the-wild test.
- changes_view: Treats video-to-speech as one-to-many; gains are quality-focused, not universal.

### 67. X-TaSNet: Robust and Accurate Time-Domain Speaker Extraction Network (2020)
- id: x-tasnet-robust-and-accurate-time-domain-speaker-extraction-network
- trust: high for speech extraction; out of SSI.
- did: GE2E embeddings + Conv-TasNet target-speaker extraction with distortion loss, alternating training, and absent-speaker handling; mixed speech + reference utterance.
- evidence: X-TaSNet: SDRi 14.7 dB, SI-SNRi 13.8 dB, NSR 4.3%, SpkER 4.6%. X-TaSNet-PIT: SI-SNRi 14.5 dB, NER 72.4%. Voicefilter: SDRi 7.4 dB, SI-SNRi 6.4 dB, NSR 9.2%.
- conditions: LibriSpeech clean two-speaker mixtures plus Voicefilter; objective metrics and subjective SpkER listening.
- limits: Needs clean reference speech; clean two-speaker/single-channel scope; absent detection below 80%; no SSI.
- changes_view: Strong extraction benchmark, only adjacent to SSI.

### 68. Listening to Sounds of Silence for Speech Denoising (2020)
- id: listening-to-sounds-of-silence-for-speech-denoising
- trust: high for denoising; not SSI.
- did: Uses detected natural silent intervals in mono speech audio as supervision for two-step denoising.
- evidence: Silent-interval detection: DEMAND precision 0.876, recall 0.866, F1 0.869, accuracy 0.918; AudioSet F1 0.807, accuracy 0.873. VoiceBank-DEMAND denoising: PESQ 3.16, STOI 0.98.
- conditions: Multi-dataset benchmarks, detector metrics, ablations, published comparisons, qualitative real-world tests.
- limits: Requires natural pauses and detector accuracy; real-world tests lack clean references; no articulatory sensing, silent communication, or SSI deployment.
- changes_view: Acoustic pause supervision helps denoising; it is not silent speech.

### 69. Discriminative Sounding Objects Localization via Self-supervised Audiovisual Matching (2020)
- id: discriminative-sounding-objects-localization-via-self-supervised-audiovisual-matching
- trust: high for AV localization; outside SSI.
- did: Learns single-source object representations, then class-aware audio-video matching to localize sounding versus silent objects; output maps and labels.
- evidence: Introduces CIoU and NSA. MUSIC-synthetic CIoU/AUC/NSA 32.3/23.5/98.5; MUSIC-duet 30.2/22.1/83.1; AudioSet-instrument-multi 48.7/29.7/56.8.
- conditions: Musical-instrument audiovisual datasets with synthetic/real cocktail-party clips and localization metrics.
- limits: Needs single/multi-source scenario partitioning and curated instrument boxes; no speech, SSI, real-time, or mobile test.
- changes_view: Silent-object filtering is AV perception, not silent-speech interface evidence.

### 70. Digital Voicing of Silent Speech (2020)
- id: digital-voicing-of-silent-speech
- trust: high; core facial EMG SSI reconstruction.
- did: Face/jaw/throat EMG to speech audio using target transfer between vocalized and silent EMG, CCA alignment, and predicted-audio refinement; open vocabulary has 9828 words.
- evidence: Closed-vocabulary human WER 3.6%, a 94% relative error reduction over strongest baseline. Open-vocabulary human WER 95.1% to 74.8%; automatic open-vocabulary WER 91.2% to 68.0%.
- conditions: Human WER, ASR WER, and ablations on data size/electrode subsets from authors' collection.
- limits: Speaker-dependent; needs substantial subject-specific data, facial EMG gear, and training. Open-vocabulary WER remains high.
- changes_view: Silent EMG can be voiced if silent/vocalized mismatch is modeled, but usability is not solved.

### 71. End-to-End Speaker-Dependent Voice Activity Detection (2020)
- id: end-to-end-speaker-dependent-voice-activity-detection
- trust: high for target-speaker VAD; not SSI.
- did: End-to-end model detects only target-speaker activity in microphone speech audio; output labels.
- evidence: LSTM SDVAD+binning+post reaches 94.62% ACC and 93.47% F-score. Segment J-VAD for LSTM SDVAD+binning is 73.66%, below LSTM VAD/SV baseline 76.68%, due to fragmentation.
- conditions: Frame ACC/F-score plus segment J-VAD; online negligible-latency claim.
- limits: Audio-only speaker-dependent task; fragmentation and border precision remain issues; no SSI deployment.
- changes_view: Good target filtering; frame metrics overstate temporal cleanliness.

### 72. A comparison of oscillatory characteristics in covert speech and speech perception (2020)
- id: a-comparison-of-oscillatory-characteristics-in-covert-speech-and-speech-perception
- trust: high for foundational EEG analysis.
- did: EEG comparison of covert speech and speech perception over a small fixed lexicon; output labels/oscillatory analyses.
- evidence: 8 participants; per-participant 10-fold SVM precision/recall/F1. Wilcoxon: perception shows stronger delta/theta (p<0.01, p<0.0001), covert speech stronger low-gamma (p<0.05); significant theta-gamma PAC at 200-500 ms.
- conditions: Frequency-band statistics, cross-task comparison, PAC analysis.
- limits: Small lexicon, participant variability, no SSI decoder/user study/deployment; one- and two-syllable items at same rate.
- changes_view: Covert speech is not just muted perception; evidence is neuroscience foundation, not interface.

### 73. Silent Speech Interfaces for Speech Restoration: A Review (2020)
- id: silent-speech-interfaces-for-speech-restoration-a-review
- trust: high as field survey.
- did: Reviews speech-restoration SSI via non-acoustic biosignals and articulator sensing across brain, muscle, face, lip, oral cavity, throat, and tongue.
- evidence: Latency targets: ~50 ms ideal, up to 100 ms possibly acceptable, ~200 ms disruptive. Covers brain activity sensors, muscle activity sensors, and articulator tracking.
- conditions: Comparative review of modalities, restoration scenarios, latency, patient-data scarcity, and dataset constraints.
- limits: No unified benchmark or new system; inherits uneven prior evidence; does not solve deployment obstacles.
- changes_view: Best use is bottleneck map: latency, scarce patient data, modality invasiveness, and practicality dominate.

### 74. An Overview of Deep-Learning-Based Audio-Visual Speech Enhancement and Separation (2020)
- id: an-overview-of-deep-learning-based-audio-visual-speech-enhancement-and-separation
- trust: high as adjacent AV survey.
- did: Organizes microphone+camera speech enhancement/separation by features, fusion, targets, datasets, methods, and evaluation; output speech audio.
- evidence: Common metrics: PESQ, STOI/ESTOI, SDR/SI-SDR, WER. Survey states visual information helps especially at low SNR and source-permutation cases.
- conditions: Literature review including silent-video and non-speech AV source-separation neighbors.
- limits: No new benchmark, unified re-evaluation, empirical ranking, or deployable system; standardized AV evaluation is missing.
- changes_view: Good design/evaluation map, but not primary SSI evidence.

### 75. CITISEN: A Deep Learning-Based Speech Signal-Processing Mobile Application (2020)
- id: citisen-a-deep-learning-based-speech-signal-processing-mobile-application
- trust: high for mobile speech processing; not SSI.
- did: Mobile/cloud audible-speech app for enhancement, personalized model adaptation, and background-noise conversion; microphone audio to enhanced/converted speech.
- evidence: MA(N), MA(S), MA(N+S): STOI +5.06%, +2.94%, +5.84%; PESQ +12.48%, +3.32%, +11.24% over FCN baseline. BNC accuracy above 90%; CCR drops when enhanced speech replaces clean speech.
- conditions: Objective metrics, listening tests, acoustic-scene classification, ASR-based evaluation.
- limits: Cloud-backed, audible-speech, task-specific app; not low-resource on-device SSI.
- changes_view: Shows integration/package value, not silent-speech sensing progress.

### 76. Foley Music: Learning to Generate Music from Videos (2020)
- id: foley-music-learning-to-generate-music-from-videos
- trust: high for multimedia generation; outside SSI.
- did: Camera video of instrument performance to body keypoints to variable-length MIDI to synthesized audio.
- evidence: Human preference wins every instrument category, 56%-72%. Real-vs-fake success 38% versus 8%-12% baselines. NDB 20 versus 25-33, lower is more diverse.
- conditions: Human preference, real-vs-fake listening, NDB diversity, NLL ablations on tested instruments/videos.
- limits: Instrument music, not speech; waveform realism depends on external synthesizer; no SSI/language/interaction path.
- changes_view: Strong motion-to-music method; must be labeled as SSI distractor.

### 77. Learning Frame Level Attention for Environmental Sound Classification (2020)
- id: learning-frame-level-attention-for-environmental-sound-classification
- trust: high for compact audio classification.
- did: ACRNN applies frame-level attention to environmental spectrograms; output sound labels.
- evidence: Best accuracy: 93.7% ESC-10, 86.1% ESC-50. Size: 3.81M parameters, 9.18M FLOPs versus PiczakCNN 31.53M and 63.27M. Best attention placement is recurrent output layer l10.
- conditions: 5-fold ESC-10/ESC-50 benchmarks with attention placement/scaling ablations.
- limits: Environmental clips only; no SSI/wearable/real-time/speech task; noise robustness not quantified.
- changes_view: Efficient salient-frame attention is adjacent method context, not SSI.

### 78. Ultra2Speech -- A Deep Learning Framework for Formant Frequency Estimation and Tracking from Ultrasound Tongue Images (2020)
- id: ultra2speech-a-deep-learning-framework-for-formant-frequency-estimation-and-tracking-from-ultrasound-tongue-images
- trust: high; core ultrasound articulatory-to-acoustic mapping.
- did: U2F maps ultrasound tongue/oral-cavity image sequences to f1/f2 formant trajectories, then Klatt-synthesized vowel audio; hybrid 2D spatial + 1D temporal convs with channel shuffling.
- evidence: Best U2F mean R2 99.96 on joint f1-f2 prediction, versus Conv-BiLSTM 90.01; beats recurrent and standard 3D CNN baselines.
- conditions: Collected ultrasound train/dev/test with MAE, mean R2, baselines, ablations.
- limits: Formants/vowel trajectories only; no full open-vocabulary restoration, cross-speaker clinical deployment, or real-time device.
- changes_view: Strong constrained ultrasound-to-acoustics evidence, not full SSI speech restoration.

### 79. Application of Just-Noticeable Difference in Quality as Environment Suitability Test for Crowdsourcing Speech Quality Assessment Task (2020)
- id: application-of-just-noticeable-difference-in-quality-as-environment-suitability-test-for-crowdsourcing-speech-quality-assessment-task
- trust: high for crowdsourcing QC; not SSI.
- did: Modified JNDQ screens playback device/background-noise suitability before crowdsourced MOS speech-quality tests; output suitability labels.
- evidence: JND 6 dB with >=3/4 correct gives highest lab-MOS correlation. Lenient JND 10 dB with >=1/4 correct fails ~15% answers versus 61% strict. Uses PCC, SRCC, RMSE.
- conditions: Lab plus crowdsourcing evaluation over tested JND levels, degradations, and platform.
- limits: Screens only one time; frequent insertion lengthens sessions, infrequent screening misses environment changes; evaluation control only.
- changes_view: Useful speech-quality study gate, not silent-speech sensing/interface evidence.
