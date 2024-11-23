from bs4 import Tag
import logging

logger = logging.getLogger(__name__)

class EnhancedDomService:
    """Enhanced DOM service with improved element detection capabilities."""
    
    @staticmethod
    def is_interactive_element(element: Tag) -> bool:
        """Enhanced check for interactive elements including cookie consent elements."""
        interactive_elements = {
            'a',
            'button',
            'input',
            'select',
            'textarea',
            'summary',
            'dialog',
            'div',
        }

        interactive_roles = {
            'button',
            'link',
            'menuitem',
            'tab',
            'checkbox',
            'radio',
            'switch',
            'option',
            'combobox',
            'textbox',
            'searchbox',
            'slider',
            'spinbutton',
            'scrollbar',
            'progressbar',
            'tooltip',
            'dialog',
            'alertdialog',
            'banner',
            'menuitemcheckbox',
            'menuitemradio',
        }

        return (
            element.name in interactive_elements
            or element.get('role') in interactive_roles
            or element.get('aria-role') in interactive_roles
            or element.get('tabindex') == '0'
            or EnhancedDomService.is_cookie_consent_element(element)
        )

    @staticmethod
    def is_cookie_consent_element(element: Tag) -> bool:
        """Check if element is related to cookie consent."""
        cookie_keywords = {
            'cookie', 'cookies', 'consent', 'accept', 'agree', 'privacy',
            'gdpr', 'ccpa', 'allow', 'accept all', 'got it', 'i accept',
            'continue', 'ok', 'yes', 'dismiss'
        }
        
        # Get text content
        text = element.get_text(strip=True).lower()
        
        # Get common attributes
        id_attr = element.get('id', '').lower()
        class_attr = ' '.join(element.get('class', [])).lower()
        aria_label = element.get('aria-label', '').lower()
        data_attrs = ' '.join([v for k, v in element.attrs.items() if k.startswith('data-')]).lower()
        
        # Combine all searchable content
        searchable_content = f"{text} {id_attr} {class_attr} {aria_label} {data_attrs}"
        
        # Check if any cookie-related keyword is present
        return any(keyword in searchable_content for keyword in cookie_keywords)

    @staticmethod
    def is_visible_element(element: Tag) -> bool:
        """Enhanced check for element visibility."""
        return not (
            element.get('style', '').lower().find('display: none') >= 0
            or element.get('style', '').lower().find('visibility: hidden') >= 0
            or element.get('hidden') is not None
            or element.get('aria-hidden') == 'true'
            or element.get('aria-disabled') == 'true'
            or element.get('type') == 'hidden'
        )
