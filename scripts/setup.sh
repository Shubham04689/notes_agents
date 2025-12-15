#!/bin/bash
# Setup script for AI Note Generator

echo "=== AI Note Generator Setup ==="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please edit .env and add your API keys"
fi

# Create output directory
echo ""
echo "Creating output directory..."
mkdir -p generated_notes

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Edit .env file with your API keys"
echo "3. Run the application: python main.py"
echo ""
echo "For Ollama users:"
echo "  - Install Ollama from https://ollama.ai"
echo "  - Run: ollama serve"
echo "  - Pull a model: ollama pull llama2"
echo ""
