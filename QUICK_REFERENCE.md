# Quick Reference Guide

## Installation

```bash
# Clone repository
git clone <repository-url>
cd ai-note-generator

# Run setup script
# Windows:
scripts\setup.bat

# Linux/Mac:
chmod +x scripts/setup.sh
./scripts/setup.sh

# Or manual setup:
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## Configuration

### .env File
```env
GEMINI_API_KEY=your_key_here
MISTRAL_API_KEY=your_key_here
OLLAMA_HOST=http://localhost:11434
```

### config.yaml
```yaml
generation:
  max_depth: 5              # Outline depth
  min_section_length: 500   # Min words per section
  max_iterations: 100       # Safety limit
  expansion_threshold: 0.8  # Quality threshold
```

## Usage

### Basic Usage
```bash
python main.py
```

### Validation
```bash
python scripts/validate.py
```

### Examples
```bash
python examples/example_usage.py
```

### Testing
```bash
pytest tests/
```

## Model Providers

### Ollama (Local)
```bash
# Install from https://ollama.ai
ollama serve
ollama pull llama2
```

### Google Gemini
1. Get API key: https://makersuite.google.com/app/apikey
2. Add to .env: `GEMINI_API_KEY=your_key`

### Mistral AI
1. Get API key: https://console.mistral.ai
2. Add to .env: `MISTRAL_API_KEY=your_key`

## Common Commands

### Start Generation
```bash
python main.py
```

### Resume Session
```bash
python main.py
# Select "Resume" when prompted
```

### Clear Session
```bash
# Windows:
del generated_notes\session_state.json

# Linux/Mac:
rm generated_notes/session_state.json
```

### View Output
```bash
# Windows:
dir generated_notes\content
start generated_notes\*.pdf

# Linux/Mac:
ls generated_notes/content/
open generated_notes/*.pdf
```

## File Locations

### Generated Content
- `generated_notes/content/*.txt` - Individual sections
- `generated_notes/*.pdf` - Final PDF output
- `generated_notes/session_state.json` - Session state
- `generated_notes/metadata.json` - Generation metadata

### Configuration
- `.env` - API keys and environment
- `config.yaml` - Application settings

### Source Code
- `src/models/` - Model adapters
- `src/agents/` - AI agents
- `src/core/` - Core system
- `src/pdf/` - PDF generation
- `src/ui/` - User interface

## Troubleshooting

### No providers available
```bash
# Check Ollama
ollama serve

# Check API keys
cat .env  # Linux/Mac
type .env  # Windows
```

### Failed to list models
```bash
# Test Ollama
curl http://localhost:11434/api/tags

# Verify API keys are correct
```

### Content too short
Edit `config.yaml`:
```yaml
generation:
  min_section_length: 1000  # Increase
```

### Generation too slow
Edit `config.yaml`:
```yaml
generation:
  min_section_length: 300  # Decrease
  max_depth: 3  # Reduce depth
```

### PDF generation fails
```bash
pip install --upgrade reportlab
```

## Agent Roles

1. **Planner**: Creates comprehensive outline
2. **Researcher**: Deep research (500+ words)
3. **Author**: Polishes into book-quality prose
4. **Tracker**: Maintains progress memory
5. **Reviewer**: Quality assurance
6. **Judge**: Determines completeness

## Workflow

```
Topic Input
    ↓
Planner → Outline
    ↓
For each node:
    Researcher → Content
    Reviewer → Quality Check
    Author → Polish
    Storage → Save
    Tracker → Update
    ↓
Judge → Approve?
    ↓
PDF Generator → Final PDF
```

## Configuration Presets

### Quick Draft
```yaml
generation:
  max_depth: 3
  min_section_length: 300
  max_iterations: 50
```

### Standard (Default)
```yaml
generation:
  max_depth: 5
  min_section_length: 500
  max_iterations: 100
```

### Comprehensive Book
```yaml
generation:
  max_depth: 5
  min_section_length: 1000
  max_iterations: 200
```

## Performance Tips

- **Fast**: Use Ollama with quick draft preset
- **Quality**: Use Gemini with comprehensive preset
- **Balanced**: Use Mistral with standard preset

## Documentation

- `README.md` - Overview and quick start
- `USAGE_GUIDE.md` - Detailed usage (1000+ lines)
- `ARCHITECTURE.md` - System design (2000+ lines)
- `PROMPTS.md` - Agent behaviors (800+ lines)
- `CONTRIBUTING.md` - Contribution guide
- `CHANGELOG.md` - Version history

## Support

- GitHub Issues: Bug reports
- GitHub Discussions: Questions
- Documentation: Comprehensive guides

## License

MIT License - See LICENSE file
