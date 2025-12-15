# AI Note Generator - Web Interface

## 🌐 Simple Web Frontend

A beautiful, easy-to-use web interface for generating AI notes.

---

## ✨ Features

- **Beautiful UI** - Modern, gradient design
- **Real-time Progress** - Live updates during generation
- **4 Model Providers** - Ollama, LM Studio, Gemini, Mistral
- **Customizable Settings** - Adjust depth, length, iterations
- **One-Click Download** - Get your PDF instantly

---

## 🚀 Quick Start

### 1. Install Web Dependencies

```bash
pip install -r requirements_web.txt
```

### 2. Start the Web Server

```bash
python web_app.py
```

### 3. Open Your Browser

Navigate to: **http://localhost:5000**

---

## 🤖 Supported Model Providers

### 1. Ollama (Local, Free)
- **Setup**: Install from https://ollama.ai
- **Start**: `ollama serve`
- **Pull Model**: `ollama pull llama3.2:3b`
- **Benefits**: Free, no API key, runs locally

### 2. LM Studio (Local, Free) ⭐ NEW
- **Setup**: Install from https://lmstudio.ai
- **Start**: Open LM Studio → Start Server
- **Benefits**: Free, easy UI, runs locally, no API key

### 3. Google Gemini (Cloud)
- **Setup**: Get API key from https://makersuite.google.com/app/apikey
- **Config**: Add to `.env`: `GEMINI_API_KEY=your_key`
- **Benefits**: High quality, fast

### 4. Mistral AI (Cloud)
- **Setup**: Get API key from https://console.mistral.ai
- **Config**: Add to `.env`: `MISTRAL_API_KEY=your_key`
- **Benefits**: Fast, high quality, good limits

---

## 📖 How to Use

### Step 1: Select Provider
Choose from available providers (Ollama, LM Studio, Gemini, Mistral)

### Step 2: Select Model
Pick a specific model from the provider

### Step 3: Enter Topic
Type your topic (e.g., "Python Functions", "Machine Learning Basics")

### Step 4: Adjust Settings (Optional)
- **Outline Depth**: 2-5 (default: 3)
- **Min Words/Section**: 100-1000 (default: 250)
- **Max Iterations**: 5-100 (default: 20)

### Step 5: Generate
Click "Generate Notes" and watch the progress!

### Step 6: Download
Once complete, click "Download PDF" to get your notes

---

## 🎯 LM Studio Setup (Recommended for Beginners)

LM Studio is the easiest way to run local models with a GUI!

### Installation

1. **Download LM Studio**
   - Visit: https://lmstudio.ai
   - Download for your OS (Windows/Mac/Linux)
   - Install and open

2. **Download a Model**
   - Click "Search" tab
   - Search for: "llama-3.2-3b" or "mistral-7b"
   - Click download
   - Wait for download to complete

3. **Start the Server**
   - Click "Local Server" tab
   - Click "Start Server"
   - Default port: 1234
   - Server is now running!

4. **Use in Web Interface**
   - Open http://localhost:5000
   - Select "LM Studio (Local)"
   - Choose your downloaded model
   - Start generating!

### Why LM Studio?

- ✅ **Easy GUI** - No command line needed
- ✅ **Free** - No API costs
- ✅ **Fast** - Runs on your computer
- ✅ **Private** - Your data stays local
- ✅ **No API Key** - Just download and run
- ✅ **Multiple Models** - Download many models
- ✅ **Cross-Platform** - Works on Windows, Mac, Linux

---

## 🔧 Configuration

### Default Settings
```yaml
max_depth: 3              # Outline depth
min_section_length: 250   # Words per section
max_iterations: 20        # Max generation cycles
```

### Quick Generation (Fast)
```
Depth: 2
Min Words: 150
Max Iterations: 10
```

### Comprehensive (Detailed)
```
Depth: 4
Min Words: 500
Max Iterations: 50
```

---

## 📊 Generation Process

1. **Initializing** (10%) - Loading model
2. **Planning** (30%) - Creating outline
3. **Generating** (70%) - Writing content
4. **Creating PDF** (90%) - Compiling document
5. **Complete** (100%) - Ready to download!

---

## 🎨 Web Interface Features

### Real-Time Updates
- Live progress bar
- Status messages
- Stage indicators

### Beautiful Design
- Modern gradient theme
- Responsive layout
- Clean, intuitive UI

### Easy Configuration
- Dropdown menus
- Number inputs with validation
- Helpful descriptions

### Instant Download
- One-click PDF download
- No file management needed
- Direct browser download

---

## 🐛 Troubleshooting

### "No providers available"

**For Ollama:**
```bash
ollama serve
ollama pull llama3.2:3b
```

**For LM Studio:**
1. Open LM Studio
2. Go to "Local Server" tab
3. Click "Start Server"

**For Gemini/Mistral:**
- Check `.env` file has correct API keys

### "Failed to start generation"

- Check model is loaded
- Verify server is running
- Check console for errors

### "Connection refused"

- Ensure web server is running: `python web_app.py`
- Check port 5000 is not in use
- Try restarting the server

---

## 💡 Tips

### For Best Results

1. **Use LM Studio** - Easiest for beginners
2. **Start Small** - Test with simple topics first
3. **Adjust Settings** - Lower values = faster generation
4. **Local Models** - Free and unlimited
5. **Cloud Models** - Higher quality but costs money

### Recommended Models

**LM Studio/Ollama:**
- llama-3.2-3b (fast, good quality)
- mistral-7b (balanced)
- llama2 (reliable)

**Gemini:**
- gemini-pro (best quality)

**Mistral:**
- mistral-small-latest (fast)
- mistral-medium-latest (balanced)

---

## 📁 Output Location

Generated files are saved to:
```
./web_output/<topic_name>/
├── content/          # Individual sections
├── state.json        # Session state
└── <topic>_notes.pdf # Final PDF
```

---

## 🎉 Advantages Over CLI

- ✅ **No Command Line** - Just click buttons
- ✅ **Visual Progress** - See what's happening
- ✅ **Easy Settings** - Adjust with sliders
- ✅ **Instant Download** - One-click PDF
- ✅ **Beautiful UI** - Modern design
- ✅ **Real-Time Updates** - Live status
- ✅ **No File Management** - Automatic handling

---

## 🚀 Next Steps

1. **Install LM Studio** (recommended for beginners)
2. **Start Web Server**: `python web_app.py`
3. **Open Browser**: http://localhost:5000
4. **Generate Notes** on your favorite topic!

---

## 📞 Support

- **Documentation**: See README.md
- **CLI Version**: `python main.py`
- **Examples**: Check `demo_*.py` files

---

**Enjoy generating comprehensive notes with a beautiful web interface!** 🎊
