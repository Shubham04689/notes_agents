"""Tests for model adapters"""
import pytest
from src.models import OllamaAdapter, GeminiAdapter, MistralAdapter


def test_ollama_adapter_initialization():
    """Test Ollama adapter can be initialized"""
    adapter = OllamaAdapter()
    assert adapter is not None
    assert adapter.host == "http://localhost:11434"


def test_ollama_adapter_custom_host():
    """Test Ollama adapter with custom host"""
    adapter = OllamaAdapter(host="http://custom:8080")
    assert adapter.host == "http://custom:8080"


def test_model_temperature_bounds():
    """Test temperature is bounded between 0 and 1"""
    adapter = OllamaAdapter()
    
    adapter.set_temperature(0.5)
    assert adapter.temperature == 0.5
    
    adapter.set_temperature(-0.5)
    assert adapter.temperature == 0.0
    
    adapter.set_temperature(1.5)
    assert adapter.temperature == 1.0


def test_model_set_model():
    """Test setting model name"""
    adapter = OllamaAdapter()
    adapter.set_model("llama2")
    assert adapter.model_name == "llama2"


def test_gemini_adapter_initialization():
    """Test Gemini adapter can be initialized"""
    try:
        adapter = GeminiAdapter()
        assert adapter is not None
    except ImportError:
        pytest.skip("google-generativeai not installed")


def test_mistral_adapter_initialization():
    """Test Mistral adapter can be initialized"""
    try:
        adapter = MistralAdapter()
        assert adapter is not None
    except ImportError:
        pytest.skip("mistralai not installed")
