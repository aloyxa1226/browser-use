"""Cookie consent handling for browser_use framework."""

import logging
from typing import Optional, List
from browser_use.browser.service import Browser

logger = logging.getLogger(__name__)

class CookieConsentHandler:
    """Enhanced cookie consent handling for browser_use framework."""
    
    def __init__(self):
        self.consent_keywords = [
            'accept', 'agree', 'allow', 'consent',
            'got it', 'i understand', 'ok', 'continue',
            'cookie', 'cookies', 'privacy'
        ]
        
    async def handle(self, browser: Browser) -> bool:
        """Handle cookie consent banners if present."""
        try:
            # Get current page state
            state = await browser.get_state()
            
            # Look for consent-related elements
            consent_elements = []
            for idx, item in enumerate(state.items):
                text = item.get('innerText', '').lower()
                role = item.get('role', '').lower()
                
                # Check if element matches consent patterns
                if any(keyword in text for keyword in self.consent_keywords):
                    if role in ['button', 'link'] or 'button' in item.get('tag', '').lower():
                        consent_elements.append(idx)
                        
            # Try clicking consent elements
            for element_idx in consent_elements:
                try:
                    await browser._click_element_by_xpath(state.selector_map[element_idx])
                    logger.info("Successfully clicked cookie consent button")
                    return True
                except Exception as e:
                    logger.debug(f"Failed to click consent element: {str(e)}")
                    continue
                    
            logger.debug("No cookie consent buttons found or interacted with")
            return False
                
        except Exception as e:
            logger.warning(f"Error handling cookie consent: {str(e)}")
            return False
