#!/bin/bash

echo "========================================="
echo "FILE VERIFICATION CHECKLIST"
echo "========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        return 0
    else
        echo -e "${RED}✗${NC} $1 - MISSING!"
        return 1
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
        return 0
    else
        echo -e "${RED}✗${NC} $1/ - MISSING!"
        return 1
    fi
}

MISSING=0

echo "=== ROOT FILES ==="
check_file "README.md" || ((MISSING++))
check_file ".env.example" || ((MISSING++))
check_file ".gitignore" || ((MISSING++))
check_file "docker-compose.yml" || ((MISSING++))
check_file "IMPLEMENTATION_SUMMARY.md" || ((MISSING++))
check_file "DELIVERABLES_CHECKLIST.md" || ((MISSING++))

echo ""
echo "=== DOCKER FILES ==="
check_file "docker/backend.Dockerfile" || ((MISSING++))
check_file "docker/frontend.Dockerfile" || ((MISSING++))

echo ""
echo "=== BACKEND FILES ==="
check_file "backend/requirements.txt" || ((MISSING++))
check_file "backend/alembic.ini" || ((MISSING++))
check_file "backend/app/__init__.py" || ((MISSING++))
check_file "backend/app/main.py" || ((MISSING++))

echo ""
echo "=== BACKEND CORE ==="
check_file "backend/app/core/__init__.py" || ((MISSING++))
check_file "backend/app/core/config.py" || ((MISSING++))
check_file "backend/app/core/security.py" || ((MISSING++))

echo ""
echo "=== BACKEND DATABASE ==="
check_file "backend/app/db/__init__.py" || ((MISSING++))
check_file "backend/app/db/database.py" || ((MISSING++))

echo ""
echo "=== BACKEND MODELS ==="
check_file "backend/app/models/__init__.py" || ((MISSING++))
check_file "backend/app/models/user.py" || ((MISSING++))
check_file "backend/app/models/project.py" || ((MISSING++))
check_file "backend/app/models/image.py" || ((MISSING++))
check_file "backend/app/models/annotation.py" || ((MISSING++))
check_file "backend/app/models/task.py" || ((MISSING++))
check_file "backend/app/models/model.py" || ((MISSING++))

echo ""
echo "=== BACKEND SCHEMAS ==="
check_file "backend/app/schemas/__init__.py" || ((MISSING++))
check_file "backend/app/schemas/user.py" || ((MISSING++))
check_file "backend/app/schemas/project.py" || ((MISSING++))
check_file "backend/app/schemas/image.py" || ((MISSING++))
check_file "backend/app/schemas/annotation.py" || ((MISSING++))
check_file "backend/app/schemas/task.py" || ((MISSING++))
check_file "backend/app/schemas/model.py" || ((MISSING++))

echo ""
echo "=== BACKEND API ==="
check_file "backend/app/api/__init__.py" || ((MISSING++))
check_file "backend/app/api/auth.py" || ((MISSING++))
check_file "backend/app/api/projects.py" || ((MISSING++))
check_file "backend/app/api/images.py" || ((MISSING++))
check_file "backend/app/api/annotations.py" || ((MISSING++))
check_file "backend/app/api/tasks.py" || ((MISSING++))
check_file "backend/app/api/models.py" || ((MISSING++))
check_file "backend/app/api/export.py" || ((MISSING++))

echo ""
echo "=== BACKEND SERVICES ==="
check_file "backend/app/services/__init__.py" || ((MISSING++))
check_file "backend/app/services/vision_service.py" || ((MISSING++))
check_file "backend/app/services/export_service.py" || ((MISSING++))
check_file "backend/app/services/training_service.py" || ((MISSING++))

echo ""
echo "=== BACKEND UTILS ==="
check_file "backend/app/utils/__init__.py" || ((MISSING++))
check_file "backend/app/utils/file_utils.py" || ((MISSING++))

echo ""
echo "=== ALEMBIC MIGRATIONS ==="
check_file "backend/alembic/env.py" || ((MISSING++))
check_file "backend/alembic/script.py.mako" || ((MISSING++))
check_file "backend/alembic/versions/001_initial_migration.py" || ((MISSING++))

echo ""
echo "=== FRONTEND FILES ==="
check_file "frontend/package.json" || ((MISSING++))
check_file "frontend/tsconfig.json" || ((MISSING++))
check_file "frontend/tsconfig.node.json" || ((MISSING++))
check_file "frontend/vite.config.ts" || ((MISSING++))
check_file "frontend/index.html" || ((MISSING++))
check_file "frontend/tailwind.config.js" || ((MISSING++))
check_file "frontend/postcss.config.js" || ((MISSING++))
check_file "frontend/.eslintrc.cjs" || ((MISSING++))

echo ""
echo "=== FRONTEND SOURCE ==="
check_file "frontend/src/main.tsx" || ((MISSING++))
check_file "frontend/src/App.tsx" || ((MISSING++))
check_file "frontend/src/index.css" || ((MISSING++))

echo ""
echo "=== FRONTEND TYPES ==="
check_file "frontend/src/types/index.ts" || ((MISSING++))

echo ""
echo "=== FRONTEND SERVICES ==="
check_file "frontend/src/services/api.ts" || ((MISSING++))

echo ""
echo "=== FRONTEND STORE ==="
check_file "frontend/src/store/authStore.ts" || ((MISSING++))
check_file "frontend/src/store/annotationStore.ts" || ((MISSING++))

echo ""
echo "=== FRONTEND HOOKS ==="
check_file "frontend/src/hooks/useKeyboardShortcuts.ts" || ((MISSING++))

echo ""
echo "=== FRONTEND UTILS ==="
check_file "frontend/src/utils/helpers.ts" || ((MISSING++))

echo ""
echo "=== FRONTEND COMPONENTS ==="
check_file "frontend/src/components/AnnotationCanvas.tsx" || ((MISSING++))
check_file "frontend/src/components/Button.tsx" || ((MISSING++))
check_file "frontend/src/components/Input.tsx" || ((MISSING++))
check_file "frontend/src/components/Modal.tsx" || ((MISSING++))
check_file "frontend/src/components/Loader.tsx" || ((MISSING++))
check_file "frontend/src/components/ImageUpload.tsx" || ((MISSING++))

echo ""
echo "=== FRONTEND PAGES ==="
check_file "frontend/src/pages/Login.tsx" || ((MISSING++))
check_file "frontend/src/pages/Register.tsx" || ((MISSING++))
check_file "frontend/src/pages/Dashboard.tsx" || ((MISSING++))
check_file "frontend/src/pages/Annotate.tsx" || ((MISSING++))

echo ""
echo "========================================="
echo "SUMMARY"
echo "========================================="

if [ $MISSING -eq 0 ]; then
    echo -e "${GREEN}✓ ALL FILES PRESENT!${NC}"
    echo "Total files checked: $(find . -type f -not -path "./.git/*" -not -path "*/__pycache__/*" | wc -l)"
    exit 0
else
    echo -e "${RED}✗ $MISSING FILES MISSING!${NC}"
    exit 1
fi
