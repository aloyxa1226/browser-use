import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

class ConversationSaver:
    """Handles saving and loading of agent conversations."""
    
    def __init__(self, save_path: Optional[str] = None):
        self.save_path = save_path
        
    def save_conversation(self, history: List[Dict[str, Any]]) -> None:
        """Save conversation history with timestamps."""
        if not self.save_path:
            logger.debug("No save path specified, skipping conversation save")
            return
            
        try:
            save_path = Path(self.save_path)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Add timestamps to history
            timestamped_history = []
            for entry in history:
                timestamped_entry = entry.copy()
                timestamped_entry['timestamp'] = datetime.now().isoformat()
                timestamped_history.append(timestamped_entry)
            
            # Save with pretty formatting
            with open(save_path, 'w') as f:
                json.dump(timestamped_history, f, indent=2)
                
            logger.info(f"Successfully saved conversation to {save_path}")
            
        except Exception as e:
            logger.error(f"Error saving conversation: {str(e)}")
            
    def load_conversation(self) -> Optional[List[Dict[str, Any]]]:
        """Load saved conversation history."""
        if not self.save_path:
            logger.debug("No save path specified, cannot load conversation")
            return None
            
        try:
            save_path = Path(self.save_path)
            if not save_path.exists():
                logger.debug(f"Save file does not exist: {save_path}")
                return None
                
            with open(save_path, 'r') as f:
                history = json.load(f)
                
            logger.info(f"Successfully loaded conversation from {save_path}")
            return history
            
        except Exception as e:
            logger.error(f"Error loading conversation: {str(e)}")
            return None
