import streamlit as st
import os
from dotenv import load_dotenv

# Set page config must be the first Streamlit command
st.set_page_config(page_title="Arabic TTS", page_icon="🔊", layout="wide")

# Load environment variables
load_dotenv()

# Import internal modules
from config import SPEECH_DIR, AZURE_DIR, ELEVEN_DIR, FACEBOOK_DIR
from utils import ensure_directories, load_metadata
from models import load_facebook_model, load_translation_model
from ui_components import render_sidebar, render_arabic_input_tab, render_translation_tab

# Create necessary directories
ensure_directories([SPEECH_DIR, AZURE_DIR, ELEVEN_DIR, FACEBOOK_DIR])

# Load AI models
facebook_model, facebook_tokenizer, facebook_model_loaded = load_facebook_model()
translation_model, translation_tokenizer, translation_model_loaded = load_translation_model()

# Main app content
st.title("Arabic Text-to-Speech Comparison")

# Load metadata for file listing
metadata = load_metadata()
files = metadata.get("files", [])

# Render sidebar
render_sidebar(metadata, files)

# Create tabs for different input methods
tabs = st.tabs(["Arabic Input", "English-to-Arabic"])

with tabs[0]:
    render_arabic_input_tab(facebook_model, facebook_tokenizer)

with tabs[1]:
    render_translation_tab(translation_model, translation_tokenizer, facebook_model, facebook_tokenizer)

# App footer
st.markdown("---")
st.write("Arabic TTS Comparison Tool - © 2025")