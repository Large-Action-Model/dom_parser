"""
Main DOM Parser class for analyzing HTML content.

This class provides the primary interface for DOM parsing and analysis,
integrating with Browser Controller and providing structured data for
AI-driven web interaction.
"""

import time
import asyncio
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from loguru import logger

# Import browser controller types (assuming they're available)
try:
    from browser_controller.types import PageInfo  # Adjust import path as needed
except ImportError:
    # Fallback if browser controller isn't available
    from dataclasses import dataclass
    @dataclass
    class PageInfo:
        url: str
        title: str
        source: str
        timestamp: float
        metadata: Dict[str, Any]

from data_types import (
    DOMAnalysisResult, InteractiveElement, PageStructure,
    SemanticBlock, FormStructure, NavigationStructure,
    AccessibilityInfo, ElementType
)
from html_analyzer import HTMLAnalyzer
from element_classifier import ElementClassifier
from semantic_extractor import SemanticExtractor
from form_analyzer import FormAnalyzer
from accessibility_analyzer import AccessibilityAnalyzer
from structure_mapper import StructureMapper


class DOMParser:
    """
    Main DOM Parser class for analyzing HTML content from Browser Controller.
    
    This class orchestrates the entire DOM analysis process, from raw HTML
    parsing to intelligent semantic extraction and accessibility analysis.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize DOM Parser with optional configuration.
        
        Args:
            config: Configuration dictionary for parser behavior
        """
        self.config = config or {}
        self.logger = logger.bind(component="DOMParser")
        
        # Initialize analysis components
        self.html_analyzer = HTMLAnalyzer(self.config.get('html_analyzer', {}))
        self.element_classifier = ElementClassifier(self.config.get('element_classifier', {}))
        self.semantic_extractor = SemanticExtractor(self.config.get('semantic_extractor', {}))
        self.form_analyzer = FormAnalyzer(self.config.get('form_analyzer', {}))
        self.accessibility_analyzer = AccessibilityAnalyzer(self.config.get('accessibility_analyzer', {}))
        self.structure_mapper = StructureMapper(self.config.get('structure_mapper', {}))
        
        # Analysis state
        self._last_analysis: Optional[DOMAnalysisResult] = None
        self._analysis_cache: Dict[str, DOMAnalysisResult] = {}
        
        self.logger.info("DOM Parser initialized", extra={
            "cache_enabled": self.config.get('enable_cache', True),
            "max_cache_size": self.config.get('max_cache_size', 100)
        })
    
    async def parse_page(self, html_source: str, url: str, metadata: Optional[Dict[str, Any]] = None) -> DOMAnalysisResult:
        """
        Parse HTML page and perform comprehensive DOM analysis.
        
        Args:
            html_source: Raw HTML source code
            url: Page URL
            metadata: Additional metadata about the page
            
        Returns:
            Complete DOM analysis result
        """
        start_time = time.time()
        metadata = metadata or {}
        
        self.logger.info("Starting DOM analysis", extra={
            "url": url,
            "html_length": len(html_source),
            "metadata_keys": list(metadata.keys())
        })
        
        try:
            # Check cache first
            cache_key = self._generate_cache_key(html_source, url)
            if self.config.get('enable_cache', True) and cache_key in self._analysis_cache:
                self.logger.info("Returning cached analysis result")
                return self._analysis_cache[cache_key]
            
            # Step 1: Parse HTML structure
            dom_tree = await self.html_analyzer.parse_html(html_source)
            
            # Step 2: Extract and classify interactive elements
            interactive_elements = await self.extract_interactive_elements(dom_tree)
            
            # Step 3: Analyze page structure
            page_structure = await self.analyze_page_structure(dom_tree)
            
            # Step 4: Extract semantic blocks
            semantic_blocks = await self.extract_semantic_blocks(dom_tree)
            
            # Step 5: Analyze forms
            form_structures = await self.analyze_forms(dom_tree)
            
            # Step 6: Extract navigation structure
            navigation_structure = await self.extract_navigation_elements(dom_tree)
            
            # Step 7: Perform accessibility analysis
            accessibility_tree = await self.accessibility_analyzer.analyze_accessibility(dom_tree)
            
            # Step 8: Generate performance hints
            performance_hints = await self._generate_performance_hints(dom_tree, interactive_elements)
            
            # Step 9: Build element relationships
            element_relationships = await self._build_element_relationships(interactive_elements)
            
            # Create element index for quick lookup
            element_index = {elem.element_id: elem for elem in interactive_elements}
            
            # Build final result
            analysis_result = DOMAnalysisResult(
                page_structure=page_structure,
                interactive_elements=interactive_elements,
                semantic_blocks=semantic_blocks,
                form_structures=form_structures,
                navigation_structure=navigation_structure,
                accessibility_tree=accessibility_tree,
                performance_hints=performance_hints,
                element_relationships=element_relationships,
                element_index=element_index,
                source_url=url,
                source_title=await self._extract_page_title(dom_tree),
                processing_time=time.time() - start_time,
                metadata=metadata
            )
            
            # Cache result
            if self.config.get('enable_cache', True):
                self._cache_result(cache_key, analysis_result)
            
            self._last_analysis = analysis_result
            
            self.logger.info("DOM analysis completed", extra={
                "processing_time": analysis_result.processing_time,
                "interactive_elements": len(interactive_elements),
                "semantic_blocks": len(semantic_blocks),
                "forms": len(form_structures)
            })
            
            return analysis_result
            
        except Exception as e:
            self.logger.error("DOM analysis failed", extra={"error": str(e), "url": url})
            # Return basic result with error information
            return DOMAnalysisResult(
                page_structure=PageStructure(),
                source_url=url,
                processing_time=time.time() - start_time,
                errors=[f"Analysis failed: {str(e)}"],
                metadata=metadata
            )
    
    async def parse_page_from_browser_info(self, page_info: PageInfo) -> DOMAnalysisResult:
        """
        Parse page using Browser Controller's PageInfo object.
        
        Args:
            page_info: PageInfo object from Browser Controller
            
        Returns:
            Complete DOM analysis result
        """
        return await self.parse_page(
            html_source=page_info.source,
            url=page_info.url,
            metadata={
                "title": page_info.title,
                "timestamp": page_info.timestamp,
                "browser_metadata": page_info.metadata
            }
        )
    
    async def extract_interactive_elements(self, dom_tree) -> List[InteractiveElement]:
        """
        Extract and classify all interactive elements from DOM tree.
        
        Args:
            dom_tree: Parsed DOM tree from HTML analyzer
            
        Returns:
            List of classified interactive elements
        """
        return await self.element_classifier.classify_elements(dom_tree)
    
    async def analyze_page_structure(self, dom_tree) -> PageStructure:
        """
        Analyze overall page structure and layout.
        
        Args:
            dom_tree: Parsed DOM tree from HTML analyzer
            
        Returns:
            Page structure analysis result
        """
        return await self.structure_mapper.map_page_structure(dom_tree)
    
    async def extract_semantic_blocks(self, dom_tree) -> List[SemanticBlock]:
        """
        Extract semantically meaningful content blocks.
        
        Args:
            dom_tree: Parsed DOM tree from HTML analyzer
            
        Returns:
            List of semantic content blocks
        """
        return await self.semantic_extractor.extract_semantic_blocks(dom_tree)
    
    async def analyze_forms(self, dom_tree) -> List[FormStructure]:
        """
        Analyze form structures and field relationships.
        
        Args:
            dom_tree: Parsed DOM tree from HTML analyzer
            
        Returns:
            List of analyzed form structures
        """
        return await self.form_analyzer.analyze_forms(dom_tree)
    
    async def extract_navigation_elements(self, dom_tree) -> NavigationStructure:
        """
        Extract and analyze navigation structure.
        
        Args:
            dom_tree: Parsed DOM tree from HTML analyzer
            
        Returns:
            Navigation structure analysis result
        """
        return await self.semantic_extractor.extract_navigation_structure(dom_tree)
    
    async def get_element_hierarchy(self, element_id: str) -> Optional[Dict[str, Any]]:
        """
        Get hierarchical information for a specific element.
        
        Args:
            element_id: ID of the element to analyze
            
        Returns:
            Element hierarchy information or None if not found
        """
        if not self._last_analysis:
            return None
        
        element = self._last_analysis.get_interactive_element(element_id)
        if not element:
            return None
        
        return {
            "element_id": element_id,
            "hierarchy": element.hierarchy,
            "parent": self._last_analysis.get_interactive_element(element.hierarchy.parent),
            "children": [self._last_analysis.get_interactive_element(child_id) 
                        for child_id in element.hierarchy.children],
            "siblings": [self._last_analysis.get_interactive_element(sibling_id) 
                        for sibling_id in element.hierarchy.siblings]
        }
    
    async def find_similar_elements(self, target_element_id: str) -> List[InteractiveElement]:
        """
        Find elements similar to the target element.
        
        Args:
            target_element_id: ID of the target element
            
        Returns:
            List of similar elements
        """
        if not self._last_analysis:
            return []
        
        target = self._last_analysis.get_interactive_element(target_element_id)
        if not target:
            return []
        
        similar_elements = []
        for element in self._last_analysis.interactive_elements:
            if element.element_id == target_element_id:
                continue
                
            similarity_score = self._calculate_element_similarity(target, element)
            if similarity_score > 0.7:  # Threshold for similarity
                similar_elements.append(element)
        
        # Sort by similarity (highest first)
        similar_elements.sort(key=lambda x: self._calculate_element_similarity(target, x), reverse=True)
        return similar_elements
    
    async def get_accessibility_info(self, element_id: str) -> Optional[AccessibilityInfo]:
        """
        Get accessibility information for a specific element.
        
        Args:
            element_id: ID of the element
            
        Returns:
            Accessibility information or None if not found
        """
        if not self._last_analysis:
            return None
        
        element = self._last_analysis.get_interactive_element(element_id)
        return element.accessibility_info if element else None
    
    def get_last_analysis(self) -> Optional[DOMAnalysisResult]:
        """Get the last analysis result."""
        return self._last_analysis
    
    def clear_cache(self) -> None:
        """Clear the analysis cache."""
        self._analysis_cache.clear()
        self.logger.info("Analysis cache cleared")
    
    # Private helper methods
    
    def _generate_cache_key(self, html_source: str, url: str) -> str:
        """Generate a cache key for the analysis result."""
        import hashlib
        content = f"{url}:{len(html_source)}:{hash(html_source)}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _cache_result(self, cache_key: str, result: DOMAnalysisResult) -> None:
        """Cache an analysis result."""
        max_size = self.config.get('max_cache_size', 100)
        
        if len(self._analysis_cache) >= max_size:
            # Remove oldest entry
            oldest_key = next(iter(self._analysis_cache))
            del self._analysis_cache[oldest_key]
        
        self._analysis_cache[cache_key] = result
    
    async def _extract_page_title(self, dom_tree) -> Optional[str]:
        """Extract page title from DOM tree."""
        try:
            title_element = dom_tree.find('title')
            return title_element.get_text(strip=True) if title_element else None
        except Exception:
            return None
    
    async def _generate_performance_hints(self, dom_tree, interactive_elements: List[InteractiveElement]) -> Dict[str, Any]:
        """Generate performance optimization hints."""
        hints = {
            "total_elements": len(dom_tree.find_all()),
            "interactive_elements": len(interactive_elements),
            "forms": len([e for e in interactive_elements if e.element_type == ElementType.FORM]),
            "complexity": "low"
        }
        
        # Determine complexity
        total_elements = hints["total_elements"]
        if total_elements > 1000:
            hints["complexity"] = "high"
        elif total_elements > 500:
            hints["complexity"] = "medium"
        
        # Add optimization suggestions
        hints["suggestions"] = []
        if hints["interactive_elements"] > 100:
            hints["suggestions"].append("Consider pagination or lazy loading for better performance")
        
        return hints
    
    async def _build_element_relationships(self, interactive_elements: List[InteractiveElement]) -> Dict[str, List[str]]:
        """Build relationships between elements."""
        relationships = {}
        
        for element in interactive_elements:
            relationships[element.element_id] = {
                "parent": element.hierarchy.parent,
                "children": element.hierarchy.children,
                "siblings": element.hierarchy.siblings,
                "form_association": getattr(element, 'form_id', None)
            }
        
        return relationships
    
    def _calculate_element_similarity(self, element1: InteractiveElement, element2: InteractiveElement) -> float:
        """Calculate similarity score between two elements."""
        score = 0.0
        
        # Same element type
        if element1.element_type == element2.element_type:
            score += 0.3
        
        # Same semantic type
        if element1.semantic_type == element2.semantic_type:
            score += 0.2
        
        # Similar text content
        if element1.text_content and element2.text_content:
            text_similarity = len(set(element1.text_content.lower().split()) & 
                                set(element2.text_content.lower().split())) / \
                            max(len(element1.text_content.split()), len(element2.text_content.split()))
            score += text_similarity * 0.2
        
        # Similar attributes
        common_attrs = set(element1.attributes.keys()) & set(element2.attributes.keys())
        if common_attrs:
            attr_similarity = len(common_attrs) / max(len(element1.attributes), len(element2.attributes))
            score += attr_similarity * 0.3
        
        return min(score, 1.0)