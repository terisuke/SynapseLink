# SynapseLink

A 3D AI chat system combining ChatdollKit for VRM character animation with LangChain for AI conversation management. Designed for reception and visitor management scenarios with support for both 2D and AR/VR environments.

## Features

- 🤖 VRM-compatible 3D character with voice, lip-sync, and animations
- 🗣️ Multi-modal AI support (text, voice, vision)
- 🏢 Vendor-neutral design for on-premises and cloud deployment
- 🌐 Japanese and English language support
- 🎯 Reception and visitor management capabilities
- 🔒 Privacy-first architecture with local AI options

## Technology Stack

- **Backend**: Python, FastAPI, LangChain
- **Frontend**: Unity 2022.3 LTS, ChatdollKit
- **Database**: PostgreSQL/Supabase, Qdrant (Vector DB)
- **AI Services**: Gemini API, Ollama (local), Whisper
- **XR Support**: AR Foundation

## Quick Start

### Prerequisites

- Python 3.11+
- Unity 2022.3 LTS
- Docker (optional)
- PostgreSQL

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/terisuke/SynapseLink.git
cd SynapseLink

# Set up Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Copy environment variables
cp ../.env.example ../.env
# Edit .env with your configuration

# Run the backend server
cd ..
uvicorn backend.src.main:app --reload --port 8000
```

### Unity Setup

1. Open Unity Hub and add the `unity/` directory as a project
2. Open with Unity 2022.3 LTS
3. Install required packages via Unity Package Manager:
   - ChatdollKit: `https://github.com/uezo/ChatdollKit.git`
   - AR Foundation
   - VRM Importer

## Documentation

For detailed documentation, see:
- [Architecture Overview](.kiro/specs/3d-ai-chat-system/design.md)
- [Requirements](.kiro/specs/3d-ai-chat-system/requirements.md)
- [Implementation Tasks](.kiro/specs/3d-ai-chat-system/tasks.md)
- [Development Guide](CLAUDE.md)

## Development

See [CLAUDE.md](CLAUDE.md) for detailed development instructions and project structure.

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

## Support

For issues and feature requests, please use the GitHub issue tracker.