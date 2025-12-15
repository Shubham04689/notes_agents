# System Architecture

## Overview

The AI Note Generator is a production-ready, agent-based system designed to generate comprehensive, book-quality notes on any topic. The system follows a modular architecture with clear separation of concerns.

## Core Principles

1. **Agent-Based Design**: Six specialized agents work together, each with a specific role
2. **Model Agnostic**: Pluggable adapter pattern supports multiple LLM providers
3. **Persistent State**: All progress is saved incrementally to disk
4. **Error Recovery**: Graceful handling of failures with automatic resume capability
5. **Quality Assurance**: Multiple review stages ensure comprehensive coverage
6. **Iterative Expansion**: Never stops until topic is exhaustively covered

## System Components

### 1. Model Adapters (`src/models/`)

**Purpose**: Abstract LLM provider differences behind a common interface

**Components**:
- `BaseModelAdapter`: Abstract base class defining the interface
- `OllamaAdapter`: Local model support via Ollama
- `GeminiAdapter`: Google Gemini API integration
- `MistralAdapter`: Mistral AI API integration

**Key Features**:
- Auto-detection of available models
- Normalized input/output handling
- Token limit management
- Temperature and parameter control

**Extension Point**: Add new providers by implementing `BaseModelAdapter`

### 2. Agents (`src/agents/`)

**Purpose**: Specialized AI agents that perform specific tasks in the generation pipeline

#### PlannerAgent
- **Role**: Creates comprehensive hierarchical outlines
- **Input**: Topic string
- **Output**: JSON outline with chapters, sections, subsections
- **Behavior**: Thinks like a book author planning a 300+ page book

#### ResearcherAgent
- **Role**: Deep research and content expansion
- **Input**: Topic node, parent context, covered topics
- **Output**: Comprehensive content (minimum 500 words)
- **Behavior**: Provides exhaustive coverage with examples, theory, applications

#### AuthorAgent
- **Role**: Transforms research into polished prose
- **Input**: Raw research content
- **Output**: Book-quality, professionally written text
- **Behavior**: Improves clarity, flow, structure, and readability

#### CoverageTrackerAgent
- **Role**: Maintains perfect memory of progress
- **Input**: Actions (initialize, mark_complete, get_next, get_status)
- **Output**: Tracking state and status reports
- **Behavior**: Prevents duplication, tracks gaps, manages queue

#### ReviewerAgent
- **Role**: Quality assurance and completeness checking
- **Input**: Generated content
- **Output**: Approval/rejection with quality score and feedback
- **Behavior**: Demands excellence, rejects shallow content

#### CompletionJudgeAgent
- **Role**: Final arbiter of completeness
- **Input**: Full outline, coverage status, word count
- **Output**: Judgment on whether work is complete and ready for PDF
- **Behavior**: Extremely strict, only approves truly complete work

### 3. Core System (`src/core/`)

#### Orchestrator
- **Purpose**: Coordinates all agents in the generation pipeline
- **Responsibilities**:
  - Execute planning phase
  - Run iterative generation loop
  - Coordinate agent interactions
  - Enforce quality standards
  - Manage completion judgment

**Generation Loop**:
```
1. Get next pending node from tracker
2. Research node (ResearcherAgent)
3. Review quality (ReviewerAgent)
4. If rejected, re-research with deeper prompt
5. Polish content (AuthorAgent)
6. Save to storage
7. Update tracker
8. Repeat until all nodes complete
9. Judge completeness (CompletionJudgeAgent)
10. If approved, proceed to PDF generation
```

#### StorageManager
- **Purpose**: Manages file-based storage of generated content
- **Responsibilities**:
  - Save content incrementally to disk
  - Organize files by node ID and title
  - Maintain metadata
  - Provide content retrieval
  - Support PDF compilation

**Storage Structure**:
```
generated_notes/
├── content/
│   ├── ch1_Introduction.txt
│   ├── ch1_s1_Background.txt
│   └── ...
├── metadata.json
└── session_state.json
```

#### StateManager
- **Purpose**: Manages persistent session state
- **Responsibilities**:
  - Track covered and pending nodes
  - Maintain word count
  - Store outline and configuration
  - Enable session resume
  - Prevent data loss

**State Schema**:
```json
{
  "topic": "string",
  "model_name": "string",
  "outline": {},
  "covered_nodes": [],
  "pending_nodes": [],
  "covered_topics": [],
  "total_word_count": 0,
  "status": "in_progress|complete",
  "created_at": "ISO8601",
  "updated_at": "ISO8601"
}
```

### 4. PDF Generation (`src/pdf/`)

#### PDFGenerator
- **Purpose**: Compile content into professional PDF documents
- **Technology**: ReportLab library
- **Features**:
  - Title page with metadata
  - Table of contents
  - Hierarchical formatting (chapters, sections, subsections)
  - Professional typography
  - Proper spacing and margins
  - Markdown-to-PDF conversion

**PDF Structure**:
1. Title page
2. Table of contents
3. Chapters (with page breaks)
4. Sections (hierarchical)
5. Subsections (nested)
6. Body content (justified, proper line spacing)

### 5. User Interface (`src/ui/`)

#### CLI
- **Purpose**: Command-line interface for user interaction
- **Technology**: Rich library for beautiful terminal output
- **Features**:
  - Provider selection with availability detection
  - Model listing and selection
  - Topic input
  - Progress tracking
  - Session resume
  - PDF generation trigger

**User Flow**:
```
1. Check for existing session → Resume or New
2. Select provider (Ollama/Gemini/Mistral)
3. Select specific model
4. Enter topic
5. Watch generation progress
6. Approve PDF generation
7. Receive final PDF
```

## Data Flow

```
User Input (Topic)
    ↓
PlannerAgent → Outline
    ↓
Orchestrator Loop:
    ↓
CoverageTrackerAgent → Next Node
    ↓
ResearcherAgent → Raw Content
    ↓
ReviewerAgent → Quality Check
    ↓ (if approved)
AuthorAgent → Polished Content
    ↓
StorageManager → Save to Disk
    ↓
StateManager → Update State
    ↓
(Repeat until complete)
    ↓
CompletionJudgeAgent → Final Approval
    ↓
PDFGenerator → Final PDF
    ↓
User Output (PDF Document)
```

## Safety Mechanisms

### 1. Infinite Loop Prevention
- Maximum iteration limit (configurable)
- Progress tracking with automatic termination
- Completion judge as final gate

### 2. Data Loss Prevention
- Incremental saving after each node
- Persistent state on disk
- Resume capability from any point
- No in-memory-only data

### 3. Quality Assurance
- Minimum word count enforcement
- Multi-stage review process
- Automatic re-generation for shallow content
- Strict completion criteria

### 4. Error Handling
- Graceful API failure handling
- Model switching support
- Validation at every stage
- Clear error messages

### 5. Duplication Prevention
- Coverage tracker maintains history
- Covered topics passed to researcher
- Node ID-based tracking
- Prevents redundant content

## Configuration

### Application Config (`config.yaml`)
- Storage paths
- Generation parameters (depth, length, iterations)
- PDF formatting options
- Quality thresholds

### Environment Config (`.env`)
- API keys for cloud providers
- Service endpoints (Ollama host)
- Optional overrides

## Extension Points

### Adding New Model Providers
1. Implement `BaseModelAdapter`
2. Add to `src/models/__init__.py`
3. Update CLI provider selection
4. Add configuration options

### Adding New Agents
1. Extend `BaseAgent`
2. Implement `_get_system_prompt()` and `execute()`
3. Register in `src/agents/__init__.py`
4. Integrate into orchestrator workflow

### Adding New Output Formats
1. Create new generator in `src/pdf/` (or new module)
2. Implement content parsing and formatting
3. Add to CLI as option
4. Update orchestrator to support new format

### Adding Citations/Bibliography
1. Create `CitationAgent` extending `BaseAgent`
2. Track sources during research phase
3. Format citations in author phase
4. Add bibliography section to PDF

### Adding Web UI
1. Create `src/web/` module
2. Implement REST API or WebSocket server
3. Create frontend (React/Vue/etc.)
4. Reuse existing core components

## Performance Considerations

### Model Selection
- **Local (Ollama)**: Fast, free, but may produce shorter content
- **Cloud (Gemini/Mistral)**: Slower, costs money, but higher quality

### Optimization Strategies
- Adjust `min_section_length` for depth vs. speed tradeoff
- Lower `max_iterations` for faster (less complete) results
- Use faster models for initial drafts
- Switch to better models for final polish

### Scalability
- Current design: Single-threaded, sequential processing
- Future: Parallel node processing (independent sections)
- Future: Distributed agent execution
- Future: Caching and incremental updates

## Testing Strategy

### Unit Tests
- Model adapters (mocked API calls)
- Individual agents (mocked model responses)
- Storage manager (temporary directories)
- State manager (in-memory state)

### Integration Tests
- Full generation pipeline (small topic)
- Resume functionality
- PDF generation
- Error recovery

### Manual Testing
- Real model providers
- Complex topics
- Long-running sessions
- Edge cases (API failures, interruptions)

## Security Considerations

1. **API Keys**: Stored in `.env`, never committed to git
2. **File System**: Validates paths, prevents directory traversal
3. **Input Validation**: Sanitizes user input for filenames
4. **Resource Limits**: Max iterations, token limits, file size limits
5. **Error Messages**: No sensitive information in logs

## Future Enhancements

1. **Multi-language Support**: Generate notes in different languages
2. **Citation Management**: Automatic source tracking and bibliography
3. **Image Generation**: Diagrams and illustrations
4. **Collaborative Editing**: Human-in-the-loop refinement
5. **Version Control**: Track changes and iterations
6. **Export Formats**: EPUB, HTML, Markdown, LaTeX
7. **Web Interface**: Browser-based UI
8. **API Server**: RESTful API for programmatic access
9. **Batch Processing**: Generate multiple topics in parallel
10. **Quality Metrics**: Automated quality scoring and analytics
