from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.chat import router as chat_router ,init_tts_model_ig, init_tts_model_en

app = FastAPI()

# ✅ Load TTS model once at startup
@app.on_event("startup")
def startup_event():
    init_tts_model_ig()
    init_tts_model_en()

# Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router setup
app.include_router(chat_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
