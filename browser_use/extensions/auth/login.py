import os
import logging
from typing import Optional, Tuple
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from browser_use_local.browser.service import Browser

logger = logging.getLogger(__name__)

class LoginHandler:
    """Enhanced login handling with environment variable support."""
    
    def __init__(self, browser: Browser):
        self.browser = browser
        load_dotenv()
        self.username = os.getenv("LOGIN_USERNAME")
        self.password = os.getenv("LOGIN_PASSWORD")
        
    def handle_login(self) -> bool:
        """Handle login process using environment credentials."""
        if not self.username or not self.password:
            logger.warning("Login credentials not found in environment")
            return False
            
        try:
            # Find login form elements
            username_field, password_field, submit_button = self._find_login_elements()
            if not all([username_field, password_field, submit_button]):
                logger.warning("Could not find all login form elements")
                return False
                
            # Enter credentials
            username_field.send_keys(self.username)
            password_field.send_keys(self.password)
            
            # Handle "Remember me" option
            self._handle_remember_me()
            
            # Submit form
            submit_button.click()
            
            # Verify login success
            return self._verify_login()
            
        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
            return False
            
    def _find_login_elements(self) -> Tuple[Optional[object], Optional[object], Optional[object]]:
        """Find username, password, and submit elements."""
        try:
            # Username/Email field patterns
            username_patterns = [
                "//input[@type='text']",
                "//input[@type='email']",
                "//input[contains(@id, 'user')]",
                "//input[contains(@id, 'email')]",
                "//input[contains(@name, 'user')]",
                "//input[contains(@name, 'email')]"
            ]
            
            # Password field patterns
            password_patterns = [
                "//input[@type='password']",
                "//input[contains(@id, 'pass')]",
                "//input[contains(@name, 'pass')]"
            ]
            
            # Submit button patterns
            submit_patterns = [
                "//button[@type='submit']",
                "//input[@type='submit']",
                "//button[contains(., 'Sign')]",
                "//button[contains(., 'Log')]",
                "//input[contains(@value, 'Sign')]",
                "//input[contains(@value, 'Log')]"
            ]
            
            username_field = None
            password_field = None
            submit_button = None
            
            # Find username field
            for pattern in username_patterns:
                elements = self.browser.driver.find_elements(By.XPATH, pattern)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        username_field = element
                        break
                if username_field:
                    break
                    
            # Find password field
            for pattern in password_patterns:
                elements = self.browser.driver.find_elements(By.XPATH, pattern)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        password_field = element
                        break
                if password_field:
                    break
                    
            # Find submit button
            for pattern in submit_patterns:
                elements = self.browser.driver.find_elements(By.XPATH, pattern)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        submit_button = element
                        break
                if submit_button:
                    break
                    
            return username_field, password_field, submit_button
            
        except Exception as e:
            logger.error(f"Error finding login elements: {str(e)}")
            return None, None, None
            
    def _handle_remember_me(self) -> None:
        """Handle 'Remember me' or 'Stay signed in' options."""
        try:
            remember_patterns = [
                "//input[@type='checkbox'][contains(@id, 'remember')]",
                "//input[@type='checkbox'][contains(@name, 'remember')]",
                "//label[contains(., 'Remember')]//input[@type='checkbox']",
                "//label[contains(., 'Stay')]//input[@type='checkbox']"
            ]
            
            for pattern in remember_patterns:
                elements = self.browser.driver.find_elements(By.XPATH, pattern)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        if not element.is_selected():
                            element.click()
                        break
                        
        except Exception as e:
            logger.warning(f"Error handling remember me option: {str(e)}")
            
    def _verify_login(self) -> bool:
        """Verify successful login."""
        try:
            # Common error message patterns
            error_patterns = [
                "//div[contains(@class, 'error')]",
                "//div[contains(@class, 'alert')]",
                "//p[contains(., 'incorrect')]",
                "//span[contains(., 'failed')]"
            ]
            
            # Check for error messages
            for pattern in error_patterns:
                elements = self.browser.driver.find_elements(By.XPATH, pattern)
                for element in elements:
                    if element.is_displayed():
                        logger.warning(f"Login failed: {element.text}")
                        return False
                        
            # Check for success indicators
            success_patterns = [
                "//div[contains(@class, 'profile')]",
                "//a[contains(., 'Account')]",
                "//span[contains(., 'Welcome')]",
                "//div[contains(@class, 'logged-in')]"
            ]
            
            for pattern in success_patterns:
                elements = self.browser.driver.find_elements(By.XPATH, pattern)
                for element in elements:
                    if element.is_displayed():
                        logger.info("Login successful")
                        return True
                        
            logger.warning("Could not verify login status")
            return False
            
        except Exception as e:
            logger.error(f"Error verifying login: {str(e)}")
            return False
