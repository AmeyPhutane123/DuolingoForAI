# app.py — Router with st.Page + st.navigation; shared utilities via context
import streamlit as st
from pathlib import Path
import json, datetime as dt, requests
from typing import Dict, Any, List
from pydantic import BaseModel, ValidationError, conlist

st.set_page_config(page_title="AI Learn", page_icon="🎓", layout="wide")

# ---------- Shared config ----------
COURSES_DIR = Path("Courses")

def _get_secret(key: str, default: str) -> str:
    try: return st.secrets.get(key, default)
    except Exception: return default

AGENT_URL = _get_secret("AGENT_URL", "https://YOUR-SPACE.hf.space/generate_lesson")

# ---------- Shared schema ----------
class Quiz(BaseModel):
    id: str
    q: str
    choices: conlist(str, min_length=4, max_length=4)
    answer_index: int
    explain: str
    xp_correct: int = 5
    xp_incorrect: int = 0

class Flashcard(BaseModel):
    id: str
    q: str
    a: str
    xp: int = 2

class LessonJSON(BaseModel):
    version: str
    metadata: Dict[str, Any]
    overview: Dict[str, Any]
    content: Dict[str, Any]
    flashcards: List[Flashcard] = []
    quizzes: List[Quiz] = []

# ---------- Shared utils ----------
def load_json(path: Path):
    if not path.exists(): return None
    with path.open(encoding="utf-8") as f: return json.load(f)

def save_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)

def list_dirs(p: Path):
    if not p.exists(): return []
    return sorted([d.name for d in p.iterdir() if d.is_dir()])

def list_lessons(course: str, section: str):
    p = COURSES_DIR/course/section
    if not p.exists(): return []
    return sorted([f.stem for f in p.glob("*.json")])

def ensure_seed_dirs():
    (COURSES_DIR/"llm"/"1.introduction").mkdir(parents=True, exist_ok=True)

# ---------- Shared state ----------
ss = st.session_state
ss.setdefault("xp_total", 0)
ss.setdefault("hearts", 5)
ss.setdefault("streak", 1)
ss.setdefault("gems", 50)
ss.setdefault("daily_goal", 30)
ss.setdefault("xp_today", 0)
ss.setdefault("show_shop", False)
ss.setdefault("nav_course", None)
ss.setdefault("nav_section", None)
ss.setdefault("nav_lesson", None)

def xp_gain(amount: int):
    mult = 2 if ss.get("xp_boost_until") and dt.datetime.utcnow() < ss["xp_boost_until"] else 1
    gained = amount * mult
    ss["xp_total"] += gained
    ss["xp_today"] += gained
    return gained

def ensure_course_selected() -> List[str]:
    courses = list_dirs(COURSES_DIR) or ["llm"]
    if not ss.get("nav_course"): ss["nav_course"] = courses[0]
    return courses

# ---------- Provide context to pages ----------
context = {
    "COURSES_DIR": COURSES_DIR,
    "AGENT_URL": AGENT_URL,
    "LessonJSON": LessonJSON,
    "Quiz": Quiz,
    "Flashcard": Flashcard,
    "load_json": load_json,
    "save_json": save_json,
    "list_dirs": list_dirs,
    "list_lessons": list_lessons,
    "ensure_seed_dirs": ensure_seed_dirs,
    "ensure_course_selected": ensure_course_selected,
    "xp_gain": xp_gain,
}

st.session_state["_ctx"] = context

# ---------- Define pages ----------
pg = st.navigation(
    [
        st.Page("pages/home.py", title="Home", icon="🏠"),
        st.Page("pages/learn.py", title="Learn", icon="📘"),
        st.Page("pages/developer.py", title="Developer", icon="🛠️"),
    ],
    position="sidebar"
)
ensure_seed_dirs()
pg.run()
