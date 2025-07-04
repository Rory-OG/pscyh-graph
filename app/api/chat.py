from fastapi import APIRouter, HTTPException
from ..models.schemas import ChatMessage, ChatResponse
from ..services.chat_agent import chat_agent
from typing import List, Dict, Any

router = APIRouter()

@router.post("/message", response_model=ChatResponse)
async def send_message(message: ChatMessage):
    """Send a message to the chat agent"""
    try:
        response = chat_agent.process_message(message.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_chat_history():
    """Get the conversation history"""
    try:
        history = chat_agent.get_conversation_history()
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/history")
async def clear_chat_history():
    """Clear the conversation history"""
    try:
        chat_agent.conversation_history = []
        return {"message": "Chat history cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))