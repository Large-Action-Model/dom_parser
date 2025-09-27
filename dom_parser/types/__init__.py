from .dom_data_types import (
    DOMAnalysisResult, InteractiveElement, PageStructure, 
    SemanticBlock, FormStructure, NavigationStructure,
    AccessibilityInfo, PageSection, NavigationArea,
    ContentArea, SidebarArea, HeaderFooterInfo, ElementHierarchy
)
from .element_data_types import (
    ElementType, InteractionType, SemanticType,
    FormFieldType, AccessibilityRole,
    get_interactive_element_types, get_content_element_types,
    get_structural_element_types, get_form_field_types,
    HTML_TAG_TO_ELEMENT_TYPE, INPUT_TYPE_TO_FORM_FIELD_TYPE
)

__all__ = [
    # From dom_data_types
    "DOMAnalysisResult",
    "InteractiveElement", 
    "PageStructure",
    "SemanticBlock",
    "FormStructure",
    "NavigationStructure",
    "AccessibilityInfo",
    "PageSection",
    "NavigationArea",
    "ContentArea",
    "SidebarArea", 
    "HeaderFooterInfo",
    "ElementHierarchy",
    
    # From element_data_types
    "ElementType",
    "InteractionType",
    "SemanticType",
    "FormFieldType",
    "AccessibilityRole",
]