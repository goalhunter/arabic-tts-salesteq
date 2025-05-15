import streamlit as st

def translate_english_to_arabic(text, translation_model=None, translation_tokenizer=None):
    """Translate English text to Arabic."""
    try:
        # Try using the local translation model first
        if translation_model is not None and translation_tokenizer is not None:
            import torch
            
            # Tokenize the text
            batch = translation_tokenizer([text], return_tensors="pt", padding=True, truncation=True, max_length=512)
            
            # Translate
            with torch.no_grad():
                translated = translation_model.generate(**batch)
            
            # Decode the translated text
            translated_text = translation_tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
            return translated_text
        else:
            # Fallback to online translation API
            import requests
            
            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                "client": "gtx",
                "sl": "en",
                "tl": "ar",
                "dt": "t",
                "q": text
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                # Extract the translated text from the response
                translation = response.json()[0][0][0]
                return translation
            else:
                raise Exception(f"Translation API failed: {response.status_code}")
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return None