#!/bin/bash

# Simple web test runner with pytest commands

# --- OLD IMPLEMENTATION ---
# The following lines run all test suites in parallel without any control over the
# number of concurrent jobs. This can lead to high memory consumption.
# I have commented this out in favor of a more controlled approach below.
#

#pytest tests/web/login --username="998771" --account=demo --alluredir=allure-login &
#pytest tests/web/settings --username="998772" --account=demo --alluredir=allure-settings &
#pytest tests/web/home --username="998773" --account=demo --alluredir=allure-home &
#pytest tests/web/signal --username="998774" --account=demo --alluredir=allure-signal &
#pytest tests/web/markets --username="998775" --account=demo --alluredir=allure-markets &
#pytest tests/web/trade/market --username="998776" --account=demo --alluredir=allure-market &
#pytest tests/web/trade/market_oct --username="998777" --account=demo --alluredir=allure-market_oct &
#pytest tests/web/trade/limit --username="998778" --account=demo --alluredir=allure-limit &
#pytest tests/web/trade/limit_oct --username="998779" --account=demo --alluredir=allure-limit_oct &
#pytest tests/web/trade/stop --username="998780" --account=demo --alluredir=allure-stop &
#pytest tests/web/trade/stop_oct --username="998846" --account=demo --alluredir=allure-stop_oct &
#pytest tests/web/trade/stop_limit --username="998847" --account=demo --alluredir=allure-stop_limit &
#pytest tests/web/trade/stop_limit_oct --username="998848" --account=demo --alluredir=allure-stop_limit_oct &
#pytest tests/web/trade/chart --username="998849" --account=demo --allured I will restore the original file content and then apply the correct changes.
#pytest tests/web/trade/control_button --username="998850" --account=demo --alluredir=allure-control_button &
#pytest tests/web/asset/limit --username="998851" --account=demo --alluredir=allure-asset-limit &
#pytest tests/web/asset/limit_oct --username="998852" --account=demo --alluredir=allure-asset-limit_oct &
#pytest tests/web/asset/market --username="998853" --account=demo --alluredir=allure-asset-market &
#pytest tests/web/asset/market_oct --username="998854" --account=demo --alluredir=allure-asset-market_oct &
#pytest tests/web/asset/others --username="998855" --account=demo --alluredir=allure-asset-others &
#pytest tests/web/asset/stop --username="998856" --account=demo --alluredir=allure-asset-stop &
#pytest tests/web/asset/stop_oct --username="998857" --account=demo --alluredir=allure-asset-stop_oct &
#pytest tests/web/asset/stop_limit --username="998858" --account=demo --alluredir=allure-asset-stop_limit &
#pytest tests/web/asset/stop_limit_oct --username="998859" --account=demo --alluredir=allure-asset-stop_limit_oct

#
#wait

# --- NEW IMPLEMENTATION ---
# Controls parallel execution to manage memory usage.

# --- Configuration ---
# Set the maximum number of parallel test suites to run at once.
# Adjust this number based on your machine's memory and CPU cores.
# A good starting point is half the number of your CPU cores. For example, if you have 8 cores, try 4.
MAX_PARALLEL_SUITES=4

# --- Test Suites ---
# Define all test suites to be run.
# Using a 'here document' to create a list of commands.
# To add or remove a test suite from the run, simply add or remove a line in this block.


#pytest tests/web/trade/limit --username="998778" --account=demo --alluredir=allure-limit
#pytest tests/web/trade/limit_oct --username="998779" --account=demo --alluredir=allure-limit_oct
#pytest tests/web/trade/stop --username="998780" --account=demo --alluredir=allure-stop
#pytest tests/web/trade/stop_oct --username="998846" --account=demo --alluredir=allure-stop_oct
#pytest tests/web/trade/stop_limit --username="998847" --account=demo --alluredir=allure-stop_limit
#pytest tests/web/trade/stop_limit_oct --username="998848" --account=demo --alluredir=allure-stop_limit_oct
#pytest tests/web/trade/chart --username="998849" --account=demo --alluredir=allure-chart
#pytest tests/web/trade/control_button --username="998850" --account=demo --alluredir=allure-control_button
#pytest tests/web/asset/limit --username="998851" --account=demo --alluredir=allure-asset-limit
#pytest tests/web/asset/limit_oct --username="998852" --account=demo --alluredir=allure-asset-limit_oct
#pytest tests/web/asset/market --username="998853" --account=demo --alluredir=allure-asset-market
#pytest tests/web/asset/market_oct --username="998854" --account=demo --alluredir=allure-asset-market_oct
#pytest tests/web/asset/others --username="998855" --account=demo --alluredir=allure-asset-others
#pytest tests/web/asset/stop --username="998856" --account=demo --alluredir=allure-asset-stop
#pytest tests/web/asset/stop_oct --username="998857" --account=demo --alluredir=allure-asset-stop_oct
#pytest tests/web/asset/stop_limit --username="998858" --account=demo --alluredir=allure-asset-stop_limit
#pytest tests/web/asset/stop_limit_oct --username="998859" --account=demo --alluredir=allure-asset-stop_limit_oct



#pytest tests/web/asset/limit --user="2092009113" --account=demo --alluredir=allure-asset-limit
#pytest tests/web/asset/limit_oct --user="2092009114" --account=demo --alluredir=allure-asset-limit_oct

read -r -d '' TEST_COMMANDS <<'EOF'
pytest tests/web/markets --client=lirunex -m critical --user="2092009111" --account=demo --alluredir=allure-market
pytest tests/web/home --client=lirunex -m critical --user="2092009112" --account=demo --alluredir=allure-home
EOF

# --- Execution ---
# The script will now run up to MAX_PARALLEL_SUITES jobs at a time.
# It filters out any commented-out lines before running.
echo "$TEST_COMMANDS" | grep -v '^[[:space:]]*#' | xargs -P "$MAX_PARALLEL_SUITES" -I CMD bash -c 'CMD'

echo "All test suites have completed." 