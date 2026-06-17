# SSI Knowledge Distillation Process Report and View Catalog

created: 2026-06-17T14:44:07+0900

## 1. Scope

This report reconstructs the SSI knowledge-distillation process from the local artifacts created in GitHub Issues #67 and #68.

Primary source artifacts:

- `reports/ssi_all_context_framework/all_compressed_codex.md`
- `reports/ssi_all_context_framework/framework_from_all_compressed.md`
- `reports/ssi_all_context_framework/framework_audit.md`
- `reports/ssi_10_loop_views/README.md`
- `reports/ssi_10_loop_views/audit.md`
- `reports/ssi_10_loop_views/loops/loop_01_review.md` through `loop_10_review.md`
- `reports/ssi_10_loop_views/loops/loop_01_compressed.md` through `loop_10_compressed.md`
- `reports/ssi_10_loop_views/loops/loop_01_next_view.md` through `loop_10_next_view.md`

Local duplicate artifacts with the suffix ` 2` were also inspected because they remain available in this worktree and contain the same report structure.

## 2. What Was Being Tested

The experiment was not "summarize SSI papers once."

The target was:

- collect many SSI-related source records;
- compress each record enough to fit many records into one model context;
- ask Codex to read the whole compressed bundle without using the master's hand-built SSI framework;
- derive a first broad analytical view from the bundle;
- repeatedly reread the same bundle through the latest view;
- observe whether the view becomes sharper over loops.

The important test was whether a large compressed bundle can produce higher-order domain judgment:

- not only "what each paper says";
- but "how to read the field";
- "which claims are strong or weak";
- "where results break";
- "what hidden conditions support the numbers";
- "which questions should guide the next reading."

## 3. Issue #67: Build the All-SSI Compressed Context

Issue #67 created the first cross-document SSI context.

Input:

- 105 SSI-related expert-review records.
- These records covered core SSI, low-volume and whispered speech, lip-to-speech, ultrasound, EMG, EEG, ECoG, EPG, radar, speech enhancement, Foley, audio-visual segmentation, and other neighboring work.

Important limitation:

- The input was not every original full-paper PDF.
- It was an expert-review export that already contained selected judgment material.

Compression result:

- source records: 105 papers
- source tokens: 256,916
- compressed Codex bundle tokens: 24,227
- compressed ratio: 9.43% against the source JSON
- bundle coverage: 105 / 105 records

Artifacts:

- `ssi-review.json`
- `compressed/batch_00_26.md`
- `compressed/batch_27_53.md`
- `compressed/batch_54_79.md`
- `compressed/batch_80_104.md`
- `all_compressed_codex.md`
- `framework_from_all_compressed.md`
- `framework_audit.md`

Method:

- Records were split into four batches.
- Each batch was compressed while preserving decision material, numbers, constraints, failures, and limits.
- The four batch outputs were merged into one Codex-readable bundle.
- A worker then read the whole compressed bundle and produced a fresh SSI framework without reading the master's pre-existing hand-made framework.

Weak result:

- The bundle preserved judgment material, not full experiment tables.
- Exact protocol details, statistics, code release status, and audio samples were not rechecked.
- The final view depends on what survived the expert-review export and compression.

## 4. First Framework From the 105-Record Bundle

The first framework already moved away from a simple paper ranking.

Main facts it extracted:

- Many of the 105 records were not core SSI. Some were neighboring component research.
- Practical-looking systems were often not pure silent open-vocabulary speech. They narrowed the task: lip commands, spelling, whispered or low-volume speech, smartphone acoustic sensing, EPG spelling.
- Strong speech restoration papers often remained speaker-dependent, closed-vocabulary, controlled-environment, or offline.
- From roughly 2022-2023 onward, many systems borrowed large speech representations: HuBERT, AV-HuBERT, wav2vec2, speech units, lip-reader guidance, ASR guidance, audio memory, speaker embedding.
- Noninvasive EEG and MEG looked closer to basic research than practical SSI.

Main interpretation:

- SSI should not be read as one single race toward fully silent natural conversation.
- The field is a mix of input design, body-signal reading, speech generation, correction, and connection to existing ASR/TTS or smart-speaker systems.

Initial 12 views:

1. Inputs that arrive before fully silent speech.
2. Narrower tasks are closer to use.
3. Speaker dependence remains central.
4. Silent, whispered, normal, and vocalized speech are different modes.
5. Sensor placement often determines model performance.
6. Speech-side knowledge is increasingly borrowed.
7. Text output and speech output are different fields.
8. Metrics can hide the real purpose.
9. Practical closeness is determined more by operating conditions than benchmark scores.
10. Direct patient value remains weakly proven.
11. Neighboring research should be read as parts, not as SSI evidence.
12. Strong studies show failure conditions.

## 4A. Performance Comparison and Ranking Catalog

The original loop did contain early performance comparison, especially in loop 01. However, the first version of this report underplayed it by emphasizing the later route-based view. That was incomplete: ranking is still important. The correct lesson is not "do not rank"; it is "rank under an explicit comparison axis."

The ranking problem has three layers:

- global practical ranking: which systems look closest to actual communication use today;
- route-level ranking: which systems are strongest inside the same route;
- metric-level ranking: which papers report the strongest numbers under their own task definition.

A single all-paper leaderboard is dangerous because the tasks differ: 30 commands, spelling, 54 sentences, open-vocabulary speech, silent-to-speech generation, low-volume enhancement, EEG imagined speech, and patient restoration are not the same problem. But a report must still preserve rankable evidence.

### 4A.1 Provisional Global Practical Ranking

Criterion:

- Can the system support actual communication soon?
- Important factors: live use, latency, user correction, task usefulness, setup burden, and whether the output can connect to an existing communication system.

This is not a pure SSI ranking. It is a "near-term communication usefulness" ranking from the compressed 105-record bundle.

Rank 1: SilentSpeller

- Evidence: 124-electrode EPG, 26 letters and space, about 97% character accuracy, 92% word accuracy, unknown 100 words at 94.5% character and 85.5% word, seven-user live average 37 wpm at 87%, best 53 wpm at 91%, walking 97.5%, seated 96.5%.
- Why high: live communication, speed, editing, walking evidence.
- Cost: custom dental impression, 1-2 h user-dependent training, spelling input, no punctuation/capitalization in the compressed record.
- Judgment: strongest near-term communication route, but it wins by changing the task into spelling.

Rank 2: LipLearner

- Evidence: smartphone front camera, 25-30 command setting, one-shot 81.7%, five-shot 98.8%, F1 0.8947 for 25-command condition, about 422 ms latency, 11 participants and 16-person field/live evidence in the compressed record.
- Why high: ordinary device direction, low latency, active learning, clear command use.
- Cost: limited command vocabulary, similar-command confusion, user correction burden, enrollment.
- Judgment: very strong near-term command interface, not open conversation.

Rank 3: WESPER

- Evidence: whisper-to-normal speech conversion, Google ASR WER/CER 44.70/28.38 to 26.68/12.70; HuBERT-base condition 13.75/5.47.
- Why high: uses a realistic input path and connects to existing speech systems.
- Cost: whisper or low-volume input, not fully silent.
- Judgment: practical and useful, but weaker as evidence for pure silent speech.

Rank 4: NasoVoce

- Evidence: nasal-pad low-volume speech, 1000 held-out items, -10 to 10 dB synthetic noise, 50-person MUSHRA, four real-environment recordings.
- Why high: wearable-ish route, existing ASR/TTS connection, environment evidence.
- Cost: low-volume speech, not pure silence; central evidence includes synthetic noise.
- Judgment: strong practical adjacent route.

Rank 5: End-to-End Silent Speech Recognition with Acoustic Sensing

- Evidence: smartphone-like inaudible acoustic sensing, 54 sentences, domain-dependent WER 2.6%, domain-independent average 8.4%, unseen-sentence WER 8.1%.
- Why high: low apparent user burden and strong WER inside its sentence space.
- Cost: only 54 sentences in the compressed record; broader vocabulary and long-term use are unclear.
- Judgment: strong controlled-sentence result; rank would drop for open vocabulary.

Rank 6: SottoVoce

- Evidence: submandibular ultrasound to regenerated audio, Google STT WER 41.03% to 33.56%, Alexa command success 65.0%, total processing 2.61 s.
- Why high: bridges silent articulation into existing smart-speaker audio interface.
- Cost: ultrasound probe, speaker-dependent data, short commands, latency, only partial success.
- Judgment: conceptually important bridge, but not yet near-term robust communication.

Rank 7: Guided lip-to-speech / visual-to-speech systems such as LipVoicer and AKVSR

- Evidence: LipVoicer LRS3 WER 21.4% with ASR guidance; AKVSR LRS3 WER 46.1% to 23.6%.
- Why high: strong modern speech-model support and open-ended generation direction.
- Cost: heavy external guidance; LipVoicer without guidance worsens to 86.2% WER.
- Judgment: strong research direction, but practical rank is limited by hidden model dependency and recovery design.

Rank 8: Ultrasound, EMG, and TaL-style silent reconstruction systems

- Evidence: TaL silent WER 43.114%, vocalized 17.309%; TaL80 silent 69.84, modal 39.34; ultrasound STN recovered 88% cross-speaker gap and 92% cross-session gap; Digital Voicing closed-vocabulary human WER 3.6% but open-vocabulary human WER 74.8%, automatic 68.0%.
- Why high: core silent-articulation route.
- Cost: speaker dependence, remount, probe/electrode burden, open-vocabulary failure.
- Judgment: central scientifically, but lower near-term practical rank.

Rank 9: Patient-restoration route

- Evidence: Cross-Modal Masking improved Whisper v3 WER by up to 14 absolute points and included laryngeal/laryngectomized direction; SottoVoce also points toward assistive value.
- Why high: highest social value.
- Cost: laryngectomized adaptation is weak; target-user evidence remains small.
- Judgment: value rank high, performance rank still weak.

Rank 10: EEG/MEG/noninvasive brain-signal route

- Evidence: MEG imagined speech Recall@1 about 9.1%; EEG imagined direct 30.5% +/- 4.9%; continuous EEG SSR WER 74.86%-84.22%, cross-subject 92.55%; JapanEEG has 1020 h but n=3 and no mature decoding benchmark in the compressed record.
- Why included: important long-range route.
- Cost: equipment, low accuracy, generalization, distance from daily communication.
- Judgment: scientifically important, currently lowest practical rank.

### 4A.2 Route-Level Rankings

#### Low-volume / whisper route

Rank 1: WESPER

- Best compressed-record evidence: WER/CER 44.70/28.38 to 26.68/12.70; HuBERT-base 13.75/5.47.
- Strength: ASR-facing practical improvement.
- Weakness: whisper input, not silent input.

Rank 2: NasoVoce

- Best compressed-record evidence: 1000 held-out items, -10 to 10 dB noise, 50-person MUSHRA, four real environments.
- Strength: wearable-ish input and environment-oriented evaluation.
- Weakness: low-volume speech and synthetic-noise emphasis.

#### Command / spelling / short-controlled route

Rank 1: SilentSpeller

- Best compressed-record evidence: live seven-user 37 wpm at 87%, best 53 wpm at 91%; walking 97.5%; seated 96.5%.
- Strength: live communication and correction.
- Weakness: custom oral device and spelling.

Rank 2: LipLearner

- Best compressed-record evidence: 30-command one-shot 81.7%, five-shot 98.8%, about 422 ms.
- Strength: smartphone route and low latency.
- Weakness: command limitation and correction burden.

Rank 3: IR-UWB radar

- Best compressed-record evidence: 25 words 88.95%, 12 phrases 96.88%.
- Strength: contactless sensing.
- Weakness: closed set and geometry dependence.

Rank 4: Acoustic sensing

- Best compressed-record evidence: 54 sentences, unseen-sentence WER 8.1%.
- Strength: strong sentence-level number.
- Weakness: sentence set too small for open-vocabulary claims.

#### Silent reconstruction route

Rank 1: Digital Voicing, closed-vocabulary condition

- Best compressed-record evidence: closed-vocabulary human WER 3.6%.
- Strength: very strong number in narrow setting.
- Weakness: open-vocabulary human WER 74.8%, automatic 68.0%; subject-specific data.

Rank 2: Metric-learning normal-to-silent visual speech work

- Best compressed-record evidence: best silent WER 9.97% on AV Digits 10 phrases.
- Strength: directly attacks normal-silent gap.
- Weakness: phrase/digit domain.

Rank 3: Let There Be Sound

- Best compressed-record evidence: GRID WER 17.07%.
- Strength: strong number in GRID setting with HuBERT units.
- Weakness: dataset/task constraints.

Rank 4: LipVoicer with guidance

- Best compressed-record evidence: LRS3 WER 21.4%.
- Strength: strong open visual-to-speech direction.
- Weakness: without guidance WER worsens to 86.2%.

Rank 5: AKVSR

- Best compressed-record evidence: LRS3 WER 46.1% to 23.6%.
- Strength: audio memory / pretrained representation improves decoding.
- Weakness: external speech-model burden.

Rank 6: Intelligible Lip-to-Speech with Speech Units

- Best compressed-record evidence: LRS3 WER 29.8%.
- Strength: speech-unit supervision without text labels.
- Weakness: still speech-prior dependent.

Rank 7: SottoVoce

- Best compressed-record evidence: Google STT WER 33.56%, Alexa success 65.0%.
- Strength: smart-speaker bridge.
- Weakness: ultrasound, latency, speaker dependence.

Rank 8: TaL / TaL80 silent conditions

- Best compressed-record evidence: TaL silent 43.114%, TaL80 silent 69.84.
- Strength: important benchmark direction.
- Weakness: silent condition remains hard.

#### Patient-restoration route

Rank 1: Cross-Modal Masking with sEMG and lipreading

- Best compressed-record evidence: Whisper v3 WER improved by up to 14 absolute points.
- Strength: directly touches laryngeal/laryngectomized direction.
- Weakness: laryngectomized adaptation remains weak.

Rank 2: SottoVoce as assistive bridge

- Best compressed-record evidence: 65.0% smart-speaker command success.
- Strength: silent articulation to voice-agent operation.
- Weakness: not clinically proven as patient restoration in the compressed record.

#### Brain-signal route

Rank 1: Brain2Char for invasive or severe-case direction

- Best compressed-record evidence: normal WER 7.0%-10.6%, but silent/mimed 40%/67%.
- Strength: strongest communication-shaped brain-signal route in the compressed set.
- Weakness: invasive and silent/mimed degradation.

Rank 2: EEG imagined direct classification

- Best compressed-record evidence: 30.5% +/- 4.9% in five classes.
- Strength: noninvasive signal exists.
- Weakness: not yet robust communication.

Rank 3: MEG imagined speech

- Best compressed-record evidence: Recall@1 about 9.1%.
- Strength: interesting mapping from imagined to listened speech.
- Weakness: very far from daily use.

Rank 4: Continuous EEG silent speech recognition

- Best compressed-record evidence: WER 74.86%-84.22%, cross-subject 92.55%.
- Strength: exposes current difficulty.
- Weakness: high WER and poor cross-subject behavior.

### 4A.3 Metric-Level Top Results

This table is useful for preserving the early "performance comparison" instinct. It must be read with the task column.

| Rank type | System / paper family | Reported number in compressed bundle | Task condition | Main caveat |
|---|---|---:|---|---|
| Best narrow human WER | Digital Voicing | 3.6% human WER | closed vocabulary | open vocabulary much worse |
| Best controlled sentence WER | Acoustic sensing | 2.6% domain-dependent WER; 8.1% unseen-sentence WER | 54 sentences | small sentence universe |
| Best live spelling throughput | SilentSpeller | 37 wpm at 87%; best 53 wpm at 91% | spelling | custom palate and training |
| Best command accuracy | LipLearner | 81.7% one-shot; 98.8% five-shot | 30 commands | enrollment and command limit |
| Best radar phrase number | IR-UWB radar | 12 phrases 96.88%; 25 words 88.95% | closed set | geometry dependence |
| Best whisper-to-ASR improvement | WESPER | WER/CER 44.70/28.38 to 26.68/12.70; HuBERT-base 13.75/5.47 | whispered speech | not fully silent |
| Strong guided LRS3 result | LipVoicer | 21.4% WER | guided lip-to-speech | no-guidance WER 86.2% |
| Strong audio-memory LRS3 result | AKVSR | 46.1% to 23.6% WER | visual speech with audio memory | external model burden |
| Smart-speaker bridge | SottoVoce | 65.0% Alexa success; 33.56% Google STT WER | ultrasound to regenerated audio | latency 2.61 s |
| Silent benchmark difficulty | TaL / TaL80 | TaL silent 43.114%; TaL80 silent 69.84 | silent articulation | still high error |
| Brain-signal current limit | MEG / EEG | MEG Recall@1 about 9.1%; EEG cross-subject WER 92.55% | imagined/silent brain signal | not practical communication |

### 4A.4 Ranking Rules To Keep

To preserve ranking without fooling ourselves:

1. Always rank within a route first.
2. Put task condition beside every number.
3. Put the hidden cost beside every rank.
4. Separate "practical communication rank" from "scientific ambition rank."
5. Separate "pure silent SSI rank" from "low-volume or adjacent route rank."
6. Penalize results that collapse when guidance, speaker-specific data, fixed placement, or closed vocabulary is removed.
7. Reward papers that reveal failure conditions, even if their top-line number is worse.
8. Do not collapse WER, command accuracy, wpm, MOS, PESQ, STOI, and success rate into one numeric score without a declared weighting.

The correct final stance is:

- ranking is necessary;
- global ranking is provisional;
- route-aware ranking is mandatory;
- every rank needs its cost and stop condition beside it.

## 5. Issue #68: Ten Review-Compression-Next-View Loops

Issue #68 performed the repeated view refinement.

Loop shape:

- `review`: read the bundle using the previous view as the current lens.
- `compressed`: keep only the judgment-changing elements from that review.
- `next_view`: define the next reading lens, including facts, inferences, unknowns, and warnings.

Verification:

- review files: 10
- compressed files: 10
- next_view files: 10
- loop 04 used loop 03 next_view.
- loop 05 used loop 04 next_view.
- loop 06 used loop 05 next_view.
- loop 07 used loop 06 next_view.
- loop 08 used loop 07 next_view.
- loop 09 used loop 08 next_view.
- loop 10 used loop 09 next_view.

Token totals:

- review total: 14,149
- compressed total: 5,164
- next_view total: 2,502
- all loop files total: 21,815

Compression ratios by loop:

- loop 01: 0.312
- loop 02: 0.298
- loop 03: 0.343
- loop 04: 0.388
- loop 05: 0.363
- loop 06: 0.378
- loop 07: 0.367
- loop 08: 0.410
- loop 09: 0.478
- loop 10: 0.393

Weak result:

- The 10-loop structure was completed.
- The loop-compressed files were shorter than the reviews, but not all reached 20% or lower.
- The loops used the 105-paper compressed expert-review bundle, not full original PDFs.
- The run was not an externally refreshed literature review.

## 6. Loop-by-Loop Evolution

### Loop 01: From Paper Ranking to Communication Use

Reading view:

- Read the 105 records as "can this actually communicate intent today?"

What it found:

- The closest systems were not fully silent open-vocabulary natural conversation.
- They narrowed the task or weakened the silence condition.
- LipLearner handled 30 commands: one-shot 81.7%, five-shot 98.8%, about 422 ms.
- SilentSpeller handled spelling: average 37 wpm at 87%, best 53 wpm at 91%.
- Acoustic sensing handled 54 sentences with unseen-sentence WER 8.1%, but the sentence set was small.
- NasoVoce and WESPER moved toward open-vocabulary use by accepting low-volume or whispered input.
- Digital Voicing had strong closed-vocabulary human WER 3.6%, but open-vocabulary human WER 74.8% and automatic WER 68.0%.
- SottoVoce reached 65.0% Alexa command success and 2.61 s total processing.
- LipVoicer collapsed from 21.4% to 86.2% WER when ASR guidance was removed.

View change:

- The field stopped looking like a direct "who has the best WER" contest.
- It began looking like a communication-design problem.

Next view:

- Read by who pays the burden: user, device, training data, environment, external model, task limitation.

### Loop 02: Burden Allocation

Reading view:

- Ask who pays for the result.

What it found:

- Nearer systems often asked the user to pay a little:
  - few-shot enrollment;
  - correction;
  - spelling;
  - one to two hours of training;
  - custom mouth hardware;
  - speaker-specific data.
- Farther systems often asked the device or environment to pay:
  - ultrasound probe fixing;
  - remount adaptation;
  - radar geometry;
  - multi-view cameras;
  - high-density EEG or MEG.
- Generation systems asked external models and pretrained representations to pay:
  - HuBERT;
  - audio memory;
  - speech units;
  - lip-reader text;
  - ASR guidance.
- Task limitation was itself a form of burden:
  - 30 commands;
  - 26 letters;
  - 54 sentences;
  - 8 vowels, 11 consonants, 25 words, 12 phrases;
  - 5 classes;
  - 76 words.

View change:

- High score became less important than burden placement.
- Practical systems looked strong when the burden was distributed and acceptable.

Next view:

- Read by where information shortage is repaired.

### Loop 03: Repair Stage

Reading view:

- Divide the pipeline into four stages:
  - acquisition;
  - speech-mode difference;
  - decoding freedom;
  - handoff and correction after output.

What it found:

- Acquisition often breaks first:
  - ultrasound needs probe placement;
  - radar needs geometry;
  - lip systems need view and alignment;
  - NasoVoce weakens on whisper vibration;
  - EPG, EMG, ultrasound, radar all have placement costs.
- Silent speech is not just normal speech with sound removed:
  - normal-to-silent transfer loses performance;
  - silent, whispered, mimed, vocalized, and post-laryngectomy speech differ.
- Increasing vocabulary or output freedom causes errors to jump.
- Systems closer to use had handoff and correction:
  - smart speaker connection;
  - edit gestures;
  - active learning;
  - ASR/TTS connection.

View change:

- SSI progress became a sequence of repair sites, not one model-quality score.

Next view:

- Read by who corrects errors, and when.

### Loop 04: Error Correction Contract

Reading view:

- Ask who corrects errors:
  - device or preprocessing;
  - model;
  - external model;
  - user;
  - existing service.

What it found:

- Device-side correction:
  - ultrasound STN recovered 88% cross-speaker gap and 92% cross-session gap.
  - cross-modal masking improved Whisper v3 WER by up to 14 absolute points.
- Model-side correction:
  - metric learning aligned normal and silent distributions;
  - pseudo-target and domain-adversarial approaches handled silent-vocalized mismatch.
- External-model correction:
  - LipVoicer depended heavily on ASR guidance;
  - AKVSR reduced LRS3 WER from 46.1% to 23.6%.
- User-side correction:
  - LipLearner used active learning and correction;
  - SilentSpeller used spelling and edit gestures.
- Existing-service correction:
  - SottoVoce handed audio to smart speakers;
  - WESPER and NasoVoce pushed low-volume or whisper input toward existing ASR.

View change:

- "Accuracy" became incomplete unless the report also says who corrected the error.

Next view:

- Read by what the system borrows to correct errors.

### Loop 05: Dependencies

Reading view:

- Ask what the result depends on.

What it found:

- Common dependencies:
  - narrow vocabulary or task;
  - speaker-specific training;
  - fixed sensor placement;
  - speech or text prior;
  - paired vocalized-silent data;
  - low-volume or whispered speech instead of full silence.
- Light dependencies:
  - smartphone;
  - short enrollment;
  - existing ASR.
- Heavy dependencies:
  - custom oral hardware;
  - long speaker-specific training;
  - fixed ultrasound probe;
  - paired corpora;
  - large external speech model.

View change:

- Modality became secondary.
- The important question became: what must be held fixed for the result to exist?

Next view:

- Read by where these dependencies break over time.

### Loop 06: Durability Over Time

Reading view:

- Ask whether the system works tomorrow, next week, after remounting, with fatigue, with new words, and in new conditions.

What it found:

- Direct evidence for long-term and repeated use was sparse.
- Many studies remained same-session, single-speaker, offline, read-speech, or controlled.
- Remounting was a major failure source.
- SilentSpeller had live use and walking/seated results, but required custom dental hardware and training.
- LipLearner had live study and about 422 ms latency, but still had command confusion and correction burden.
- NasoVoce and WESPER looked easier to maintain, but were not fully silent.
- SottoVoce had useful smart-speaker connection but 65.0% success and 2.61 s total processing.

View change:

- Practicality shifted from "can it work once?" to "how badly does it decay?"

Next view:

- Read by how the system recovers after failure.

### Loop 07: Recovery After Failure

Reading view:

- Ask how communication resumes after an error, delay, sensor shift, or user fatigue.

What it found:

- Explicit recovery designs were rare.
- LipLearner recovered through few-shot enrollment and active learning.
- SilentSpeller recovered through spelling, push-to-talk, and edit gestures.
- NasoVoce and WESPER recovered by falling back to low-volume or whisper paths.
- SottoVoce connected to smart speakers but did not have a fast recovery loop.
- Generation-heavy systems often corrected before the user saw an error, but did not expose confidence, rejection, or partial editing in the compressed records.
- Weak lines such as EEG, TaL80, and Brain2Char showed little usable recovery procedure.

View change:

- The most useful systems were not necessarily the most accurate ones.
- They were the systems where failure could be made small and recoverable.

Next view:

- Read by what stops communication entirely.

### Loop 08: Stop Conditions

Reading view:

- Identify conditions where communication stops.

What it found:

Major stop conditions:

- open vocabulary;
- speech-mode mismatch;
- unseen speaker;
- patient or laryngectomized adaptation;
- remount or sensor position;
- real-time latency;
- real environment;
- lightweight wearable use;
- clinical evidence.

Examples:

- Digital Voicing stopped at open vocabulary: human WER 74.8, automatic WER 68.0.
- LipVoicer stopped when guidance was removed: WER 86.2.
- TaL and TaL80 stopped at silent-vs-vocalized mismatch.
- EEG stopped at cross-subject generalization.
- SottoVoce stopped at latency and partial command success.
- NasoVoce still leaned on synthetic-noise evidence.
- SilentSpeller handled walking but paid with dental hardware and spelling input.

View change:

- A single global ranking became clearly wrong.
- Each approach fights a different stop condition.

Next view:

- Read by route: which stop condition the system is trying to remove.

### Loop 09: Route-Based Reading

Reading view:

- Split studies by route instead of ranking them together.

Five routes:

1. Low-volume input connected to existing speech systems.
2. Commands, spelling, or short controlled input.
3. Silent video or articulatory signal to speech or text.
4. Direct restoration for patients or people with voice loss.
5. Brain-signal or basic-research route.

What it found:

- Low-volume route:
  - NasoVoce and WESPER weaken full silence but gain connection and near-term usability.
- Narrow-task route:
  - LipLearner, SilentSpeller, and radar improve reliability by narrowing the communication act.
- Silent-reconstruction route:
  - AKVSR, LipVoicer, TaL, TaL80, SottoVoce and related work have research depth but many stop conditions.
- Patient-restoration route:
  - Cross-modal masking and SottoVoce show direction, but patient evidence remains weak.
- Brain-signal route:
  - JapanEEG, MEG, EEG, Brain2Char are valuable but far from everyday communication.

View change:

- Comparing LipLearner 98.8% and TaL silent WER 43.114% as if they were the same task became invalid.
- Route separation preserved both practical and scientific value.

Next view:

- Read by who pays the remaining burden in each route.

### Loop 10: Burden by Route

Reading view:

- For each route, ask who still pays the cost.

Findings:

- Low-volume route:
  - existing speech ecosystem pays much of the cost;
  - user and device cost are lower;
  - full silence is not paid.
- Narrow-task route:
  - user pays through command set, spelling, registration, gestures, and sometimes hardware;
  - device cost can stay manageable.
- Silent-reconstruction route:
  - model and device pay heavily;
  - external guidance, speech priors, sensor stability, and latency become major costs.
- Patient-restoration route:
  - social value is highest;
  - burden is hardest to move away from the user and device;
  - direct evidence remains thin.
- Brain-signal route:
  - equipment and research side pay very heavily;
  - everyday use remains distant.

Final reading procedure:

1. Decide the route.
2. Identify the output: text, speech, command, spelling, or low-volume speech.
3. Identify which stop condition was removed: vocabulary, unseen speaker, remount, real time, real environment, patient evidence.
4. Identify who pays the cost: user, device, model, environment, or surrounding speech system.
5. Ask what remains when external support is weakened.

Final view:

- A strong SSI paper is not simply one with high numbers.
- A strong SSI paper removes at least one real stop condition and makes the cost of that removal readable.

## 7. Complete View Catalog

### A. Initial Cross-Bundle Views

#### A01. Inputs before full silence

Meaning:

- Treat whispered, low-volume, lip-command, smartphone-acoustic, nasal-pad, and spelling systems as important practical SSI-adjacent routes.

Use:

- Avoid discarding useful systems just because they are not perfectly silent.

Risk:

- Do not mislabel low-volume or whispered systems as proof of fully silent SSI.

#### A02. Narrow task as practical progress

Meaning:

- Commands, fixed phrases, spelling, and keyword spotting may be nearer to use than open-vocabulary conversation.

Use:

- Read high scores together with vocabulary and task size.

Risk:

- Do not treat 30-command accuracy as free-conversation progress.

#### A03. Speaker dependence

Meaning:

- Because SSI reads body signals, speaker-specific and user-specific adaptation remain central.

Use:

- Always check speaker-dependent, seen-speaker, unseen-speaker, cross-session, cross-subject, and remount conditions.

Risk:

- Do not generalize within-speaker scores to new users.

#### A04. Speech-mode difference

Meaning:

- Silent speech, whispered speech, normal speech, vocalized speech, mimed speech, and post-laryngectomy speech are not interchangeable.

Use:

- Check whether training and testing use matched modes.

Risk:

- Do not assume vocalized training transfers cleanly to silent use.

#### A05. Sensor placement

Meaning:

- Electrode location, probe fixation, camera angle, nasal pad, radar geometry, and oral hardware can dominate model performance.

Use:

- Treat sensor reproducibility as part of the method, not as a setup detail.

Risk:

- Do not assume lab placement can be reproduced in daily use.

#### A06. Borrowed speech knowledge

Meaning:

- Modern systems increasingly use HuBERT, AV-HuBERT, wav2vec2, speech units, lip-readers, ASR guidance, TTS, vocoders, and speaker embeddings.

Use:

- Separate what the body signal provides from what the speech model fills in.

Risk:

- Do not confuse natural generated speech with correct decoding.

#### A07. Output type split

Meaning:

- Text recognition, speech restoration, command recognition, spelling, speech enhancement, and synchronized TTS are different tasks.

Use:

- Compare WER, CER, PESQ, STOI, MOS, success rate, latency, and wpm only within task context.

Risk:

- Do not equate naturalness with communication accuracy.

#### A08. Metric purpose

Meaning:

- Metrics often measure acoustic similarity or classification, not successful communication.

Use:

- Prefer metrics tied to the intended communication act.

Risk:

- Do not overread MSE, PESQ, or MOS as usability.

#### A09. Operating conditions over headline scores

Meaning:

- Real-time operation, mobility, registration, retraining, correction, noise, lighting, motion, and power determine practical closeness.

Use:

- Rank systems by use conditions, not only benchmark numbers.

Risk:

- Do not call a high-offline-score system practical without operating evidence.

#### A10. Patient value evidence

Meaning:

- Medical or assistive value is the strongest social motivation, but direct patient evidence remains limited.

Use:

- Separate healthy-subject silent imitation from clinical restoration.

Risk:

- Do not treat healthy-subject results as patient results.

#### A11. Neighboring research as parts

Meaning:

- Foley, enhancement, separation, audio-visual segmentation, environmental sound, and dead-air detection may supply parts, but are not SSI evidence by themselves.

Use:

- Classify each source as SSI core, low-volume adjacent, generation part, evaluation part, or outside SSI.

Risk:

- Do not include papers as SSI just because they contain "silent", "audio-visual", or "speech".

#### A12. Failure conditions as value

Meaning:

- Papers that expose unseen-speaker, cross-session, silent-mode, field, ablation, or negative-control failures can be more useful than papers that only show high scores.

Use:

- Preserve failures during compression.

Risk:

- Do not discard weak-number studies if they reveal where the field breaks.

### B. Field Map Views

#### B01. Input modality map

Categories:

- lip and face video;
- ultrasound tongue imaging;
- sEMG and facial EMG;
- EPG and oral sensors;
- smartphone acoustics, nasal pad, whisper, low-volume input;
- radar and contactless sensing;
- EEG, MEG, ECoG, rtMRI.

Main use:

- Quickly place each work by what it can observe and what it cannot observe.

#### B02. Output map

Categories:

- text;
- restored speech;
- command;
- spelling;
- synchronized TTS, voice-over, Foley, or enhancement component.

Main use:

- Prevent unfair comparisons across incompatible objectives.

#### B03. Evaluation-strength map

Strong evidence:

- unseen speaker;
- cross-session;
- silent-only;
- real-time;
- live user task;
- latency;
- wpm;
- field condition;
- ablation.

Medium evidence:

- held-out sentences;
- objective metrics;
- MOS;
- benchmark WER.

Weak evidence:

- single speaker;
- closed set;
- random split;
- MSE only;
- qualitative demo only;
- synthetic noise only.

#### B04. Practical-closeness map

Nearer:

- LipLearner;
- SilentSpeller;
- NasoVoce;
- WESPER;
- smartphone acoustic SSI.

Conditionally near:

- SottoVoce;
- sEMG speech restoration;
- multi-view or large-scale visual-to-speech;
- ultrasound adaptation.

Research-stage:

- single-speaker ultrasound regression;
- EMG speaker-dependent restoration;
- TaL-style speaker-independent research;
- large-scale visual speech research.

Distant:

- EEG or MEG imagined speech;
- rtMRI;
- general-use ECoG;
- Foley and non-SSI audio separation.

#### B05. Research-strength map

Strong core:

- TaL family;
- Digital Voicing;
- SilentSpeller;
- LipLearner;
- SottoVoce;
- SVTS;
- LipVoicer;
- AKVSR;
- Brain2Char;
- ultrasound STN adaptation.

Strong adjacent:

- WESPER;
- NasoVoce;
- audio-visual enhancement and separation;
- target speech extraction;
- JNDQ.

Weak but informative:

- EEG continuous SSR;
- MEG imagined speech;
- early radar;
- textile strain sensors.

Weak as SSI evidence:

- Foley;
- music separation;
- environmental sound;
- telephony dead-air;
- relay power control.

### C. Loop-Derived Views

#### C01. Communication-readiness view

Question:

- Can this actually communicate intent today?

Keeps:

- task size;
- live use;
- latency;
- correction;
- real user setting;
- whether the output can drive an actual service.

Main warning:

- High acoustic naturalness is not communication success.

#### C02. Burden-payer view

Question:

- Who pays for the performance?

Payers:

- user;
- device;
- training data;
- environment;
- external model;
- task limitation.

Main warning:

- Performance numbers often hide the payer.

#### C03. Repair-stage view

Question:

- At which stage is missing information repaired?

Stages:

- acquisition;
- speech-mode adaptation;
- decoding freedom;
- handoff and correction.

Main warning:

- Fixing one stage does not prove full communication.

#### C04. Error-correction actor view

Question:

- Who corrects errors, and when?

Actors:

- preprocessing or device;
- model;
- external model;
- user;
- existing service;
- conversation partner.

Main warning:

- A corrected result is not the same as a directly decoded result.

#### C05. Dependency view

Question:

- What must be borrowed for the result to exist?

Dependencies:

- narrow task;
- personal training;
- fixed placement;
- speech or text prior;
- paired data;
- low-volume input.

Main warning:

- The heaviest dependency often determines deployment difficulty.

#### C06. Durability view

Question:

- What breaks after time passes?

Break points:

- remount;
- retraining;
- fatigue;
- new vocabulary;
- new environment;
- power;
- hygiene;
- sensor shift.

Main warning:

- Same-session success is not long-term usability.

#### C07. Recovery view

Question:

- After failure, how does communication resume?

Recovery forms:

- re-enrollment;
- active learning;
- edit gesture;
- spelling correction;
- confidence and reject;
- fallback to low-volume or whisper;
- handoff to existing ASR.

Main warning:

- A high-score system without recovery can be brittle.

#### C08. Stop-condition view

Question:

- What condition stops communication?

Stop conditions:

- open vocabulary;
- speech-mode mismatch;
- unseen speaker;
- remount;
- real time;
- real environment;
- lightweight wearability;
- patient evidence.

Main warning:

- A system can be strong on one stop condition and weak on another.

#### C09. Route view

Question:

- Which route is this work on?

Routes:

1. low-volume input into existing speech systems;
2. command, spelling, or short controlled input;
3. silent video or articulation to speech or text;
4. patient or voice-loss restoration;
5. brain-signal or basic-research route.

Main warning:

- Do not rank all routes on one line.

#### C10. Route-burden view

Question:

- For each route, who pays the remaining cost?

Route costs:

- low-volume: surrounding speech systems pay, full silence is sacrificed;
- narrow task: user pays through command limits, spelling, registration, gestures;
- silent reconstruction: model and device pay heavily;
- patient restoration: user and device burden remain high, direct evidence is thin;
- brain signal: equipment and research side pay heavily.

Main warning:

- Route choice changes the meaning of every metric.

#### C11. Final individual-paper reading procedure

Procedure:

1. Identify the route.
2. Identify the output type.
3. Identify the stop condition removed.
4. Identify who pays for removing it.
5. Ask what remains when external support is weakened.

Main warning:

- The most important claim is not "score improved"; it is "this real stop condition was removed at this cost."

### D. Route Catalog

#### D01. Low-volume route

Examples:

- NasoVoce;
- WESPER.

Strength:

- closer to existing ASR/TTS and real-time use.

Cost:

- not fully silent.

Key question:

- Is the practical privacy gain enough if full silence is not achieved?

#### D02. Narrow-task route

Examples:

- LipLearner;
- SilentSpeller;
- IR-UWB radar command or phrase sets;
- textile strain sensor style classification.

Strength:

- near-term reliability.

Cost:

- limited vocabulary, user training, spelling, gestures, or hardware.

Key question:

- Which constrained task is valuable enough to justify the constraint?

#### D03. Silent reconstruction route

Examples:

- TaL;
- TaL80;
- AKVSR;
- LipVoicer;
- SottoVoce;
- ultrasound reconstruction;
- sEMG restoration.

Strength:

- closest to the dream of silent articulation becoming speech or text.

Cost:

- external guidance, model burden, sensor burden, speech-mode mismatch, latency.

Key question:

- What remains when guidance, paired audio, or strong speech priors are removed?

#### D04. Patient-restoration route

Examples:

- Cross-modal masking with laryngectomized subjects;
- SottoVoce as assistive direction;
- Brain2Char as a possible severe-case direction.

Strength:

- highest social value.

Cost:

- patient evidence is small, adaptation is hard, equipment burden is high.

Key question:

- What works for actual target users, repeatedly, at home or in clinic?

#### D05. Brain-signal route

Examples:

- JapanEEG;
- MEG imagined speech;
- EEG continuous silent speech recognition;
- Brain2Char;
- ECoG work.

Strength:

- scientifically important and relevant to severe paralysis or future restoration.

Cost:

- low current decoding reliability, heavy equipment, poor generalization, or invasiveness.

Key question:

- Can noninvasive or minimally invasive systems reach communication usefulness, not only signal detection?

## 8. What the View Became by the End

The final view can be stated compactly:

SSI should be read as the design of a communication route under missing speech information.

For each paper, ask:

- What route is it on?
- What is the output?
- What stops communication in this route?
- Which stop condition did the paper remove?
- What cost was paid?
- Who paid it?
- Does the result still hold when external support is weakened?
- Is the evidence from healthy-subject lab data or actual target users?
- Is there recovery after error?
- Is there long-term or repeated-use evidence?

Final judgment rule:

- A strong SSI paper is not merely a paper with high numbers.
- It is a paper that removes a real communication stop condition and makes the cost of that removal visible.

## 9. Remaining Weaknesses

Known weaknesses of this distillation:

- It used compressed expert-review records, not all full papers.
- It did not recheck every original protocol, table, audio sample, or statistic.
- It did not search for newer follow-up work during the 10-loop run.
- Some source records were SSI-adjacent rather than core SSI.
- The loop compression did not always reach 20% of review tokens.
- Some classifications, such as practical closeness and research strength, are judgment calls from the compressed bundle, not official rankings.

What should be done next if this process is rerun:

- Use full PDFs or full-text where possible.
- Keep the same final reading procedure.
- Add a source-level audit for each claim.
- Mark every study by route, output, stop condition, payer, patient evidence, and recovery mechanism.
- Re-read key papers such as SottoVoce using the final procedure.
- Compare whether the final procedure produces better expert judgment than a normal single-pass summary.
