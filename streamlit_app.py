import streamlit as st
import requests

APP_DOMAIN = "https://nexusai123.base44.app"
ASK_CAESURA_URL = f"{APP_DOMAIN}/functions/askNexus"

LANG_LABELS = {
    "English":   "🇬🇧 English",
    "Kiswahili": "🇰🇪 Kiswahili",
    "French":    "🇫🇷 French",
    "Chinese":   "🇨🇳 Chinese",
    "Arabic":    "🇸🇦 Arabic",
    "German":    "🇩🇪 German",
    "Luganda":   "LU  Luganda",
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
    "math","algebra","calculus","geometry","fraction","integer","equation",
    "theorem","product","summation","matrix","vector","derivative","integral",
    "angle","triangle","polygon","arithmetic","quadratic","trigonometry",
    "ratio","percent","probability","statistics","function","graph",
    "exponent","logarithm","prime","factor","division","sum","subtraction",
    "factorial","addition","multiplication","number","digit","set","proof",
    "limit","series","polynomial","linear","circle","sphere","cube","parabola",
    "scale","formula","simplify","expand","plus","minus","solve","find",
    "calculate","show","define","mean","example","rule","property",
]

UI_TEXT = {
    "English": {
        "tagline": "Math Made Easier",
        "language": "🌐 Language",
        "select_language": "Select language",
        "curricula": "📚 Curricula",
        "new_chat": "➕ New Chat",
        "thinking": "Caesura is thinking...",
        "no_answer": "Sorry, no answer returned.",
        "http_error": "❌ Something went wrong",
        "network_error": "❌ Network error",
    },
    "Kiswahili": {
        "tagline": "Hisabati Imerahisishwa",
        "language": "🌐 Lugha",
        "select_language": "Chagua lugha",
        "curricula": "📚 Mitaala",
        "new_chat": "➕ Mazungumzo Mapya",
        "thinking": "Caesura anafikiria...",
        "no_answer": "Samahani, hakuna jibu lililopatikana.",
        "http_error": "❌ Hitilafu imetokea",
        "network_error": "❌ Hitilafu ya mtandao",
    },
    "French": {
        "tagline": "Les maths rendues faciles",
        "language": "🌐 Langue",
        "select_language": "Choisir une langue",
        "curricula": "📚 Programmes",
        "new_chat": "➕ Nouvelle discussion",
        "thinking": "Caesura réfléchit...",
        "no_answer": "Désolé, aucune réponse n'a été trouvée.",
        "http_error": "❌ Une erreur est survenue",
        "network_error": "❌ Erreur réseau",
    },
    "Chinese": {
        "tagline": "让数学更简单",
        "language": "🌐 语言",
        "select_language": "选择语言",
        "curricula": "📚 课程体系",
        "new_chat": "➕ 新聊天",
        "thinking": "Caesura 正在思考...",
        "no_answer": "抱歉，没有返回答案。",
        "http_error": "❌ 出现错误",
        "network_error": "❌ 网络错误",
    },
    "Arabic": {
        "tagline": "الرياضيات أصبحت أسهل",
        "language": "🌐 اللغة",
        "select_language": "اختر اللغة",
        "curricula": "📚 المناهج",
        "new_chat": "➕ محادثة جديدة",
        "thinking": "Caesura يفكر...",
        "no_answer": "عذراً، لم يتم العثور على إجابة.",
        "http_error": "❌ حدث خطأ",
        "network_error": "❌ خطأ في الشبكة",
    },
    "German": {
        "tagline": "Mathematik leicht gemacht",
        "language": "🌐 Sprache",
        "select_language": "Sprache auswählen",
        "curricula": "📚 Lehrpläne",
        "new_chat": "➕ Neuer Chat",
        "thinking": "Caesura denkt nach...",
        "no_answer": "Entschuldigung, keine Antwort erhalten.",
        "http_error": "❌ Etwas ist schiefgelaufen",
        "network_error": "❌ Netzwerkfehler",
    },
    "Luganda": {
        "tagline": "Ekibalo Kyanguyiziddwa",
        "language": "🌐 Olulimi",
        "select_language": "Londa olulimi",
        "curricula": "📚 Enteekateeka y'Okusoma",
        "new_chat": "➕ Okunyumya Okuggya",
        "thinking": "Caesura alowooza...",
        "no_answer": "Nsonyiwa, tewali kyaddamu.",
        "http_error": "❌ Waliwo ensobi",
        "network_error": "❌ Ensobi ku mutimbagano",
    }
}

WELCOME_MESSAGES = {
    "English":   "👋 Hi! I'm **Caesura Tutor** — your friendly math tutor. Ask me anything about maths and I'll explain it simply. Try: *\"What is a fraction?\"* or *\"How do I solve 2x + 3 = 7?\"*",
    "Kiswahili": "👋 Habari! Mimi ni **Caesura Tutor** — mwalimu wako wa hisabati. Niulize chochote kuhusu hisabati!",
    "French":    "👋 Bonjour! Je suis **Caesura Tutor** — votre tuteur en mathématiques. Posez-moi n'importe quelle question!",
    "Chinese":   "👋 你好！我是 **Caesura Tutor** — 你的数学辅导老师。问我任何数学问题！",
    "Arabic":    "👋 مرحباً! أنا **Caesura Tutor** — مدرسك للرياضيات. اسألني أي سؤال!",
    "German":    "👋 Hallo! Ich bin **Caesura Tutor** — dein Mathe-Tutor. Frag mich alles!",
    "Luganda":   "👋 Ki kati! Nze **Caesura Tutor** — omusomesa wo ow'okubala. Mbuuza kyonna ky'oyagala!",
}

NOT_MATH_MESSAGES = {
    "English":   "⚠️ Please ask a math-related question (e.g. fractions, algebra, geometry).",
    "Kiswahili": "⚠️ Tafadhali uliza swali linalohusu hisabati.",
    "French":    "⚠️ Veuillez poser une question liée aux mathématiques.",
    "Chinese":   "⚠️ 请提出与数学相关的问题。",
    "Arabic":    "⚠️ يرجى طرح سؤال متعلق بالرياضيات.",
    "German":    "⚠️ Bitte stellen Sie eine mathematische Frage.",
    "Luganda":   "⚠️ Mukwano, baako ekibuuzo ky'okubala ky'obuuza.",
}

PLACEHOLDER_MAP = {
    "English": "Ask a math question...",
    "Kiswahili": "Uliza swali la hisabati...",
    "French": "Posez une question de maths...",
    "Chinese": "提问数学问题...",
    "Arabic": "اسأل سؤالاً رياضياً...",
    "German": "Stellen Sie eine Mathe-Frage...",
    "Luganda": "Baako ekibuuzo ky'okubala ky'obuuza...",
}


def t(key):
    return UI_TEXT[st.session_state.lang][key]


def is_math_query(text):
    """Check if the query contains math-related keywords."""
    lower = text.lower()
    return any(kw in lower for kw in MATH_KEYWORDS)


def ask_caesura(query, history, curriculum, lang):
    """Send the query to the Caesura backend and return the answer."""
    try:
        resp = requests.post(
            ASK_CAESURA_URL,
            json={
                "query": query,
                "history": history,
                "curriculum": curriculum,
                "lang": lang,
            },
            timeout=120,
        )
        if resp.status_code != 200:
            return f"{t('http_error')} (HTTP {resp.status_code})."
        data = resp.json()
        return data.get("answer") or data.get("response") or t("no_answer")
    except requests.exceptions.RequestException as e:
        return f"{t('network_error')}: `{e}`"
    except Exception as e:
        return f"❌ Error: `{e}`"



# ── Page config ──────────────────────────────────────────────
st.set_page_config(page_title="Caesura Tutor — Math Tutor", page_icon="🟢", layout="wide")

st.markdown("""
<style>
  html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #000000 !important; color: #ffffff;
  }
  [data-testid="stSidebar"] { background-color: #080808 !important; }
  [data-testid="stSidebar"] * { color: #ffffff; }
  h1, h2, h3 { color: #00FF00 !important; }
  .stChatMessage { background: #0d0d0d; border: 1px solid #00FF0026; border-radius: 12px; }
  .stButton>button { background: #00FF00; color: #000; font-weight: 700; border: none; border-radius: 8px; }
  .stButton>button:hover { filter: brightness(1.1); }
  .stSelectbox label, .stRadio label { color: #00FF00 !important; font-size: 11px; }
  .stTextInput>div>div>input, .stTextArea>div>div>textarea {
    background: #0a0a0a !important; border: 1px solid #00FF0033 !important;
    color: #fff !important; border-radius: 12px;
  }
  .stChatInputContainer { background: #0a0a0a; border-top: 1px solid #00FF0020; }
</style>
""", unsafe_allow_html=True)

# ── Session state (single initialization) ───────────────────
if "messages" not in st.session_state:
    st.session_[state.me](https://state.me)ssages = []
if "lang" not in st.session_state:
    st.session_state.lang = "English"
if "curriculum" not in st.session_state:
    st.session_state.curriculum = "Illustrative Mathematics (IM)"

lang = st.session_state.lang
curriculum = st.session_state.curriculum

# ── Sidebar ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🟢 CAESURA TUTOR")
    st.markdown(
        f"<small style='color:#00FF0080'>{t('tagline')}</small>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    st.markdown(f"#### {t('language')}")
    lang_choice = st.radio(
        t("select_language"),
        options=list(LANG_LABELS.keys()),
        format_func=lambda x: LANG_LABELS[x],
        index=list(LANG_LABELS.keys()).index(st.session_state.lang),
        label_visibility="collapsed",
    )
    if lang_choice != st.session_state.lang:
        st.session_state.lang = lang_choice
        st.session_[state.me](https://state.me)ssages = []
        st.rerun()

    st.markdown("---")

    st.markdown(f"#### {t('curricula')}")
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

    if st.button(UI_TEXT[st.session_state.lang]["new_chat"], use_container_width=True):
        st.session_[state.me](https://state.me)ssages = []
        st.rerun()

    if len(st.session_[state.me](https://state.me)ssages) > 0:
        chat_export = ""
        for m in st.session_[state.me](https://state.me)ssages:
            role = "Student" if m["role"] == "user" else "Caesura Tutor"
            chat_export += f"{role}: {m['content']}\n\n"
        st.download_button(
            label="📥 Download Notes",
            data=chat_export,
            file_name="caesura_math_notes.txt",
            mime="text/plain",
            use_container_width=True,
        )

    st.markdown("---")

# ── Main content area ───────────────────────────────────────
if not st.session_[state.me](https://state.me)ssages:
    st.markdown(
        "<h1 style='text-align:center;font-size:3.5rem;letter-spacing:0.3em;color:#00FF00'>CAESURA TUTOR</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='text-align:center;color:#00FF0080'>{t('tagline')} &nbsp;·&nbsp; {curriculum}</p>",
        unsafe_allow_html=True,
    )
    st.markdown("")
    with st.chat_message("assistant"):
        st.markdown(WELCOME_MESSAGES[lang])
else:
    st.markdown(
        "<h4 style='color:#00FF00;letter-spacing:0.2em'>CAESURA TUTOR</h4>",
        unsafe_allow_html=True,
    )
    for msg in st.session_[state.me](https://state.me)ssages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ── Single chat input ────────────────────────────────────────
query = st.chat_input(PLACEHOLDER_MAP.get(lang, "Ask a math question..."))

if query:
    query = query.strip()

    with st.chat_message("user"):
        st.markdown(query)
    st.session_[state.messages.app](https://state.messages.app)end({"role": "user", "content": query})

    if not is_math_query(query):
        err = NOT_MATH_MESSAGES[lang]
        with st.chat_message("assistant"):
            st.markdown(err)
        st.session_[state.messages.app](https://state.messages.app)end({"role": "assistant", "content": err})
    else:
        chat_history = build_history(st.session_[state.me](https://state.me)ssages[:-1])

        with st.chat_message("assistant"):
            with st.spinner(t("thinking")):
                answer = ask_caesura(query, chat_history, curriculum, lang)
                st.markdown(answer)
        st.session_[state.messages.app](https://state.messages.app)end({"role": "assistant", "content": answer})
