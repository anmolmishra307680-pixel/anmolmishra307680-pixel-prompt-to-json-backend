# 🐳 Docker Quick Start - FIXED!

## ✅ Problem Solved!

The 401 error was caused by missing environment variables. Here's the **working solution**:

## 🚀 Quick Commands

### 1. Build Image
```bash
docker build -t prompt-backend .
```

### 2. Run with Environment Variables (REQUIRED)
```bash
docker run --rm -d \
  --name prompt-backend \
  -p 8000:8000 \
  -e API_KEY=test-api-key \
  -e DEMO_USERNAME=testuser \
  -e DEMO_PASSWORD=testpass \
  -e JWT_SECRET=test-jwt-secret \
  -e SECRET_KEY=test-secret-key \
  prompt-backend
```

### 3. Test Authentication Flow

**Step 1: Get JWT Token**
```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass"}'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Step 2: Use Protected Endpoints**
```bash
# Replace YOUR_TOKEN with actual token from step 1
curl -X GET "http://localhost:8000/health" \
  -H "X-API-Key: test-api-key" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Step 3: Test Generate Endpoint**
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-api-key" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"prompt":"Modern office building"}'
```

## 🔧 Alternative Methods

### Use Environment File
```bash
# Create .env file with variables
docker run --rm -d \
  --name prompt-backend \
  -p 8000:8000 \
  --env-file .env.docker \
  prompt-backend
```

### Use Provided Scripts
**Windows:** `docker-run.bat`
**Linux/Mac:** `./docker-run.sh`

## ✅ Verification

All endpoints now work correctly:
- ✅ Token endpoint: `POST /token` (public)
- ✅ Health endpoint: `GET /health` (protected)
- ✅ Generate endpoint: `POST /generate` (protected)
- ✅ All other endpoints require dual authentication

## 🛑 Common Issues

**401 Unauthorized Error:**
- **Cause**: Missing environment variables
- **Solution**: Always include `-e API_KEY=...` and other env vars

**Container Won't Start:**
- Check logs: `docker logs prompt-backend`
- Verify port availability: `netstat -an | grep 8000`

**Connection Refused:**
- Wait 5-10 seconds for container startup
- Check container status: `docker ps`

## 🎉 Success!

Your Docker container now works perfectly with enterprise-grade dual authentication!