# Compute Routing Configuration

## Overview
Intelligent routing between local RTX-3060 GPU and Yotta cloud based on complexity and cost optimization.

## Routing Logic

### Complexity Scoring (0.0 - 1.0)
```python
def calculate_complexity(prompt, spec_data=None):
    score = 0.0
    
    # Prompt complexity
    if len(prompt.split()) > 20: score += 0.2
    if any(word in prompt.lower() for word in ["complex", "advanced", "detailed"]): score += 0.3
    
    # Design type complexity
    complexity_weights = {
        "electronics": 0.4,
        "vehicle": 0.6,
        "building": 0.7,
        "appliance": 0.3,
        "furniture": 0.2
    }
    
    # Performance requirements
    if spec_data and "performance" in spec_data:
        perf = spec_data["performance"]
        if perf.get("power", 0) > 1000: score += 0.2
        if perf.get("efficiency", 0) > 0.9: score += 0.1
    
    return min(score, 1.0)
```

### Routing Decision Matrix

| Complexity Score | Compute Target | Reasoning |
|-----------------|----------------|-----------|
| 0.0 - 0.3 | Local RTX-3060 | Simple designs, fast local processing |
| 0.3 - 0.6 | Hybrid (prefer local) | Medium complexity, cost-effective |
| 0.6 - 1.0 | Yotta Cloud | Complex designs, need cloud power |

## Cost Analysis

### Local RTX-3060 Costs
- **Hardware**: $400 one-time cost
- **Power**: ~220W @ $0.12/kWh = $0.026/hour
- **Token Cost**: $0.0001/token (amortized)
- **Latency**: 50-200ms
- **Availability**: 24/7 (when system running)

### Yotta Cloud Costs
- **Compute**: $0.50/hour for GPU instances
- **Token Cost**: $0.002/token
- **Latency**: 200-500ms (network overhead)
- **Availability**: 99.9% SLA
- **Scaling**: Auto-scale to demand

### Cost Optimization
```python
def calculate_cost_savings():
    local_cost_per_token = 0.0001
    cloud_cost_per_token = 0.002
    
    savings_per_token = cloud_cost_per_token - local_cost_per_token
    savings_percentage = (savings_per_token / cloud_cost_per_token) * 100
    
    return {
        "savings_per_token": savings_per_token,  # $0.0019
        "savings_percentage": savings_percentage,  # 95%
        "break_even_tokens": 400 / savings_per_token  # ~210,526 tokens
    }
```

## Configuration

### Environment Variables
```bash
# Compute Routing
ENABLE_LOCAL_GPU=true
LOCAL_GPU_TYPE=rtx3060
LOCAL_GPU_MEMORY=12GB
COMPLEXITY_THRESHOLD_LOCAL=0.3
COMPLEXITY_THRESHOLD_CLOUD=0.6

# Yotta Cloud
YOTTA_API_KEY=your-yotta-api-key
YOTTA_ENDPOINT=https://api.yotta.com/v1
YOTTA_MODEL=gpt-4-turbo
YOTTA_MAX_TOKENS=4096

# Fallback Strategy
FALLBACK_TO_CLOUD=true
LOCAL_TIMEOUT_SECONDS=30
CLOUD_TIMEOUT_SECONDS=60
```

### Routing Rules
```python
class ComputeRouter:
    def route_request(self, prompt, spec_data=None):
        complexity = self.calculate_complexity(prompt, spec_data)
        
        # Force cloud for specific keywords
        cloud_keywords = ["enterprise", "production", "large-scale"]
        if any(kw in prompt.lower() for kw in cloud_keywords):
            return "yotta_cloud"
        
        # Route based on complexity
        if complexity < 0.3:
            return "local_rtx3060"
        elif complexity < 0.6:
            return "local_rtx3060" if self.local_available() else "yotta_cloud"
        else:
            return "yotta_cloud"
    
    def local_available(self):
        # Check GPU availability, memory, temperature
        return self.gpu_monitor.is_healthy()
```

## Monitoring & Metrics

### Performance Tracking
```python
{
    "compute_stats": {
        "local_requests": 1250,
        "cloud_requests": 340,
        "local_avg_latency": 120,
        "cloud_avg_latency": 380,
        "local_success_rate": 0.98,
        "cloud_success_rate": 0.995
    },
    "cost_tracking": {
        "local_cost_today": 2.45,
        "cloud_cost_today": 15.80,
        "total_savings": 68.50,
        "savings_percentage": 87.2
    }
}
```

### Health Checks
- **GPU Temperature**: < 80°C
- **GPU Memory**: < 90% utilization
- **GPU Utilization**: Monitor for overload
- **Cloud API**: Response time < 1s
- **Network**: Latency to Yotta < 200ms

## Fallback Strategies

### Local GPU Failure
1. **Immediate**: Route to Yotta cloud
2. **Notification**: Alert admin of GPU issues
3. **Recovery**: Auto-retry local after cooldown
4. **Logging**: Track failure patterns

### Cloud API Failure
1. **Retry**: 3 attempts with exponential backoff
2. **Fallback**: Use local GPU regardless of complexity
3. **Degraded Mode**: Simplified processing
4. **User Notification**: Inform of potential delays

### Network Issues
1. **Local Priority**: Route everything to local GPU
2. **Queue Management**: Buffer requests during outage
3. **Batch Processing**: Process queued requests when online
4. **Status Page**: Update system status

## Optimization Recommendations

### Daily Operations
- Monitor GPU temperature and performance
- Track cost savings vs cloud-only approach
- Analyze complexity scoring accuracy
- Review routing decisions for optimization

### Weekly Reviews
- Analyze cost trends and savings
- Review complexity threshold effectiveness
- Check for routing pattern changes
- Update cloud vs local performance metrics

### Monthly Planning
- Evaluate hardware upgrade needs
- Review cloud provider pricing changes
- Optimize complexity scoring algorithm
- Plan capacity for growth