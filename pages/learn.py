# pages/learn.py — Modern Path + Lesson UI with enhanced interactivity
import streamlit as st
from pydantic import ValidationError
import json
from pathlib import Path

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
    
    # Apply custom CSS
    with open(Path(__file__).parent.parent / "styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Header container with modern styling
    with st.container():
        st.markdown("<div class='learn-header'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1.2, 1.6, 1.2])
        
        with col1:
            st.markdown("<h1 style='display:flex;align-items:center;gap:10px;margin-bottom:0.5rem'>"
                      "<span style='font-size:2rem;'>🎓</span> AI Learn</h1>", unsafe_allow_html=True)
            
            # Course selector with improved styling
            courses = ensure_course_selected()
            selected = st.selectbox("Course", 
                                   options=courses, 
                                   index=courses.index(ss["nav_course"]), 
                                   label_visibility="collapsed")
            
            if selected != ss["nav_course"]:
                ss["nav_course"] = selected
                ss["nav_section"] = None
                ss["nav_lesson"] = None
                st.rerun()
        
        with col2:
            st.markdown("<h4 style='margin-bottom:0.5rem'>Daily Goal</h4>", unsafe_allow_html=True)
            pct = min(100, int(100 * ss["xp_today"] / max(1, ss["daily_goal"])))
            st.progress(pct, text=f"{ss['xp_today']}/{ss['daily_goal']} XP")
            st.caption("Keep your streak alive by meeting your daily goal!")
        
        with col3:
            stats_cols = st.columns(3)
            
            with stats_cols[0]:
                with st.container():
                    st.markdown(f"<div class='stat-card'><div class='stat-value'>🔥 {ss['streak']}</div>"
                              f"<div class='stat-label'>Day Streak</div></div>", unsafe_allow_html=True)
            
            with stats_cols[1]:
                with st.container():
                    st.markdown(f"<div class='stat-card'><div class='stat-value'>♥ {ss['hearts']}</div>"
                              f"<div class='stat-label'>Hearts</div></div>", unsafe_allow_html=True)
            
            with stats_cols[2]:
                with st.container():
                    st.markdown(f"<div class='stat-card'><div class='stat-value'>💎 {ss['gems']}</div>"
                              f"<div class='stat-label'>Gems</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

def start_lesson(course: str, section: str, lesson: str):
    st.session_state["nav_course"] = course
    st.session_state["nav_section"] = section
    st.session_state["nav_lesson"] = lesson
    st.rerun()

header()

# Learning Path Section
with st.container():
    st.markdown("<div class='learning-path-container'>", unsafe_allow_html=True)
    course = st.session_state["nav_course"]
    st.markdown("<h2 class='section-title'>Learning Path</h2>", unsafe_allow_html=True)
    
    sections = list_dirs(COURSES_DIR/course)
    if not sections:
        st.info("No units yet. Use the Developer page to add a lesson.")
    else:
        # Course progress overview
        total_lessons = sum(len(list_lessons(course, sec)) for sec in sections)
        completed_lessons = 0  # This would be tracked in a real app
        
        if total_lessons > 0:
            overall_progress = int((completed_lessons / total_lessons) * 100)
            st.markdown(f"<div class='course-overview'>"
                      f"<h3>{course.replace('_',' ').replace('-',' ').title()}</h3>"
                      f"<div class='progress-stats'>"
                      f"<span>{completed_lessons}/{total_lessons} lessons completed</span>"
                      f"<span>{overall_progress}% complete</span>"
                      f"</div>"
                      f"</div>", unsafe_allow_html=True)
            st.progress(overall_progress / 100)
        
        # Units and lessons
        for unit_idx, sec in enumerate(sections, start=1):
            with st.container():
                st.markdown("<div class='unit-container'>", unsafe_allow_html=True)
                # Unit header with modern styling
                st.markdown(f"<div class='unit-header'>"
                          f"<div class='unit-number'>{unit_idx}</div>"
                          f"<div class='unit-details'>"
                          f"<h3>{sec.replace('_',' ').replace('-',' ').title()}</h3>"
                          f"<div class='unit-progress'>0% complete</div>"
                          f"</div>"
                          f"</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                lessons = list_lessons(course, sec)
                if not lessons:
                    with st.container():
                        st.markdown("<div class='empty-unit'>", unsafe_allow_html=True)
                        st.caption("No lessons yet in this unit.")
                        st.markdown("</div>", unsafe_allow_html=True)
                    continue
                
                # Lesson cards with improved styling
                st.markdown("<div class='lessons-container'>", unsafe_allow_html=True)
                
                rows = [lessons[i:i+2] for i in range(0, len(lessons), 2)]
                for pair in rows:
                    cols = st.columns(len(pair))
                    for col, ls in zip(cols, pair):
                        with col:
                            with st.container():
                                st.markdown("<div class='lesson-card'>", unsafe_allow_html=True)
                                lesson_title = ls.replace('_',' ').title()
                                st.markdown(f"<div class='lesson-icon'>📘</div>", unsafe_allow_html=True)
                                st.markdown(f"<h4>{lesson_title}</h4>", unsafe_allow_html=True)
                                st.caption(f"{course.replace('_',' ').title()} • {sec.replace('_',' ').title()}")
                                st.button("Start Lesson", 
                                         key=f"start_{course}_{sec}_{ls}", 
                                         use_container_width=True, 
                                         type="primary",
                                         on_click=start_lesson, 
                                         args=(course, sec, ls))
                                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)

# Render selected lesson with enhanced UI
if st.session_state.get("nav_section") and st.session_state.get("nav_lesson"):
    st.divider()
    
    # Load lesson data
    path = COURSES_DIR / course / st.session_state["nav_section"] / f"{st.session_state['nav_lesson']}.json"
    data = load_json(path)
    
    if data:
        try:
            obj = LessonJSON(**data)
            ov = obj.overview
            
            # Lesson header with metadata
            with st.container():
                st.markdown("<div class='lesson-header'>", unsafe_allow_html=True)
                st.markdown(f"<h2>{ov.get('title', 'Lesson')}</h2>", unsafe_allow_html=True)
                
                # Lesson metadata badges
                st.markdown(f"<div class='lesson-meta'>"
                          f"<span class='lesson-badge'>{ov.get('subtitle','')}</span>"
                          f"<span class='lesson-badge difficulty-{ov.get('difficulty','').lower()}'>{ov.get('difficulty','')}</span>"
                          f"<span class='lesson-badge'>{ov.get('duration_minutes',0)} min</span>"
                          f"</div>", unsafe_allow_html=True)
            
            # Reading sections with improved styling
            st.markdown("<h3 class='content-section-title'>📚 Reading Material</h3>", unsafe_allow_html=True)
            
            for idx, sec in enumerate(obj.content.get("sections", [])):
                with st.container():
                    st.markdown("<div class='content-section'>", unsafe_allow_html=True)
                    st.markdown(f"<h4>{sec.get('title','Section')}</h4>", unsafe_allow_html=True)
                    st.markdown(sec.get("body",""))
                    st.markdown("</div>", unsafe_allow_html=True)
            
            # Interactive quizzes with enhanced UI
            if obj.quizzes:
                st.markdown("<h3 class='content-section-title'>🧠 Knowledge Check</h3>", unsafe_allow_html=True)
                
                for q_idx, q in enumerate(obj.quizzes):
                    with st.container():
                        st.markdown("<div class='quiz-container'>", unsafe_allow_html=True)
                        # Question number and text
                        st.markdown(f"<div class='quiz-question'>"
                                  f"<span class='question-number'>Q{q_idx+1}</span>"
                                  f"<span class='question-text'>{q.q}</span>"
                                  f"</div>", unsafe_allow_html=True)
                        
                        # Answer choices with better styling
                        choice = st.radio(
                            "Choice", 
                            options=list(range(4)), 
                            format_func=lambda i: q.choices[i], 
                            key=f"q_{q.id}", 
                            horizontal=True, 
                            label_visibility="collapsed"
                        )
                        
                        # Check answer button with feedback
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            if st.button("Check Answer", key=f"chk_{q.id}", type="primary"):
                                if choice == q.answer_index:
                                    gained = xp_gain(q.xp_correct)
                                    with col2:
                                        st.success(f"Correct! +{gained} XP")
                                else:
                                    st.session_state["hearts"] = max(0, st.session_state["hearts"]-1)
                                    with col2:
                                        st.error(f"Incorrect. You lost 1 heart. Correct answer: {q.choices[q.answer_index]}")
                        st.markdown("</div>", unsafe_allow_html=True)
        
        except ValidationError:
            st.error("Invalid lesson JSON format. Please check the lesson file.")
    else:
        st.error("Lesson not found. The requested lesson file could not be loaded.")
