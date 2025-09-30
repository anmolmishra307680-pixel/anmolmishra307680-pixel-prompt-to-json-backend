# API Contract v2 - Complete Endpoint Documentation

## Overview
Complete API documentation for all v2 endpoints with exact request/response schemas, authentication requirements, and integration examples.

## Authentication
All protected endpoints require dual authentication:
- **API Key**: `X-API-Key: bhiv-secret-key-2024` header
- **JWT Token**: `Authorization: Bearer <token>` header

## Endpoints

### POST /api/v1/generate
Generate design specifications from natural language prompts.

**Headers:**
```
Content-Type: application/json
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <jwt-token>
```

**Request Schema:**
```json
{
  "user_id": "string",
  "prompt": "string",
  "context": {
    "style": "string",
    "budget": "string",
    "constraints": ["string"]
  }
}
```

**Example Request:**
```json
{
  "user_id": "u123",
  "prompt": "Living room with marble floor",
  "context": {
    "style": "modern",
    "budget": "high-end",
    "constraints": ["eco-friendly materials"]
  }
}
```

**Response Schema:**
```json
{
  "spec_id": "string",
  "spec_json": {
    "objects": [
      {
        "object_id": "string",
        "type": "string",
        "material": "string",
        "dimensions": {
          "width": "number",
          "height": "number",
          "depth": "number"
        },
        "position": {
          "x": "number",
          "y": "number", 
          "z": "number"
        },
        "editable": "boolean"
      }
    ],
    "scene": {
      "name": "string",
      "description": "string",
      "total_objects": "number"
    }
  },
  "preview_url": "string",
  "processing_time": "number"
}
```

**Example Response:**
```json
{
  "spec_id": "spec_001",
  "spec_json": {
    "objects": [
      {
        "object_id": "floor_1",
        "type": "floor",
        "material": "marble_white",
        "dimensions": {"width": 5.0, "height": 0.1, "depth": 4.0},
        "position": {"x": 0.0, "y": 0.0, "z": 0.0},
        "editable": true
      }
    ],
    "scene": {
      "name": "Modern Living Room",
      "description": "Living room with marble floor",
      "total_objects": 1
    }
  },
  "preview_url": "/preview/spec_001.jpg",
  "processing_time": 0.245
}
```

### POST /api/v1/switch
Switch object materials/properties based on natural language instruction.

**Headers:**
```
Content-Type: application/json
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <jwt-token>
```

**Request Schema:**
```json
{
  "user_id": "string",
  "spec_id": "string",
  "target": {
    "object_id": "string"
  },
  "update": {
    "material": "string",
    "properties": {}
  }
}
```

**Example Request:**
```json
{
  "user_id": "u123",
  "spec_id": "spec_001",
  "target": {
    "object_id": "floor_1"
  },
  "update": {
    "material": "marble_black"
  }
}
```

**Response Schema:**
```json
{
  "spec_id": "string",
  "updated_spec_json": {},
  "preview_url": "string",
  "iteration_id": "string",
  "changed": {
    "object_id": "string",
    "before": {},
    "after": {}
  }
}
```

**Example Response:**
```json
{
  "spec_id": "spec_001",
  "updated_spec_json": {
    "objects": [
      {
        "object_id": "floor_1",
        "type": "floor",
        "material": "marble_black",
        "dimensions": {"width": 5.0, "height": 0.1, "depth": 4.0},
        "position": {"x": 0.0, "y": 0.0, "z": 0.0},
        "editable": true
      }
    ]
  },
  "preview_url": "/preview/spec_001_v2.jpg",
  "iteration_id": "iter_001",
  "changed": {
    "object_id": "floor_1",
    "before": {"material": "marble_white"},
    "after": {"material": "marble_black"}
  }
}
```

### POST /api/v1/evaluate
Evaluate design specifications against criteria.

**Headers:**
```
Content-Type: application/json
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <jwt-token>
```

**Request Schema:**
```json
{
  "user_id": "string",
  "spec_id": "string",
  "criteria": ["string"]
}
```

**Example Request:**
```json
{
  "user_id": "u123",
  "spec_id": "spec_001",
  "criteria": ["aesthetics", "functionality", "cost"]
}
```

**Response Schema:**
```json
{
  "evaluation_id": "string",
  "spec_id": "string",
  "scores": {
    "overall": "number",
    "criteria": {
      "aesthetics": "number",
      "functionality": "number",
      "cost": "number"
    }
  },
  "feedback": "string",
  "recommendations": ["string"]
}
```

**Example Response:**
```json
{
  "evaluation_id": "eval_001",
  "spec_id": "spec_001",
  "scores": {
    "overall": 8.5,
    "criteria": {
      "aesthetics": 9.0,
      "functionality": 8.0,
      "cost": 8.5
    }
  },
  "feedback": "Excellent material choice with good functionality",
  "recommendations": ["Consider adding accent lighting", "Optimize material costs"]
}
```

### POST /api/v1/iterate
Run reinforcement learning iterations for design improvement.

**Headers:**
```
Content-Type: application/json
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <jwt-token>
```

**Request Schema:**
```json
{
  "user_id": "string",
  "spec_id": "string",
  "strategy": "string",
  "max_iterations": "number"
}
```

**Example Request:**
```json
{
  "user_id": "u123",
  "spec_id": "spec_001",
  "strategy": "improve_materials",
  "max_iterations": 5
}
```

**Response Schema:**
```json
{
  "session_id": "string",
  "spec_id": "string",
  "iterations": [
    {
      "iteration": "number",
      "before_spec": {},
      "after_spec": {},
      "score_improvement": "number",
      "feedback": "string"
    }
  ],
  "final_spec": {},
  "preview_url": "string"
}
```

**Example Response:**
```json
{
  "session_id": "rl_session_001",
  "spec_id": "spec_001",
  "iterations": [
    {
      "iteration": 1,
      "before_spec": {"material": "marble_black"},
      "after_spec": {"material": "marble_carrara"},
      "score_improvement": 0.5,
      "feedback": "Upgraded to premium marble"
    }
  ],
  "final_spec": {"material": "marble_carrara"},
  "preview_url": "/preview/spec_001_final.jpg"
}
```

### POST /api/v1/compliance/run_case
Run compliance checks on design specifications.

**Headers:**
```
Content-Type: application/json
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <jwt-token>
```

**Request Schema:**
```json
{
  "user_id": "string",
  "spec_id": "string",
  "case_id": "string",
  "compliance_rules": ["string"]
}
```

**Example Request:**
```json
{
  "user_id": "u123",
  "spec_id": "spec_001",
  "case_id": "case_001",
  "compliance_rules": ["building_code", "accessibility", "fire_safety"]
}
```

**Response Schema:**
```json
{
  "case_id": "string",
  "spec_id": "string",
  "compliance_results": {
    "overall_status": "string",
    "rule_results": {
      "building_code": {
        "status": "string",
        "score": "number",
        "issues": ["string"]
      }
    }
  },
  "geometry_url": "string",
  "report_url": "string"
}
```

**Example Response:**
```json
{
  "case_id": "case_001",
  "spec_id": "spec_001",
  "compliance_results": {
    "overall_status": "PASSED",
    "rule_results": {
      "building_code": {
        "status": "PASSED",
        "score": 95,
        "issues": []
      },
      "accessibility": {
        "status": "WARNING",
        "score": 85,
        "issues": ["Consider wider doorways"]
      }
    }
  },
  "geometry_url": "/geometry/case_001.stl",
  "report_url": "/reports/case_001.pdf"
}
```

### POST /api/v1/compliance/feedback
Submit feedback on compliance results.

**Headers:**
```
Content-Type: application/json
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <jwt-token>
```

**Request Schema:**
```json
{
  "user_id": "string",
  "case_id": "string",
  "feedback": {
    "rating": "number",
    "comments": "string",
    "suggestions": ["string"]
  }
}
```

**Example Request:**
```json
{
  "user_id": "u123",
  "case_id": "case_001",
  "feedback": {
    "rating": 4,
    "comments": "Good compliance check, helpful suggestions",
    "suggestions": ["Add more detailed accessibility guidelines"]
  }
}
```

**Response Schema:**
```json
{
  "feedback_id": "string",
  "case_id": "string",
  "status": "string",
  "message": "string"
}
```

**Example Response:**
```json
{
  "feedback_id": "feedback_001",
  "case_id": "case_001",
  "status": "received",
  "message": "Feedback recorded successfully"
}
```

### POST /api/v1/core/run
Execute core design generation pipeline.

**Headers:**
```
Content-Type: application/json
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <jwt-token>
```

**Request Schema:**
```json
{
  "user_id": "string",
  "pipeline": "string",
  "input_data": {},
  "options": {
    "async": "boolean",
    "priority": "string"
  }
}
```

**Example Request:**
```json
{
  "user_id": "u123",
  "pipeline": "full_design_generation",
  "input_data": {
    "prompt": "Modern kitchen design",
    "constraints": ["budget: $50k", "space: 200sqft"]
  },
  "options": {
    "async": true,
    "priority": "high"
  }
}
```

**Response Schema:**
```json
{
  "job_id": "string",
  "status": "string",
  "result": {},
  "processing_time": "number",
  "queue_position": "number"
}
```

**Example Response:**
```json
{
  "job_id": "job_001",
  "status": "completed",
  "result": {
    "spec_id": "spec_kitchen_001",
    "generated_objects": 15,
    "compliance_score": 92
  },
  "processing_time": 2.5,
  "queue_position": 0
}
```

### GET /api/v1/reports/{spec_id}
Retrieve detailed reports for specifications.

**Headers:**
```
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <jwt-token>
```

**Path Parameters:**
- `spec_id`: Specification ID

**Response Schema:**
```json
{
  "spec_id": "string",
  "report": {
    "generation_details": {},
    "evaluation_history": [],
    "compliance_results": {},
    "iteration_logs": []
  },
  "created_at": "string",
  "last_updated": "string"
}
```

**Example Response:**
```json
{
  "spec_id": "spec_001",
  "report": {
    "generation_details": {
      "prompt": "Living room with marble floor",
      "processing_time": 0.245,
      "agent_used": "MainAgent"
    },
    "evaluation_history": [
      {
        "evaluation_id": "eval_001",
        "score": 8.5,
        "timestamp": "2024-01-15T10:30:00Z"
      }
    ],
    "compliance_results": {
      "case_001": {
        "status": "PASSED",
        "score": 95
      }
    },
    "iteration_logs": []
  },
  "created_at": "2024-01-15T10:30:00Z",
  "last_updated": "2024-01-15T10:35:00Z"
}
```

### POST /api/v1/auth/login
Authenticate user and receive JWT tokens.

**Headers:**
```
Content-Type: application/json
X-API-Key: bhiv-secret-key-2024
```

**Request Schema:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Example Request:**
```json
{
  "username": "admin",
  "password": "bhiv2024"
}
```

**Response Schema:**
```json
{
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "string",
  "expires_in": "number"
}
```

**Example Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### GET /api/v1/health
System health check (public endpoint).

**Headers:**
```
None required (public endpoint)
```

**Response Schema:**
```json
{
  "status": "string",
  "database": "boolean",
  "agents": ["string"],
  "timestamp": "string"
}
```

**Example Response:**
```json
{
  "status": "healthy",
  "database": true,
  "agents": ["prompt", "evaluator", "rl"],
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### GET /api/v1/metrics
Prometheus metrics (public endpoint).

**Headers:**
```
None required (public endpoint)
```

**Response:**
```
# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{method="POST",endpoint="/api/v1/generate"} 1234
# HELP generation_time_seconds Time spent generating specifications
# TYPE generation_time_seconds histogram
generation_time_seconds_bucket{le="0.1"} 45
generation_time_seconds_bucket{le="0.5"} 123
```

### DELETE /api/v1/data/{user_id}
Delete all user data (GDPR compliance).

**Headers:**
```
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <jwt-token>
```

**Path Parameters:**
- `user_id`: User ID to delete data for

**Response Schema:**
```json
{
  "ok": "boolean",
  "deleted_records": {
    "specs": "number",
    "evaluations": "number",
    "iterations": "number",
    "feedback": "number"
  },
  "message": "string"
}
```

**Example Response:**
```json
{
  "ok": true,
  "deleted_records": {
    "specs": 15,
    "evaluations": 8,
    "iterations": 3,
    "feedback": 2
  },
  "message": "All user data deleted successfully"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request format",
  "error_code": "VALIDATION_ERROR",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid or missing API key. Include X-API-Key header.",
  "error_code": "AUTHENTICATION_ERROR",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 404 Not Found
```json
{
  "detail": "Spec not found",
  "error_code": "NOT_FOUND",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 429 Too Many Requests
```json
{
  "detail": "Rate limit exceeded: 20 per minute",
  "error_code": "RATE_LIMIT_ERROR",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 500 Internal Server Error
```json
{
  "detail": "LM inference failed: connection timeout",
  "error_code": "INTERNAL_ERROR",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Rate Limiting
- **Limit**: 20 requests per minute per IP
- **Headers**: Rate limit information included in response headers
- **Scope**: Applied per endpoint
- **Exceptions**: Health and metrics endpoints have higher limits

## Authentication Flow
1. **Get JWT Token**: POST to `/api/v1/auth/login` with API key and credentials
2. **Use Token**: Include both API key and JWT token in subsequent requests
3. **Refresh Token**: Use refresh token to get new access token when expired

## Integration Examples

### Python Integration
```python
import requests
import os

API_BASE = os.getenv("API_BASE", "http://localhost:8000/api/v1")
API_KEY = "bhiv-secret-key-2024"

def get_jwt():
    r = requests.post(f"{API_BASE}/auth/login",
                      json={"username":"admin","password":"bhiv2024"},
                      headers={"X-API-Key": API_KEY})
    return r.json()["access_token"]

TOKEN = "Bearer " + get_jwt()

# Generate design
gen = requests.post(f"{API_BASE}/generate",
                    json={"user_id":"u123","prompt":"Living room with marble floor","context":{"style":"modern"}},
                    headers={"Authorization":TOKEN, "X-API-Key": API_KEY})
spec = gen.json()

# Switch material
sw = requests.post(f"{API_BASE}/switch",
                   json={"user_id":"u123","spec_id":spec["spec_id"],"target":{"object_id":"floor_1"},"update":{"material":"marble_black"}},
                   headers={"Authorization":TOKEN, "X-API-Key": API_KEY})
```

### JavaScript Integration
```javascript
const API_BASE = process.env.API_BASE || 'http://localhost:8000/api/v1';
const API_KEY = 'bhiv-secret-key-2024';

async function getJWT() {
  const response = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': API_KEY
    },
    body: JSON.stringify({
      username: 'admin',
      password: 'bhiv2024'
    })
  });
  const data = await response.json();
  return data.access_token;
}

async function generateDesign(prompt) {
  const token = await getJWT();
  const response = await fetch(`${API_BASE}/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      'X-API-Key': API_KEY
    },
    body: JSON.stringify({
      user_id: 'u123',
      prompt: prompt,
      context: { style: 'modern' }
    })
  });
  return response.json();
}
```

## Performance Characteristics
- **Response Time**: <200ms average for standard requests
- **Throughput**: 1000+ requests/minute sustained
- **Concurrent Users**: Validated for 1000+ simultaneous users
- **Reliability**: 99.9% uptime with automatic failover

## Security Features
- **Dual Authentication**: API key + JWT token required
- **Input Validation**: Comprehensive request validation
- **Rate Limiting**: Per-IP and per-user limits
- **Error Sanitization**: No sensitive data in error responses
- **Audit Logging**: All requests logged for security monitoring
- **GDPR Compliance**: User data deletion endpoint available