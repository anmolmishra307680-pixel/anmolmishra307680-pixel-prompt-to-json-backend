#!/bin/bash

# Load Testing Script for Prompt-to-JSON Backend
# Usage: ./run_load_tests.sh [test_type] [target_url] [vus] [duration]

set -e

# Default values
TEST_TYPE=${1:-"basic"}
TARGET_URL=${2:-"http://localhost:8000"}
VUS=${3:-"50"}
DURATION=${4:-"3m"}
API_KEY=${API_KEY:-"bhiv-secret-key-2024"}

# Create results directory
mkdir -p load-tests/results

# Get timestamp for results
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RESULTS_DIR="load-tests/results/${TIMESTAMP}"
mkdir -p "$RESULTS_DIR"

echo "🚀 Starting Load Tests"
echo "Target URL: $TARGET_URL"
echo "Virtual Users: $VUS"
echo "Duration: $DURATION"
echo "Results will be saved to: $RESULTS_DIR"
echo "----------------------------------------"

# Function to run k6 test
run_k6_test() {
    local test_file=$1
    local test_name=$2
    local output_file="$RESULTS_DIR/${test_name}_results.json"
    local summary_file="$RESULTS_DIR/${test_name}_summary.txt"
    
    echo "Running $test_name test..."
    
    k6 run \
        --env TARGET_URL="$TARGET_URL" \
        --env VUS="$VUS" \
        --env DURATION="$DURATION" \
        --env API_KEY="$API_KEY" \
        --out json="$output_file" \
        "$test_file" | tee "$summary_file"
    
    echo "✅ $test_name test completed"
    echo "Results saved to: $output_file"
    echo "Summary saved to: $summary_file"
    echo "----------------------------------------"
}

# Run tests based on type
case $TEST_TYPE in
    "basic")
        run_k6_test "load-tests/k6/generate_load_test.js" "basic_load"
        ;;
    "auth")
        run_k6_test "load-tests/k6/auth_load_test.js" "auth_load"
        ;;
    "all")
        run_k6_test "load-tests/k6/generate_load_test.js" "basic_load"
        sleep 10
        run_k6_test "load-tests/k6/auth_load_test.js" "auth_load"
        ;;
    *)
        echo "❌ Unknown test type: $TEST_TYPE"
        echo "Available types: basic, auth, all"
        exit 1
        ;;
esac

# Generate summary report
SUMMARY_REPORT="$RESULTS_DIR/load_test_summary.md"
cat > "$SUMMARY_REPORT" << EOF
# Load Test Results - $(date)

## Test Configuration
- **Target URL**: $TARGET_URL
- **Virtual Users**: $VUS
- **Duration**: $DURATION
- **Test Type**: $TEST_TYPE
- **API Key**: ${API_KEY:0:10}...

## Results Location
- **Results Directory**: $RESULTS_DIR
- **JSON Results**: Available for each test
- **Text Summaries**: Available for each test

## Quick Analysis
Run the following to analyze results:
\`\`\`bash
# View summary
cat $RESULTS_DIR/*_summary.txt

# Analyze JSON results (requires jq)
jq '.metrics.http_req_duration' $RESULTS_DIR/*_results.json
\`\`\`

EOF

echo "📊 Load test completed!"
echo "Summary report: $SUMMARY_REPORT"
echo "All results saved to: $RESULTS_DIR"