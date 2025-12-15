# Usage Guide

Complete guide for using the AI Note Generator system.

## Quick Start

### 1. Installation

```bash
# Clone repository
git clone <repository-url>
cd ai-note-generator

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### 2. First Run

```bash
python main.py
```

The system will:
1. Detect available model providers
2. Guide you through model selection
3. Ask for a topic
4. Generate comprehensive notes
5. Create a PDF document

## Detailed Walkthrough

### Step 1: Provider Selection

```
Available Model Providers:
┌───┬──────────────────┬──────────────┐
│ # │ Provider         │ Status       │
├───┼──────────────────┼──────────────┤
│ 1 │ Ollama (Local)   │ ✓ Available  │
│ 2 │ Google Gemini    │ ✓ Available  │
│ 3 │ Mistral AI       │ ✗ No API key │
└───┴──────────────────┴──────────────┘

Select provider: 1
```

**Tips**:
- Ollama is free but requires local installation
- Cloud providers (Gemini, Mistral) need API keys
- Cloud providers generally produce higher quality content

### Step 2: Model Selection

```
Available Models:
┌───┬─────────────────────┐
│ # │ Model Name          │
├───┼─────────────────────┤
│ 1 │ llama2              │
│ 2 │ mistral             │
│ 3 │ codellama           │
└───┴─────────────────────┘

Select model: 1
Selected: llama2
```

**Tips**:
- Larger models produce better content but are slower
- For technical topics, consider specialized models (codellama)
- For general topics, general-purpose models work well

### Step 3: Topic Input

```
Enter the topic for note generation: Machine Learning Fundamentals
```

**Tips**:
- Be specific but not too narrow
- Good: "Machine Learning Fundamentals"
- Too broad: "Computer Science"
- Too narrow: "Gradient descent learning rate optimization"

### Step 4: Generation Process

```
[Planner] Creating comprehensive outline for: Machine Learning Fundamentals
[Planner] Created outline with 45 nodes

[Iteration 1] Processing: Introduction to Machine Learning (chapter)
[Researcher] Researching...
[Researcher] Generated 823 words
[Reviewer] Reviewing quality...
[Reviewer] Quality score: 85/100
[Author] Polishing content...
[Author] Final content: 856 words
[Storage] Saved to: generated_notes/content/ch1_Introduction_to_Machine_Learning.txt
[Progress] 1/45 nodes (2.22%) - 856 total words

[Iteration 2] Processing: What is Machine Learning? (section)
...
```

**What's Happening**:
1. **Planner** creates a comprehensive outline
2. For each node:
   - **Researcher** generates detailed content
   - **Reviewer** checks quality
   - **Author** polishes the prose
   - **Storage** saves to disk
   - **Tracker** updates progress
3. Process continues until all nodes are complete

### Step 5: Completion Judgment

```
[Completion Judge] Evaluating completeness...
[Completion Judge] Complete: true
[Completion Judge] Ready for PDF: true
[Completion Judge] Reasoning: All 45 nodes covered with 25,340 total words. 
Content is comprehensive and meets book-quality standards.

[Orchestrator] Generation complete! Ready for PDF compilation.
```

### Step 6: PDF Generation

```
Generate PDF? [Y/n]: y

Generating PDF...
[PDF Generator] Creating PDF: generated_notes/Machine_Learning_Fundamentals_notes.pdf
[PDF Generator] Successfully created: generated_notes/Machine_Learning_Fundamentals_notes.pdf

PDF generated successfully!
Location: generated_notes/Machine_Learning_Fundamentals_notes.pdf
```

## Advanced Usage

### Resuming Interrupted Sessions

If generation is interrupted (Ctrl+C, crash, etc.):

```bash
python main.py
```

```
Found existing session:
  Topic: Machine Learning Fundamentals
  Model: llama2
  Status: in_progress

Resume this session? [Y/n]: y

[Orchestrator] Resuming session for: Machine Learning Fundamentals
[Progress] 23/45 nodes (51.11%) - 12,450 total words
...
```

**Benefits**:
- Never lose progress
- Can pause and resume anytime
- State is saved after each node

### Customizing Generation Parameters

Edit `config.yaml`:

```yaml
generation:
  max_depth: 5              # Outline depth (chapters → sections → subsections)
  min_section_length: 500   # Minimum words per section
  max_iterations: 100       # Safety limit (prevents infinite loops)
  expansion_threshold: 0.8  # Quality threshold for approval
```

**Parameters Explained**:

- **max_depth**: How deep the outline hierarchy goes
  - 3 = Chapters → Sections
  - 4 = Chapters → Sections → Subsections
  - 5 = Chapters → Sections → Subsections → Sub-subsections

- **min_section_length**: Minimum words per section
  - 300 = Brief coverage
  - 500 = Standard (recommended)
  - 1000 = Very detailed

- **max_iterations**: Maximum generation cycles
  - Prevents infinite loops
  - 100 = Default (sufficient for most topics)
  - Increase for very large topics

- **expansion_threshold**: Quality score threshold
  - 0.7 = More lenient (faster)
  - 0.8 = Balanced (recommended)
  - 0.9 = Very strict (slower, higher quality)

### Customizing PDF Output

Edit `config.yaml`:

```yaml
pdf:
  title_font_size: 24
  chapter_font_size: 18
  section_font_size: 14
  body_font_size: 11
  line_spacing: 1.5
  margin: 72  # Points (72 = 1 inch)
```

**Tips**:
- Larger fonts = easier to read, more pages
- Smaller margins = more content per page
- Line spacing affects readability

### Using Different Models Mid-Session

Currently not supported. To switch models:

1. Let current session complete or interrupt
2. Delete `generated_notes/session_state.json`
3. Start fresh with new model

**Future Enhancement**: Model switching will be supported.

## Common Workflows

### Workflow 1: Quick Overview

**Goal**: Fast, high-level overview of a topic

**Configuration**:
```yaml
generation:
  max_depth: 3
  min_section_length: 300
  max_iterations: 50
```

**Model**: Fast local model (llama2)

**Expected Output**: 5,000-10,000 words, 30-60 minutes

### Workflow 2: Comprehensive Book

**Goal**: Deep, exhaustive treatment suitable for publication

**Configuration**:
```yaml
generation:
  max_depth: 5
  min_section_length: 1000
  max_iterations: 200
```

**Model**: High-quality cloud model (Gemini Pro)

**Expected Output**: 50,000+ words, 3-6 hours

### Workflow 3: Technical Documentation

**Goal**: Precise technical reference

**Configuration**:
```yaml
generation:
  max_depth: 4
  min_section_length: 500
  max_iterations: 100
```

**Model**: Specialized model (codellama for code topics)

**Expected Output**: 20,000-30,000 words, 1-2 hours

## Troubleshooting

### Issue: "No providers available"

**Cause**: No model providers are configured

**Solution**:
1. For Ollama: Install and start Ollama service
   ```bash
   # Install from https://ollama.ai
   ollama serve
   ollama pull llama2
   ```

2. For Gemini: Add API key to `.env`
   ```
   GEMINI_API_KEY=your_key_here
   ```

3. For Mistral: Add API key to `.env`
   ```
   MISTRAL_API_KEY=your_key_here
   ```

### Issue: "Failed to list models"

**Cause**: Provider is configured but not accessible

**Solution**:
- **Ollama**: Check if service is running (`ollama serve`)
- **Gemini/Mistral**: Verify API key is correct
- Check network connectivity
- Check firewall settings

### Issue: Content is too short/shallow

**Cause**: Model producing brief responses

**Solution**:
1. Increase `min_section_length` in config
2. Use a more capable model
3. Adjust model temperature:
   ```python
   # In code (future enhancement)
   model.set_temperature(0.8)  # Higher = more creative
   ```

### Issue: Generation is too slow

**Cause**: Large topic, slow model, or high quality settings

**Solution**:
1. Use faster local model (Ollama)
2. Reduce `min_section_length`
3. Reduce `max_depth`
4. Use smaller model variant

### Issue: PDF generation fails

**Cause**: Missing dependencies or file permissions

**Solution**:
1. Ensure reportlab is installed:
   ```bash
   pip install reportlab
   ```
2. Check write permissions in output directory
3. Verify content files exist in `generated_notes/content/`

### Issue: Out of memory

**Cause**: Very large topic with many nodes

**Solution**:
1. Process in smaller chunks (split topic)
2. Reduce `max_depth`
3. Increase system RAM
4. Use streaming/chunking (future enhancement)

## Best Practices

### 1. Topic Selection

**Good Topics**:
- "Introduction to Quantum Computing"
- "Python Web Development with Django"
- "Financial Derivatives Trading"
- "Renaissance Art History"

**Avoid**:
- Too broad: "Science" (split into subtopics)
- Too narrow: "The third parameter of function X" (too specific)
- Ambiguous: "IT" (be more specific)

### 2. Model Selection

**For Technical Topics**:
- Use specialized models (codellama, deepseek-coder)
- Higher quality models (Gemini Pro, GPT-4)

**For General Topics**:
- General-purpose models work well
- Balance speed vs. quality

**For Cost Optimization**:
- Use local models (Ollama) when possible
- Reserve cloud models for final polish

### 3. Quality vs. Speed

**Prioritize Quality**:
- Increase `min_section_length`
- Use better models
- Higher `expansion_threshold`
- More review iterations

**Prioritize Speed**:
- Decrease `min_section_length`
- Use faster models
- Lower `expansion_threshold`
- Fewer depth levels

### 4. Monitoring Progress

**Watch For**:
- Quality scores consistently low → Switch model
- Content too short → Increase min_section_length
- Too many iterations → Topic may be too broad
- Slow progress → Consider faster model

### 5. Post-Generation

**Review**:
- Read generated PDF
- Check for gaps or errors
- Verify technical accuracy

**Refine**:
- Edit content files directly if needed
- Regenerate PDF with changes
- Consider re-running specific sections

## Tips and Tricks

### Tip 1: Batch Processing

Generate notes for multiple topics:

```bash
# Create a script
for topic in "Topic 1" "Topic 2" "Topic 3"; do
    echo "$topic" | python main.py
done
```

### Tip 2: Custom Outlines

Manually edit the outline after planning phase:

1. Interrupt after planning
2. Edit `generated_notes/session_state.json`
3. Modify outline structure
4. Resume generation

### Tip 3: Incremental Refinement

Generate quick draft, then refine:

1. First pass: Fast model, low quality settings
2. Review output
3. Second pass: Better model, higher quality settings
4. Focus on weak sections

### Tip 4: Combining Models

Use different models for different phases:

1. Planning: Fast model (quick outline)
2. Research: Specialized model (deep content)
3. Polish: High-quality model (final prose)

**Note**: Currently requires manual intervention; future enhancement.

### Tip 5: Content Reuse

Save generated content for future use:

- Content files are plain text
- Easy to edit and reuse
- Can be imported into other documents
- Version control friendly

## Performance Benchmarks

### Ollama (llama2, local)
- Speed: ~50 words/second
- Quality: 70/100
- Cost: Free
- Best for: Quick drafts, experimentation

### Google Gemini Pro
- Speed: ~30 words/second
- Quality: 90/100
- Cost: ~$0.50 per 10k words
- Best for: High-quality final output

### Mistral Large
- Speed: ~40 words/second
- Quality: 85/100
- Cost: ~$0.30 per 10k words
- Best for: Balanced quality and cost

**Note**: Benchmarks are approximate and vary by topic complexity.

## Getting Help

### Documentation
- `README.md` - Overview and quick start
- `ARCHITECTURE.md` - System design and internals
- `PROMPTS.md` - Agent prompts and behavior
- `USAGE_GUIDE.md` - This file

### Support
- GitHub Issues: Report bugs and request features
- Discussions: Ask questions and share tips
- Wiki: Community-contributed guides

### Contributing
- Fork repository
- Create feature branch
- Submit pull request
- Follow code style guidelines
