# pages/learn.py — Improved Path + Lesson UI
import streamlit as st
from pydantic import ValidationError
import json

ctx = st.session_state["_ctx"]
COURSES_DIR = ctx["COURSES_DIR"]
LessonJSON = ctx["LessonJSON"]
list_dirs = ctx["list_dirs"]
list_lessons = ctx["list_lessons"]
ensure_course_selected = ctx["ensure_course_selected"]
xp_gain = ctx["xp_gain"]
load_json = ctx["load_json"]

def header():
    ss = st.session_state
    c1, c2, c3 = st.columns([1.05, 1.6, 1.05])
    with c1:
        st.markdown("### 🎓 AI Learn")
        courses = ensure_course_selected()
        selected = st.selectbox("Course", options=courses, index=courses.index(ss["nav_course"]), label_visibility="collapsed")
        if selected != ss["nav_course"]:
            ss["nav_course"] = selected; ss["nav_section"] = None; ss["nav_lesson"] = None; st.rerun()
    with c2:
        st.caption("Daily goal")
        pct = min(100, int(100 * ss["xp_today"] / max(1, ss["daily_goal"])))
        st.progress(pct, text=f"{ss['xp_today']}/{ss['daily_goal']} XP")
        st.caption("Keep the streak alive by meeting your goal")
    with c3:
        m1, m2, m3 = st.columns(3)
        with m1: st.metric("🔥 Streak", f"{ss['streak']}d")
        with m2: st.metric("♥ Hearts", f"{ss['hearts']}")
        with m3: st.metric("💎 Gems", f"{ss['gems']}")

def start_lesson(course: str, section: str, lesson: str):
    st.session_state["nav_course"] = course
    st.session_state["nav_section"] = section
    st.session_state["nav_lesson"] = lesson
    st.rerun()

header()

# Path
course = st.session_state["nav_course"]
st.markdown("### Path")
sections = list_dirs(COURSES_DIR/course)
if not sections:
    st.info("No units yet. Use the Developer page to add a lesson.")
else:
    for unit_idx, sec in enumerate(sections, start=1):
        head = st.container()
        with head:
            u1, u2, u3 = st.columns([1, 5, 1.6])
            with u1: st.markdown(f"#### {unit_idx}"); st.caption("Unit")
            with u2: st.markdown(f"**{sec.replace('_',' ').replace('-',' ').title()}**"); st.caption("0% complete")
            with u3: st.write("")

        lessons = list_lessons(course, sec)
        if not lessons:
            with st.container(border=True):
                st.caption("No lessons yet in this unit.")
            continue

        rows = [lessons[i:i+2] for i in range(0, len(lessons), 2)]
        for pair in rows:
            cols = st.columns(len(pair))
            for col, ls in zip(cols, pair):
                with col:
                    with st.container(border=True):
                        st.markdown(f"**📘 {ls.replace('_',' ').title()}**")
                        st.caption(f"{course} • {sec}")
                        st.button("Start", key=f"start_{course}_{sec}_{ls}", use_container_width=True, on_click=start_lesson, args=(course, sec, ls))

# Render selected lesson below, if any
if st.session_state.get("nav_section") and st.session_state.get("nav_lesson"):
    st.divider()
    path = COURSES_DIR / course / st.session_state["nav_section"] / f"{st.session_state['nav_lesson']}.json"
    data = load_json(path)
    if data:
        try:
            obj = LessonJSON(**data)
            ov = obj.overview
            st.subheader(ov.get("title", "Lesson"))
            st.caption(f"{ov.get('subtitle','')} • {ov.get('difficulty','')} • {ov.get('duration_minutes',0)} min")
            
            st.markdown("### Reading")
            for sec in obj.content.get("sections", []):
                with st.container(border=True):
                    st.markdown(f"**{sec.get('title','Section')}**")
                    st.markdown(sec.get("body",""))
            
            if obj.quizzes:
                st.markdown("### Quizzes")
                for q in obj.quizzes:
                    with st.container(border=True):
                        st.write(q.q)
                        choice = st.radio("Choice", options=list(range(4)), format_func=lambda i: q.choices[i], key=f"q_{q.id}", horizontal=True, label_visibility="collapsed")
                        if st.button("Check", key=f"chk_{q.id}"):
                            if choice == q.answer_index:
                                gained = xp_gain(q.xp_correct); st.success(f"Correct! +{gained} XP")
                            else:
                                st.session_state["hearts"] = max(0, st.session_state["hearts"]-1); st.error("Incorrect.")
        except ValidationError:
            st.error("Invalid lesson JSON")
    else:
        st.error("Lesson not found")
