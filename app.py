

import streamlit as st
st.set_page_config(page_title="AI Learn Platform", page_icon="🎓", layout="wide")

# Custom theme and card styles
PRIMARY = "#22c55e"
st.markdown(f"""
    <style>
    .stApp {{ background: #0b1220; color: #e5f6ee; }}
    .course-card {{ padding:1.5rem 1.5rem; border-radius:22px; background:#16213a; border:2px solid #22c55e; margin-bottom:1rem; box-shadow:0 2px 12px #0002; text-align:left; }}
    .course-img {{ width:100%; border-radius:18px; margin-bottom:1rem; }}
    .course-title {{ font-size:1.5rem; font-weight:700; margin-bottom:0.5rem; }}
    .course-desc {{ font-size:1.1rem; margin-bottom:1.5rem; color:#e5f6ee; }}
    .stButton>button {{ background:{PRIMARY}; color:#032b23; border-radius:14px; font-weight:700; margin-top:0.5rem; }}
    </style>
""", unsafe_allow_html=True)

# Course metadata
courses = [
    {
        "key": "llm",
        "title": "LLM Course",
        "desc": "This course will teach you about large language models using libraries from the HF ecosystem.",
        "img": "https://huggingface.co/course/static/llm-card.png"
    },
    {
        "key": "mcp",
        "title": "MCP Course",
        "desc": "This course will teach you about Model Context Protocol.",
        "img": "https://huggingface.co/course/static/mcp-card.png"
    },
    {
        "key": "agents",
        "title": "Agents Course",
        "desc": "Learn to build and deploy your own AI agents.",
        "img": "https://huggingface.co/course/static/agents-card.png"
    },
    {
        "key": "rl",
        "title": "Deep RL Course",
        "desc": "This course will teach you about deep reinforcement learning using libraries from the HF ecosystem.",
        "img": "https://huggingface.co/course/static/rl-card.png"
    }
]



# Page selection
st.sidebar.title("Course Navigation")
if 'selected_course' not in st.session_state:
    st.session_state.selected_course = "Home"
course_options = ["Home"] + [c["title"] for c in courses]
page = st.sidebar.selectbox("Select a course:", course_options)

import os
import glob

def get_sections_and_lessons(course_key):
    base = os.path.join("courses", f"{course_key}")
    if not os.path.exists(base):
        return [], {}
    # Only include folders that contain at least one .md file
    sections = []
    lessons = {}
    for d in sorted(os.listdir(base)):
        section_path = os.path.join(base, d)
        if os.path.isdir(section_path):
            lesson_files = sorted(glob.glob(os.path.join(section_path, '*.md')))
            if lesson_files:
                sections.append(d)
                lessons[d] = [os.path.basename(f) for f in lesson_files]
    return sections, lessons

def get_lesson_title(filename):
    if not filename:
        return "Lesson"
    return filename.replace('.md','').replace('_',' ').replace('-',' ').capitalize()

def load_markdown(course_key, section, lesson):
    path = f"courses/{course_key}/{section}/{lesson}"
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            return f.read()
    return "Lesson not found."


import streamlit as st
if 'selected_course' not in st.session_state:
    st.session_state.selected_course = "Home"


if page == "Home":
    st.title("🎓 Learn")
    st.markdown("<h2>Learn</h2>", unsafe_allow_html=True)
    cols = st.columns(2)
    for i, course in enumerate(courses):
        with cols[i % 2]:
            with st.container():
                st.markdown(f"""
                    <div class='course-card'>
                        <img src='{course['img']}' class='course-img'/>
                        <div class='course-title'>{course['title']}</div>
                        <div class='course-desc'>{course['desc']}</div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"Start {course['title']}", key=f"start_{course['key']}", use_container_width=True):
                    st.session_state.selected_course = course['title']
                    st.rerun()
    st.stop()

# Check for course navigation from buttons
if st.session_state.selected_course != "Home":
    page = st.session_state.selected_course

if page != "Home":
    # Map course title to key
    course_map = {c['title']: c['key'] for c in courses}
    course_key = course_map.get(page, None)
    if not course_key:
        found = [c['key'] for c in courses if c['title'] == page]
        course_key = found[0] if found else None
    if not course_key and page != "Home":
        st.error("Course not found. Please select a valid course from the sidebar.")
        st.stop()
    st.title(page)
    # Get sections and lessons
    sections, lessons = get_sections_and_lessons(course_key)
    # Sidebar navigation for sections/lessons
    st.sidebar.markdown("---")
    st.sidebar.subheader("Sections")
    selected_section = st.sidebar.selectbox("Select section:", sections) if sections else None
    lesson_list = lessons.get(selected_section, []) if selected_section else []
    st.sidebar.subheader("Lessons")
    selected_lesson = st.sidebar.selectbox("Select lesson:", lesson_list) if lesson_list else None
    # Progress bar (Duolingo style)
    completed = lesson_list.index(selected_lesson) + 1 if selected_lesson in lesson_list else 0
    st.sidebar.progress(completed / max(1, len(lesson_list)) if lesson_list else 1, text=f"Progress: {completed}/{len(lesson_list)} lessons")
    # Mascot/avatar
    st.sidebar.image("https://raw.githubusercontent.com/huggingface/brand-assets/main/huggingface_logo.png", width=80)
    # Main content
    st.markdown(f"## {get_lesson_title(selected_lesson)}")
    if selected_section and selected_lesson:
        st.markdown(load_markdown(course_key, selected_section, selected_lesson))
        st.markdown(f"<span style='color:{PRIMARY};font-weight:700;'>Lesson {completed} of {len(lesson_list)}</span>", unsafe_allow_html=True)
    else:
        st.info("No lessons available for this course yet.")
