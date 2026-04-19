#!/bin/bash
# Quick test runner for the watermarking engine

echo "╔════════════════════════════════════════════╗"
echo "║  Forensic Watermarking Engine - Test Suite ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Check if FFmpeg is available (needed for tests)
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg not found. Some tests will be skipped."
    echo "   Install: brew install ffmpeg (macOS) or apt-get install ffmpeg (Linux)"
    echo ""
fi

echo "📋 Checking dependencies..."
python3 -c "import numpy, PIL, cv2" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Missing dependencies. Run: pip3 install -r requirements.txt"
fi

echo ""
echo "🧪 Running tests..."
echo ""

# Run the test suite
python3 test_engine.py

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Some tests failed."
fi

exit $EXIT_CODE
