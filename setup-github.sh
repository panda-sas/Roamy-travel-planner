#!/bin/bash

# Script to create and push to GitHub repository

REPO_NAME="Roamy-travel-planner"
CURRENT_DIR=$(pwd)

echo "🚀 Setting up GitHub repository: $REPO_NAME"
echo "=========================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not initialized. Run 'git init' first."
    exit 1
fi

# Check if remote already exists
if git remote get-url origin > /dev/null 2>&1; then
    echo "⚠️  Remote 'origin' already exists:"
    git remote get-url origin
    read -p "Do you want to update it? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git remote remove origin
    else
        echo "Keeping existing remote."
        exit 0
    fi
fi

echo ""
echo "Choose how to create the repository:"
echo "1) Create via GitHub CLI (gh) - if installed"
echo "2) Create manually on GitHub.com (I'll provide instructions)"
echo "3) Use GitHub API with personal access token"
echo ""
read -p "Enter your choice (1/2/3): " choice

case $choice in
    1)
        echo ""
        echo "Creating repository with GitHub CLI..."
        if command -v gh &> /dev/null; then
            gh repo create "$REPO_NAME" --public --source=. --remote=origin --push
            echo "✅ Repository created and code pushed!"
        else
            echo "❌ GitHub CLI (gh) not found. Please install it or choose option 2."
            exit 1
        fi
        ;;
    2)
        echo ""
        echo "📝 Manual Setup Instructions:"
        echo "============================"
        echo ""
        echo "1. Go to https://github.com/new"
        echo "2. Repository name: $REPO_NAME"
        echo "3. Choose Public or Private"
        echo "4. DO NOT initialize with README, .gitignore, or license"
        echo "5. Click 'Create repository'"
        echo ""
        echo "6. After creating, run these commands:"
        echo ""
        echo "   git remote add origin https://github.com/YOUR_USERNAME/$REPO_NAME.git"
        echo "   git branch -M main"
        echo "   git push -u origin main"
        echo ""
        read -p "Press Enter after you've created the repository on GitHub..."
        read -p "Enter your GitHub username: " username
        git remote add origin "https://github.com/$username/$REPO_NAME.git"
        git branch -M main
        echo ""
        echo "Pushing to GitHub..."
        git push -u origin main
        echo "✅ Code pushed to GitHub!"
        ;;
    3)
        echo ""
        read -p "Enter your GitHub Personal Access Token: " -s token
        echo ""
        read -p "Enter your GitHub username: " username
        echo ""
        echo "Creating repository via API..."
        
        response=$(curl -s -w "\n%{http_code}" -X POST \
            -H "Authorization: token $token" \
            -H "Accept: application/vnd.github.v3+json" \
            https://api.github.com/user/repos \
            -d "{\"name\":\"$REPO_NAME\",\"private\":false}")
        
        http_code=$(echo "$response" | tail -n1)
        response_body=$(echo "$response" | sed '$d')
        
        if [ "$http_code" -eq 201 ]; then
            echo "✅ Repository created successfully!"
            git remote add origin "https://github.com/$username/$REPO_NAME.git"
            git branch -M main
            git push -u origin main
            echo "✅ Code pushed to GitHub!"
        else
            echo "❌ Error creating repository:"
            echo "$response_body" | grep -o '"message":"[^"]*"' || echo "HTTP $http_code"
            exit 1
        fi
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "🎉 Repository setup complete!"
echo "Your repository is available at: https://github.com/$username/$REPO_NAME"
echo ""
echo "Next steps:"
echo "1. Add OPENAI_API_KEY as a secret in your repository settings (if deploying)"
echo "2. Deploy to Streamlit Cloud: https://share.streamlit.io"

