#!/usr/bin/env python3
"""
Ultimate AI Notes Generator - Complete Web Application
Features: Profile-based generation, API key management, resume functionality, real-time progress
"""

import os
import sys
import yaml
import json
import traceback
import time
import threading
import uuid
from datetime import datetime
from pathlib import Path
from threading import Thread, Event

from flask import Flask, render_template, request, jsonify, send_file, abort
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.models import OllamaAdapter, GeminiAdapter, MistralAdapter, LMStudioAdapter
from src.core import Orchestrator, StorageManager, StateManager
from src.pdf import PDFGenerator

# Load environment
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ultimate-notes-generator-2024'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", logger=False, engineio_logger=False)

# Load config
try:
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
except Exception as e:
    print(f"Warning: Could not load config.yaml: {e}")
    config = {
        'generation': {
            'max_iterations': 50,
            'min_section_length': 300,
            'max_depth': 3
        },
        'pdf': {
            'margin': 72,
            'title_font_size': 24,
            'chapter_font_size': 18,
            'section_font_size': 14,
            'body_font_size': 11,
            'line_spacing': 1.5
        }
    }

# Global state
active_generations = {}  # Track multiple generations by session ID
generation_history = []
stop_events = {}  # Stop events for each generation

class GenerationManager:
    """Manages generation sessions with stop functionality"""
    
    def __init__(self):
        self.sessions = {}
        self.lock = threading.Lock()
    
    def create_session(self, session_id, topic, provider, model, profile):
        """Create a new generation session"""
        with self.lock:
            self.sessions[session_id] = {
                'id': session_id,
                'topic': topic,
                'provider': provider,
                'model': model,
                'profile': profile,
                'status': 'starting',
                'progress': 0,
                'started': datetime.now().isoformat(),
                'stop_event': Event(),
                'thread': None
            }
            return self.sessions[session_id]
    
    def get_session(self, session_id):
        """Get session by ID"""
        with self.lock:
            return self.sessions.get(session_id)
    
    def stop_session(self, session_id):
        """Stop a generation session"""
        with self.lock:
            if session_id in self.sessions:
                self.sessions[session_id]['stop_event'].set()
                self.sessions[session_id]['status'] = 'stopping'
                return True
            return False
    
    def remove_session(self, session_id):
        """Remove completed session"""
        with self.lock:
            if session_id in self.sessions:
                del self.sessions[session_id]
    
    def get_active_sessions(self):
        """Get all active sessions"""
        with self.lock:
            return {k: v for k, v in self.sessions.items() 
                   if v['status'] not in ['completed', 'failed', 'stopped']}

generation_manager = GenerationManager()

def get_generation_profiles():
    """Get predefined generation profiles for different use cases"""
    profiles = {
        'student_elementary': {
            'name': 'Elementary Student',
            'description': 'Simple, easy-to-understand notes with basic concepts and visual examples',
            'icon': '🎒',
            'color': '#10b981',
            'settings': {
                'max_depth': 2,
                'min_section_length': 150,
                'max_iterations': 20
            },
            'features': ['Simple language', 'Visual examples', 'Basic concepts', 'Short sections'],
            'topics': [
                'Basic Math - Addition and Subtraction',
                'Science - Plants and Animals',
                'Geography - Countries and Capitals',
                'History - Ancient Civilizations'
            ]
        },
        'student_middle': {
            'name': 'Middle School Student',
            'description': 'Detailed notes with examples, practice questions, and clear explanations',
            'icon': '📚',
            'color': '#3b82f6',
            'settings': {
                'max_depth': 3,
                'min_section_length': 250,
                'max_iterations': 35
            },
            'features': ['Detailed explanations', 'Practice questions', 'Examples', 'Structured content'],
            'topics': [
                'Algebra - Linear Equations',
                'Biology - Cell Structure',
                'World History - Medieval Period',
                'Literature - Poetry Analysis'
            ]
        },
        'student_high': {
            'name': 'High School Student',
            'description': 'Comprehensive notes with advanced concepts, exam preparation, and analysis',
            'icon': '🎓',
            'color': '#8b5cf6',
            'settings': {
                'max_depth': 3,
                'min_section_length': 350,
                'max_iterations': 50
            },
            'features': ['Advanced concepts', 'Exam preparation', 'Critical analysis', 'Comprehensive coverage'],
            'topics': [
                'Calculus - Derivatives and Integrals',
                'Physics - Mechanics and Thermodynamics',
                'AP History - American Revolution',
                'Advanced Literature - Shakespeare'
            ]
        },
        'student_college': {
            'name': 'College/University',
            'description': 'In-depth academic notes with research, citations, and scholarly analysis',
            'icon': '🏛️',
            'color': '#f59e0b',
            'settings': {
                'max_depth': 4,
                'min_section_length': 500,
                'max_iterations': 75
            },
            'features': ['Research-based', 'Citations', 'Scholarly analysis', 'In-depth coverage'],
            'topics': [
                'Advanced Mathematics - Real Analysis',
                'Computer Science - Data Structures',
                'Psychology - Cognitive Behavioral Theory',
                'Economics - Macroeconomic Policy'
            ]
        },
        'professional_quick': {
            'name': 'Professional Quick Reference',
            'description': 'Concise, actionable notes for busy professionals and quick learning',
            'icon': '⚡',
            'color': '#ef4444',
            'settings': {
                'max_depth': 2,
                'min_section_length': 200,
                'max_iterations': 25
            },
            'features': ['Concise format', 'Actionable insights', 'Key points', 'Time-efficient'],
            'topics': [
                'Project Management - Agile Methodologies',
                'Marketing - Digital Strategies',
                'Finance - Investment Basics',
                'Leadership - Team Management'
            ]
        },
        'professional_detailed': {
            'name': 'Professional Comprehensive',
            'description': 'Detailed professional documentation with best practices and case studies',
            'icon': '💼',
            'color': '#6366f1',
            'settings': {
                'max_depth': 4,
                'min_section_length': 600,
                'max_iterations': 100
            },
            'features': ['Best practices', 'Case studies', 'Detailed analysis', 'Professional insights'],
            'topics': [
                'Software Architecture - Design Patterns',
                'Business Strategy - Market Analysis',
                'Data Science - Machine Learning',
                'Cybersecurity - Risk Management'
            ]
        },
        'research_academic': {
            'name': 'Academic Research',
            'description': 'Scholarly notes with citations, methodology, and comprehensive analysis',
            'icon': '🔬',
            'color': '#059669',
            'settings': {
                'max_depth': 5,
                'min_section_length': 800,
                'max_iterations': 150
            },
            'features': ['Citations', 'Methodology', 'Comprehensive analysis', 'Academic rigor'],
            'topics': [
                'Research Methods - Quantitative Analysis',
                'Literature Review - Systematic Approach',
                'Statistical Analysis - Advanced Methods',
                'Academic Writing - Publication Standards'
            ]
        },
        'creative_writing': {
            'name': 'Creative & Writing',
            'description': 'Creative and engaging notes with storytelling and narrative elements',
            'icon': '✍️',
            'color': '#ec4899',
            'settings': {
                'max_depth': 3,
                'min_section_length': 400,
                'max_iterations': 60
            },
            'features': ['Storytelling', 'Narrative elements', 'Creative examples', 'Engaging content'],
            'topics': [
                'Creative Writing - Character Development',
                'Storytelling - Narrative Techniques',
                'Content Creation - Engaging Audiences',
                'Communication - Persuasive Writing'
            ]
        }
    }
    
    return profiles

def get_available_providers():
    """Get list of available model providers with detailed status"""
    providers = []
    
    # Check Ollama
    try:
        ollama = OllamaAdapter()
        if ollama.is_available():
            models = ollama.list_models()
            providers.append({
                'id': 'ollama',
                'name': 'Ollama',
                'type': 'local',
                'status': 'available',
                'models': models,
                'description': f'{len(models)} local models - Free, private, unlimited',
                'icon': '🏠',
                'color': '#2563eb',
                'recommended_for': 'Privacy-focused users, unlimited usage'
            })
        else:
            providers.append({
                'id': 'ollama',
                'name': 'Ollama',
                'type': 'local',
                'status': 'unavailable',
                'models': [],
                'description': 'Install Ollama for free, private AI models',
                'icon': '🏠',
                'color': '#6b7280',
                'recommended_for': 'Users who want privacy and unlimited usage'
            })
    except Exception as e:
        providers.append({
            'id': 'ollama',
            'name': 'Ollama',
            'type': 'local',
            'status': 'error',
            'models': [],
            'description': f'Error: {str(e)}',
            'icon': '🏠',
            'color': '#dc2626',
            'recommended_for': 'Troubleshooting needed'
        })
    
    # Check LM Studio
    try:
        lmstudio = LMStudioAdapter()
        if lmstudio.is_available():
            models = lmstudio.list_models()
            providers.append({
                'id': 'lmstudio',
                'name': 'LM Studio',
                'type': 'local',
                'status': 'available',
                'models': models,
                'description': f'{len(models)} local models - User-friendly interface',
                'icon': '🖥️',
                'color': '#059669',
                'recommended_for': 'Users who prefer GUI-based model management'
            })
        else:
            providers.append({
                'id': 'lmstudio',
                'name': 'LM Studio',
                'type': 'local',
                'status': 'unavailable',
                'models': [],
                'description': 'Install LM Studio for easy local AI models',
                'icon': '🖥️',
                'color': '#6b7280',
                'recommended_for': 'Users who want easy-to-use local models'
            })
    except Exception as e:
        providers.append({
            'id': 'lmstudio',
            'name': 'LM Studio',
            'type': 'local',
            'status': 'error',
            'models': [],
            'description': f'Error: {str(e)}',
            'icon': '🖥️',
            'color': '#dc2626',
            'recommended_for': 'Troubleshooting needed'
        })
    
    # Check Gemini
    gemini_key = os.getenv('GEMINI_API_KEY')
    if gemini_key and gemini_key != 'your_gemini_api_key_here':
        try:
            gemini = GeminiAdapter()
            if gemini.is_available():
                models = gemini.list_models()
                providers.append({
                    'id': 'gemini',
                    'name': 'Google Gemini',
                    'type': 'cloud',
                    'status': 'available',
                    'models': models[:15],
                    'description': f'{len(models)} cloud models - High quality, fast',
                    'icon': '🌟',
                    'color': '#7c3aed',
                    'recommended_for': 'Users needing highest quality content'
                })
            else:
                providers.append({
                    'id': 'gemini',
                    'name': 'Google Gemini',
                    'type': 'cloud',
                    'status': 'unavailable',
                    'models': [],
                    'description': 'API key configured but service unavailable',
                    'icon': '🌟',
                    'color': '#6b7280',
                    'recommended_for': 'High-quality content generation'
                })
        except Exception as e:
            providers.append({
                'id': 'gemini',
                'name': 'Google Gemini',
                'type': 'cloud',
                'status': 'error',
                'models': [],
                'description': f'Error: {str(e)}',
                'icon': '🌟',
                'color': '#dc2626',
                'recommended_for': 'Troubleshooting needed'
            })
    else:
        providers.append({
            'id': 'gemini',
            'name': 'Google Gemini',
            'type': 'cloud',
            'status': 'no_key',
            'models': [],
            'description': 'Add API key for premium AI models',
            'icon': '🌟',
            'color': '#6b7280',
            'recommended_for': 'Users with API access for premium quality'
        })
    
    # Check Mistral
    mistral_key = os.getenv('MISTRAL_API_KEY')
    if mistral_key and mistral_key != 'your_mistral_api_key_here':
        try:
            mistral = MistralAdapter()
            if mistral.is_available():
                models = mistral.list_models()
                providers.append({
                    'id': 'mistral',
                    'name': 'Mistral AI',
                    'type': 'cloud',
                    'status': 'available',
                    'models': models[:15],
                    'description': f'{len(models)} cloud models - Fast, efficient',
                    'icon': '⚡',
                    'color': '#ea580c',
                    'recommended_for': 'Users needing fast, efficient generation'
                })
            else:
                providers.append({
                    'id': 'mistral',
                    'name': 'Mistral AI',
                    'type': 'cloud',
                    'status': 'unavailable',
                    'models': [],
                    'description': 'API key configured but service unavailable',
                    'icon': '⚡',
                    'color': '#6b7280',
                    'recommended_for': 'Fast, efficient content generation'
                })
        except Exception as e:
            providers.append({
                'id': 'mistral',
                'name': 'Mistral AI',
                'type': 'cloud',
                'status': 'error',
                'models': [],
                'description': f'Error: {str(e)}',
                'icon': '⚡',
                'color': '#dc2626',
                'recommended_for': 'Troubleshooting needed'
            })
    else:
        providers.append({
            'id': 'mistral',
            'name': 'Mistral AI',
            'type': 'cloud',
            'status': 'no_key',
            'models': [],
            'description': 'Add API key for fast AI models',
            'icon': '⚡',
            'color': '#6b7280',
            'recommended_for': 'Users with API access for fast generation'
        })
    
    return providers

def create_topic_directory(topic, profile_name):
    """Create organized directory structure for topic"""
    # Sanitize topic name for filesystem
    safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_topic = safe_topic.replace(' ', '_')
    
    # Create timestamp for uniqueness
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create directory structure with profile
    base_dir = f"./notes_output/{profile_name}/{safe_topic}_{timestamp}"
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(f"{base_dir}/content", exist_ok=True)
    os.makedirs(f"{base_dir}/pdfs", exist_ok=True)
    
    return base_dir

# Routes
@app.route('/')
def index():
    """Serve the main page"""
    return render_template('ultimate_interface.html')

@app.route('/api/profiles', methods=['GET'])
def get_profiles():
    """Get available generation profiles"""
    try:
        profiles = get_generation_profiles()
        return jsonify({'profiles': profiles})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/providers', methods=['GET'])
def get_providers():
    """Get available model providers"""
    try:
        providers = get_available_providers()
        available_count = len([p for p in providers if p['status'] == 'available'])
        return jsonify({
            'providers': providers,
            'available_count': available_count,
            'total_count': len(providers)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/api-keys', methods=['GET'])
def get_api_keys():
    """Get current API key status (without revealing actual keys)"""
    try:
        gemini_key = os.getenv('GEMINI_API_KEY', '')
        mistral_key = os.getenv('MISTRAL_API_KEY', '')
        ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        
        return jsonify({
            'keys': {
                'gemini': {
                    'configured': bool(gemini_key and gemini_key != 'your_gemini_api_key_here'),
                    'masked': '***' + gemini_key[-4:] if gemini_key and len(gemini_key) > 4 and gemini_key != 'your_gemini_api_key_here' else '',
                    'placeholder': 'Enter your Google Gemini API key'
                },
                'mistral': {
                    'configured': bool(mistral_key and mistral_key != 'your_mistral_api_key_here'),
                    'masked': '***' + mistral_key[-4:] if mistral_key and len(mistral_key) > 4 and mistral_key != 'your_mistral_api_key_here' else '',
                    'placeholder': 'Enter your Mistral AI API key'
                },
                'ollama': {
                    'configured': bool(ollama_host),
                    'value': ollama_host,
                    'placeholder': 'http://localhost:11434'
                }
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/api-keys', methods=['POST'])
def update_api_keys():
    """Update API keys and save to .env file"""
    try:
        data = request.json
        keys = data.get('keys', {})
        
        # Read current .env file
        env_path = '.env'
        env_vars = {}
        
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()
        
        # Update with new values
        if 'gemini' in keys and keys['gemini'].strip():
            env_vars['GEMINI_API_KEY'] = keys['gemini'].strip()
        
        if 'mistral' in keys and keys['mistral'].strip():
            env_vars['MISTRAL_API_KEY'] = keys['mistral'].strip()
        
        if 'ollama' in keys and keys['ollama'].strip():
            env_vars['OLLAMA_HOST'] = keys['ollama'].strip()
        
        # Write back to .env file
        with open(env_path, 'w') as f:
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")
        
        # Reload environment variables
        load_dotenv(override=True)
        
        return jsonify({
            'success': True,
            'message': 'API keys updated successfully. Please refresh providers to see changes.'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get generation history"""
    return jsonify({'history': generation_history[-20:]})  # Last 20 generations

@app.route('/api/active-sessions', methods=['GET'])
def get_active_sessions():
    """Get currently active generation sessions"""
    sessions = generation_manager.get_active_sessions()
    
    # Create JSON-serializable version of sessions
    serializable_sessions = []
    for session in sessions.values():
        serializable_session = {
            'id': session['id'],
            'topic': session['topic'],
            'provider': session['provider'],
            'model': session['model'],
            'profile': session['profile'],
            'status': session['status'],
            'progress': session['progress'],
            'started': session['started']
        }
        serializable_sessions.append(serializable_session)
    
    return jsonify({'sessions': serializable_sessions})

@app.route('/api/resumable', methods=['GET'])
def get_resumable_generation():
    """Check if there's a resumable generation available"""
    try:
        # Look for the most recent failed or incomplete generation
        resumable = None
        
        for entry in reversed(generation_history):
            # Check if generation failed or was incomplete
            if (not entry.get('success', False) and 
                entry.get('error') and 
                'state_file' in entry and 
                os.path.exists(entry['state_file'])):
                
                # Check if state file indicates incomplete generation
                try:
                    with open(entry['state_file'], 'r') as f:
                        state_data = json.load(f)
                    
                    # If there's an active session with partial progress
                    if (state_data.get('active') and 
                        state_data.get('covered_nodes') and
                        len(state_data.get('covered_nodes', [])) > 0):
                        
                        resumable = {
                            'id': entry.get('id'),
                            'topic': entry['topic'],
                            'provider': entry['provider'],
                            'model': entry['model'],
                            'profile': entry.get('profile', 'unknown'),
                            'error': entry['error'],
                            'timestamp': entry['timestamp'],
                            'progress': len(state_data.get('covered_nodes', [])),
                            'total_nodes': len(state_data.get('outline', {}).get('children', [])),
                            'state_file': entry['state_file'],
                            'base_dir': entry.get('base_dir')
                        }
                        break
                        
                except Exception as e:
                    print(f"Error reading state file {entry['state_file']}: {e}")
                    continue
        
        return jsonify({
            'resumable': resumable is not None,
            'generation': resumable
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def start_generation():
    """Start note generation"""
    data = request.json
    
    provider_id = data.get('provider')
    model_name = data.get('model')
    topic = data.get('topic', '').strip()
    profile_id = data.get('profile')
    custom_settings = data.get('settings', {})
    
    if not all([provider_id, model_name, topic, profile_id]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if len(topic) < 3:
        return jsonify({'error': 'Topic must be at least 3 characters long'}), 400
    
    # Get profile
    profiles = get_generation_profiles()
    if profile_id not in profiles:
        return jsonify({'error': 'Invalid profile selected'}), 400
    
    profile = profiles[profile_id]
    
    # Create unique session ID
    session_id = str(uuid.uuid4())
    
    # Create generation session
    session = generation_manager.create_session(session_id, topic, provider_id, model_name, profile_id)
    
    # Start generation in background thread
    thread = Thread(target=generate_notes, args=(session_id, provider_id, model_name, topic, profile, custom_settings))
    thread.daemon = True
    session['thread'] = thread
    thread.start()
    
    return jsonify({
        'status': 'started', 
        'message': 'Generation started successfully',
        'session_id': session_id
    })

@app.route('/api/resume', methods=['POST'])
def resume_generation():
    """Resume a previous failed generation"""
    data = request.json
    generation_id = data.get('generation_id')
    
    if not generation_id:
        return jsonify({'error': 'Missing generation_id'}), 400
    
    # Find the generation to resume
    resumable_gen = None
    for entry in generation_history:
        if entry.get('id') == generation_id:
            resumable_gen = entry
            break
    
    if not resumable_gen:
        return jsonify({'error': 'Generation not found'}), 404
    
    if not resumable_gen.get('state_file') or not os.path.exists(resumable_gen['state_file']):
        return jsonify({'error': 'State file not found - cannot resume'}), 400
    
    # Create unique session ID for resume
    session_id = str(uuid.uuid4())
    
    # Get profile
    profiles = get_generation_profiles()
    profile_id = resumable_gen.get('profile', 'professional_detailed')
    profile = profiles.get(profile_id, profiles['professional_detailed'])
    
    # Create generation session for resume
    session = generation_manager.create_session(
        session_id, 
        resumable_gen['topic'], 
        resumable_gen['provider'], 
        resumable_gen['model'],
        profile_id
    )
    
    # Start resume in background thread
    thread = Thread(target=resume_notes_generation, args=(session_id, resumable_gen, profile))
    thread.daemon = True
    session['thread'] = thread
    thread.start()
    
    return jsonify({
        'status': 'resumed', 
        'message': 'Resuming generation from previous state',
        'session_id': session_id
    })

@app.route('/api/stop/<session_id>', methods=['POST'])
def stop_generation(session_id):
    """Stop a specific generation"""
    if generation_manager.stop_session(session_id):
        socketio.emit('stopped', {
            'session_id': session_id,
            'message': 'Generation stopped by user'
        })
        return jsonify({'status': 'stopped', 'message': 'Generation stopped successfully'})
    else:
        return jsonify({'error': 'Session not found or already completed'}), 404

@app.route('/api/download/<path:filename>')
def download_file(filename):
    """Download generated PDF"""
    try:
        # Security check - ensure file is in notes_output directory
        if not filename.startswith('./notes_output/'):
            filename = f'./notes_output/{filename}'
        
        if not os.path.exists(filename):
            abort(404)
        
        return send_file(filename, as_attachment=True)
    except Exception as e:
        print(f"Download error: {e}")
        abort(404)

@app.route('/api/files')
def list_files():
    """List generated files organized by profile and topic"""
    try:
        profiles = {}
        notes_output_dir = './notes_output'
        
        if os.path.exists(notes_output_dir):
            for profile_dir in os.listdir(notes_output_dir):
                profile_path = os.path.join(notes_output_dir, profile_dir)
                if os.path.isdir(profile_path):
                    profiles[profile_dir] = {}
                    
                    for topic_dir in os.listdir(profile_path):
                        topic_path = os.path.join(profile_path, topic_dir)
                        if os.path.isdir(topic_path):
                            # Extract topic name (remove timestamp)
                            topic_name = topic_dir.rsplit('_', 2)[0].replace('_', ' ')
                            
                            if topic_name not in profiles[profile_dir]:
                                profiles[profile_dir][topic_name] = []
                            
                            # Look for PDFs in this topic directory
                            pdf_dir = os.path.join(topic_path, 'pdfs')
                            if os.path.exists(pdf_dir):
                                for filename in os.listdir(pdf_dir):
                                    if filename.endswith('.pdf'):
                                        filepath = os.path.join(pdf_dir, filename)
                                        stat = os.stat(filepath)
                                        profiles[profile_dir][topic_name].append({
                                            'name': filename,
                                            'path': filepath,
                                            'size': stat.st_size,
                                            'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                                            'topic_dir': topic_dir
                                        })
        
        return jsonify({'profiles': profiles})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def resume_notes_generation(session_id, resumable_gen, profile):
    """Resume a failed generation from its previous state"""
    global generation_history
    
    session = generation_manager.get_session(session_id)
    if not session:
        return
    
    stop_event = session['stop_event']
    start_time = time.time()
    
    try:
        topic = resumable_gen['topic']
        provider_id = resumable_gen['provider']
        model_name = resumable_gen['model']
        state_file = resumable_gen['state_file']
        base_dir = resumable_gen['base_dir']
        
        # Update stage
        session['status'] = 'resuming'
        session['progress'] = 10
        socketio.emit('status', {
            'session_id': session_id,
            'stage': 'resuming', 
            'message': f'Resuming generation from previous state...',
            'progress': 10
        })
        
        # Check for stop
        if stop_event.is_set():
            raise InterruptedError("Generation stopped by user")
        
        # Initialize model
        model = None
        try:
            if provider_id == 'ollama':
                model = OllamaAdapter()
            elif provider_id == 'lmstudio':
                model = LMStudioAdapter()
            elif provider_id == 'gemini':
                model = GeminiAdapter()
            elif provider_id == 'mistral':
                model = MistralAdapter()
            else:
                raise ValueError(f'Unknown provider: {provider_id}')
            
            model.set_model(model_name)
            
            if not model.is_available():
                raise RuntimeError(f'{provider_id} is not available')
                
        except Exception as e:
            socketio.emit('error', {
                'session_id': session_id,
                'message': f'Failed to initialize {provider_id}: {str(e)}'
            })
            return
        
        # Check for stop
        if stop_event.is_set():
            raise InterruptedError("Generation stopped by user")
        
        # Apply profile settings
        gen_config = config.get('generation', {}).copy()
        gen_config.update(profile['settings'])
        
        # Setup storage and state with existing files
        storage = StorageManager(base_dir)
        state = StateManager(state_file)
        orchestrator = Orchestrator(model, storage, state, gen_config)
        
        session['status'] = 'resuming_generation'
        session['progress'] = 25
        socketio.emit('status', {
            'session_id': session_id,
            'stage': 'resuming_generation', 
            'message': 'Continuing from where we left off...',
            'progress': 25
        })
        
        # Check for stop
        if stop_event.is_set():
            raise InterruptedError("Generation stopped by user")
        
        # Resume generation
        result = orchestrator.generate_notes(topic, resume=True)
        
        # Check for stop
        if stop_event.is_set():
            raise InterruptedError("Generation stopped by user")
        
        if result['success']:
            session['status'] = 'generating_pdf'
            session['progress'] = 90
            socketio.emit('status', {
                'session_id': session_id,
                'stage': 'generating_pdf', 
                'message': 'Creating professional PDF with table of contents...',
                'progress': 90
            })
            
            # Generate PDF
            pdf_gen = PDFGenerator(config)
            content_files = storage.get_all_content_files()
            
            if not content_files:
                raise RuntimeError('No content files generated')
            
            # Create PDF in organized directory
            pdf_filename = f"{topic.replace(' ', '_')}_notes_resumed.pdf"
            pdf_path = os.path.join(base_dir, 'pdfs', pdf_filename)
            
            metadata = {
                'model': f'{provider_id}/{model_name}',
                'profile': profile['name'],
                'total_word_count': result.get('total_word_count', 0),
                'generation_time': time.time() - start_time,
                'settings': gen_config,
                'topic': topic,
                'generated_date': datetime.now().isoformat(),
                'resumed': True,
                'original_error': resumable_gen.get('error', 'Unknown error')
            }
            
            pdf_gen.generate(topic, content_files, pdf_path, metadata)
            
            # Calculate final stats
            end_time = time.time()
            duration = end_time - start_time
            
            # Update history entry
            for entry in generation_history:
                if entry.get('id') == resumable_gen['id']:
                    entry.update({
                        'word_count': result.get('total_word_count', 0),
                        'sections': len(content_files),
                        'duration': duration,
                        'pdf_path': pdf_path,
                        'success': True,
                        'resumed': True,
                        'resume_timestamp': datetime.now().isoformat()
                    })
                    break
            
            # Success response
            session['status'] = 'completed'
            session['progress'] = 100
            socketio.emit('complete', {
                'session_id': session_id,
                'message': 'Generation resumed and completed successfully!',
                'word_count': result.get('total_word_count', 0),
                'pdf_path': pdf_path,
                'sections': len(content_files),
                'duration': f"{duration:.1f}s",
                'model': f'{provider_id}/{model_name}',
                'profile': profile['name'],
                'progress': 100,
                'base_dir': base_dir,
                'resumed': True
            })
            
        else:
            error_msg = result.get('error', 'Resume failed for unknown reason')
            raise RuntimeError(error_msg)
    
    except InterruptedError:
        # Handle stop request
        session['status'] = 'stopped'
        generation_entry = {
            'id': session_id,
            'topic': topic,
            'provider': provider_id,
            'model': model_name,
            'profile': profile.get('name', 'Unknown'),
            'error': 'Stopped by user during resume',
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'stopped': True
        }
        generation_history.append(generation_entry)
        
        socketio.emit('stopped', {
            'session_id': session_id,
            'message': 'Resume stopped by user request'
        })
    
    except Exception as e:
        error_msg = str(e)
        print(f"Resume error: {error_msg}")
        print(traceback.format_exc())
        
        session['status'] = 'failed'
        generation_entry = {
            'id': session_id,
            'topic': topic,
            'provider': provider_id,
            'model': model_name,
            'profile': profile.get('name', 'Unknown'),
            'error': f'Resume failed: {error_msg}',
            'timestamp': datetime.now().isoformat(),
            'success': False
        }
        generation_history.append(generation_entry)
        
        socketio.emit('error', {
            'session_id': session_id,
            'message': f'Resume failed: {error_msg}',
            'details': 'The generation could not be resumed from the previous state'
        })
    
    finally:
        # Clean up session
        generation_manager.remove_session(session_id)

def generate_notes(session_id, provider_id, model_name, topic, profile, custom_settings):
    """Generate notes in background with stop functionality"""
    global generation_history
    
    session = generation_manager.get_session(session_id)
    if not session:
        return
    
    stop_event = session['stop_event']
    start_time = time.time()
    
    try:
        # Update stage
        session['status'] = 'initializing'
        session['progress'] = 5
        socketio.emit('status', {
            'session_id': session_id,
            'stage': 'initializing', 
            'message': f'Initializing {provider_id} model: {model_name}...',
            'progress': 5
        })
        
        # Check for stop
        if stop_event.is_set():
            raise InterruptedError("Generation stopped by user")
        
        # Initialize model
        model = None
        try:
            if provider_id == 'ollama':
                model = OllamaAdapter()
            elif provider_id == 'lmstudio':
                model = LMStudioAdapter()
            elif provider_id == 'gemini':
                model = GeminiAdapter()
            elif provider_id == 'mistral':
                model = MistralAdapter()
            else:
                raise ValueError(f'Unknown provider: {provider_id}')
            
            model.set_model(model_name)
            
            if not model.is_available():
                raise RuntimeError(f'{provider_id} is not available')
                
        except Exception as e:
            socketio.emit('error', {
                'session_id': session_id,
                'message': f'Failed to initialize {provider_id}: {str(e)}'
            })
            return
        
        # Check for stop
        if stop_event.is_set():
            raise InterruptedError("Generation stopped by user")
        
        # Apply profile settings with custom overrides
        gen_config = config.get('generation', {}).copy()
        gen_config.update(profile['settings'])
        
        # Apply custom settings if provided
        if custom_settings:
            if 'max_depth' in custom_settings:
                gen_config['max_depth'] = max(2, min(5, int(custom_settings['max_depth'])))
            if 'min_section_length' in custom_settings:
                gen_config['min_section_length'] = max(100, min(2000, int(custom_settings['min_section_length'])))
            if 'max_iterations' in custom_settings:
                gen_config['max_iterations'] = max(5, min(200, int(custom_settings['max_iterations'])))
        
        # Create organized directory structure
        base_dir = create_topic_directory(topic, profile['name'].lower().replace(' ', '_'))
        state_file = os.path.join(base_dir, "state.json")
        
        storage = StorageManager(base_dir)
        state = StateManager(state_file)
        orchestrator = Orchestrator(model, storage, state, gen_config)
        
        # Update progress
        session['status'] = 'planning'
        session['progress'] = 15
        socketio.emit('status', {
            'session_id': session_id,
            'stage': 'planning', 
            'message': 'Creating comprehensive outline...',
            'progress': 15
        })
        
        # Check for stop
        if stop_event.is_set():
            raise InterruptedError("Generation stopped by user")
        
        # Update progress during generation
        session['status'] = 'generating'
        session['progress'] = 30
        socketio.emit('status', {
            'session_id': session_id,
            'stage': 'generating', 
            'message': f'Researching and writing content using {profile["name"]} profile...',
            'progress': 30
        })
        
        # Generate notes
        result = orchestrator.generate_notes(topic, resume=False)
        
        # Check for stop one more time
        if stop_event.is_set():
            raise InterruptedError("Generation stopped by user")
        
        if result['success']:
            session['status'] = 'generating_pdf'
            session['progress'] = 90
            socketio.emit('status', {
                'session_id': session_id,
                'stage': 'generating_pdf', 
                'message': 'Creating professional PDF with table of contents...',
                'progress': 90
            })
            
            # Generate PDF
            pdf_gen = PDFGenerator(config)
            content_files = storage.get_all_content_files()
            
            if not content_files:
                raise RuntimeError('No content files generated')
            
            # Create PDF in organized directory
            pdf_filename = f"{topic.replace(' ', '_')}_notes.pdf"
            pdf_path = os.path.join(base_dir, 'pdfs', pdf_filename)
            
            metadata = {
                'model': f'{provider_id}/{model_name}',
                'profile': profile['name'],
                'total_word_count': result.get('total_word_count', 0),
                'generation_time': time.time() - start_time,
                'settings': gen_config,
                'topic': topic,
                'generated_date': datetime.now().isoformat()
            }
            
            pdf_gen.generate(topic, content_files, pdf_path, metadata)
            
            # Calculate final stats
            end_time = time.time()
            duration = end_time - start_time
            
            # Add to history
            generation_entry = {
                'id': session_id,
                'topic': topic,
                'provider': provider_id,
                'model': model_name,
                'profile': profile['name'],
                'word_count': result.get('total_word_count', 0),
                'sections': len(content_files),
                'duration': duration,
                'timestamp': datetime.now().isoformat(),
                'pdf_path': pdf_path,
                'base_dir': base_dir,
                'state_file': state_file,
                'success': True
            }
            generation_history.append(generation_entry)
            
            # Success response
            session['status'] = 'completed'
            session['progress'] = 100
            socketio.emit('complete', {
                'session_id': session_id,
                'message': 'Generation completed successfully!',
                'word_count': result.get('total_word_count', 0),
                'pdf_path': pdf_path,
                'sections': len(content_files),
                'duration': f"{duration:.1f}s",
                'model': f'{provider_id}/{model_name}',
                'profile': profile['name'],
                'progress': 100,
                'base_dir': base_dir
            })
            
        else:
            error_msg = result.get('error', 'Generation failed for unknown reason')
            raise RuntimeError(error_msg)
    
    except InterruptedError:
        # Handle stop request
        session['status'] = 'stopped'
        generation_entry = {
            'id': session_id,
            'topic': topic,
            'provider': provider_id,
            'model': model_name,
            'profile': profile['name'],
            'error': 'Stopped by user',
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'stopped': True
        }
        generation_history.append(generation_entry)
        
        socketio.emit('stopped', {
            'session_id': session_id,
            'message': 'Generation stopped by user request'
        })
    
    except Exception as e:
        error_msg = str(e)
        print(f"Generation error: {error_msg}")
        print(traceback.format_exc())
        
        session['status'] = 'failed'
        generation_entry = {
            'id': session_id,
            'topic': topic,
            'provider': provider_id,
            'model': model_name,
            'profile': profile['name'],
            'error': error_msg,
            'timestamp': datetime.now().isoformat(),
            'state_file': locals().get('state_file'),
            'base_dir': locals().get('base_dir'),
            'success': False
        }
        generation_history.append(generation_entry)
        
        socketio.emit('error', {
            'session_id': session_id,
            'message': f'Generation failed: {error_msg}',
            'details': 'Check console for more details'
        })
    
    finally:
        # Clean up session
        generation_manager.remove_session(session_id)

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {'message': 'Connected to Ultimate Notes Generator'})

if __name__ == '__main__':
    print("🚀 Ultimate AI Notes Generator - Complete System")
    print("=" * 70)
    print("✅ Profile-based generation system")
    print("🔑 API key management")
    print("🔄 Resume failed generations")
    print("🛑 Stop generation anytime")
    print("📁 Organized file structure")
    print("📊 Multiple concurrent generations")
    print("📄 Professional PDF output")
    print("🌐 Open your browser to: http://localhost:5000")
    print()
    print("🛑 Press Ctrl+C to stop")
    print("=" * 70)
    
    try:
        # Test providers
        providers = get_available_providers()
        available = len([p for p in providers if p['status'] == 'available'])
        print(f"📊 Found {len(providers)} providers, {available} available")
        
        # Ensure output directory exists
        os.makedirs('./notes_output', exist_ok=True)
        
        socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server failed to start: {e}")
        traceback.print_exc()
        sys.exit(1)