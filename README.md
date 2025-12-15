# AI Note Generator

A complete, production-ready agent-based system that generates comprehensive, book-quality notes on any topic and compiles them into professional PDF documents.

## 📚 Project Documentation

This project contains extensive documentation to help you understand, use, and extend the system:

### 🚀 Getting Started
- **[START_HERE.md](START_HERE.md)**: The best place to start for new users.
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)**: Handy cheat sheet for common commands and shortcuts.
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)**: Detailed step-by-step instructions for all features.

### 📖 System Overview
- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)**: High-level vision and capabilities of the system.
- **[ARCHITECTURE.md](ARCHITECTURE.md)**: Deep dive into the agentic architecture and technical design.
- **[APPLICATION_STATUS.md](APPLICATION_STATUS.md)**: Current operational status and functional verification.
- **[STATUS.md](STATUS.md)**: Brief project status update.

### 🌐 Web Interface
- **[WEB_README.md](WEB_README.md)**: Guide for the web-based version of the application.
- **[WEB_INTERFACE.md](WEB_INTERFACE.md)**: Details on the web UI components and features.
- **[COMPLETE_WEB_GUIDE.md](COMPLETE_WEB_GUIDE.md)**: Comprehensive guide for web deployment and usage.

### 🛠️ Development & Reference
- **[PROMPTS.md](PROMPTS.md)**: The system prompts that power the individual AI agents.
- **[CONTRIBUTING.md](CONTRIBUTING.md)**: Guidelines for contributing to the project.
- **[CHANGELOG.md](CHANGELOG.md)**: History of changes and updates.

### 📊 Summaries
- **[COMPLETE_PROJECT_SUMMARY.md](COMPLETE_PROJECT_SUMMARY.md)**: Full summary of the project's development.
- **[FINAL_SUMMARY.md](FINAL_SUMMARY.md)**: Conclusion of the development phase.
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)**: Concise project abstract.

### 🎓 Specialized Guides
- **[STUDENT_APP_GUIDE.md](STUDENT_APP_GUIDE.md)**: Specific guide for using the app for academic purposes.
- **[ULTIMATE_README.md](ULTIMATE_README.md)**: An alternative, detailed comprehensive readme.

---

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
# 🚀 Ultimate AI Notes Generator

A complete, production-ready AI-powered note generation system with profile-based generation, API key management, resume functionality, and professional PDF output.

## ✨ Features

### 🎯 Profile-Based Generation System
- **8 Specialized Profiles** for different use cases:
  - 🎒 **Elementary Student** - Simple, easy-to-understand notes
  - 📚 **Middle School Student** - Detailed notes with examples
  - 🎓 **High School Student** - Comprehensive notes with analysis
  - 🏛️ **College/University** - In-depth academic notes
  - ⚡ **Professional Quick** - Concise, actionable notes
  - 💼 **Professional Detailed** - Comprehensive professional docs
  - 🔬 **Academic Research** - Scholarly notes with citations
  - ✍️ **Creative & Writing** - Engaging notes with storytelling

### 🤖 Multi-Provider AI Support
- **Local Models**: Ollama, LM Studio (Free, Private)
- **Cloud Models**: Google Gemini, Mistral AI (High Quality)
- **Automatic Detection** of available providers
- **Model Selection** with recommendations

### 🔑 Built-in API Key Management
- **Secure Storage** in .env file
- **Visual Status** indicators
- **Easy Configuration** through web interface
- **Direct Links** to get API keys

### 🔄 Resume Failed Generations
- **Automatic Detection** of failed generations
- **Resume from Last State** with partial progress
- **No Lost Work** - continue where you left off
- **Smart Recovery** from errors and limits

### 🛑 Advanced Generation Control
- **Stop Anytime** and still get PDF with completed sections
- **Multiple Concurrent** generations
- **Real-time Progress** tracking
- **Session Management** with unique IDs

### 📁 Organized File Structure
```
notes_output/
├── elementary_student/
│   ├── topic_name_20241215_143022/
│   │   ├── content/
│   │   └── pdfs/
├── professional_detailed/
│   ├── another_topic_20241215_144533/
│   │   ├── content/
│   │   └── pdfs/
└── ...
```

### 📄 Professional PDF Output
- **Table of Contents** with page navigation
- **Hierarchical Headers** and proper formatting
- **Code Block** highlighting
- **Metadata** including generation details
- **Professional Layout** with consistent styling

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Environment (Optional)
```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your API keys (optional)
# GEMINI_API_KEY=your_key_here
# MISTRAL_API_KEY=your_key_here
# OLLAMA_HOST=http://localhost:11434
```

### 3. Run the Application
```bash
python run_ultimate_app.py
```

### 4. Open Your Browser
Navigate to: http://localhost:5000

## 🎯 How to Use

### Step 1: Choose Your Profile
Select the generation profile that matches your needs:
- **Students**: Elementary → Middle School → High School → College
- **Professionals**: Quick Reference → Comprehensive Documentation
- **Researchers**: Academic Research with citations
- **Writers**: Creative & Engaging content

### Step 2: Select AI Provider
- **Local Models** (Free, Private): Ollama or LM Studio
- **Cloud Models** (High Quality): Google Gemini or Mistral AI
- **API Keys**: Configure through the web interface

### Step 3: Enter Your Topic
Be specific for better results:
- ✅ "Machine Learning Fundamentals with Python Examples"
- ✅ "World War II: Causes, Events, and Consequences"
- ❌ "Math" (too vague)

### Step 4: Generate & Download
- Watch real-time progress
- Stop anytime if needed
- Download professional PDF
- Resume failed generations automatically

## 🔧 Configuration

### API Keys
Configure API keys directly through the web interface:
1. Click "Manage API Keys" in the sidebar
2. Enter your API keys
3. Keys are automatically saved to `.env` file
4. Providers refresh automatically

### Custom Settings
Override profile defaults:
- **Content Depth**: 2-5 levels of detail
- **Section Length**: 100-1000 words per section
- **Quality Level**: 10-200 processing cycles

### Local Models Setup

#### Ollama
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Download models
ollama pull llama2
ollama pull mistral
ollama pull codellama

# Start server
ollama serve
```

#### LM Studio
1. Download from https://lmstudio.ai/
2. Install and start the application
3. Download models through the GUI
4. Start local server

## 📊 Generation Profiles Details

| Profile | Depth | Length | Iterations | Best For |
|---------|-------|--------|------------|----------|
| Elementary | 2 | 150 | 20 | Ages 6-11, Simple concepts |
| Middle School | 3 | 250 | 35 | Ages 12-14, Detailed explanations |
| High School | 3 | 350 | 50 | Ages 15-18, Exam preparation |
| College | 4 | 500 | 75 | University level, Research |
| Professional Quick | 2 | 200 | 25 | Busy professionals, Key points |
| Professional Detailed | 4 | 600 | 100 | Comprehensive documentation |
| Academic Research | 5 | 800 | 150 | Scholarly work, Citations |
| Creative Writing | 3 | 400 | 60 | Engaging content, Storytelling |

## 🔄 Resume Functionality

The system automatically detects failed generations and offers resume options:

### When Resume is Available
- Generation failed due to API limits
- Network interruption during generation
- Model timeout or error
- User stopped generation early

### Resume Process
1. **Automatic Detection**: System scans for incomplete generations
2. **Resume Prompt**: Shows failed generation details
3. **Continue Generation**: Picks up from last completed section
4. **Complete PDF**: Generates final document with all content

## 📁 File Organization

### Directory Structure
```
notes_output/
├── profile_name/
│   ├── topic_timestamp/
│   │   ├── content/           # Raw content files
│   │   │   ├── ch1_s1_intro.txt
│   │   │   ├── ch1_s2_basics.txt
│   │   │   └── ...
│   │   ├── pdfs/             # Generated PDFs
│   │   │   ├── topic_notes.pdf
│   │   │   └── topic_notes_resumed.pdf
│   │   └── state.json        # Generation state
│   └── ...
└── ...
```

### File Naming Convention
- **Directories**: `profile_name/topic_name_YYYYMMDD_HHMMSS/`
- **PDFs**: `topic_name_notes.pdf` or `topic_name_notes_resumed.pdf`
- **Content**: `ch{chapter}_s{section}_{title}.txt`

## 🛠️ Troubleshooting

### Common Issues

#### No AI Providers Available
- **Ollama**: Install and run `ollama serve`
- **LM Studio**: Start the application and local server
- **Cloud APIs**: Add API keys through web interface

#### Generation Fails
- Check API key validity
- Verify model availability
- Check network connection
- Use resume functionality for partial recovery

#### PDF Generation Issues
- Ensure content was generated successfully
- Check disk space for output directory
- Verify write permissions

### Error Recovery
1. **Failed Generations**: Use resume functionality
2. **API Limits**: Wait and resume, or switch providers
3. **Network Issues**: Resume when connection restored
4. **Model Errors**: Try different model or provider

## 🔒 Security & Privacy

### Local Processing
- **Ollama & LM Studio**: Complete privacy, no data leaves your machine
- **Local Storage**: All files stored locally
- **No Telemetry**: No usage data collected

### API Key Security
- **Local Storage**: Keys stored in `.env` file only
- **Masked Display**: Only last 4 characters shown
- **Secure Transmission**: HTTPS for API calls
- **No Logging**: Keys never logged or transmitted to third parties

## 🚀 Advanced Usage

### Multiple Concurrent Generations
- Generate multiple topics simultaneously
- Each generation has unique session ID
- Independent progress tracking
- Stop individual generations

### Custom Profile Creation
Modify `ultimate_notes_app.py` to add custom profiles:
```python
'custom_profile': {
    'name': 'Custom Profile',
    'description': 'Your custom description',
    'icon': '🎯',
    'color': '#your_color',
    'settings': {
        'max_depth': 3,
        'min_section_length': 400,
        'max_iterations': 60
    },
    'features': ['Feature 1', 'Feature 2'],
    'topics': ['Example Topic 1', 'Example Topic 2']
}
```

### Batch Processing
Use the API endpoints for automated generation:
```bash
# Start generation
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"provider":"ollama","model":"llama2","topic":"Your Topic","profile":"professional_detailed"}'

# Check status
curl http://localhost:5000/api/active-sessions
```

## 📈 Performance Tips

### Optimal Settings
- **Local Models**: Use smaller models for faster generation
- **Cloud Models**: Use for highest quality output
- **Concurrent Limit**: Max 3-4 simultaneous generations
- **Topic Specificity**: More specific topics = better results

### Resource Management
- **Memory**: 8GB+ RAM recommended for local models
- **Storage**: 1GB+ free space for outputs
- **Network**: Stable connection for cloud providers
- **CPU**: Multi-core recommended for concurrent generations

## 🤝 Contributing

### Development Setup
```bash
# Clone repository
git clone <repository_url>
cd ultimate-notes-generator

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python ultimate_notes_app.py
```

### Adding New Features
1. **New Profiles**: Add to `get_generation_profiles()`
2. **New Providers**: Extend provider detection
3. **UI Improvements**: Modify `templates/ultimate_interface.html`
4. **API Extensions**: Add new routes to `ultimate_notes_app.py`

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **AI Providers**: Ollama, LM Studio, Google Gemini, Mistral AI
- **Frontend**: Font Awesome icons, Socket.IO for real-time updates
- **Backend**: Flask, Flask-SocketIO for web framework
- **PDF Generation**: ReportLab for professional document creation

---

**🚀 Ready to generate amazing notes? Run `python run_ultimate_app.py` and start creating!**
