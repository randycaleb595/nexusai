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
    "Luganda":    "LU  Luganda",
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
    "math","algebra","calculus","geometry","fraction","integer","equation","theorem","product","summation"
    "matrix","vector","derivative","integral","angle","triangle","polygon","arithmetic","quadratic"
    "trigonometry","ratio","percent","probability","statistics","function","graph","+","-","=","math_contest"
    "exponent","logarithm","prime","factor","division","multiplier","sum","subtraction","factorial"
    "addition","multiplication","number","digit","set","proof","limit","series","/","vector","equation","theorem",
    "sequence","polynomial","quadratic","linear","circle","sphere","cube","parabola","scale","solution"
    "what","how","why","explain","solve","find","calculate","show","define","mean","translation",
    "is","are","does","example","formula","rule","property","simplify","expand","plus", "minus",
]
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
    },

    "Luganda": {
        "tagline": "Ekibalo Kyanguyiziddwa",
        "language": "🌐 Olulimi",
        "select_language": "Londa olulimi",
        "curricula": "📚 Enteekateeka y'Okusoma",
        "new_chat": "➕ Okunyumya Okuggya",
        "thinking": "Nexus alowooza...",
        "no_answer": "Nsonyiwa, tewali kyaddamu.",
        "http_error": "❌ Waliwo ensobi",
        "network_error": "❌ Ensobi ku mutimbagano",
    }
}

def t(key):
    return UI_TEXT[st.session_state.lang][key]
    
WELCOME_MESSAGES = {
    "English":   "👋 Hi! I'm **Caesura Tutor** — your friendly math tutor. Ask me anything about maths and I'll explain it simply. Try: *\"What is a fraction?\"* or *\"How do I solve 2x + 3 = 7?\"*",
    "Kiswahili": "👋 Habari! Mimi ni **Caesura Tutor** — mwalimu wako wa hisabati. Niulize chochote kuhusu hisabati!",
    "French":    "👋 Bonjour! Je suis **Caesura Tutor** — votre tuteur en mathématiques. Posez-moi n'importe quelle question!",
    "Chinese":   "👋 你好！我是 **Caesura Tutor** — 你的数学辅导老师。问我任何数学问题！",
    "Arabic":    "👋 مرحباً! أنا **Caesura Tutor** — مدرسك للرياضيات. اسألني أي سؤال!",
    "German":    "👋 Hallo! Ich bin **Caesura Tutor** — dein Mathe-Tutor. Frag mich alles!",
    "Luganda":   "👋 Ki kati! Nze **Caesura Tutor** — omusomesa wo ow'okubala. Mbuuza kyonna ky'oyagala!"
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

if "authed" not in st.session_state:
    st.session_state.authed = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "lang" not in st.session_state:
    st.session_state.lang = "English"
if "curriculum" not in st.session_state:
    st.session_state.curriculum = "Illustrative Mathematics (IM)"

lang = st.session_state.lang
curriculum = st.session_state.curriculum

with st.sidebar:
    if st.session_state.get("user_email"):
        st.markdown(f"<small style='color:#00FF0080'>👋 {st.session_state.user_email}</small>", unsafe_allow_html=True)

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
        st.session_state.messages = []
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
        st.session_state.messages = []
        st.rerun()
    if len(st.session_state.messages) > 0:
        chat_export = ""
        for m in st.session_state.messages:
            role = "Student" if m["role"] == "user" else "Caesura Tutor"
            chat_export += f"{role}: {m['content']}\n\n"
            
        st.download_button(
            label="📥 Download Notes",
            data=chat_export,
            file_name="nexus_math_notes.txt",
            mime="text/plain",
            use_container_width=True
        )      

    st.markdown("---")


if not st.session_state.messages:
    st.markdown(f"<h1 style='text-align:center;font-size:3.5rem;letter-spacing:0.3em;color:#00FF00'>CAESURA TUTOR</h1>", unsafe_allow_html=True)
    st.markdown(
    f"<p style='text-align:center;color:#00FF0080'>{t('tagline')} &nbsp;·&nbsp; {curriculum}</p>",
    unsafe_allow_html=True,
)
    st.markdown("")
    with st.chat_message("assistant"):
        st.markdown(WELCOME_MESSAGES[lang])
else:
    st.markdown(f"<h4 style='color:#00FF00;letter-spacing:0.2em'>CAESURA TUTOR</h4>", unsafe_allow_html=True)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


def ask_nexus(query, history, curriculum, lang):
    try:
        resp = requests.post(
            ASK_NEXUS_URL,
            json={"query": query, "history": history,
                  "curriculum": curriculum, "lang": lang},
            timeout=120,
        )
        if resp.status_code != 200:
            return f"{t('http_error')} (HTTP {resp.status_code})."
        data = resp.json()
        return data.get("answer") or t("no_answer")
    except requests.exceptions.RequestException as e:
        return f"{t('network_error')}: `{e}`"
    except Exception as e:
        return f"❌ Error: `{e}`"


user_input = st.chat_input(PLACEHOLDER_MAP.get(lang, "Ask a math question..."))

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
        history = []
        msgs = [m for m in st.session_state.messages[:-1]]
        for i, m in enumerate(msgs):
            if m["role"] == "user" and i + 1 < len(msgs) and msgs[i+1]["role"] == "assistant":
                history.append({"question": m["content"], "answer": msgs[i+1]["content"]})
        history = history[-6:]

        with st.chat_message("assistant"):
            with st.spinner(t("thinking")):
                answer = ask_nexus(query, history, curriculum, lang)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
