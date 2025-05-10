from fastapi import APIRouter, Request
from pydantic import BaseModel
from services.gemini import get_gemini_response


router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str
    
    
    
@router.post("/chat")

async def chat(req : PromptRequest):
    reply = get_gemini_response(req.prompt)
    return {
        "response": reply
    }