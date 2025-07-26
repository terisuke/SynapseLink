"""
Test for minimal FastAPI application
Phase 0.2: Basic endpoint testing
"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["service"] == "synapselink-api"


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to SynapseLink API"
    assert data["version"] == "0.1.0"


def test_conversation_endpoint_japanese():
    """Test conversation endpoint with Japanese"""
    request_data = {
        "user_id": "test_user_001",
        "message": "こんにちは",
        "message_type": "text",
        "session_id": "test_session_001",
        "language": "ja"
    }
    
    response = client.post("/api/v1/conversation", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["response_text"] == "こんにちは！私はSynapseLinkの受付アシスタントです。ただいまテスト中です。"
    assert data["session_id"] == "test_session_001"
    assert len(data["animations"]) == 2
    assert data["animations"][0]["animation_type"] == "greeting"
    assert "timestamp" in data


def test_conversation_endpoint_english():
    """Test conversation endpoint with English"""
    request_data = {
        "user_id": "test_user_002",
        "message": "Hello",
        "message_type": "text",
        "session_id": "test_session_002",
        "language": "en"
    }
    
    response = client.post("/api/v1/conversation", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["response_text"] == "Hello! I'm the SynapseLink reception assistant. Currently in test mode."
    assert data["session_id"] == "test_session_002"


def test_test_endpoint():
    """Test simple test endpoint"""
    response = client.get("/api/v1/test")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "API is working!"
    assert "timestamp" in data


def test_conversation_validation():
    """Test conversation endpoint validation"""
    # Missing required fields
    request_data = {
        "user_id": "test_user_003",
        "message": "Hello"
        # Missing session_id
    }
    
    response = client.post("/api/v1/conversation", json=request_data)
    assert response.status_code == 422  # Validation error