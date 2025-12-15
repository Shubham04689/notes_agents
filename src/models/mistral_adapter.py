import os
from typing import List, Optional
from .base import BaseModelAdapter

try:
    from mistralai import Mistral
    MISTRAL_AVAILABLE = True
except ImportError:
    MISTRAL_AVAILABLE = False


class MistralAdapter(BaseModelAdapter):
    """Adapter for Mistral AI models"""
    
    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        super().__init__(model_name)
        self.api_key = api_key or os.getenv('MISTRAL_API_KEY')
        
        if not MISTRAL_AVAILABLE:
            raise ImportError("mistralai package not installed")
        
        self.client = None
        if self.api_key:
            self.client = Mistral(api_key=self.api_key)
    
    def is_available(self) -> bool:
        """Check if Mistral API is available"""
        return bool(self.api_key and MISTRAL_AVAILABLE and self.client)
    
    def list_models(self) -> List[str]:
        """List available Mistral models"""
        if not self.is_available():
            return []
        
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception as e:
            raise RuntimeError(f"Failed to list Mistral models: {str(e)}")
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate text using Mistral"""
        if not self.client:
            raise ValueError("Mistral client not initialized")
        
        if not self.model_name:
            raise ValueError("No model selected. Call set_model() first.")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # Retry logic for rate limits
        max_retries = 3
        retry_delay = 2  # seconds
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.complete(
                    model=self.model_name,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                return response.choices[0].message.content
            except Exception as e:
                error_str = str(e)
                # Check if it's a rate limit error
                if "429" in error_str or "rate" in error_str.lower():
                    if attempt < max_retries - 1:
                        import time
                        wait_time = retry_delay * (attempt + 1)
                        print(f"   ⚠ Rate limit hit, waiting {wait_time}s before retry...")
                        time.sleep(wait_time)
                        continue
                raise RuntimeError(f"Mistral generation failed: {error_str}")
