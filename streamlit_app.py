import streamlit as st
import requests

# ✅ Replace YOUR_APP_DOMAIN with your published Base44 app domain
#    e.g. https://my-nexus-app.base44.app  (no trailing slash)
APP_DOMAIN = "https://YOUR_APP_DOMAIN.base44.app"
ASK_NEXUS_URL = f"{APP_DOMAIN}/functions/askNexus"

LANGUAGES = ["English", "Kiswahili", "French", "Chinese", "Arabic", "German"]
CURRICULUMS = [
    "Illustrative Mathematics (IM)",
    "Cambridge International (IGCSE / A-Levels)",
    "International Baccalaureate (IB Math)",
    "Singapore Math (Math in Focus)",
    "Khan Academy",
    "Uganda NCDC Competency-Based Curriculum",
    "Saxon Math",
    "General",
]

MATH_KEYWORDS = [
    "math","algebra","calculus","geometry","fraction","integer","equation","theorem",
    "matrix","vector","derivative","integral","angle","triangle","polygon","arithmetic",
    "trigonometry","ratio","percent","probability","statistics","function","graph",
    "exponent","logarithm","prime","factor","division","multiplier","sum","subtraction",
    "addition","multiplication","number","digit","set","proof","limit","series",
    "sequence","polynomial","quadratic","linear","circle","sphere","cube","parabola",
    "what","how","why","explain","solve","find","calculate","show","define","mean",
    "is","are","does","example","formula","rule","property","simplify","expand",
]

WELCOME = {
    "English": "👋 Hi! I'm **Nexus AI** — your friendly math tutor. Ask me anything about maths!",
    "Kiswahili": "👋 Habari! Mimi ni **Nexus AI** — mwalimu wako wa hisabati.",
    "French": "👋 Bonjour! Je suis **Nexus AI** — votre tuteur en mathématiques.",
    "Chinese": "👋 你好！我是 **Nexus AI** — 你的数学辅导老师。",
    "Arabic": "👋 مرحباً! أنا **Nexus AI** — مدرسك للرياضيات.",
    "German": "👋 Hallo! Ich bin **Nexus AI** — dein Mathe-Tutor.",
}

# --- Page config ---
st.set_page_config(page_title="Nexus AI", page_icon="🧮", layout="centered")

# --- Custom black + neon green theme ---
st.markdown("""
    <style>
      .stApp { background:#000000; color:#ffffff; }
      h1, h2, h3, .nexus-title { color:#00FF66 !important; letter-spacing:3px; }
      .stChatMessage, .stTextArea textarea {
        background:#0a0a0a !important;
        border:1px solid rgba(0,255,102,0.2) !important;
      }
      .stButton > button {
        background-color:#00FF66 !important; color:#000 !important;
        font-weight:700; border:none;
      }
      .stButton > button:hover { filter:brightness(1.1); }
      .stMarkdown, .stText { color:#e6e6e6; }
      a, .css-1cpxqw2 { color:#00FF66; }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 style='text-align:center'>NEXUS AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#00FF66;opacity:0.5'>MATH MADE EASIER</p>", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    lang = st.selectbox("Language", LANGUAGES, index=0)
    curriculum = st.selectbox("Curriculum", CURRICULUMS, index=0)
    st.markdown("---")
    st.caption("No API key needed — powered by your Base44 backend.")

# --- Ask Nexus via the deployed function ---
def ask_nexus(query, history=None, curriculum=curriculum, lang=lang):
    try:
        resp = requests.post(
            ASK_NEXUS_URL,
            json={"query": query, "history": history or [],
                  "curriculum": curriculum, "lang": lang},
            timeout=120,
        )
        if resp.status_code != 200:
            return f"❌ Something went wrong (HTTP {resp.status_code})."
        data = resp.json()
        return data.get("answer") or "Sorry, no answer returned."
    except requests.exceptions.RequestException as e:
        return f"❌ Network error: `{e}`"
    except Exception as e:
        return f"❌ Error: `{e}`"

# --- Chat state ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant","text":WELCOME[lang]}]

# Display history
for m in st.session_state.messages:
    with st.chat_message("user" if m["role"]=="user" else "assistant",
                          avatar="🧑‍🎓" if m["role"]=="user" else "🤖"):
        st.markdown(m["text"])

# Input
user_input = st.chat_input("Ask a math question...")
if user_input:
    lower = user_input.lower()
    if not any(k in lower for k in MATH_KEYWORDS):
        st.session_state.messages.append({"role":"user","text":user_input})
        st.session_state.messages.append({"role":"assistant",
                                           "text":"⚠️ Please ask a math-related question (e.g. fractions, algebra, geometry)."})
        st.rerun()
    else:
        st.session_state.messages.append({"role":"user","text":user_input})
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(user_input)
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Nexus is thinking…"):
                # Build context from last 6 exchanges
                hist = []
                msgs = [m for m in st.session_state.messages if not m.get("error")]
                for i in range(0, len(msgs)-1, 2):
                    if msgs[i]["role"]=="user" and msgs[i+1]["role"]=="assistant":
                        hist.append({"question":msgs[i]["text"],"answer":msgs[i+1]["text"]})
                hist = hist[-6:]
                answer = ask_nexus(user_input, hist, curriculum, lang)
                st.markdown(answer)
        st.session_state.messages.append({"role":"assistant","text":answer})
