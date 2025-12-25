#!/bin/bash
# setup.sh - Automated TransformerIQ Setup Script
set -e

echo "🚀 TransformerIQ - Automated Setup"
echo "=================================="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

echo "📁 Creating project structure..."
mkdir -p transformeriq/templates

echo "📝 Creating requirements.txt..."
cat > transformeriq/requirements.txt << 'EOF'
Flask==2.3.3
pandas==2.0.3
numpy==1.24.3
gunicorn==21.2.0
selenium==4.11.2
matplotlib==3.7.2
scipy==1.11.1
EOF

echo "🔧 Creating virtual environment..."
python3 -m venv transformeriq/venv

echo "📦 Installing dependencies..."
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source transformeriq/venv/Scripts/activate
else
    source transformeriq/venv/bin/activate
fi

pip install -r transformeriq/requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Run: python transformeriq/app.py"
echo "2. Open: http://localhost:8080"
echo ""
