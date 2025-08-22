#!/bin/bash

# Number of times to run the entire test suite
PLATFORM=${1:-"android"}
TOTAL_RUNS=${2:-10}

# Function to run a single iteration of tests
run_test_iteration() {
    local iteration=$1
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local base_dir="iteration_${iteration}_${timestamp}"
    
    # Create directories for this iteration
    local allure_lirunex_mt5="allure-lirunex-mt5-${iteration}"
    local allure_lirunex_mt4="allure-lirunex-mt4-${iteration}"
    local allure_transactCloud="allure-transactCloud-${iteration}"
    
    echo "Starting test iteration $iteration at $(date)"
    
    # Run tests sequentially
    echo "Running MT4 tests..."
    pytest tests/$PLATFORM/chart -m critical --user="400000010" --account=live --password="Asd123" --client=lirunex --server=mt4 --alluredir="$allure_lirunex_mt4"
    echo "Completed MT4 tests for iteration $iteration"
    
    echo "Running MT5 tests..."
    pytest tests/$PLATFORM/chart -m critical --user="569200615" --account=live --password="Master@12345" --client=lirunex --server=mt5 --alluredir="$allure_lirunex_mt5"
    echo "Completed MT5 tests for iteration $iteration"
    
    echo "Running TransactCloud tests..."
    pytest tests/$PLATFORM/chart -m critical --user="998545" --account=live --password='Master@12345' --client=transactCloud --alluredir="$allure_transactCloud"
    echo "Completed TransactCloud tests for iteration $iteration"
    
    echo "All tests completed for iteration $iteration"
    
    # Create merge directory for this iteration
    local merge_dir="merged-results-${iteration}"
    local report_dir="reports/$PLATFORM/report${iteration}"
    
    # Cleanup and create merge directory
    rm -rf "$merge_dir"
    mkdir -p "$merge_dir"
    
    # Merge results for this iteration
    for dir in "$allure_lirunex_mt4" "$allure_lirunex_mt5" "$allure_transactCloud"; do
        if [ -d "$dir" ]; then
            echo "Merging: $dir"
            cp -r "$dir"/* "$merge_dir"/
        fi
    done
    
    # Generate Allure report for this iteration
    echo "Generating report for iteration $iteration"
    mkdir -p "$report_dir"
    allure generate "$merge_dir" -o "$report_dir" --clean
    
    # Cleanup intermediate results
    rm -rf "$merge_dir" "$allure_lirunex_mt5" "$allure_lirunex_mt4" "$allure_transactCloud"
    
    echo "Completed iteration $iteration at $(date)"
    echo "Report generated in: $report_dir"
    echo "----------------------------------------"
}

# Main execution
echo "Starting test automation suite with $TOTAL_RUNS iterations"
echo "Platform: $PLATFORM"
echo "Started at: $(date)"
echo "----------------------------------------"

for ((i=1; i<=$TOTAL_RUNS; i++)); do
    run_test_iteration $i
done

echo "All iterations completed at: $(date)"
echo "Reports are available in the reports/$PLATFORM/ directory"

# Optionally open the latest report
latest_report="reports/$PLATFORM/report${TOTAL_RUNS}"
if [ -d "$latest_report" ]; then
    echo "Opening the latest report (iteration $TOTAL_RUNS)"
    allure open "$latest_report"
fi
