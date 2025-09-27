"""
Element Classifier for intelligent identification of interactive elements.

Analyzes DOM elements to classify them into interactive vs content elements,
determines interaction capabilities, and provides semantic meaning.
"""

import re
import uuid
from typing import List, Dict, Any, Optional, Set
from bs4 import BeautifulSoup, Tag

from ..types.dom_data_types import (
    InteractiveElement, AccessibilityInfo, ElementHierarchy
)
from ..types.element_data_types import (
    ElementType, InteractionType, SemanticType, FormFieldType,
    HTML_TAG_TO_ELEMENT_TYPE, INPUT_TYPE_TO_FORM_FIELD_TYPE,
    get_interactive_element_types
)
from ..utils.css_selector_generator import CSSSelectorsGenerator
from ..utils.xpath_generator import XPathGenerator


class ElementClassifier:
    """
    Classifies DOM elements into interactive and content types.
    
    Provides intelligent analysis of element capabilities, semantic meaning,
    and interaction patterns for AI-driven web automation.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Element Classifier with configuration.
        
        Args:
            config: Configuration dictionary for classifier behavior
        """
        self.config = config or {}
        
        # Initialize utility generators
        self.css_generator = CSSSelectorsGenerator()
        self.xpath_generator = XPathGenerator()
        
        # Classification thresholds and rules
        self.min_text_length = self.config.get('min_text_length', 3)
        self.confidence_threshold = self.config.get('confidence_threshold', 0.7)
        self.include_hidden_elements = self.config.get('include_hidden_elements', False)
        
        # Interactive element indicators
        self.interactive_attributes = {
            'onclick', 'onmousedown', 'onmouseup', 'onkeypress', 'onkeydown',
            'href', 'data-toggle', 'data-target', 'data-dismiss', 'role'
        }
        
        # Semantic classification patterns
        self.semantic_patterns = self._load_semantic_patterns()
    
    async def classify_elements(self, soup: BeautifulSoup) -> List[InteractiveElement]:
        """
        Classify all elements in the DOM tree.
        
        Args:
            soup: BeautifulSoup DOM tree
            
        Returns:
            List of classified interactive elements
        """
        interactive_elements = []
        
        # Find all potentially interactive elements
        all_elements = soup.find_all()
        
        for element in all_elements:
            if not isinstance(element, Tag):
                continue
            
            # Skip if element is hidden and we're not including hidden elements
            if not self.include_hidden_elements and self._is_hidden_element(element):
                continue
            
            # Classify the element
            classified_element = await self._classify_single_element(element, soup)
            
            if classified_element:
                interactive_elements.append(classified_element)
        
        # Build element relationships
        await self._build_element_relationships(interactive_elements, soup)
        
        return interactive_elements
    
    async def _classify_single_element(self, element: Tag, soup: BeautifulSoup) -> Optional[InteractiveElement]:
        """
        Classify a single DOM element.
        
        Args:
            element: BeautifulSoup Tag element
            soup: Full DOM tree for context
            
        Returns:
            InteractiveElement if element is interactive, None otherwise
        """
        # Determine basic element type
        element_type = self._get_element_type(element)
        
        # Skip non-interactive elements unless they have interactive attributes
        if (element_type not in get_interactive_element_types() and 
            not self._has_interactive_attributes(element)):
            return None
        
        # Generate unique element ID
        element_id = self._generate_element_id(element)
        
        # Generate locators
        locators = await self._generate_locators(element, soup)
        
        # Extract element properties
        properties = self._extract_element_properties(element)
        attributes = dict(element.attrs) if element.attrs else {}
        
        # Determine interaction types
        interaction_types = self._determine_interaction_types(element, element_type)
        
        # Generate interaction hints
        interaction_hints = self._generate_interaction_hints(element, interaction_types)
        
        # Extract text content
        text_content = self._extract_text_content(element)
        visible_text = self._extract_visible_text(element)
        
        # Get form field type if applicable
        form_field_type = self._get_form_field_type(element)
        
        # Determine semantic type
        semantic_type = self._determine_semantic_type(element, text_content)
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(element, element_type, semantic_type)
        
        # Extract accessibility information
        accessibility_info = self._extract_accessibility_info(element)
        
        # Get bounding box if available
        bounding_box = self._get_bounding_box(element)
        
        # Determine visibility and state
        is_visible = not self._is_hidden_element(element)
        is_enabled = not self._is_disabled_element(element)
        
        # Create InteractiveElement
        interactive_element = InteractiveElement(
            element_id=element_id,
            element_type=element_type,
            tag_name=element.name,
            locators=locators,
            properties=properties,
            attributes=attributes,
            interaction_types=interaction_types,
            interaction_hints=interaction_hints,
            text_content=text_content,
            visible_text=visible_text,
            placeholder=element.get('placeholder'),
            value=element.get('value'),
            bounding_box=bounding_box,
            is_visible=is_visible,
            is_enabled=is_enabled,
            accessibility_info=accessibility_info,
            form_field_type=form_field_type,
            semantic_type=semantic_type,
            confidence_score=confidence_score
        )
        
        return interactive_element
    
    def _get_element_type(self, element: Tag) -> ElementType:
        """
        Determine the basic element type from the HTML tag.
        
        Args:
            element: BeautifulSoup Tag element
            
        Returns:
            ElementType enum value
        """
        tag_name = element.name.lower()
        
        # Handle input elements with specific types
        if tag_name == 'input':
            input_type = element.get('type', 'text').lower()
            if input_type in ['checkbox']:
                return ElementType.CHECKBOX
            elif input_type in ['radio']:
                return ElementType.RADIO
            elif input_type in ['file']:
                return ElementType.FILE_INPUT
            elif input_type in ['submit', 'button']:
                return ElementType.SUBMIT
            else:
                return ElementType.INPUT
        
        # Use the mapping for other elements
        return HTML_TAG_TO_ELEMENT_TYPE.get(tag_name, ElementType.UNKNOWN)
    
    def _has_interactive_attributes(self, element: Tag) -> bool:
        """
        Check if element has attributes that make it interactive.
        
        Args:
            element: BeautifulSoup Tag element
            
        Returns:
            True if element has interactive attributes
        """
        if not element.attrs:
            return False
        
        # Check for known interactive attributes
        for attr in self.interactive_attributes:
            if attr in element.attrs:
                return True
        
        # Check for role attributes that indicate interactivity
        role = element.get('role', '').lower()
        interactive_roles = {'button', 'link', 'menuitem', 'tab', 'option', 'checkbox', 'radio'}
        if role in interactive_roles:
            return True
        
        # Check for CSS classes that suggest interactivity
        css_classes = element.get('class', [])
        if isinstance(css_classes, str):
            css_classes = css_classes.split()
        
        interactive_class_patterns = ['btn', 'button', 'link', 'click', 'toggle', 'submit']
        for class_name in css_classes:
            for pattern in interactive_class_patterns:
                if pattern in class_name.lower():
                    return True
        
        return False
    
    def _generate_element_id(self, element: Tag) -> str:
        """
        Generate a unique ID for the element.
        
        Args:
            element: BeautifulSoup Tag element
            
        Returns:
            Unique element identifier
        """
        # Use existing ID if available
        if element.get('id'):
            return f"id_{element.get('id')}"
        
        # Use name if available
        if element.get('name'):
            return f"name_{element.get('name')}"
        
        # Generate based on tag and position
        tag_name = element.name
        
        # Find position among siblings of same type
        siblings = element.parent.find_all(tag_name) if element.parent else [element]
        position = siblings.index(element) if element in siblings else 0
        
        # Create a more descriptive ID
        base_id = f"{tag_name}_{position}"
        
        # Add distinguishing characteristics
        if element.get('class'):
            classes = ' '.join(element.get('class'))
            # Use first class as part of ID
            first_class = element.get('class')[0]
            base_id += f"_{first_class}"
        
        if element.get('type'):
            base_id += f"_{element.get('type')}"
        
        # Add text content for uniqueness (truncated)
        text = self._extract_text_content(element)
        if text and len(text) > 3:
            # Use first few words
            words = text.split()[:2]
            text_part = '_'.join(words).lower()
            # Clean for ID usage
            text_part = re.sub(r'[^a-zA-Z0-9_]', '', text_part)
            if text_part:
                base_id += f"_{text_part}"
        
        return base_id[:100]  # Limit length
    
    async def _generate_locators(self, element: Tag, soup: BeautifulSoup) -> Dict[str, str]:
        """
        Generate multiple locator strategies for the element.
        
        Args:
            element: BeautifulSoup Tag element
            soup: Full DOM tree for context
            
        Returns:
            Dictionary of locator strategies
        """
        locators = {}
        
        # ID locator
        if element.get('id'):
            locators['id'] = f"#{element.get('id')}"
            locators['css'] = f"#{element.get('id')}"
            locators['xpath'] = f"//*[@id='{element.get('id')}']"
        
        # Name locator
        if element.get('name'):
            locators['name'] = element.get('name')
            locators['css_name'] = f"[name='{element.get('name')}']"
            locators['xpath_name'] = f"//*[@name='{element.get('name')}']"
        
        # Class-based locator
        if element.get('class'):
            classes = '.'.join(element.get('class'))
            locators['css_class'] = f".{classes}"
        
        # Generate CSS selector
        css_selector = await self.css_generator.generate_selector(element, soup)
        if css_selector:
            locators['css_generated'] = css_selector
        
        # Generate XPath
        xpath = await self.xpath_generator.generate_xpath(element, soup)
        if xpath:
            locators['xpath_generated'] = xpath
        
        # Text-based locators
        text_content = self._extract_text_content(element)
        if text_content and len(text_content.strip()) > 0:
            if element.name == 'a':
                locators['link_text'] = text_content.strip()
            elif element.name in ['button', 'input'] and element.get('type') in ['submit', 'button']:
                locators['button_text'] = text_content.strip()
        
        # Attribute-based locators
        for attr_name, attr_value in element.attrs.items():
            if attr_name in ['data-testid', 'data-cy', 'data-test']:
                locators[f'attr_{attr_name}'] = f"[{attr_name}='{attr_value}']"
        
        return locators
    
    def _extract_element_properties(self, element: Tag) -> Dict[str, Any]:
        """
        Extract element properties and characteristics.
        
        Args:
            element: BeautifulSoup Tag element
            
        Returns:
            Dictionary of element properties
        """
        properties = {
            'tag_name': element.name,
            'has_children': len(list(element.children)) > 0,
            'is_self_closing': element.name in ['img', 'input', 'br', 'hr', 'meta', 'link'],
            'attribute_count': len(element.attrs) if element.attrs else 0,
        }
        
        # Form-specific properties
        if element.name == 'input':
            properties['input_type'] = element.get('type', 'text')
            properties['required'] = element.has_attr('required')
            properties['readonly'] = element.has_attr('readonly')
            properties['multiple'] = element.has_attr('multiple')
        
        # Link-specific properties
        if element.name == 'a':
            href = element.get('href', '')
            properties['is_external_link'] = href.startswith('http') and 'http' in href
            properties['is_anchor_link'] = href.startswith('#')
            properties['is_mailto'] = href.startswith('mailto:')
            properties['is_tel'] = href.startswith('tel:')
        
        # Form association
        if element.get('form'):
            properties['associated_form'] = element.get('form')
        
        return properties
    
    def _determine_interaction_types(self, element: Tag, element_type: ElementType) -> List[InteractionType]:
        """
        Determine what types of interactions are possible with the element.
        
        Args:
            element: BeautifulSoup Tag element
            element_type: Classified element type
            
        Returns:
            List of possible interaction types
        """
        interactions = []
        
        # Click interactions
        if element_type in [ElementType.BUTTON, ElementType.LINK, ElementType.SUBMIT]:
            interactions.append(InteractionType.CLICK)
        
        if element.get('onclick') or element.get('role') == 'button':
            interactions.append(InteractionType.CLICK)
        
        # Type interactions
        if element_type in [ElementType.INPUT, ElementType.TEXTAREA]:
            input_type = element.get('type', 'text').lower()
            if input_type not in ['submit', 'button', 'checkbox', 'radio', 'file']:
                interactions.append(InteractionType.TYPE)
        
        # Select interactions
        if element_type == ElementType.SELECT:
            interactions.append(InteractionType.SELECT)
            if element.get('multiple'):
                interactions.append(InteractionType.MULTI_SELECT)
        
        if element_type in [ElementType.CHECKBOX, ElementType.RADIO]:
            interactions.append(InteractionType.SELECT)
        
        # Special input types
        input_type = element.get('type', '').lower()
        if input_type == 'file':
            interactions.append(InteractionType.UPLOAD)
        elif input_type == 'range':
            interactions.append(InteractionType.RANGE_SELECT)
        elif input_type == 'color':
            interactions.append(InteractionType.COLOR_PICK)
        elif input_type in ['date', 'datetime-local', 'time']:
            interactions.append(InteractionType.DATE_PICK)
        
        # Hover interactions for elements with titles or complex content
        if element.get('title') or element.name in ['abbr', 'acronym']:
            interactions.append(InteractionType.HOVER)
        
        # Focus interactions for form elements
        if element.name in ['input', 'textarea', 'select', 'button']:
            interactions.append(InteractionType.FOCUS)
            interactions.append(InteractionType.BLUR)
        
        # Submit interactions for forms
        if element.name == 'form' or (element.name == 'input' and element.get('type') == 'submit'):
            interactions.append(InteractionType.SUBMIT)
        
        # Navigation for links
        if element.name == 'a' and element.get('href'):
            interactions.append(InteractionType.NAVIGATE)
        
        return interactions
    
    def _generate_interaction_hints(self, element: Tag, interaction_types: List[InteractionType]) -> List[str]:
        """
        Generate hints for how to interact with the element.
        
        Args:
            element: BeautifulSoup Tag element
            interaction_types: List of possible interactions
            
        Returns:
            List of interaction hints
        """
        hints = []
        
        # Click hints
        if InteractionType.CLICK in interaction_types:
            if element.name == 'button':
                hints.append("Click to activate button")
            elif element.name == 'a':
                href = element.get('href', '')
                if href.startswith('#'):
                    hints.append("Click to navigate to page section")
                elif href.startswith('mailto:'):
                    hints.append("Click to send email")
                elif href.startswith('tel:'):
                    hints.append("Click to make phone call")
                else:
                    hints.append("Click to navigate to URL")
            else:
                hints.append("Element is clickable")
        
        # Type hints
        if InteractionType.TYPE in interaction_types:
            input_type = element.get('type', 'text').lower()
            placeholder = element.get('placeholder', '')
            
            if input_type == 'email':
                hints.append("Enter email address")
            elif input_type == 'password':
                hints.append("Enter password")
            elif input_type == 'search':
                hints.append("Enter search query")
            elif input_type == 'number':
                hints.append("Enter numeric value")
            elif placeholder:
                hints.append(f"Enter {placeholder}")
            else:
                hints.append("Enter text")
        
        # Select hints
        if InteractionType.SELECT in interaction_types:
            if element.name == 'select':
                if element.get('multiple'):
                    hints.append("Select one or more options")
                else:
                    hints.append("Select an option")
            elif element.get('type') == 'checkbox':
                hints.append("Check or uncheck")
            elif element.get('type') == 'radio':
                hints.append("Select radio option")
        
        # Upload hints
        if InteractionType.UPLOAD in interaction_types:
            accept = element.get('accept', '')
            if 'image' in accept:
                hints.append("Upload image file")
            elif accept:
                hints.append(f"Upload file ({accept})")
            else:
                hints.append("Upload file")
        
        return hints
    
    def _extract_text_content(self, element: Tag) -> str:
        """
        Extract all text content from the element.
        
        Args:
            element: BeautifulSoup Tag element
            
        Returns:
            Text content as string
        """
        return element.get_text(strip=True)
    
    def _extract_visible_text(self, element: Tag) -> str:
        """
        Extract only visible text content.
        
        Args:
            element: BeautifulSoup Tag element
            
        Returns:
            Visible text content as string
        """
        # For now, same as text content - could be enhanced to check CSS visibility
        return self._extract_text_content(element)
    
    def _get_form_field_type(self, element: Tag) -> Optional[FormFieldType]:
        """
        Determine the form field type if element is a form field.
        
        Args:
            element: BeautifulSoup Tag element
            
        Returns:
            FormFieldType if applicable, None otherwise
        """
        if element.name == 'input':
            input_type = element.get('type', 'text').lower()
            return INPUT_TYPE_TO_FORM_FIELD_TYPE.get(input_type)
        elif element.name == 'textarea':
            return FormFieldType.TEXTAREA
        elif element.name == 'select':
            if element.get('multiple'):
                return FormFieldType.MULTISELECT
            else:
                return FormFieldType.SELECT
        elif element.name == 'button':
            return FormFieldType.BUTTON
        
        return None
    
    def _determine_semantic_type(self, element: Tag, text_content: str) -> Optional[SemanticType]:
        """
        Determine the semantic type of the element.
        
        Args:
            element: BeautifulSoup Tag element
            text_content: Element's text content
            
        Returns:
            SemanticType if determinable, None otherwise
        """
        # Check element attributes for semantic hints
        element_id = element.get('id', '').lower()
        element_classes = ' '.join(element.get('class', [])).lower()
        text_lower = text_content.lower()
        
        # Search forms
        search_indicators = ['search', 'query', 'find']
        if any(indicator in element_id or indicator in element_classes or indicator in text_lower 
               for indicator in search_indicators):
            return SemanticType.SEARCH_FORM
        
        # Login forms
        login_indicators = ['login', 'signin', 'sign-in', 'auth', 'user']
        if any(indicator in element_id or indicator in element_classes or indicator in text_lower 
               for indicator in login_indicators):
            return SemanticType.LOGIN_FORM
        
        # Navigation elements
        nav_indicators = ['nav', 'menu', 'header', 'breadcrumb']
        if (element.name == 'nav' or 
            any(indicator in element_id or indicator in element_classes 
                for indicator in nav_indicators)):
            return SemanticType.PRIMARY_NAV
        
        # Check for specific patterns in text
        for semantic_type, patterns in self.semantic_patterns.items():
            if any(pattern in text_lower for pattern in patterns):
                return semantic_type
        
        return None
    
    def _calculate_confidence_score(self, element: Tag, element_type: ElementType, semantic_type: Optional[SemanticType]) -> float:
        """
        Calculate confidence score for element classification.
        
        Args:
            element: BeautifulSoup Tag element
            element_type: Classified element type
            semantic_type: Classified semantic type
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        score = 0.5  # Base score
        
        # Higher confidence for standard interactive elements
        if element_type in get_interactive_element_types():
            score += 0.3
        
        # Higher confidence if semantic type was determined
        if semantic_type:
            score += 0.2
        
        # Higher confidence for elements with clear attributes
        if element.get('id') or element.get('name'):
            score += 0.1
        
        # Higher confidence for elements with descriptive text
        text_content = self._extract_text_content(element)
        if text_content and len(text_content.strip()) > self.min_text_length:
            score += 0.1
        
        # Lower confidence for generic divs/spans without clear indicators
        if element.name in ['div', 'span'] and not self._has_interactive_attributes(element):
            score -= 0.2
        
        return min(max(score, 0.0), 1.0)
    
    def _extract_accessibility_info(self, element: Tag) -> AccessibilityInfo:
        """
        Extract accessibility information from the element.
        
        Args:
            element: BeautifulSoup Tag element
            
        Returns:
            AccessibilityInfo object
        """
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
                elif aria_name == 'invalid':
                    accessibility_info.invalid = attr_value.lower() == 'true'
                elif aria_name == 'expanded':
                    accessibility_info.expanded = attr_value.lower() == 'true'
                elif aria_name == 'checked':
                    accessibility_info.checked = attr_value.lower() == 'true'
                else:
                    accessibility_info.attributes[attr_name] = attr_value
        
        # Extract role
        role = element.get('role')
        if role:
            # Convert string role to AccessibilityRole enum if possible
            try:
                from ..types.element_data_types import AccessibilityRole
                accessibility_info.role = AccessibilityRole(role.upper())
            except (ValueError, ImportError):
                accessibility_info.attributes['role'] = role
        
        # Extract other accessibility-related attributes
        if element.has_attr('disabled'):
            accessibility_info.disabled = True
        
        if element.has_attr('required'):
            accessibility_info.required = True
        
        # Check for associated label
        if element.get('id'):
            # Note: This would require access to the full DOM to find labels
            # For now, just mark that we should look for labels
            accessibility_info.attributes['has_id'] = element.get('id')
        
        return accessibility_info
    
    def _get_bounding_box(self, element: Tag) -> Optional[Dict[str, int]]:
        """
        Get bounding box information if available.
        
        Args:
            element: BeautifulSoup Tag element
            
        Returns:
            Bounding box dictionary or None
        """
        # This would typically require browser execution context
        # For static analysis, we can't determine actual positions
        return None
    
    def _is_hidden_element(self, element: Tag) -> bool:
        """
        Check if element is hidden.
        
        Args:
            element: BeautifulSoup Tag element
            
        Returns:
            True if element appears to be hidden
        """
        # Check common hiding attributes
        if element.get('hidden') is not None:
            return True
        
        if element.get('aria-hidden') == 'true':
            return True
        
        # Check style attribute for visibility/display
        style = element.get('style', '')
        if style:
            style_lower = style.lower()
            if ('display:none' in style_lower.replace(' ', '') or 
                'visibility:hidden' in style_lower.replace(' ', '')):
                return True
        
        # Check input type hidden
        if element.name == 'input' and element.get('type') == 'hidden':
            return True
        
        return False
    
    def _is_disabled_element(self, element: Tag) -> bool:
        """
        Check if element is disabled.
        
        Args:
            element: BeautifulSoup Tag element
            
        Returns:
            True if element is disabled
        """
        return (element.has_attr('disabled') or 
                element.get('aria-disabled') == 'true')
    
    async def _build_element_relationships(self, interactive_elements: List[InteractiveElement], soup: BeautifulSoup) -> None:
        """
        Build hierarchical relationships between elements.
        
        Args:
            interactive_elements: List of classified elements
            soup: Full DOM tree
        """
        # Create a mapping of element IDs to their DOM elements
        element_map = {}
        for elem in interactive_elements:
            # Find the actual DOM element for this interactive element
            # This is simplified - in practice you'd need better element tracking
            dom_element = self._find_dom_element_by_locators(elem.locators, soup)
            if dom_element:
                element_map[elem.element_id] = (elem, dom_element)
        
        # Build relationships
        for element_id, (interactive_elem, dom_elem) in element_map.items():
            hierarchy = ElementHierarchy()
            
            # Find parent
            parent_elem = dom_elem.parent
            if parent_elem:
                parent_interactive = self._find_interactive_element_for_dom(parent_elem, element_map)
                if parent_interactive:
                    hierarchy.parent = parent_interactive.element_id
            
            # Find children
            for child in dom_elem.find_all():
                child_interactive = self._find_interactive_element_for_dom(child, element_map)
                if child_interactive and child_interactive.element_id != element_id:
                    hierarchy.children.append(child_interactive.element_id)
            
            # Calculate depth
            depth = 0
            current = dom_elem
            while current.parent:
                depth += 1
                current = current.parent
            hierarchy.depth = depth
            
            interactive_elem.hierarchy = hierarchy
    
    def _find_dom_element_by_locators(self, locators: Dict[str, str], soup: BeautifulSoup) -> Optional[Tag]:
        """
        Find DOM element using its locators.
        
        Args:
            locators: Dictionary of locator strategies
            soup: BeautifulSoup DOM tree
            
        Returns:
            Found Tag element or None
        """
        # Try ID first
        if 'id' in locators:
            element_id = locators['id'].replace('#', '')
            return soup.find(id=element_id)
        
        # Try name
        if 'name' in locators:
            return soup.find(attrs={'name': locators['name']})
        
        # Try CSS selector
        if 'css' in locators:
            try:
                return soup.select_one(locators['css'])
            except:
                pass
        
        return None
    
    def _find_interactive_element_for_dom(self, dom_elem: Tag, element_map: Dict) -> Optional[InteractiveElement]:
        """
        Find the interactive element that corresponds to a DOM element.
        
        Args:
            dom_elem: BeautifulSoup Tag element
            element_map: Mapping of element IDs to (InteractiveElement, Tag) tuples
            
        Returns:
            Corresponding InteractiveElement or None
        """
        for element_id, (interactive_elem, mapped_dom_elem) in element_map.items():
            if dom_elem == mapped_dom_elem:
                return interactive_elem
        return None
    
    def _load_semantic_patterns(self) -> Dict[SemanticType, List[str]]:
        """
        Load semantic classification patterns.
        
        Returns:
            Dictionary mapping semantic types to text patterns
        """
        return {
            SemanticType.SEARCH_FORM: ['search', 'find', 'query', 'lookup'],
            SemanticType.LOGIN_FORM: ['login', 'sign in', 'log in', 'signin', 'authenticate'],
            SemanticType.REGISTRATION_FORM: ['register', 'sign up', 'signup', 'create account'],
            SemanticType.CONTACT_FORM: ['contact', 'message', 'feedback', 'inquiry'],
            SemanticType.CHECKOUT_FORM: ['checkout', 'payment', 'billing', 'purchase'],
            SemanticType.CART: ['cart', 'basket', 'bag', 'shopping'],
            SemanticType.WISHLIST: ['wishlist', 'favorites', 'saved', 'bookmark'],
            SemanticType.SOCIAL_MEDIA: ['share', 'like', 'follow', 'tweet', 'facebook', 'twitter'],
            SemanticType.ADVERTISEMENT: ['ad', 'advertisement', 'sponsor', 'promoted'],
            SemanticType.COOKIE_BANNER: ['cookie', 'privacy', 'accept', 'consent'],
        }