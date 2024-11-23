"""Resource cleanup extension for browser_use framework."""

import logging
from browser_use.browser.service import Browser

logger = logging.getLogger(__name__)

class ResourceCleanup:
    """Handles cleanup of browser resources."""
    
    async def cleanup(self, browser: Browser) -> None:
        """Clean up browser resources."""
        try:
            # Clear cookies
            await self._clear_cookies(browser)
            
            # Clear local storage
            await self._clear_local_storage(browser)
            
            # Close extra tabs
            await self._close_extra_tabs(browser)
            
            logger.info("Successfully cleaned up browser resources")
            
        except Exception as e:
            logger.error(f"Error cleaning up resources: {str(e)}")
            raise
            
    async def _clear_cookies(self, browser: Browser) -> None:
        """Clear browser cookies."""
        try:
            session = await browser.get_session()
            await session.context.clear_cookies()
            logger.debug("Cleared browser cookies")
        except Exception as e:
            logger.warning(f"Error clearing cookies: {str(e)}")
            
    async def _clear_local_storage(self, browser: Browser) -> None:
        """Clear local storage."""
        try:
            page = await browser.get_current_page()
            await page.evaluate("window.localStorage.clear()")
            logger.debug("Cleared local storage")
        except Exception as e:
            logger.warning(f"Error clearing local storage: {str(e)}")
            
    async def _close_extra_tabs(self, browser: Browser) -> None:
        """Close all tabs except the current one."""
        try:
            session = await browser.get_session()
            current_page = session.current_page
            
            for page in session.context.pages:
                if page != current_page:
                    await page.close()
                    
            logger.debug("Closed extra browser tabs")
        except Exception as e:
            logger.warning(f"Error closing extra tabs: {str(e)}")
