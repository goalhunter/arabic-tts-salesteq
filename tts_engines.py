import os
import time
import streamlit as st
from config import AZURE_DIR, ELEVEN_DIR, FACEBOOK_DIR
from utils import generate_filename, add_file_to_metadata

def azure_tts(text, dialect=None, original_text=None):
    """Generate speech using Azure TTS."""
    try:
        import azure.cognitiveservices.speech as speechsdk
        
        key = os.getenv("AZURE_API_KEY")
        region = os.getenv("AZURE_REGION", "eastus")
        
        if not key:
            st.error("Azure API key not found. Please check your .env file.")
            return None, 0
        
        speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
        speech_config.speech_synthesis_voice_name = "ar-SA-ZariyahNeural"
        
        # Generate unique filename
        type_prefix = "dialect" if dialect else ""
        if original_text:
            type_prefix = "translated"
        
        filename = generate_filename("azure", type_prefix)
        filepath = os.path.join(AZURE_DIR, filename)
        
        audio_cfg = speechsdk.AudioConfig(filename=filepath)
        synth = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_cfg)
        
        start_time = time.perf_counter()
        result = synth.speak_text_async(text).get()
        elapsed = time.perf_counter() - start_time
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            # Add to metadata
            add_file_to_metadata(filepath, "Azure", text, dialect, original_text)
            return filepath, elapsed
        else:
            st.error("Azure synthesis failed.")
            return None, 0
    except ImportError:
        st.error("Azure Speech SDK not installed. Try: pip install azure-cognitiveservices-speech")
        return None, 0
    except Exception as e:
        st.error(f"Azure TTS error: {str(e)}")
        return None, 0

def elevenlabs_tts(text, dialect=None, original_text=None):
    """Generate speech using ElevenLabs TTS."""
    try:
        from elevenlabs import VoiceSettings
        from elevenlabs.client import ElevenLabs
        
        key = os.getenv("ELEVENLABS_API_KEY")
        if not key:
            st.error("ElevenLabs API key not found. Please check your .env file.")
            return None, 0
        
        client = ElevenLabs(api_key=key)
        
        # Generate unique filename
        type_prefix = "dialect" if dialect else ""
        if original_text:
            type_prefix = "translated"
            
        filename = generate_filename("eleven", type_prefix, ".mp3")
        filepath = os.path.join(ELEVEN_DIR, filename)
        
        start_time = time.perf_counter()
        response = client.text_to_speech.convert(
            voice_id="pNInz6obpgDQGcFmaJgB",
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_turbo_v2_5",
            voice_settings=VoiceSettings(stability=0.0, similarity_boost=1.0, style=0.0, use_speaker_boost=True, speed=1.0),
        )
        
        with open(filepath, "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)
                    
        elapsed = time.perf_counter() - start_time
        
        # Add to metadata
        add_file_to_metadata(filepath, "ElevenLabs", text, dialect, original_text)
        return filepath, elapsed
    except ImportError:
        st.error("ElevenLabs library not installed. Try: pip install elevenlabs")
        return None, 0
    except Exception as e:
        st.error(f"ElevenLabs TTS error: {str(e)}")
        return None, 0

def facebook_tts(text, model, tokenizer, dialect=None, original_text=None):
    """Generate speech using Facebook MMS-TTS."""
    try:
        import torch
        import soundfile as sf
        
        if model is None or tokenizer is None:
            loading_placeholder = st.empty()
            loading_placeholder.info("Loading Facebook MMS-TTS model... This may take a moment.")
            
            from transformers import VitsModel, AutoTokenizer
            model = VitsModel.from_pretrained("facebook/mms-tts-ara")
            tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-ara")
            
            loading_placeholder.empty()
        
        inputs = tokenizer(text, return_tensors="pt")
        
        start_time = time.perf_counter()
        with torch.no_grad():
            waveform = model(**inputs).waveform.squeeze().cpu().numpy()
        
        # Generate unique filename
        type_prefix = "dialect" if dialect else ""
        if original_text:
            type_prefix = "translated"
            
        filename = generate_filename("facebook", type_prefix)
        filepath = os.path.join(FACEBOOK_DIR, filename)
        
        sf.write(filepath, waveform, model.config.sampling_rate)
        elapsed = time.perf_counter() - start_time
        
        # Add to metadata
        add_file_to_metadata(filepath, "Facebook MMS-TTS", text, dialect, original_text)
        return filepath, elapsed
    except ImportError:
        st.error("Required libraries not installed. Try: pip install transformers torch soundfile")
        return None, 0
    except Exception as e:
        st.error(f"Facebook TTS error: {str(e)}")
        return None, 0