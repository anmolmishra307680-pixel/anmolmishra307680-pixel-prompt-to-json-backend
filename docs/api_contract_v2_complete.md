# Complete API Contract v2 - All Endpoints

## Authentication
All endpoints require dual authentication unless specified:
- **API Key**: `X-API-Key: bhiv-secret-key-2024`
- **JWT Token**: `Authorization: Bearer <token>`

## Core Generation Endpoints

### POST /api/v1/generate
Enhanced generation with LM adapter integration.

**Request**:
```json
{
  "prompt": "Modern electric vehicle with aerodynamic design",
  "context": {"target_audience": "luxury market"},
  "style": "futuristic",
  "constraints": ["environmentally friendly", "maximum 4 seats"]
}
```

**Response**:
```json
{
  "spec_id": "550e8400-e29b-41d4-a716-446655440000",
  "spec_json": {
    "spec_id": "550e8400-e29b-41d4-a716-446655440000",
    "objects": [
      {
        "id": "obj_001",
        "type": "main_structure",
        "material": "carbon_fiber",
        "position": {"x": 0.0, "y": 0.0, "z": 0.0},
        "dimensions": {"width": 10.0, "height": 3.0, "depth": 10.0, "units": "meters"},
        "editable": true,
        "properties": {"design_type": "vehicle", "features": ["aerodynamic", "electric"]}
      }
    ],
    "scene": {
      "name": "Vehicle from prompt",
      "description": "Modern electric vehicle with aerodynamic design",
      "total_objects": 1,
      "bounding_box": {"width": 50.0, "height": 20.0, "depth": 50.0, "units": "meters"}
    },
    "version": {
      "version": "1.0",
      "created_at": "2024-01-15T10:30:00Z",
      "modified_at": "2024-01-15T10:30:00Z",
      "author": "system"
    },
    "metadata": {
      "original_spec": {"design_type": "vehicle", "category": "electric"},
      "generation_method": "lm_adapter",
      "style": "futuristic"
    }
  },
  "preview_url": "https://storage.bhiv.com/preview/550e8400-e29b-41d4-a716-446655440000.png?expires=1705320600&signature=a1b2c3d4e5f6...",
  "created_at": "2024-01-15T10:30:00Z",
  "processing_time": 0.245
}
```

### POST /api/v1/switch
Material switching with natural language instructions.

**Request**:
```json
{
  "spec_id": "550e8400-e29b-41d4-a716-446655440000",
  "instruction": "change floor to marble"
}
```

**Response**:
```json
{
  "spec_id": "550e8400-e29b-41d4-a716-446655440000",
  "updated_spec_json": {
    "spec_id": "550e8400-e29b-41d4-a716-446655440000",
    "objects": [
      {
        "id": "floor_obj_001",
        "type": "floor",
        "material": "marble",
        "position": {"x": 0.0, "y": 0.0, "z": 0.0},
        "dimensions": {"width": 10.0, "height": 0.1, "depth": 10.0, "units": "meters"},
        "editable": true,
        "properties": {"color": "white", "finish": "polished"}
      }
    ],
    "version": {
      "version": "1.1",
      "modified_at": "2024-01-15T10:35:00Z"
    }
  },
  "preview_url": "https://storage.bhiv.com/preview/550e8400-e29b-41d4-a716-446655440000.png?expires=1705320900&signature=b2c3d4e5f6g7...",
  "iteration_id": "iter_123456",
  "changed": {
    "object_id": "floor_obj_001",
    "before": {"material": "wood", "properties": {"color": "brown"}},
    "after": {"material": "marble", "properties": {"color": "white", "finish": "polished"}}
  },
  "saved_at": "2024-01-15T10:35:00Z"
}
```

## Compliance Endpoints

### POST /api/v1/compliance/run_case
Proxy to Soham's compliance service.

**Request**:
```json
{
  "case_id": "case_123456",
  "project_id": "project_789",
  "spec_data": {
    "design_type": "building",
    "objects": [{"type": "wall", "material": "concrete"}]
  },
  "compliance_rules": ["accessibility", "fire_safety", "building_codes"]
}
```

**Response**:
```json
{
  "success": true,
  "case_id": "case_123456",
  "result": {
    "status": "passed",
    "score": 85,
    "violations": [],
    "recommendations": ["Add emergency exits", "Improve accessibility ramps"]
  },
  "geometry_url": "/geometry/case_123456.stl",
  "message": "Compliance case processed"
}
```

### POST /api/v1/compliance/feedback
Send feedback to compliance service.

**Request**:
```json
{
  "case_id": "case_123456",
  "feedback_type": "correction",
  "feedback_data": {
    "violation_id": "v001",
    "user_correction": "Added required fire exit",
    "confidence": 0.9
  }
}
```

**Response**:
```json
{
  "success": true,
  "result": {
    "feedback_id": "fb_789",
    "status": "received",
    "impact": "high"
  },
  "message": "Compliance feedback sent"
}
```

## Pipeline Endpoints

### POST /api/v1/pipeline/run
End-to-end pipeline: spec → compliance → geometry.

**Request**:
```json
{
  "prompt": "Modern office building with sustainable features",
  "project_id": "project_456",
  "compliance_rules": ["LEED", "accessibility", "fire_safety"]
}
```

**Response**:
```json
{
  "success": true,
  "pipeline_id": "pipeline_789",
  "spec_data": {
    "design_type": "building",
    "objects": [{"type": "structure", "material": "steel"}]
  },
  "compliance_result": {
    "status": "passed",
    "score": 92,
    "violations": []
  },
  "geometry_url": "/geometry/pipeline_789.stl",
  "message": "Pipeline completed successfully"
}
```

## Mobile Endpoints

### POST /api/v1/mobile/generate
Mobile-optimized generation for React Native/Expo.

**Request**:
```json
{
  "prompt": "Modern chair design",
  "device_info": {"platform": "ios", "version": "17.0"},
  "location": {"lat": 37.7749, "lng": -122.4194}
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "spec_id": "mobile_chair_1705320600",
    "spec_json": {
      "objects": [
        {
          "id": "chair_001",
          "type": "chair",
          "material": "wood",
          "editable": true
        }
      ],
      "scene": {"name": "Mobile Chair", "total_objects": 1}
    },
    "preview_url": "/mobile/preview/chair.jpg",
    "mobile_metadata": {
      "optimized": true,
      "reduced_payload": true,
      "cache_recommended": true
    }
  },
  "mobile_optimized": true,
  "message": "Mobile generation completed"
}
```

### POST /api/v1/mobile/switch
Mobile-optimized material switching.

**Request**:
```json
{
  "spec_id": "mobile_chair_1705320600",
  "instruction": "make it leather",
  "device_info": {"platform": "android", "version": "14.0"}
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "spec_id": "mobile_chair_1705320600",
    "updated_spec_json": {
      "objects": [
        {
          "id": "chair_001",
          "type": "chair",
          "material": "leather",
          "editable": true
        }
      ]
    },
    "preview_url": "/mobile/preview/mobile_chair_1705320600.jpg",
    "changed": {
      "object_id": "chair_001",
      "material": "leather"
    },
    "mobile_metadata": {"optimized": true}
  },
  "mobile_optimized": true,
  "message": "Mobile switch completed"
}
```

## VR/AR Endpoints (Stubs)

### POST /api/v1/vr/generate
VR scene generation for Bhavesh.

**Request**:
```json
{
  "prompt": "VR office environment",
  "vr_context": {"room_scale": true, "hand_tracking": true},
  "headset_type": "oculus"
}
```

**Response**:
```json
{
  "success": true,
  "vr_scene": {
    "vr_scene_id": "vr_scene_123",
    "unity_package_url": "/vr/scenes/vr_scene_123.unitypackage",
    "oculus_compatible": true,
    "spatial_anchors": [
      {"id": "anchor_1", "position": [0, 0, 0]},
      {"id": "anchor_2", "position": [5, 0, 0]}
    ],
    "interaction_points": [
      {"object_id": "obj_1", "interaction_type": "grab"},
      {"object_id": "obj_2", "interaction_type": "modify"}
    ]
  },
  "message": "VR scene generated (stub implementation)"
}
```

### POST /api/v1/ar/overlay
AR overlay creation for mobile AR.

**Request**:
```json
{
  "spec_id": "spec_123",
  "camera_position": {"x": 0, "y": 1.6, "z": 0},
  "surface_detection": {"plane_detection": true, "vertical_planes": false}
}
```

**Response**:
```json
{
  "success": true,
  "ar_overlay": {
    "ar_overlay_id": "ar_overlay_123",
    "arcore_config": {
      "plane_detection": true,
      "light_estimation": true,
      "occlusion": false
    },
    "arkit_config": {
      "world_tracking": true,
      "face_tracking": false,
      "image_tracking": true
    },
    "overlay_objects": [
      {
        "id": "overlay_obj_1",
        "type": "3d_model",
        "position": [0, 0, -2],
        "scale": [1, 1, 1]
      }
    ]
  },
  "message": "AR overlay created (stub implementation)"
}
```

## Authentication Endpoints

### POST /api/v1/auth/login
JWT login with refresh tokens.

**Request**:
```json
{
  "username": "admin",
  "password": "bhiv2024"
}
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

### POST /api/v1/auth/refresh
Refresh access token.

**Request**:
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
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

## Frontend Integration Endpoints

### POST /api/v1/ui/session
Create UI testing session.

**Request**:
```json
{
  "session_id": "ui_session_123",
  "user": "yash",
  "browser": "chrome",
  "test_type": "integration"
}
```

**Response**:
```json
{
  "success": true,
  "session": {
    "session_id": "ui_session_123",
    "user_data": {"user": "yash", "browser": "chrome"},
    "created_at": "2024-01-15T10:30:00Z",
    "flows_completed": [],
    "three_js_ready": false
  },
  "message": "UI session created"
}
```

### GET /api/v1/three-js/{spec_id}
Get Three.js formatted data.

**Response**:
```json
{
  "success": true,
  "spec_id": "spec_123",
  "three_js_data": {
    "scene": {
      "objects": [
        {
          "id": "floor_1",
          "type": "floor",
          "geometry": {"type": "PlaneGeometry", "args": [10, 10]},
          "material": {
            "type": "MeshLambertMaterial",
            "color": "#8B4513",
            "properties": {}
          },
          "position": [0, 0, 0],
          "scale": [10, 0.1, 10],
          "editable": true
        }
      ],
      "camera": {"position": [0, 10, 20], "target": [0, 0, 0]},
      "lighting": {
        "ambient": 0.4,
        "directional": {"intensity": 0.8, "position": [10, 10, 5]}
      }
    },
    "metadata": {
      "spec_id": "spec_123",
      "object_count": 1,
      "editable_objects": ["floor_1"]
    }
  }
}
```

## Monitoring Endpoints

### GET /metrics (Public)
Prometheus metrics endpoint.

**Response**:
```
# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total 1247

# HELP compute_jobs_total Total compute jobs
# TYPE compute_jobs_total counter
compute_jobs_total 156

# HELP compute_cost_total Total compute cost
# TYPE compute_cost_total gauge
compute_cost_total 12.45
```

### GET /api/v1/metrics/detailed
Detailed metrics with authentication.

**Response**:
```json
{
  "health": {
    "status": "healthy",
    "uptime_seconds": 86400,
    "requests_total": 1247,
    "errors_total": 12,
    "database_status": "healthy"
  },
  "compute": {
    "total_jobs": 156,
    "total_cost": 12.45,
    "local_jobs": 140,
    "yotta_jobs": 16,
    "avg_complexity": 67.3
  },
  "timestamp": "2024-01-15T10:30:00Z"
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
  "detail": "Invalid or missing API key",
  "error_code": "AUTHENTICATION_ERROR",
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
  "detail": "Internal server error",
  "error_code": "INTERNAL_ERROR",
  "timestamp": "2024-01-15T10:30:00Z"
}
```