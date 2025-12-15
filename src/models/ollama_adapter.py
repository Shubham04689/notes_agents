import requests
from typing import List, Optional
import os
from .base import BaseModelAdapter


class OllamaAdapter(BaseModelAdapter):
    """Adapter for Ollama local models"""
    
    def __init__(self, host: str = "http://localhost:11434", model_name: Optional[str] = None):
        super().__init__(model_name)
        self.host = host.rstrip('/')
        self.api_url = f"{self.host}/api"
    
    def is_available(self) -> bool:
        """Check if Ollama service is running"""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def list_models(self) -> List[str]:
        """List all available Ollama models"""
        try:
            response = requests.get(f"{self.api_url}/tags", timeout=10)
            response.raise_for_status()
            data = response.json()
            return [model['name'] for model in data.get('models', [])]
        except Exception as e:
            raise RuntimeError(f"Failed to list Ollama models: {str(e)}")
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate text using Ollama"""
        if not self.model_name:
            raise ValueError("No model selected. Call set_model() first.")
        
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        try:
            response = requests.post(
                f"{self.api_url}/generate",
                json=payload,
                timeout=int(os.environ.get('OLLAMA_TIMEOUT', 1200))
            )
            response.raise_for_status()
            return response.json()['response']
        except Exception as e:
            raise RuntimeError(f"Ollama generation failed: {str(e)}")
