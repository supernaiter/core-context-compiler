# SSI all compressed reviews for one-context reading

Source: https://nao-ki-mura.com/exports/ssi-review.json
Source updated: 2026-06-09T07:31:19Z

Total papers: 105




<!-- reports/ssi_all_context_framework/compressed/batch_00_26.md -->

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


<!-- reports/ssi_all_context_framework/compressed/batch_27_53.md -->

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


<!-- reports/ssi_all_context_framework/compressed/batch_54_79.md -->

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


<!-- reports/ssi_all_context_framework/compressed/batch_80_104.md -->

### 80. Vocoder-Based Speech Synthesis from Silent Videos (2020)
- id: vocoder-based-speech-synthesis-from-silent-videos
- trust: high; venue=arXiv / imported corpus page.
- did: Frontal face/mouth video -> speech audio; predicts WORLD SP/F0/AP/V-UV with 3-D conv, GRU, separate decoders, auxiliary VSR/CTC, STRAIGHT synthesis.
- evidence: GRID 34 speakers x 1000 six-word sentences. Speaker-dependent mouth+VSR: PESQ 1.90, ESTOI 0.455, WER 15.1%; speaker-independent: PESQ 1.23, ESTOI 0.227, WER 51.6%.
- conditions: PESQ/ESTOI/WER on speaker-dependent and independent GRID splits.
- limits: Closed grammar, frontal video, no noise/open/in-the-wild test; unseen speakers fail sharply.
- changes_view: Strong full-vocoder lip-to-speech baseline; controlled claim only.

### 81. Continuous Silent Speech Recognition using EEG (2020)
- id: continuous-silent-speech-recognition-using-eeg
- trust: high; venue=arXiv / imported corpus page.
- did: 31-channel wet scalp EEG during silent sentence reading -> English text; 155 handcrafted features -> 20 KPCA dims; CTC ASR with 2 GRUs, TCN, character softmax, 4-gram LM.
- evidence: 4 male subjects, 30 USC-TIMIT sentences, 1000 Hz EEG. WER about 74.86%-84.22%; 72-sentence WER 83.34%; cross-subject WER 92.55%.
- conditions: Varying test sizes, random 80/20 split, cross-subject test.
- limits: Tiny data, high WER, no real time, no wearable/cross-device/mobile condition.
- changes_view: Important because it makes continuous EEG-SSR failure rates concrete.

### 82. Brain2Char: A Deep Architecture for Decoding Text from Brain Recordings (2019)
- id: brain2char-a-deep-architecture-for-decoding-text-from-brain-recordings
- trust: medium-high; venue=arXiv / imported corpus page.
- did: Invasive ECoG -> character text; 3D inception, BiLSTM, dilated CNN, CTC, LM beam search, regularizers.
- evidence: 4 participants; 16x16/16x8 ECoG grids on VSMC/IFG/STG. WER 10.6%, 8.5%, 7.0% on 1200-1900 word vocabularies; silent/mimed WER 40%/67% on 20 sentences.
- conditions: Subject/session-specific ECoG; small silent trials.
- limits: Invasive implant, calibration, no cross-subject transfer, limited vocabulary, silent speech worse.
- changes_view: Sentence-level brain text decoding real; clinical deployment remains constrained.

### 83. Demucs: Deep Extractor for Music Sources with extra unlabeled data remixed (2019)
- id: demucs-deep-extractor-for-music-sources-with-extra-unlabeled-data-remixed
- trust: medium; venue=arXiv / imported corpus page.
- did: Waveform music -> separated stems; conv encoder, LSTM, conv decoder, GLU, U-Net skips, large strides, plus remix semi-supervision from unlabeled tracks with silent-source detection.
- evidence: MusDB 150 songs: 100 train/50 test, drums/bass/other/vocals; 2,000 unlabeled tracks. Median SDR on SiSec MusDB; beats Wave-U-Net by 1.6 SDR points.
- conditions: Offline music-source benchmark with SDR and ablations.
- limits: No speech, articulatory signal, real-time/mobile, or SSI adaptation; depends on music data.
- changes_view: Useful outside-domain waveform-separation distractor, not SSI evidence.

### 84. Attention based Convolutional Recurrent Neural Network for Environmental Sound Classification (2019)
- id: attention-based-convolutional-recurrent-neural-network-for-environmental-sound-classification
- trust: medium; venue=arXiv / imported corpus page.
- did: Acoustic clips -> ESC labels; CRNN with frame attention at CNN/RNN layers over Log-Gammatone spectrogram plus delta features.
- evidence: ESC-10/ESC-50, 5 s clips, 44.1 kHz, 5-fold CV. Accuracy: 93.7% ESC-10, 86.1% ESC-50; confusion matrices reported.
- conditions: Public ESC benchmarks with augmentation; accuracy main metric.
- limits: Fixed clips, no unseen noise/environment, no real-time or embedded test, no speech/SSI signal.
- changes_view: Attention helps sound classification; peripheral to silent speech.

### 85. Lipper: Synthesizing Thy Speech using Multi-View Lipreading (2019)
- id: lipper-synthesizing-thy-speech-using-multi-view-lipreading
- trust: high; venue=arXiv / imported corpus page.
- did: Multi-view lip/face video -> speech audio; regression framing, OuluVS2 speaker-dependent/independent tests, OOV phrases, latency analysis.
- evidence: Best 0+45+60 deg view set: PESQ 2.315. Delay 0.169 s across phrases vs 0.94-1.95 s comparison. User study: 80.25% audio-only, 81.25% audio-visual.
- conditions: Controlled OuluVS2 multi-camera PESQ, OOV, latency, user study.
- limits: Robotic audio, controlled pose/cameras, weak speaker independence, lip-only prosody/vocal-tract gaps.
- changes_view: Multi-view geometry and low latency matter, but naturalness/generalization remain weak.

### 86. Ultrasound-based Silent Speech Interface Built on a Continuous Vocoder (2019)
- id: ultrasound-based-silent-speech-interface-built-on-a-continuous-vocoder
- trust: medium-high; venue=arXiv / imported corpus page.
- did: UTI tongue images -> speech audio; continuous F0 interpolation replaces V/UV discontinuity; CNN predicts ContF0, MVF, MGC from single frames.
- evidence: 4 Hungarian speakers, 209 sentences each, about 15 min, 82 fps. V/UV about 78.8%; F0 RMSE 65.3 -> 30.6 Hz; MVF RMSE 654-1177 Hz; 23-listener MUSHRA trend not significant.
- conditions: Objective V/UV/RMSE plus Hungarian MUSHRA.
- limits: Small speaker-dependent set, single-frame CNN, no cross-speaker/wearable/real-time proof.
- changes_view: Continuous pitch modeling helps ultrasound SSI, but evidence is narrow.

### 87. Video-Driven Speech Reconstruction using Generative Adversarial Networks (2019)
- id: video-driven-speech-reconstruction-using-generative-adversarial-networks
- trust: high; venue=arXiv / imported corpus page.
- did: Silent frontal face video -> raw speech audio; direct generation with GAN and perceptual losses; evaluates seen/unseen GRID speakers.
- evidence: Speaker-dependent: WER 26.6%, STOI 0.518, MCD 22.29, AV confidence 4.4 at one-frame offset. Unseen: WER 40.5%, PESQ 1.24. Ablation: adversarial loss produces speech; perceptual loss preserves content.
- conditions: GRID PESQ/WER/AV synchrony/STOI/MCD plus ablations.
- limits: Frontal only, artifacts, poor unseen-speaker voice consistency, narrow GRID, in-the-wild unresolved.
- changes_view: Foundational direct video-to-audio result; generalization failure is part of the value.

### 88. A Novel Task-Oriented Text Corpus in Silent Speech Recognition and its Natural Language Generation Construction Method (2019)
- id: a-novel-task-oriented-text-corpus-in-silent-speech-recognition-and-its-natural-language-generation-construction-method
- trust: medium; venue=arXiv / imported corpus page.
- did: EEG-SSR corpus design -> task text corpus; narrows to life-support conversation, seeds manually, expands with neural NLG.
- evidence: Claims hybrid NLG beats pure template and pure neural NLG in SSR experiments, but extracted text lacks numeric margins. Motivation: open-domain EEG-text collection is too expensive.
- conditions: Methodological corpus construction with qualitative/comparative claims.
- limits: No EEG decoder, no deployed SSR system, narrow domain, weak auditable numbers.
- changes_view: Useful dataset-framing move: shrink language before EEG decoding.

### 89. Autoencoder-Based Articulatory-to-Acoustic Mapping for Ultrasound Silent Speech Interfaces (2019)
- id: autoencoder-based-articulatory-to-acoustic-mapping-for-ultrasound-silent-speech-interfaces
- trust: medium-high; venue=arXiv / imported corpus page.
- did: Ultrasound tongue video -> acoustic parameters/audio; autoencoder bottleneck features feed DNN MGC-LSP prediction, allowing multi-frame input without huge model growth.
- evidence: 2-4 MHz convex array, midsagittal 82 fps. One Hungarian female speaker, 438 sentences. Bottleneck features lower NMSE, raise Pearson correlation, improve MUSHRA naturalness vs full-image baseline; no numeric table exposed here.
- conditions: 25-parameter MGC-LSP regression plus MUSHRA listening.
- limits: Single speaker, no cross-session/speaker test, limited bottleneck study, no real-time/mobile proof.
- changes_view: Ultrasound representation compression helps, but evidence is single-speaker.

### 90. Denoising convolutional autoencoder based B-mode ultrasound tongue image feature extraction (2019)
- id: denoising-convolutional-autoencoder-based-b-mode-ultrasound-tongue-image-feature-extraction
- trust: medium-high; venue=arXiv / imported corpus page.
- did: B-mode UTI -> latent SSI recognition/text features; DCAE denoises speckle and preserves tongue structure better than AE/DCT.
- evidence: 2010 Silent Speech Challenge; midsagittal UTI 60 fps, 4-8 MHz, 128-element microconvex probe. DCAE WER 6.17% vs 6.45% DCT; CAE/DCAE improve MSE and CW-SSIM.
- conditions: Single-speaker challenge dataset; MSE, CW-SSIM, WER.
- limits: Single speaker, no cross-corpus/speaker validation, motion/speckle and hardware/stabilization remain.
- changes_view: Good ultrasound feature baseline, not deployed recognition.

### 91. All-neural online source separation, counting, and diarization for meeting analysis (2019)
- id: all-neural-online-source-separation-counting-and-diarization-for-meeting-analysis
- trust: high; venue=arXiv / imported corpus page.
- did: Single-channel meeting audio -> separated speech/diarization; block-online neural estimator jointly separates, counts sources, and preserves speaker identity through silent blocks.
- evidence: 12-block conversation-like condition: SDR 11.7 dB, DER 6.6%, SCER 4.9%; source counting >98%, >99% in most other conditions.
- conditions: Simulated online meeting mixtures; SDR, DER, SCER, count accuracy.
- limits: Meeting analysis, not SSI; simulated mixtures; no human-interaction deployment; below ideal-ratio-mask upper bound.
- changes_view: Adjacent idea for identity-through-silence, not silent-speech decoding.

### 92. SottoVoce: An Ultrasound Imaging-Based Silent Speech Interaction Using Deep Neural Networks (2019)
- id: sottovoce
- trust: high; venue=CHI '19.
- did: Under-jaw ultrasound -> regenerated audio -> unmodified smart speaker. Two-stage DNN frames SSI as audio regeneration/ecosystem reuse.
- evidence: 3.5 MHz convex probe; about 500 commands per collaborator; speaker-dependent. Network1 success 42.5%, Network1+2 65.0%, ground truth 90.0%. Google STT WER: 41.03%, 33.56%, 20.61%. Four Alexa commands x5; 3.68 s clip -> 2.61 s total.
- conditions: Smart-speaker success, Google WER, user adaptation notes.
- limits: Small vocabulary/data, speaker-dependent, slow, bulky probe/display capture, adaptation needed, safety/wearability untested.
- changes_view: Canonical pivot: regenerated audio reuses voice agents despite weak prototype.

### 93. Audio Spectrogram Factorization for Classification of Telephony Signals below the Auditory Threshold (2018)
- id: audio-spectrogram-factorization-for-classification-of-telephony-signals-below-the-auditory-threshold
- trust: high; venue=arXiv / imported corpus page.
- did: First 2 s telephony audio -> SPAM/HAM; SVD spectrogram features detect sub-audible/dead-air robocalls within call-bridging latency.
- evidence: Random Forest precision 83.82%, recall 63.27%, accuracy 90.40%, better than linear SVC for high-precision business goal. Traffic-pumping attacks add 10,000-33,000 silent calls/day; max latency 2 s.
- conditions: Cross-validation on proprietary labeled telephony calls.
- limits: No speech decoding/SSI; proprietary imbalanced data; specialized VoIP anti-SPAM setting.
- changes_view: "Silent" means dead-air telephony, not silent speech.

### 94. Proactive Security: Embedded AI Solution for Violent and Abusive Speech Recognition (2018)
- id: proactive-security-embedded-ai-solution-for-violent-and-abusive-speech-recognition
- trust: medium; venue=arXiv / imported corpus page.
- did: Smartphone mic -> violent/abusive alert; SpeechRecognizer + SVM BoW/embeddings + SMOTE.
- evidence: 1200 PT-BR sentences: 400 positive, 800 negative. BoW+SVM: 79% acc, F1 0.78, FP 26%, FN 14%. Embeddings+SMOTE: 87.5% acc, F1 0.87, TP 94%, FP 6%, TN 78%, FN 22%; model <10 MB.
- conditions: Internal 70/30 validation, no real-world study.
- limits: Not SSI; beeps/restarts/battery ~15 h; small PT-BR corpus.
- changes_view: Deployment caution for microphone alerts, not SSI.

### 95. Harnessing AI for Speech Reconstruction using Multi-view Silent Video Feed (2018)
- id: harnessing-ai-for-speech-reconstruction-using-multi-view-silent-video-feed
- trust: medium-high; venue=arXiv / imported corpus page.
- did: Multi-view silent video -> synchronized speech audio; CNN-LSTM maps views to LPC features and studies camera placement.
- evidence: OuluVS2, 53 speakers, angles 0/30/45/60/90 deg. PESQ used. Combining 30-60 deg views gives about 26%-27% improvement over best single view.
- conditions: Controlled OuluVS2 PESQ evaluation.
- limits: Multiple optimally placed cameras, controlled lighting, speaker-dependent training, limited vocabulary, no noisy/in-the-wild robustness.
- changes_view: View geometry helps video-to-speech, but hardware/control burden is high.

### 96. Visual-Only Recognition of Normal, Whispered and Silent Speech (2018)
- id: visual-only-recognition-of-normal-whispered-and-silent-speech
- trust: high; venue=arXiv / imported corpus page.
- did: Normal/whispered/silent visual speech -> text labels; tests whether silent speech can use vocalized training.
- evidence: Digits 53 participants; phrases 39. Cameras: frontal/45 deg/profile, 1280x780, 30 fps. Matched digits: 68.0/70.5/62.2%; normal->silent 59.7%. Matched phrases: 69.7/70.8/64.4%; normal->silent 61.2%.
- conditions: Subject-independent train/validation/test for digits and fixed phrases.
- limits: Closed vocabulary, lab capture, no open/in-the-wild/live interface, rates below practical communication.
- changes_view: Core warning: silent visual speech is distinct; vocalized-only training is suboptimal.

### 97. Cross-modal Embeddings for Video and Audio Retrieval (2018)
- id: cross-modal-embeddings-for-video-and-audio-retrieval
- trust: high; venue=arXiv / imported corpus page.
- did: Precomputed YouTube-8M audio/video features -> retrieval ranking; learns joint embedding for audio-to-video and video-to-audio retrieval.
- evidence: 6,000-clip subset. At 256 candidates: A->V Recall@1/5/10 = 21.5/52.0/63.1; V->A = 22.3/51.7/64.4. Recall@1 drops to about 10% at 1024 candidates.
- conditions: Bidirectional retrieval; Recall@1/5/10; visual features at 1 Hz.
- limits: No speech decoding/synthesis, no communication task, no fine temporal alignment, offline precomputed features.
- changes_view: Multimodal distractor, not SSI.

### 98. Lip2AudSpec: Speech reconstruction from silent lip movements video (2017)
- id: lip2audspec-speech-reconstruction-from-silent-lip-movements-video
- trust: high; venue=arXiv / imported corpus page.
- did: Silent lip video -> speech audio; auditory-spectrogram bottleneck target predicted by CNN/LSTM/FC layers.
- evidence: 4 GRID speakers. STMI 0.80 vs 0.52; PESQ 1.88 vs 1.76; Corr2D 0.88 vs 0.61. MTurk: word accuracy 55.8% vs 50.9%; gender 85.1% vs 43.2%.
- conditions: Corr2D/PESQ/STMI plus human transcription and naturalness/gender surveys.
- limits: Lip-only misses tongue/throat cues; closed vocabulary, 4 speakers, no real-world deployment.
- changes_view: Target representation matters; deep auditory bottlenecks improve lip-to-speech.

### 99. Updating the silent speech challenge benchmark with deep learning (2017)
- id: updating-the-silent-speech-challenge-benchmark-with-deep-learning
- trust: high; venue=arXiv / imported corpus page.
- did: Ultrasound tongue + lip video -> text; reruns 2010 Silent Speech Challenge in Kaldi with HTK/GMM-HMM/DNN-HMM and LM/feature sweeps.
- evidence: Single native-English-speaker archive with independent test. WER: original HTK 17.4%, Kaldi GMM-HMM 17.4%, DNN-HMM 30-DCT 6.45%. DNN WER: WSJ LM 11.44%, task CSR LM 6.45%.
- conditions: Matched benchmark decoding and LM comparison.
- limits: Single-speaker controlled archive; no speaker independence, live deployment, or calibration burden.
- changes_view: Canonical benchmark update: DNN-HMM and task LM materially change SSI WER.

### 100. Seeing Through Noise: Visually Driven Speaker Separation and Enhancement (2017)
- id: seeing-through-noise-visually-driven-speaker-separation-and-enhancement
- trust: high; venue=arXiv / imported corpus page.
- did: Audio mixture + face video -> target audio; vid2speech mel predictions become mask priors, not final output.
- evidence: GRID ratio mask SDR 5.62/PESQ 2.6 vs audio-only 1.74/1.85. TCD-TIMIT SDR 8.68/PESQ 2.71 vs 2.91/2.16. Unknown GRID after 5-min fine-tune: SDR 3.06, PESQ 2.42.
- conditions: Synthetic GRID/TCD-TIMIT mixtures; SDR/SIR/SAR/PESQ; limited transfer.
- limits: Not SSI; needs visible face+audio, speaker-dependent training/fine-tuning, no real noisy benchmark.
- changes_view: Visual priors help separation; not silent communication.

### 101. Improved Speech Reconstruction from Silent Video (2017)
- id: improved-speech-reconstruction-from-silent-video
- trust: high; venue=arXiv / imported corpus page.
- did: Silent full-face frames + optical flow -> speech audio; dual-stream ResNet, spectrogram decoder, CBHG postnet, regression framing.
- evidence: GRID S3: STOI 0.68, ESTOI 0.398, PESQ 1.974, ViSQOL 3.349. TCD-TIMIT L3: STOI 0.63, ESTOI 0.447, PESQ 1.612. MTurk 50.9% -> 55.8%; flow/postnet help.
- conditions: GRID S1-S4, TCD-TIMIT L1-L3; objective metrics, humans, ablations.
- limits: Speaker-dependent registered video; partial unconstrained intelligibility; no unseen-speaker/real-time/wild test.
- changes_view: Strong video-to-speech baseline with unresolved generalization.

### 102. Vid2speech: Speech Reconstruction from Silent Video (2017)
- id: vid2speech-speech-reconstruction-from-silent-video
- trust: high; venue=arXiv / imported corpus page.
- did: Silent face/lip video -> speech audio; CNN regresses acoustic/LPC features and tests held-out digits.
- evidence: GRID 25 FPS, 720x576, 3 s clips, 51-word grammar; 1000 S4 videos. S4 audio-only 82.6%; S4/S2 audio-visual 79.9%/79.0% vs prior 40.0%/51.9%. OOV audio-visual 51.6% vs 10.0% chance and 93.4% no holdout.
- conditions: MTurk intelligibility for audio-only/audio-visual/OOV.
- limits: Speaker-specific, constrained GRID, LPC artifacts, no open/in-the-wild/live system.
- changes_view: Early lip-to-speech milestone; OOV result matters.

### 103. Contour-based 3d tongue motion visualization using ultrasound image sequences (2016)
- id: contour-based-3d-tongue-motion-visualization-using-ultrasound-image-sequences
- trust: high; venue=arXiv / imported corpus page.
- did: B-mode ultrasound tongue contour -> 3D tongue visualization; contour extraction drives finite-element tongue model via modal reduction, modal warping, and database matching.
- evidence: 1000 sample 3D tongue shapes. Section 5: about 1.2 s average to associate a frame with the 3D model. Authors say no effective quantitative evaluation method is available.
- conditions: Qualitative visualization, runtime report, midsagittal overlay.
- limits: Not recognition/communication; midsagittal misses out-of-plane motion; simplified four-node drive; no MRI/EMA quantitative validation; not proven real-time.
- changes_view: Useful articulatory-analysis support, not decoder evidence.

### 104. Optimal Power Control for Analog Bidirectional Relaying with Long-Term Relay Power Constraint (2014)
- id: optimal-power-control-for-analog-bidirectional-relaying-with-long-term-relay-power-constraint
- trust: medium-high; venue=arXiv / imported corpus page.
- did: Relay-link CSI -> optimal relay power policy; outage-minimizing allocation for bidirectional AF relaying with fixed source powers and long-term average relay power.
- evidence: Theorem 1: truncated channel-inversion cutoff policy; transmit at minimum outage-free short-term relay power below cutoff rho, otherwise silent. Figs. 2-3 compare outage/power saving vs fixed and short-term controls.
- conditions: Closed-form derivation plus Rayleigh block-fading simulations, perfect relay CSI, fixed end-node powers.
- limits: Communications theory only; no implementation, speech/video, SSI, or realistic-channel deployment.
- changes_view: Outside-domain distractor; "silent" has no SSI relevance.
