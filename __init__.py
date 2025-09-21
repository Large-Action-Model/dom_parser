"""
DOM Parser & Analyzer Component

A robust DOM parsing and analysis component for Large Action Model (LAM) systems.
Processes HTML content from the Browser Controller and provides structured analysis
for AI-driven web interaction.
"""

from .dom_parser import DOMParser
from .data_types import (
    DOMAnalysisResult, InteractiveElement, PageStructure, 
    SemanticBlock, FormStructure, NavigationStructure,
    AccessibilityInfo, PageSection, ContentArea,
    HeaderFooterInfo, ElementHierarchy, NavigationArea, SidebarArea
)
from .data_types import (
    ElementType, InteractionType, SemanticType,
    FormFieldType, AccessibilityRole
)

# Package metadata
__version__ = "1.0.0"
__author__ = "LAM Project"
__description__ = "DOM Parser & Analyzer component for Large Action Model web automation"
__license__ = "MIT"

# Main exports
__all__ = [
    # Main classes
    "DOMParser",
    
    # Core data structures
    "DOMAnalysisResult",
    "InteractiveElement", 
    "PageStructure",
    "SemanticBlock",
    "FormStructure",
    "NavigationStructure",
    "AccessibilityInfo",
    "PageSection",
    "ContentArea",
    "HeaderFooterInfo",
    "ElementHierarchy",
    
    # Type enums
    "ElementType",
    "InteractionType", 
    "SemanticType",
    "FormFieldType",
    "AccessibilityRole",
    
    # Package info
    "__version__",
    "__author__",
    "__description__", 
    "__license__",
]