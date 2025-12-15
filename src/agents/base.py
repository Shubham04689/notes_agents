from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ..models.base import BaseModelAdapter


class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, model: BaseModelAdapter, name: str):
        self.model = model
        self.name = name
        self.system_prompt = self._get_system_prompt()
    
    @abstractmethod
    def _get_system_prompt(self) -> str:
        """Return the system prompt for this agent"""
        pass
    
    def generate(self, prompt: str) -> str:
        """Generate response using the model"""
        return self.model.generate(prompt, self.system_prompt)
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's primary function"""
        pass
