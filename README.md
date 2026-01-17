WIP1

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-🟢-brightgreen" alt="Streamlit Badge" />
  <img src="https://img.shields.io/badge/HuggingFace-🤗-yellow" alt="HuggingFace Badge" />
</p>

# DuolingoForAI

> **A free, Duolingo‑style Streamlit app that teaches what tokenization is by letting you type text and instantly see tokens, input IDs, attention masks, and subword splits using a fast Hugging Face tokenizer.**

---

## 🚀 Why this exists
LLMs operate on tokens, not words. Understanding tokenization helps you write better prompts, control costs, and predict model behavior. This app visualizes how text becomes model‑ready inputs—making the invisible visible!

Streamlit makes it easy to ship interactive lessons and demos on the web, for free, with zero setup.

---

## 🎮 What it does
- **Interactive playground:** Type a sentence and instantly visualize tokens, input IDs, attention masks, and optional character offsets/word alignment from fast tokenizers.
- **Mini‑quiz:** “Guess the token count” with instant feedback and a celebratory animation to keep learning fun.
- **Duolingo feel:** Themed UI via `.streamlit/config.toml` with bright colors, rounded cards, and playful micro‑interactions.

---

## 🛠️ Tech stack
- **Streamlit** for UI and state management
- **Hugging Face Transformers** AutoTokenizer (fast) for tokenization and offsets mapping
- **Optional hosting:** Streamlit Community Cloud or Hugging Face Spaces for free, public access

---

## 📁 Project structure
- `app.py` — main Streamlit app. Keep UI logic here and import small helpers if needed.
- `.streamlit/config.toml` — theme (colors, fonts) for a consistent “Duolingo” vibe on local and cloud runs.
- `requirements.txt` — pinned versions for reliable cloud builds.

---

## 🖥️ Local setup
Create a virtual environment, install dependencies, and run locally with hot‑reload:

```sh
python -m venv .venv
# Activate your environment
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

## 🌍 Deploy options
- **Streamlit Community Cloud:** Connect the repo and deploy; manage and view logs from the “Manage app” panel.
- **Hugging Face Spaces:** Add README and config; Spaces reads the repo and builds automatically. Use the README’s YAML header to set title/emoji/thumbnail if desired.

---

## 📦 Requirements (example)
```
streamlit==1.36.0
transformers==4.43.3
tokenizers==0.19.1
torch==2.3.1
huggingface-hub==0.24.6
```
*Pinned versions help avoid cloud‑build incompatibilities.*

---

## 🧑‍💻 How it works (under the hood)
- `AutoTokenizer.from_pretrained("distilbert-base-uncased", use_fast=True)` loads a fast tokenizer with offset mapping.
- The app calls `tokenizer(text, return_offsets_mapping=True, add_special_tokens=True)` and renders:
  - tokens via `convert_ids_to_tokens`
  - input_ids and attention_mask from the BatchEncoding
  - offsets/word_ids (when available) to highlight subword spans in the original text.

---

## 🗺️ Roadmap
- **Lesson 1 (this app):** Tokenization basics and subword intuition.
- **Upcoming lessons:** Transformers basics, sentiment demo, fine‑tuning primer, and RAG walkthrough—all using the same Streamlit + free hosting setup.

---

## 🏅 Badges and Space metadata (optional)
Add a “Duplicate this Space” or “Open in Spaces” badge to the README for easy sharing using the Hugging Face badges set.
Add a YAML header to the README to customize the Space’s title, emoji, and thumbnail.

---

## 🙏 Acknowledgments
Built with Streamlit’s recommended app structure and theming for approachable, production‑friendly GenAI demos.
Tokenization concepts and APIs from Hugging Face Transformers documentation.

---

## 📚 Related
- What specific features should the README explain for our Streamlit GenAI app
- How should we describe the recommended folder structure and utils usage
- Which setup steps and secrets handling must I include for deployment
- Why should we document prompt templates and LLM utility patterns
- How can I show examples of running and testing the app locally
