# Scripts Directory

Utility scripts for setting up and managing the AI Note Generator.

## Setup Scripts

### setup.sh (Linux/Mac)

Automated setup script for Unix-based systems.

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

**What it does:**
- Checks Python version
- Creates virtual environment
- Installs dependencies
- Creates .env file from template
- Creates output directory

### setup.bat (Windows)

Automated setup script for Windows.

```cmd
scripts\setup.bat
```

**What it does:**
- Checks Python version
- Creates virtual environment
- Installs dependencies
- Creates .env file from template
- Creates output directory

## Validation Script

### validate.py

Comprehensive validation script to check system readiness.

```bash
python scripts/validate.py
```

**What it checks:**
- Python version (3.8+)
- Required dependencies
- Optional dependencies
- Required files and directories
- Environment configuration
- Ollama availability
- API key configuration

**Example output:**
```
=== AI Note Generator Validation ===

Checking required dependencies:
✓ yaml
✓ dotenv
✓ rich
✓ reportlab

Checking optional dependencies:
✓ ollama - Ollama support
○ google.generativeai - Google Gemini support (not installed)

Checking Ollama availability:
✓ Ollama is running at http://localhost:11434
  Available models: 2
    - llama2
    - mistral

=== Validation Summary ===

✓ PASS: Python Version
✓ PASS: Dependencies
✓ PASS: Files
✓ PASS: Environment
✓ PASS: Ollama

✓ All checks passed! System is ready to use.
```

## Usage

### First Time Setup

1. Run setup script for your platform
2. Edit .env file with your API keys
3. Run validation script
4. Start using the application

### Troubleshooting

If validation fails:
- Check error messages
- Install missing dependencies
- Configure API keys in .env
- Ensure Ollama is running (if using local models)

## Additional Scripts

You can add custom scripts here for:
- Batch processing
- Automated testing
- Deployment
- Maintenance tasks
