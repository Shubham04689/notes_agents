#!/usr/bin/env python3
"""
Cleanup script to remove unnecessary web app files
Keeps only the ultimate app and essential files
"""

import os
import shutil
from pathlib import Path

def main():
    print("🧹 Cleaning up unnecessary web app files...")
    print("=" * 50)
    
    # Files to remove
    files_to_remove = [
        'web_app.py',
        'complete_web_app.py', 
        'student_notes_app.py',
        'working_web.py',
        'simple_web.py',
        'debug_web.py',
        'start_web.py',
        'web_app_debug.py',
        'test_web_complete.py',
        'test_flask.py',
        'test_imports.py',
        'run_student_app.py',
        'run_complete_web.py',
        'setup_web.bat',
        'start_web.bat',
        'templates/index.html',
        'templates/complete_interface.html',
        'templates/student_interface.html'
    ]
    
    # Directories to remove
    dirs_to_remove = [
        'web_output',
        'mistral_output',
        'mistral_demo_output',
        'demo_output',
        'ollama_test_output',
        'test_output'
    ]
    
    removed_files = 0
    removed_dirs = 0
    
    # Remove files
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"✅ Removed file: {file_path}")
                removed_files += 1
            except Exception as e:
                print(f"❌ Failed to remove {file_path}: {e}")
        else:
            print(f"⚠️  File not found: {file_path}")
    
    # Remove directories
    for dir_path in dirs_to_remove:
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
                print(f"✅ Removed directory: {dir_path}")
                removed_dirs += 1
            except Exception as e:
                print(f"❌ Failed to remove {dir_path}: {e}")
        else:
            print(f"⚠️  Directory not found: {dir_path}")
    
    print("=" * 50)
    print(f"🎉 Cleanup complete!")
    print(f"📁 Removed {removed_files} files")
    print(f"📂 Removed {removed_dirs} directories")
    print()
    print("✅ Remaining files:")
    print("   • ultimate_notes_app.py - Main application")
    print("   • templates/ultimate_interface.html - UI template")
    print("   • run_ultimate_app.py - Startup script")
    print("   • src/ - Core functionality")
    print("   • notes_output/ - Generated files (organized by profile)")
    print()
    print("🚀 Run 'python run_ultimate_app.py' to start the ultimate app!")

if __name__ == "__main__":
    main()