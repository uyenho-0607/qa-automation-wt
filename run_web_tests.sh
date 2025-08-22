#!/bin/bash

# Simple web test runner with pytest commands

MAX_PARALLEL_SUITES=4

# --- Test Suites ---
# Define all test suites to be run.
# Using a 'here document' to create a list of commands.
# To add or remove a test suite from the run, simply add or remove a line in this block.

read -r -d '' TEST_COMMANDS <<'EOF'
pytest tests/web/chart -m critical --user="569200615" --account=live --password="Master@12345" --client=lirunex --server=mt5 --alluredir=allure-lirunex-mt5-1
pytest tests/web/chart -m critical --user="400000010" --account=live --password="Asd123" --client=lirunex --server=mt4 --alluredir=allure-lirunex-mt4-1
pytest tests/web/chart -m critical --user="998545" --account=live --password='Master@12345' --client=transactCloud --alluredir=allure-transactCloud-1
EOF

# --- Execution ---
# The script will now run up to MAX_PARALLEL_SUITES jobs at a time.
# It filters out any commented-out lines before running.
echo "$TEST_COMMANDS" | grep -v '^[[:space:]]*#' | xargs -P "$MAX_PARALLEL_SUITES" -I CMD bash -c 'CMD'

echo "All test suites have completed."