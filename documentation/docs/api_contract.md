# API Contract Documentation

## Base URL
- **Production**: `https://prompt-to-json-backend.onrender.com`
- **Development**: `http://localhost:8000`

## Authentication

### Required Headers
```http
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <jwt-token>
```

### Get JWT Token
```http
POST /token
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
  "token_type": "bearer"
}
```

## Core Endpoints

### 1. Generate Design
```http
POST /generate
Content-Type: application/json
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <token>

{
  "prompt": "Modern electric vehicle with 400-mile range"
}
```

**Response:**
```json
{
  "design_type": "vehicle",
  "materials": ["carbon_fiber", "aluminum", "lithium_battery"],
  "dimensions": {"length": 4.5, "width": 1.8, "height": 1.4},
  "performance_specs": {"range_miles": 400, "acceleration_0_60": 3.5},
  "components": ["electric_motor", "battery_pack", "regenerative_brakes"],
  "features": ["autopilot", "wireless_charging", "solar_roof"],
  "sustainability": {"carbon_footprint": "zero_emission", "recyclability": 85},
  "cost_estimate": 45000
}
```

### 2. Evaluate Design
```http
POST /evaluate
Content-Type: application/json
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <token>

{
  "design_spec": { /* design object */ },
  "criteria": ["performance", "sustainability", "cost"]
}
```

### 3. Health Check (Public)
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "2.1.1"
}
```

## Design Types Supported
- `building`: Residential, commercial, industrial
- `vehicle`: Cars, trucks, aircraft, boats
- `electronics`: Computers, phones, IoT devices
- `appliance`: Kitchen, HVAC, smart home
- `furniture`: Chairs, tables, storage

## Error Responses
```json
{
  "detail": "Authentication failed",
  "status_code": 401
}
```

## Rate Limits
- **Protected Endpoints**: 20 requests/minute
- **Public Endpoints**: No limit

## Integration Examples

### JavaScript/React
```javascript
const response = await fetch('https://prompt-to-json-backend.onrender.com/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'bhiv-secret-key-2024',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({ prompt: 'Smart home thermostat' })
});
```

### Python
```python
import requests

headers = {
    'X-API-Key': 'bhiv-secret-key-2024',
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

response = requests.post(
    'https://prompt-to-json-backend.onrender.com/generate',
    headers=headers,
    json={'prompt': 'Sustainable office building'}
)
```

## Status Codes
- `200`: Success
- `401`: Authentication required
- `429`: Rate limit exceeded
- `500`: Server error