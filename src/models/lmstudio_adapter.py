import requests
from typing import List, Optional
from .base import BaseModelAdapter


class LMStudioAdapter(BaseModelAdapter):
    """Adapter for LM Studio local models"""
    
    def __init__(self, host: str = "http://localhost:1234", model_name: Optional[str] = None):
        super().__init__(model_name)
        self.host = host.rstrip('/')
        self.api_url = f"{self.host}/v1"
    
    def is_available(self) -> bool:
        """Check if LM Studio service is running"""
        try:
            response = requests.get(f"{self.api_url}/models", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def list_models(self) -> List[str]:
        """List all available LM Studio models"""
        try:
            response = requests.get(f"{self.api_url}/models", timeout=10)
            response.raise_for_status()
            data = response.json()
            return [model['id'] for model in data.get('data', [])]
        except Exception as e:
            raise RuntimeError(f"Failed to list LM Studio models: {str(e)}")
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate text using LM Studio"""
        if not self.model_name:
            # Use first available model if none selected
            models = self.list_models()
            if models:
                self.model_name = models[0]
            else:
                raise ValueError("No models available in LM Studio")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": False
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/chat/completions",
                json=payload,
                timeout=300
            )
            response.raise_for_status()
            data = response.json()
            return data['choices'][0]['message']['content']
        except Exception as e:
            raise RuntimeError(f"LM Studio generation failed: {str(e)}")
