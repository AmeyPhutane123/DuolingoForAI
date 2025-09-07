# pages/developer.py — Generate → Validate → Save JSON lessons
import streamlit as st
from pydantic import ValidationError
import requests
import json

ctx = st.session_state["_ctx"]
COURSES_DIR = ctx["COURSES_DIR"]
AGENT_URL = ctx["AGENT_URL"]
LessonJSON = ctx["LessonJSON"]
save_json = ctx["save_json"]

st.markdown("## Developer")
st.caption("Generate → Validate → Save JSON lessons")

c1, c2, c3 = st.columns(3)
with c1: course_key = st.text_input("course_key", value="llm")
with c2: section_key = st.text_input("section_key", value="1.introduction")
with c3: lesson_key = st.text_input("lesson_key", value="01.overview")

src_type = st.radio("Source", ["url","markdown"], horizontal=True)
src_value = st.text_input("Lesson URL") if src_type=="url" else st.text_area("Paste Markdown", height=220)

o1, o2 = st.columns(2)
with o1: difficulty = st.selectbox("Difficulty", ["beginner","intermediate","advanced"])
with o2: duration = st.number_input("Duration (min)", 5, 90, 20, 5)

if st.button("Generate", type="primary"):
    if not src_value:
        st.warning("Provide a URL or Markdown")
    else:
        payload = {
            "course_key": course_key,
            "section_key": section_key,
            "lesson_key": lesson_key,
            "source": {"type": src_type, "value": src_value},
            "options": {"difficulty": difficulty, "duration_hint": duration}
        }
        try:
            r = requests.post(AGENT_URL, json=payload, timeout=90)
            r.raise_for_status()
            res = r.json()
            
            if res.get("ok"):
                data = res["data"]
                st.subheader("Preview JSON")
                st.json(data, expanded=False)
                try:
                    LessonJSON(**data)
                    st.success("Schema OK")
                    save_path = COURSES_DIR/course_key/section_key/f"{lesson_key}.json"
                    if st.button("Save to repository", type="primary", use_container_width=True):
                        save_json(save_path, data)
                        st.success(f"Saved: {save_path}")
                except ValidationError as e:
                    st.error("Schema validation failed")
                    st.json(e.errors(), expanded=False)
            else:
                st.error("Agent returned failure")
                st.json(res)
        except Exception as e:
            st.error(f"Agent error: {e}")
