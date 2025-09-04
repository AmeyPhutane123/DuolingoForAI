# AGENTS.md - Duolingo-style AI Learning Platform

## Build/Run Commands
- **Local development**: `streamlit run llm-duo/app.py`
- **Setup environment**: `python -m venv .venv && .venv\Scripts\activate && pip install -r llm-duo/requirements.txt`
- **No tests configured** - this is a Streamlit educational app without automated testing

## Architecture & Structure
- **Main app**: `llm-duo/app.py` - Streamlit app with course navigation and lesson rendering
- **Course content**: `llm-duo/courses/{course_key}/{section}/` - Markdown lessons organized by course and section
- **Styling**: `llm-duo/.streamlit/config.toml` - Duolingo-inspired theme (green primary, dark backgrounds)
- **Dependencies**: Streamlit, HuggingFace Transformers, tokenizers, PyTorch for AI/ML lessons

## Code Style Guidelines
- **Python naming**: snake_case for variables/functions, ALL_CAPS for constants, CamelCase for classes
- **Imports**: Standard library first, then third-party, group related imports
- **Strings**: Use f-strings for dynamic content, triple quotes for multi-line HTML/CSS
- **Session state**: Consistent patterns with `st.session_state` for navigation state
- **Error handling**: Use `st.error()` and `st.stop()` for early returns in Streamlit context
- **File organization**: Config/styling at top, data structures, helper functions, main logic at bottom

## Course Content
- Courses stored as markdown files in `courses/{course_key}/{section}/lesson.md` structure
- Supports LLM, MCP, Agents, and Deep RL courses with progressive lesson navigation
