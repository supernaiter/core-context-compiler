# SSI Review Compression Batch 00-26

### 0. Cross-Modal Masking for Robust Silent Speech Synthesis Using sEMG and Lipreading (2026)
- id: cross-modal-masking-for-robust-silent-speech-synthesis-using-semg-and-lipreading
- trust: high; venue: arXiv.
- did: Masked multimodal SSI maps 8-channel face/neck sEMG plus RGB lip video to mel-spectrogram speech and phonetic labels.
- evidence: Spanish ReSSInt audible/silent data with laryngeal and laryngectomized speakers; text-independent splits; monomodal/multimodal baselines; masking and bitrate/video-degradation ablations. Metrics: Phone Accuracy, Whisper v3 WER, SSIM; WER improved up to 14 absolute points.
- conditions: Controlled studio, Spanish sentence data, limited phoneme/vocabulary scope.
- limits: Laryngectomized adaptation remains weak because articulation varies and paired audible speech is missing; no real-time, mobile, spontaneous, other-language, or large-vocabulary test.
- changes_view: Robust fusion helps, but clinical value depends on speaker adaptation, not just multimodal masking.

### 1. A 1000-hour EEG-EMG-audio dataset of Japanese speech production (2026)
- id: a-1000-hour-eeg-emg-audio-dataset-of-japanese-speech-production
- trust: high; venue: arXiv.
- did: Releases JapanEEG, 1020 h of simultaneous scalp EEG, facial EMG, and audio for open-vocabulary overt Japanese speech.
- evidence: 3 healthy native Japanese male participants; g.Pangolin 128 ch, g.SCARABEO 62 ch, eego sports 63 ch; 3 bipolar facial EMG channels around upper lip, lower lip, eyes; lavalier audio. OpenNeuro/BIDS, CC0, about 955 GB. PSD/ERP validation shows expected 1/f, alpha attenuation, and speech-locked responses.
- conditions: Dataset resource, not a decoder; useful for cross-device, longitudinal, artifact, and adaptation work.
- limits: n=3 and all male Japanese; no downstream decoding benchmark, wearable/mobile test, or deployment evidence.
- changes_view: Scale/data quality move the field; population breadth and actual decoding value remain open.

### 2. Zero-Shot Imagined Speech Decoding via Imagined-to-Listened MEG Mapping (2026)
- id: zero-shot-imagined-speech-decoding-via-imagined-to-listened-meg-mapping
- trust: high; venue: arXiv.
- did: Maps imagined MEG to listened MEG, then uses a contrastive listened-speech decoder for zero-shot imagined word decoding.
- evidence: 157-channel MEG from 17 trained musicians listening/imagining four rhythmic stimuli; vocabulary 76 poem content words. Six mapping models are above-null and transfer leave-one-subject-out. Metrics: per-channel Pearson correlation and rank decoding; listened decoder Recall@1 up to about 9.1% with BERT + Wav2Vec2.
- conditions: Rhythmic stimuli/trained users reduce timing mismatch; imagined labels not used for decoder training.
- limits: Decoding far below listened ceiling; small correlations add noise; MEG is expensive/non-portable; small vocabulary, non-natural task, no real time.
- changes_view: Borrowing listened-speech structure is promising, but hardware and vocabulary still dominate practicality.

### 3. NasoVoce: A Nose-Mounted Low-Audibility Speech Interface for Always-Available Speech Interaction (2026)
- id: nasovoce
- trust: high; venue: CHI '26 / arXiv.
- did: Smart-glasses nose-pad interface captures whispered/low-volume speech using air plus skin conduction for enhancement and ASR.
- evidence: Syntiant SPH0141LM4H-1 MEMS microphone plus V2S200D vibration sensor, synchronized PDM. Whisper Large-v2 ASR on 1,000 held-out items with synthetic noise -10 to 10 dB; metrics WER, CER, PESQ, STOI; MUSHRA with 50 evaluators; qualitative recordings in four real environments.
- conditions: Discreet low-audibility speech, not fully silent SSI; assumes hand-covering mouth for privacy.
- limits: Fusion not fully streaming; vibration weak for whispers; extreme noise can favor vibration-only; synthetic-noise evidence dominates; no unseen-word, phone integration, SNR gating, or nasal-patency calibration.
- changes_view: Low-audibility open-vocabulary AI interaction may be nearer-term than fully silent speech.

### 4. SonicVisionLM: Playing Sound with Vision Language Models (2024)
- id: sonicvisionlm-playing-sound-with-vision-language-models
- trust: high; venue: arXiv / imported corpus page.
- did: Decomposes video-to-audio into VLM event text, timestamp localization, and time-conditioned text-to-audio generation.
- evidence: CondPromptBank trains timing adapter. Conditional metrics: CLAP-top 36.8%/42.8%, Onset Accuracy 27.6%, Onset AP 78.1%, Time Accuracy 43.8%, IoU 39.7%; unconditional IoU 39.5 Greatest Hits, 42.0 CountixAV. 300-person subjective scores: quality 75, relevance 69, time-sync 87; FID under 25, MKL about 2.3.
- conditions: Video-only Foley/post-production, no speech or body sensor.
- limits: Timestamp/visual understanding still weak; offline/GPU-heavy, not real time; noisy audio ground truth complicates metrics; no SSI, communication, or mobile evidence.
- changes_view: Valuable for editable audiovisual timing, but not a silent speech result.

### 5. IR-UWB Radar-Based Contactless Silent Speech Recognition of Vowels, Consonants, Words, and Phrases (2023)
- id: ir-uwb-radar-based-contactless-silent-speech-recognition-of-vowels-consonants-words-and-phrases
- trust: high; venue: arXiv / imported corpus page.
- did: Contactless IR-UWB radar SSR with FERASEC feature extraction for phonemes, words, and phrases.
- evidence: 20 participants; 8 vowels, 11 consonants, 25 words, 12 phrases, 20 reps each. Upper patch antennas face lips; lower sinuous antennas below chin. FERASEC combines raw/clutter-reduced frames, envelope, downsampling, DC removal, derivatives. Leave-one-out DNN-HMM upper radar: 86.47% vowels, 81.59% consonants, 88.95% words, 96.88% phrases; raw/clutter-only phonemes below 50%.
- conditions: Closed-set prompted lab articulations; lip-alignment/range aiding algorithm.
- limits: Teeth can block tongue signal; placement sensitive; no open vocabulary, conversational speech, broad speaker diversity, or daily-use hardware test.
- changes_view: Contactless phoneme SSI is feasible, but sensor geometry is the central constraint.

### 6. Ultrasensitive Textile Strain Sensors Redefine Wearable Silent Speech Interfaces with High Machine Learning Efficiency (2023)
- id: ultrasensitive-textile-strain-sensors-redefine-wearable-silent-speech-interfaces-with-high-machine-learning-efficiency
- trust: high; venue: arXiv / imported corpus page.
- did: Graphene textile throat-strain choker plus lightweight residual 1D CNN for silent word classification.
- evidence: Ordered microcracks improve gauge factor by 420%; gauge factor 317 within <=5% strain; stable over 10,000 cycles; 500 Hz sampling. 3 participants; datasets: 20 words, 10 confusable pairs, 5 long words, 100 samples/class, 80/20 split. Accuracy 95.25%, 93%, 96%; few-shot transfer to new user/10 unseen words 90% with 30 samples/class; claimed 90% compute reduction.
- conditions: Throat vibration strain, isolated closed-vocabulary words, speaker-dependent wearable.
- limits: n=3, max 20 words, no continuous speech/sentences, broad demographics, or real deployment.
- changes_view: Better sensors can shrink models, but vocabulary/participant scale still limits SSI claims.

### 7. Distributed pressure matching strategy using diffusion adaptation (2023)
- id: distributed-pressure-matching-strategy-using-diffusion-adaptation
- trust: high; venue: arXiv / imported corpus page.
- did: Distributed pressure-matching sound-zone control via diffusion LMS; nodes use local costs and neighbor exchange, no root node.
- evidence: 100 Monte Carlo simulations with synthetic RIR/noise, room 8.088 m x 7.346 m x 2.865 m, T60 about 200 ms; 9 loudspeakers, 16 microphones, 2 topologies, 100-4000 Hz bins. Metrics NMSE and Acoustic Contrast: control about -16 dB/16 dB after 5000 iterations; validation about -14 dB/14 dB; comparable to centralized PM.
- conditions: Personal sound zones, acoustic input/output only.
- limits: Simulation-only; no real-room measurement, synchronization/calibration failure, ATF drift, user study, speech task, or SSI modality.
- changes_view: Adjacent distributed-acoustic evidence; not silent speech.

### 8. Advancing Test-Time Adaptation for Acoustic Foundation Models in Open-World Shifts (2023)
- id: advancing-test-time-adaptation-for-acoustic-foundation-models-in-open-world-shifts
- trust: high; venue: arXiv / imported corpus page.
- did: Confidence-Enhanced Adaptation keeps high-entropy non-silent frames with confidence weights and adds temporal consistency for ASR TTA.
- evidence: WER tests on LibriSpeech corruptions, environmental sounds, L2-Arctic accents, DSing, Hansen; Wav2vec2 Base/Large, Conformer, Transducer. Results: 21.5% average relative WER improvement on Gaussian LS-C; 41.7% at 5 dB SNR Air Conditioner. Runtime about 1.07 s adaptation plus 1.20 s recognition on A5000 GPU.
- conditions: Offline utterance-level microphone ASR under acoustic shifts.
- limits: Decoder/text-domain adaptation absent; no multi-speaker/cross-task study; not streaming; latency blocks immediate real-time use; no silent speech.
- changes_view: High-entropy frames may carry useful semantics; filtering them can hurt adaptation.

### 9. Sound Source Localization is All about Cross-Modal Alignment (2023)
- id: sound-source-localization-is-all-about-cross-modal-alignment
- trust: high; venue: arXiv / imported corpus page.
- did: Adds semantic audio-visual alignment to sound source localization using multi-positive contrastive learning and retrieval evaluation.
- evidence: Positives from augmentation and conceptually similar samples mined by pretrained encoders. Datasets: VGGSound, SoundNet-Flickr, AVSBench S4, extended variants with boxes/segments. Metrics: corrected IoU, AUC, R@1/R@5/R@10, false-positive AP and max F1; includes open-set category and false-positive tests.
- conditions: Camera + microphone; outputs localization/retrieval labels, not text/audio speech.
- limits: Curated benchmarks and encoder-mined positives; k-nearest choices matter; no real-time, user-centered, spontaneous speech, or SSI evaluation.
- changes_view: Spatial localization metrics alone can fake grounding; semantic alignment needs separate tests.

### 10. Let There Be Sound: Reconstructing High Quality Speech from Silent Videos (2023)
- id: let-there-be-sound-reconstructing-high-quality-speech-from-silent-videos
- trust: high; venue: arXiv / imported corpus page.
- did: Lip-to-speech pipeline uses SSL linguistic units, pitch/energy variance predictors, and flow post-net to reduce one-to-many ambiguity.
- evidence: Best linguistic target: HuBERT-large layer 12 with 200 K-means clusters. Evaluated on GRID and Lip2Wav Chemistry/Chess with MOS, ASR WER/CER, pitch/energy stats, ablations. GRID: MOS gap vs vocoded speech 0.28 naturalness and 0.13 intelligibility; WER 17.07%, CER 9.17%.
- conditions: Silent lip video to speech audio; camera input; multi-stage benchmark system with neural vocoder.
- limits: Not end-to-end; no latency, streaming, on-device, open-world, or cross-domain deployment evidence; Lip2Wav labels required manual transcription.
- changes_view: Explicit linguistic/prosodic factors beat direct mel regression for lip-to-speech.

### 11. An Initial Exploration: Learning to Generate Realistic Audio for Silent Video (2023)
- id: an-initial-exploration-learning-to-generate-realistic-audio-for-silent-video
- trust: medium-high; venue: arXiv / imported corpus page.
- did: Compares deep-fusion CNN, dilated Wavenet CNN, and transformer models for non-speech audio from silent video.
- evidence: Tiny type-specific car chase, clapping, nature videos; validation cross-entropy plus waveform/perceptual checks. Table I: Transformer -0.22000, -0.00797, -0.00862; Wavenet -0.03785, 0.00029, 0.01669; deep-fusion 1.65133e-05, -1.36272e-07, 1.04321e-05. Transformer best for low/mid frequencies; Wavenet noise-like, deep-fusion discontinuous.
- conditions: Camera-only Foley-like generation; not speech.
- limits: Single-video overfitting, tiny curated data, weak high-frequency fidelity, qualitative-heavy evaluation, no diverse benchmark or deployment.
- changes_view: Useful as preliminary negative/architecture evidence, not SSI.

### 12. Audio Knowledge Empowered Visual Speech Recognition (2023)
- id: akvsr-audio-knowledge-empowered-visual-speech-recognition-by-compressing-audio-knowledge-of-a-pretrained-model
- trust: high; venue: arXiv / imported corpus page.
- did: AKVSR stores pretrained audio linguistic knowledge in compact discrete memory and injects it into video-only VSR via ABM cross-attention.
- evidence: Vector-quantized HuBERT/CPC/wav2vec2 memory removes speaker/noise factors. LRS3 WER: baseline 46.1%, BASE 41.6%, LARGE 29.1% (30h), 27.6% (433h), 23.6% augmented. LRS2 LARGE: 32.2% to 28.7% at 28h; 25.5% to 24.1% at 223h. Ablations cover model, memory, ABM, data.
- conditions: LRS2/LRS3 sentence VSR; audio not needed at inference.
- limits: Offline memory construction before training; no live camera, latency, streaming, external environment, or real deployment test.
- changes_view: Audio transfer works best when reduced to linguistic memory, not raw feature concatenation.

### 13. Knowledge Distilled Ensemble Model for sEMG-based Silent Speech Interface (2023)
- id: knowledge-distilled-ensemble-model-for-semg-based-silent-speech-interface
- trust: high; venue: arXiv / imported corpus page.
- did: Distills a 6-model ResNet ensemble into KDE-SSI for 3-channel facial sEMG NATO-alphabet spelling.
- evidence: 3900 samples; 5 males aged 22-24; 26 NATO words x30; 150/class. BITalino MuscleBIT adhesive Ag/AgCl on levator anguli oris, depressor anguli oris, zygomaticus major. 4:1:1 split. ResNet1D 81.2%; VE-ResNet 86.0%; KDE-SSI 85.9%. Size/latency: 21.1 MB/0.12 ms vs 147.9 MB/2.50 ms.
- conditions: Speaker-dependent, quiet seated spelling interface.
- limits: 5 young males only; adhesive placement; no cross-subject/session, unseen-word, demographic, or continuous-speech result.
- changes_view: Distillation solves model size/latency, not the speaker-independence/electrode bottleneck.

### 14. Automatically measuring speech fluency in people with aphasia: first achievements using read-speech data (2023)
- id: automatically-measuring-speech-fluency-in-people-with-aphasia-first-achievements-using-read-speech-data
- trust: high; venue: arXiv / imported corpus page.
- did: Regresses aphasia fluency ratings from noisy remote read-speech using engineered acoustic predictors.
- evidence: 95 sentences from 34 participants: 29 aphasia, 5 controls; French BDAE long sentences over Zoom with built-in PC mics, 16 kHz. Three expert SLPs give 5-point ratings. Forward-backward divergence segmentation extracts pseudo-syllables/silent breaks; predictors: pseudo-syllable rate, speech ratio, silent-break rate, pseudo-syllable length SD. Leave-one-speaker-out MLR/SVR/RF: RMSE as low as 0.47; Pearson 0.87 sentence-level, 0.93-0.96 participant-level.
- conditions: Acoustic read speech; output clinical labels.
- limits: Fixed French read sentences, small data, 3 raters, weak repetition modeling initially; no spontaneous speech, multilingual, SSI, or non-acoustic sensing.
- changes_view: Strong clinical speech analytics, not silent speech decoding.

### 15. Exploring how a Generative AI interprets music (2023)
- id: exploring-how-a-generative-ai-interprets-music
- trust: high; venue: arXiv / imported corpus page.
- did: Interprets Google MusicVAE latent space for symbolic monophonic music.
- evidence: MusicVAE has 512 latent dimensions; trained on about 1.5M MIDI files filtered for 4/4, yielding 3.8M 2-bar and 11.4M 16-bar monophonic sequences. In 50,000 melodies, about 37 "music neurons" have small SD/varying means; about 475 "noise neurons" have sigma about 1 and mu about 0. phik correlations with music21/jSymbolic link first canonical neuron to pitch, second to rhythm; melody appears in longer sequences/lower ranks.
- conditions: Symbolic MIDI analysis; output latent-feature interpretation.
- limits: Correlation-only, non-causal, monophonic, MusicVAE-specific; no downstream task, speech, articulation, wearable, deployment, or SSI value.
- changes_view: Exclude except as distant representation-compression analogy.

### 16. Audio-visual video-to-speech synthesis with synthesized input audio (2023)
- id: audio-visual-video-to-speech-synthesis-with-synthesized-input-audio
- trust: high; venue: arXiv / imported corpus page.
- did: Two-stage V2A then AV2A uses silent video plus synthesized audio, with modality dropout, in waveform and mel domains.
- evidence: AV2A fuses audio/video plus speaker embedding. GRID 4-speaker seen with pretraining/dropout/GT audio: PESQ 1.95, STOI 0.698, ESTOI 0.532, WER 3.67%. GRID 33-speaker seen: 2.10, 0.723, 0.553, WER 2.65%. TCD-TIMIT 3 lipspeakers: 1.44, 0.566, 0.411. LRW best raw waveform WER 24.96%.
- conditions: Benchmark V2S; benefit depends on first-stage audio quality.
- limits: Gains inconsistent; no noisy/in-the-wild, real-time, latency, or deployment test; TCD-TIMIT WER unavailable.
- changes_view: Synthesized audio can be a useful intermediate, but deployment is unproven.

### 17. Audio-aware Query-enhanced Transformer for Audio-Visual Segmentation (2023)
- id: audio-aware-query-enhanced-transformer-for-audio-visual-segmentation
- trust: high; venue: arXiv / imported corpus page.
- did: AuTR uses audio-aware decoder queries and dynamic convolution for sounding-object segmentation.
- evidence: AVSBench S4/MS3, S4-to-MS3 fine-tuning, open-set held-out categories, ablations. PVT-v2: 80.4 MJ/.891 MF on S4, 56.2 MJ/.672 MF on MS3; S4 pretrain then MS3 gives 60.95 MJ/.725 MF. Unseen categories: 66.22 MJ/.777 MF vs TPAVI 55.86 MJ/.719; AuTR still drops from 77.56 to 66.22 MJ on PVT-v2.
- conditions: Audio+video segmentation labels for sounding objects.
- limits: AVSBench-style masks only; no speech, language output, latency, product deployment, user study, or SSI.
- changes_view: Good audio-conditioned query design; outside silent speech.

### 18. RobustL2S: Speaker-Specific Lip-to-Speech Synthesis exploiting Self-Supervised Representations (2023)
- id: robustl2s-speaker-specific-lip-to-speech-synthesis-exploiting-self-supervised-representations
- trust: high; venue: arXiv / imported corpus page.
- did: Maps AV-HuBERT visual SSL features to speech HuBERT SSL representations, then vocodes waveform.
- evidence: Modular lip encoder, non-autoregressive seq2seq content mapper, vocoder; avoids direct mel regression. Evaluated on Lip2Wav, GRID-4S, TCD-TIMIT-3S with STOI, ESTOI, WER, MOS. TCD-TIMIT-3S: STOI 0.596, ESTOI 0.452, WER 29.03. Lip2Wav speaker-dependent Deep Learning speaker: STOI/ESTOI up to 0.627/0.419.
- conditions: Silent lip video to speech audio; strongest in speaker-specific/seen-speaker benchmarks.
- limits: Prosody limited by speech SSL embeddings; no speaker-independent, real-time, mobile, latency, or broad unseen-word evidence; Lip2Wav transcripts needed Whisper for finetuning.
- changes_view: SSL content disentanglement helps, but prosody and speaker generalization remain.

### 19. Diff-Foley: Synchronized Video-to-Audio Synthesis with Latent Diffusion Models (2023)
- id: diff-foley-synchronized-video-to-audio-synthesis-with-latent-diffusion-models
- trust: high; venue: arXiv / imported corpus page.
- did: Foley V2A using CAVP aligned audio-visual pretraining plus latent diffusion and double guidance.
- evidence: VGGSound quantitative tests, guidance/pretraining ablations, sampler-speed study, EPIC-Kitchens fine-tuning. With double guidance: IS 62.37, FID 9.87, KL 6.43, Align Acc 94.05, 0.38 s/sample with DPM-Solver 25 steps. Stage 1 scaled to VGGSound+AudioSet-V2A gives Align Acc 94.78 under DDIM. EPIC-Kitchens evidence is mostly qualitative object sounds.
- conditions: Offline video-to-Foley audio, no speech/body sensing.
- limits: Diffusion heavier/slower than GANs; super-large scale untested due compute; no SSI/human communication evaluation.
- changes_view: Alignment pretraining/guidance are transferable ideas; the result itself is outside SSI.

### 20. High-Quality Automatic Voice Over with Accurate Alignment: Supervision through Self-Supervised Discrete Speech Units (2023)
- id: high-quality-automatic-voice-over-with-accurate-alignment-supervision-through-self-supervised-discrete-speech-units
- trust: high; venue: arXiv / imported corpus page.
- did: Automatic voice-over predicts HuBERT+k-means speech units from text+lip frames, then uses Unit HiFi-GAN for synthesis.
- evidence: Chem single-speaker English dataset from YouTube transcripts: 6088 train, 200 validation, 200 test. Metrics: LSE-C 6.81, LSE-D 7.56, FD 3.23, WER 24.7%, MOS 3.98 +/- 0.08, BWS lip-sync best 84.0% / worst 1.3%. Uses objective metrics and listening tests.
- conditions: Requires text script plus video; video-conditioned TTS/voice-over, not silent recognition.
- limits: Single speaker only; paired video/text/audio and pretrained tokenizer/vocoder required; no multi-speaker, unseen-word, walking/moving, in-the-wild, or deployment test.
- changes_view: Discrete unit supervision improves alignment, but the task is scripted voice-over.

### 21. Large-scale unsupervised audio pre-training for video-to-speech synthesis (2023)
- id: large-scale-unsupervised-audio-pre-training-for-video-to-speech-synthesis
- trust: high; venue: arXiv / imported corpus page.
- did: Pretrains audio decoders on over 3,500 h of 24 kHz audio, then initializes video-to-speech decoders.
- evidence: Separate audio/video BN stats enable transfer. GRID/TCD-TIMIT/LRW metrics: PESQ 1.26-2.07, STOI 0.49-0.72, ESTOI 0.20-0.53, WER 2.66%-42.38%. GRID unseen V2A-MelSpec-S-SP + fine-tuning: 1.43, 0.598, 0.335, WER 17.90. LRW scratch: 1.48, 0.649, 0.484, WER 14.96.
- conditions: Mouth-region video input; audio-only corpora for pretraining.
- limits: WER gains not uniform; audio quality modest; no MOS, latency, live interface, or capture-robustness test.
- changes_view: Audio pretraining helps quality/data efficiency, not reliable recognition accuracy.

### 22. LipVoicer: Generating Speech from Silent Videos Guided by Lip Reading (2023)
- id: lipvoicer-generating-speech-from-silent-videos-guided-by-lip-reading
- trust: high; venue: arXiv / imported corpus page.
- did: Diffusion lip-to-speech uses text predicted by lip-reader plus ASR classifier guidance at inference.
- evidence: LRS2/LRS3 in-the-wild data with hundreds of speakers/open vocabulary. Metrics: human MOS for intelligibility/naturalness/quality/sync, WER, DNSMOS, STOI-Net, SyncNet LSE-C/LSE-D. LRS3 ablation: without ASR guidance WER worsens from 21.4% to 86.2%. Human intelligibility MOS near ground truth: 3.44-3.53 vs 4.33-4.38. Lip-reader WER: 14.6% LRS2, 19.1% LRS3.
- conditions: Silent lip video; inferred text drives heavy offline diffusion.
- limits: Depends on lip-reader/ASR quality; hundreds of inference steps; no real-time/mobile claim; weaker lip-reader degrades quality; text-injection misuse risk.
- changes_view: Text guidance is decisive, but imports recognition errors and security risk.

### 23. Intelligible Lip-to-Speech Synthesis with Speech Units (2023)
- id: intelligible-lip-to-speech-synthesis-with-speech-units
- trust: high; venue: arXiv / imported corpus page.
- did: Lip-to-speech predicts quantized SSL speech units as pseudo-text targets and vocodes with mel plus units.
- evidence: No paired text labels needed. LRS2/LRS3 metrics: STOI, ESTOI, PESQ, WER, MOS. LRS3: 0.578, 0.393, 1.31, WER 29.8% vs Multi-Task 65.8%. LRS2: 0.585, 0.412, 1.34, WER 35.7%. MOS: 15 raters, 20 LRS3 samples. AV-HuBERT can use LRS3/VoxCeleb2.
- conditions: Camera lip video to speech audio; sentence-level benchmarks.
- limits: Speech far from natural; vocoder stack complex; no cross-dataset, latency, on-device, occlusion, camera, lighting, mobility, or live deployment test.
- changes_view: Speech units are strong content supervision when transcripts are absent.

### 24. Adaptation of Tongue Ultrasound-Based Silent Speech Interfaces Using Spatial Transformer Networks (2023)
- id: adaptation-of-tongue-ultrasound-based-silent-speech-interfaces-using-spatial-transformer-networks
- trust: high; venue: the Proceedings of Interspeech 2023.
- did: Adds STN front-end to ultrasound-to-speech SSI so adaptation updates alignment and optionally output layer instead of retraining all weights.
- evidence: Articulate Instruments Micro ultrasound with probe-fixing headset; Hungarian tongue ultrasound to spectrogram/speech regression. 4 speakers with 209 read sentences each plus 4 remounted sessions from speaker 048. MSE evaluation. 2D: STN-only closes 75-76% of adaptation gap; STN+out recovers 88% cross-speaker and 92% cross-session gap relative to full adaptation. 3D Table 3: 87% average for STN+out.
- conditions: Controlled supervised adaptation; remounting/session robustness.
- limits: Fixes mainly affine image misalignment/output-layer shift; 4 speakers, read Hungarian, MSE not intelligibility/user study; supervised adaptation still needed.
- changes_view: A large part of ultrasound retuning is image alignment.

### 25. Zero-shot personalized lip-to-speech synthesis with face image based voice control (2023)
- id: zero-shot-personalized-lip-to-speech-synthesis-with-face-image-based-voice-control
- trust: high; venue: arXiv / imported corpus page.
- did: Personalizes Lip2Speech without enrollment speech by aligning face-image speaker embeddings to speech identity embeddings; VAE disentangles content/identity.
- evidence: GRID 33 speakers; train 20 (10 female, 10 male), test 13 unseen. Input lip video plus face image; output speech audio. Face encoder uses cosine, gender contrastive, cross-entropy losses; embedding plus latent content drives decoding. Metrics: STOI, ESTOI, PESQ, EER, MOS-SN, MOS-FVM. MTurk: 20 listeners, 20 sentences. Face embeddings give comparable intelligibility/quality to speech embeddings; reference-speech embeddings lower EER; Proposed-VAE sometimes wrong gender.
- conditions: GRID constrained 6-word utterances, zero-shot identity control.
- limits: Below ground truth/seen-speaker upper bound; no open vocabulary, in-the-wild video, pose/lighting, mobile, or real-time result.
- changes_view: Face-to-voice control is novel, but identity fidelity and scale remain unresolved.

### 26. Improving the Gap in Visual Speech Recognition Between Normal and Silent Speech Based on Metric Learning (2023)
- id: improving-the-gap-in-visual-speech-recognition-between-normal-and-silent-speech-based-on-metric-learning
- trust: high; venue: arXiv / imported corpus page.
- did: Aligns normal and silent VSR viseme distributions using KL-divergence metric-learning losses.
- evidence: Lip-focused grayscale video, Dlib face alignment/cropping; text output. VER/WER on AV Digits normal/silent plus OuluVS2 normal augmentation. AV Digits: 39 speakers, 10 fixed phrases; 1560 OuluVS2 normal utterances; test 550 utterances from 11 speakers. Best silent result 6.66% VER, 9.97% WER with LNCE + LSCE + LWKL + LNKL + LSKL; can match baseline using twice the silent data.
- conditions: Closed-vocabulary phrase recognition with visual and language models plus text-phoneme-viseme mapping.
- limits: 10 phrases; controlled datasets; no open vocabulary, continuous speech, in-the-wild, real-time mobile, or robust deployment evaluation.
- changes_view: Key value is low-data normal-to-silent transfer via alignment.
