# pages/home.py — Clean landing with hero + course cards (FIXED NAMING)
import streamlit as st
import re

ctx = st.session_state["_ctx"]
COURSES_DIR = ctx["COURSES_DIR"]
list_dirs = ctx["list_dirs"]

def clean_course_name(folder_name):
    """Remove numeric prefixes and clean up course names"""
    # Remove leading numbers and dots
    name = re.sub(r'^\d+\.?', '', folder_name)
    # Replace underscores with spaces and title case
    name = name.replace('_', ' ').title()
    return name

def open_shop():
    st.session_state["show_shop"] = True

def top_bar_min():
    ss = st.session_state
    c1, c2, c3 = st.columns([1.2, 1.4, 1.2])
    with c1: st.markdown("### 🎓 AI Learn")
    with c2:
        st.caption("Daily goal")
        pct = min(100, int(100 * ss["xp_today"] / max(1, ss["daily_goal"])))
        st.progress(pct, text=f"{ss['xp_today']}/{ss['daily_goal']} XP")
    with c3:
        m1, m2, m3 = st.columns(3)
        with m1: st.metric("🔥", f"{ss['streak']}d", label_visibility="collapsed")
        with m2: st.metric("♥", f"{ss['hearts']}", label_visibility="collapsed")
        with m3: st.metric("💎", f"{ss['gems']}", label_visibility="collapsed")
        st.button("🛍 Shop", key="btn_shop_home", use_container_width=True, on_click=open_shop)

def render_shop_modal():
    ss = st.session_state
    if not ss.get("show_shop"): return
    with st.container(border=True):
        st.markdown("#### 🛍 Shop")
        if st.button("Close", use_container_width=True): ss["show_shop"] = False

top_bar_min()
render_shop_modal()

st.markdown("## Learn faster with AI-crafted lessons")
st.caption("Pick a course to start. Add more from the Developer tab any time.")
st.divider()

courses = list_dirs(COURSES_DIR)
if not courses:
    st.info("No courses yet. Use the Developer tab to generate your first lesson.")
else:
    cols_per_row = 3
    rows = [courses[i:i+cols_per_row] for i in range(0, len(courses), cols_per_row)]
    for row in rows:
        cols = st.columns(len(row))
        for c, course in zip(cols, row):
            with c:
                with st.container(border=True):
                    # Fix: Clean the course name display
                    clean_name = clean_course_name(course)
                    st.markdown(f"### {clean_name}")
                    sections = list_dirs(COURSES_DIR / course)
                    st.caption(f"{len(sections)} unit(s)")
                    if st.button("Open", key=f"open_{course}", use_container_width=True):
                        st.session_state["nav_course"] = course
                        st.session_state["nav_section"] = None
                        st.session_state["nav_lesson"] = None
                        st.switch_page("pages/learn.py")
