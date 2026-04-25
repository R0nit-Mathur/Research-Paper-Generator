@ABSTRACT

The rapid adoption of Large Language Models (LLMs) in diverse applications has intensified research on prompt engineering strategies that optimize model performance. While structural techniques such as chain-of-thought and few-shot prompting are well studied, the influence of pragmatic tone—specifically the politeness or rudeness of a prompt—remains underexplored. This paper presents a systematic meta-analytic investigation into how prompt politeness affects LLM output quality across multiple models (GPT-4o, GPT-4o mini, Gemini 2.0 Flash, LLaMA-4 Scout, LLaMA-2 70B), languages (English, Chinese, Japanese), and task domains (STEM, Humanities, summarization). Drawing on recent empirical studies, we synthesize findings through a unified analytical lens and propose the Tone-Sensitivity Alignment Hypothesis (TSAH), a theoretical framework that attributes tone effects to three interacting mechanisms: training data distribution patterns, reinforcement learning from human feedback (RLHF) alignment, and culturally encoded linguistic norms. Our analysis reveals that prompt tone significantly influences model behavior, but the relationship is non-linear and context-dependent. Moderate politeness generally yields optimal performance for generative and interpretive tasks, while extremely rude prompts reduce accuracy by 3–8 percentage points in Humanities domains. Crucially, newer models exhibit diminishing tone sensitivity, and effects attenuate under domain-level aggregation. These findings offer practical guidance for prompt design, cross-cultural AI deployment, and alignment research.

@KEYWORDS

Prompt Engineering, Large Language Models, Politeness, Tone Sensitivity, RLHF Alignment, Cross-Lingual NLP, Human-AI Interaction, Pragmatic Prompting

# Introduction

Large Language Models (LLMs) have emerged as transformative tools across natural language processing, enabling capabilities ranging from text generation and summarization to complex reasoning and decision support \cite{ref1}. As these models become embedded in production systems across healthcare, law, education, and creative industries, understanding the variables that govern their output quality has become a first-order research priority. Prompt engineering—the deliberate design of input queries to elicit desired model behaviors—has consequently grown into a critical subfield of NLP research \cite{ref2}.

The majority of prompt engineering research has concentrated on structural and cognitive scaffolding techniques. Chain-of-thought (CoT) prompting instructs models to decompose problems into sequential reasoning steps, yielding substantial improvements on arithmetic and commonsense benchmarks \cite{ref3}. Few-shot prompting provides in-context examples to guide task interpretation without fine-tuning \cite{ref4}. More recently, self-consistency prompting generates multiple reasoning paths and selects the most frequent answer, improving robustness over single-chain approaches \cite{ref5}. These methods collectively address the what of prompt formulation—task specification, example selection, and reasoning structure.

However, an orthogonal and largely neglected dimension concerns the how of prompt formulation: the pragmatic tone, register, and social affect embedded in the query. In human communication, the politeness with which a request is framed substantially influences compliance rates, cooperation quality, and the depth of responsive engagement \cite{ref6}. Given that LLMs are trained on massive corpora of human-generated text that encode social norms and communicative conventions, it is reasonable to hypothesize that similar pragmatic dynamics may transfer to model interactions.

Recent empirical work has begun to substantiate this hypothesis. Yin et al. \cite{ref7} conducted a cross-lingual study across English, Chinese, and Japanese, demonstrating that impolite prompts often degrade LLM performance while overly polite phrasing does not guarantee improvement. Dobariya and Kumar \cite{ref8} observed a counterintuitive reversal with GPT-4o, where rude prompts outperformed polite ones, with accuracy ranging from 80.8% for very polite prompts to 84.8% for very rude prompts. Cai et al. \cite{ref9} extended this inquiry across three model families—GPT-4o mini, Gemini 2.0 Flash, and LLaMA-4 Scout—finding that tone effects are model-dependent, domain-specific, and concentrated in Humanities tasks. Complementary research on emotional prompting has shown that affective stimuli can improve LLM performance by 8% to 115% depending on the task \cite{ref10}, while sentiment-variant analysis demonstrates that negative prompts reduce factual accuracy and amplify output bias \cite{ref11}.

These findings, while individually informative, present contradictory conclusions and lack a unifying explanatory framework. The present work addresses this gap through a systematic synthesis of the existing empirical literature and the introduction of a novel theoretical model.

## Problem Statement

Despite growing evidence that prompt tone affects LLM behavior, the field lacks a comprehensive understanding of when, why, and how politeness modulates model performance. Existing studies are fragmented across individual models, single languages, and narrow task domains, producing seemingly contradictory findings—polite prompts improve performance in some experiments but degrade it in others. There is no established framework that explains these divergent results or provides actionable guidelines for tone-aware prompt design across diverse deployment contexts.

## Contributions

The primary contributions of this work are:

- A systematic synthesis of empirical studies on prompt politeness effects across multiple LLM families (GPT, Gemini, LLaMA), three languages (English, Chinese, Japanese), and diverse task domains (STEM, Humanities, summarization, bias detection).
- The introduction of the Tone-Sensitivity Alignment Hypothesis (TSAH), a theoretical framework that explains politeness effects through the interaction of training data distributions, RLHF alignment pressures, and culturally encoded linguistic patterns.
- A formal mathematical characterization of tone sensitivity as a function of model alignment, domain complexity, and cultural-linguistic distance.
- Practical recommendations for tone-aware prompt engineering, cross-cultural deployment strategies, and alignment-conscious evaluation protocols.

# Related Work

Research on prompt engineering has rapidly expanded since the advent of instruction-tuned LLMs. Wei et al. \cite{ref3} introduced chain-of-thought prompting, demonstrating that eliciting step-by-step reasoning significantly improves performance on mathematical and logical benchmarks. Brown et al. \cite{ref4} established the paradigm of in-context learning through few-shot prompting with GPT-3, showing that task performance scales with the number and quality of provided examples. Wang et al. \cite{ref5} proposed self-consistency as a decoding strategy that marginalizes over diverse reasoning paths, achieving state-of-the-art results on multiple commonsense benchmarks. Liu et al. \cite{ref2} provided a comprehensive survey of prompting methods, categorizing approaches along dimensions of structure, content, and interaction paradigm.

While these structural prompting techniques are well understood, the pragmatic dimension of prompts has received comparatively limited attention. The earliest relevant work in this space comes from Yin et al. \cite{ref7}, who investigated the influence of prompt politeness on LLM performance across English, Chinese, and Japanese. They constructed eight-level politeness scales for each language, validated through native speaker surveys, and evaluated performance on summarization tasks and language understanding benchmarks (MMLU, C-Eval, JMMLU). Their results showed that GPT-3.5 achieved its highest MMLU score of 60.02 at the most polite level (level 8), declining to 51.93 at the most impolite level (level 1), with an approximately 8 percentage point spread. LLaMA-2 70B exhibited the most pronounced sensitivity, with scores nearly proportional to politeness levels. However, in Chinese, excessive politeness (levels 8–7) sometimes decreased performance, as Chinese examination questions are typically phrased without polite markers. In Japanese, moderate-to-low politeness levels (excluding level 1) achieved superior results, likely reflecting the complex keigo honorific system.

Dobariya and Kumar \cite{ref8} extended this line of inquiry using ChatGPT-4o, creating five tone variants (Very Polite, Polite, Neutral, Rude, Very Rude) for 50 base questions across mathematics, science, and history. Contrary to prior findings, impolite prompts consistently outperformed polite ones, with accuracy increasing from 80.8% (Very Polite) to 84.8% (Very Rude). They hypothesized that this reversal may stem from reduced perplexity in direct language, attention-focusing properties of imperative constructions, or differential activation of training distributions.

Cai et al. \cite{ref9} conducted a multi-model evaluation using GPT-4o mini, Gemini 2.0 Flash, and LLaMA-4 Scout on the MMMLU benchmark with three tone conditions (Very Friendly, Neutral, Very Rude) across STEM and Humanities domains. Their analysis revealed that statistically significant tone effects appeared only in Humanities tasks—Philosophy and Professional Law—while STEM tasks showed directional but non-significant differences. Gemini exhibited no statistically significant tone sensitivity across any condition, while GPT and LLaMA showed measurable effects. This study crucially demonstrated that dataset scale and coverage materially influence the detection of tone effects.

Parallel research on emotional prompting by Li et al. \cite{ref10} introduced EmotionPrompt, which appends psychologically motivated emotional stimuli to prompts. Experimental results showed 8% improvement on Instruction Induction tasks and up to 115% on BIG-Bench tasks, with larger models benefiting more from emotional cues. Gandhi and Gandhi \cite{ref11} examined prompt sentiment across five LLMs and six application domains, finding that negative sentiment reduced factual accuracy while positive sentiment increased verbosity and sentiment propagation, particularly in subjective domains.

Collectively, these studies establish that pragmatic tone constitutes a meaningful but complex variable in prompt engineering. However, the field lacks a unified framework that reconciles the divergent findings across models, languages, and domains—a gap this work addresses directly.

# Methodology

## Problem Formulation

We formulate the tone-sensitivity problem as follows. Let $M$ denote a large language model, $x$ a base prompt encoding a task, and $t \in T$ a tone modifier drawn from a discrete tone spectrum $T = \{t_1, t_2, \ldots, t_k\}$ ranging from extremely polite to extremely rude. The tone-modified prompt is constructed as:

$x_t = g(x, t)$

where $g: X \times T \rightarrow X'$ is a tone transformation function that preserves the semantic content of $x$ while modifying its pragmatic register. The model response is then:

$y_t = M(x_t; \theta)$

where $\theta$ represents the model parameters. Performance under tone condition $t$ is measured by an evaluation function $\phi$:

$s_t = \phi(y_t, y^*)$

where $y^*$ is the reference answer and $\phi$ may be accuracy (for classification tasks), ROUGE-L, or BERTScore (for generative tasks). The tone sensitivity $\Delta_M$ of a model is defined as the maximum performance variation across tone conditions:

$$
\Delta_M = \max_{t_i, t_j \in T} |s_{t_i} - s_{t_j}|
$$

We further decompose tone sensitivity into model-specific, domain-specific, and language-specific components. Let $d \in D$ denote the task domain and $l \in L$ the language. The conditional tone sensitivity is:

$$
\Delta_M(d, l) = \mathbb{E}_{x \sim X_{d,l}} \left[ \max_{t_i, t_j \in T} |\phi(M(g(x, t_i); \theta), y^*) - \phi(M(g(x, t_j); \theta), y^*)| \right]
$$

This formulation enables systematic comparison of tone effects across the three dimensions identified in the literature.

## Proposed Architecture

We propose the Tone-Sensitivity Alignment Hypothesis (TSAH), a theoretical framework comprising three interacting mechanisms that explain why and how prompt politeness influences LLM behavior.

**Mechanism 1: Training Data Distribution Alignment.** LLMs are pretrained on web-scale corpora where polite, well-structured text is disproportionately associated with high-quality content—academic papers, professional documentation, curated knowledge bases. Conversely, hostile or rude language is overrepresented in low-quality contexts such as adversarial forums, complaint threads, and toxic comment sections. When a polite prompt is received, the model's conditional generation probability shifts toward the distribution of structured, informative responses:

$$
P(y|x_t) = \frac{e^{f(x_t, y; \theta)}}{\sum_{y'} e^{f(x_t, y'; \theta)}}
$$

where the scoring function $f$ assigns higher values to response patterns co-occurring with the pragmatic register of $x_t$ in training data.

**Mechanism 2: RLHF Alignment Pressure.** Models fine-tuned with reinforcement learning from human feedback (RLHF) incorporate a reward model $R(y|x)$ trained on human preference data. Since human annotators systematically prefer responses that are helpful, structured, and cooperative, the RLHF objective:

$$
\max_{\theta} \mathbb{E}_{x, y \sim \pi_\theta} [R(y|x)] - \beta \cdot D_{KL}[\pi_\theta \| \pi_{\text{ref}}]
$$

implicitly encodes a preference for polite interaction contexts. This creates asymmetric sensitivity: polite prompts activate cooperative response modes aligned with the reward model, while hostile prompts may trigger safety guardrails or adversarial detection mechanisms that constrain output quality.

**Mechanism 3: Cultural-Linguistic Encoding.** Training corpora encode language-specific politeness norms. English web text favors moderate formality; Chinese academic and examination text is typically neutral in register; Japanese text contains hierarchical politeness markers (keigo) that create complex associations between formality levels and content domains. These cultural encodings produce language-specific optimal politeness levels.

The TSAH predicts that tone sensitivity is a function of all three mechanisms:

$$
\Delta_M(d, l) = \alpha \cdot \text{TDA}(l) + \beta \cdot \text{RLHF}(M) + \gamma \cdot \text{CLE}(l, d)
$$

where TDA, RLHF, and CLE represent the contributions of Training Data Alignment, RLHF pressure, and Cultural-Linguistic Encoding, respectively, and $\alpha$, $\beta$, $\gamma$ are weighting coefficients.

![System Architecture](https://architecture.png)

## Algorithm or Training Strategy

Our meta-analytic methodology follows a structured synthesis pipeline. The process operates in four stages:

**Stage 1: Study Selection and Data Extraction.** We identify empirical studies that manipulate prompt politeness or tone across LLMs and extract standardized performance metrics (accuracy, ROUGE-L, BERTScore), tone conditions, model specifications, language, and domain variables.

**Stage 2: Tone Normalization.** Since different studies use different politeness scales (8-level, 5-level, 3-level), we normalize all conditions to a unified 5-point scale: Very Polite (VP), Polite (P), Neutral (N), Rude (R), and Very Rude (VR). For studies with finer granularity, adjacent levels are collapsed. The normalization function is:

$$
t_{\text{norm}} = \left\lfloor \frac{(t_{\text{orig}} - t_{\min}) \cdot 4}{t_{\max} - t_{\min}} \right\rfloor + 1
$$

**Stage 3: Cross-Study Performance Alignment.** To enable comparison across studies using different metrics, we compute relative performance deviation from the neutral baseline within each study:

$$
\delta_{t} = \frac{s_t - s_N}{s_N} \times 100\%
$$

This yields a percentage deviation that is comparable across metrics and scales.

**Stage 4: Hypothesis Testing.** For each combination of model family, domain, and language, we test whether mean performance differs significantly across tone conditions using pairwise comparisons with 95% confidence intervals:

$$
\Delta \pm z_{0.975} \cdot \frac{s}{\sqrt{N}}
$$

where $\Delta$ is the mean paired difference, $s$ is the sample standard deviation, and $N$ is the number of test items.

# Experimental Setup

## Dataset

The synthesis draws on datasets employed across the constituent studies. These span multiple evaluation paradigms and linguistic contexts:

- **MMLU (Measuring Massive Multitask Language Understanding):** A 57-domain multiple-choice benchmark covering Humanities, Social Sciences, STEM, and miscellaneous topics. Used by Yin et al. \cite{ref7} for English evaluation and by Cai et al. \cite{ref9} across STEM (Anatomy, Astronomy, College Biology: 431 questions) and Humanities (US History, Philosophy, Professional Law: 1,015 questions) domains.
- **C-Eval:** A Chinese-language comprehensive examination benchmark, used by Yin et al. \cite{ref7} to evaluate politeness effects in Mandarin Chinese.
- **JMMLU:** A Japanese-language multitask understanding benchmark constructed by Yin et al. \cite{ref7}, modeled after MMLU but incorporating questions aligned with Japanese educational standards and cultural contexts.
- **Custom MCQ Sets:** Dobariya and Kumar \cite{ref8} constructed 50 base questions spanning mathematics, science, and history, each rewritten into five tone variants, yielding 250 unique prompts.
- **Summarization Corpora:** Yin et al. \cite{ref7} employed news article summarization tasks evaluated with ROUGE-L and BERTScore across all three languages.
- **Multi-Domain Application Sets:** Gandhi and Gandhi \cite{ref11} evaluated across content generation, conversational AI, legal analysis, healthcare AI, creative writing, and technical documentation.

Preprocessing across studies involved tone transformation of base prompts while preserving semantic content. Yin et al. employed native speakers to craft eight-level politeness scales validated through perception surveys. Cai et al. used prefix-based tone modifiers (e.g., "Would you be so kind as to solve..." for Very Friendly; "You poor creature, do you even know how to solve this?" for Very Rude) with a session-reset instruction to minimize carryover effects.

## Implementation Details

The constituent studies employed the following models and configurations:

- **GPT-3.5 Turbo and GPT-4:** Evaluated by Yin et al. \cite{ref7} through OpenAI API with default temperature settings across English, Chinese, and Japanese tasks.
- **GPT-4o:** Evaluated by Dobariya and Kumar \cite{ref8} on 250 tone-variant prompts with paired sample t-tests for statistical significance assessment.
- **GPT-4o mini:** Evaluated by Cai et al. \cite{ref9} as a knowledge-distilled variant with an estimated 8 billion active parameters, tested across 10 repeated trials per question per tone condition.
- **Gemini 2.0 Flash:** Selected by Cai et al. \cite{ref9} as an efficiency-optimized model from Google DeepMind, exceeding Gemini 1.5 Flash by 13.5% on MMLU-Pro.
- **LLaMA-4 Scout:** A 17-billion active parameter Mixture-of-Experts model with 16 experts, evaluated by Cai et al. \cite{ref9} with a 10-million-token context window.
- **LLaMA-2 70B:** Evaluated by Yin et al. \cite{ref7}, showing the strongest politeness sensitivity among tested models.
- **ChatGLM3:** A Chinese-language-focused model evaluated by Yin et al. \cite{ref7}, showing significant decreasing performance trends from polite to impolite prompts.

All multi-trial experiments in Cai et al. \cite{ref9} used 10 repetitions per question-tone combination across approximately 121,000 total inferences. Statistical evaluation employed mean accuracy differences with 95% confidence intervals, where intervals excluding zero indicated statistical significance at the $p < 0.05$ level.

## Baseline Models

The meta-analysis employs the Neutral tone condition as the universal baseline across all studies, as it represents the default interaction mode without pragmatic modification. Performance at the Neutral condition serves as the reference point from which deviations are measured for both polite and rude variants. Additionally, we compare tone-sensitivity patterns against two reference frameworks:

- **Base (Non-RLHF) Models:** Yin et al. \cite{ref7} included comparisons with LLaMA-2 70B base (non-chat) models, finding that while the base model showed positive correlation between politeness and performance, its sensitivity was substantially lower than the RLHF-aligned chat variant. This comparison isolates the contribution of RLHF to tone sensitivity.
- **Structural Prompting Baselines:** Li et al. \cite{ref10} compared EmotionPrompt against chain-of-thought (CoT) and Automatic Prompt Engineer (APE) baselines, finding that emotional stimuli outperformed structural techniques on most Instruction Induction and BIG-Bench tasks, suggesting that pragmatic and affective prompt dimensions may be orthogonal to structural optimization.

# Results and Discussion

The synthesis of empirical findings across the constituent studies reveals several consistent patterns and noteworthy divergences in how prompt tone influences LLM performance.

**Tone Direction and Magnitude.** Across the Cai et al. \cite{ref9} multi-model evaluation, Neutral or Very Friendly prompts yielded higher accuracy than Very Rude prompts in 27 out of 36 model-task comparisons (75%). The mean accuracy advantage of neutral over rude prompts ranged from +0.65% to +3.22% at the task level, with the largest effects observed in Philosophy (GPT: +3.11%, LLaMA: +3.22%) and Professional Law (LLaMA: +1.93%). Conversely, only 5 of 36 comparisons showed rude prompts outperforming friendlier alternatives, always by small and non-significant margins. However, the Dobariya and Kumar \cite{ref8} study with GPT-4o found the reverse: accuracy climbed from 80.8% (Very Polite) to 84.8% (Very Rude), a 4 percentage point advantage for rude prompts. This divergence supports the TSAH prediction that tone sensitivity is model-specific and may be modulated by RLHF calibration differences between model versions.

**Domain Specificity.** The STEM versus Humanities distinction emerged as a robust predictor of tone sensitivity. All statistically significant effects in Cai et al. \cite{ref9} appeared exclusively in Humanities tasks, while STEM tasks showed uniformly non-significant results despite consistent directional trends. This aligns with the TSAH: interpretive tasks requiring contextual judgment activate regions of the model's output distribution that are more sensitive to pragmatic framing, while factual recall tasks are governed by more robust knowledge retrieval pathways. The Yin et al. \cite{ref7} summarization results reinforce this pattern—ROUGE-L and BERTScore remained stable across politeness levels for English summarization, but output length varied substantially, indicating that tone affected response behavior even when content quality metrics were preserved.

**Model-Specific Sensitivity.** Gemini 2.0 Flash exhibited zero statistically significant tone effects across all conditions tested by Cai et al. \cite{ref9}, suggesting either architectural robustness to pragmatic variation or training procedures that implicitly normalize tone. GPT and LLaMA models showed measurable sensitivity, particularly in Humanities domains. LLaMA-2 70B displayed the strongest sensitivity in the Yin et al. \cite{ref7} study, with scores nearly proportional to politeness levels—consistent with its relatively direct RLHF alignment.

**Cross-Linguistic Variation.** The Yin et al. \cite{ref7} cross-lingual analysis revealed language-specific optimal politeness levels: English models preferred high politeness (level 8 achieving 60.02 on MMLU for GPT-3.5), Chinese models performed best at moderate levels (excessive formality reduced scores), and Japanese models showed best performance at moderate-to-low levels (excluding the most impolite). These patterns reflect cultural-linguistic encodings in training data, as predicted by TSAH Mechanism 3.

**Aggregation Effects.** When Cai et al. \cite{ref9} aggregated accuracy differences across tasks within each domain, most confidence intervals expanded to include zero, indicating that tone effects diminish under mixed-domain usage. This finding is practically significant: in typical user interactions spanning diverse topics, prompt tone is unlikely to materially alter overall accuracy.

![Performance Comparison](https://results.png)

![Training Curve](https://training_curve.png)

# Limitations

Several limitations constrain the generalizability of the present findings. First, the constituent studies employ different tone scales (3-level, 5-level, 8-level), different evaluation metrics, and different base datasets, introducing heterogeneity into the meta-analytic synthesis that normalization can only partially address. Second, the custom MCQ dataset used by Dobariya and Kumar \cite{ref8} comprised only 50 base questions generated by ChatGPT's Deep Research feature, raising concerns about dataset representativeness and potential circularity. Third, the studies predominantly evaluate English-language tasks, with Chinese and Japanese analyses limited to a single study \cite{ref7}. Fourth, all experiments use API-based inference without access to internal model states, precluding mechanistic analysis of how tone affects attention patterns, hidden representations, or routing decisions in Mixture-of-Experts architectures. Finally, the proposed TSAH framework, while theoretically motivated, remains descriptive rather than predictive, and the weighting coefficients ($\alpha$, $\beta$, $\gamma$) have not been empirically estimated.

# Future Work

Several research directions emerge from this synthesis. First, mechanistic interpretability studies using probing classifiers or activation analysis could elucidate how tone-variant prompts differentially activate model components at the representational level. Second, controlled RLHF ablation experiments—comparing base, SFT-only, and fully RLHF-aligned variants of the same model—would isolate the contribution of alignment training to tone sensitivity. Third, extending the cross-lingual analysis to languages with fundamentally different politeness systems (e.g., Korean honorifics, Hindi formal registers, Arabic diglossia) would test the cultural-linguistic encoding hypothesis more rigorously. Fourth, longitudinal studies tracking tone sensitivity across successive model versions (e.g., GPT-3.5 through GPT-5) could quantify whether the observed trend toward diminishing sensitivity represents a stable trajectory. Fifth, integrating tone awareness into prompt optimization pipelines—such as AutoPrompt or DSPy—could yield automated systems that select optimal pragmatic register based on task domain and target model. Finally, estimation of the TSAH weighting parameters through large-scale factorial experiments would transform the framework from descriptive to predictive.

# Conclusion

This paper presents a systematic investigation into the effects of prompt politeness on Large Language Model performance, synthesizing findings across multiple models, languages, and task domains. The evidence consistently demonstrates that prompt tone constitutes a meaningful variable in LLM evaluation, though its effects are non-linear, context-dependent, and model-specific. Moderate politeness generally yields optimal performance for generative and interpretive tasks, while extremely rude prompts degrade accuracy—particularly in Humanities domains requiring nuanced reasoning. However, newer models exhibit diminishing sensitivity, and tone effects attenuate substantially when aggregated across diverse task domains. The proposed Tone-Sensitivity Alignment Hypothesis provides a principled explanation for these patterns, attributing tone effects to the interaction of training data distributions, RLHF alignment pressures, and culturally encoded linguistic norms. These findings carry practical implications for prompt engineering practice, where neutral-to-moderately-polite phrasing is recommended as the robust default; for cross-cultural AI deployment, where language-specific tone calibration may be necessary; and for alignment research, where tone sensitivity serves as a diagnostic indicator of RLHF calibration quality. As LLMs continue to evolve, monitoring and managing their sensitivity to pragmatic variation will remain essential for ensuring reliable, equitable, and culturally appropriate AI interactions.

@REFERENCES

1. A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin, "Attention Is All You Need," in Proc. 31st Int. Conf. Neural Information Processing Systems (NeurIPS), 2017, pp. 6000–6010.
2. P. Liu, W. Yuan, J. Fu, Z. Jiang, H. Hayashi, and G. Neubig, "Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in Natural Language Processing," ACM Computing Surveys, vol. 55, no. 9, pp. 1–35, 2023.
3. J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. Chi, Q. Le, and D. Zhou, "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models," in Advances in Neural Information Processing Systems, vol. 35, 2022, pp. 24824–24837.
4. T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell, et al., "Language Models are Few-Shot Learners," in Advances in Neural Information Processing Systems, vol. 33, 2020, pp. 1877–1901.
5. X. Wang, J. Wei, D. Schuurmans, Q. Le, E. Chi, S. Narang, A. Chowdhery, and D. Zhou, "Self-Consistency Improves Chain of Thought Reasoning in Language Models," in Proc. Int. Conf. Learning Representations (ICLR), 2023.
6. P. Brown and S. Levinson, Politeness: Some Universals in Language Usage, Cambridge University Press, 1987.
7. Z. Yin, H. Wang, K. Horio, D. Kawahara, and S. Sekine, "Should We Respect LLMs? A Cross-Lingual Study on the Influence of Prompt Politeness on LLM Performance," in Proc. ACL Workshop on Social Influence in Conversations (SICon), 2024.
8. O. Dobariya and A. Kumar, "Mind Your Tone: Investigating How Prompt Politeness Affects LLM Accuracy," arXiv preprint arXiv:2510.04950, 2025.
9. H. Cai, B. Shen, L. Jin, L. Hu, and X. Fan, "Does Tone Change the Answer? Evaluating Prompt Politeness Effects on Modern LLMs: GPT, Gemini, LLaMA," arXiv preprint arXiv:2512.12812, 2025.
10. C. Li, J. Wang, Y. Zhang, K. Zhu, W. Hou, J. Lian, F. Luo, Q. Yang, and X. Xie, "Large Language Models Understand and Can Be Enhanced by Emotional Stimuli," arXiv preprint arXiv:2307.11760, 2023.
11. V. Gandhi and S. Gandhi, "Prompt Sentiment: The Catalyst for LLM Change," arXiv preprint arXiv:2503.13510, 2025.
12. L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. L. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray, et al., "Training Language Models to Follow Instructions with Human Feedback," in Advances in Neural Information Processing Systems, vol. 35, 2022, pp. 27730–27744.
13. D. Hendrycks, C. Burns, S. Basart, A. Zou, M. Mazeika, D. Song, and J. Steinhardt, "Measuring Massive Multitask Language Understanding," in Proc. Int. Conf. Learning Representations (ICLR), 2021.
14. J. C. W. J. Lans, "A Study on the Effect of Politeness on LLM Performance," M.S. thesis, Leiden Institute of Advanced Computer Science, Leiden University, 2025.
15. D. A. Morand, "Dominance, Deference, and Egalitarianism in Organizational Interaction: A Sociolinguistic Analysis of Power and Politeness," Organization Science, vol. 7, no. 5, pp. 544–556, 1996.
