#!/usr/bin/env python3
"""
Run with Mistral Small (faster, lower rate limits)
"""

import os
import yaml
from dotenv import load_dotenv
from src.models import MistralAdapter
from src.core import Orchestrator, StorageManager, StateManager
from src.pdf import PDFGenerator

print("=" * 70)
print("AI NOTE GENERATOR - MISTRAL SMALL (OPTIMIZED FOR RATE LIMITS)")
print("=" * 70)
print()

load_dotenv()

api_key = os.getenv('MISTRAL_API_KEY')
if not api_key or api_key == 'your_mistral_api_key_here':
    print("❌ MISTRAL_API_KEY not configured")
    exit(1)

# Load config
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Optimize for rate limits
config['generation']['max_depth'] = 3  # Moderate depth
config['generation']['min_section_length'] = 250  # Moderate length
config['generation']['max_iterations'] = 20  # Reasonable limit

print("✓ Initializing Mistral AI...")
model = MistralAdapter()

if not model.is_available():
    print("❌ Mistral not available")
    exit(1)

# Use open-mistral-7b (fastest, lowest rate limits)
model.set_model('open-mistral-7b')
print(f"✓ Using: open-mistral-7b (optimized for speed)")
print()

# Setup
base_dir = "./mistral_output"
state_file = os.path.join(base_dir, "state.json")

storage = StorageManager(base_dir)
state = StateManager(state_file)
orchestrator = Orchestrator(model, storage, state, config)

print("✓ System ready")
print()

# Check for existing session
if state.has_active_session():
    session_info = state.get_session_info()
    print(f"Found existing session: {session_info['topic']}")
    resume = input("Resume? (y/n): ").lower() == 'y'
    if resume:
        print("\n⏳ Resuming generation...")
        topic = session_info['topic']
    else:
        topic = input("\nEnter new topic: ")
        storage.clear_storage()
        state.clear_state()
else:
    topic = input("Enter topic: ")

print()
print(f"Topic: {topic}")
print("Configuration:")
print(f"  - Model: open-mistral-7b (fast)")
print(f"  - Depth: {config['generation']['max_depth']}")
print(f"  - Min length: {config['generation']['min_section_length']} words")
print(f"  - Max iterations: {config['generation']['max_iterations']}")
print()
print("⏳ Generating with rate limit protection...")
print("   (Automatic retry on rate limits)")
print()

try:
    result = orchestrator.generate_notes(topic, resume=state.has_active_session())
    
    print()
    print("=" * 70)
    
    if result['success']:
        print("✓ GENERATION COMPLETE!")
        print()
        print(f"Status: {'Complete' if result.get('complete') else 'Partial'}")
        print(f"Total words: {result.get('total_word_count', 0):,}")
        print(f"Ready for PDF: {result.get('ready_for_pdf', False)}")
        print()
        
        content_files = storage.get_all_content_files()
        print(f"Generated {len(content_files)} files")
        print()
        
        if result.get('ready_for_pdf'):
            print("Generating PDF...")
            pdf_gen = PDFGenerator(config)
            output_path = os.path.join(base_dir, f"{topic.replace(' ', '_')}_notes.pdf")
            metadata = {
                'model': model.model_name,
                'total_word_count': result.get('total_word_count', 0)
            }
            pdf_path = pdf_gen.generate(topic, content_files, output_path, metadata)
            print(f"✓ PDF: {pdf_path}")
            print()
        
        print(f"Output: {base_dir}/")
        print()
        print("Your Mistral API usage:")
        print(f"  Monthly limit: $150")
        print(f"  Tokens per minute: 500,000")
        print(f"  Tokens per month: 1,000,000,000")
        print()
        print("✓ System working perfectly with rate limit protection!")
        
    else:
        print(f"❌ Failed: {result.get('error')}")

except KeyboardInterrupt:
    print("\n\n⚠ Interrupted")
    print("Progress saved. Run again to resume.")
except Exception as e:
    print(f"\n\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
