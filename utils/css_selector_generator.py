"""
CSS Selector Generator for creating robust CSS selectors.

Generates multiple CSS selector strategies for DOM elements,
providing fallback options for reliable element location.
"""

from typing import Optional, List, Dict, Any
from bs4 import BeautifulSoup, Tag
import re


class CSSSelectorsGenerator:
    """
    Generates CSS selectors for DOM elements using various strategies.
    
    Provides multiple selector approaches for maximum reliability
    in different page contexts and structural changes.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize CSS Selector Generator.
        
        Args:
            config: Configuration for selector generation preferences
        """
        self.config = config or {}
        self.max_depth = self.config.get('max_depth', 10)
        self.prefer_ids = self.config.get('prefer_ids', True)
        self.prefer_classes = self.config.get('prefer_classes', True)
        self.avoid_indices = self.config.get('avoid_indices', False)
    
    async def generate_selector(self, element: Tag, soup: BeautifulSoup) -> str:
        """
        Generate the best CSS selector for the element.
        
        Args:
            element: Target BeautifulSoup Tag element
            soup: Full DOM tree for context
            
        Returns:
            CSS selector string
        """
        # Try different selector strategies in order of preference
        selectors = []
        
        # 1. ID-based selector (most reliable)
        id_selector = self._generate_id_selector(element)
        if id_selector:
            selectors.append(id_selector)
        
        # 2. Unique attribute selector
        attr_selector = self._generate_unique_attribute_selector(element, soup)
        if attr_selector:
            selectors.append(attr_selector)
        
        # 3. Class-based selector
        class_selector = self._generate_class_selector(element, soup)
        if class_selector:
            selectors.append(class_selector)
        
        # 4. Hierarchical selector
        hierarchical_selector = self._generate_hierarchical_selector(element, soup)
        if hierarchical_selector:
            selectors.append(hierarchical_selector)
        
        # 5. Text-based selector
        text_selector = self._generate_text_selector(element)
        if text_selector:
            selectors.append(text_selector)
        
        # 6. Fallback: nth-child selector
        if not selectors or self.config.get('include_nth_child', False):
            nth_selector = self._generate_nth_child_selector(element)
            if nth_selector:
                selectors.append(nth_selector)
        
        # Return the first (most reliable) selector
        return selectors[0] if selectors else self._generate_fallback_selector(element)
    
    def generate_all_selectors(self, element: Tag, soup: BeautifulSoup) -> List[str]:
        """
        Generate all possible CSS selectors for the element.
        
        Args:
            element: Target BeautifulSoup Tag element
            soup: Full DOM tree for context
            
        Returns:
            List of CSS selector strings
        """
        selectors = []
        
        # ID selector
        id_selector = self._generate_id_selector(element)
        if id_selector:
            selectors.append(id_selector)
        
        # Unique attribute selectors
        attr_selector = self._generate_unique_attribute_selector(element, soup)
        if attr_selector:
            selectors.append(attr_selector)
        
        # Class selectors
        class_selectors = self._generate_all_class_selectors(element, soup)
        selectors.extend(class_selectors)
        
        # Text selectors
        text_selector = self._generate_text_selector(element)
        if text_selector:
            selectors.append(text_selector)
        
        # Hierarchical selectors
        hierarchical_selectors = self._generate_hierarchical_selectors(element, soup)
        selectors.extend(hierarchical_selectors)
        
        # Remove duplicates while preserving order
        unique_selectors = []
        for selector in selectors:
            if selector not in unique_selectors:
                unique_selectors.append(selector)
        
        return unique_selectors
    
    def _generate_id_selector(self, element: Tag) -> Optional[str]:
        """Generate ID-based CSS selector."""
        element_id = element.get('id')
        if element_id and self._is_valid_id(element_id):
            return f"#{self._escape_css_identifier(element_id)}"
        return None
    
    def _generate_unique_attribute_selector(self, element: Tag, soup: BeautifulSoup) -> Optional[str]:
        """Generate selector based on unique attributes."""
        # Priority attributes for uniqueness
        unique_attrs = ['name', 'data-testid', 'data-cy', 'data-test', 'data-automation']
        
        for attr_name in unique_attrs:
            attr_value = element.get(attr_name)
            if attr_value:
                # Check if this attribute value is unique in the document
                selector = f"[{attr_name}=\"{self._escape_attribute_value(attr_value)}\"]"
                if self._is_selector_unique(selector, element, soup):
                    return selector
        
        # Try other data attributes
        for attr_name, attr_value in element.attrs.items():
            if attr_name.startswith('data-') and attr_name not in unique_attrs:
                selector = f"[{attr_name}=\"{self._escape_attribute_value(attr_value)}\"]"
                if self._is_selector_unique(selector, element, soup):
                    return selector
        
        return None
    
    def _generate_class_selector(self, element: Tag, soup: BeautifulSoup) -> Optional[str]:
        """Generate class-based CSS selector."""
        classes = element.get('class', [])
        if not classes:
            return None
        
        # Try single classes first
        for class_name in classes:
            if self._is_meaningful_class(class_name):
                selector = f".{self._escape_css_identifier(class_name)}"
                if self._is_selector_unique(selector, element, soup):
                    return selector
        
        # Try combinations of classes
        if len(classes) > 1:
            meaningful_classes = [c for c in classes if self._is_meaningful_class(c)]
            if meaningful_classes:
                class_selector = '.' + '.'.join(self._escape_css_identifier(c) for c in meaningful_classes)
                if self._is_selector_unique(class_selector, element, soup):
                    return class_selector
        
        return None
    
    def _generate_all_class_selectors(self, element: Tag, soup: BeautifulSoup) -> List[str]:
        """Generate all possible class-based selectors."""
        selectors = []
        classes = element.get('class', [])
        
        if not classes:
            return selectors
        
        # Single class selectors
        for class_name in classes:
            if self._is_meaningful_class(class_name):
                selector = f".{self._escape_css_identifier(class_name)}"
                selectors.append(selector)
        
        # Combined class selectors
        meaningful_classes = [c for c in classes if self._is_meaningful_class(c)]
        if len(meaningful_classes) > 1:
            # All combinations
            for i in range(2, len(meaningful_classes) + 1):
                from itertools import combinations
                for combo in combinations(meaningful_classes, i):
                    class_selector = '.' + '.'.join(self._escape_css_identifier(c) for c in combo)
                    selectors.append(class_selector)
        
        return selectors
    
    def _generate_hierarchical_selector(self, element: Tag, soup: BeautifulSoup) -> Optional[str]:
        """Generate hierarchical CSS selector."""
        parts = []
        current = element
        depth = 0
        
        while current and depth < self.max_depth:
            part = self._generate_element_part(current, soup)
            if part:
                parts.insert(0, part)
            
            # Move up the hierarchy
            current = current.parent
            depth += 1
            
            # Stop if we have a unique selector
            if parts:
                test_selector = ' > '.join(parts)
                if self._is_selector_unique(test_selector, element, soup):
                    return test_selector
        
        # Return the full path if no unique partial path found
        return ' > '.join(parts) if parts else None
    
    def _generate_hierarchical_selectors(self, element: Tag, soup: BeautifulSoup) -> List[str]:
        """Generate multiple hierarchical selectors with different strategies."""
        selectors = []
        
        # Direct child selector
        direct_selector = self._generate_hierarchical_selector(element, soup)
        if direct_selector:
            selectors.append(direct_selector)
        
        # Descendant selector (with spaces)
        descendant_selector = self._generate_descendant_selector(element, soup)
        if descendant_selector:
            selectors.append(descendant_selector)
        
        return selectors
    
    def _generate_descendant_selector(self, element: Tag, soup: BeautifulSoup) -> Optional[str]:
        """Generate descendant-based CSS selector."""
        parts = []
        current = element
        depth = 0
        
        while current and depth < self.max_depth:
            part = self._generate_element_part(current, soup)
            if part:
                parts.insert(0, part)
            
            current = current.parent
            depth += 1
            
            # Test with descendant combinator
            if len(parts) >= 2:
                test_selector = ' '.join(parts)
                if self._is_selector_unique(test_selector, element, soup):
                    return test_selector
        
        return ' '.join(parts) if len(parts) >= 2 else None
    
    def _generate_text_selector(self, element: Tag) -> Optional[str]:
        """Generate text-based CSS selector."""
        text_content = element.get_text(strip=True)
        if not text_content or len(text_content) > 50:  # Avoid very long text
            return None
        
        # For specific element types with text
        if element.name == 'a':
            return f"a:contains('{self._escape_text_content(text_content)}')"
        elif element.name == 'button':
            return f"button:contains('{self._escape_text_content(text_content)}')"
        elif element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            return f"{element.name}:contains('{self._escape_text_content(text_content)}')"
        
        return None
    
    def _generate_nth_child_selector(self, element: Tag) -> Optional[str]:
        """Generate nth-child CSS selector."""
        if not element.parent:
            return None
        
        # Find position among siblings of same type
        siblings = [child for child in element.parent.children 
                   if hasattr(child, 'name') and child.name == element.name]
        
        try:
            position = siblings.index(element) + 1  # CSS is 1-based
            return f"{element.name}:nth-child({position})"
        except ValueError:
            return None
    
    def _generate_element_part(self, element: Tag, soup: BeautifulSoup) -> Optional[str]:
        """Generate CSS selector part for a single element."""
        parts = [element.name]
        
        # Add ID if available
        if element.get('id') and self.prefer_ids:
            return f"{element.name}#{self._escape_css_identifier(element.get('id'))}"
        
        # Add classes if available and meaningful
        classes = element.get('class', [])
        meaningful_classes = [c for c in classes if self._is_meaningful_class(c)]
        
        if meaningful_classes and self.prefer_classes:
            # Use first meaningful class
            class_part = f".{self._escape_css_identifier(meaningful_classes[0])}"
            test_selector = f"{element.name}{class_part}"
            
            # Check if this makes the selector more specific
            if len(soup.select(test_selector)) < len(soup.select(element.name)):
                parts.append(class_part)
        
        return ''.join(parts) if parts else None
    
    def _generate_fallback_selector(self, element: Tag) -> str:
        """Generate a fallback selector when all else fails."""
        return element.name
    
    def _is_selector_unique(self, selector: str, target_element: Tag, soup: BeautifulSoup) -> bool:
        """Check if selector uniquely identifies the target element."""
        try:
            selected_elements = soup.select(selector)
            return len(selected_elements) == 1 and selected_elements[0] == target_element
        except Exception:
            return False
    
    def _is_meaningful_class(self, class_name: str) -> bool:
        """Check if a class name is meaningful for CSS selection."""
        # Avoid generated/random class names
        if len(class_name) < 2:
            return False
        
        # Avoid classes that look like generated IDs
        if re.match(r'^[a-f0-9]{8,}$', class_name.lower()):
            return False
        
        # Avoid utility classes that are likely to be non-unique
        utility_patterns = [
            r'^(hidden|visible|flex|block|inline)$',
            r'^(mt?|mb?|ml?|mr?|pt?|pb?|pl?|pr?)-?\d+$',  # Margin/padding utilities
            r'^(w|h)-?\d+$',  # Width/height utilities
            r'^text-(left|right|center)$',
            r'^bg-\w+$',  # Background utilities
            r'^text-\w+$',  # Text color utilities
        ]
        
        for pattern in utility_patterns:
            if re.match(pattern, class_name, re.IGNORECASE):
                return False
        
        return True
    
    def _is_valid_id(self, element_id: str) -> bool:
        """Check if an ID is valid and meaningful."""
        if not element_id or len(element_id) < 1:
            return False
        
        # Check CSS identifier validity
        if not re.match(r'^[a-zA-Z][\w-]*$', element_id):
            return False
        
        return True
    
    def _escape_css_identifier(self, identifier: str) -> str:
        """Escape CSS identifier for use in selectors."""
        # Basic escaping - in practice might need more sophisticated escaping
        return re.sub(r'([^a-zA-Z0-9_-])', r'\\\1', identifier)
    
    def _escape_attribute_value(self, value: str) -> str:
        """Escape attribute value for use in selectors."""
        return value.replace('"', '\\"').replace("'", "\\'")
    
    def _escape_text_content(self, text: str) -> str:
        """Escape text content for use in selectors."""
        return text.replace("'", "\\'").replace('"', '\\"')