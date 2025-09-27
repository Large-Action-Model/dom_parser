"""
Semanfrom data_types import (
    SemanticBlock, NavigationStructure, NavigationLink,
    SemanticType, ElementType
)Extractor for identifying meaningful content blocks.

Analyzes DOM structure to extract semantic content areas,
navigation elements, and page organization patterns.
"""

from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup, Tag

from ..types.dom_data_types import (
    SemanticBlock, NavigationStructure, NavigationArea
)
from ..types.element_data_types import (
    SemanticType, ElementType
)


class SemanticExtractor:
    """
    Extracts semantic meaning from DOM structures.
    
    Identifies content blocks, navigation areas, and organizational
    patterns for better AI understanding of page layout.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize Semantic Extractor."""
        self.config = config or {}
    
    async def extract_semantic_blocks(self, soup: BeautifulSoup) -> List[SemanticBlock]:
        """Extract semantically meaningful content blocks."""
        blocks = []
        
        # Find semantic HTML5 elements
        semantic_elements = soup.find_all(['article', 'section', 'aside', 'main', 'header', 'footer'])
        
        for idx, element in enumerate(semantic_elements):
            semantic_type = self._determine_semantic_type_from_tag(element.name)
            
            block = SemanticBlock(
                block_id=f"semantic_block_{idx}",
                semantic_type=semantic_type,
                element_ids=[f"elem_{idx}"],
                text_content=element.get_text(strip=True)[:200],  # Truncate
                importance_score=self._calculate_importance_score(element)
            )
            blocks.append(block)
        
        return blocks
    
    async def extract_navigation_structure(self, soup: BeautifulSoup) -> NavigationStructure:
        """Extract navigation structure from the page."""
        nav_structure = NavigationStructure()
        
        # Find navigation elements
        nav_elements = soup.find_all('nav')
        
        if nav_elements:
            # Assume first nav is primary
            primary_nav = NavigationArea(
                nav_id="primary_nav",
                nav_type=SemanticType.PRIMARY_NAV,
                links=[f"link_{i}" for i in range(len(nav_elements[0].find_all('a')))]
            )
            nav_structure.primary_navigation = primary_nav
        
        return nav_structure
    
    def _determine_semantic_type_from_tag(self, tag_name: str) -> SemanticType:
        """Map HTML tag to semantic type."""
        mapping = {
            'article': SemanticType.MAIN_CONTENT,
            'section': SemanticType.MAIN_CONTENT,
            'aside': SemanticType.SIDEBAR,
            'main': SemanticType.MAIN_CONTENT,
            'header': SemanticType.PRIMARY_NAV,
            'footer': SemanticType.SECONDARY_NAV,
        }
        return mapping.get(tag_name, SemanticType.UNKNOWN)
    
    def _calculate_importance_score(self, element: Tag) -> float:
        """Calculate importance score for a semantic block."""
        score = 0.5
        
        # Boost score for main content
        if element.name in ['main', 'article']:
            score += 0.3
        
        # Boost for text content
        text_length = len(element.get_text(strip=True))
        if text_length > 100:
            score += 0.2
        
        return min(score, 1.0)