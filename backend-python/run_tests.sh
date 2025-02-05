#!/bin/bash

# Set environment variables for testing
export PYTHONPATH=.
export TESTING=1

# Run current functionality tests only
echo "Running current functionality tests..."
pytest app/tests/test_trial_analysis.py \
      app/tests/test_trial_analytics_service.py \
      app/tests/test_company_routes.py \
      app/tests/test_trial_routes.py \
      app/tests/test_integration.py \
      -v --cov=app --cov-report=term-missing

# Run all tests including future concepts (if specified)
if [ "$1" == "--include-future" ]; then
    echo "Running all tests including future concepts..."
    INCLUDE_FUTURE_TESTS=1 pytest app/tests/ -v --cov=app --cov-report=term-missing
fi 