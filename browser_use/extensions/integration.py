"""Integration module for browser-use extensions."""

from typing import Optional

from browser_use.extensions.auth.login import LoginHandler
from browser_use.extensions.conversation.saver import ConversationSaver
from browser_use.extensions.cookie_consent.handler import CookieConsentHandler
from browser_use.extensions.element_detection.enhanced_dom import EnhancedDOMService
from browser_use.extensions.resource_management.cleanup import ResourceManager

class ExtensionsManager:
    """Manager class for browser-use extensions."""
    
    def __init__(self):
        self.login_handler = LoginHandler()
        self.conversation_saver = ConversationSaver()
        self.cookie_consent = CookieConsentHandler()
        self.dom_service = EnhancedDOMService()
        self.resource_manager = ResourceManager()
        
    async def handle_login(self, url: str) -> bool:
        """Handle login for a given URL."""
        return await self.login_handler.handle_login(url)
        
    async def save_conversation(self, conversation: dict) -> str:
        """Save conversation history."""
        return await self.conversation_saver.save(conversation)
        
    async def handle_cookie_consent(self) -> bool:
        """Handle cookie consent popups."""
        return await self.cookie_consent.handle()
        
    async def find_element(self, selector: str, context: Optional[dict] = None) -> Optional[dict]:
        """Find element using enhanced DOM service."""
        return await self.dom_service.find_element(selector, context)
        
    async def cleanup_resources(self) -> None:
        """Clean up browser resources."""
        await self.resource_manager.cleanup()
