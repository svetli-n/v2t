#!/bin/bash

# Voice-to-Text Launcher
# This script starts the Voice-to-Text app

cd /Users/svetlin/workspace/v2t

# Check if another instance is running
if pgrep -f "python.*main.py" > /dev/null; then
    echo "⚠️  Voice-to-Text is already running!"
    echo "To stop it, run: pkill -f 'python.*main.py'"
    exit 1
fi

echo "🎙️  Starting Voice-to-Text..."
echo "Press Right Command to toggle recording (Start/Stop)"
echo "Press Ctrl+C to quit"
echo ""

uv run python main.py
