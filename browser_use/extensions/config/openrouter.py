import os
from typing import Optional
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class OpenRouterConfig:
    """Configuration handler for OpenRouter integration."""
    
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        self.model = os.getenv("OPENROUTER_MODEL", "gpt-4o")
        
    @property
    def is_configured(self) -> bool:
        """Check if OpenRouter is properly configured."""
        return bool(self.api_key)
        
    def get_headers(self) -> dict:
        """Get headers for OpenRouter API requests."""
        if not self.is_configured:
            raise ValueError("OpenRouter API key not configured")
            
        return {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://browser-use.com",
            "X-Title": "Browser Use Framework"
        }
        
    def get_model_config(self) -> dict:
        """Get model configuration for OpenRouter."""
        return {
            "model": self.model,
            "base_url": self.base_url,
            "headers": self.get_headers()
        }
