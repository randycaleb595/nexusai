import streamlit as st

import streamlit as st


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

