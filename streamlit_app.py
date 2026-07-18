import streamlit as st
import requests

# ✅ Replace YOUR_APP_DOMAIN with your published Base44 app domain
#    e.g. https://my-nexus-app.base44.app  (no trailing slash)
APP_DOMAIN = "https://nexusai123.base44.app"
ASK_NEXUS_URL = f"{APP_DOMAIN}/functions/askNexus"

LANG_LABELS = {
    "English":   "🇬🇧 English",
    "Kiswahili": "🇰🇪 Kiswahili",
    "French":    "🇫🇷 French",
    "Chinese":   "🇨🇳 Chinese",
    "Arabic":    "🇸🇦 Arabic",
    "German":    "🇩🇪 German",
}

CURRICULUMS = {
    "Global & Institutional": [
        "Illustrative Mathematics (IM)",
        "Cambridge International (IGCSE / A-Levels)",
        "International Baccalaureate (IB Math)",
        "Uganda NCDC Competency-Based Curriculum",
        "Agile Mind Common Core Math",
        "Big Ideas Math",
    ],
    "Conceptual & Mastery-Based": [
        "Singapore Math (Math in Focus)", "Math-U-See", "Math Academy",
        "Math Mammoth", "RightStart Mathematics", "CTCMath",
    ],
    "Spiral & Repetition-Based": [
        "Saxon Math", "Everyday Mathematics", "Horizons Math",
        "Go Math!", "Think Academy Math",
    ],
    "Digital & Self-Paced": [
        "Khan Academy", "Teaching Textbooks", "Beast Academy",
        "Prodigy Math", "IXL Learning Math", "ALEKS Math",
    ],
    "Specialized & Advanced": [
        "Russian School of Mathematics (RSM)", "Life of Fred Math",
    ],
}

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

WELCOME_MESSAGES  = {
    "English":   "👋 Hi! I'm **Nexus AI** — your friendly math tutor. Ask me anything about maths and I'll explain it simply. Try: *\"What is a fraction?\"* or *\"How do I solve 2x + 3 = 7?\"*",
    "Kiswahili": "👋 Habari! Mimi ni **Nexus AI** — mwalimu wako wa hisabati. Niulize chochote kuhusu hisabati!",
    "French":    "👋 Bonjour! Je suis **Nexus AI** — votre tuteur en mathématiques. Posez-moi n'importe quelle question!",
    "Chinese":   "👋 你好！我是 **Nexus AI** — 你的数学辅导老师。问我任何数学问题！",
    "Arabic":    "👋 مرحباً! أنا **Nexus AI** — مدرسك للرياضيات. اسألني أي سؤال!",
    "German":    "👋 Hallo! Ich bin **Nexus AI** — dein Mathe-Tutor. Frag mich alles!",

}

st.set_page_config(
    page_title="Nexus AI — Math Tutor",
    page_icon="🟢",
    layout="wide",
)

st.markdown("""
<style>
  /* Pure black background, neon green accents */
  html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #000000 !important;
    color: #ffffff;
  }
  [data-testid="stSidebar"] { background-color: #080808 !important; }
  [data-testid="stSidebar"] * { color: #ffffff; }
  h1, h2, h3 { color: #00FF00 !important; }
  .stChatMessage { background: #0d0d0d; border: 1px solid #00FF0026; border-radius: 12px; }
  .stButton>button {
    background: #00FF00; color: #000; font-weight: 700; border: none;
    border-radius: 8px;
  }
  .stButton>button:hover { filter: brightness(1.1); }
  .stSelectbox label, .stRadio label { color: #00FF00 !important; font-size: 11px; }
  .stTextInput>div>div>input, .stTextArea>div>div>textarea {
    background: #0a0a0a !important;
    border: 1px solid #00FF0033 !important;
    color: #fff !important;
    border-radius: 12px;
  }
  .stChatInputContainer { background: #0a0a0a; border-top: 1px solid #00FF0020; }
</style>
""", unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state.messages = []
if "lang" not in st.session_state:
    st.session_state.lang = "English"
if "curriculum" not in st.session_state:
    st.session_state.curriculum = "Illustrative Mathematics (IM)"


with st.sidebar:
    st.markdown("## 🟢 NEXUS AI")
    st.markdown("<small style='color:#00FF0080'>MATH MADE EASIER</small>", unsafe_allow_html=True)
    st.markdown("---")

    # Language picker
    st.markdown("#### 🌐 Language")
    lang_choice = st.radio(
        "Select language",
        options=list(LANG_LABELS.keys()),
        format_func=lambda x: LANG_LABELS[x],
        index=list(LANG_LABELS.keys()).index(st.session_state.lang),
        label_visibility="collapsed",
    )
    if lang_choice != st.session_state.lang:
        st.session_state.lang = lang_choice
        st.session_state.messages = []  # reset chat on lang change
        st.rerun()

    st.markdown("---")

    # Curriculum picker
    st.markdown("#### 📚 Curricula")
    for cat, items in CURRICULUMS.items():
        with st.expander(cat, expanded=False):
            for item in items:
                if st.button(
                    item,
                    key=f"curr_{item}",
                    use_container_width=True,
                    type="primary" if st.session_state.curriculum == item else "secondary",
                ):
                    st.session_state.curriculum = item
                    st.rerun()



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
