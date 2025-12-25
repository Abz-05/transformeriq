#!/bin/bash
# test_local.sh - Test your app locally
echo "🧪 Testing TransformerIQ Locally"
echo "==============================="
echo ""

if [ ! -f "app.py" ]; then
    echo "❌ app.py not found in current directory"
    exit 1
fi

if [ ! -f "templates/index.html" ]; then
    echo "❌ templates/index.html not found"
    exit 1
fi

echo "✅ All required files found"
echo ""

if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "🚀 Starting Flask server..."
echo "📍 Open http://localhost:8080 in your browser"
echo "⏸️  Press Ctrl+C to stop"
echo ""

python app.py
