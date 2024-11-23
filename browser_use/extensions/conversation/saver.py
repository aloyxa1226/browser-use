"""Conversation saver extension for browser_use framework."""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ConversationSaver:
    """Handles saving and managing conversation history."""
    
    def __init__(self, save_dir: Optional[str] = None):
        """Initialize the conversation saver."""
        self.save_dir = save_dir or os.path.join(os.path.expanduser('~'), '.browser_use', 'conversations')
        
    async def initialize(self) -> None:
        """Initialize the conversation saver."""
        try:
            # Create save directory if it doesn't exist
            Path(self.save_dir).mkdir(parents=True, exist_ok=True)
            logger.info(f"Initialized conversation saver with directory: {self.save_dir}")
        except Exception as e:
            logger.error(f"Error initializing conversation saver: {str(e)}")
            raise
            
    async def save(self, conversation: Dict[str, Any]) -> str:
        """Save a conversation to disk."""
        try:
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.json"
            filepath = os.path.join(self.save_dir, filename)
            
            # Add metadata
            conversation['metadata'] = {
                'timestamp': timestamp,
                'version': '1.0'
            }
            
            # Save conversation
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(conversation, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Saved conversation to: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error saving conversation: {str(e)}")
            return ""
            
    async def load(self, filepath: str) -> Optional[Dict[str, Any]]:
        """Load a conversation from disk."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                conversation = json.load(f)
            return conversation
        except Exception as e:
            logger.error(f"Error loading conversation: {str(e)}")
            return None
            
    async def list_conversations(self) -> list[str]:
        """List all saved conversations."""
        try:
            files = []
            for file in Path(self.save_dir).glob("conversation_*.json"):
                files.append(str(file))
            return sorted(files)
        except Exception as e:
            logger.error(f"Error listing conversations: {str(e)}")
            return []
