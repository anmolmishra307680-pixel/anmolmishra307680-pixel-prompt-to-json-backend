# Compute Routing Configuration

## Routing Logic

### Local Compute (Default)
- Simple prompts (< 500 chars)
- Standard iterations (< 5)
- Cost: $0.01 per job
- Provider: `local`

### Yotta Cloud Routing
- Heavy jobs: `params.heavy_job = true`
- Long prompts: > 500 characters
- High iterations: > 5 iterations
- Cost: $0.05 per job
- Provider: `yotta`

## Implementation

### LM Adapter Routing
```python
if params.get("heavy_job") or len(prompt) > 500:
    return self._route_to_yotta(prompt, params)
else:
    return self._heuristic_generate(prompt, params)
```

### Usage Logging
- File: `logs/usage_logs.json`
- Fields: provider, cost, prompt_length, timestamp
- Automatic cost tracking per job

### Environment Variables
```bash
YOTTA_API_URL=https://yotta-compute.example.com
YOTTA_API_KEY=yotta-secret-key
```

### Fallback Strategy
1. Try Yotta cloud compute
2. On failure, fallback to local compute
3. Log failed attempts for monitoring