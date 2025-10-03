# API Contract v2 - Complete Reference

## Authentication

All endpoints require dual authentication:
- **API Key**: `X-API-Key: bhiv-secret-key-2024`
- **JWT Token**: `Authorization: Bearer <token>`

### Get JWT Token
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

## Core Endpoints

### 1. Generate Design
```bash
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
  "prompt": "Modern electric vehicle with 400-mile range",
  "specification": {
    "design_type": "vehicle",
    "category": "electric_car",
    "objects": [
      {
        "id": "obj_001",
        "name": "battery_pack",
        "type": "component",
        "material": "lithium_ion",
        "dimensions": {"length": 2.0, "width": 1.5, "height": 0.3}
      }
    ],
    "materials": [
      {
        "type": "aluminum",
        "grade": "6061-T6",
        "properties": {"density": 2.7, "strength": 310}
      }
    ],
    "dimensions": {
      "length": 4.5,
      "width": 1.8,
      "height": 1.4,
      "units": "metric"
    },
    "performance": {
      "power": 300,
      "efficiency": 0.85,
      "speed": 200,
      "other_specs": {"range": 400, "charging_time": 45}
    },
    "features": ["autopilot", "fast_charging", "regenerative_braking"],
    "components": ["motor", "battery", "chassis", "body"],
    "estimated_cost": 45000,
    "metadata": {
      "editable": true,
      "version": "1.0",
      "created_at": "2024-10-03T12:00:00Z"
    }
  }
}
```

### 2. Evaluate Design
```bash
POST /api/v1/evaluate
Content-Type: application/json
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <token>

{
  "spec": {
    "design_type": "vehicle",
    "materials": [{"type": "aluminum", "grade": "6061-T6"}],
    "performance": {"power": 300, "efficiency": 0.85}
  }
}
```

**Response:**
```json
{
  "evaluation_id": "eval_123",
  "overall_score": 8.5,
  "criteria_scores": {
    "feasibility": 9.0,
    "cost_effectiveness": 8.0,
    "sustainability": 8.5,
    "innovation": 8.0,
    "market_viability": 9.0
  },
  "recommendations": [
    "Consider using recycled aluminum for better sustainability",
    "Optimize battery placement for better weight distribution"
  ],
  "timestamp": "2024-10-03T12:00:00Z"
}
```

### 3. Iterate Design
```bash
POST /api/v1/iterate
Content-Type: application/json
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <token>

{
  "spec": {
    "design_type": "vehicle",
    "materials": [{"type": "aluminum"}]
  },
  "feedback": "Make it more sustainable",
  "iterations": 3
}
```

**Response:**
```json
{
  "iteration_id": "iter_456",
  "improved_spec": {
    "design_type": "vehicle",
    "materials": [{"type": "recycled_aluminum", "sustainability_score": 9.5}],
    "performance": {"efficiency": 0.90}
  },
  "improvements": [
    "Switched to recycled aluminum (+15% sustainability)",
    "Improved efficiency by 5%"
  ],
  "iteration_count": 3,
  "timestamp": "2024-10-03T12:00:00Z"
}
```

## Mobile API

### Mobile Generate
```bash
POST /api/v1/mobile/generate
Content-Type: application/json
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <token>

{
  "prompt": "Compact smart home device",
  "platform": "react-native",
  "optimize_for_mobile": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "spec": {
      "design_type": "electronics",
      "mobile_optimized": true
    },
    "mobile_features": {
      "touch_optimized": true,
      "responsive_design": true
    }
  },
  "mobile_optimized": true
}
```

### Mobile Preview
```bash
POST /api/v1/mobile/preview
Content-Type: application/json
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <token>

{
  "spec_id": "spec_123",
  "format": "base64",
  "size": "mobile"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "preview_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ...",
    "dimensions": {"width": 400, "height": 300},
    "mobile_optimized": true
  }
}
```

## VR/AR API

### VR Generate
```bash
POST /api/v1/vr/generate
Content-Type: application/json
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <token>

{
  "prompt": "Interactive office space",
  "vr_platform": "oculus",
  "immersion_level": "full"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "vr_spec": {
      "design_type": "vr_experience",
      "vr_metadata": {
        "platform": "oculus",
        "immersion_level": "full",
        "interaction_methods": ["hand_tracking", "controllers"]
      },
      "scene_objects": [
        {
          "id": "obj_001",
          "type": "interactive_element",
          "position": [0, 1.2, -2]
        }
      ]
    },
    "unity_package": "vr_scene_001.unitypackage",
    "webxr_compatible": true
  },
  "vr_compatible": true
}
```

### VR Export
```bash
POST /api/v1/vr/export?spec_id=spec_123&format=unity
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "spec_id": "spec_123",
    "format": "unity",
    "download_url": "/downloads/vr_export_spec_123.unity",
    "unity_version": "2022.3 LTS",
    "packages": ["XR Toolkit", "Universal RP"]
  }
}
```

## Preview & Storage

### Generate Preview
```bash
POST /api/v1/preview/generate
Content-Type: application/json
X-API-Key: bhiv-secret-key-2024
Authorization: Bearer <token>

{
  "spec_id": "spec_123",
  "format": "threejs",
  "quality": "high"
}
```

**Response:**
```json
{
  "success": true,
  "preview_url": "https://bucket.bhiv.com/previews/spec_123.jpg",
  "threejs_data": {
    "geometry": {...},
    "materials": {...},
    "scene": {...}
  },
  "expires_at": "2024-10-04T12:00:00Z"
}
```

## Error Responses

All endpoints return consistent error format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid prompt format",
    "details": {
      "field": "prompt",
      "issue": "Cannot be empty"
    }
  },
  "timestamp": "2024-10-03T12:00:00Z"
}
```

## Rate Limits

- **Protected Endpoints**: 20 requests/minute
- **Public Health**: No limit
- **Batch Operations**: 5 requests/minute

## Status Codes

- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized (missing/invalid API key)
- `403` - Forbidden (invalid JWT token)
- `429` - Rate Limit Exceeded
- `500` - Internal Server Error