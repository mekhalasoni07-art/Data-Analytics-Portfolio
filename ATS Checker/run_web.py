#!/usr/bin/env python3
"""
Run script for the AI Skill Assessment Agent Web Interface
"""

import os
import sys
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    print("🚀 Starting AI Skill Assessment Agent Web Interface...")
    print("📍 Make sure Ollama is running if you want to use AI models")
    print("🌐 Web interface will be available at: http://localhost:5000")
    print("❌ Press Ctrl+C to stop the server")
    print("-" * 60)

    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())