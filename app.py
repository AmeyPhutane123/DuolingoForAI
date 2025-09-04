
import streamlit as st

st.set_page_config(page_title="LLM Course - Duolingo Style", page_icon="🎓", layout="wide")

# Custom theme
PRIMARY = "#22c55e"
st.markdown(f"""
    <style>
    .stApp {{ background: #0b1220; color: #e5f6ee; }}
    .stButton>button {{ background:{PRIMARY}; color:#032b23; border-radius:14px; font-weight:700; }}
    .course-card {{ padding:1.5rem 1.5rem; border-radius:22px; background:#16213a; border:2px solid #22c55e; margin-bottom:1.5rem; box-shadow:0 2px 12px #0002; }}
    .author-card {{ background:#0f1b2e; border-radius:14px; padding:1rem; margin-bottom:1rem; border:1px solid #123; }}
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation for 12 topics
topics = [
    "Introduction",
    "Natural Language Processing and Large Language Models",
    "Transformers, what can they do?",
    "How do Transformers work?",
    "How 🤗 Transformers solve tasks",
    "Transformer Architectures",
    "Quick quiz",
    "Inference with LLMs",
    "Bias and limitations",
    "Summary",
    "Certification exam",
    "FAQ"
]

st.sidebar.title("LLM Course Navigation")
selected = st.sidebar.radio("Jump to:", topics)

if selected == "Introduction":
    st.title("🎓 Welcome to the 🤗 LLM Course!")
    st.markdown("""
        <div class="course-card">
        <h3>Ask a Question</h3>
        <p>Welcome to the 🤗 Course!<br>
        This course will teach you about large language models (LLMs) and natural language processing (NLP) using libraries from the Hugging Face ecosystem — 🤗 Transformers, 🤗 Datasets, 🤗 Tokenizers, and 🤗 Accelerate — as well as the Hugging Face Hub.<br><br>
        We’ll also cover libraries outside the Hugging Face ecosystem. These are amazing contributions to the AI community and incredibly useful tools.<br><br>
        <b>It’s completely free and without ads.</b>
        </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        ## Understanding NLP and LLMs
        NLP (Natural Language Processing) is the broader field focused on enabling computers to understand, interpret, and generate human language. NLP encompasses many techniques and tasks such as sentiment analysis, named entity recognition, and machine translation.<br><br>
        LLMs (Large Language Models) are a powerful subset of NLP models characterized by their massive size, extensive training data, and ability to perform a wide range of language tasks with minimal task-specific training. Models like the Llama, GPT, or Claude series are examples of LLMs that have revolutionized what’s possible in NLP.<br><br>
        Throughout this course, you’ll learn about both traditional NLP concepts and cutting-edge LLM techniques, as understanding the foundations of NLP is crucial for working effectively with LLMs.
    """, unsafe_allow_html=True)

    st.markdown("""
        ## What to expect?
        <ul>
        <li>Chapters 1 to 4: Introduction to 🤗 Transformers library, how Transformer models work, using models from the Hugging Face Hub, fine-tuning, and sharing results.</li>
        <li>Chapters 5 to 8: Basics of 🤗 Datasets and 🤗 Tokenizers, classic NLP tasks, and LLM techniques.</li>
        <li>Chapter 9: Building and sharing demos of your models on the 🤗 Hub.</li>
        <li>Chapters 10 to 12: Advanced LLM topics like fine-tuning, curating high-quality datasets, and building reasoning models.</li>
        </ul>
        <b>This course requires good Python knowledge and is best taken after an introductory deep learning course.</b>
    """, unsafe_allow_html=True)

    st.markdown("""
        ## Who are we?
    """)
    st.markdown("""
        <div class="author-card">
        <b>Abubakar Abid</b> — ML Team Lead, Gradio founder, Stanford PhD<br>
        <b>Ben Burtenshaw</b> — ML Engineer, PhD in NLP, Hugging Face<br>
        <b>Matthew Carrigan</b> — ML Engineer, Hugging Face, Dublin<br>
        <b>Lysandre Debut</b> — ML Engineer, 🤗 Transformers core dev<br>
        <b>Sylvain Gugger</b> — Research Engineer, fast.ai co-author<br>
        <b>Dawood Khan</b> — ML Engineer, Gradio co-founder<br>
        <b>Merve Noyan</b> — Developer Advocate, Hugging Face<br>
        <b>Lucile Saulnier</b> — ML Engineer, NLP researcher<br>
        <b>Lewis Tunstall</b> — ML Engineer, O’Reilly author<br>
        <b>Leandro von Werra</b> — ML Engineer, O’Reilly author
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        ## FAQ
        <ul>
        <li><b>Certification?</b> No official certification yet, but it’s coming soon!</li>
        <li><b>Time commitment?</b> Each chapter is designed for 1 week, 6-8 hours/week, but go at your own pace.</li>
        <li><b>Questions?</b> Click the “Ask a question” banner or visit the Hugging Face forums.</li>
        <li><b>Course code?</b> Run code in Colab or SageMaker Studio Lab via the course repo.</li>
        <li><b>Contribute?</b> Open issues, help translate, or improve the course on GitHub.</li>
        <li><b>Languages?</b> Available in many languages thanks to the community!</li>
        </ul>
        <br>
        <b>Let’s go 🚀</b> — Ready to roll? In this chapter, you’ll learn how to use <code>pipeline()</code> for NLP tasks, about Transformer architecture, and more!
    """, unsafe_allow_html=True)

# ...existing code for other topics (add similar structure for each topic)...
