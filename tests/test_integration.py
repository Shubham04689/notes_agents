"""Integration tests for the complete system"""
import pytest
import os
import tempfile
import shutil
from unittest.mock import Mock, patch
from src.models import OllamaAdapter
from src.agents import PlannerAgent, ResearcherAgent, CoverageTrackerAgent
from src.core import Orchestrator, StorageManager, StateManager


@pytest.fixture
def temp_dir():
    """Create temporary directory for testing"""
    temp = tempfile.mkdtemp()
    yield temp
    shutil.rmtree(temp)


@pytest.fixture
def mock_model():
    """Create mock model for testing"""
    model = Mock()
    model.model_name = "test-model"
    model.generate.return_value = "Test generated content " * 100  # 300 words
    return model


@pytest.fixture
def test_config(temp_dir):
    """Create test configuration"""
    return {
        'storage': {
            'base_dir': temp_dir,
            'state_file': 'test_state.json'
        },
        'generation': {
            'max_depth': 3,
            'min_section_length': 100,
            'max_iterations': 10,
            'expansion_threshold': 0.7
        },
        'pdf': {
            'title_font_size': 24,
            'chapter_font_size': 18,
            'section_font_size': 14,
            'body_font_size': 11,
            'line_spacing': 1.5,
            'margin': 72
        }
    }


def test_storage_manager_integration(temp_dir):
    """Test storage manager can save and load content"""
    storage = StorageManager(temp_dir)
    
    # Save content
    filepath = storage.save_content(
        node_id='test1',
        title='Test Title',
        content='Test content here',
        node_type='section'
    )
    
    assert os.path.exists(filepath)
    
    # Load content
    loaded = storage.load_content('test1')
    assert 'Test Title' in loaded
    assert 'Test content here' in loaded
    
    # Get all files
    files = storage.get_all_content_files()
    assert len(files) == 1


def test_state_manager_integration(temp_dir):
    """Test state manager can persist and restore state"""
    state_file = os.path.join(temp_dir, 'test_state.json')
    state = StateManager(state_file)
    
    # Initialize session
    outline = {
        'topic': 'Test Topic',
        'chapters': [
            {
                'id': 'ch1',
                'title': 'Chapter 1',
                'sections': []
            }
        ]
    }
    
    state.initialize_session('Test Topic', 'test-model', outline)
    
    # Verify state
    assert state.state['topic'] == 'Test Topic'
    assert state.state['model_name'] == 'test-model'
    assert len(state.state['pending_nodes']) == 1
    
    # Mark node complete
    state.mark_node_complete('ch1', 'Chapter 1', 500)
    
    # Verify update
    assert len(state.state['covered_nodes']) == 1
    assert len(state.state['pending_nodes']) == 0
    assert state.state['total_word_count'] == 500
    
    # Create new state manager (simulating restart)
    state2 = StateManager(state_file)
    
    # Verify state was persisted
    assert state2.state['topic'] == 'Test Topic'
    assert len(state2.state['covered_nodes']) == 1


def test_planner_agent_creates_outline(mock_model):
    """Test planner agent can create an outline"""
    # Mock JSON response
    mock_model.generate.return_value = '''
    {
        "topic": "Test Topic",
        "chapters": [
            {
                "id": "ch1",
                "title": "Introduction",
                "sections": [
                    {
                        "id": "ch1_s1",
                        "title": "Background",
                        "subsections": []
                    }
                ]
            }
        ]
    }
    '''
    
    planner = PlannerAgent(mock_model)
    result = planner.execute({'topic': 'Test Topic'})
    
    assert result['success']
    assert 'outline' in result
    assert result['outline']['topic'] == 'Test Topic'
    assert len(result['outline']['chapters']) == 1


def test_researcher_agent_generates_content(mock_model):
    """Test researcher agent generates content"""
    researcher = ResearcherAgent(mock_model)
    
    node = {
        'id': 'test1',
        'title': 'Test Node',
        'type': 'section'
    }
    
    result = researcher.execute({
        'node': node,
        'parent_context': 'Test context',
        'covered_topics': []
    })
    
    assert result['success']
    assert 'content' in result
    assert result['node_id'] == 'test1'
    assert result['title'] == 'Test Node'


def test_coverage_tracker_workflow(mock_model):
    """Test coverage tracker workflow"""
    tracker = CoverageTrackerAgent(mock_model)
    
    outline = {
        'topic': 'Test',
        'chapters': [
            {
                'id': 'ch1',
                'title': 'Chapter 1',
                'sections': [
                    {
                        'id': 'ch1_s1',
                        'title': 'Section 1',
                        'subsections': []
                    }
                ]
            }
        ]
    }
    
    # Initialize
    result = tracker.execute({'action': 'initialize', 'outline': outline})
    assert result['success']
    assert result['total_nodes'] == 2
    
    # Get next
    result = tracker.execute({'action': 'get_next'})
    assert result['success']
    assert result['has_next']
    assert result['node']['id'] == 'ch1'
    
    # Mark complete
    result = tracker.execute({
        'action': 'mark_complete',
        'node_id': 'ch1',
        'title': 'Chapter 1'
    })
    assert result['success']
    assert result['covered_count'] == 1
    
    # Get status
    result = tracker.execute({'action': 'get_status'})
    assert result['success']
    assert result['covered_count'] == 1
    assert result['pending_count'] == 1


def test_full_system_integration(mock_model, test_config, temp_dir):
    """Test full system integration"""
    # Setup
    state_file = os.path.join(temp_dir, 'test_state.json')
    storage = StorageManager(temp_dir)
    state = StateManager(state_file)
    
    # Mock planner response
    mock_model.generate.return_value = '''
    {
        "topic": "Test Topic",
        "chapters": [
            {
                "id": "ch1",
                "title": "Introduction",
                "sections": []
            }
        ]
    }
    '''
    
    orchestrator = Orchestrator(mock_model, storage, state, test_config)
    
    # Note: Full generation test would require more complex mocking
    # This verifies the orchestrator can be initialized
    assert orchestrator.planner is not None
    assert orchestrator.researcher is not None
    assert orchestrator.author is not None
    assert orchestrator.tracker is not None
    assert orchestrator.reviewer is not None
    assert orchestrator.judge is not None


def test_ollama_adapter_initialization():
    """Test Ollama adapter can be initialized"""
    adapter = OllamaAdapter()
    assert adapter is not None
    assert adapter.host == "http://localhost:11434"
    
    # Test with custom host
    adapter = OllamaAdapter(host="http://custom:8080")
    assert adapter.host == "http://custom:8080"
