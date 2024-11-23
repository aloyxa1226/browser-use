import logging
from typing import Optional
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from browser_use.browser.service import Browser

logger = logging.getLogger(__name__)

class CookieConsentHandler:
    """Enhanced cookie consent handling for browser_use framework."""
    
    def __init__(self, browser: Browser):
        self.browser = browser
        
    def handle_consent(self) -> bool:
        """Handle cookie consent banners if present."""
        try:
            if not self.browser or not hasattr(self.browser, 'driver'):
                logger.debug("Browser driver not initialized")
                return False

            # Get page source and parse with BeautifulSoup
            page_source = self.browser.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Try multiple strategies
            strategies = [
                self._try_xpath_buttons,
                self._try_class_based_buttons,
                self._try_text_based_buttons,
                self._try_aria_based_buttons
            ]
            
            for strategy in strategies:
                if strategy():
                    return True
                    
            logger.debug("No cookie consent buttons found or interacted with")
            return False
                
        except Exception as e:
            logger.warning(f"Error handling cookie consent: {str(e)}")
            return False
            
    def _try_xpath_buttons(self) -> bool:
        """Try to find and click cookie consent buttons using XPath patterns."""
        button_patterns = [
            "//button[contains(., 'cookie')]",
            "//button[contains(., 'Cookie')]",
            "//button[contains(., 'Accept')]",
            "//button[contains(., 'Agree')]",
            "//button[contains(., 'Got it')]",
            "//button[contains(., 'OK')]",
            "//button[contains(., 'Continue')]",
            "//div[contains(@class, 'cookie')]//button",
            "//div[contains(@id, 'cookie')]//button"
        ]
        
        return self._try_click_elements(button_patterns, By.XPATH)
        
    def _try_class_based_buttons(self) -> bool:
        """Try to find and click cookie consent buttons using class patterns."""
        class_patterns = [
            '[class*="cookie-consent"] button',
            '[class*="cookie-banner"] button',
            '[class*="cookie-notice"] button',
            '[class*="cookie-policy"] button',
            '[class*="consent-banner"] button'
        ]
        
        return self._try_click_elements(class_patterns, By.CSS_SELECTOR)
        
    def _try_text_based_buttons(self) -> bool:
        """Try to find and click cookie consent buttons using text content."""
        text_patterns = [
            'Accept All Cookies',
            'Accept Cookies',
            'I Accept',
            'Allow All',
            'Got it',
            'I understand',
            'Continue to site'
        ]
        
        for text in text_patterns:
            xpath = f"//*[contains(text(), '{text}')]"
            if self._try_click_elements([xpath], By.XPATH):
                return True
        return False
        
    def _try_aria_based_buttons(self) -> bool:
        """Try to find and click cookie consent buttons using ARIA attributes."""
        aria_patterns = [
            '[aria-label*="cookie"] button',
            '[aria-label*="consent"] button',
            '[role="dialog"] button',
            '[role="alertdialog"] button'
        ]
        
        return self._try_click_elements(aria_patterns, By.CSS_SELECTOR)
        
    def _try_click_elements(self, patterns: list[str], by: str) -> bool:
        """Try to click elements matching the given patterns."""
        for pattern in patterns:
            try:
                elements = self.browser.driver.find_elements(by, pattern)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        try:
                            element.click()
                            logger.info(f"Successfully clicked cookie consent button: {pattern}")
                            return True
                        except Exception:
                            continue
            except Exception:
                continue
        return False
