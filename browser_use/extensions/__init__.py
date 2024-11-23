"""
Browser Use Extensions - Enhanced functionality for browser automation.

This package provides additional features and improvements for the browser_use framework:
- Cookie consent handling
- Enhanced element detection
- Resource management
- Authentication
- Conversation management
- Configuration management
"""

from browser_use.extensions.auth.login import LoginHandler
from browser_use.extensions.cookie_consent.handler import CookieConsentHandler
from browser_use.extensions.conversation.saver import ConversationSaver
from browser_use.extensions.element_detection.enhanced_dom import EnhancedDOMService
from browser_use.extensions.resource_management.cleanup import ResourceCleanup

__all__ = [
    'LoginHandler',
    'CookieConsentHandler',
    'ConversationSaver',
    'EnhancedDOMService',
    'ResourceCleanup',
]
