import streamlit as st

import streamlit as st

# Force a clean black background page configuration
st.set_page_config(
    page_title="NEXUS AI", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Custom CSS styling to make the background strictly black and fonts completely sans-serif
import streamlit as st
import requests
from anthropic import Anthropic

# 1. Page Configuration
st.set_page_config(
    page_title="S2 Math Guard AI & Online Dictionary",
    page_icon="📐",
    layout="centered"
)

# 2. Initialize Anthropic Client
if "ANTHROPIC_API_KEY" in st.secrets:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
elif "anthropic_key" in st.session_state:
    api_key = st.session_state["anthropic_key"]
else:
    api_key = ""

# --- SIDEBAR FOR API KEY ---
with st.sidebar:
    st.header("Settings")
    if not api_key:
        user_key = st.text_input("Enter Anthropic API Key:", type="password")
        if user_key:
            st.session_state["anthropic_key"] = user_key
            st.rerun()
    else:
        st.success("Anthropic API Key Loaded!")

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
st.title("📐 S2 Math Guard: Smart Online Dictionary Lookup")
st.write("Looks up any word online, checks if it belongs in S2 Math, and blocks non-math terms.")

# Inputs
search_word = st.text_input("Enter a word to look up (e.g., 'Hypotenuse', 'Matrix', 'Photosynthesis'):")
target_lang = st.selectbox("Choose Local Translation Language:", ["Luganda", "Kiswahili"])

if st.button("Process & Guard Word"):
    if not api_key:
        st.error("Please add your Anthropic API Key in the sidebar.")
    elif not search_word:
        st.warning("Please type a word first.")
    else:
        with st.spinner("Fetching from online dictionary and validating..."):
            # Step 1: Hit the live online dictionary API
            online_definition = fetch_online_dictionary(search_word)
            
            if not online_definition:
                st.error(f"Could not find the word '{search_word}' in the online dictionary database.")
            else:
                # Step 2: Use Claude to act as a Gatekeeper & analyze if it's a math term
                client = Anthropic(api_key=api_key)
                
                guard_prompt = f"""
                You are a security gatekeeper for a Uganda Senior Two (S2) Mathematics application.
                Your task is to analyze the following word and its dictionary definition to see if it is a relevant mathematical or business math term.
                
                Word: {search_word}
                Online Dictionary Definition: 
                {online_definition}
                
                CRITICAL INSTRUCTIONS:
                1. Determine if this word is a mathematical term or highly relevant to high school business/science mathematics.
                2. If it is NOT a math term (e.g., it is a biology, history, or everyday word like 'photosynthesis' or 'kitchen'), you must output exactly: "BLOCKED: NOT A MATH TERM" and state why.
                3. If it IS a valid mathematical term, translate the term and its concept safely into {target_lang}, explain its definition in an easy S2 style, and show its common high school formula if applicable.
                """
                
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

