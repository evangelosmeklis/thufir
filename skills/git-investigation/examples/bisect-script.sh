#!/bin/bash

# Git Bisect Automated Test Script Example
#
# This script automates git bisect by testing each commit checkout.
# It should exit 0 for "good" (test passes) and non-zero for "bad" (test fails).
#
# Usage:
#   git bisect start HEAD <known-good-commit>
#   git bisect run ./bisect-script.sh

set -e  # Exit on error

echo "Testing commit: $(git rev-parse --short HEAD)"

# Example 1: Test if specific error occurs
# --------------------------------------
# This tests if running the code produces a specific error

# Uncomment and adapt for your use case:
# npm install --silent > /dev/null 2>&1
# output=$(npm test 2>&1 || true)
# if echo "$output" | grep -q "ConnectionPoolExhausted"; then
#   echo "Error found - marking as BAD"
#   exit 1  # Bad commit
# else
#   echo "No error - marking as GOOD"
#   exit 0  # Good commit
# fi

# Example 2: Run unit tests
# -------------------------
# This runs test suite and fails if tests don't pass

# Uncomment and adapt:
# npm install --silent > /dev/null 2>&1
# if npm test > /dev/null 2>&1; then
#   echo "Tests pass - marking as GOOD"
#   exit 0  # Good commit
# else
#   echo "Tests fail - marking as BAD"
#   exit 1  # Bad commit
# fi

# Example 3: Check for specific code pattern
# ------------------------------------------
# This checks if problematic code exists in specific file

# Uncomment and adapt:
# if grep -q "max: 10" src/config/database.js; then
#   echo "Problematic config found - marking as BAD"
#   exit 1  # Bad commit
# else
#   echo "Config looks good - marking as GOOD"
#   exit 0  # Good commit
# fi

# Example 4: Test API endpoint
# ----------------------------
# This starts app and tests if endpoint works

# Uncomment and adapt:
# npm install --silent > /dev/null 2>&1
# npm start > /dev/null 2>&1 &
# server_pid=$!
# sleep 5  # Wait for server to start
#
# # Test endpoint
# response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/health || echo "000")
#
# kill $server_pid > /dev/null 2>&1
#
# if [ "$response" = "200" ]; then
#   echo "Endpoint works - marking as GOOD"
#   exit 0
# else
#   echo "Endpoint broken - marking as BAD"
#   exit 1
# fi

# Example 5: Check configuration value
# ------------------------------------
# This verifies configuration has correct value

# Uncomment and adapt:
# config_value=$(grep "max:" src/config/database.js | grep -oE "[0-9]+" | head -1)
# if [ "$config_value" -ge "100" ]; then
#   echo "Config value OK ($config_value) - marking as GOOD"
#   exit 0
# else
#   echo "Config value too low ($config_value) - marking as BAD"
#   exit 1
# fi

# Example 6: Performance test
# ---------------------------
# This checks if performance is acceptable

# Uncomment and adapt:
# npm install --silent > /dev/null 2>&1
# npm start > /dev/null 2>&1 &
# server_pid=$!
# sleep 5
#
# # Measure response time
# response_time=$(curl -s -o /dev/null -w "%{time_total}" http://localhost:3000/api/endpoint)
#
# kill $server_pid > /dev/null 2>&1
#
# # Check if response time is under 1 second
# if awk "BEGIN {exit !($response_time < 1.0)}"; then
#   echo "Performance OK (${response_time}s) - marking as GOOD"
#   exit 0
# else
#   echo "Performance poor (${response_time}s) - marking as BAD"
#   exit 1
# fi

# Example 7: Complex multi-step test
# ----------------------------------
# This combines multiple checks

# Uncomment and adapt:
# echo "Step 1: Install dependencies..."
# npm install --silent > /dev/null 2>&1 || exit 125  # Exit 125 = skip this commit
#
# echo "Step 2: Check for compilation errors..."
# npm run build > /dev/null 2>&1 || {
#   echo "Build fails - marking as BAD"
#   exit 1
# }
#
# echo "Step 3: Run unit tests..."
# npm test > /dev/null 2>&1 || {
#   echo "Tests fail - marking as BAD"
#   exit 1
# }
#
# echo "Step 4: Check for specific bug..."
# output=$(npm start 2>&1 &)
# sleep 5
# if curl -s http://localhost:3000/api/test | grep -q "error"; then
#   echo "Bug present - marking as BAD"
#   killall node > /dev/null 2>&1
#   exit 1
# fi
#
# echo "All checks pass - marking as GOOD"
# killall node > /dev/null 2>&1
# exit 0

# Default behavior if no test is uncommented
# ------------------------------------------
echo "ERROR: Please uncomment and adapt one of the example tests above"
echo "Exiting with 125 to skip this commit"
exit 125  # 125 = ask git to skip this commit
