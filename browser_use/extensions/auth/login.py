"""Login handler extension for browser automation."""

import os
import logging
from typing import Optional
from dotenv import load_dotenv

from browser_use.browser.service import Browser

logger = logging.getLogger(__name__)

class LoginHandler:
    """Handles login operations for web pages."""
    
    def __init__(self):
        """Initialize the login handler."""
        load_dotenv()
        self.username = os.getenv('LOGIN_USERNAME')
        self.password = os.getenv('LOGIN_PASSWORD')
        
    async def handle_login(self, browser: Browser, url: str) -> bool:
        """Handle login for a given URL."""
        try:
            # Navigate to login URL if provided
            if url:
                await browser.navigate_to(url)
                
            # Get current page state
            state = await browser.get_state()
            selector_map = state.selector_map
            
            # Find login form elements using selector map
            username_field = None
            password_field = None
            submit_button = None
            
            for idx, item in enumerate(state.items):
                if any(attr in item.get('attributes', {}).get('type', '').lower() for attr in ['text', 'email']):
                    username_field = idx
                elif 'password' in item.get('attributes', {}).get('type', '').lower():
                    password_field = idx
                elif any(attr in item.get('attributes', {}).get('type', '').lower() for attr in ['submit']):
                    submit_button = idx
            
            if username_field is None or password_field is None:
                logger.warning("Could not find login form elements")
                return False
                
            if not self.username or not self.password:
                logger.warning("Login credentials not found in environment variables")
                return False
            
            # Enter credentials
            await browser._input_text_by_xpath(selector_map[username_field], self.username)
            await browser._input_text_by_xpath(selector_map[password_field], self.password)
            
            # Submit form
            if submit_button is not None:
                await browser._click_element_by_xpath(selector_map[submit_button])
            
            # Wait for navigation
            await browser.wait_for_page_load()
            
            # Verify login success by checking for common post-login elements
            new_state = await browser.get_state()
            for item in new_state.items:
                text = item.get('innerText', '').lower()
                if any(indicator in text for indicator in ['logout', 'sign out', 'profile', 'account']):
                    return True
                    
            return False
            
        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
            return False
