"""OpenRouter configuration and LLM initialization."""

import os
import logging
from typing import Optional
from dotenv import load_dotenv
import openai

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def get_llm() -> Optional[openai.OpenAI]:
    """Get configured OpenAI client for OpenRouter."""
    try:
        # Get API key and base URL from environment
        api_key = os.getenv('OPENROUTER_API_KEY')
        base_url = os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')
        model = os.getenv('OPENROUTER_MODEL', 'anthropic/claude-2')
        
        if not api_key:
            logger.error("OpenRouter API key not found in environment")
            return None
            
        # Configure OpenAI client for OpenRouter
        client = openai.OpenAI(
            base_url=base_url,
            api_key=api_key,
            default_headers={
                "HTTP-Referer": "https://github.com/browser-use",
                "X-Title": "Browser Use AI Framework"
            }
        )
        
        # Test the configuration
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Test connection"}],
            max_tokens=10
        )
        
        logger.info("Successfully configured OpenRouter LLM client")
        return client
        
    except Exception as e:
        logger.error(f"Error configuring OpenRouter LLM: {str(e)}")
        return None
