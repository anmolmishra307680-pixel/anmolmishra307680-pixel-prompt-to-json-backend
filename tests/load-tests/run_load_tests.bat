@echo off
REM Load Testing Script for Windows
REM Usage: run_load_tests.bat [test_type] [target_url] [vus] [duration]

setlocal enabledelayedexpansion

REM Default values
set TEST_TYPE=%1
if "%TEST_TYPE%"=="" set TEST_TYPE=basic

set TARGET_URL=%2
if "%TARGET_URL%"=="" set TARGET_URL=http://localhost:8000

set VUS=%3
if "%VUS%"=="" set VUS=50

set DURATION=%4
if "%DURATION%"=="" set DURATION=3m

if "%API_KEY%"=="" set API_KEY=bhiv-secret-key-2024

REM Create results directory
if not exist "load-tests\results" mkdir "load-tests\results"

REM Get timestamp for results
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "TIMESTAMP=%dt:~0,8%_%dt:~8,6%"
set "RESULTS_DIR=load-tests\results\%TIMESTAMP%"
mkdir "%RESULTS_DIR%"

echo 🚀 Starting Load Tests
echo Target URL: %TARGET_URL%
echo Virtual Users: %VUS%
echo Duration: %DURATION%
echo Results will be saved to: %RESULTS_DIR%
echo ----------------------------------------

REM Function to run k6 test
if "%TEST_TYPE%"=="basic" (
    echo Running basic load test...
    k6 run --env TARGET_URL=%TARGET_URL% --env VUS=%VUS% --env DURATION=%DURATION% --env API_KEY=%API_KEY% --out json=%RESULTS_DIR%\basic_results.json load-tests\k6\generate_load_test.js > %RESULTS_DIR%\basic_summary.txt
    echo ✅ Basic test completed
)

if "%TEST_TYPE%"=="auth" (
    echo Running auth load test...
    k6 run --env TARGET_URL=%TARGET_URL% --env VUS=%VUS% --env DURATION=%DURATION% --env API_KEY=%API_KEY% --out json=%RESULTS_DIR%\auth_results.json load-tests\k6\auth_load_test.js > %RESULTS_DIR%\auth_summary.txt
    echo ✅ Auth test completed
)

if "%TEST_TYPE%"=="all" (
    echo Running basic load test...
    k6 run --env TARGET_URL=%TARGET_URL% --env VUS=%VUS% --env DURATION=%DURATION% --env API_KEY=%API_KEY% --out json=%RESULTS_DIR%\basic_results.json load-tests\k6\generate_load_test.js > %RESULTS_DIR%\basic_summary.txt
    echo ✅ Basic test completed
    
    timeout /t 10 /nobreak > nul
    
    echo Running auth load test...
    k6 run --env TARGET_URL=%TARGET_URL% --env VUS=%VUS% --env DURATION=%DURATION% --env API_KEY=%API_KEY% --out json=%RESULTS_DIR%\auth_results.json load-tests\k6\auth_load_test.js > %RESULTS_DIR%\auth_summary.txt
    echo ✅ Auth test completed
)

echo 📊 Load test completed!
echo Results saved to: %RESULTS_DIR%
pause