# 🐳 Docker Setup Guide

## Quick Fix for 401 Error

The 401 error occurs because the API requires **dual authentication** (API Key + JWT Token). Here's how to run the Docker container properly:

### Option 1: Run with Environment Variables

```bash
# Stop existing container
docker stop test-container 2>/dev/null || true

# Run with proper environment variables
docker run --rm -d \
  --name prompt-backend \
  -p 8000:8000 \
  -e API_KEY="test-api-key" \
  -e DEMO_USERNAME="testuser" \
  -e DEMO_PASSWORD="testpass" \
  -e JWT_SECRET="test-jwt-secret" \
  -e SECRET_KEY="test-secret-key" \
  -e TESTING="false" \
  -e PRODUCTION_MODE="false" \
  879b4a0be9f5d8add257d33fb09a482a9c431e3abe742628084f811e66ea61b5
```

### Option 2: Use Environment File

```bash
# Run with environment file
docker run --rm -d \
  --name prompt-backend \
  -p 8000:8000 \
  --env-file .env.docker \
  879b4a0be9f5d8add257d33fb09a482a9c431e3abe742628084f811e66ea61b5
```

### Option 3: Use Provided Scripts

**Windows:**
```cmd
docker-run.bat
```

**Linux/Mac:**
```bash
chmod +x docker-run.sh
./docker-run.sh
```

## Testing the Container

### 1. Get JWT Token (Public Endpoint)
```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass"}'
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### 2. Test Protected Endpoints
```bash
# Replace YOUR_TOKEN with the actual token from step 1
curl -X GET "http://localhost:8000/health" \
  -H "X-API-Key: test-api-key" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. Test Generate Endpoint
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-api-key" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"prompt":"Modern office building"}'
```

### 4. Automated Testing
```bash
# Run automated test script
python test-docker.py
```

## Container Management

### Check Container Status
```bash
docker ps
docker logs prompt-backend
```

### Stop Container
```bash
docker stop prompt-backend
```

### Container Health Check
```bash
docker exec prompt-backend curl -f http://localhost:8000/metrics || echo "Container unhealthy"
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_KEY` | `test-api-key` | API key for authentication |
| `DEMO_USERNAME` | `testuser` | Username for JWT token |
| `DEMO_PASSWORD` | `testpass` | Password for JWT token |
| `JWT_SECRET` | `test-jwt-secret` | JWT signing secret |
| `SECRET_KEY` | `test-secret-key` | Application secret key |
| `TESTING` | `false` | Enable test mode |
| `PRODUCTION_MODE` | `false` | Enable production mode |
| `PORT` | `8000` | Server port |
| `WORKERS` | `2` | Number of workers |

## Troubleshooting

### 401 Unauthorized Error
- **Cause**: Missing or invalid authentication
- **Solution**: Use both `X-API-Key` header and `Authorization: Bearer <token>` header

### Container Won't Start
```bash
# Check logs
docker logs prompt-backend

# Check if port is available
netstat -an | grep 8000
```

### Connection Refused
```bash
# Wait for container startup
sleep 5

# Check if container is running
docker ps | grep prompt-backend
```

### Health Check Fails
```bash
# The health check requires authentication, use metrics instead
curl http://localhost:8000/metrics
```

## Production Configuration

For production deployment, use secure environment variables:

```bash
docker run --rm -d \
  --name prompt-backend-prod \
  -p 8000:8000 \
  -e API_KEY="your-secure-api-key" \
  -e DEMO_USERNAME="your-username" \
  -e DEMO_PASSWORD="your-secure-password" \
  -e JWT_SECRET="your-jwt-secret" \
  -e SECRET_KEY="your-secret-key" \
  -e PRODUCTION_MODE="true" \
  -e WORKERS="4" \
  879b4a0be9f5d8add257d33fb09a482a9c431e3abe742628084f811e66ea61b5
```

## API Endpoints Summary

- **Public**: `/token`, `/metrics`
- **Protected**: All other endpoints require dual authentication
- **Rate Limits**: 20 requests/minute for protected endpoints
- **Documentation**: http://localhost:8000/docs