from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.multi_agent import get_orchestrator, MultiAgentOrchestrator

router = APIRouter(prefix="/api/v1", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = ""

class ChatResponse(BaseModel):
    response: str
    suggestions: List[str]
    agent: Optional[str] = "Sentinel AI"
    badge: Optional[str] = "🤖 Sentinel AI"

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    orchestrator: MultiAgentOrchestrator = Depends(get_orchestrator)
):
    result = await orchestrator.route_and_execute(request.message, request.context)
    return ChatResponse(
        response=result["response"],
        suggestions=result["suggestions"],
        agent=result.get("agent", "Sentinel AI"),
        badge=result.get("badge", "🤖 Sentinel AI")
    )
