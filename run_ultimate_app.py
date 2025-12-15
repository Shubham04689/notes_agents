#!/usr/bin/env python3
"""
Startup script for Ultimate AI Notes Generator
Complete profile-based system with all features
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🚀 Ultimate AI Notes Generator - Complete System")
    print("=" * 70)
    print("✅ Profile-based generation system")
    print("🔑 API key management")
    print("🔄 Resume failed generations")
    print("🛑 Stop generation anytime")
    print("📁 Organized file structure by profile")
    print("📊 Multiple concurrent generations")
    print("📄 Professional PDF output")
    print("=" * 70)
    
    # Check if we're in the right directory
    if not os.path.exists('ultimate_notes_app.py'):
        print("❌ Error: ultimate_notes_app.py not found")
        print("   Make sure you're running this from the project root directory")
        return 1
    
    # Check if templates directory exists
    if not os.path.exists('templates/ultimate_interface.html'):
        print("❌ Error: templates/ultimate_interface.html not found")
        print("   The template file is missing")
        return 1
    
    # Check if src directory exists
    if not os.path.exists('src'):
        print("❌ Error: src directory not found")
        print("   The source code directory is missing")
        return 1
    
    print("✅ All required files found")
    print("🌐 Starting ultimate web server...")
    print("📱 Open your browser to: http://localhost:5000")
    print()
    print("🎯 Available Generation Profiles:")
    print("   • Elementary Student - Simple, easy-to-understand notes")
    print("   • Middle School Student - Detailed notes with examples")
    print("   • High School Student - Comprehensive notes with analysis")
    print("   • College/University - In-depth academic notes")
    print("   • Professional Quick - Concise, actionable notes")
    print("   • Professional Detailed - Comprehensive professional docs")
    print("   • Academic Research - Scholarly notes with citations")
    print("   • Creative & Writing - Engaging notes with storytelling")
    print()
    print("🛑 Press Ctrl+C to stop")
    print("=" * 70)
    
    try:
        # Run the ultimate notes app
        subprocess.run([sys.executable, 'ultimate_notes_app.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Server failed to start: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())