"""Enhanced DOM service for advanced element detection."""

import logging
from typing import Optional, Dict, Any

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from browser_use.browser.service import Browser

logger = logging.getLogger(__name__)

class EnhancedDOMService:
    """Enhanced DOM service with advanced element detection capabilities."""
    
    def __init__(self, browser: Optional[Browser] = None):
        """Initialize the DOM service."""
        self.browser = browser
        
    async def find_element(self, selector: str, context: Optional[Dict[str, Any]] = None) -> Optional[Any]:
        """Find an element using enhanced detection strategies."""
        try:
            if not self.browser:
                logger.warning("Browser instance not available")
                return None
                
            # Try CSS selector first
            try:
                element = WebDriverWait(self.browser.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if element.is_displayed():
                    return element
            except:
                pass
                
            # Try XPATH as fallback
            try:
                xpath_selector = f"//*[@{selector}]"
                element = WebDriverWait(self.browser.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, xpath_selector))
                )
                if element.is_displayed():
                    return element
            except:
                pass
                
            # Try ARIA role if context specifies it
            if context and 'role' in context:
                try:
                    role_selector = f"//*[@role='{context['role']}']"
                    element = WebDriverWait(self.browser.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, role_selector))
                    )
                    if element.is_displayed():
                        return element
                except:
                    pass
                    
            return None
            
        except Exception as e:
            logger.error(f"Error finding element: {str(e)}")
            return None
