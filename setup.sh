#!/bin/bash
# Setup script for Noon Last-Mile Resolver

echo "🚀 Setting up Noon Last-Mile Resolver..."
echo ""

# Create virtual environment
echo "📦 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment template if .env doesn't exist
if [ ! -f .env ]; then
    echo "⚙️ Creating .env from template..."
    cp .env.example .env
    echo "   Please edit .env and add your GROQ_API_KEY"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit .env and add your GROQ_API_KEY"
echo "2. Run: streamlit run app.py"
echo ""
echo "🎯 Access the app at: http://localhost:8501"
