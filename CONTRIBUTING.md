# Contributing to AI Note Generator

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Maintain a professional environment

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs. actual behavior
   - System information (OS, Python version, model used)
   - Error messages and logs

### Suggesting Features

1. Check if the feature has been suggested in Issues
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Potential implementation approach
   - Any relevant examples

### Submitting Code

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/ai-note-generator.git
   cd ai-note-generator
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the code style guidelines (see below)
   - Add tests for new functionality
   - Update documentation as needed

4. **Test your changes**
   ```bash
   pytest tests/
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide clear description of changes
   - Reference any related issues
   - Ensure all tests pass

## Code Style Guidelines

### Python Style

- Follow PEP 8
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use docstrings for all public functions and classes

Example:
```python
def generate_content(topic: str, depth: int = 3) -> Dict[str, Any]:
    """
    Generate content for a given topic.
    
    Args:
        topic: The topic to generate content for
        depth: Hierarchical depth of the outline (default: 3)
    
    Returns:
        Dictionary containing generated content and metadata
    
    Raises:
        ValueError: If topic is empty or invalid
    """
    pass
```

### Documentation

- Update README.md for user-facing changes
- Update ARCHITECTURE.md for system design changes
- Update USAGE_GUIDE.md for new features
- Add docstrings to all new functions and classes

### Testing

- Write unit tests for new functionality
- Maintain or improve code coverage
- Test edge cases and error conditions
- Use meaningful test names

Example:
```python
def test_planner_creates_valid_outline():
    """Test that planner agent creates a valid hierarchical outline"""
    # Test implementation
    pass
```

## Project Structure

```
ai-note-generator/
├── src/
│   ├── agents/          # Agent implementations
│   ├── models/          # Model adapters
│   ├── core/            # Core system components
│   ├── pdf/             # PDF generation
│   └── ui/              # User interface
├── tests/               # Test suite
├── examples/            # Example scripts
├── scripts/             # Setup and utility scripts
└── docs/                # Additional documentation
```

## Development Setup

1. **Clone and setup**
   ```bash
   git clone https://github.com/yourusername/ai-note-generator.git
   cd ai-note-generator
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Install development dependencies**
   ```bash
   pip install pytest pytest-cov black flake8 mypy
   ```

3. **Run tests**
   ```bash
   pytest tests/ -v
   ```

4. **Check code style**
   ```bash
   black src/ tests/
   flake8 src/ tests/
   mypy src/
   ```

## Areas for Contribution

### High Priority

- [ ] Add support for more LLM providers (Anthropic Claude, OpenAI)
- [ ] Implement parallel node processing for faster generation
- [ ] Add web-based UI
- [ ] Improve error handling and recovery
- [ ] Add progress persistence for very long sessions

### Medium Priority

- [ ] Citation and bibliography support
- [ ] Image and diagram generation
- [ ] Export to additional formats (EPUB, HTML, Markdown)
- [ ] Multi-language support
- [ ] Quality metrics and analytics

### Low Priority

- [ ] GUI application (desktop)
- [ ] Collaborative editing features
- [ ] Version control for generated content
- [ ] Integration with note-taking apps
- [ ] Cloud storage integration

## Adding New Model Providers

To add support for a new LLM provider:

1. **Create adapter class** in `src/models/`
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

2. **Register in `src/models/__init__.py`**
   ```python
   from .new_provider_adapter import NewProviderAdapter
   __all__ = [..., 'NewProviderAdapter']
   ```

3. **Add to CLI** in `src/ui/cli.py`
   - Add provider detection
   - Add to provider selection menu
   - Add initialization logic

4. **Update documentation**
   - Add to README.md
   - Add configuration instructions
   - Add example usage

5. **Add tests**
   - Unit tests for adapter
   - Integration tests
   - Mock API responses

## Adding New Agents

To add a new agent:

1. **Create agent class** in `src/agents/`
   ```python
   from .base import BaseAgent
   
   class NewAgent(BaseAgent):
       def _get_system_prompt(self) -> str:
           return "Agent's role and instructions"
       
       def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
           # Implementation
           pass
   ```

2. **Register in `src/agents/__init__.py`**

3. **Integrate into orchestrator** in `src/core/orchestrator.py`

4. **Document behavior** in `PROMPTS.md`

5. **Add tests**

## Release Process

1. Update version in `setup.py`
2. Update CHANGELOG.md
3. Create git tag: `git tag v1.x.x`
4. Push tag: `git push origin v1.x.x`
5. Create GitHub release with notes

## Questions?

- Open an issue for questions
- Join discussions in GitHub Discussions
- Check existing documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
