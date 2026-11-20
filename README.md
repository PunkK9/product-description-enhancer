# Product Description Enhancer

[![Built with askThili](https://msrit.ask.thili.ai/api/v1/public/projects/xckp9ykg2p/badge.svg)](https://msrit.ask.thili.ai/b/xckp9ykg2p)

This project develops a Product Description Enhancer for e-commerce managers. It leverages the LoRA fine-tuning technique to adapt a pre-trained language model, transforming basic product specs into compelling, SEO-optimized descriptions. The tool aims to streamline content creation for online storefronts.

## What you are building

**Goal.** You will build a tool that fine-tunes a language model using LoRA to transform basic product specifications into compelling, SEO-optimized descriptions for online storefronts.

**Done when.** The project is done when the LoRA fine-tuning technique has been successfully applied to adapt a pre-trained LLM, and the Streamlit UI can generate compelling product descriptions after training and merging the adapter.

## Milestones

Tick these off as you go, and commit after each one.

- [x] **1. Compile a small dataset of product specs and marketing descriptions.**  
      Hint: For data collection, focus on pairing short product specs with longer, descriptive marketing texts.
- [x] **2. Implement LoRA adapter injection and training on a pre-trained LLM (e.g., GPT-2).**  
      Hint: Implement LoRA adapter injection and training using the `lfllm-lflora` technique on a pre-trained LLM like GPT-2.
- [x] **3. Develop a Streamlit UI to input product specs and generate enhanced descriptions.**  
      Hint: Use Streamlit components to create input fields for product specs and display the generated descriptions.
- [x] **4. Assess the creativity and relevance of the generated descriptions.**  
      Hint: Manually review the output for coherence, creativity, and relevance to the input specs.
- [x] **5. Implement adapter merging for inference.**  
      Hint: Apply the adapter merging technique from `lfllm-lflora` to prepare the model for efficient inference.

## Run it

You need Python 3.12 and git. Versions are pinned in `requirements.txt`.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
streamlit run app/main.py
pytest
```

On macOS or Linux, activate with `source .venv/bin/activate` and copy settings with `cp .env.example .env`.

The Streamlit page previews a template description immediately. Choosing "Merged LoRA model" downloads GPT-2 and trains the adapter on first use. A recorded comparison of that run is already in `results/evaluation.json` and is shown on the page.

To reproduce the recorded numbers:

```bash
python -m app.record
```

## Data

The pairs live in `milestone_1` inside `app/core.py`. Each row is a short catalogue spec and a longer marketing description written for this project. Nothing is scraped from a store.

## Results

`results/evaluation.json` is one recorded run, and the Streamlit page shows the same file. GPT-2 small, LoRA rank 4 and alpha 16 on each attention `c_attn` layer (147,456 trainable parameters). The adapter trains for 40 steps on the first 8 pairs, then the low-rank update is merged into the base weights (124,439,808 parameters, the same size as GPT-2).

Loss on those 8 pairs, with padding ignored:

| | loss |
| --- | --- |
| Before any LoRA step | 3.35 |
| After 40 steps, eval mode | 1.43 |

Keyword overlap on the first three specs (share of spec words that reappear). Those three specs are inside the eight training pairs.

| generator | keyword overlap | composite |
| --- | --- | --- |
| Template that pastes the spec into a sentence | 1.00 | 0.85 |
| Untouched GPT-2 | 0.22 | 0.49 |
| LoRA, merged | 0.68 | 0.67 |

The template wins keyword overlap because it copies the spec. It is the baseline, not a better writer. Untouched GPT-2, given the headphones spec, talks about an HTC phone. After the merge, the same prompt starts: "Capture your music with the ultimate in wireless Bluetooth headphones. The 40mm drivers deliver crisp, detailed sound..." The chino prompt still collapses into repeated words (`machine-stripping`), so the adapter has not learned every product.

Limits, also listed on the page:

- Only the first 8 of 30 pairs are trained, truncated to 128 tokens. There is no held-out shop catalogue.
- Keyword overlap and the composite score (length, overlap, and whether sentences start differently) are not a shopper's judgment.
- Forty steps are enough for the training specs to move toward the marketing style, and not enough to stop repetition or to cover a spec the adapter never saw.

## Settings and secrets

Model settings live in `.env`, which is ignored by git. **Never commit `.env` or paste a key into code.** If a key ever
reaches GitHub, treat it as leaked and make a new one.

## Stretch ideas

- Add a feature to the Streamlit UI for users to provide feedback on generated descriptions, allowing for iterative model improvement.
- Explore different pre-trained LLMs beyond GPT-2 to see if they yield better description quality.
- Implement a simple A/B testing framework within the UI to compare descriptions generated by different LoRA adapters or base models.
