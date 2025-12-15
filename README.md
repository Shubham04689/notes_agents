# AI Note Generator

A complete, production-ready agent-based system that generates comprehensive, book-quality notes on any topic and compiles them into professional PDF documents.

## Features

- **Multi-Model Support**: Works with Ollama (local), Google Gemini, and Mistral AI
- **Agent-Based Architecture**: Six specialized agents work together:
  - **Planner**: Creates comprehensive hierarchical outlines
  - **Researcher**: Performs deep research on each topic
  - **Author**: Polishes content into book-quality prose
  - **Coverage Tracker**: Maintains perfect memory of progress
  - **Reviewer**: Ensures quality and completeness
  - **Completion Judge**: Determines when work is truly complete
- **Persistent State**: Resume interrupted sessions seamlessly
- **Iterative Expansion**: Never stops until topic is exhaustively covered
- **Professional PDF Output**: Publication-ready documents with proper formatting
- **Error Recovery**: Graceful handling of failures with automatic state saving

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         CLI Interface                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                      Orchestrator                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Planner  │  │Researcher│  │  Author  │  │ Reviewer │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│  ┌──────────┐  ┌──────────┐                                │
│  │ Tracker  │  │  Judge   │                                │
│  └──────────┘  └──────────┘                                │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
┌───────▼──────┐ ┌───▼────┐ ┌─────▼─────┐
│Model Adapters│ │Storage │ │   State   │
│ Ollama       │ │Manager │ │  Manager  │
│ Gemini       │ └────────┘ └───────────┘
│ Mistral      │
└──────────────┘
```

## Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd ai-note-generator
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

4. **Configure settings** (optional):
Edit `config.yaml` to customize generation parameters.

## Configuration

### Environment Variables (.env)

```env
# For Google Gemini
GEMINI_API_KEY=your_gemini_api_key_here

# For Mistral AI
MISTRAL_API_KEY=your_mistral_api_key_here

# For Ollama (local)
OLLAMA_HOST=http://localhost:11434
```

### Application Settings (config.yaml)

```yaml
storage:
  base_dir: "./generated_notes"  # Where content is stored
  state_file: "session_state.json"  # Session state file

generation:
  max_depth: 5  # Maximum outline depth
  min_section_length: 500  # Minimum words per section
  max_iterations: 100  # Safety limit
  expansion_threshold: 0.8  # Quality threshold

pdf:
  title_font_size: 24
  chapter_font_size: 18
  section_font_size: 14
  body_font_size: 11
  line_spacing: 1.5
  margin: 72  # Points (1 inch)
```

## Usage

### Basic Usage

```bash
python main.py
```

The application will:
1. Detect available model providers
2. Let you select a provider and model
3. Ask for a topic
4. Generate comprehensive notes
5. Compile into a PDF

### Model Providers

#### Ollama (Local)

1. Install Ollama: https://ollama.ai
2. Pull a model: `ollama pull llama2`
3. Ensure Ollama is running
4. Run the application

#### Google Gemini

1. Get API key: https://makersuite.google.com/app/apikey
2. Add to `.env`: `GEMINI_API_KEY=your_key`
3. Run the application

#### Mistral AI

1. Get API key: https://console.mistral.ai
2. Add to `.env`: `MISTRAL_API_KEY=your_key`
3. Run the application

### Resume Sessions

If generation is interrupted, simply run the application again. It will detect the existing session and offer to resume.

## How It Works

### 1. Planning Phase
The Planner agent creates a comprehensive hierarchical outline covering all aspects of the topic.

### 2. Iterative Generation Loop
For each node in the outline:
- **Researcher** generates deep, detailed content
- **Reviewer** evaluates quality and completeness
- **Author** polishes into book-quality prose
- **Tracker** updates progress and memory
- Content is saved to disk incrementally

### 3. Completion Judgment
The Completion Judge evaluates:
- All topics covered?
- Sufficient depth and word count?
- Any remaining gaps?
- Ready for publication?

### 4. PDF Compilation
Once approved, generates a professional PDF with:
- Title page
- Table of contents
- Properly formatted chapters and sections
- Professional typography

## Output Structure

```
generated_notes/
├── session_state.json          # Session state (for resuming)
├── metadata.json               # Generation metadata
├── content/                    # Individual content files
│   ├── ch1_Introduction.txt
│   ├── ch1_s1_Background.txt
│   └── ...
└── Topic_Name_notes.pdf        # Final PDF output
```

## Safety Features

- **Iteration Limit**: Prevents infinite loops (configurable)
- **State Persistence**: Never lose progress
- **Error Recovery**: Graceful handling of API failures
- **Quality Checks**: Multiple review stages
- **Duplication Prevention**: Tracks covered topics
- **Gap Detection**: Ensures comprehensive coverage

## Extending the System

### Adding New Model Providers

1. Create adapter in `src/models/`:
```python
from .base import BaseModelAdapter

class NewProviderAdapter(BaseModelAdapter):
    def list_models(self) -> List[str]:
        # Implementation
        pass
    
    def generate(self, prompt: str, system_prompt: str) -> str:
        # Implementation
        pass
    
    def is_available(self) -> bool:
        # Implementation
        pass
```

2. Register in `src/models/__init__.py`
3. Add to CLI provider selection

### Adding New Agents

1. Create agent in `src/agents/`:
```python
from .base import BaseAgent

class NewAgent(BaseAgent):
    def _get_system_prompt(self) -> str:
        return "Agent's role and instructions"
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation
        pass
```

2. Register in `src/agents/__init__.py`
3. Integrate into orchestrator workflow

## Troubleshooting

### "No providers available"
- Ensure at least one provider is configured
- Check API keys in `.env`
- For Ollama, ensure service is running: `ollama serve`

### "Failed to list models"
- Verify API keys are correct
- Check network connectivity
- For Ollama, verify host URL in `.env`

### "Content too short" warnings
- Increase `min_section_length` in config
- Model may need more specific prompts
- Try a more capable model

### PDF generation fails
- Ensure `reportlab` is installed
- Check write permissions in output directory
- Verify content files exist

## Performance Tips

- **Local models (Ollama)**: Faster, no API costs, but may produce shorter content
- **Cloud models (Gemini/Mistral)**: Higher quality, more comprehensive, but slower and costs API credits
- **Adjust `max_iterations`**: Lower for faster (but less complete) results
- **Adjust `min_section_length`**: Higher for more detailed content

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
