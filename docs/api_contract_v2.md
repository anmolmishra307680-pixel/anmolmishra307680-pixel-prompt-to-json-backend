# API Contract v2 - LM Adapter Integration

## POST /api/v1/generate

Enhanced generation endpoint with LM Adapter integration and extended spec schema.

### Request

```json
{
  "prompt": "Modern office building with glass facade",
  "context": {
    "design_type": "building",
    "style": "modern",
    "constraints": ["budget: 1M", "height: max 10 floors"]
  },
  "design_type": "building"
}
```

### Response

```json
{
  "spec_id": "spec_12345",
  "spec_json": {
    "spec_id": "spec_12345",
    "objects": [
      {
        "id": "obj_001",
        "type": "main_structure",
        "material": "steel",
        "editable": true,
        "properties": {
          "width": 10.0,
          "height": 8.0,
          "depth": 12.0
        }
      }
    ],
    "scene": {
      "environment": "indoor",
      "lighting": "natural",
      "scale": 1.0,
      "background": null
    },
    "design_type": "building",
    "metadata": {
      "generated_from": "lm_adapter"
    }
  },
  "preview_url": "https://preview.example.com/spec_12345",
  "status": "success"
}
```

### Schema Definitions

#### ObjectSpec
```json
{
  "id": "string",
  "type": "string", 
  "material": "string",
  "editable": "boolean",
  "properties": "object"
}
```

#### SceneSpec
```json
{
  "environment": "string",
  "lighting": "string", 
  "scale": "number",
  "background": "string|null"
}
```

#### Spec
```json
{
  "spec_id": "string",
  "objects": "ObjectSpec[]",
  "scene": "SceneSpec",
  "design_type": "string|null",
  "metadata": "object|null"
}
```

### Authentication
- **API Key**: Required in `X-API-Key` header
- **JWT Token**: Required in `Authorization: Bearer <token>` header

### Sample cURL

```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: bhiv-secret-key-2024" \
  -H "Authorization: Bearer <jwt-token>" \
  -d '{
    "prompt": "Modern office building with glass facade",
    "context": {
      "design_type": "building",
      "style": "modern"
    }
  }'
```

### LM Adapter Features

- **Fallback Support**: Automatically falls back to heuristic generation if LM unavailable
- **OpenAI Integration**: Uses GPT-3.5-turbo when API key available
- **Context Awareness**: Processes context parameters for enhanced generation
- **Type Detection**: Automatically detects design type from prompt

### Error Responses

```json
{
  "detail": "Generation failed: <error message>",
  "status_code": 500
}
```

### Rate Limiting
- 20 requests per minute per IP address