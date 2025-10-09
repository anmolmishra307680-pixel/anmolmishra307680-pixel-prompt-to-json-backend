# 🚀 Prompt-to-JSON Backend

**Universal AI Design System** - Production-ready FastAPI backend for AI-powered design generation with multi-agent coordination, reinforcement learning, and comprehensive testing.

[![Production Status](https://img.shields.io/badge/Status-Production%20Ready-green)](https://prompt-to-json-backend.onrender.com)
[![API Version](https://img.shields.io/badge/API-v2.1.1-blue)](https://prompt-to-json-backend.onrender.com/docs)
[![Test Coverage](https://img.shields.io/badge/Tests-46/46%20Passing-brightgreen)](test_all_endpoints.py)
[![Endpoint Status](https://img.shields.io/badge/Endpoints-46/46%20Validated-brightgreen)](https://prompt-to-json-backend.onrender.com/docs)

## 📋 What is This Project?

A production-ready FastAPI backend that converts natural language prompts into structured design specifications using AI agents. Features include:

- **AI-Powered Generation**: Multi-agent system for design specification generation
- **Reinforcement Learning**: Iterative improvement through RL training loops
- **Dual Authentication**: Enterprise-grade API Key + JWT security
- **46 API Endpoints**: Comprehensive REST API with 100% test coverage
- **Real-time Evaluation**: Multi-criteria design assessment
- **Database Integration**: PostgreSQL (Supabase) with SQLite fallback
- **Production Monitoring**: Prometheus metrics, health checks, logging

## 🚀 How to Run This Project

### Prerequisites
- Python 3.8+
- pip

### Quick Start

```bash
# 1. Clone and setup
git clone <repository-url>
cd prompt-to-json-backend
python -m venv .venv
.venv\Scripts\activate  # Windows (.venv/bin/activate for Unix)
pip install -r requirements.txt

# 2. Configure environment
cp config/.env.example config/.env
# Edit config/.env with your settings

# 3. Run database migrations (optional)
alembic upgrade head

# 4. Start the server
python -m src.main
```

### Access Points
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Authentication

```bash
# Get JWT token
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: bhiv-secret-key-2024" \
  -d '{"username":"admin","password":"bhiv2024"}'

# Use token for API calls
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "X-API-Key: bhiv-secret-key-2024" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{"prompt":"Modern office chair"}'
```

## 🧪 Testing

```bash
# Run all tests (46 endpoints validated)
python test_all_endpoints.py

# Run unit tests
pytest tests/tests/ -v

# Run with coverage
pytest tests/tests/ --cov=src --cov-report=html
```

## 📁 Project Structure

```
prompt-to-json-backend/
├── src/
│   ├── main.py                  # FastAPI application (46 endpoints)
│   ├── agents/                  # AI agent implementations
│   ├── core/                    # Core utilities (auth, cache, adapters)
│   ├── data/                    # Database models and operations
│   ├── schemas/                 # Pydantic schemas
│   ├── services/                # Business logic services
│   └── utils/                   # Helper utilities
├── tests/
│   ├── tests/                   # Unit and integration tests
│   └── load-tests/              # Performance testing
├── config/                      # Configuration files
├── docs/                        # Documentation
├── test_all_endpoints.py        # Comprehensive endpoint testing
└── requirements.txt             # Python dependencies
```

## 🔧 Key Features

### AI Agents
- **MainAgent**: Prompt processing and spec generation
- **EvaluatorAgent**: Multi-criteria design evaluation
- **RLLoop**: Reinforcement learning for iterative improvement
- **FeedbackAgent**: Continuous learning from user feedback
- **AgentCoordinator**: Multi-agent orchestration

### Security
- Dual authentication (API Key + JWT)
- Rate limiting (20 req/min)
- CORS protection
- Input validation
- Secure token management

### Database
- PostgreSQL (Supabase) primary
- SQLite fallback
- Alembic migrations
- Automated logging

## 📊 API Endpoints

**46 Endpoints Organized in 12 Categories:**

1. **🔐 Authentication** (2) - Login, token refresh
2. **📊 System Monitoring** (7) - Health, metrics, status
3. **🤖 AI Generation** (5) - Generate, switch, core pipeline
4. **⚖️ Compliance** (3) - Validation, feedback, pipeline
5. **🧠 Evaluation & RL** (6) - Evaluate, iterate, batch processing
6. **📋 Reports & Data** (3) - Reports, logs, iterations
7. **🔧 Administration** (1) - Log management
8. **🖥️ Frontend Integration** (4) - UI sessions, Three.js data
9. **🖼️ Preview Management** (5) - Preview generation, verification
10. **📱 Mobile Platform** (2) - Mobile-optimized endpoints
11. **🥽 VR/AR Platform** (5) - VR/AR scene generation
12. **💰 Cost Management** (4) - Cost tracking, compute stats

See `/docs` for interactive API documentation.

## 🚀 Production Deployment

**Live URL**: https://prompt-to-json-backend.onrender.com

### Docker
```bash
docker build -t prompt-backend .
docker run -p 8000:8000 --env-file config/.env prompt-backend
```

### Environment Variables
```bash
API_KEY=your-api-key
DEMO_USERNAME=admin
DEMO_PASSWORD=your-password
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
JWT_SECRET_KEY=your-jwt-secret
```

## 📈 Performance

- **Response Time**: <200ms average
- **Test Coverage**: 46/46 endpoints (100%)
- **Concurrent Users**: 1000+ validated
- **Rate Limiting**: 20 req/min per endpoint
- **Uptime**: 99.9% target

## 📚 Documentation

- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Detailed Guides**: See `docs/` folder

## 🤝 Contributing

See `docs/` for development guidelines.

## 📄 License

See LICENSE file for details.

---

**Production Status**: ✅ All 46 endpoints validated and operational