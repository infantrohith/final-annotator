#!/bin/bash

# Final Annotator - Setup Test Script
# This script verifies that all components are properly configured

set -e

echo "========================================="
echo "Final Annotator - Setup Verification"
echo "========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to print test result
test_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: $2"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}: $2"
        ((TESTS_FAILED++))
    fi
}

# Check if .env exists
echo "Checking configuration files..."
if [ -f ".env" ]; then
    test_result 0 ".env file exists"
else
    echo -e "${YELLOW}⚠ WARNING${NC}: .env file not found. Creating from .env.example..."
    cp .env.example .env
    test_result 0 "Created .env from template"
fi

# Check Docker files
echo ""
echo "Checking Docker configuration..."
[ -f "docker-compose.yml" ] && test_result 0 "docker-compose.yml exists" || test_result 1 "docker-compose.yml missing"
[ -f "docker/backend.Dockerfile" ] && test_result 0 "Backend Dockerfile exists" || test_result 1 "Backend Dockerfile missing"
[ -f "docker/frontend.Dockerfile" ] && test_result 0 "Frontend Dockerfile exists" || test_result 1 "Frontend Dockerfile missing"

# Check backend structure
echo ""
echo "Checking backend structure..."
[ -f "backend/requirements.txt" ] && test_result 0 "Backend requirements.txt exists" || test_result 1 "Backend requirements.txt missing"
[ -f "backend/app/main.py" ] && test_result 0 "Backend main.py exists" || test_result 1 "Backend main.py missing"
[ -f "backend/alembic.ini" ] && test_result 0 "Alembic config exists" || test_result 1 "Alembic config missing"
[ -d "backend/alembic/versions" ] && test_result 0 "Migration directory exists" || test_result 1 "Migration directory missing"

# Count backend files
API_FILES=$(find backend/app/api -name "*.py" 2>/dev/null | wc -l)
MODEL_FILES=$(find backend/app/models -name "*.py" 2>/dev/null | wc -l)
SCHEMA_FILES=$(find backend/app/schemas -name "*.py" 2>/dev/null | wc -l)

echo ""
echo "Backend components:"
echo "  - API endpoints: $API_FILES files"
echo "  - Models: $MODEL_FILES files"
echo "  - Schemas: $SCHEMA_FILES files"

# Check frontend structure
echo ""
echo "Checking frontend structure..."
[ -f "frontend/package.json" ] && test_result 0 "Frontend package.json exists" || test_result 1 "Frontend package.json missing"
[ -f "frontend/vite.config.ts" ] && test_result 0 "Vite config exists" || test_result 1 "Vite config missing"
[ -f "frontend/tsconfig.json" ] && test_result 0 "TypeScript config exists" || test_result 1 "TypeScript config missing"
[ -f "frontend/src/main.tsx" ] && test_result 0 "Frontend entry point exists" || test_result 1 "Frontend entry point missing"

# Count frontend files
COMPONENT_FILES=$(find frontend/src/components -name "*.tsx" 2>/dev/null | wc -l)
PAGE_FILES=$(find frontend/src/pages -name "*.tsx" 2>/dev/null | wc -l)

echo ""
echo "Frontend components:"
echo "  - Components: $COMPONENT_FILES files"
echo "  - Pages: $PAGE_FILES files"

# Check Python syntax
echo ""
echo "Checking Python syntax..."
if command -v python3 &> /dev/null; then
    if python3 -m py_compile backend/app/main.py 2>/dev/null; then
        test_result 0 "Backend main.py syntax valid"
    else
        test_result 1 "Backend main.py syntax error"
    fi
else
    echo -e "${YELLOW}⚠ SKIP${NC}: Python3 not available for syntax check"
fi

# Summary
echo ""
echo "========================================="
echo "Test Summary"
echo "========================================="
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Review and update .env with your configuration"
    echo "2. Run: docker-compose build"
    echo "3. Run: docker-compose up -d"
    echo "4. Access the application at http://localhost:3000"
    exit 0
else
    echo -e "${RED}✗ Some checks failed. Please review the errors above.${NC}"
    exit 1
fi
