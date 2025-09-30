# Load Testing with k6

This directory contains k6 load testing scripts for the Prompt-to-JSON Backend API.

## Prerequisites

Install k6:
```bash
# Windows (using Chocolatey)
choco install k6

# macOS (using Homebrew)
brew install k6

# Linux
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6
```

## Test Scripts

### 1. Basic Load Test (`generate_load_test.js`)
Tests multiple endpoints with configurable load:
- `/generate` (with authentication)
- `/health` 
- `/basic-metrics`

### 2. Authentication Load Test (`auth_load_test.js`)
Tests the complete authentication flow:
- Get JWT token from `/token`
- Use token for authenticated `/generate` requests

## Running Tests

### Quick Start
```bash
# Basic test with default settings (50 VUs, 3 minutes)
k6 run load-tests/k6/generate_load_test.js

# Custom configuration
k6 run --env VUS=100 --env DURATION=5m --env TARGET_URL=http://localhost:8000 load-tests/k6/generate_load_test.js
```

### Using Runner Scripts

#### Windows
```cmd
# Basic test
load-tests\run_load_tests.bat basic

# Authentication test  
load-tests\run_load_tests.bat auth

# All tests
load-tests\run_load_tests.bat all

# Custom parameters
load-tests\run_load_tests.bat basic http://localhost:8000 100 5m
```

#### Linux/macOS
```bash
# Make script executable
chmod +x load-tests/run_load_tests.sh

# Basic test
./load-tests/run_load_tests.sh basic

# Authentication test
./load-tests/run_load_tests.sh auth

# All tests
./load-tests/run_load_tests.sh all

# Custom parameters
./load-tests/run_load_tests.sh basic http://localhost:8000 100 5m
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VUS` | 50 | Number of virtual users |
| `DURATION` | 3m | Test duration |
| `TARGET_URL` | http://localhost:8000 | API base URL |
| `API_KEY` | bhiv-secret-key-2024 | API key for authentication |
| `JWT_TOKEN` | (empty) | JWT token for protected endpoints |

## Test Scenarios

### Light Load (Development)
```bash
k6 run --env VUS=10 --env DURATION=1m load-tests/k6/generate_load_test.js
```

### Medium Load (Staging)
```bash
k6 run --env VUS=50 --env DURATION=3m load-tests/k6/generate_load_test.js
```

### Heavy Load (Production Validation)
```bash
k6 run --env VUS=200 --env DURATION=10m load-tests/k6/generate_load_test.js
```

## Results Analysis

Results are saved to `load-tests/results/TIMESTAMP/`:
- `*_results.json`: Detailed metrics in JSON format
- `*_summary.txt`: Human-readable summary
- `load_test_summary.md`: Combined report

### Key Metrics to Monitor
- **http_req_duration**: Response time percentiles
- **http_req_failed**: Error rate
- **http_reqs**: Total requests and RPS
- **checks**: Success rate of assertions

### Performance Thresholds
- 95% of requests < 2000ms
- Error rate < 10%
- All health checks pass

## Production Testing

### Against Live API
```bash
k6 run --env TARGET_URL=https://prompt-to-json-backend.onrender.com --env VUS=25 --env DURATION=2m load-tests/k6/generate_load_test.js
```

### With Authentication
```bash
# First get a JWT token manually, then:
k6 run --env JWT_TOKEN=your_jwt_token --env VUS=10 load-tests/k6/auth_load_test.js
```

## Sample Results

See `results_summary.txt` for example output showing:
- 2,980 requests over 3 minutes
- 16.55 requests/second
- 145.6ms average response time
- 0% error rate
- 100% check success rate