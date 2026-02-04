#!/bin/bash
# Clean slate: Remove genetic algorithm, simplify docs, reset tests

set -e

echo "🧹 Starting clean slate cleanup..."
echo ""

# 1. Delete all extra markdown files
echo "📄 Cleaning up documentation..."
rm -f CHANGELOG.md
rm -f CLEANUP_SUMMARY.md
rm -f COMMANDS.md
rm -f README_NEW.md
rm -f QUICKSTART_NEW.md
rm -f BUGFIXES_SUMMARY.md
rm -f CONFIG_IMPROVEMENTS.md
rm -f UNIFIED_CONFIG_EXPERIENCE.md
rm -f CONTEXT.md
rm -f README_old_backup.md
rm -f QUICKSTART_old_backup.md
rm -f cleanup.sh
rm -f cleanup_docs.sh 2>/dev/null || true
echo "  ✅ Removed extra markdown files"

# 2. Replace PROJECT_PLAN with simplified version
if [ -f PROJECT_PLAN_NEW.md ]; then
    rm -f PROJECT_PLAN_old.md 2>/dev/null || true
    mv PROJECT_PLAN_NEW.md PROJECT_PLAN.md
    echo "  ✅ Updated PROJECT_PLAN.md"
fi

# 3. Remove old tests and coverage
echo ""
echo "🧪 Resetting test directory..."
rm -rf tests/
rm -rf htmlcov/
rm -f .coverage
rm -f conftest.py 2>/dev/null || true
echo "  ✅ Removed old tests and coverage reports"

# 4. Simplify pytest.ini
if [ -f pytest_new.ini ]; then
    mv pytest.ini pytest_old.ini 2>/dev/null || true
    mv pytest_new.ini pytest.ini
    echo "  ✅ Simplified pytest.ini"
fi

# 5. Create fresh test structure
echo "  📁 Creating fresh test structure..."
mkdir -p tests/unit
mkdir -p tests/integration
cat > tests/__init__.py << 'EOF'
"""
Test suite for alg-snake.

Structure:
- unit/       Unit tests for individual components
- integration/  Integration tests for full game scenarios
"""
EOF

touch tests/unit/__init__.py
touch tests/integration/__init__.py
echo "  ✅ Created empty test directories"

echo ""
echo "✨ Clean slate complete!"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "Final structure:"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "📚 Documentation (3 files):"
echo "  📖 README.md       - Main documentation"
echo "  🚀 QUICKSTART.md   - Getting started guide"
echo "  📋 PROJECT_PLAN.md - Development roadmap"
echo ""
echo "🧪 Tests (fresh start):"
echo "  tests/unit/        - Empty, ready for new tests"
echo "  tests/integration/ - Empty, ready for new tests"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "Next steps:"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "1. Review changes:"
echo "   git status"
echo ""
echo "2. Test the game still runs:"
echo "   python main.py"
echo ""
echo "3. Commit:"
echo "   git add -A"
echo "   git commit -m 'refactor: clean slate - remove genetic algorithm, simplify docs, reset tests'"
echo ""
echo "4. Start Phase 1: Python 3.14 migration + modern tooling"
echo ""
