# Architecture & Project Structure

## API Status
✅ **Production Ready** - All 17 endpoints operational
- Authentication: Dual API Key + JWT system
- Generation: Universal design system (buildings, vehicles, electronics, appliances, furniture)
- Evaluation: Multi-criteria assessment with RL training
- Monitoring: Prometheus metrics + health checks

## Project Structure
```
prompt-to-json-backend/
├── config/              # Configuration files
├── docs/                # Consolidated documentation
├── deployment/          # Docker & CI/CD
├── src/
│   ├── main.py          # FastAPI entrypoint
│   ├── agents/          # AI agents (MainAgent, EvaluatorAgent, RLLoop)
│   ├── api/             # FastAPI endpoints
│   ├── auth/            # JWT authentication
│   ├── core/            # Core business logic
│   ├── data/            # Database operations
│   ├── schemas/         # Data models (universal, legacy, v2)
│   ├── services/        # External integrations
│   └── utils/           # Utilities & monitoring
├── tests/               # Test suite (48 tests)
├── assets/              # Sample data & artifacts
├── reports/             # Logs & evaluation reports
└── .github/             # CI/CD workflows
```

## Import Fixes Summary
- ✅ Resolved circular imports with lazy loading
- ✅ Updated all import paths for new structure
- ✅ Maintained backward compatibility
- ✅ Fixed schema compatibility (UniversalDesignSpec ↔ DesignSpec)
- ✅ All 48 tests passing

## Key Components
- **MainAgent**: Universal design generation
- **EvaluatorAgent**: Multi-criteria evaluation
- **RLLoop**: Reinforcement learning training
- **Database**: Supabase PostgreSQL + SQLite fallback
- **Authentication**: API Key + JWT dual system
- **Monitoring**: Prometheus + HIDG logging