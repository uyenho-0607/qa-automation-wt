#!/bin/bash

# === CONFIGURATION ===
RESULTS_DIR="allure-results"
REPORT_DIR="allure-report"
DEPLOY_URL="https://automation-wt.netlify.app"

echo "=============================="
echo "🧪 Running Pytest Tests..."
echo "=============================="

pytest tests/metatrader --alluredir="$RESULTS_DIR"

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
echo "🚀 Deploying to Netlify..."
echo "=============================="

# Assume site is already linked with `netlify link`
netlify deploy --dir="$REPORT_DIR" --prod
if [ $? -ne 0 ]; then
  echo "❌ Netlify deployment failed."
  exit 1
fi

echo ""
echo "✅ Deployment successful!"
echo "🌐 Report URL: $DEPLOY_URL"
