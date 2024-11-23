"""Integration module for browser-use extensions."""

import logging
from typing import Optional, Dict, Any

from browser_use.browser.service import Browser
from browser_use.extensions.auth.login import LoginHandler
from browser_use.extensions.conversation.saver import ConversationSaver
from browser_use.extensions.cookie_consent.handler import CookieConsentHandler
from browser_use.extensions.resource_management.cleanup import ResourceCleanup

logger = logging.getLogger(__name__)

class ExtensionsManager:
    """Manager class for browser-use extensions."""
    
    def __init__(self):
        """Initialize extension handlers."""
        self.login_handler = LoginHandler()
        self.conversation_saver = ConversationSaver()
        self.cookie_consent = CookieConsentHandler()
        self.resource_cleanup = ResourceCleanup()
        
    async def handle_login(self, browser: Browser, url: str) -> bool:
        """Handle login for a given URL."""
        try:
            return await self.login_handler.handle_login(browser, url)
        except Exception as e:
            logger.error(f"Error in login handler: {str(e)}")
            return False
        
    async def save_conversation(self, conversation: Dict[str, Any]) -> str:
        """Save conversation history."""
        try:
            return await self.conversation_saver.save(conversation)
        except Exception as e:
            logger.error(f"Error saving conversation: {str(e)}")
            return ""
        
    async def handle_cookie_consent(self, browser: Browser) -> bool:
        """Handle cookie consent popups."""
        try:
            return await self.cookie_consent.handle(browser)
        except Exception as e:
            logger.error(f"Error handling cookie consent: {str(e)}")
            return False
        
    async def cleanup_resources(self, browser: Browser) -> None:
        """Clean up browser resources."""
        try:
            await self.resource_cleanup.cleanup(browser)
        except Exception as e:
            logger.error(f"Error cleaning up resources: {str(e)}")
            
    async def initialize_extensions(self, browser: Browser) -> None:
        """Initialize all extensions for a browser instance."""
        try:
            # Handle any cookie consent popups
            await self.handle_cookie_consent(browser)
            
            # Initialize conversation saver
            await self.conversation_saver.initialize()
            
            logger.info("Extensions initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing extensions: {str(e)}")
            raise
