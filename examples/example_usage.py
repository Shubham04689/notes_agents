#!/usr/bin/env python3
"""
Example usage of the AI Note Generator programmatically
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
from src.models import OllamaAdapter, GeminiAdapter
from src.core import Orchestrator, StorageManager, StateManager
from src.pdf import PDFGenerator
import yaml


def example_basic_usage():
    """Basic usage example"""
    print("=== Basic Usage Example ===\n")
    
    # Load environment and config
    load_dotenv()
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize model (using Ollama for this example)
    print("Initializing Ollama adapter...")
    model = OllamaAdapter()
    
    if not model.is_available():
        print("Error: Ollama is not available. Please start Ollama service.")
        return
    
    # List and select model
    models = model.list_models()
    print(f"Available models: {models}")
    
    if not models:
        print("No models available. Please pull a model: ollama pull llama2")
        return
    
    model.set_model(models[0])
    print(f"Using model: {models[0]}\n")
    
    # Initialize components
    base_dir = config['storage']['base_dir']
    state_file = os.path.join(base_dir, config['storage']['state_file'])
    
    storage = StorageManager(base_dir)
    state = StateManager(state_file)
    orchestrator = Orchestrator(model, storage, state, config)
    
    # Generate notes
    topic = "Introduction to Python Programming"
    print(f"Generating notes for: {topic}\n")
    
    result = orchestrator.generate_notes(topic, resume=False)
    
    if result['success'] and result.get('ready_for_pdf'):
        print("\n=== Generation Complete ===")
        print(f"Total words: {result['total_word_count']}")
        
        # Generate PDF
        print("\nGenerating PDF...")
        pdf_gen = PDFGenerator(config)
        content_files = storage.get_all_content_files()
        
        output_path = os.path.join(base_dir, f"{topic.replace(' ', '_')}_notes.pdf")
        metadata = {
            'model': model.model_name,
            'total_word_count': result['total_word_count']
        }
        
        pdf_path = pdf_gen.generate(topic, content_files, output_path, metadata)
        print(f"PDF created: {pdf_path}")
    else:
        print("\n=== Generation Incomplete ===")
        print("Run again to continue or adjust configuration.")


def example_with_gemini():
    """Example using Google Gemini"""
    print("=== Gemini Usage Example ===\n")
    
    load_dotenv()
    
    # Check for API key
    if not os.getenv('GEMINI_API_KEY'):
        print("Error: GEMINI_API_KEY not found in environment")
        return
    
    # Initialize Gemini
    print("Initializing Gemini adapter...")
    model = GeminiAdapter()
    
    if not model.is_available():
        print("Error: Gemini is not available")
        return
    
    # List models
    models = model.list_models()
    print(f"Available Gemini models: {models[:3]}")  # Show first 3
    
    # Select a model (e.g., gemini-pro)
    gemini_pro = [m for m in models if 'gemini-pro' in m.lower()]
    if gemini_pro:
        model.set_model(gemini_pro[0])
        print(f"Using: {gemini_pro[0]}\n")
    else:
        print("gemini-pro not found")
        return
    
    # Rest of the process is the same as basic example
    print("Ready to generate notes with Gemini!")


def example_custom_config():
    """Example with custom configuration"""
    print("=== Custom Configuration Example ===\n")
    
    # Create custom config
    custom_config = {
        'storage': {
            'base_dir': './custom_output',
            'state_file': 'custom_state.json'
        },
        'generation': {
            'max_depth': 3,  # Shallower outline
            'min_section_length': 300,  # Shorter sections
            'max_iterations': 50,  # Fewer iterations
            'expansion_threshold': 0.7  # More lenient
        },
        'pdf': {
            'title_font_size': 20,
            'chapter_font_size': 16,
            'section_font_size': 12,
            'body_font_size': 10,
            'line_spacing': 1.3,
            'margin': 60
        }
    }
    
    print("Custom configuration:")
    print(f"  - Output directory: {custom_config['storage']['base_dir']}")
    print(f"  - Max depth: {custom_config['generation']['max_depth']}")
    print(f"  - Min section length: {custom_config['generation']['min_section_length']}")
    print(f"  - Max iterations: {custom_config['generation']['max_iterations']}")
    print("\nThis configuration will generate faster but less detailed notes.")


def example_resume_session():
    """Example of resuming an interrupted session"""
    print("=== Resume Session Example ===\n")
    
    load_dotenv()
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Check for existing session
    base_dir = config['storage']['base_dir']
    state_file = os.path.join(base_dir, config['storage']['state_file'])
    
    state = StateManager(state_file)
    
    if state.has_active_session():
        session_info = state.get_session_info()
        print("Found existing session:")
        print(f"  Topic: {session_info['topic']}")
        print(f"  Model: {session_info['model']}")
        print(f"  Status: {session_info['status']}")
        
        status = state.get_status()
        print(f"\nProgress:")
        print(f"  Covered: {status['covered_count']}/{status['total_nodes']} nodes")
        print(f"  Progress: {status['progress_percent']}%")
        print(f"  Total words: {status['total_word_count']}")
        
        print("\nTo resume, run the main application.")
    else:
        print("No active session found.")


def example_inspect_output():
    """Example of inspecting generated output"""
    print("=== Inspect Output Example ===\n")
    
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    base_dir = config['storage']['base_dir']
    
    if not os.path.exists(base_dir):
        print(f"Output directory not found: {base_dir}")
        return
    
    # Check state
    state_file = os.path.join(base_dir, config['storage']['state_file'])
    if os.path.exists(state_file):
        state = StateManager(state_file)
        status = state.get_status()
        
        print("Session Status:")
        print(f"  Topic: {status['topic']}")
        print(f"  Total nodes: {status['total_nodes']}")
        print(f"  Covered: {status['covered_count']}")
        print(f"  Pending: {status['pending_count']}")
        print(f"  Progress: {status['progress_percent']}%")
        print(f"  Total words: {status['total_word_count']}")
    
    # List content files
    content_dir = os.path.join(base_dir, 'content')
    if os.path.exists(content_dir):
        files = [f for f in os.listdir(content_dir) if f.endswith('.txt')]
        print(f"\nContent files: {len(files)}")
        for f in files[:5]:  # Show first 5
            print(f"  - {f}")
        if len(files) > 5:
            print(f"  ... and {len(files) - 5} more")
    
    # Check for PDF
    pdf_files = [f for f in os.listdir(base_dir) if f.endswith('.pdf')]
    if pdf_files:
        print(f"\nPDF files:")
        for f in pdf_files:
            filepath = os.path.join(base_dir, f)
            size = os.path.getsize(filepath) / 1024  # KB
            print(f"  - {f} ({size:.1f} KB)")


if __name__ == '__main__':
    print("AI Note Generator - Example Usage\n")
    print("Choose an example:")
    print("1. Basic usage with Ollama")
    print("2. Usage with Google Gemini")
    print("3. Custom configuration")
    print("4. Resume interrupted session")
    print("5. Inspect generated output")
    print("0. Exit")
    
    choice = input("\nEnter choice (0-5): ").strip()
    print()
    
    if choice == '1':
        example_basic_usage()
    elif choice == '2':
        example_with_gemini()
    elif choice == '3':
        example_custom_config()
    elif choice == '4':
        example_resume_session()
    elif choice == '5':
        example_inspect_output()
    elif choice == '0':
        print("Goodbye!")
    else:
        print("Invalid choice")
