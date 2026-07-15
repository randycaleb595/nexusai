import streamlit as st
from google import genai  # <─── USE THIS INSTEAD OF .generativeai
# ─── CONFIG ───────────────────────────────────────────────────────────────────
GEMINI_API_KEY = "AQ.Ab8RN6Lv2L7kXrFPYwdBi4zWWHSdzv_GBN6Vr4qShTw9EixZmg"
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

WELCOME_MESSAGES = {
    "English":   "👋 Hi! I'm **Nexus AI** — your friendly math tutor. Ask me anything about maths and I'll explain it simply. Try: *\"What is a fraction?\"* or *\"How do I solve 2x + 3 = 7?\"*",
    "Kiswahili": "👋 Habari! Mimi ni **Nexus AI** — mwalimu wako wa hisabati. Niulize chochote kuhusu hisabati!",
    "French":    "👋 Bonjour! Je suis **Nexus AI** — votre tuteur en mathématiques. Posez-moi n'importe quelle question!",
    "Chinese":   "👋 你好！我是 **Nexus AI** — 你的数学辅导老师。问我任何数学问题！",
    "Arabic":    "👋 مرحباً! أنا **Nexus AI** — مدرسك للرياضيات. اسألني أي سؤال!",
    "German":    "👋 Hallo! Ich bin **Nexus AI** — dein Mathe-Tutor. Frag mich alles!",
}

NOT_MATH_MESSAGES = {
    "English":   "⚠️ Please ask a math-related question (e.g. fractions, algebra, geometry).",
    "Kiswahili": "⚠️ Tafadhali uliza swali linalohusu hisabati.",
    "French":    "⚠️ Veuillez poser une question liée aux mathématiques.",
    "Chinese":   "⚠️ 请提出与数学相关的问题。",
    "Arabic":    "⚠️ يرجى طرح سؤال متعلق بالرياضيات.",
    "German":    "⚠️ Bitte stellen Sie eine mathematische Frage.",
}

# ─── PAGE SETUP ───────────────────────────────────────────────────────────────
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

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "lang" not in st.session_state:
    st.session_state.lang = "English"
if "curriculum" not in st.session_state:
    st.session_state.curriculum = "Illustrative Mathematics (IM)"

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
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

    st.markdown("---")

    # New Chat button
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ─── MAIN AREA ────────────────────────────────────────────────────────────────
lang = st.session_state.lang
curriculum = st.session_state.curriculum

# Show hero when no messages yet
if not st.session_state.messages:
    st.markdown(f"<h1 style='text-align:center;font-size:3.5rem;letter-spacing:0.3em;color:#00FF00'>NEXUS AI</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;color:#00FF0080'>Math Made Easier &nbsp;·&nbsp; 📌 {curriculum}</p>", unsafe_allow_html=True)
    st.markdown("")
    # Show welcome message bubble
    with st.chat_message("assistant"):
        st.markdown(WELCOME_MESSAGES[lang])
else:
    st.markdown(f"<h4 style='color:#00FF00;letter-spacing:0.2em'>NEXUS AI</h4>", unsafe_allow_html=True)
    # Render chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ─── GEMINI CALL ──────────────────────────────────────────────────────────────
def ask_gemini(query, history, curriculum, lang):
    model = genai.GenerativeModel("gemini-2.0-flash")
    client = genai.Client(api_key=GEMINI_API_KEY)

    # Build conversation history
    gemini_history = []
    for h in history:
        gemini_history.append({"role": "user", "parts": [h["question"]]})
        gemini_history.append({"role": "model", "parts": [h["answer"]]})
    
    chat = model.start_chat(history=gemini_history)
    
    prompt = f"""You are Nexus AI, a friendly math tutor. The student is using the "{curriculum}" curriculum.

Explain this in the simplest way possible — like you are talking to a 12-year-old who is hearing this for the first time.
- Use short sentences.
- Avoid big technical words. If you must use one, explain it right away in simple words.
- Use a real-life example (like food, money, sports, or everyday things) to explain the idea.
- If there is a formula, show it clearly and then explain each part in plain English.
- End with one encouraging line.

Student's question or topic: "{query}"

Language to respond in: {lang}"""
    
    response = chat.send_message(prompt)
    return response.text

# ─── CHAT INPUT ───────────────────────────────────────────────────────────────
placeholder_map = {
    "English": "Ask a math question...",
    "Kiswahili": "Uliza swali la hisabati...",
    "French": "Posez une question de maths...",
    "Chinese": "提问数学问题...",
    "Arabic": "اسأل سؤالاً رياضياً...",
    "German": "Stellen Sie eine Mathe-Frage...",
}

user_input = st.chat_input(placeholder_map.get(lang, "Ask a math question..."))

if user_input:
    query = user_input.strip()
    lower = query.lower()
    is_math = any(kw in lower for kw in MATH_KEYWORDS)

    # Show user message
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    if not is_math:
        err = NOT_MATH_MESSAGES[lang]
        with st.chat_message("assistant"):
            st.warning(err)
        st.session_state.messages.append({"role": "assistant", "content": err})
    else:
        # Build history for context (last 6 exchanges)
        history = []
        msgs = [m for m in st.session_state.messages[:-1]]  # exclude just-added user msg
        for i, m in enumerate(msgs):
            if m["role"] == "user" and i + 1 < len(msgs) and msgs[i+1]["role"] == "assistant":
                history.append({"question": m["content"], "answer": msgs[i+1]["content"]})
        history = history[-6:]

        with st.chat_message("assistant"):
            with st.spinner("Nexus is thinking..."):
                try:
                    answer = ask_gemini(query, history, curriculum, lang)
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    err = f"❌ Error: {str(e)}"
                    st.error(err)
                    st.session_state.messages.append({"role": "assistant", "content": err})
  
