#!/usr/bin/env python3
"""
Generate PDF from existing content files
"""

import os
import yaml
from src.pdf import PDFGenerator
from src.core import StorageManager

print("=" * 60)
print("PDF GENERATOR - From Existing Content")
print("=" * 60)
print()

# Load config
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Check available content directories
content_dirs = [
    './mistral_demo_output',
    './mistral_output',
    './demo_output',
    './generated_notes'
]

available = []
for dir_path in content_dirs:
    content_path = os.path.join(dir_path, 'content')
    if os.path.exists(content_path):
        files = [f for f in os.listdir(content_path) if f.endswith('.txt')]
        if files:
            available.append((dir_path, len(files)))

if not available:
    print("❌ No content found to generate PDF from.")
    print()
    print("Run one of these first:")
    print("  - demo_mistral.py")
    print("  - run_with_mistral_small.py")
    print("  - main.py")
    exit(0)

print("Available content:")
for i, (dir_path, count) in enumerate(available, 1):
    print(f"  {i}. {dir_path} ({count} files)")
print()

if len(available) == 1:
    choice = 0
else:
    choice = int(input(f"Select directory [1-{len(available)}]: ")) - 1

selected_dir = available[choice][0]
print(f"\n✓ Using: {selected_dir}")
print()

# Initialize storage
storage = StorageManager(selected_dir)

# Get content files
content_files = storage.get_all_content_files()
print(f"Found {len(content_files)} content files:")
for f in content_files:
    filename = os.path.basename(f)
    print(f"  - {filename}")
print()

# Get topic from first file
with open(content_files[0], 'r', encoding='utf-8') as f:
    lines = f.readlines()
    topic = lines[0].replace('# ', '').strip() if lines else "Generated Notes"

# Count total words
total_words = 0
for filepath in content_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        total_words += len(f.read().split())

print(f"Topic: {topic}")
print(f"Total words: {total_words:,}")
print()

# Generate PDF
output_filename = f"{topic.replace(' ', '_')}_notes.pdf"
output_path = os.path.join(selected_dir, output_filename)

print("⏳ Generating PDF...")
print()

try:
    pdf_gen = PDFGenerator(config)
    
    metadata = {
        'model': 'Mistral AI',
        'total_word_count': total_words
    }
    
    pdf_path = pdf_gen.generate(topic, content_files, output_path, metadata)
    
    print("=" * 60)
    print("✓ PDF GENERATED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print(f"Location: {pdf_path}")
    print(f"Size: {os.path.getsize(pdf_path) / 1024:.1f} KB")
    print()
    print("The PDF contains:")
    print(f"  - {len(content_files)} sections")
    print(f"  - {total_words:,} words")
    print(f"  - Professional formatting")
    print(f"  - Table of contents")
    print()
    print("To open:")
    print(f"  start {pdf_path}")
    
except Exception as e:
    print(f"❌ Error generating PDF: {e}")
    import traceback
    traceback.print_exc()
