import os
from typing import List, Optional
from .base import BaseModelAdapter

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class GeminiAdapter(BaseModelAdapter):
    """Adapter for Google Gemini models"""
    
    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        super().__init__(model_name)
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai package not installed")
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
        
        self.client = None
        if model_name:
            self._init_client()
    
    def _init_client(self):
        """Initialize the Gemini client"""
        if not self.api_key:
            raise ValueError("Gemini API key not provided")
        
        self.client = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={
                "temperature": self.temperature,
                "max_output_tokens": self.max_tokens,
            }
        )
    
    def is_available(self) -> bool:
        """Check if Gemini API is available"""
        return bool(self.api_key and GEMINI_AVAILABLE)
    
    def list_models(self) -> List[str]:
        """List available Gemini models"""
        if not self.is_available():
            return []
        
        try:
            models = genai.list_models()
            return [m.name.replace('models/', '') for m in models 
                   if 'generateContent' in m.supported_generation_methods]
        except Exception as e:
            raise RuntimeError(f"Failed to list Gemini models: {str(e)}")
    
    def set_model(self, model_name: str):
        """Set the active Gemini model"""
        super().set_model(model_name)
        self._init_client()
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate text using Gemini"""
        if not self.client:
            raise ValueError("No model selected. Call set_model() first.")
        
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        try:
            response = self.client.generate_content(full_prompt)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Gemini generation failed: {str(e)}")
