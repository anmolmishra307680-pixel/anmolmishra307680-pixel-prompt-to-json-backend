# 🔧 DOCKER 401 ERROR - IMMEDIATE FIX

## ❌ Your Problem
You're running: `docker run --rm -d --name test-container -p 8000:8000 IMAGE_ID`

This gives 401 error because **NO ENVIRONMENT VARIABLES**.

## ✅ EXACT FIX

**Instead of your command, use this:**

```bash
docker run --rm -d --name test-container -p 8000:8000 \
  -e API_KEY=test-api-key \
  -e DEMO_USERNAME=testuser \
  -e DEMO_PASSWORD=testpass \
  -e JWT_SECRET=test-jwt-secret \
  -e SECRET_KEY=test-secret-key \
  prompt-backend
```

## 🧪 Test Commands

**1. Get Token:**
```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass"}'
```

**2. Use Token:**
```bash
curl -X GET "http://localhost:8000/health" \
  -H "X-API-Key: test-api-key" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🎯 The Issue
- Your image requires environment variables for authentication
- Without `-e API_KEY=...` the container has no credentials
- All endpoints except `/token` and `/metrics` require dual auth

## ✅ Working Solution
Always include the `-e` environment variables when running the container.