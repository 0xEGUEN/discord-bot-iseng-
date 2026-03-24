#!/bin/bash
# GitHub Pages Deployment Setup Script

echo "🚀 Setting up GitHub Pages deployment..."

# Check if .github/workflows exists
if [ ! -d ".github/workflows" ]; then
    mkdir -p .github/workflows
    echo "✓ Created .github/workflows directory"
fi

# Check if docs folder exists
if [ ! -d "docs" ]; then
    mkdir -p docs
    echo "✓ Created docs directory"
fi

# Check if index.html exists in docs
if [ ! -f "docs/index.html" ]; then
    echo "❌ docs/index.html not found. Please ensure it's created."
else
    echo "✓ docs/index.html exists"
fi

# Check if GitHub Actions workflow exists
if [ ! -f ".github/workflows/deploy.yml" ]; then
    echo "❌ .github/workflows/deploy.yml not found."
else
    echo "✓ .github/workflows/deploy.yml exists"
fi

echo ""
echo "📋 Setup Summary:"
echo "  1. Frontend static files: docs/index.html"
echo "  2. Deployment workflow: .github/workflows/deploy.yml"
echo "  3. Guide: DEPLOYMENT.md"
echo ""
echo "✅ Ready to deploy!"
echo ""
echo "📌 Next steps:"
echo "  1. git add ."
echo "  2. git commit -m 'Setup GitHub Pages deployment'"
echo "  3. git push origin main"
echo ""
echo "  Then enable GitHub Pages in repo settings!"
