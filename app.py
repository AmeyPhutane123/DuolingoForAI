
import streamlit as st
st.set_page_config(page_title="AI Learn Platform", page_icon="🎓", layout="wide")
from pathlib import Path
import base64


# Custom CSS for Duolingo/Hugging Face style
st.markdown('''
    <style>
    .sidebar-content {background: #232946; color: #eebbc3;}
    .sidebar-content .stHeader, .sidebar-content .stSubheader {color: #eebbc3;}
    .sidebar-content .stExpander {background: #232946; border-radius: 8px; margin-bottom: 8px;}
    .sidebar-content .stButton>button {background: #eebbc3; color: #232946; border-radius: 6px; margin: 2px 0; font-weight: 600;}
    .sidebar-content .stButton>button:hover {background: #f7f7f7; color: #232946;}
    .sidebar-content .stProgress>div>div {background: linear-gradient(90deg, #eebbc3 60%, #f7f7f7 100%);}
    .main-card {background: #f7f7f7; border-radius: 16px; padding: 32px 24px; margin-top: 24px; box-shadow: 0 2px 16px #23294622;}
    .lesson-title {font-size: 2.2rem; font-weight: 700; color: #232946; margin-bottom: 12px;}
    .lesson-progress {font-size: 1.1rem; color: #eebbc3; font-weight: 600; margin-bottom: 16px;}
    .mascot-img {border-radius: 50%; box-shadow: 0 2px 8px #23294644; margin-bottom: 16px;}
    </style>
''', unsafe_allow_html=True)

# Course metadata
courses = [
    {
        "key": "1.llm",
        "title": "LLM Course",
        "desc": "This course will teach you about large language models using libraries from the HF ecosystem.",
        "img": "https://huggingface.co/course/static/llm-card.png"
    },
    {
        "key": "2.mcp",
        "title": "MCP Course",
        "desc": "This course will teach you about Model Context Protocol.",
        "img": "https://huggingface.co/course/static/mcp-card.png"
    },
    {
        "key": "3.agents",
        "title": "Agents Course",
        "desc": "Learn to build and deploy your own AI agents.",
        "img": "https://huggingface.co/course/static/agents-card.png"
    },
    {
        "key": "4.rl",
        "title": "Deep RL Course",
        "desc": "This course will teach you about deep reinforcement learning using libraries from the HF ecosystem.",
        "img": "https://huggingface.co/course/static/rl-card.png"
    }
]



# Page selection
st.sidebar.title("Course Navigation")
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


if 'selected_course' not in st.session_state:
    st.session_state.selected_course = "Home"

if page == "Home":
    st.title("🎓 Learn")
    st.markdown("<h2>Learn</h2>", unsafe_allow_html=True)
    cols = st.columns(2)
    for i, course in enumerate(courses):
        with cols[i % 2]:
            st.markdown(f"""
                <div class='course-card'>
                    <img src='{course['img']}' class='course-img'/>
                    <div class='course-title'>{course['title']}</div>
                    <div class='course-desc'>{course['desc']}</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Go to {course['title']}", key=f"go_{course['key']}"):
                st.session_state.selected_course = course['title']
                st.experimental_rerun()
    st.stop()

# Sync sidebar selection with session state
course_options = ["Home"] + [c["title"] for c in courses]
if st.session_state.selected_course != page:
    page = st.session_state.selected_course

# Use session state for navigation
if st.session_state.selected_course != "Home" and page == "Home":
    page = st.session_state.selected_course

else:
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
    st.sidebar.subheader("Lessons")

    st.sidebar.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
    st.sidebar.image("https://raw.githubusercontent.com/huggingface/brand-assets/main/huggingface_logo.png", width=80, caption="Your AI Mascot", output_format="PNG")
    st.sidebar.markdown("<h2 style='color:#eebbc3;margin-bottom:0;'>Course Navigation</h2>", unsafe_allow_html=True)
    for section, lessons_in_section in lessons.items():
        with st.sidebar.expander(f"📚 {section.replace('_', ' ').capitalize()}", expanded=(section == st.session_state.get('selected_section'))):
            for lesson in lessons_in_section:
                button_label = f"📝 {lesson.replace('.md', '').replace('_', ' ').capitalize()}"
                if st.sidebar.button(button_label, key=f"{section}_{lesson}"):
                    st.session_state.selected_section = section
                    st.session_state.selected_lesson = lesson
                    st.experimental_rerun()
    lesson_list = lessons.get(st.session_state.get('selected_section'), [])
    completed = lesson_list.index(st.session_state.get('selected_lesson')) + 1 if st.session_state.get('selected_lesson') in lesson_list else 0
    st.sidebar.progress(completed / max(1, len(lesson_list)) if lesson_list else 1, text=f"Progress: {completed}/{len(lesson_list)} lessons")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    # Main content
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    if lesson_list:
        st.markdown(f"<div class='lesson-title'>{get_lesson_title(st.session_state.get('selected_lesson'))}</div>", unsafe_allow_html=True)
        if st.session_state.get('selected_section') and st.session_state.get('selected_lesson'):
            st.markdown(f"<div class='lesson-progress'>Lesson {completed} of {len(lesson_list)}</div>", unsafe_allow_html=True)
            st.markdown(load_markdown(course_key, st.session_state.get('selected_section'), st.session_state.get('selected_lesson')))
    else:
        st.info("No lessons available for this course yet.")
    st.markdown("</div>", unsafe_allow_html=True)
