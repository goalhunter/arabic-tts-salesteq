from transformers import VitsModel, AutoTokenizer
import torch
import soundfile as sf
import time

# Load model & tokenizer
model = VitsModel.from_pretrained("facebook/mms-tts-ara")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-ara")

# A test sentence about a car’s technical specs
text = (
    "يتميز المحرك سداسي الأسطوانات بشاحن توربيني مزدوج سعة 3.0 لتر "
    "يولد قوة 400 حصان وعزم دوران 550 نيوتن·متر، وينقلها ناقل حركة ثنائي "
    "القابض بثماني سرعات، مع نظام تعليق هوائي قابل للتعديل لتحقيق توازن "
    "مثالي بين الراحة والثبات."
)

# Najdi
# text = (
#     "هالموتر جايب مكينه ست سلندر بشاحن تربو مزدوج سعة 3.0 لتر "
#     "يطلع 400 حصان وعزم دوران 550 نيوتن متر، ينقله قير ثنائي القابض "
#     "بثمان سرعات، ومعاه نظام تعليق هوائي تقدر تضبطه علشان يوازن بين الراحة والثبات."
# )


#“The 3.0-liter V6 engine features a twin turbocharger that produces 400 horsepower and 550 Nm of torque, which is delivered via an eight-speed dual-clutch transmission, and it rides on an adjustable air suspension system to achieve the ideal balance between comfort and stability.”

inputs = tokenizer(text, return_tensors="pt")

# Time the TTS generation
start_time = time.perf_counter()
with torch.no_grad():
    output = model(**inputs).waveform
elapsed = time.perf_counter() - start_time

# Save to WAV (assuming 16 kHz sample rate)
waveform = output.squeeze().cpu().numpy()
sf.write("car_test.wav", waveform, model.config.sampling_rate)
