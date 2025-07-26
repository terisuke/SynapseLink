# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SynapseLink is a 3D AI chat system that combines ChatdollKit for VRM character animation with LangChain for AI conversation management. The system is designed for reception/visitor management scenarios and supports both 2D and AR/VR environments.

### Key Features
- VRM-compatible 3D character with voice, lip-sync, and animations
- Multi-modal AI support (text, voice, vision)
- Vendor-neutral design for on-premises and cloud deployment
- Japanese and English language support
- Reception and visitor management capabilities

## Architecture

### Backend (Python/LangChain)
- **Framework**: FastAPI for REST API and WebSocket endpoints
- **AI Orchestration**: LangChain with agent-based architecture
- **Database**: PostgreSQL/Supabase with vector search (Qdrant)
- **Caching**: Redis for performance optimization
- **Container**: Docker and Kubernetes support

### Frontend (Unity/ChatdollKit)
- **Unity Version**: 2022.3 LTS
- **3D Characters**: VRM format support via ChatdollKit
- **XR Support**: AR Foundation for cross-platform AR/VR
- **Communication**: REST API and WebSocket for real-time interaction

### AI Services
- **LLM**: Gemini API (cloud) or Ollama (local)
- **Vision**: Multimodal AI for document/ID recognition
- **TTS**: AIVIS (Japanese), ElevenLabs (English), pluggable architecture
- **STT**: Whisper API or platform-native solutions

## Development Commands

### Backend Setup
```bash
# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (once requirements.txt is created)
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Database migrations (once implemented)
alembic upgrade head

# Run backend server
uvicorn main:app --reload --port 8000

# Run tests
pytest tests/ --cov=src --cov-report=html

# Lint and format
black .
ruff check .
mypy .
```

### Unity Development
```bash
# Unity project will be in the unity/ directory
# Open with Unity 2022.3 LTS

# Package dependencies (via Unity Package Manager):
# - ChatdollKit: https://github.com/uezo/ChatdollKit.git
# - VRM Importer
# - AR Foundation
# - Unity Localization
```

### Docker Development
```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f api-server

# Run specific service
docker-compose up postgres redis
```

## Project Structure (Planned)

```
SynapseLink/
├── backend/                 # Python/LangChain backend
│   ├── src/
│   │   ├── api/            # FastAPI endpoints
│   │   ├── agents/         # LangChain agents
│   │   ├── tools/          # MCP and other tools
│   │   ├── models/         # Pydantic models
│   │   └── services/       # Business logic
│   ├── tests/              # pytest tests
│   ├── migrations/         # Alembic migrations
│   └── config/             # Configuration files
├── unity/                  # Unity frontend project
│   ├── Assets/
│   │   ├── Scripts/        # C# scripts
│   │   ├── ChatdollKit/    # ChatdollKit integration
│   │   ├── Models/         # VRM models
│   │   └── XR/             # AR Foundation setup
│   └── ProjectSettings/
├── docker/                 # Docker configurations
├── k8s/                    # Kubernetes manifests
└── docs/                   # Additional documentation
```

## Key Implementation Files

### Backend Core Files
- `backend/src/agents/reception_agent.py` - Main LangChain agent orchestrator
- `backend/src/api/conversation.py` - Conversation API endpoints
- `backend/src/tools/supabase_tool.py` - Database access via MCP
- `backend/src/tools/playwright_tool.py` - Web automation via MCP
- `backend/src/services/multimodal_processor.py` - Vision/multimodal AI

### Unity Core Files
- `unity/Assets/Scripts/Controllers/VRMCharacterController.cs` - VRM character control
- `unity/Assets/Scripts/Managers/XRSpatialManager.cs` - AR/VR spatial management
- `unity/Assets/Scripts/API/ConversationClient.cs` - Backend API client
- `unity/Assets/Scripts/UI/ReceptionInterfaceManager.cs` - Reception UI

## Testing Strategy

### Backend Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_reception_agent.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run integration tests only
pytest -m integration
```

### Unity Testing
- Use Unity Test Runner for unit tests
- Test VRM loading, animation, and XR functionality
- Integration tests for API communication

## Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/reception_db
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-key

# AI Services
GEMINI_API_KEY=your-gemini-key
OLLAMA_BASE_URL=http://localhost:11434

# Security
SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256

# Language
DEFAULT_LANGUAGE=ja
SUPPORTED_LANGUAGES=ja,en
```

## Development Workflow

1. **Phase 0**: Start with basic API-Unity communication prototype
2. **Backend First**: Implement core LangChain agents and database
3. **Frontend Integration**: Unity/ChatdollKit with basic VRM support
4. **Feature Development**: Add multimodal AI, TTS/STT, XR features
5. **Testing**: Comprehensive unit and integration tests
6. **Deployment**: Docker/Kubernetes configuration

## Important Notes

- **Vendor Neutral**: System must work completely offline with local models
- **Multi-language**: All user-facing text must support Japanese and English
- **Security**: All PII data must be encrypted, input sanitization required
- **Performance**: Response time < 2.5s, AR/VR maintain 60+ FPS
- **Open Source**: Follow Apache License 2.0, maintain good documentation

## Quick Start for New Features

1. Check requirements in `.kiro/specs/3d-ai-chat-system/requirements.md`
2. Review design patterns in `.kiro/specs/3d-ai-chat-system/design.md`
3. Find relevant tasks in `.kiro/specs/3d-ai-chat-system/tasks.md`
4. Write tests first (TDD approach)
5. Implement feature following existing patterns
6. Update documentation as you code

## Common Workflows

### Adding a New LangChain Tool
1. Create tool class in `backend/src/tools/`
2. Implement BaseTool interface
3. Add tool to agent orchestrator
4. Write unit tests
5. Update tool documentation

### Adding a New Unity Animation
1. Import animation to `unity/Assets/Animations/`
2. Update VRMCharacterController
3. Add animation trigger in conversation response
4. Test with different VRM models

### Implementing a New Language
1. Add language code to supported languages
2. Create prompt templates in config
3. Add UI translations in Unity Localization
4. Configure appropriate TTS provider
5. Test full conversation flow