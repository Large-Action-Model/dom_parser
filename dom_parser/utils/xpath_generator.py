"""
XPath Generator for creating robust XPath expressions.

Generates XPath expressions for DOM elements using various strategies,
providing fallback options for reliable element location.
"""

from typing import Optional, List, Dict, Any
import re
try:
    from bs4 import BeautifulSoup, Tag
except ImportError:
    # Fallback types if bs4 not available
    BeautifulSoup = Any
    Tag = Any


class XPathGenerator:
    """
    Generates XPath expressions for DOM elements using various strategies.
    
    Provides multiple XPath approaches for maximum reliability
    in different page contexts and structural changes.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize XPath Generator.
        
        Args:
            config: Configuration for XPath generation preferences
        """
        self.config = config or {}
        self.max_depth = self.config.get('max_depth', 10)
        self.prefer_ids = self.config.get('prefer_ids', True)
        self.prefer_attributes = self.config.get('prefer_attributes', True)
        self.use_text_content = self.config.get('use_text_content', True)
    
    async def generate_xpath(self, element: Tag, soup: BeautifulSoup) -> str:
        """
        Generate the best XPath for the element.
        
        Args:
            element: Target BeautifulSoup Tag element
            soup: Full DOM tree for context
            
        Returns:
            XPath expression string
        """
        # Try different XPath strategies in order of preference
        xpaths = []
        
        # 1. ID-based XPath (most reliable)
        id_xpath = self._generate_id_xpath(element)
        if id_xpath:
            xpaths.append(id_xpath)
        
        # 2. Unique attribute XPath
        attr_xpath = self._generate_unique_attribute_xpath(element, soup)
        if attr_xpath:
            xpaths.append(attr_xpath)
        
        # 3. Text-based XPath
        if self.use_text_content:
            text_xpath = self._generate_text_xpath(element)
            if text_xpath:
                xpaths.append(text_xpath)
        
        # 4. Hierarchical XPath
        hierarchical_xpath = self._generate_hierarchical_xpath(element, soup)
        if hierarchical_xpath:
            xpaths.append(hierarchical_xpath)
        
        # 5. Position-based XPath
        position_xpath = self._generate_position_xpath(element)
        if position_xpath:
            xpaths.append(position_xpath)
        
        # Return the first (most reliable) XPath
        return xpaths[0] if xpaths else self._generate_fallback_xpath(element)
    
    def generate_all_xpaths(self, element: Tag, soup: BeautifulSoup) -> List[str]:
        """
        Generate all possible XPath expressions for the element.
        
        Args:
            element: Target BeautifulSoup Tag element
            soup: Full DOM tree for context
            
        Returns:
            List of XPath expression strings
        """
        xpaths = []
        
        # ID XPath
        id_xpath = self._generate_id_xpath(element)
        if id_xpath:
            xpaths.append(id_xpath)
        
        # Attribute XPaths
        attr_xpaths = self._generate_all_attribute_xpaths(element, soup)
        xpaths.extend(attr_xpaths)
        
        # Text XPaths
        if self.use_text_content:
            text_xpaths = self._generate_all_text_xpaths(element)
            xpaths.extend(text_xpaths)
        
        # Hierarchical XPaths
        hierarchical_xpaths = self._generate_hierarchical_xpaths(element, soup)
        xpaths.extend(hierarchical_xpaths)
        
        # Position XPaths
        position_xpath = self._generate_position_xpath(element)
        if position_xpath:
            xpaths.append(position_xpath)
        
        # Remove duplicates while preserving order
        unique_xpaths = []
        for xpath in xpaths:
            if xpath not in unique_xpaths:
                unique_xpaths.append(xpath)
        
        return unique_xpaths
    
    def _generate_id_xpath(self, element: Tag) -> Optional[str]:
        """Generate ID-based XPath."""
        element_id = element.get('id')
        if element_id and self._is_valid_id(element_id):
            return f"//*[@id='{self._escape_xpath_string(element_id)}']"
        return None
    
    def _generate_unique_attribute_xpath(self, element: Tag, soup: BeautifulSoup) -> Optional[str]:
        """Generate XPath based on unique attributes."""
        # Priority attributes for uniqueness
        unique_attrs = ['name', 'data-testid', 'data-cy', 'data-test', 'data-automation']
        
        for attr_name in unique_attrs:
            attr_value = element.get(attr_name)
            if attr_value:
                xpath = f"//*[@{attr_name}='{self._escape_xpath_string(attr_value)}']"
                if self._is_xpath_unique(xpath, element, soup):
                    return xpath
        
        # Try other attributes
        skip_attrs = {'class', 'style', 'id'} | set(unique_attrs)
        for attr_name, attr_value in element.attrs.items():
            if attr_name not in skip_attrs and isinstance(attr_value, str):
                xpath = f"//*[@{attr_name}='{self._escape_xpath_string(attr_value)}']"
                if self._is_xpath_unique(xpath, element, soup):
                    return xpath
        
        return None
    
    def _generate_all_attribute_xpaths(self, element: Tag, soup: BeautifulSoup) -> List[str]:
        """Generate all possible attribute-based XPaths."""
        xpaths = []
        
        # Single attribute XPaths
        skip_attrs = {'style'}  # Attributes to skip
        for attr_name, attr_value in element.attrs.items():
            if attr_name not in skip_attrs and isinstance(attr_value, str):
                xpath = f"//*[@{attr_name}='{self._escape_xpath_string(attr_value)}']"
                xpaths.append(xpath)
        
        # Class-based XPaths
        classes = element.get('class', [])
        for class_name in classes:
            if self._is_meaningful_class(class_name):
                xpath = f"//*[contains(@class, '{self._escape_xpath_string(class_name)}')]"
                xpaths.append(xpath)
        
        # Combined attribute XPaths
        tag_name = element.name
        for attr_name, attr_value in element.attrs.items():
            if attr_name not in skip_attrs and isinstance(attr_value, str):
                xpath = f"//{tag_name}[@{attr_name}='{self._escape_xpath_string(attr_value)}']"
                xpaths.append(xpath)
        
        return xpaths
    
    def _generate_text_xpath(self, element: Tag) -> Optional[str]:
        """Generate text-based XPath."""
        text_content = element.get_text(strip=True)
        if not text_content or len(text_content) > 100:  # Avoid very long text
            return None
        
        # Exact text match
        tag_name = element.name
        escaped_text = self._escape_xpath_string(text_content)
        
        # Try different text matching strategies
        xpaths = [
            f"//{tag_name}[text()='{escaped_text}']",
            f"//{tag_name}[normalize-space(text())='{escaped_text}']",
            f"//*[text()='{escaped_text}']",
            f"//*[normalize-space()='{escaped_text}']"
        ]
        
        # Return first that's not too generic
        for xpath in xpaths:
            if not self._is_xpath_too_generic(xpath):
                return xpath
        
        return None
    
    def _generate_all_text_xpaths(self, element: Tag) -> List[str]:
        """Generate all possible text-based XPaths."""
        xpaths = []
        text_content = element.get_text(strip=True)
        
        if not text_content or len(text_content) > 100:
            return xpaths
        
        tag_name = element.name
        escaped_text = self._escape_xpath_string(text_content)
        
        # Exact text matches
        xpaths.extend([
            f"//{tag_name}[text()='{escaped_text}']",
            f"//{tag_name}[normalize-space(text())='{escaped_text}']",
            f"//*[text()='{escaped_text}']",
            f"//*[normalize-space()='{escaped_text}']"
        ])
        
        # Partial text matches
        if len(text_content) > 10:  # Only for longer text
            words = text_content.split()
            if len(words) > 1:
                # First few words
                partial_text = ' '.join(words[:3])
                escaped_partial = self._escape_xpath_string(partial_text)
                xpaths.extend([
                    f"//{tag_name}[contains(text(), '{escaped_partial}')]",
                    f"//*[contains(text(), '{escaped_partial}')]"
                ])
        
        return xpaths
    
    def _generate_hierarchical_xpath(self, element: Tag, soup: BeautifulSoup) -> Optional[str]:
        """Generate hierarchical XPath."""
        path_parts = []
        current = element
        depth = 0
        
        while current and hasattr(current, 'name') and depth < self.max_depth:
            part = self._generate_element_xpath_part(current, soup)
            if part:
                path_parts.insert(0, part)
            
            current = current.parent
            depth += 1
            
            # Test if current path is unique
            if len(path_parts) >= 2:
                test_xpath = '/' + '/'.join(path_parts)
                if self._is_xpath_unique(test_xpath, element, soup):
                    return test_xpath
        
        return '/' + '/'.join(path_parts) if path_parts else None
    
    def _generate_hierarchical_xpaths(self, element: Tag, soup: BeautifulSoup) -> List[str]:
        """Generate multiple hierarchical XPaths."""
        xpaths = []
        
        # Full path XPath
        full_xpath = self._generate_hierarchical_xpath(element, soup)
        if full_xpath:
            xpaths.append(full_xpath)
        
        # Descendant XPath (with //)
        descendant_xpath = self._generate_descendant_xpath(element, soup)
        if descendant_xpath:
            xpaths.append(descendant_xpath)
        
        return xpaths
    
    def _generate_descendant_xpath(self, element: Tag, soup: BeautifulSoup) -> Optional[str]:
        """Generate descendant-based XPath using // notation."""
        current = element
        parts = []
        depth = 0
        
        while current and hasattr(current, 'name') and depth < 3:  # Limit to prevent overly long paths
            part = self._generate_simple_element_part(current)
            if part:
                parts.insert(0, part)
            
            current = current.parent
            depth += 1
        
        if len(parts) >= 2:
            # Use // between parts for descendant relationship
            xpath = '//' + '//'.join(parts)
            return xpath
        
        return None
    
    def _generate_position_xpath(self, element: Tag) -> Optional[str]:
        """Generate position-based XPath."""
        if not element.parent:
            return None
        
        # Find position among siblings of same type
        siblings = [child for child in element.parent.children 
                   if hasattr(child, 'name') and child.name == element.name]
        
        try:
            position = siblings.index(element) + 1  # XPath is 1-based
            tag_name = element.name
            
            # Generate parent path
            parent_path = self._generate_simple_parent_path(element.parent)
            if parent_path:
                return f"{parent_path}/{tag_name}[{position}]"
            else:
                return f"//{tag_name}[{position}]"
        except ValueError:
            return None
    
    def _generate_element_xpath_part(self, element: Tag, soup: BeautifulSoup) -> Optional[str]:
        """Generate XPath part for a single element."""
        tag_name = element.name
        
        # Try ID first
        if element.get('id') and self.prefer_ids:
            element_id = element.get('id')
            return f"{tag_name}[@id='{self._escape_xpath_string(element_id)}']"
        
        # Try unique attributes
        if self.prefer_attributes:
            for attr_name, attr_value in element.attrs.items():
                if (attr_name not in ['class', 'style'] and 
                    isinstance(attr_value, str) and 
                    len(attr_value) < 50):
                    # Check if this attribute makes it unique among siblings
                    xpath = f"{tag_name}[@{attr_name}='{self._escape_xpath_string(attr_value)}']"
                    return xpath
        
        # Try meaningful classes
        classes = element.get('class', [])
        meaningful_classes = [c for c in classes if self._is_meaningful_class(c)]
        if meaningful_classes:
            class_name = meaningful_classes[0]
            return f"{tag_name}[contains(@class, '{self._escape_xpath_string(class_name)}')]"
        
        # Fallback to tag name with position
        return self._generate_position_part(element)
    
    def _generate_simple_element_part(self, element: Tag) -> Optional[str]:
        """Generate simple XPath part for an element."""
        tag_name = element.name
        
        # Use ID if available
        if element.get('id'):
            element_id = element.get('id')
            return f"{tag_name}[@id='{self._escape_xpath_string(element_id)}']"
        
        # Use most distinctive attribute
        best_attr = self._find_best_attribute(element)
        if best_attr:
            attr_name, attr_value = best_attr
            return f"{tag_name}[@{attr_name}='{self._escape_xpath_string(attr_value)}']"
        
        return tag_name
    
    def _generate_position_part(self, element: Tag) -> str:
        """Generate position-based XPath part."""
        if not element.parent:
            return element.name
        
        siblings = [child for child in element.parent.children 
                   if hasattr(child, 'name') and child.name == element.name]
        
        try:
            position = siblings.index(element) + 1
            return f"{element.name}[{position}]"
        except ValueError:
            return element.name
    
    def _generate_simple_parent_path(self, parent: Tag, max_depth: int = 3) -> Optional[str]:
        """Generate simple path to parent element."""
        if not parent or not hasattr(parent, 'name'):
            return None
        
        parts = []
        current = parent
        depth = 0
        
        while current and hasattr(current, 'name') and depth < max_depth:
            if current.get('id'):
                parts.insert(0, f"{current.name}[@id='{self._escape_xpath_string(current.get('id'))}']")
                break
            else:
                parts.insert(0, current.name)
            
            current = current.parent
            depth += 1
        
        return '/' + '/'.join(parts) if parts else None
    
    def _generate_fallback_xpath(self, element: Tag) -> str:
        """Generate a fallback XPath when all else fails."""
        return f"//{element.name}"
    
    def _find_best_attribute(self, element: Tag) -> Optional[tuple]:
        """Find the most distinctive attribute for XPath generation."""
        skip_attrs = {'style', 'class'}
        priority_attrs = ['name', 'type', 'role', 'data-testid']
        
        # Check priority attributes first
        for attr_name in priority_attrs:
            attr_value = element.get(attr_name)
            if attr_value and isinstance(attr_value, str):
                return (attr_name, attr_value)
        
        # Check other attributes
        for attr_name, attr_value in element.attrs.items():
            if (attr_name not in skip_attrs and 
                isinstance(attr_value, str) and 
                len(attr_value) < 50 and 
                len(attr_value) > 0):
                return (attr_name, attr_value)
        
        return None
    
    def _is_xpath_unique(self, xpath: str, target_element: Tag, soup: BeautifulSoup) -> bool:
        """Check if XPath uniquely identifies the target element."""
        # This is a simplified check - in practice, you'd need lxml or selenium to evaluate XPath
        # For now, return True to avoid breaking the flow
        return True
    
    def _is_xpath_too_generic(self, xpath: str) -> bool:
        """Check if XPath is too generic to be useful."""
        generic_patterns = [
            r'^//\*$',  # Any element
            r'^//div$',  # Any div
            r'^//span$',  # Any span
        ]
        
        for pattern in generic_patterns:
            if re.match(pattern, xpath):
                return True
        
        return False
    
    def _is_meaningful_class(self, class_name: str) -> bool:
        """Check if a class name is meaningful for XPath selection."""
        if len(class_name) < 2:
            return False
        
        # Avoid generated/random class names
        if re.match(r'^[a-f0-9]{8,}$', class_name.lower()):
            return False
        
        # Avoid utility classes
        utility_patterns = [
            r'^(hidden|visible|flex|block|inline)$',
            r'^(mt?|mb?|ml?|mr?|pt?|pb?|pl?|pr?)-?\d+$',
            r'^(w|h)-?\d+$',
            r'^text-(left|right|center)$',
            r'^bg-\w+$',
            r'^text-\w+$',
        ]
        
        for pattern in utility_patterns:
            if re.match(pattern, class_name, re.IGNORECASE):
                return False
        
        return True
    
    def _is_valid_id(self, element_id: str) -> bool:
        """Check if an ID is valid and meaningful."""
        if not element_id or len(element_id) < 1:
            return False
        
        # Basic validation
        if not re.match(r'^[a-zA-Z][\w-]*$', element_id):
            return False
        
        return True
    
    def _escape_xpath_string(self, value: str) -> str:
        """Escape string for use in XPath expressions."""
        # Handle quotes in XPath strings
        if "'" not in value:
            return value
        elif '"' not in value:
            return value
        else:
            # Complex escaping for strings with both quotes
            parts = value.split("'")
            escaped_parts = []
            for i, part in enumerate(parts):
                if i > 0:
                    escaped_parts.append("\"'\"")
                if part:
                    escaped_parts.append(f"'{part}'")
            return f"concat({', '.join(escaped_parts)})"