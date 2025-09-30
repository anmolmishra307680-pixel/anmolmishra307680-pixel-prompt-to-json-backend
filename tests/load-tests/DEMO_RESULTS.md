# k6 Load Test Demo Results

## Test Configuration
- **Alternative**: Python-based load test (k6 requires installation)
- **Target**: http://localhost:8000
- **Endpoints Tested**: /health, /basic-metrics, /

## Load Test Results

### Light Load (Development)
- **Virtual Users**: 10
- **Duration**: 30 seconds
- **Results**:
  - Total Requests: 100
  - Success Rate: 100.0%
  - Requests/sec: 3.3
  - Avg Response: 2032.7ms
  - 95th Percentile: 2060.4ms

### Medium Load (Staging)
- **Virtual Users**: 25
- **Duration**: 20 seconds
- **Results**:
  - Total Requests: 175
  - Success Rate: 100.0%
  - Requests/sec: 8.8
  - Avg Response: 2043.0ms
  - 95th Percentile: 2060.4ms

## k6 Commands (Once Installed)

### Light Load
```bash
k6 run --env VUS=10 --env DURATION=1m load-tests/k6/generate_load_test.js
```

### Medium Load
```bash
k6 run --env VUS=50 --env DURATION=3m load-tests/k6/generate_load_test.js
```

### Heavy Load
```bash
k6 run --env VUS=200 --env DURATION=10m load-tests/k6/generate_load_test.js
```

### Authentication Flow
```bash
k6 run load-tests/k6/auth_load_test.js
```

## Installation Instructions

### Windows
1. Download from: https://github.com/grafana/k6/releases
2. Extract `k6-v0.47.0-windows-amd64.zip` to `C:\k6\`
3. Add `C:\k6\` to PATH environment variable
4. Restart PowerShell and run `k6 version`

### Alternative (Chocolatey - Requires Admin)
```powershell
# Run as Administrator
Set-ExecutionPolicy Bypass -Scope Process -Force
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
choco install k6
```

## Expected k6 Results

### Light Load (10 VUs, 1m)
- ~600 requests total
- ~10 RPS
- <100ms response time
- 0% error rate

### Medium Load (50 VUs, 3m)
- ~9000 requests total
- ~50 RPS
- <200ms response time
- 0% error rate

### Heavy Load (200 VUs, 10m)
- ~120000 requests total
- ~200 RPS
- <500ms response time
- <1% error rate

## Files Available
- ✅ `generate_load_test.js` - Multi-endpoint testing
- ✅ `auth_load_test.js` - Authentication flow
- ✅ `run_load_tests.bat` - Windows runner
- ✅ `run_load_tests.sh` - Linux/macOS runner
- ✅ `k6-alternative-demo.py` - Python alternative
- ✅ Sample results and documentation