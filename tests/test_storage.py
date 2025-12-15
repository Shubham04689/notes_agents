"""Tests for storage manager"""
import os
import tempfile
import shutil
import pytest
from src.core import StorageManager


@pytest.fixture
def temp_storage():
    """Create temporary storage directory"""
    temp_dir = tempfile.mkdtemp()
    storage = StorageManager(temp_dir)
    yield storage
    shutil.rmtree(temp_dir)


def test_storage_initialization(temp_storage):
    """Test storage manager initialization"""
    assert os.path.exists(temp_storage.content_dir)


def test_save_content(temp_storage):
    """Test saving content"""
    filepath = temp_storage.save_content(
        node_id='test1',
        title='Test Title',
        content='Test content here',
        node_type='section'
    )
    
    assert os.path.exists(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        assert 'Test Title' in content
        assert 'Test content here' in content


def test_load_content(temp_storage):
    """Test loading content"""
    temp_storage.save_content(
        node_id='test2',
        title='Test Title 2',
        content='Test content 2',
        node_type='section'
    )
    
    loaded = temp_storage.load_content('test2')
    assert 'Test Title 2' in loaded
    assert 'Test content 2' in loaded


def test_get_all_content_files(temp_storage):
    """Test getting all content files"""
    temp_storage.save_content('test1', 'Title 1', 'Content 1', 'section')
    temp_storage.save_content('test2', 'Title 2', 'Content 2', 'section')
    
    files = temp_storage.get_all_content_files()
    assert len(files) == 2


def test_save_load_metadata(temp_storage):
    """Test saving and loading metadata"""
    metadata = {
        'topic': 'Test Topic',
        'model': 'test-model',
        'word_count': 1000
    }
    
    temp_storage.save_metadata(metadata)
    loaded = temp_storage.load_metadata()
    
    assert loaded['topic'] == 'Test Topic'
    assert loaded['model'] == 'test-model'
    assert loaded['word_count'] == 1000
