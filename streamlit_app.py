import streamlit as st
import requests
APP_DOMAIN = "https://nexusai123.base44.app"
ASK_NEXUS_URL = f"{APP_DOMAIN}/functions/askNexus"
LANG_LABELS = {
    "English":   "🇬🇧 English",
    "Kiswahili": "🇰🇪 Kiswahili",
    "French":    "🇫🇷 French",
    "Chinese":   "🇨🇳 Chinese",
    "Arabic":    "🇸🇦 Arabic",
    "German":    "🇩🇪 German",
    "Luganda":   "LU Luganda",
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
    "math","algebra","calculus","geometry","add","subtract","fraction","integer","+","-","x","equation","theorem",
    "matrix","vector","derivative","integral","angle","triangle","polygon","arithmetic","plus","minus","divide by","summation",
    "trigonometry","ratio","percent","probability","statistics","function","graph",
    "exponent","logarithm","prime","factor","division","multiplier","sum","subtraction",
    "addition","multiplication","number","digit","set","proof","limit","series","love",
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
    "Luganda":   "👋 Mulamwa! Nze Nexus AI — omusomesa wo ow'ekibalo omwangu. Mbuuza kyonna ku kibalo era ngya kukinyonnyola mu ngeri ennyangu!",
}
NOT_MATH_MESSAGES = {
    "English":   "⚠️ Please ask a math-related question (e.g. fractions, algebra, geometry).",
    "Kiswahili": "⚠️ Tafadhali uliza swali linalohusu hisabati.",
    "French":    "⚠️ Veuillez poser une question liée aux mathématiques.",
    "Chinese":   "⚠️ 请提出与数学相关的问题。",
    "Arabic":    "⚠️ يرجى طرح سؤال متعلق بالرياضيات.",
    "German":    "⚠️ Bitte stellen Sie eine mathematische Frage.",
    "Luganda":   "⚠️ Mwattu buuza ekibuzo ku kibalo (okugeza: emiganyulo, algebra, oba geometry)",
}
UI_TEXT = {
    "English": {
        "tagline": "Math Made Easier",
        "language": "🌐 Language",
        "select_language": "Select language",
        "curricula": "📚 Curricula",
        "new_chat": "➕ New Chat",
        "thinking": "Nexus is thinking...",
        "no_answer": "Sorry, no answer returned.",
        "http_error": "❌ Something went wrong",
        "network_error": "❌ Network error",
        "welcome_user": "👋",
    },

    "Kiswahili": {
        "tagline": "Hisabati Imerahisishwa",
        "language": "🌐 Lugha",
        "select_language": "Chagua lugha",
        "curricula": "📚 Mitaala",
        "new_chat": "➕ Mazungumzo Mapya",
        "thinking": "Nexus anafikiria...",
        "no_answer": "Samahani, hakuna jibu lililopatikana.",
        "http_error": "❌ Hitilafu imetokea",
        "network_error": "❌ Hitilafu ya mtandao",
        "welcome_user": "👋",
    },

    "French": {
        "tagline": "Les maths rendues faciles",
        "language": "🌐 Langue",
        "select_language": "Choisir une langue",
        "curricula": "📚 Programmes",
        "new_chat": "➕ Nouvelle discussion",
        "thinking": "Nexus réfléchit...",
        "no_answer": "Désolé, aucune réponse n'a été trouvée.",
        "http_error": "❌ Une erreur est survenue",
        "network_error": "❌ Erreur réseau",
        "welcome_user": "👋",
    },

    "Chinese": {
        "tagline": "让数学更简单",
        "language": "🌐 语言",
        "select_language": "选择语言",
        "curricula": "📚 课程体系",
        "new_chat": "➕ 新聊天",
        "thinking": "Nexus 正在思考...",
        "no_answer": "抱歉，没有返回答案。",
        "http_error": "❌ 出现错误",
        "network_error": "❌ 网络错误",
        "welcome_user": "👋",
    },

    "Arabic": {
        "tagline": "الرياضيات أصبحت أسهل",
        "language": "🌐 اللغة",
        "select_language": "اختر اللغة",
        "curricula": "📚 المناهج",
        "new_chat": "➕ محادثة جديدة",
        "thinking": "نيكسس يفكر...",
        "no_answer": "عذراً، لم يتم العثور على إجابة.",
        "http_error": "❌ حدث خطأ",
        "network_error": "❌ خطأ في الشبكة",
        "welcome_user": "👋",
    },

    "German": {
        "tagline": "Mathematik leicht gemacht",
        "language": "🌐 Sprache",
        "select_language": "Sprache auswählen",
        "curricula": "📚 Lehrpläne",
        "new_chat": "➕ Neuer Chat",
        "thinking": "Nexus denkt nach...",
        "no_answer": "Entschuldigung, keine Antwort erhalten.",
        "http_error": "❌ Etwas ist schiefgelaufen",
        "network_error": "❌ Netzwerkfehler",
        "welcome_user": "👋",
    },

    "Luganda": {
        "tagline": "Ekibalo Kyanguyiziddwa",
        "language": "🌐 Olulimi",
        "select_language": "Londa olulimi",
        "curricula": "📚 Enteekateeka y'okusoma",
        "new_chat": "➕ Okunyumya Okuggya",
        "thinking": "Nexus alowooza...",
        "no_answer": "Nsonyiwa, tewali kyaddamu.",
        "http_error": "❌ Waliwo ensobi",
        "network_error": "❌ Ensobi ku mutimbagano",
        "welcome_user": "👋",
    },
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
    if st.session_state.get("user_email"):
        st.markdown(f"<small style='color:#00FF0080'>👋 {st.session_state.user_email}</small>", unsafe_allow_html=True)
    st.markdown("## 🟢 NEXUS AI")
st.markdown(
    f"<small style='color:#00FF0080'>{t('tagline')}</small>",unsafe_allow_html=True,
)
st.markdown("---")
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
st.markdown("#### 📚 Curricula")
for cat, items in CURRICULUMS.items():
    with st.expander(cat, expanded=False):
        for  
        item in items:
        if st.button(
                    item,
                    key=f"curr_{item}",
                    use_container_width=True,
                    type="primary" if st.session_state.curriculum == item else "secondary",
                ):
                    st.session_state.curriculum = item
                    st.rerun()
    st.markdown("---")
if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
lang = st.session_state.lang
curriculum = st.session_state.curriculum
if not st.session_state.messages:
    st.markdown(f"<h1 style='text-align:center;font-size:3.5rem;letter-spacing:0.3em;color:#00FF00'>NEXUS AI</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;color:#00FF0080'>Math Made Easier &nbsp;·&nbsp; 📌 {curriculum}</p>", unsafe_allow_html=True)
    st.markdown("")
    with st.chat_message("assistant"):
        st.markdown(WELCOME_MESSAGES[lang])
else:
    st.markdown(f"<h4 style='color:#00FF00;letter-spacing:0.2em'>NEXUS AI</h4>", unsafe_allow_html=True)
    # Render chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
def ask_nexus(query, history, curriculum, lang):
    """Calls the deployed Base44 askNexus function (built-in LLM, no API key)."""
    try:
        resp = requests.post(
            ASK_NEXUS_URL,
            json={"query": query, "history": history,
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
                answer = ask_nexus(query, history, curriculum, lang)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
