"""
Minimal FastAPI application for SynapseLink
Phase 0.2: Basic API endpoint implementation
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="SynapseLink Reception API",
    description="3D AI Chat System Backend",
    version="0.1.0"
)

# Configure CORS for Unity client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify Unity app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class ConversationRequest(BaseModel):
    user_id: str
    message: str
    message_type: str = "text"  # "text", "voice", "image"
    session_id: str
    language: str = "ja"


class AnimationCommand(BaseModel):
    animation_type: str
    duration: float
    parameters: Optional[dict] = None


class ConversationResponse(BaseModel):
    response_text: str
    audio_url: Optional[str] = None
    animations: List[AnimationCommand] = []
    ui_updates: Optional[dict] = None
    session_id: str
    timestamp: datetime


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for Docker and monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "synapselink-api"
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to SynapseLink API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health"
    }


# Main conversation endpoint (Phase 0.2 - Fixed response)
@app.post("/api/v1/conversation", response_model=ConversationResponse)
async def process_conversation(request: ConversationRequest):
    """
    Process conversation request and return fixed response.
    This is a minimal implementation for Phase 0.2.
    """
    
    # Fixed response for testing
    fixed_response = "こんにちは！私はSynapseLinkの受付アシスタントです。ただいまテスト中です。"
    
    if request.language == "en":
        fixed_response = "Hello! I'm the SynapseLink reception assistant. Currently in test mode."
    
    # Create simple animation commands
    animations = [
        AnimationCommand(
            animation_type="greeting",
            duration=2.0,
            parameters={"intensity": 0.8}
        ),
        AnimationCommand(
            animation_type="idle",
            duration=5.0,
            parameters={"loop": True}
        )
    ]
    
    # Return fixed response
    return ConversationResponse(
        response_text=fixed_response,
        audio_url=None,  # No audio in minimal version
        animations=animations,
        ui_updates={"show_greeting": True},
        session_id=request.session_id,
        timestamp=datetime.now()
    )


# Simple test endpoint for debugging
@app.get("/api/v1/test")
async def test_endpoint():
    """Simple test endpoint"""
    return {
        "message": "API is working!",
        "timestamp": datetime.now().isoformat()
    }


# Run the application
if __name__ == "__main__":
    # This is for development only
    # In production, use the Docker CMD or a proper ASGI server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )