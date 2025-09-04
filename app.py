import streamlit as st
from transformers import AutoTokenizer

st.set_page_config(page_title="Duolingo-for-Tokenizers", page_icon="🟢", layout="centered")

PRIMARY = "#22c55e"  # bright green
st.markdown(f"""
    <style>
    .stApp {{ background: #0b1220; color: #e5f6ee; }}
    .stButton>button {{ background:{PRIMARY}; color:#032b23; border-radius:14px; font-weight:700; }}
    .stTextArea textarea {{ border-radius:14px; }}
    .lesson-card {{ padding:1rem 1.25rem; border-radius:18px; background:#0f1b2e; border:1px solid #123; }}
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_tokenizer():
    return AutoTokenizer.from_pretrained("distilbert-base-uncased", use_fast=True)

tok = get_tokenizer()

st.title("🟢 Tokenization Lesson 1")
st.caption("Breezy, gamified tokenizer intro — Duolingo style")

with st.container():
    st.markdown("### 🧠 Intro")
    st.markdown('<div class="lesson-card">LLMs read tokens, not words. Type a sentence and peek at subwords and IDs.</div>', unsafe_allow_html=True)

text = st.text_area("Type a sentence", "Transformers learn from tokens, not whole words.", height=120)

c1, c2, c3 = st.columns(3)
with c1: add_special = st.checkbox("Add special tokens", True)
with c2: show_offsets = st.checkbox("Show offsets", True)
with c3: st.write("")

if st.button("Tokenize ▶"):
    enc = tok(text, return_offsets_mapping=show_offsets, add_special_tokens=add_special)
    tokens = tok.convert_ids_to_tokens(enc["input_ids"])
    st.subheader("🧩 Tokens")
    st.code(tokens)
    st.subheader("🔢 Input IDs")
    st.code(enc["input_ids"])
    st.subheader("📶 Attention mask")
    st.code(enc["attention_mask"])

    if show_offsets and "offset_mapping" in enc:
        offsets = enc["offset_mapping"]
        rows = []
        for i, (start, end) in enumerate(offsets):
            span = text[start:end] if start is not None and end is not None else ""
            rows.append({"i": i, "token": tokens[i], "start": start, "end": end, "span": span})
        st.subheader("🧭 Offsets")
        st.dataframe(rows, use_container_width=True)

st.markdown("### 🎯 Mini‑quiz")
quiz_sent = st.text_input("Guess the token count for:", "Subword tokenizers split uncommon words.")
if st.button("Check ✅"):
    count = len(tok(quiz_sent, add_special_tokens=False)["input_ids"])
    guess = st.number_input("Your guess", min_value=1, step=1, value=6, key="guess", help="Enter a number, then click Check again.")
    if guess == count:
        st.success(f"Nice! Exactly {count} tokens.")
        st.balloons()
    else:
        st.warning(f"Close! Actual: {count} tokens. Try another sentence!")
