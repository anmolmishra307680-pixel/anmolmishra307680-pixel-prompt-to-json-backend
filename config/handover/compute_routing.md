# Compute Routing Configuration

## Overview
Intelligent routing between local RTX-3060 and Yotta cloud based on complexity analysis.

## Routing Logic

### Complexity Calculation
```python
complexity = len(prompt.split())  # Base word count
complexity += len(str(context)) // 10  # Context bonus
complexity += 20 * keyword_matches  # Keyword multipliers
```

### Keywords Adding Complexity (+20 each)
- "detailed"
- "complex" 
- "advanced"
- "comprehensive"

### Routing Decision
```
if complexity < COMPLEXITY_THRESHOLD:
    → Local RTX-3060 ($0.001/token)
else:
    → Yotta Cloud ($0.01/token)
    → Fallback to Local on failure
```

## Configuration

### Environment Variables
```bash
COMPLEXITY_THRESHOLD=100
YOTTA_URL=http://yotta-service:8000
LOCAL_COST_PER_TOKEN=0.001
YOTTA_COST_PER_TOKEN=0.01
```

### Threshold Guidelines
- **< 50**: Simple prompts (local only)
- **50-100**: Medium complexity (configurable)
- **> 100**: Complex prompts (cloud preferred)

## Usage Logs

### Job Logging Format
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "job_type": "generation_v2",
  "complexity": 45,
  "compute_type": "local_rtx3060",
  "cost": 0.045
}
```

### Log Files
- **Location**: `logs/compute_jobs.json`
- **Retention**: 30 days default
- **Format**: JSON array of job entries

## Monitoring

### Metrics Available
```bash
# Get compute statistics
curl http://localhost:8000/api/v1/metrics/detailed \
  -H "X-API-Key: bhiv-secret-key-2024" \
  -H "Authorization: Bearer <token>"
```

### Key Metrics
- `total_jobs`: Total compute jobs processed
- `total_cost`: Cumulative compute costs
- `local_jobs`: Jobs processed locally
- `yotta_jobs`: Jobs routed to cloud
- `avg_complexity`: Average complexity score

## Cost Analysis

### Local RTX-3060
- **Cost**: $0.001 per token
- **Latency**: ~100ms
- **Capacity**: 1000 jobs/hour
- **Best For**: Simple to medium complexity

### Yotta Cloud
- **Cost**: $0.01 per token (10x more expensive)
- **Latency**: ~500ms
- **Capacity**: Unlimited
- **Best For**: Complex, resource-intensive tasks

### Cost Optimization
1. **Tune Threshold**: Adjust based on cost/performance needs
2. **Monitor Usage**: Track cost trends
3. **Batch Processing**: Group similar complexity jobs

## Troubleshooting

### Common Issues
1. **High Costs**: Lower complexity threshold
2. **Slow Performance**: Increase threshold for more cloud usage
3. **Cloud Failures**: Check Yotta service availability

### Debug Commands
```bash
# Check routing decision
python -c "
from src.compute_router import compute_router
complexity = compute_router._calculate_complexity('your prompt here')
print(f'Complexity: {complexity}')
print(f'Route: {'local' if complexity < 100 else 'cloud'}')
"

# View job logs
cat logs/compute_jobs.json | jq '.[-10:]'  # Last 10 jobs
```

## Performance Tuning

### Threshold Optimization
- **Start**: 100 (default)
- **Monitor**: Cost vs performance
- **Adjust**: Based on usage patterns

### Batch Processing
- Group similar prompts
- Process during off-peak hours
- Use local for development/testing