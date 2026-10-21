
import io
import streamlit as st
from google import genai
from google.genai import types

MODEL = "gemini-2.5-flash-lite"
VOICE = "JBFqncBSd6RMkjVDRZzb"  # ElevenLabs 'George', on every free account
MAX_TURNS = 20                 # each turn spends YOUR credits, and anyone with the link can talk to it

st.set_page_config(page_title="My voice agent", page_icon="🎙️")

def secret(name):
    """A key from Streamlit's Secrets box (never from the code), or None if it isn't there."""
    try:
        return st.secrets.get(name)
    except Exception:  # no Secrets at all
        return None

if not secret("GEMINI_API_KEY"):
    st.error("No GEMINI_API_KEY in this app's Secrets. On share.streamlit.io: your app → ┇ → Settings → Secrets.")
    st.stop()
    @st.cache_resource  # one Gemini client, created once, not on every click
    def gemini():
        return genai.Client(api_key=secret("GEMINI_API_KEY"))

gem = gemini()

# Streamlit re-runs this whole file on every click. st.session_state is what survives, per visitor.
for key, start in {"todos": [], "history": [], "log": [], "turn": 0, "reply_audio": None}.items():
    if key not in st.session_state:
        st.session_state[key] = start
TODOS = st.session_state.todos  # your tools read and change this list

# ==================== PASTE FROM COLAB: START ====================
#  COPY THIS (1 of 2): who the agent is
AGENT_NAME = "Pip"
SYSTEM_PROMPT = """You are Pip, a voice to-do assistant for a busy student.
Everything you say is read aloud, so: one or two short sentences, no lists, no markdown, no emojis.
Use your tools to add, read and finish to-dos. Never say you did something unless a tool did it.
If the user asks for something none of your tools can do, say so plainly and do nothing."""

#  COPY THIS (2 of 2): what the agent can do
def add_todo(task: str) -> str:
    """Add a task to the user's to-do list."""
    TODOS.append({"task": task, "done": False})

