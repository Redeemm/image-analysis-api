#!/bin/bash

echo "🚀 Setting up Image Analysis API..."

# Check if .env.example exists
if [ ! -f ".env.example" ]; then
    echo "❌ Error: .env.example not found!"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists, skipping..."
else
    python3 -m venv venv || {
        echo "❌ Failed to create virtual environment"
        exit 1
    }
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate || {
    echo "❌ Failed to activate virtual environment"
    exit 1
}

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt || {
    echo "❌ Failed to install dependencies"
    exit 1
}

# Handle .env file
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists, skipping copy..."
    echo "💡 If you want to regenerate, delete .env and run this script again"
else
    echo "📝 Creating .env file..."
    cp .env.example .env || {
        echo "❌ Failed to create .env file"
        exit 1
    }

    # Generate API key
    echo "🔑 Generating API key..."
    API_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))") || {
        echo "❌ Failed to generate API key"
        exit 1
    }

    # Update API_KEY in .env file
    echo "🔧 Updating .env with generated API key..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/^API_KEY=.*/API_KEY=$API_KEY/" .env || {
            echo "❌ Failed to update API key"
            exit 1
        }
    else
        # Linux
        sed -i "s/^API_KEY=.*/API_KEY=$API_KEY/" .env || {
            echo "❌ Failed to update API key"
            exit 1
        }
    fi

    echo "📋 Your API key: $API_KEY"
fi

# Create uploads directory
if [ ! -d "uploads" ]; then
    echo "📁 Creating uploads directory..."
    mkdir -p uploads
fi

echo ""
echo "✨ Setup complete!"
echo ""

# Check if script was sourced or executed
if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
    # Script was sourced - venv is active
    echo "✅ Virtual environment is active!"
    echo ""
    echo "🚀 To start the server, run:"
    echo "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
else
    # Script was executed - venv is not active in parent shell
    echo "🚀 To start the server, run:"
    echo "   source venv/bin/activate"
    echo "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
    echo ""
    echo "💡 Tip: Run 'source setup.sh' instead of './setup.sh' to keep venv active"
fi

echo ""
echo "📖 API Documentation: http://localhost:8000/api/v1/docs"
