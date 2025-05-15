import streamlit as st

# Load Facebook MMS-TTS model at app startup
@st.cache_resource(show_spinner=False)
def load_facebook_model():
    """Load the Facebook MMS-TTS model."""
    try:
        from transformers import VitsModel, AutoTokenizer
        model = VitsModel.from_pretrained("facebook/mms-tts-ara")
        tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-ara")
        return model, tokenizer, True
    except Exception as e:
        return None, None, False

# Load English-to-Arabic translation model
@st.cache_resource(show_spinner=False)
def load_translation_model():
    """Load the translation model."""
    try:
        from transformers import MarianMTModel, MarianTokenizer
        model_name = "Helsinki-NLP/opus-mt-en-ar"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        return model, tokenizer, True
    except Exception as e:
        return None, None, False