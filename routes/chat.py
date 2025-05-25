from fastapi import APIRouter
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional
import io
import soundfile as sf
from TTS.api import TTS
import google.generativeai as genai
import json
from config import GEMINI_API_KEY

router = APIRouter()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


tts_model_en = None
tts_model_ig = None

def init_tts_model_en():
    global tts_model_en
    if tts_model_en is None:
        print("Loading English TTS model...")
        tts_model_en = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
        print(" English TTS model loaded.")

def init_tts_model_ig():
    global tts_model_ig
    if tts_model_ig is None:
        print("Loading Igbo TTS model...")
        tts_model_ig = TTS(model_name="tts_models/yor/openbible/vits")
        print("Igbo TTS model loaded.")

#  Prompt enhancer
def get_prompt_by_lang_mode(user_prompt: str, lang_mode: str) -> str:
    base = "You are Humonoid, a helpful assistant developed by Divyansh Singh at Hiteshi.\n"
    if lang_mode == "en-ig":
        return f"{base}Translate and reply in Igbo only. Do not repeat the question in the answer, give the answer only.\nUser: {user_prompt}"
    elif lang_mode == "ig-ig":
        return f"{base}Respond to the user in Igbo. Do not repeat the question in your answer.\nUser: {user_prompt}"
    elif lang_mode == "en-en":
        return f"{base}Respond in English, be friendly and concise, do not repeat words, give a good response, and do not use the '*' sign in the response.\nUser: {user_prompt}"
    else:
        return f"{base}Respond in English.\nUser: {user_prompt}"

#  Gemini response
def get_gemini_response(prompt: str, lang_mode: str) -> str:
    full_prompt = get_prompt_by_lang_mode(prompt, lang_mode)
    response = model.generate_content([{"role": "user", "parts": [full_prompt]}])
    raw_text = response.text.strip()

    try:
        parsed = json.loads(raw_text)
        if isinstance(parsed, list):
            translated_texts = []
            for item in parsed:
                if isinstance(item, dict):
                    translated = item.get("translated", "").strip()
                    # Skip if translated text is exactly same as prompt or empty
                    if translated and translated.lower() != prompt.lower().strip():
                        translated_texts.append(translated)
            return " ".join(translated_texts).strip()
    except Exception:
        pass

    return raw_text

#  TTS Audio Stream
def generate_audio_stream(text: str, lang_mode: str) -> io.BytesIO:
    if lang_mode == "en-en":
        init_tts_model_en()
        audio = tts_model_en.tts(text, speed=1.0)
        sample_rate = tts_model_en.synthesizer.output_sample_rate
    else:
        init_tts_model_ig()
        audio = tts_model_ig.tts(text, speed=1.3)
        sample_rate = tts_model_ig.synthesizer.output_sample_rate

    buffer = io.BytesIO()
    sf.write(buffer, audio, samplerate=sample_rate, format="WAV")
    buffer.seek(0)
    return buffer

#  Request body
class PromptRequest(BaseModel):
    prompt: str
    lang_mode: str
    response_type: Optional[str] = None  # "text" or None for audio

# Unified endpoint
@router.post("/chat")
async def chat(req: PromptRequest):
    reply = get_gemini_response(req.prompt, req.lang_mode)

    # Return text JSON if explicitly requested
    if req.response_type == "text":
        return JSONResponse({"response": reply})

    # Return audio stream for supported lang modes
    if req.lang_mode in ["en-en", "en-ig", "ig-ig"]:
        audio_stream = generate_audio_stream(reply, req.lang_mode)
        return StreamingResponse(audio_stream, media_type="audio/wav")

    # Default fallback text response
    return JSONResponse({"response": reply})
