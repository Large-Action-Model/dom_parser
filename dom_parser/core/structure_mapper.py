"""
Structure Mapper for analyzing page layout and element hierarchy.

Maps the overall structure of the page, identifies layout patterns,
and builds hierarchical relationships between elements.
"""

from typing import Dict, Any, Optional, List
from bs4 import BeautifulSoup, Tag

from ..types.dom_data_types import (
    PageStructure, PageSection, NavigationArea, ContentArea,
    SidebarArea, HeaderFooterInfo
)
from ..types.element_data_types import SemanticType


class StructureMapper:
    """
    Maps page structure and layout patterns.
    
    Analyzes DOM hierarchy to understand page organization,
    layout patterns, and structural relationships.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize Structure Mapper."""
        self.config = config or {}
    
    async def map_page_structure(self, soup: BeautifulSoup) -> PageStructure:
        """Map the overall structure of the page."""
        page_structure = PageStructure()
        
        # Identify major sections
        sections = await self._identify_page_sections(soup)
        page_structure.sections = sections
        
        # Identify navigation areas
        nav_areas = await self._identify_navigation_areas(soup)
        page_structure.navigation_areas = nav_areas
        
        # Identify content areas
        content_areas = await self._identify_content_areas(soup)
        page_structure.content_areas = content_areas
        
        # Identify sidebar areas
        sidebar_areas = await self._identify_sidebar_areas(soup)
        page_structure.sidebar_areas = sidebar_areas
        
        # Identify header and footer
        header_footer = await self._identify_header_footer(soup)
        page_structure.header_footer = header_footer
        
        # Determine layout type
        page_structure.layout_type = self._determine_layout_type(soup)
        
        # Build heading structure
        page_structure.heading_structure = self._build_heading_structure(soup)
        
        return page_structure
    
    async def _identify_page_sections(self, soup: BeautifulSoup) -> List[PageSection]:
        """Identify major page sections."""
        sections = []
        
        # Find semantic section elements
        section_elements = soup.find_all(['section', 'article', 'main', 'aside'])
        
        for idx, element in enumerate(section_elements):
            section_type = self._get_section_semantic_type(element)
            
            section = PageSection(
                section_id=f"section_{idx}",
                section_type=section_type,
                element_ids=[f"elem_{idx}"],
                heading=self._extract_section_heading(element)
            )
            sections.append(section)
        
        return sections
    
    async def _identify_navigation_areas(self, soup: BeautifulSoup) -> List[NavigationArea]:
        """Identify navigation areas."""
        nav_areas = []
        
        nav_elements = soup.find_all('nav')
        for idx, nav_element in enumerate(nav_elements):
            nav_area = NavigationArea(
                nav_id=f"nav_{idx}",
                nav_type=SemanticType.PRIMARY_NAV if idx == 0 else SemanticType.SECONDARY_NAV,
                links=[f"link_{i}" for i in range(len(nav_element.find_all('a')))]
            )
            nav_areas.append(nav_area)
        
        return nav_areas
    
    async def _identify_content_areas(self, soup: BeautifulSoup) -> List[ContentArea]:
        """Identify main content areas."""
        content_areas = []
        
        # Look for main content elements
        content_elements = soup.find_all(['main', 'article'])
        
        for idx, element in enumerate(content_elements):
            content_area = ContentArea(
                content_id=f"content_{idx}",
                content_type=SemanticType.MAIN_CONTENT,
                headings=[f"heading_{i}" for i in range(len(element.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])))],
                paragraphs=[f"para_{i}" for i in range(len(element.find_all('p')))],
                word_count=len(element.get_text(strip=True).split())
            )
            content_areas.append(content_area)
        
        return content_areas
    
    async def _identify_sidebar_areas(self, soup: BeautifulSoup) -> List[SidebarArea]:
        """Identify sidebar areas."""
        sidebar_areas = []
        
        aside_elements = soup.find_all('aside')
        for idx, element in enumerate(aside_elements):
            sidebar = SidebarArea(
                sidebar_id=f"sidebar_{idx}",
                position="right",  # Default position
                widgets=[f"widget_{i}" for i in range(len(element.find_all(['div', 'section'])))]
            )
            sidebar_areas.append(sidebar)
        
        return sidebar_areas
    
    async def _identify_header_footer(self, soup: BeautifulSoup) -> HeaderFooterInfo:
        """Identify header and footer information."""
        header_footer = HeaderFooterInfo()
        
        # Find header
        header_element = soup.find('header')
        if header_element:
            header_footer.header_id = "main_header"
            header_footer.header_elements = ["header_elem_0"]
            
            # Look for logo
            logo_element = header_element.find(['img', '.logo', '#logo'])
            if logo_element:
                header_footer.logo = "logo_elem"
        
        # Find footer
        footer_element = soup.find('footer')
        if footer_element:
            header_footer.footer_id = "main_footer"
            header_footer.footer_elements = ["footer_elem_0"]
            
            # Look for copyright
            copyright_text = footer_element.get_text()
            if '©' in copyright_text or 'copyright' in copyright_text.lower():
                header_footer.copyright = copyright_text.strip()[:100]
        
        return header_footer
    
    def _get_section_semantic_type(self, element: Tag) -> SemanticType:
        """Determine semantic type of a section element."""
        tag_name = element.name.lower()
        
        if tag_name == 'main':
            return SemanticType.MAIN_CONTENT
        elif tag_name == 'article':
            return SemanticType.MAIN_CONTENT
        elif tag_name == 'aside':
            return SemanticType.SIDEBAR
        elif tag_name == 'section':
            return SemanticType.MAIN_CONTENT
        
        return SemanticType.UNKNOWN
    
    def _extract_section_heading(self, element: Tag) -> Optional[str]:
        """Extract the main heading from a section."""
        heading = element.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if heading:
            return heading.get_text(strip=True)
        return None
    
    def _determine_layout_type(self, soup: BeautifulSoup) -> str:
        """Determine the overall layout type of the page."""
        # Simple heuristics for layout detection
        has_main = bool(soup.find('main'))
        has_aside = bool(soup.find('aside'))
        has_nav = bool(soup.find('nav'))
        
        if has_main and has_aside:
            return "two_column"
        elif has_main and has_nav and has_aside:
            return "three_column"
        elif has_main:
            return "single_column"
        else:
            return "unknown"
    
    def _build_heading_structure(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Build hierarchical heading structure."""
        headings = []
        heading_elements = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        for idx, heading in enumerate(heading_elements):
            level = int(heading.name[1])  # Extract number from h1, h2, etc.
            headings.append({
                'id': f"heading_{idx}",
                'level': level,
                'text': heading.get_text(strip=True),
                'tag': heading.name
            })
        
        return headings