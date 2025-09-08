# pages/home.py — Modern landing with hero + course cards
import streamlit as st
import re
from pathlib import Path
import random

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

def get_course_icon(course_name):
    """Return an appropriate icon for each course type"""
    course_name = course_name.lower()
    if "llm" in course_name:
        return "🤖"
    elif "agent" in course_name:
        return "🕵️"
    elif "mcp" in course_name:
        return "🧠"
    elif "rl" in course_name:
        return "🎮"
    else:
        icons = ["📊", "📈", "🔍", "💻", "🧪"]
        # Use the course name as a seed for consistent icon selection
        random.seed(course_name)
        return random.choice(icons)

def top_bar_min():
    ss = st.session_state
    
    # Header with logo and stats
    header_container = st.container()
    with header_container:
        col1, col2 = st.columns([2, 3])
        
        with col1:
            st.markdown("<h1 style='display:flex;align-items:center;gap:10px;margin-bottom:0'>"
                      "<span style='font-size:2rem;'>🎓</span> AI Learn</h1>", unsafe_allow_html=True)
            st.markdown("<p style='margin-top:0;color:#CBD5E1;font-size:1rem;'>"
                      "Master AI concepts through interactive lessons</p>", unsafe_allow_html=True)
        
        with col2:
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
    
    # Progress bar for daily goal
    st.markdown("### Daily Progress")
    progress_container = st.container()
    with progress_container:
        col1, col2 = st.columns([4, 1])
        with col1:
            pct = min(100, int(100 * ss["xp_today"] / max(1, ss["daily_goal"])))
            st.progress(pct, text=f"{ss['xp_today']}/{ss['daily_goal']} XP")
            st.caption(f"You've completed {pct}% of your daily goal")
        with col2:
            st.button("🛍 Shop", key="btn_shop_home", use_container_width=True, on_click=open_shop, type="primary")

def render_shop_modal():
    ss = st.session_state
    if not ss.get("show_shop"): return
    
    with st.container(border=True):
        st.markdown("<h2 style='display:flex;align-items:center;gap:10px;margin-bottom:1rem'>"
                  "<span style='font-size:1.5rem;'>🛍️</span> Shop</h2>", unsafe_allow_html=True)
        
        shop_cols = st.columns(3)
        
        with shop_cols[0]:
            with st.container(className="course-card"):
                st.markdown("### 💎 100 Gems")
                st.markdown("Get 5 hearts to continue learning when you make mistakes")
                st.button("Purchase", key="buy_hearts", use_container_width=True, type="primary")
        
        with shop_cols[1]:
            with st.container(className="course-card"):
                st.markdown("### ⚡ XP Boost")
                st.markdown("Double XP for all lessons completed in the next 24 hours")
                st.button("50 gems", key="buy_xp_boost", use_container_width=True, type="primary")
        
        with shop_cols[2]:
            with st.container(className="course-card"):
                st.markdown("### 🎯 Streak Freeze")
                st.markdown("Protect your streak for one day of inactivity")
                st.button("20 gems", key="buy_streak_freeze", use_container_width=True, type="primary")
        
        st.button("Close Shop", use_container_width=True, on_click=lambda: ss.update({"show_shop": False}))

# Apply custom CSS
with open(Path(__file__).parent.parent / "styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Render the UI components
top_bar_min()
render_shop_modal()

# Hero section
st.markdown("<h2 style='margin-top:2rem;font-size:1.8rem;'>Learn AI concepts faster with interactive lessons</h2>", unsafe_allow_html=True)
st.markdown("<p style='font-size:1.1rem;color:#CBD5E1;margin-bottom:1.5rem;'>"
          "Choose a course below to start your learning journey. New courses are added regularly.</p>", unsafe_allow_html=True)

# Course cards section
courses = list_dirs(COURSES_DIR)
if not courses:
    st.info("No courses yet. Use the Developer tab to generate your first lesson.")
else:
    # Featured course (first course)
    featured_course = courses[0]
    clean_featured_name = clean_course_name(featured_course)
    sections = list_dirs(COURSES_DIR / featured_course)
    
    with st.container():
        st.markdown("<h3 style='margin-bottom:1rem;'>Featured Course</h3>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown("<div class='tile'>", unsafe_allow_html=True)
            # Add a gradient background
            st.markdown(f"""
            <div style="position:absolute;inset:0;background:linear-gradient(135deg, #4338ca 0%, #7c3aed 100%);opacity:0.8;"></div>
            <div class="tile-grad"></div>
            <div class="badges">
                <div class="badge">Featured</div>
                <div class="badge">{len(sections)} Units</div>
            </div>
            <div class="tile-content">
                <h2 class="tile-title">{clean_featured_name}</h2>
                <p class="tile-desc">Master the fundamentals and advanced concepts through interactive lessons</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Position the button at the bottom right
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("Start Learning", key=f"open_{featured_course}", type="primary"):
                    st.session_state["nav_course"] = featured_course
                    st.session_state["nav_section"] = None
                    st.session_state["nav_lesson"] = None
                    st.switch_page("pages/learn.py")
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Other courses
    st.markdown("<h3 style='margin-top:2rem;margin-bottom:1rem;'>All Courses</h3>", unsafe_allow_html=True)
    
    # Create a responsive grid layout
    cols_per_row = 3
    other_courses = courses
    rows = [other_courses[i:i+cols_per_row] for i in range(0, len(other_courses), cols_per_row)]
    
    for row in rows:
        cols = st.columns(len(row))
        for c, course in zip(cols, row):
            with c:
                clean_name = clean_course_name(course)
                course_icon = get_course_icon(course)
                sections = list_dirs(COURSES_DIR / course)
                
                with st.container():
                    st.markdown("<div class='course-card'>", unsafe_allow_html=True)
                    st.markdown(f"<h3><span class='course-icon'>{course_icon}</span> {clean_name}</h3>", unsafe_allow_html=True)
                    
                    # Course metadata
                    st.markdown(f"""
                    <div class="course-meta">
                        <span>📚 {len(sections)} Units</span>
                        <span>⏱️ Self-paced</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Progress indicator (placeholder for now)
                    st.markdown("<div class='course-progress'>", unsafe_allow_html=True)
                    st.progress(0, text="Not started")
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Action button
                    if st.button(f"Start Learning", key=f"open_{course}", use_container_width=True, type="primary"):
                        st.session_state["nav_course"] = course
                        st.session_state["nav_section"] = None
                        st.session_state["nav_lesson"] = None
                        st.switch_page("pages/learn.py")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
