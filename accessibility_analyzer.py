"""
Accessibility Analyzer for extracting ARIA and accessibility information.

Analyzes DOM elements for accessibility attributes, roles, labels,
and other accessibility features for better AI understanding.
"""

from typing import Dict, Any, Optional
from bs4 import BeautifulSoup, Tag

from data_types import AccessibilityInfo, AccessibilityRole


class AccessibilityAnalyzer:
    """
    Analyzes accessibility features in DOM elements.
    
    Extracts ARIA attributes, roles, labels, and other accessibility
    information to improve AI interaction with web content.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize Accessibility Analyzer."""
        self.config = config or {}
    
    async def analyze_accessibility(self, soup: BeautifulSoup) -> AccessibilityInfo:
        """Analyze overall page accessibility."""
        page_accessibility = AccessibilityInfo()
        
        # Find page title
        title_elem = soup.find('title')
        if title_elem:
            page_accessibility.label = title_elem.get_text(strip=True)
        
        # Check for main landmark
        main_elem = soup.find(['main', '[role="main"]'])
        if main_elem:
            page_accessibility.role = AccessibilityRole.MAIN
        
        # Count accessibility features
        aria_elements = soup.find_all(lambda tag: any(attr.startswith('aria-') for attr in tag.attrs))
        page_accessibility.attributes['aria_elements_count'] = len(aria_elements)
        
        return page_accessibility
    
    def extract_element_accessibility(self, element: Tag) -> AccessibilityInfo:
        """Extract accessibility info from a single element."""
        accessibility_info = AccessibilityInfo()
        
        # Extract ARIA attributes
        for attr_name, attr_value in element.attrs.items():
            if attr_name.startswith('aria-'):
                aria_name = attr_name[5:]  # Remove 'aria-' prefix
                
                if aria_name == 'label':
                    accessibility_info.label = attr_value
                elif aria_name == 'describedby':
                    accessibility_info.described_by = attr_value.split()
                elif aria_name == 'labelledby':
                    accessibility_info.labelled_by = attr_value.split()
                elif aria_name == 'hidden':
                    accessibility_info.hidden = attr_value.lower() == 'true'
                elif aria_name == 'disabled':
                    accessibility_info.disabled = attr_value.lower() == 'true'
                elif aria_name == 'required':
                    accessibility_info.required = attr_value.lower() == 'true'
                else:
                    accessibility_info.attributes[attr_name] = attr_value
        
        # Extract role
        role = element.get('role')
        if role:
            try:
                accessibility_info.role = AccessibilityRole(role.upper())
            except ValueError:
                accessibility_info.attributes['role'] = role
        
        return accessibility_info