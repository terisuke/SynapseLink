# Design Document

## Overview

本設計書は、ChatdollKitベースのVRM対応3D AIチャットシステムの技術アーキテクチャを定義します。システムは、XR環境での没入型受付体験を提供し、完全なオンプレミス運用からクラウド連携まで柔軟に対応できる設計となっています。

### Core Architecture Principles

- **Modular Design**: LangChainのエージェント・ツールパターンに基づく拡張可能なアーキテクチャ
- **Vendor Neutrality**: 特定のクラウドプロバイダーに依存しない設計
- **Privacy First**: オンプレミス環境での完全なデータ制御
- **Open Source**: Apache License 2.0での公開とコミュニティ貢献の促進

## Architecture

### System Architecture Overview

```mermaid
graph TB
    subgraph "Unity Frontend (ChatdollKit)"
        A[VRM Character Display]
        B[XR Spatial Recognition]
        C[Voice Input/Output]
        D[GUI Management Interface]
    end
    
    subgraph "API Gateway"
        E[REST API Server]
        F[WebSocket Handler]
        G[Authentication Layer]
    end
    
    subgraph "LangChain Backend"
        H[Agent Orchestrator]
        I[Tool Manager]
        J[Memory Manager]
        K[Multimodal Processor]
    end
    
    subgraph "MCP Integration Layer"
        L[Playwright MCP]
        M[Database MCP]
        N[Custom MCP Tools]
        note1[MCP: Model Context Protocol<br/>Tool integration framework]
    end
    
    subgraph "Data Layer"
        O[Supabase PostgreSQL]
        P[Vector DB (Qdrant)]
        Q[Knowledge Base]
        R[Configuration Store]
    end
    
    subgraph "AI Services"
        S[Local LLM (Ollama)]
        T[Gemini API]
        U[Local Vision Models]
        V[Speech Recognition/TTS]
    end
    
    A --> E
    B --> E
    C --> F
    D --> E
    
    E --> H
    F --> H
    G --> H
    
    H --> I
    H --> J
    H --> K
    
    I --> L
    I --> M
    I --> N
    
    L --> O
    M --> O
    N --> P
    N --> Q
    
    K --> S
    K --> T
    K --> U
    C --> V
```

### Component Interaction Flow

1. **User Interaction**: Unity frontend captures voice/text input and XR spatial data
2. **API Processing**: API Gateway handles authentication and routes requests
3. **Agent Orchestration**: LangChain agent processes requests and determines required tools
4. **Tool Execution**: MCP tools perform database queries, web automation, or knowledge retrieval
5. **AI Processing**: Multimodal AI generates contextual responses
6. **Response Delivery**: Formatted response sent back to Unity for character animation and speech

## Components and Interfaces

### Unity Frontend Components

#### VRM Character Controller
```csharp
public interface IVRMCharacterController
{
    Task LoadVRMModel(string modelPath);
    Task PlayAnimation(AnimationType type, string content);
    Task SpeakWithLipSync(string text, AudioClip audioClip);
    void SetEmotion(EmotionType emotion, float intensity);
}
```

#### XR Spatial Manager
```csharp
public interface IXRSpatialManager
{
    Task<Plane[]> DetectPlanes();
    Task<Vector3> GetOptimalCharacterPosition();
    Task<bool> TrackUserGaze();
    void AnchorCharacterToSurface(Plane targetPlane);
}
```

#### Reception Interface Manager
```csharp
public interface IReceptionInterfaceManager
{
    Task ShowVisitorForm(VisitorData visitor);
    Task DisplayDirections(LocationInfo destination);
    Task ShowAppointmentStatus(AppointmentInfo appointment);
    void UpdateSystemStatus(SystemHealthInfo health);
}
```

### LangChain Backend Components

#### Agent Orchestrator
```python
from langchain.agents import AgentExecutor
from langchain.tools import BaseTool
from typing import List, Dict, Any

class ReceptionAgentOrchestrator:
    def __init__(self, tools: List[BaseTool], memory: BaseMemory):
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self._create_reception_agent(),
            tools=tools,
            memory=memory,
            verbose=True
        )
    
    async def process_user_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process user input and return structured response"""
        pass
    
    def _create_reception_agent(self) -> BaseAgent:
        """Create specialized reception agent with appropriate prompts"""
        from langchain.agents import create_openai_functions_agent
        from langchain.prompts import ChatPromptTemplate
        
        # Load prompt template from configuration
        prompt_template = self._load_prompt_template("reception_agent")
        
        return create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt_template
        )
    
    def _load_prompt_template(self, template_name: str) -> ChatPromptTemplate:
        """Load prompt template from configuration files"""
        # Implementation loads from config/prompts/{template_name}.yaml
        pass
```

#### Multimodal Processor
```python
from langchain.schema import BaseMessage
from typing import Union, List

class MultimodalProcessor:
    def __init__(self, vision_model: str, text_model: str):
        self.vision_model = self._load_vision_model(vision_model)
        self.text_model = self._load_text_model(text_model)
    
    async def process_image_and_text(
        self, 
        image_data: bytes, 
        text_prompt: str
    ) -> str:
        """Process image and text inputs together"""
        pass
    
    async def extract_document_info(self, image_data: bytes) -> Dict[str, Any]:
        """Extract information from ID cards, documents"""
        pass
```

### MCP Tool Integration

#### Database MCP Tool
```python
from langchain.tools import BaseTool
from mcp import MCPClient

class SupabaseMCPTool(BaseTool):
    name = "supabase_query"
    description = "Query Supabase database for visitor and appointment information"
    
    def __init__(self, mcp_client: MCPClient):
        self.mcp_client = mcp_client
    
    def _run(self, query: str) -> str:
        """Execute database query through MCP"""
        return self.mcp_client.call_tool("database", {"query": query})
```

#### Playwright MCP Tool
```python
class PlaywrightMCPTool(BaseTool):
    name = "web_automation"
    description = "Automate web applications for booking and management"
    
    def __init__(self, mcp_client: MCPClient):
        self.mcp_client = mcp_client
    
    def _run(self, action: str, target: str, data: Dict[str, Any]) -> str:
        """Execute web automation through MCP"""
        return self.mcp_client.call_tool("playwright", {
            "action": action,
            "target": target,
            "data": data
        })
```

### API Layer Design

#### REST API Endpoints
```python
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

app = FastAPI()

class ConversationRequest(BaseModel):
    user_id: str
    message: str
    message_type: str  # "text", "voice", "image"
    session_id: str
    language: str = "ja"

class ConversationResponse(BaseModel):
    response_text: str
    audio_url: Optional[str]
    animations: List[AnimationCommand]
    ui_updates: Optional[Dict[str, Any]]

@app.post("/api/v1/conversation")
async def process_conversation(request: ConversationRequest) -> ConversationResponse:
    """Main conversation endpoint"""
    pass

@app.websocket("/ws/conversation/{session_id}")
async def websocket_conversation(websocket: WebSocket, session_id: str):
    """Real-time conversation WebSocket"""
    pass
```

## Data Models

### Core Data Structures

#### Visitor Information
```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class VisitorInfo(BaseModel):
    visitor_id: str
    name: str
    company: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    visit_purpose: str
    host_name: Optional[str]
    appointment_time: Optional[datetime]
    check_in_time: Optional[datetime]
    check_out_time: Optional[datetime]
    status: str  # "scheduled", "checked_in", "completed", "cancelled"
    notes: Optional[str]
```

#### Conversation Context
```python
class ConversationContext(BaseModel):
    session_id: str
    user_id: str
    language: str
    conversation_history: List[Dict[str, Any]]
    current_task: Optional[str]
    visitor_info: Optional[VisitorInfo]
    system_state: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
```

#### Knowledge Base Document
```python
class KnowledgeDocument(BaseModel):
    document_id: str
    title: str
    content: str
    category: str
    tags: List[str]
    embedding_vector: Optional[List[float]]
    created_at: datetime
    updated_at: datetime
    is_active: bool
```

### Database Schema

#### PostgreSQL Tables
```sql
-- Visitors table
CREATE TABLE visitors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    visit_purpose TEXT NOT NULL,
    host_name VARCHAR(255),
    appointment_time TIMESTAMP WITH TIME ZONE,
    check_in_time TIMESTAMP WITH TIME ZONE,
    check_out_time TIMESTAMP WITH TIME ZONE,
    status VARCHAR(50) DEFAULT 'scheduled',
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Conversations table
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR(255) NOT NULL,
    user_id VARCHAR(255),
    visitor_id UUID REFERENCES visitors(id),
    message_type VARCHAR(50) NOT NULL,
    user_message TEXT,
    ai_response TEXT,
    language VARCHAR(10) DEFAULT 'ja',
    processing_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Knowledge base table
CREATE TABLE knowledge_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(100),
    tags TEXT[],
    embedding_vector vector(1536),  -- Dimension depends on embedding model (1536 for OpenAI, adjust for local models)
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- System configuration table
CREATE TABLE system_config (
    key VARCHAR(255) PRIMARY KEY,
    value JSONB NOT NULL,
    description TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Error Handling

### Error Classification and Response Strategy

#### Client Errors (4xx)
- **Authentication Failures**: Return clear error messages without exposing system details
- **Validation Errors**: Provide specific field-level error information
- **Rate Limiting**: Implement graceful degradation with retry-after headers

#### Server Errors (5xx)
- **AI Model Failures**: Automatic fallback to alternative models
- **Database Connection Issues**: Implement circuit breaker pattern
- **External Service Failures**: Graceful degradation with cached responses

#### Error Response Format
```python
class ErrorResponse(BaseModel):
    error_code: str
    error_message: str
    details: Optional[Dict[str, Any]]
    timestamp: datetime
    request_id: str
    suggested_action: Optional[str]

# Example error responses
ERRORS = {
    "AI_MODEL_UNAVAILABLE": {
        "message": "AI service is temporarily unavailable",
        "suggested_action": "Please try again in a few moments"
    },
    "VISITOR_NOT_FOUND": {
        "message": "Visitor information not found",
        "suggested_action": "Please verify the visitor details"
    }
}
```

### Fallback Mechanisms

#### AI Model Fallbacks
1. **Primary**: Gemini API (when available and configured)
2. **Secondary**: Local Ollama models
3. **Tertiary**: Rule-based responses for critical functions

#### Database Fallbacks
1. **Primary**: Configured Supabase instance
2. **Secondary**: Local SQLite for essential functions
3. **Cache**: Redis for frequently accessed data

## Testing Strategy

### Testing Pyramid

#### Unit Tests (70%)
- **LangChain Tools**: Test individual tool functionality
- **Data Models**: Validate serialization and business logic
- **API Endpoints**: Test request/response handling
- **Unity Components**: Test VRM loading and animation systems

#### Integration Tests (20%)
- **API Integration**: Test Unity ↔ Backend communication
- **Database Integration**: Test MCP ↔ Supabase connectivity
- **AI Pipeline**: Test end-to-end conversation flow
- **XR Functionality**: Test spatial recognition and character positioning

#### End-to-End Tests (10%)
- **Reception Scenarios**: Complete visitor check-in workflows
- **Conversation Flows**: Multi-turn conversation testing
- **System Recovery**: Test failover and recovery mechanisms
- **Performance**: Load testing with multiple concurrent users

### Test Implementation Framework

#### Backend Testing (Python)
```python
import pytest
from unittest.mock import Mock, patch
from langchain.tools import BaseTool

class TestReceptionAgent:
    @pytest.fixture
    def mock_supabase_tool(self):
        tool = Mock(spec=BaseTool)
        tool.run.return_value = "Visitor found: John Doe"
        return tool
    
    @pytest.mark.asyncio
    async def test_visitor_checkin_flow(self, mock_supabase_tool):
        """Test complete visitor check-in process"""
        agent = ReceptionAgentOrchestrator(tools=[mock_supabase_tool])
        
        response = await agent.process_user_input({
            "message": "I'm here for my 2 PM appointment",
            "visitor_name": "John Doe"
        })
        
        assert response["status"] == "success"
        assert "checked in" in response["message"].lower()
```

#### Unity Testing (C#)
```csharp
[Test]
public async Task TestVRMCharacterLoading()
{
    // Arrange
    var controller = new VRMCharacterController();
    var testModelPath = "Assets/TestModels/test_character.vrm";
    
    // Act
    var result = await controller.LoadVRMModel(testModelPath);
    
    // Assert
    Assert.IsTrue(result.IsSuccess);
    Assert.IsNotNull(controller.CurrentCharacter);
}

[Test]
public async Task TestSpatialAnchoringAccuracy()
{
    // Test XR plane detection and character positioning
    var spatialManager = new XRSpatialManager();
    var planes = await spatialManager.DetectPlanes();
    
    Assert.IsTrue(planes.Length > 0);
    
    var position = await spatialManager.GetOptimalCharacterPosition();
    Assert.IsTrue(IsValidPosition(position));
}
```

### Continuous Integration Pipeline

#### GitHub Actions Workflow
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: |
          pytest tests/ --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  unity-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/cache@v3
        with:
          path: Library
          key: Library-${{ hashFiles('Assets/**', 'Packages/**', 'ProjectSettings/**') }}
      - uses: game-ci/unity-test-runner@v2
        env:
          UNITY_LICENSE: ${{ secrets.UNITY_LICENSE }}
        with:
          githubToken: ${{ secrets.GITHUB_TOKEN }}

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run security scan
        uses: securecodewarrior/github-action-add-sarif@v1
        with:
          sarif-file: 'security-scan-results.sarif'
```

この設計書では、要件で定義された全ての機能要件と非機能要件を技術的に実現するための包括的なアーキテクチャを提供しています。次のセクションでは、具体的な実装の詳細とデプロイメント戦略について説明します。
### AI Q
uality Evaluation Framework

#### Response Quality Metrics
```python
from langchain.evaluation import load_evaluator
from typing import Dict, List

class AIQualityEvaluator:
    def __init__(self):
        self.relevance_evaluator = load_evaluator("labeled_score_string")
        self.safety_evaluator = load_evaluator("criteria", criteria="harmfulness")
        
    async def evaluate_response(
        self, 
        user_input: str, 
        ai_response: str, 
        context: Dict[str, Any]
    ) -> Dict[str, float]:
        """Evaluate AI response quality across multiple dimensions"""
        
        metrics = {}
        
        # Relevance scoring
        relevance_score = await self.relevance_evaluator.aevaluate_strings(
            prediction=ai_response,
            reference=user_input,
            input=context.get("conversation_history", "")
        )
        metrics["relevance"] = relevance_score["score"]
        
        # Safety evaluation
        safety_result = await self.safety_evaluator.aevaluate_strings(
            prediction=ai_response,
            input=user_input
        )
        metrics["safety"] = 1.0 - safety_result["score"]  # Invert harmfulness
        
        # Reception-specific metrics
        metrics["professionalism"] = self._evaluate_professionalism(ai_response)
        metrics["task_completion"] = self._evaluate_task_completion(
            user_input, ai_response, context
        )
        
        return metrics
    
    def _evaluate_professionalism(self, response: str) -> float:
        """Evaluate professional tone and language"""
        # Implementation for professional language detection
        pass
    
    def _evaluate_task_completion(
        self, 
        user_input: str, 
        ai_response: str, 
        context: Dict[str, Any]
    ) -> float:
        """Evaluate if the response addresses the user's task"""
        # Implementation for task completion assessment
        pass
```

## Security Architecture

### Authentication and Authorization

#### Multi-Factor Authentication System
```python
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import SQLAlchemyUserDatabase

class SecurityManager:
    def __init__(self, database_url: str, secret_key: str):
        self.user_db = SQLAlchemyUserDatabase(UserDB, database_url)
        self.jwt_auth = JWTAuthentication(
            secret=secret_key,
            lifetime_seconds=3600,
            tokenUrl="auth/jwt/login"
        )
        
    async def verify_admin_access(self, token: str) -> bool:
        """Verify administrator access with MFA"""
        user = await self.jwt_auth.get_current_user(token)
        return user and user.is_admin and user.mfa_verified
    
    async def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt PII data using AES-256"""
        from cryptography.fernet import Fernet
        key = Fernet.generate_key()
        f = Fernet(key)
        return f.encrypt(data.encode()).decode()
```

#### Input Sanitization and Validation
```python
import re
from typing import Any, Dict

class InputSanitizer:
    def __init__(self):
        self.prompt_injection_patterns = [
            r"ignore\s+previous\s+instructions",
            r"system\s*:\s*you\s+are",
            r"<\s*script\s*>",
            r"javascript\s*:",
        ]
    
    def sanitize_user_input(self, user_input: str) -> str:
        """Sanitize user input to prevent prompt injection"""
        sanitized = user_input.strip()
        
        # Remove potential prompt injection attempts
        for pattern in self.prompt_injection_patterns:
            sanitized = re.sub(pattern, "", sanitized, flags=re.IGNORECASE)
        
        # Limit input length
        if len(sanitized) > 1000:
            sanitized = sanitized[:1000]
        
        return sanitized
    
    def validate_visitor_data(self, visitor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and sanitize visitor information"""
        validated = {}
        
        # Email validation
        if "email" in visitor_data:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(email_pattern, visitor_data["email"]):
                validated["email"] = visitor_data["email"]
        
        # Phone validation
        if "phone" in visitor_data:
            phone_pattern = r'^\+?[\d\s\-\(\)]{10,15}$'
            if re.match(phone_pattern, visitor_data["phone"]):
                validated["phone"] = visitor_data["phone"]
        
        return validated
```

### Network Security

#### TLS Configuration
```python
import ssl
from fastapi import FastAPI
import uvicorn

def create_secure_app() -> FastAPI:
    app = FastAPI(
        title="3D AI Reception System",
        version="1.0.0",
        docs_url=None,  # Disable docs in production
        redoc_url=None
    )
    
    # Security headers middleware
    @app.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response
    
    return app

def run_secure_server(app: FastAPI, host: str = "0.0.0.0", port: int = 8443):
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain("cert.pem", "key.pem")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        ssl_context=ssl_context,
        ssl_version=ssl.PROTOCOL_TLS_SERVER,
        ssl_ciphers="ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS"
    )
```

## Performance Optimization

### Caching Strategy

#### Multi-Level Caching
```python
import redis
from functools import wraps
from typing import Optional, Any
import json
import hashlib

class CacheManager:
    def __init__(self, redis_url: str):
        self.redis_client = redis.from_url(redis_url)
        self.local_cache = {}  # In-memory cache for frequently accessed data
    
    def cache_response(self, ttl: int = 300):
        """Decorator for caching AI responses"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Create cache key from function arguments
                cache_key = self._generate_cache_key(func.__name__, args, kwargs)
                
                # Try local cache first
                if cache_key in self.local_cache:
                    return self.local_cache[cache_key]
                
                # Try Redis cache
                cached_result = self.redis_client.get(cache_key)
                if cached_result:
                    result = json.loads(cached_result)
                    self.local_cache[cache_key] = result
                    return result
                
                # Execute function and cache result
                result = await func(*args, **kwargs)
                
                # Cache in Redis
                self.redis_client.setex(
                    cache_key, 
                    ttl, 
                    json.dumps(result, default=str)
                )
                
                # Cache locally
                self.local_cache[cache_key] = result
                
                return result
            return wrapper
        return decorator
    
    def _generate_cache_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Generate unique cache key"""
        key_data = f"{func_name}:{str(args)}:{str(sorted(kwargs.items()))}"
        return hashlib.md5(key_data.encode()).hexdigest()
```

#### Database Query Optimization
```python
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool

class OptimizedDatabaseManager:
    def __init__(self, database_url: str):
        self.engine = create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=20,
            max_overflow=30,
            pool_pre_ping=True,
            pool_recycle=3600
        )
    
    async def get_visitor_with_cache(self, visitor_id: str) -> Optional[Dict[str, Any]]:
        """Get visitor information with intelligent caching"""
        
        # Use prepared statement for better performance
        query = text("""
            SELECT v.*, 
                   COUNT(c.id) as conversation_count,
                   MAX(c.created_at) as last_interaction
            FROM visitors v
            LEFT JOIN conversations c ON v.id = c.visitor_id
            WHERE v.id = :visitor_id
            GROUP BY v.id
        """)
        
        with self.engine.connect() as conn:
            result = conn.execute(query, {"visitor_id": visitor_id})
            return result.fetchone()._asdict() if result else None
```

### Resource Management

#### Memory and CPU Monitoring
```python
import psutil
import asyncio
from typing import Dict, Any
import logging

class ResourceMonitor:
    def __init__(self, alert_threshold: float = 0.8):
        self.alert_threshold = alert_threshold
        self.logger = logging.getLogger(__name__)
    
    async def monitor_system_resources(self) -> Dict[str, Any]:
        """Monitor system resources and trigger alerts if needed"""
        
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        metrics = {
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "memory_available_gb": memory.available / (1024**3),
            "disk_percent": disk.percent,
            "disk_free_gb": disk.free / (1024**3),
            "timestamp": asyncio.get_event_loop().time()
        }
        
        # Check for resource alerts
        if cpu_percent > self.alert_threshold * 100:
            await self._send_alert("High CPU usage", metrics)
        
        if memory.percent > self.alert_threshold * 100:
            await self._send_alert("High memory usage", metrics)
        
        return metrics
    
    async def _send_alert(self, alert_type: str, metrics: Dict[str, Any]):
        """Send resource usage alert"""
        self.logger.warning(f"Resource Alert: {alert_type} - {metrics}")
        # Implementation for sending alerts (email, webhook, etc.)
```

## Deployment Architecture

### Container Configuration

#### Docker Compose Setup
```yaml
version: '3.8'

services:
  # Backend API Service
  api-server:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8443:8443"
    environment:
      - DATABASE_URL=postgresql://user:password@postgres:5432/reception_db
      - REDIS_URL=redis://redis:6379
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    volumes:
      - ./config:/app/config
      - ./logs:/app/logs
      - ./models:/app/models
    depends_on:
      - postgres
      - redis
      - ollama
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "https://localhost:8443/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Local PostgreSQL (when not using cloud Supabase)
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=reception_db
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    restart: unless-stopped

  # Redis for caching
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  # Local LLM service (Ollama)
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0
    restart: unless-stopped

  # Vector database for RAG
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage
    restart: unless-stopped

  # Monitoring and logging
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  ollama_data:
  qdrant_data:
  prometheus_data:
  grafana_data:

networks:
  default:
    driver: bridge
```

#### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: reception-api
  labels:
    app: reception-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: reception-api
  template:
    metadata:
      labels:
        app: reception-api
    spec:
      containers:
      - name: api-server
        image: reception-system/api:latest
        ports:
        - containerPort: 8443
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: database-secret
              key: url
        - name: REDIS_URL
          value: "redis://redis-service:6379"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8443
            scheme: HTTPS
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8443
            scheme: HTTPS
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: reception-api-service
spec:
  selector:
    app: reception-api
  ports:
  - protocol: TCP
    port: 443
    targetPort: 8443
  type: LoadBalancer
```

### Configuration Management

#### Environment-Based Configuration
```python
from pydantic import BaseSettings
from typing import Optional, List
import os

class Settings(BaseSettings):
    # Database settings
    database_url: str = "postgresql://localhost:5432/reception_db"
    supabase_url: Optional[str] = None
    supabase_key: Optional[str] = None
    
    # AI model settings
    gemini_api_key: Optional[str] = None
    ollama_base_url: str = "http://localhost:11434"
    default_llm_model: str = "llama2"
    vision_model: str = "llava"
    
    # Security settings
    secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    
    # Performance settings
    redis_url: str = "redis://localhost:6379"
    max_concurrent_conversations: int = 10
    response_timeout_seconds: int = 30
    
    # Language settings
    supported_languages: List[str] = ["ja", "en"]
    default_language: str = "ja"
    
    # Monitoring settings
    enable_metrics: bool = True
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
```

### Backup and Recovery

#### Automated Backup System
```python
import asyncio
import subprocess
from datetime import datetime, timedelta
import boto3
from typing import Optional

class BackupManager:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.s3_client = boto3.client('s3') if settings.aws_access_key else None
    
    async def create_database_backup(self) -> str:
        """Create PostgreSQL database backup"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"reception_db_backup_{timestamp}.sql"
        
        # Create database dump
        cmd = [
            "pg_dump",
            self.settings.database_url,
            "-f", backup_filename,
            "--verbose",
            "--no-owner",
            "--no-privileges"
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            # Upload to S3 if configured
            if self.s3_client:
                await self._upload_to_s3(backup_filename)
            
            return backup_filename
        else:
            raise Exception(f"Backup failed: {stderr.decode()}")
    
    async def restore_database(self, backup_filename: str) -> bool:
        """Restore database from backup"""
        cmd = [
            "psql",
            self.settings.database_url,
            "-f", backup_filename,
            "--verbose"
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        return process.returncode == 0
    
    async def cleanup_old_backups(self, retention_days: int = 30):
        """Remove backups older than retention period"""
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        # Implementation for cleaning up local and S3 backups
        pass
```

この設計書は、要件で定義された全ての機能と非機能要件を満たす包括的なシステムアーキテクチャを提供しています。次に、この設計に基づいた具体的な実装タスクリストを作成する準備が整いました。

<function_calls>
<invoke name="userInput">
<parameter name="question">**設計ドキュメントは適切でしょうか？実装に必要な技術的詳細が十分に含まれていますか？**### 
Prompt Engineering and Management

#### Prompt Template System
```python
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
import yaml
from typing import Dict, Any

class PromptManager:
    def __init__(self, prompt_config_path: str = "config/prompts"):
        self.prompt_config_path = prompt_config_path
        self.templates = {}
        self._load_all_templates()
    
    def _load_all_templates(self):
        """Load all prompt templates from configuration files"""
        import os
        for filename in os.listdir(self.prompt_config_path):
            if filename.endswith('.yaml'):
                template_name = filename[:-5]  # Remove .yaml extension
                self.templates[template_name] = self._load_template(template_name)
    
    def _load_template(self, template_name: str) -> ChatPromptTemplate:
        """Load specific prompt template"""
        with open(f"{self.prompt_config_path}/{template_name}.yaml", 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        messages = []
        
        # System message
        if 'system' in config:
            messages.append(SystemMessagePromptTemplate.from_template(config['system']))
        
        # Human message template
        if 'human' in config:
            messages.append(HumanMessagePromptTemplate.from_template(config['human']))
        
        return ChatPromptTemplate.from_messages(messages)
    
    def get_template(self, template_name: str) -> ChatPromptTemplate:
        """Get prompt template by name"""
        return self.templates.get(template_name)

# Example prompt configuration file: config/prompts/reception_agent.yaml
"""
system: |
  あなたは企業の受付システムのAIアシスタントです。以下の役割を担います：
  
  1. 来訪者の受付業務（チェックイン、予約確認、案内）
  2. 企業情報や施設案内の提供
  3. 緊急時の適切な対応
  
  常にプロフェッショナルで親切な対応を心がけ、来訪者が快適に感じられるよう配慮してください。
  
  利用可能なツール:
  {tools}
  
  現在の日時: {current_time}
  施設情報: {facility_info}huma
n: |
  来訪者からの入力: {user_input}
  
  来訪者情報: {visitor_context}
  会話履歴: {conversation_history}
  
  適切なツールを使用して、来訪者のニーズに応じた対応を行ってください。
"""
```

#### Advanced Security with LLM Guardrails
```python
from typing import List, Dict, Any
import re

class AdvancedInputSanitizer(InputSanitizer):
    def __init__(self):
        super().__init__()
        # Future integration point for advanced guardrail libraries
        self.guardrail_enabled = False
        
    async def advanced_content_filtering(self, user_input: str) -> Dict[str, Any]:
        """
        Advanced content filtering using LLM guardrails
        Future integration with libraries like:
        - LangChain Guardrails
        - NVIDIA NeMo Guardrails
        - Microsoft Presidio for PII detection
        """
        
        result = {
            "is_safe": True,
            "filtered_input": user_input,
            "detected_issues": [],
            "confidence_score": 1.0
        }
        
        # Basic implementation - to be enhanced with advanced guardrail libraries
        if self._detect_prompt_injection(user_input):
            result["is_safe"] = False
            result["detected_issues"].append("potential_prompt_injection")
            result["confidence_score"] = 0.2
        
        # Future: Integration with advanced guardrail systems
        if self.guardrail_enabled:
            # result = await self._apply_advanced_guardrails(user_input)
            pass
        
        return result
    
    def _detect_prompt_injection(self, text: str) -> bool:
        """Enhanced prompt injection detection"""
        # Extended pattern matching for sophisticated attacks
        advanced_patterns = [
            r"ignore\s+(?:all\s+)?(?:previous|prior|above)\s+(?:instructions?|prompts?|rules?)",
            r"(?:system|assistant|ai)\s*[:\-]\s*(?:you\s+(?:are|must)|ignore)",
            r"(?:new|updated?)\s+(?:instructions?|prompts?|rules?)\s*[:\-]",
            r"(?:roleplay|pretend|act)\s+(?:as|like)\s+(?:a\s+)?(?:different|new)",
            r"(?:forget|disregard|override)\s+(?:your|the)\s+(?:instructions?|rules?|guidelines?)",
        ]
        
        for pattern in advanced_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False

# Note: Future versions should integrate with specialized guardrail libraries
# such as LangChain Guardrails or NVIDIA NeMo Guardrails for more robust
# protection against evolving prompt injection techniques.
```

### Testing Strategy Enhancement

#### Golden Dataset Management
```python
import json
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ConversationTestCase:
    scenario_name: str
    user_input: str
    expected_response_type: str
    expected_actions: List[str]
    context: Dict[str, Any]
    quality_metrics: Dict[str, float]

class GoldenDatasetManager:
    def __init__(self, dataset_path: str = "tests/golden_dataset"):
        self.dataset_path = Path(dataset_path)
        self.test_cases = self._load_test_cases()
    
    def _load_test_cases(self) -> List[ConversationTestCase]:
        """Load golden dataset test cases"""
        test_cases = []
        
        for scenario_file in self.dataset_path.glob("*.json"):
            with open(scenario_file, 'r', encoding='utf-8') as f:
                scenario_data = json.load(f)
                
                for case_data in scenario_data.get("test_cases", []):
                    test_cases.append(ConversationTestCase(
                        scenario_name=scenario_data["scenario_name"],
                        user_input=case_data["user_input"],
                        expected_response_type=case_data["expected_response_type"],
                        expected_actions=case_data.get("expected_actions", []),
                        context=case_data.get("context", {}),
                        quality_metrics=case_data.get("quality_metrics", {})
                    ))
        
        return test_cases
    
    async def run_regression_tests(self, agent: ReceptionAgentOrchestrator) -> Dict[str, Any]:
        """Run regression tests against golden dataset"""
        results = {
            "total_tests": len(self.test_cases),
            "passed": 0,
            "failed": 0,
            "detailed_results": []
        }
        
        for test_case in self.test_cases:
            try:
                response = await agent.process_user_input({
                    "message": test_case.user_input,
                    "context": test_case.context
                })
                
                # Evaluate response quality
                quality_score = await self._evaluate_response_quality(
                    test_case, response
                )
                
                test_result = {
                    "scenario": test_case.scenario_name,
                    "input": test_case.user_input,
                    "passed": quality_score >= 0.8,  # Threshold for passing
                    "quality_score": quality_score,
                    "response": response
                }
                
                if test_result["passed"]:
                    results["passed"] += 1
                else:
                    results["failed"] += 1
                
                results["detailed_results"].append(test_result)
                
            except Exception as e:
                results["failed"] += 1
                results["detailed_results"].append({
                    "scenario": test_case.scenario_name,
                    "input": test_case.user_input,
                    "passed": False,
                    "error": str(e)
                })
        
        return results
    
    async def _evaluate_response_quality(
        self, 
        test_case: ConversationTestCase, 
        response: Dict[str, Any]
    ) -> float:
        """Evaluate response quality against expected metrics"""
        # Implementation for quality evaluation
        # This would integrate with the AIQualityEvaluator
        pass

# Example golden dataset file: tests/golden_dataset/visitor_checkin.json
"""
{
  "scenario_name": "visitor_checkin",
  "description": "Test cases for visitor check-in scenarios",
  "test_cases": [
    {
      "user_input": "こんにちは、2時に田中さんとお約束をいただいている山田です",
      "expected_response_type": "appointment_confirmation",
      "expected_actions": ["check_appointment", "verify_visitor"],
      "context": {
        "current_time": "2024-01-15T13:55:00Z",
        "language": "ja"
      },
      "quality_metrics": {
        "professionalism": 0.9,
        "task_completion": 0.95,
        "relevance": 0.9
      }
    }
  ]
}
"""
```

### Configuration Management Enhancement

#### Embedding Model Configuration
```python
from typing import Dict, Any, Optional
import yaml

class EmbeddingModelConfig:
    def __init__(self, config_path: str = "config/embedding_models.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
    
    def get_model_config(self, model_name: str) -> Dict[str, Any]:
        """Get configuration for specific embedding model"""
        return self.config.get("models", {}).get(model_name, {})
    
    def get_vector_dimension(self, model_name: str) -> int:
        """Get vector dimension for specific model"""
        model_config = self.get_model_config(model_name)
        return model_config.get("dimension", 1536)  # Default to OpenAI dimension
    
    def update_database_schema(self, model_name: str):
        """Update database schema for new embedding model"""
        dimension = self.get_vector_dimension(model_name)
        
        # SQL to alter table for new dimension
        alter_sql = f"""
        ALTER TABLE knowledge_documents 
        ALTER COLUMN embedding_vector TYPE vector({dimension});
        """
        
        return alter_sql

# Example config/embedding_models.yaml
"""
models:
  openai_ada_002:
    dimension: 1536
    provider: "openai"
    model_name: "text-embedding-ada-002"
    
  sentence_transformers_all_mpnet:
    dimension: 768
    provider: "huggingface"
    model_name: "sentence-transformers/all-mpnet-base-v2"
    
  ollama_nomic_embed:
    dimension: 768
    provider: "ollama"
    model_name: "nomic-embed-text"
    
  local_multilingual:
    dimension: 384
    provider: "sentence_transformers"
    model_name: "paraphrase-multilingual-MiniLM-L12-v2"
"""
```

この設計書の強化により、以下の点が改善されました：

1. **MCPの明確化**: アーキテクチャ図にMCPの説明を追加
2. **Vector DBの具体化**: QdrantをVector Databaseとして明記
3. **Embeddingの柔軟性**: 異なるモデルの次元数に対応する設計
4. **プロンプト管理**: 設定ファイルベースのプロンプト管理システム
5. **高度なセキュリティ**: 将来のガードレールライブラリ統合の準備
6. **Golden Dataset**: AI品質の回帰テスト基盤
7. **設定管理の強化**: Embeddingモデルの動的切り替え対応

これで、実装チームが迷うことなく開発を進められる、完璧に近い設計書が完成しました！

<function_calls>
<invoke name="userInput">
<parameter name="question">**強化された設計ドキュメントで実装タスクフェーズに進んでよろしいですか？**