import streamlit as st
import os, glob

st.set_page_config(page_title="AI Learn Platform", page_icon="🎓", layout="wide")

# ===== Global styles (professional dark) =====
st.markdown("""
<style>
/* Import modern, legible font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

/* Theme tokens */
:root{
  --bg: #0c111c;
  --panel: #121a27;
  --panel-2:#0f1625;
  --text: #e8f1fb;
  --muted:#9bb2d0;
  --brand:#22c55e;
  --brand-2:#18a14c;
  --accent:#7dd3fc;
  --border:#1f2b3d;
  --shadow: 0 10px 30px rgba(0,0,0,.40);
}

html, body, [class*="css"] {
  font-family: "Inter", system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, "Helvetica Neue", Arial, "Noto Sans", "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
}

/* App background + container width */
.stApp{ background: var(--bg); color: var(--text); }
div.block-container{ max-width: 1200px; padding-top: 1.2rem; }

/* Hide default Streamlit top padding ridge */
header[data-testid="stHeader"] { background: transparent; }

/* Sidebar styling */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, var(--panel) 0%, var(--panel-2) 100%);
  border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .stButton>button{
  width: 100%;
  border-radius: 12px;
  padding: .60rem .8rem;
  font-weight: 700;
  border: 1px solid var(--border);
}
section[data-testid="stSidebar"] button[kind="secondary"]{
  background: #0f1729;
  color: var(--text);
}
section[data-testid="stSidebar"] button[kind="primary"]{
  background: var(--brand);
  color: #031b12;
}
section[data-testid="stSidebar"] .st-expander{
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 12px;
}
section[data-testid="stSidebar"] .stProgress > div > div{
  background: var(--brand);
}

/* Headings */
h1, h2, h3{ letter-spacing: .2px; }
h1{ font-weight: 800; }

/* Course card grid */
.course-grid{ display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 22px; }
@media (max-width: 980px){ .course-grid{ grid-template-columns: 1fr; } }

/* Card */
.card{
  background: linear-gradient(180deg, rgba(34,197,94,.05) 0%, rgba(12,17,28,0) 35%), var(--panel);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 18px;
  box-shadow: var(--shadow);
  transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
}
.card:hover{ transform: translateY(-2px); border-color: #2b3d55; }

/* Card media */
.card-media{
  width: 100%;
  aspect-ratio: 16/9;
  object-fit: cover;
  border-radius: 14px;
  border: 1px solid var(--border);
  background: #0e1727;
  margin-bottom: 14px;
}

/* Card title & desc */
.card-title{ font-size: 1.15rem; font-weight: 800; margin-bottom: 6px; }
.card-desc{ color: var(--muted); margin-bottom: 12px; }

/* Primary CTA button (content area) */
.stButton>button.course-cta{
  background: var(--brand);
  color: #051a13;
  border: 1px solid #0e6b37;
  border-radius: 12px;
  font-weight: 800;
  padding: .6rem .9rem;
  width: 100%;
}
.stButton>button.course-cta:hover{ background: var(--brand-2); }

/* Lesson content typography */
.markdown-body{
  line-height: 1.7;
}
.markdown-body h1,h2,h3,h4{ color: var(--text); }
.markdown-body p, .markdown-body li{ color: #d7e4f7; }

/* Info panel */
.info{
  border: 1px dashed var(--border);
  background: #0d1728;
  border-radius: 12px;
  padding: 14px 16px;
  color: var(--muted);
}

/* Tiny helper text */
.small{ color: var(--muted); font-size: .86rem; }

/* Progress label */
.progress-label{
  color: var(--brand);
  font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

PRIMARY = "#22c55e"

# ----- Course metadata unchanged -----
courses = [
    {"key":"llm","title":"LLM Course","desc":"This course will teach you about large language models using libraries from the HF ecosystem.","img":"https://huggingface.co/course/static/llm-card.png"},
    {"key":"mcp","title":"MCP Course","desc":"This course will teach you about Model Context Protocol.","img":"https://huggingface.co/course/static/mcp-card.png"},
    {"key":"agents","title":"Agents Course","desc":"Learn to build and deploy your own AI agents.","img":"https://huggingface.co/course/static/agents-card.png"},
    {"key":"rl","title":"Deep RL Course","desc":"This course will teach you about deep reinforcement learning using libraries from the HF ecosystem.","img":"https://huggingface.co/course/static/rl-card.png"},
]

# ----- Helpers unchanged -----
def get_sections_and_lessons(course_key):
    base = os.path.join("courses", f"{course_key}")
    if not os.path.exists(base): return [], {}
    sections, lessons = [], {}
    for d in sorted(os.listdir(base)):
        section_path = os.path.join(base, d)
        if os.path.isdir(section_path):
            lesson_files = sorted(glob.glob(os.path.join(section_path, "*.md")))
            if lesson_files:
                sections.append(d)
                lessons[d] = [os.path.basename(f) for f in lesson_files]
    return sections, lessons

def get_lesson_title(filename):
    if not filename: return "Lesson"
    return filename.replace(".md","").replace("_"," ").replace("-"," ").capitalize()

def load_markdown(course_key, section, lesson):
    path = f"courses/{course_key}/{section}/{lesson}"
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f: return f.read()
    return "Lesson not found."

# ----- Session state unchanged -----
ss = st.session_state
ss.setdefault("selected_course", "Home")
ss.setdefault("selected_section", None)
ss.setdefault("selected_lesson", None)

# ===== Sidebar Navigation =====
st.sidebar.title("Course Navigation")
if st.sidebar.button("🏠 Home", use_container_width=True):
    ss.selected_course, ss.selected_section, ss.selected_lesson = "Home", None, None
    st.rerun()

st.sidebar.markdown("---")

for course in courses:
    course_selected = ss.selected_course == course["title"]
    if st.sidebar.button(
        f"📚 {course['title']}",
        key=f"nav_{course['key']}",
        use_container_width=True,
        type="primary" if course_selected else "secondary",
    ):
        ss.selected_course, ss.selected_section, ss.selected_lesson = course["title"], None, None
        st.rerun()

    if course_selected:
        sections, lessons = get_sections_and_lessons(course["key"])
        for section in sections:
            section_selected = ss.selected_section == section
            with st.sidebar.expander(f"📖 {get_lesson_title(section)}", expanded=section_selected):
                for lesson in lessons.get(section, []):
                    lesson_title = get_lesson_title(lesson)
                    lesson_selected = ss.selected_lesson == lesson
                    if st.button(
                        f"{'▶️' if lesson_selected else '📄'} {lesson_title}",
                        key=f"lesson_{course['key']}_{section}_{lesson}",
                        use_container_width=True,
                        type="primary" if lesson_selected else "secondary",
                    ):
                        ss.selected_section, ss.selected_lesson = section, lesson
                        st.rerun()

# ===== Home (course grid) =====
page = ss.selected_course
if page == "Home":
    st.markdown("### Learn")
    st.markdown("<h1 style='margin-top:-10px'>🎓 Learn</h1>", unsafe_allow_html=True)
    st.markdown("<div class='small'>Choose a track to begin. You can switch lessons anytime from the sidebar.</div>", unsafe_allow_html=True)
    st.write("")

    st.markdown("<div class='course-grid'>", unsafe_allow_html=True)
    for c in courses:
        with st.container(border=False):
            st.markdown(f"""
            <div class="card">
              <img class="card-media" src="{c['img']}" />
              <div class="card-title">{c['title']}</div>
              <div class="card-desc">{c['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Start {c['title']}", key=f"start_{c['key']}", use_container_width=True):
                ss.selected_course = c["title"]
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ===== Course page =====
if page != "Home":
    course_map = {c["title"]: c["key"] for c in courses}
    course_key = course_map.get(page) or next((c["key"] for c in courses if c["title"] == page), None)
    if not course_key:
        st.error("Course not found. Please select a valid course from the sidebar.")
        st.stop()

    st.markdown(f"<h1>{page}</h1>", unsafe_allow_html=True)

    selected_section = ss.selected_section
    selected_lesson = ss.selected_lesson

    # Sidebar progress & mascot (sticky feel)
    if selected_section and selected_lesson:
        sections, lessons = get_sections_and_lessons(course_key)
        lesson_list = lessons.get(selected_section, [])
        completed = lesson_list.index(selected_lesson) + 1 if selected_lesson in lesson_list else 0

        st.sidebar.markdown("---")
        st.sidebar.progress(completed / max(1, len(lesson_list)) if lesson_list else 1,
                            text=f"Progress: {completed}/{len(lesson_list)} lessons")
        st.sidebar.image("https://raw.githubusercontent.com/huggingface/brand-assets/main/huggingface_logo.png", width=80)

    # Main content
    if selected_section and selected_lesson:
        st.markdown(f"## {get_lesson_title(selected_lesson)}")
        file_path = f"courses/{course_key}/{selected_section}/{selected_lesson}"
        with st.expander("Debug info", expanded=False):
            st.write(f"Looking for file: {file_path}")
            st.write(f"File exists: {os.path.exists(file_path)}")

        content = load_markdown(course_key, selected_section, selected_lesson)
        if content == "Lesson not found.":
            st.error(f"Could not load lesson content from: {file_path}")
        else:
            st.markdown(f"<div class='markdown-body'>{content}</div>", unsafe_allow_html=True)

        sections, lessons = get_sections_and_lessons(course_key)
        lesson_list = lessons.get(selected_section, [])
        completed = lesson_list.index(selected_lesson) + 1 if selected_lesson in lesson_list else 0
        st.markdown(f"<div class='progress-label'>Lesson {completed} of {len(lesson_list)}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='info'>Select a lesson from the sidebar to begin learning.</div>", unsafe_allow_html=True)
