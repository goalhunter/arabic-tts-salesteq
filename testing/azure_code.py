import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os

load_dotenv()

# Replace with your Azure key & region
speech_key   = os.getenv("AZURE_API_KEY")
service_region = "eastus"

# Configure speech
speech_config = speechsdk.SpeechConfig(
    subscription=speech_key,
    region=service_region
)
speech_config.speech_synthesis_voice_name = "ar-SA-ZariyahNeural"  # Saudi Arabic neural voice
speech_config.set_speech_synthesis_output_format(
    speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm
)

# Create synthesizer
synthesizer = speechsdk.SpeechSynthesizer(
    speech_config=speech_config,
    audio_config=speechsdk.AudioConfig(filename="zariyah_output.wav")
)

# Synthesize
text = "السيارة مزودة بمحرك توربو مزدوج سعة 3.0 لتر لتحقيق أداء قوي واقتصاد في استهلاك الوقود."
result = synthesizer.speak_text_async(text).get()

if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("✅ Saved Azure Zariyah output to zariyah_output.wav")
else:
    print(f"❌ Speech synthesis failed: {result.reason}")
