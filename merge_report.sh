#!/bin/bash

# Set directories
MERGE_DIR="merged-results"
REPORT_DIR="merged-report"

# Cleanup old results
rm -rf "$MERGE_DIR" "$REPORT_DIR"
mkdir -p "$MERGE_DIR"

# Find and merge all 'allure-*' folders
for dir in allure-*; do
  if [ -d "$dir" ]; then
    echo "Merging: $dir"
    cp -r "$dir"/* "$MERGE_DIR"/
  fi
done

# Generate Allure report
allure generate "$MERGE_DIR" -o "$REPORT_DIR" --clean
allure open "$REPORT_DIR"
