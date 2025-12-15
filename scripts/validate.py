#!/usr/bin/env python3
"""
Validation script to check if the AI Note Generator is properly set up
"""

import os
import sys
import importlib.util

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python version too old: {version.major}.{version.minor}.{version.micro}")
        print("  Required: Python 3.8 or higher")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    required = [
        'yaml',
        'dotenv',
        'rich',
        'reportlab',
        'pydantic',
        'requests'
    ]
    
    optional = [
        ('ollama', 'Ollama support'),
        ('google.generativeai', 'Google Gemini support'),
        ('mistralai', 'Mistral AI support')
    ]
    
    print("\nChecking required dependencies:")
    all_ok = True
    for module in required:
        spec = importlib.util.find_spec(module)
        if spec is not None:
            print(f"✓ {module}")
        else:
            print(f"✗ {module} (missing)")
            all_ok = False
    
    print("\nChecking optional dependencies:")
    for module, desc in optional:
        spec = importlib.util.find_spec(module)
        if spec is not None:
            print(f"✓ {module} - {desc}")
        else:
            print(f"○ {module} - {desc} (not installed)")
    
    return all_ok

def check_files():
    """Check if required files exist"""
    required_files = [
        'main.py',
        'config.yaml',
        'requirements.txt',
        '.env.example'
    ]
    
    required_dirs = [
        'src',
        'src/models',
        'src/agents',
        'src/core',
        'src/pdf',
        'src/ui'
    ]
    
    print("\nChecking required files:")
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} (missing)")
            all_ok = False
    
    print("\nChecking required directories:")
    for dir in required_dirs:
        if os.path.isdir(dir):
            print(f"✓ {dir}/")
        else:
            print(f"✗ {dir}/ (missing)")
            all_ok = False
    
    return all_ok

def check_env():
    """Check environment configuration"""
    print("\nChecking environment configuration:")
    
    if os.path.exists('.env'):
        print("✓ .env file exists")
        
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check for API keys
        gemini_key = os.getenv('GEMINI_API_KEY')
        mistral_key = os.getenv('MISTRAL_API_KEY')
        ollama_host = os.getenv('OLLAMA_HOST')
        
        if gemini_key and gemini_key != 'your_gemini_api_key_here':
            print("✓ GEMINI_API_KEY configured")
        else:
            print("○ GEMINI_API_KEY not configured")
        
        if mistral_key and mistral_key != 'your_mistral_api_key_here':
            print("✓ MISTRAL_API_KEY configured")
        else:
            print("○ MISTRAL_API_KEY not configured")
        
        if ollama_host:
            print(f"✓ OLLAMA_HOST configured: {ollama_host}")
        else:
            print("○ OLLAMA_HOST not configured (will use default)")
    else:
        print("○ .env file not found (copy from .env.example)")
    
    return True

def check_ollama():
    """Check if Ollama is available"""
    print("\nChecking Ollama availability:")
    try:
        import requests
        host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        response = requests.get(f"{host}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✓ Ollama is running at {host}")
            print(f"  Available models: {len(models)}")
            for model in models[:3]:
                print(f"    - {model['name']}")
            if len(models) > 3:
                print(f"    ... and {len(models) - 3} more")
            return True
        else:
            print(f"○ Ollama responded with status {response.status_code}")
            return False
    except Exception as e:
        print(f"○ Ollama not available: {e}")
        print("  To use Ollama:")
        print("    1. Install from https://ollama.ai")
        print("    2. Run: ollama serve")
        print("    3. Pull a model: ollama pull llama2")
        return False

def main():
    """Run all validation checks"""
    print("=== AI Note Generator Validation ===\n")
    
    results = []
    
    results.append(("Python Version", check_python_version()))
    results.append(("Dependencies", check_dependencies()))
    results.append(("Files", check_files()))
    results.append(("Environment", check_env()))
    results.append(("Ollama", check_ollama()))
    
    print("\n=== Validation Summary ===\n")
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
        if not passed:
            all_passed = False
    
    print()
    
    if all_passed:
        print("✓ All checks passed! System is ready to use.")
        print("\nRun: python main.py")
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        print("\nFor help, see:")
        print("  - README.md")
        print("  - USAGE_GUIDE.md")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
