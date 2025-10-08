# Authentication Runbook

## JWT Token Management

### Environment Variables
```bash
JWT_SECRET=bhiv-secret-key-2024
DEMO_USERNAME=admin
DEMO_PASSWORD=bhiv2024
```

### Login Flow
1. POST `/api/v1/auth/login` with username/password
2. Receive JWT token (24h expiry)
3. Include in Authorization header: `Bearer <token>`

### API Key Requirements
- All endpoints require `X-API-Key: bhiv-secret-key-2024`
- Public endpoints: `/health`, `/metrics`
- Auth endpoint: `/api/v1/auth/login` (API key only)

### Token Verification
```python
from src.auth.jwt_middleware import verify_token
# Use as dependency: current_user: str = Depends(verify_token)
```

### Security Headers
```bash
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
```

### Troubleshooting
- 401 Unauthorized: Check API key and JWT token
- Token expired: Re-login to get new token
- Invalid credentials: Verify DEMO_USERNAME/DEMO_PASSWORD