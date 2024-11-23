"""Browser module for browser automation."""

from browser_use.browser.service import Browser
from browser_use.browser.views import BrowserError, BrowserState, TabInfo

__all__ = ['Browser', 'BrowserError', 'BrowserState', 'TabInfo']
