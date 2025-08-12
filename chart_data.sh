#!/bin/bash

# === CONFIGURATION ===
RESULTS_DIR="allure-results"
REPORT_DIR="allure-report"
LOCAL_HOST="192.168.0.100"
LOCAL_PORT="8080"

# Check if deployment option is provided
DEPLOY_OPTION=${1:-"local"}  # Default to local if no argument provided

echo "=============================="
echo "🧪 Running Chart Data Tests..."
echo "=============================="

pytest tests/ --alluredir="$RESULTS_DIR"
TEST_EXIT_CODE=$?

echo ""
echo "=============================="
echo "📊 Generating Allure Report..."
echo "=============================="

allure generate "$RESULTS_DIR" --clean -o "$REPORT_DIR"
if [ $? -ne 0 ]; then
  echo "❌ Allure report generation failed."
  exit 1
fi

echo ""
echo "=============================="

if [ "$DEPLOY_OPTION" = "serve" ]; then
  echo "🌐 Starting Local Allure Server..."
  echo "=============================="
  echo "📍 Report will be available at: http://$LOCAL_HOST:$LOCAL_PORT"
  echo "🔄 Server will start automatically..."
  echo "⏹️  Press Ctrl+C to stop the server"
  echo ""
  
  allure serve "$RESULTS_DIR" -h "$LOCAL_HOST" -p "$LOCAL_PORT"

else
  echo "📁 Report Generated Successfully!"
  echo "=============================="
  echo ""
  echo "🌐 Starting local server and opening report..."
  echo "📍 Report will be available at: http://localhost:4040"
  echo "🔄 Server will start automatically and open in browser"
  echo "⏹️  Press Ctrl+C to stop the server when done"
  echo ""
  
  # Start allure serve which creates a local server and auto-opens browser
  allure serve "$RESULTS_DIR"
fi 