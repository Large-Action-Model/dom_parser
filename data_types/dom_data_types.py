"""
Core Data Structures for DOM Parser

Defines the main data structures used throughout the DOM analysis process,
including results, elements, page structure, and semantic information.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime
from enum import Enum

from .element_data_types import ElementType, InteractionType, SemanticType, FormFieldType, AccessibilityRole


@dataclass
class AccessibilityInfo:
    """Accessibility information for an element or page."""
    
    role: Optional[AccessibilityRole] = None
    label: Optional[str] = None
    description: Optional[str] = None
    level: Optional[int] = None  # For headings
    expanded: Optional[bool] = None  # For collapsible elements
    checked: Optional[bool] = None  # For checkboxes/radios
    disabled: Optional[bool] = None
    required: Optional[bool] = None
    invalid: Optional[bool] = None
    live: Optional[str] = None  # aria-live values
    atomic: Optional[bool] = None
    relevant: Optional[str] = None
    busy: Optional[bool] = None
    hidden: Optional[bool] = None
    owns: List[str] = field(default_factory=list)  # aria-owns
    controls: List[str] = field(default_factory=list)  # aria-controls
    described_by: List[str] = field(default_factory=list)  # aria-describedby
    labelled_by: List[str] = field(default_factory=list)  # aria-labelledby
    flowto: List[str] = field(default_factory=list)  # aria-flowto
    
    # Additional ARIA attributes
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class ElementHierarchy:
    """Hierarchical information about an element."""
    
    parent: Optional[str] = None  # Parent element ID
    children: List[str] = field(default_factory=list)  # Child element IDs
    siblings: List[str] = field(default_factory=list)  # Sibling element IDs
    ancestors: List[str] = field(default_factory=list)  # All ancestor IDs
    descendants: List[str] = field(default_factory=list)  # All descendant IDs
    depth: int = 0  # Depth from root
    index_in_parent: int = 0  # Position among siblings


@dataclass
class InteractiveElement:
    """Represents an interactive element on the page."""
    
    element_id: str
    element_type: ElementType
    tag_name: str
    
    # Multiple ways to locate this element
    locators: Dict[str, str] = field(default_factory=dict)  # css, xpath, id, etc.
    
    # Element properties
    properties: Dict[str, Any] = field(default_factory=dict)
    attributes: Dict[str, str] = field(default_factory=dict)
    
    # Interaction capabilities
    interaction_types: List[InteractionType] = field(default_factory=list)
    interaction_hints: List[str] = field(default_factory=list)
    
    # Element text and visual info
    text_content: str = ""
    visible_text: str = ""
    placeholder: Optional[str] = None
    value: Optional[str] = None
    
    # Position and visibility
    bounding_box: Optional[Dict[str, int]] = None  # x, y, width, height
    is_visible: bool = True
    is_enabled: bool = True
    is_focused: bool = False
    
    # Accessibility information
    accessibility_info: AccessibilityInfo = field(default_factory=AccessibilityInfo)
    
    # Hierarchy information
    hierarchy: ElementHierarchy = field(default_factory=ElementHierarchy)
    
    # Form-specific information (if applicable)
    form_field_type: Optional[FormFieldType] = None
    form_validation: Dict[str, Any] = field(default_factory=dict)
    
    # Semantic classification
    semantic_type: Optional[SemanticType] = None
    confidence_score: float = 0.0  # Confidence in classification
    
    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FormStructure:
    """Represents a form and its fields."""
    
    form_id: str
    form_element_id: str  # ID of the form element itself
    
    # Form properties
    action: Optional[str] = None
    method: str = "GET"
    encoding_type: str = "application/x-www-form-urlencoded"
    
    # Form fields
    fields: List[InteractiveElement] = field(default_factory=list)
    field_groups: List[List[str]] = field(default_factory=list)  # Grouped field IDs
    
    # Validation information
    validation_rules: Dict[str, Any] = field(default_factory=dict)
    required_fields: List[str] = field(default_factory=list)
    
    # Submit actions
    submit_buttons: List[str] = field(default_factory=list)  # Element IDs
    
    # Form semantics
    form_type: Optional[SemanticType] = None
    purpose: Optional[str] = None
    
    # Accessibility
    accessibility_info: AccessibilityInfo = field(default_factory=AccessibilityInfo)
    
    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PageSection:
    """Represents a major section of the page."""
    
    section_id: str
    section_type: SemanticType
    
    # Element IDs within this section
    element_ids: List[str] = field(default_factory=list)
    
    # Hierarchical structure
    parent_section: Optional[str] = None
    child_sections: List[str] = field(default_factory=list)
    
    # Section properties
    heading: Optional[str] = None
    description: Optional[str] = None
    
    # Position and size
    bounding_box: Optional[Dict[str, int]] = None
    
    # Accessibility
    accessibility_info: AccessibilityInfo = field(default_factory=AccessibilityInfo)
    
    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NavigationArea:
    """Represents a navigation area on the page."""
    
    nav_id: str
    nav_type: SemanticType  # PRIMARY_NAV, SECONDARY_NAV, BREADCRUMB, etc.
    
    # Navigation links
    links: List[str] = field(default_factory=list)  # Element IDs
    
    # Structure
    is_hierarchical: bool = False
    hierarchy_levels: List[List[str]] = field(default_factory=list)
    
    # Current state
    current_page_indicator: Optional[str] = None  # Element ID of current page
    
    # Accessibility
    accessibility_info: AccessibilityInfo = field(default_factory=AccessibilityInfo)
    
    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ContentArea:
    """Represents a main content area."""
    
    content_id: str
    content_type: SemanticType
    
    # Content elements
    headings: List[str] = field(default_factory=list)  # Element IDs
    paragraphs: List[str] = field(default_factory=list)
    images: List[str] = field(default_factory=list)
    links: List[str] = field(default_factory=list)
    
    # Content structure
    outline: List[Dict[str, Any]] = field(default_factory=list)  # Heading outline
    
    # Content properties
    word_count: int = 0
    reading_time: Optional[int] = None  # Estimated reading time in minutes
    
    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SidebarArea:
    """Represents a sidebar area."""
    
    sidebar_id: str
    position: str  # left, right, top, bottom
    
    # Sidebar content
    widgets: List[str] = field(default_factory=list)  # Element IDs
    
    # Sidebar type
    purpose: Optional[str] = None  # navigation, advertising, related_content
    
    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HeaderFooterInfo:
    """Information about page header and footer."""
    
    # Header information
    header_id: Optional[str] = None
    header_elements: List[str] = field(default_factory=list)
    logo: Optional[str] = None  # Element ID
    site_title: Optional[str] = None
    tagline: Optional[str] = None
    
    # Footer information
    footer_id: Optional[str] = None
    footer_elements: List[str] = field(default_factory=list)
    copyright: Optional[str] = None
    
    # Navigation in header/footer
    header_nav: List[str] = field(default_factory=list)  # Navigation element IDs
    footer_nav: List[str] = field(default_factory=list)
    
    # Contact/social information
    contact_info: Dict[str, str] = field(default_factory=dict)
    social_links: List[str] = field(default_factory=list)  # Element IDs
    
    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NavigationStructure:
    """Overall navigation structure of the page."""
    
    # Main navigation areas
    primary_navigation: Optional[NavigationArea] = None
    secondary_navigation: Optional[NavigationArea] = None
    breadcrumbs: Optional[NavigationArea] = None
    pagination: Optional[NavigationArea] = None
    
    # Other navigation elements
    skip_links: List[str] = field(default_factory=list)  # Element IDs
    back_to_top: List[str] = field(default_factory=list)
    
    # Site map/structure
    site_hierarchy: List[Dict[str, Any]] = field(default_factory=list)
    
    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SemanticBlock:
    """Represents a semantically meaningful block of content."""
    
    block_id: str
    semantic_type: SemanticType
    
    # Block content
    element_ids: List[str] = field(default_factory=list)
    text_content: str = ""
    
    # Block properties
    importance_score: float = 0.0
    content_density: float = 0.0  # Text to markup ratio
    
    # Related blocks
    related_blocks: List[str] = field(default_factory=list)
    
    # Position and size
    bounding_box: Optional[Dict[str, int]] = None
    
    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PageStructure:
    """Overall structure of the page."""
    
    # Major page sections
    sections: List[PageSection] = field(default_factory=list)
    navigation_areas: List[NavigationArea] = field(default_factory=list)
    content_areas: List[ContentArea] = field(default_factory=list)
    sidebar_areas: List[SidebarArea] = field(default_factory=list)
    header_footer: HeaderFooterInfo = field(default_factory=HeaderFooterInfo)
    
    # Page layout type
    layout_type: str = "unknown"  # single_column, two_column, three_column, grid, etc.
    
    # Page hierarchy
    heading_structure: List[Dict[str, Any]] = field(default_factory=list)
    landmark_elements: List[str] = field(default_factory=list)  # Element IDs
    
    # Page characteristics
    is_single_page_app: bool = False
    has_dynamic_content: bool = False
    estimated_complexity: str = "low"  # low, medium, high
    
    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DOMAnalysisResult:
    """Complete result of DOM analysis."""
    
    # Core analysis results
    page_structure: PageStructure
    interactive_elements: List[InteractiveElement] = field(default_factory=list)
    semantic_blocks: List[SemanticBlock] = field(default_factory=list)
    form_structures: List[FormStructure] = field(default_factory=list)
    navigation_structure: NavigationStructure = field(default_factory=NavigationStructure)
    
    # Global accessibility analysis
    accessibility_tree: AccessibilityInfo = field(default_factory=AccessibilityInfo)
    
    # Performance and optimization hints
    performance_hints: Dict[str, Any] = field(default_factory=dict)
    
    # Element relationships and mappings
    element_relationships: Dict[str, List[str]] = field(default_factory=dict)
    element_index: Dict[str, InteractiveElement] = field(default_factory=dict)
    
    # Analysis metadata
    analysis_timestamp: datetime = field(default_factory=datetime.now)
    source_url: Optional[str] = None
    source_title: Optional[str] = None
    analysis_version: str = "1.0.0"
    processing_time: Optional[float] = None  # Analysis time in seconds
    
    # Quality metrics
    confidence_scores: Dict[str, float] = field(default_factory=dict)
    coverage_metrics: Dict[str, float] = field(default_factory=dict)
    
    # Error and warning information
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_interactive_element(self, element_id: str) -> Optional[InteractiveElement]:
        """Get an interactive element by ID."""
        return self.element_index.get(element_id)
    
    def get_elements_by_type(self, element_type: ElementType) -> List[InteractiveElement]:
        """Get all interactive elements of a specific type."""
        return [elem for elem in self.interactive_elements if elem.element_type == element_type]
    
    def get_elements_by_semantic_type(self, semantic_type: SemanticType) -> List[InteractiveElement]:
        """Get all elements with a specific semantic type."""
        return [elem for elem in self.interactive_elements if elem.semantic_type == semantic_type]
    
    def get_form_by_id(self, form_id: str) -> Optional[FormStructure]:
        """Get a form structure by ID."""
        return next((form for form in self.form_structures if form.form_id == form_id), None)
    
    def get_clickable_elements(self) -> List[InteractiveElement]:
        """Get all elements that can be clicked."""
        return [elem for elem in self.interactive_elements 
                if InteractionType.CLICK in elem.interaction_types]
    
    def get_form_fields(self) -> List[InteractiveElement]:
        """Get all form field elements."""
        form_element_types = {ElementType.INPUT, ElementType.TEXTAREA, ElementType.SELECT, 
                            ElementType.CHECKBOX, ElementType.RADIO}
        return [elem for elem in self.interactive_elements if elem.element_type in form_element_types]