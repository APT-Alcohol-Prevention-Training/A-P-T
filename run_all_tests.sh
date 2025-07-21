#!/bin/bash

# APT Chat Bot Complete Test Suite
# This script runs both backend and frontend tests

echo "🚀 APT Chat Bot Complete Test Suite"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Backend Tests
echo -e "${YELLOW}🔧 Running Backend Tests...${NC}"
echo "======================================"
cd backend

if command -v uv &> /dev/null; then
    echo "Using uv to run Python tests..."
    uv run python run_all_tests.py
    BACKEND_RESULT=$?
else
    echo "Using python3 to run tests..."
    python3 run_all_tests.py
    BACKEND_RESULT=$?
fi

cd ..
echo ""

# Frontend Tests
echo -e "${YELLOW}⚛️  Running Frontend Tests...${NC}"
echo "======================================"
cd frontend

if [ -f "run_frontend_tests.py" ]; then
    python3 run_frontend_tests.py
    FRONTEND_RESULT=$?
else
    echo "Frontend test runner not found. Please ensure run_frontend_tests.py exists."
    FRONTEND_RESULT=1
fi

cd ..
echo ""

# Summary
echo "======================================"
echo "📊 TEST SUMMARY"
echo "======================================"

if [ $BACKEND_RESULT -eq 0 ]; then
    echo -e "${GREEN}✅ Backend Tests: PASSED${NC}"
else
    echo -e "${RED}❌ Backend Tests: FAILED${NC}"
fi

if [ $FRONTEND_RESULT -eq 0 ]; then
    echo -e "${GREEN}✅ Frontend Tests: PASSED${NC}"
else
    echo -e "${RED}❌ Frontend Tests: FAILED${NC}"
fi

echo ""

if [ $BACKEND_RESULT -eq 0 ] && [ $FRONTEND_RESULT -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed! The application is ready for deployment.${NC}"
    exit 0
else
    echo -e "${RED}⚠️  Some tests failed. Please check the detailed reports above.${NC}"
    exit 1
fi