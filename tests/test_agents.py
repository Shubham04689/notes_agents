"""Tests for agents"""
import pytest
from unittest.mock import Mock
from src.agents import PlannerAgent, ResearcherAgent, AuthorAgent, CoverageTrackerAgent


def create_mock_model():
    """Create a mock model for testing"""
    mock = Mock()
    mock.generate.return_value = '{"topic": "Test", "chapters": []}'
    return mock


def test_planner_agent_initialization():
    """Test planner agent can be initialized"""
    model = create_mock_model()
    agent = PlannerAgent(model)
    assert agent.name == "Planner"
    assert agent.model == model


def test_researcher_agent_initialization():
    """Test researcher agent can be initialized"""
    model = create_mock_model()
    agent = ResearcherAgent(model)
    assert agent.name == "Researcher"
    assert agent.model == model


def test_author_agent_initialization():
    """Test author agent can be initialized"""
    model = create_mock_model()
    agent = AuthorAgent(model)
    assert agent.name == "Author"
    assert agent.model == model


def test_coverage_tracker_initialization():
    """Test coverage tracker can be initialized"""
    model = create_mock_model()
    agent = CoverageTrackerAgent(model)
    assert agent.name == "Coverage Tracker"
    assert len(agent.covered_nodes) == 0
    assert len(agent.pending_nodes) == 0


def test_coverage_tracker_initialize():
    """Test coverage tracker initialization"""
    model = create_mock_model()
    agent = CoverageTrackerAgent(model)
    
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
    
    result = agent.execute({'action': 'initialize', 'outline': outline})
    assert result['success']
    assert result['total_nodes'] == 2  # 1 chapter + 1 section


def test_coverage_tracker_mark_complete():
    """Test marking nodes as complete"""
    model = create_mock_model()
    agent = CoverageTrackerAgent(model)
    
    # Initialize with outline
    outline = {
        'topic': 'Test',
        'chapters': [
            {'id': 'ch1', 'title': 'Chapter 1', 'sections': []}
        ]
    }
    agent.execute({'action': 'initialize', 'outline': outline})
    
    # Mark complete
    result = agent.execute({
        'action': 'mark_complete',
        'node_id': 'ch1',
        'title': 'Chapter 1'
    })
    
    assert result['success']
    assert result['covered_count'] == 1
    assert result['pending_count'] == 0


def test_coverage_tracker_get_next():
    """Test getting next node"""
    model = create_mock_model()
    agent = CoverageTrackerAgent(model)
    
    outline = {
        'topic': 'Test',
        'chapters': [
            {'id': 'ch1', 'title': 'Chapter 1', 'sections': []}
        ]
    }
    agent.execute({'action': 'initialize', 'outline': outline})
    
    result = agent.execute({'action': 'get_next'})
    assert result['success']
    assert result['has_next']
    assert result['node']['id'] == 'ch1'
