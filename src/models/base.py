from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseModelAdapter(ABC):
    """Abstract base class for all LLM adapters"""
    
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name
        self.max_tokens = 4096
        self.temperature = 0.7
    
    @abstractmethod
    def list_models(self) -> List[str]:
        """List all available models"""
        pass
    
    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate text from prompt"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the model service is available"""
        pass
    
    def set_model(self, model_name: str):
        """Set the active model"""
        self.model_name = model_name
    
    def set_temperature(self, temperature: float):
        """Set generation temperature"""
        self.temperature = max(0.0, min(1.0, temperature))
    
    def set_max_tokens(self, max_tokens: int):
        """Set maximum tokens for generation"""
        self.max_tokens = max_tokens
