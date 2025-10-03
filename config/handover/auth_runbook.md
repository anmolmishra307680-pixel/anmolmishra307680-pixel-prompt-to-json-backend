# JWT Authentication Runbook

## Overview
The system uses dual authentication: API Key + JWT Token for enhanced security.

## Authentication Flow

### 1. API Key Validation
- **Header**: `X-API-Key: bhiv-secret-key-2024`
- **Required**: All endpoints except `/health`
- **Validation**: Constant-time comparison to prevent timing attacks

### 2. JWT Token Generation
```bash
POST /api/v1/auth/login
Content-Type: application/json
X-API-Key: bhiv-secret-key-2024

{
  "username": "admin",
  "password": "bhiv2024"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### 3. Using JWT Token
```bash
Authorization: Bearer <jwt_token>
X-API-Key: bhiv-secret-key-2024
```

## JWT Configuration

### Environment Variables
```bash
# JWT Settings
JWT_SECRET_KEY=your-super-secret-jwt-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=1

# API Key
API_KEY=bhiv-secret-key-2024

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=bhiv2024
```

### Token Structure
```json
{
  "sub": "admin",
  "exp": 1696348800,
  "iat": 1696345200,
  "type": "access_token"
}
```

## Security Features

### Rate Limiting
- **Protected Endpoints**: 20 requests/minute per IP
- **Login Endpoint**: 5 attempts/minute per IP
- **Implementation**: In-memory sliding window

### Token Validation
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Expiration**: 1 hour (configurable)
- **Refresh**: Manual re-authentication required

### Error Handling
```json
{
  "error": {
    "code": "INVALID_TOKEN",
    "message": "JWT token has expired",
    "details": {
      "expired_at": "2024-10-03T13:00:00Z"
    }
  }
}
```

## Troubleshooting

### Common Issues

1. **401 Unauthorized - Missing API Key**
   ```bash
   curl -H "Authorization: Bearer <token>" http://localhost:8000/generate
   # Missing X-API-Key header
   ```
   **Solution**: Add `X-API-Key: bhiv-secret-key-2024`

2. **403 Forbidden - Invalid JWT**
   ```bash
   curl -H "X-API-Key: bhiv-secret-key-2024" -H "Authorization: Bearer invalid" http://localhost:8000/generate
   ```
   **Solution**: Get new token from `/api/v1/auth/login`

3. **429 Rate Limited**
   ```json
   {
     "error": {
       "code": "RATE_LIMIT_EXCEEDED",
       "message": "Too many requests"
     }
   }
   ```
   **Solution**: Wait 60 seconds or implement exponential backoff

### Token Refresh Workflow
```python
import requests
import time

def get_fresh_token():
    response = requests.post(
        "http://localhost:8000/api/v1/auth/login",
        headers={"X-API-Key": "bhiv-secret-key-2024"},
        json={"username": "admin", "password": "bhiv2024"}
    )
    return response.json()["access_token"]

def make_authenticated_request(endpoint, data=None):
    token = get_fresh_token()
    headers = {
        "X-API-Key": "bhiv-secret-key-2024",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    if data:
        return requests.post(f"http://localhost:8000{endpoint}", headers=headers, json=data)
    else:
        return requests.get(f"http://localhost:8000{endpoint}", headers=headers)
```

## Production Considerations

### Security Hardening
1. **Rotate JWT Secret**: Change `JWT_SECRET_KEY` regularly
2. **HTTPS Only**: Never send tokens over HTTP in production
3. **Secure Headers**: Add security headers (HSTS, CSP, etc.)
4. **Token Storage**: Store tokens securely on client side

### Monitoring
- Track failed authentication attempts
- Monitor token usage patterns
- Alert on suspicious activity
- Log all authentication events

### Backup Authentication
- Keep admin credentials secure
- Have backup API keys ready
- Document emergency access procedures