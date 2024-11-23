import logging
from typing import Optional
from browser_use.browser.service import Browser

logger = logging.getLogger(__name__)

class ResourceManager:
    """Enhanced resource management and cleanup for browser_use framework."""
    
    def __init__(self, browser: Optional[Browser] = None):
        self.browser = browser
        
    def cleanup(self) -> None:
        """Comprehensive cleanup of browser resources."""
        try:
            if not self.browser:
                logger.debug("No browser instance to clean up")
                return
                
            if not hasattr(self.browser, 'driver'):
                logger.debug("No browser driver to clean up")
                return
                
            # Close all windows except main
            try:
                main_handle = self.browser.driver.current_window_handle
                for handle in self.browser.driver.window_handles:
                    if handle != main_handle:
                        self.browser.driver.switch_to.window(handle)
                        self.browser.driver.close()
                self.browser.driver.switch_to.window(main_handle)
            except Exception as e:
                logger.warning(f"Error closing additional windows: {str(e)}")
            
            # Clear cookies
            try:
                self.browser.driver.delete_all_cookies()
                logger.info("Successfully cleared cookies")
            except Exception as e:
                logger.warning(f"Error clearing cookies: {str(e)}")
            
            # Clear local storage
            try:
                self.browser.driver.execute_script("window.localStorage.clear();")
                logger.info("Successfully cleared local storage")
            except Exception as e:
                logger.warning(f"Error clearing local storage: {str(e)}")
            
            # Clear session storage
            try:
                self.browser.driver.execute_script("window.sessionStorage.clear();")
                logger.info("Successfully cleared session storage")
            except Exception as e:
                logger.warning(f"Error clearing session storage: {str(e)}")
            
            # Quit browser
            try:
                self.browser.driver.quit()
                logger.info("Successfully closed browser driver")
            except Exception as e:
                logger.warning(f"Error closing browser driver: {str(e)}")
                
        except Exception as e:
            logger.warning(f"Error during cleanup: {str(e)}")
        finally:
            self.browser = None
