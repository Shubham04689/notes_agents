#!/usr/bin/env python3
"""
AI Note Generator - Main Entry Point

A complete agent-based system for generating comprehensive, book-quality notes
on any topic using AI models (Ollama, Gemini, Mistral).
"""

import os
import sys
import yaml
from dotenv import load_dotenv
from src.ui import CLI


def load_config(config_path: str = 'config.yaml') -> dict:
    """Load configuration from YAML file"""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing configuration file: {e}")
        sys.exit(1)


def main():
    """Main entry point"""
    # Load environment variables
    load_dotenv()
    
    # Load configuration
    config = load_config()
    
    # Initialize and run CLI
    cli = CLI(config)
    cli.run()


if __name__ == '__main__':
    main()
