# Install k6 on Windows

## Option 1: Download Binary (Recommended)
1. Go to https://github.com/grafana/k6/releases
2. Download `k6-v0.47.0-windows-amd64.zip`
3. Extract to `C:\k6\`
4. Add `C:\k6\` to your PATH environment variable
5. Restart PowerShell and run `k6 version`

## Option 2: Install Chocolatey First
```powershell
# Install Chocolatey (run as Administrator)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Then install k6
choco install k6
```

## Option 3: Use Existing Python Load Test
```bash
# Use our Python-based load test instead
python load_test.py --comprehensive
```

## Quick Test Without k6
```powershell
# Test API health endpoint
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET

# Simple load test with PowerShell
1..100 | ForEach-Object -Parallel { 
    Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET 
} -ThrottleLimit 10
```