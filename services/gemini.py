# from TTS.api import TTS
# import soundfile as sf
# import io
# import google.generativeai as genai
# from config import GEMINI_API_KEY

# genai.configure(api_key=GEMINI_API_KEY)
# model = genai.GenerativeModel("gemini-2.0-flash")

# tts_model = None
# tts_language = None  # track last loaded model

# def get_prompt_by_lang_mode(user_prompt: str, lang_mode: str) -> str:
#     base_intro = "You are Humonoid, a smart assistant developed by Divyansh Singh and his amazing team at Hiteshi.\n"

#     if lang_mode == "en-en":
#         return f"""{base_intro}
# Respond in English, be friendly and concise.
# User: {user_prompt}"""
#     elif lang_mode == "en-ig":
#         return f"""{base_intro}
# Translate and reply only in Igbo. User will speak in English.
# User: {user_prompt}"""
#     elif lang_mode == "ig-ig":
#         return f"""{base_intro}
# User and Assistant both speak in Igbo only. No English.
# User: {user_prompt}"""
#     else:
#         return f"{base_intro}User: {user_prompt}"

# def get_gemini_response(user_prompt: str, lang_mode: str) -> str:
#     full_prompt = get_prompt_by_lang_mode(user_prompt, lang_mode)
#     response = model.generate_content([{"role": "user", "parts": [full_prompt]}])
#     return response.text.strip()

# tts_model = None

# def init_tts_model(lang_mode: str):
#     global tts_model
#     if tts_model is None or lang_mode in ["en-ig", "ig-ig"]:
#         print("🔄 Loading Yoruba (proxy for Igbo) TTS model...")
#         tts_model = TTS(model_name="tts_models/yor/openbible/vits")
#         print("✅ TTS model loaded.")



# def generate_audio_stream(text: str, lang_mode: str) -> io.BytesIO:
#     init_tts_model(lang_mode)
#     audio = tts_model.tts(text, speed=1.3)
#     buffer = io.BytesIO()
#     sf.write(buffer, audio, samplerate=tts_model.synthesizer.output_sample_rate, format="WAV")
#     buffer.seek(0)
#     return buffer

