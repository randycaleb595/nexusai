import random
import requests

# 1. Page Configuration
st.set_page_config(page_title="Nexus AI", page_icon="📐", layout="wide")

# 2. Custom Matrix/Minimalist Theme Styling (Black background, Green headers, White results, Sans-Serif font)
st.markdown("""
    <style>
    /* Main body background and font */
    .stApp, [data-testid="stSidebar"] {
        background-color: #000000 !important;
        font-family: 'Segoe UI', Helvetica, Arial, sans-serif !important;
    }
    
    /* Global text color override for generic text elements */
    h1, h2, h3, h4, h5, h6, p, span, label, li {
        font-family: 'Segoe UI', Helvetica, Arial, sans-serif !important;
    }
    
    /* Branding Header & Subtitles */
    .brand-title {
        color: #00FF00;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .brand-subtitle {
        color: #00FF00;
        font-size: 1.5rem;
        margin-top: 0px;
        margin-bottom: 20px;
        opacity: 0.8;
    }
    .welcome-sign {
        color: #00FF00;
        font-size: 1.8rem;
        font-weight: 600;
        margin-top: 10px;
    }
    
    /* Motivation and regular content text color */
    .motivation-text {
        color: #FFFFFF;
        font-style: italic;
        margin-bottom: 30px;
    }
    
    /* Output text and container styling */
    .result-container {
        color: #FFFFFF !important;
        background-color: #111111;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #333333;
        margin-top: 20px;
    }
    
    .result-header {
        color: #00FF00 !important;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    /* Sidebar text colors */
    section[data-testid="stSidebar"] .css-ng1t4o, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] label {
        color: #00FF00 !important;
    }
    
    /* Custom button overrides */
    div.stButton > button {
        background-color: #111111;
        color: #00FF00;
        border: 1px solid #00FF00;
    }
    div.stButton > button:hover {
        background-color: #00FF00;
        color: #000000;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Multilingual Dictionary Data
TRANSLATIONS = {
    "English": {
        "subtitle": "MATH MADE EASIER", "welcome": "Welcome to the future of mathematics calculation.",
        "search_label": "Ask Nexus AI a math definition or concept:", "btn": "Search",
        "curriculum_lbl": "Select a Math Curriculum Framework:", "not_math": "⚠️ Error: Nexus AI only processes mathematics-related queries. Please try again with a math term (e.g., 'Calculus', 'Fraction', 'Matrix').",
        "def_found": "Definition Found:", "source": "Source: Free Dictionary API"
    },
    "Kiswahili": {
        "subtitle": "HISABATI IMEFANYWA RAHISI", "welcome": "Karibu kwenye mustakabali wa hesabu.",
        "search_label": "Uliza Nexus AI fasili au dhana ya hisabati:", "btn": "Tafuta",
        "curriculum_lbl": "Chagua Mfumo wa Mtaala wa Hisabati:", "not_math": "⚠️ Makosa: Nexus AI inashughulikia maswali yanayohusiana na hisabati pekee. Tafadhali jaribu tena kwa neno la hisabati.",
        "def_found": "Tafsiri Imepatikana:", "source": "Chanzo: Free Dictionary API"
    },
    "French": {
        "subtitle": "LES MATHÉMATIQUES RENDUES PLUS FACILES", "welcome": "Bienvenue dans le futur du calcul mathématique.",
        "search_label": "Demandez à Nexus AI une définition ou un concept mathématique:", "btn": "Chercher",
        "curriculum_lbl": "Sélectionnez un programme de mathématiques:", "not_math": "⚠️ Erreur: Nexus AI ne traite que les requêtes liées aux mathématiques. Veuillez réessayer avec un terme mathématique.",
        "def_found": "Définition Trouvée:", "source": "Source: Free Dictionary API"
    },
    "Chinese": {
        "subtitle": "让数学更简单", "welcome": "欢迎来到数学计算的未来。",
        "search_label": "向 Nexus AI 询问数学界定或概念:", "btn": "搜索",
        "curriculum_lbl": "选择数学课程体系:", "not_math": "⚠️ 错误：Nexus AI 仅处理与数学相关的查询。请使用数学术语重试。",
        "def_found": "找到定义:", "source": "来源: Free Dictionary API"
    },
    "Arabic": {
        "subtitle": "الرياضيات أصبحت أسهل", "welcome": "مرحبًا بك في مستقبل الحسابات الرياضية.",
        "search_label": "اسأل نكسس عن تعريف أو مفهوم رياضي:", "btn": "بحث",
        "curriculum_lbl": "اختر إطار منهج الرياضيات:", "not_math": "⚠️ خطأ: نكسس يقوم بمعالجة الاستفسارات المتعلقة بالرياضيات فقط. يرجى المحاولة مرة أخرى باستخدام مصطلح رياضي.",
        "def_found": "تم العثور على التعريف:", "source": "المصدر: Free Dictionary API"
    },
    "German": {
        "subtitle": "MATHEMATIK EINFACH GEMACHT", "welcome": "Willkommen in der Zukunft der mathematischen Berechnung.",
        "search_label": "Fragen Sie Nexus AI nach einer mathematischen Definition:", "btn": "Suchen",
        "curriculum_lbl": "Wählen Sie einen Mathematiklehrplan:", "not_math": "⚠️ Fehler: Nexus AI verarbeitet nur mathematische Anfragen. Bitte versuchen Sie es mit einem mathematischen Begriff erneut.",
        "def_found": "Definition gefunden:", "source": "Quelle: Free Dictionary API"
    }
}

MOTIVATION_STATEMENTS = [
    "“Mathematics is not about numbers, equations, computations, or algorithms: it is about understanding.” — William Paul Thurston",
    "“Pure mathematics is, in its way, the poetry of logical ideas.” — Albert Einstein",
    "“Obvious’ is the most dangerous word in mathematics.” — Eric Temple Bell",
    "“Mathematics reveals its secrets only to those who approach it with pure love, for its beauty.” — Archimedes",
    "“Go down deep enough into anything and you will find mathematics.” — Dean Schlicter"
]

CURRICULUMS = {
    "Global & Institutional Frameworks": [
        "Illustrative Mathematics (IM)", "Cambridge International Curriculum (IGCSE / A-Levels)", 
        "International Baccalaureate (IB Math)", "Uganda NCDC Competency-Based Curriculum", 
        "Agile Mind Common Core Math", "Big Ideas Math"
    ],
    "Conceptual & Mastery-Based Curricula": [
        "Singapore Math (Math in Focus)", "Math-U-See", "Math Academy", 
        "Math Mammoth", "RightStart Mathematics", "CTCMath", "Ace Academy Math", "Miquon Math"
    ],
    "Spiral & Repetition-Based Curricula": [
        "Saxon Math", "Everyday Mathematics", "Horizons Math", "Go Math!", "Think Academy Math"
    ],
    "Digital & Self-Paced Platforms": [
        "Khan Academy", "Teaching Textbooks", "Beast Academy", "Prodigy Math", "IXL Learning Math", "ALEKS Math", "Zearn Math", "Elephant Learning"
    ],
    "Specialized & Advanced Programs": [
        "Russian School of Mathematics (RSM)", "Life of Fred Math"
    ]
}

# 4. Math Keyword Filter Database
MATH_KEYWORDS = [
    "math", "algebra", "calculus", "geometry", "fraction", "integer", "equation", "theorem", 
    "matrix", "vector", "derivative", "integral", "angle", "triangle", "polygon", "arithmetic", 
    "trigonometry", "ratio", "percent", "probability", "statistics", "function", "graph", 
    "exponent", "logarithm", "prime", "factor", "division", "multiplier", "sum", "subtraction"
]

# 5. Sidebar Navigation (Language & Curriculums)
st.sidebar.markdown("<h2 style='color:#00FF00;'>🌐 Preferences</h2>", unsafe_allow_html=True)
selected_lang = st.sidebar.selectbox("Language / Lugha / Langue / 语言", list(TRANSLATIONS.keys()))
text = TRANSLATIONS[selected_lang]

st.sidebar.markdown("---")
st.sidebar.markdown(f"<h3 style='color:#00FF00;'>📚 {text['curriculum_lbl']}</h3>", unsafe_allow_html=True)

selected_category = st.sidebar.selectbox("Category", list(CURRICULUMS.keys()))
selected_curriculum = st.sidebar.selectbox("Curriculum Variant", CURRICULUMS[selected_category])

# 6. Main Interface Render
st.markdown("<p class='brand-title'>NEXUS AI</p>", unsafe_allow_html=True)
st.markdown(f"<p class='brand-subtitle'>{text['subtitle']}</p>", unsafe_allow_html=True)

st.markdown(f"<p class='welcome-sign'>✨ {text['welcome']}</p>", unsafe_allow_html=True)

# Generate a consistent random math quote for the session
if 'quote' not in st.session_state:
    st.session_state.quote = random.choice(MOTIVATION_STATEMENTS)
st.markdown(f"<p class='motivation-text'>{st.session_state.quote}</p>", unsafe_allow_html=True)

st.markdown(f"<p style='color:#00FF00;'>📌 Active Curriculum Track: <b>{selected_curriculum}</b></p>", unsafe_allow_html=True)

# 7. Query Processing Engine
user_query = st.text_input(text['search_label'], placeholder="e.g., Matrix")

if st.button(text['btn']):
    if user_query:
        query_lower = user_query.lower().strip()
        
        # Guardrail: Check if query relates to math keywords
        is_math_related = any(keyword in query_lower for keyword in MATH_KEYWORDS) or len(query_lower) <= 2
        
        if not is_math_related:
            st.markdown(f"<div class='result-container' style='color:#FF3333 !important;'>{text['not_math']}</div>", unsafe_allow_html=True)
        else:
            # Query Public Online Dictionary API
            with st.spinner("Connecting to online dictionary..."):
                try:
                    response = requests.get(f"https://dictionaryapi.dev{query_lower}")
                    if response.status_state == 200 or response.status_code == 200:
                        data = response.json()
                        meanings = data[0]['meanings']
                        
                        # Format the API response nicely in white text inside container
                        output_html = f"<div class='result-container'><div class='result-header'>{text['def_found']} '{user_query.capitalize()}'</div><ul>"
                        
                        for meaning in meanings:
                            part_of_speech = meaning.get('partOfSpeech', 'noun')
                            definition = meaning['definitions'][0]['definition']
                            output_html += f"<li><b>[{part_of_speech}]</b> {definition}</li>"



# Custom CSS styling to make the background strictly black and fonts completely sans-serif 

# 1. Page Configuration
st.set_page_config(
    page_title="NEXUS AI", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# 2. Initialize Gemini API Configuration
# First, look for the key in Streamlit Secrets, then check Session State, else use your fallback key
if "Gemini API Key" in st.secrets:
    gemini_key = st.secrets["Gemini API Key"]
elif "gemini_key" in st.session_state and st.session_state["gemini_key"]:
    gemini_key = st.session_state["gemini_key"]
else:
    # Your provided fallback key
    gemini_key = ""

# --- SIDEBAR FOR API KEY CONFIGURATION ---
with st.sidebar:
    st.header("Settings")
    
    # Text input to let users manually change or paste a new Gemini Key if needed
    user_key = st.text_input(
        "Gemini API Key:", 
        value=gemini_key, 
        type="password",
        help="Paste your Google AI Studio Gemini API key here."
    )
    
    # If the user edits the key manually in the sidebar, update the active key instantly
    if user_key != gemini_key:
        st.session_state["gemini_key"] = user_key
        st.rerun()
        
    if gemini_key:
        st.success("Gemini API Key Loaded!")
    else:
        st.warning("Please provide a valid Gemini API Key to activate NEXUS AI.")


# --- HELPER FUNCTION: CALL ONLINE DICTIONARY ---
def fetch_online_dictionary(word: str):
    """Fetches real-time definition data from an online dictionary API."""
    url = f"https://dictionaryapi.dev{word.strip().lower()}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # Extract basic definition text from the API payload
            definitions = []
            for meaning in data[0].get("meanings", []):
                part_of_speech = meaning.get("partOfSpeech", "noun")
                for item in meaning.get("definitions", []):
                    definitions.append(f"({part_of_speech}) {item.get('definition')}")
            return "\n".join(definitions)
        else:
            return None
    except Exception:
        return None

# --- MAIN APP UI ---
st.title("NEXUS AI")
st.write("Looks up any word online, checks if it belongs in Math, and blocks non-math terms.")

# Inputs
search_word = st.text_input("Enter a word to look up")

if st.button("Process & Guard Word"):
    elif not search_word:
        st.warning("Please type a word first.")
    else:
        with st.spinner("Fetching from online dictionary and validating..."):
            # Step 1: Hit the live online dictionary API
            online_definition = fetch_online_dictionary(search_word)
            
            if not online_definition:
                st.error(f"Could not find the word '{search_word}' in the online dictionary database."
                Word: {search_word}
                Online Dictionary Definition: 
                {online_definition}
                
                CRITICAL INSTRUCTIONS:
                1. Determine if this word is a mathematical term or highly relevant to high school business/science mathematics.
                2. If it is NOT a math term (e.g., it is a biology, history, or everyday word like 'photosynthesis' or 'kitchen'), you must output exactly: "BLOCKED: NOT A MATH TERM" and state why.
                3. If it IS a valid mathematical term, 
                
                
                try:
                    message = client.messages.create(
                        model="claude-3-5-sonnet-20241022",
                        max_tokens=800,
                        messages=[{"role": "user", "content": guard_prompt}]
                    )
                    
                    ai_response = message.content[0].text
                    
                    # Step 3: Check if Claude triggered the filter blocking
                    if "BLOCKED" in ai_response:
                        st.error("🛑 Content Filter Triggered")
                        st.write(ai_response)
                    else:
                        st.success(f"✅ Verified Math Term: {search_word}")
                        st.write("### 📖 S2 Curriculum Multi-lingual Entry")
                        st.write(ai_response)
                        
                        # Preview of the raw online source data
                        with st.expander("View Raw Online Source Data"):
                            st.caption(online_definition)
                            
                except Exception as e:
                    st.error(f"AI Check Failed: {str(e)}")

