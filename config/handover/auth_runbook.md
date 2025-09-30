# Authentication Runbook - JWT/Secret Management

## Overview
The system uses dual authentication: API Key + JWT tokens with refresh flow.

## JWT Configuration

### Environment Variables
```bash
JWT_SECRET=your-256-bit-secret-key
DEMO_USERNAME=admin
DEMO_PASSWORD=bhiv2024
API_KEY=bhiv-secret-key-2024
```

### Token Settings
- **Access Token Expiry**: 15 minutes
- **Refresh Token Expiry**: 7 days
- **Algorithm**: HS256
- **Signing Key**: Environment-based

## Authentication Flow

### 1. Get JWT Token
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: bhiv-secret-key-2024" \
  -d '{"username":"admin","password":"bhiv2024"}'
```

**Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 900
}
```

### 2. Use Token for Protected Endpoints
```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: bhiv-secret-key-2024" \
  -H "Authorization: Bearer <access-token>" \
  -d '{"prompt":"Modern office building"}'
```

### 3. Refresh Token
```bash
curl -X POST "http://localhost:8000/api/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: bhiv-secret-key-2024" \
  -d '{"refresh_token":"<refresh-token>"}'
```

## Security Best Practices

### Production Deployment
1. **Generate Strong JWT Secret**:
   ```bash
   openssl rand -hex 32
   ```

2. **Rotate Secrets Regularly**:
   - JWT secrets every 90 days
   - API keys every 30 days

3. **Environment Security**:
   - Never commit secrets to git
   - Use environment variables
   - Encrypt secrets at rest

### Token Management
- **Short Access Tokens**: Minimize exposure window
- **Secure Refresh Flow**: Long-lived but revocable
- **Automatic Expiry**: No manual cleanup needed

## Troubleshooting

### Common Issues
1. **Invalid Token**: Check expiry and signature
2. **Missing API Key**: Ensure X-API-Key header
3. **Wrong Credentials**: Verify username/password

### Debug Commands
```bash
# Check token validity
python -c "import jwt; print(jwt.decode('TOKEN', verify=False))"

# Test authentication
curl -v http://localhost:8000/api/v1/auth/login \
  -H "X-API-Key: bhiv-secret-key-2024" \
  -d '{"username":"admin","password":"bhiv2024"}'
```

## Monitoring
- Failed authentication attempts logged
- Token usage tracked in metrics
- Sentry integration for auth errors