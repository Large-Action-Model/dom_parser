#!/usr/bin/env python3
"""
Working Comprehensive DOM Analysis Example

This example demonstrates the actual working API of the DOM Parser library
using the Example Domain sample HTML file (dom_sample_2.html).

This example shows:
- Complete DOM analysis using the correct API
- Interactive element extraction and analysis
- Form structure analysis
- Semantic block extraction
- Navigation structure analysis
- Accessibility information
- Performance metrics
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dom_parser import DOMParser
from dom_parser.types.element_data_types import ElementType, InteractionType


async def comprehensive_dom_analysis():
    """Perform comprehensive DOM analysis using the actual API."""
    
    # Load the sample HTML file
    sample_path = Path(__file__).parent / "samples" / "dom_sample_2.html" 
    
    print("Comprehensive DOM Analysis Example")
    print("=" * 60)
    print(f"Loading HTML from: {sample_path.name}")
    
    with open(sample_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    print(f"HTML content size: {len(html_content):,} characters")
    
    # Parse the HTML using DOM Parser
    parser = DOMParser()
    result = await parser.parse_page(html_content, f"file://{sample_path}")
    
    print(f"\n{'='*60}")
    print("ANALYSIS RESULTS")
    print(f"{'='*60}")
    
    # Basic document information
    print(f"\n📄 Document Information:")
    print(f"- Title: {result.source_title or 'Not available'}")
    print(f"- URL: {result.source_url}")
    print(f"- Processing time: {result.processing_time:.4f} seconds")
    print(f"- Analysis timestamp: {result.analysis_timestamp}")
    
    # Interactive elements analysis
    print(f"\n🎯 Interactive Elements ({len(result.interactive_elements)} total):")
    if result.interactive_elements:
        element_types = {}
        for element in result.interactive_elements:
            elem_type = element.element_type.name if element.element_type else 'UNKNOWN'
            element_types[elem_type] = element_types.get(elem_type, 0) + 1
        
        for elem_type, count in sorted(element_types.items()):
            print(f"- {elem_type}: {count}")
        
        print(f"\n📝 Element Details:")
        for i, element in enumerate(result.interactive_elements[:5], 1):
            print(f"{i}. {element.tag_name} (ID: {element.element_id})")
            print(f"   Text: '{element.text_content[:50]}...' " if len(element.text_content) > 50 else f"   Text: '{element.text_content}'")
            print(f"   Type: {element.element_type.name if element.element_type else 'UNKNOWN'}")
            if element.attributes:
                attrs = ', '.join([f"{k}='{v[:20]}...'" if len(str(v)) > 20 else f"{k}='{v}'" 
                                 for k, v in list(element.attributes.items())[:3]])
                print(f"   Attributes: {attrs}")
            if element.interaction_types:
                interactions = ', '.join([it.name for it in element.interaction_types])
                print(f"   Interactions: {interactions}")
            print()
    else:
        print("- No interactive elements found")
    
    # Page structure analysis
    print(f"\n🏗️ Page Structure:")
    structure = result.page_structure
    print(f"- Layout type: {structure.layout_type}")
    print(f"- Sections: {len(structure.sections)}")
    print(f"- Navigation areas: {len(structure.navigation_areas)}")
    print(f"- Content areas: {len(structure.content_areas)}")
    print(f"- Sidebar areas: {len(structure.sidebar_areas)}")
    print(f"- Single page app: {structure.is_single_page_app}")
    print(f"- Dynamic content: {structure.has_dynamic_content}")
    print(f"- Estimated complexity: {structure.estimated_complexity}")
    
    # Form structures
    print(f"\n📋 Form Structures ({len(result.form_structures)} total):")
    if result.form_structures:
        for i, form in enumerate(result.form_structures, 1):
            print(f"{i}. Form ID: {form.form_id}")
            print(f"   Action: {form.action or 'Not specified'}")
            print(f"   Method: {form.method}")
            print(f"   Fields: {len(form.fields)}")
            if form.fields:
                for field in form.fields[:3]:
                    print(f"     - {field.field_type.name if field.field_type else 'Unknown'}: {field.name}")
    else:
        print("- No forms found")
    
    # Semantic blocks
    print(f"\n🔍 Semantic Blocks ({len(result.semantic_blocks)} total):")
    if result.semantic_blocks:
        block_types = {}
        for block in result.semantic_blocks:
            block_type = block.semantic_type.name if block.semantic_type else 'UNKNOWN'
            block_types[block_type] = block_types.get(block_type, 0) + 1
        
        for block_type, count in sorted(block_types.items()):
            print(f"- {block_type}: {count}")
            
        print(f"\n📄 Block Details:")
        for i, block in enumerate(result.semantic_blocks[:3], 1):
            print(f"{i}. {block.semantic_type.name if block.semantic_type else 'Unknown'}")
            print(f"   Content: '{block.text_content[:60]}...' " if len(block.text_content) > 60 else f"   Content: '{block.text_content}'")
            print(f"   Elements: {len(block.element_ids)}")
    else:
        print("- No semantic blocks found")
    
    # Navigation structure
    print(f"\n🧭 Navigation Structure:")
    nav = result.navigation_structure
    if nav.primary_navigation:
        print(f"- Primary navigation: Found")
    if nav.secondary_navigation:
        print(f"- Secondary navigation: Found")
    if nav.breadcrumbs:
        print(f"- Breadcrumbs: Found")
    if nav.pagination:
        print(f"- Pagination: Found")
    if nav.skip_links:
        print(f"- Skip links: {len(nav.skip_links)}")
    if not any([nav.primary_navigation, nav.secondary_navigation, nav.breadcrumbs, nav.pagination, nav.skip_links]):
        print("- No navigation elements detected")
    
    # Accessibility information
    print(f"\n♿ Accessibility Analysis:")
    accessibility = result.accessibility_tree
    print(f"- Role: {accessibility.role.name if accessibility.role else 'Not specified'}")
    print(f"- Label: {accessibility.label or 'Not specified'}")
    print(f"- Description: {accessibility.description or 'Not specified'}")
    if accessibility.attributes:
        print(f"- ARIA attributes: {len(accessibility.attributes)}")
        for attr, value in list(accessibility.attributes.items())[:3]:
            print(f"  • {attr}: {value}")
    
    # Performance hints
    print(f"\n⚡ Performance Hints:")
    if result.performance_hints:
        for category, hints in result.performance_hints.items():
            if isinstance(hints, list) and hints:
                print(f"- {category}: {len(hints)} suggestions")
            elif hints:
                print(f"- {category}: {hints}")
    else:
        print("- No performance hints available")
    
    # Quality metrics
    print(f"\n📊 Quality Metrics:")
    if result.confidence_scores:
        print("- Confidence scores:")
        for metric, score in result.confidence_scores.items():
            print(f"  • {metric}: {score:.2f}")
    
    if result.coverage_metrics:
        print("- Coverage metrics:")
        for metric, coverage in result.coverage_metrics.items():
            print(f"  • {metric}: {coverage:.1%}")
    
    # Errors and warnings
    if result.errors:
        print(f"\n❌ Errors ({len(result.errors)}):")
        for error in result.errors[:3]:
            print(f"- {error}")
    
    if result.warnings:
        print(f"\n⚠️  Warnings ({len(result.warnings)}):")
        for warning in result.warnings[:3]:
            print(f"- {warning}")
    
    # Element relationships
    if result.element_relationships:
        print(f"\n🔗 Element Relationships:")
        print(f"- Total relationships: {len(result.element_relationships)}")
        for element_id, related_ids in list(result.element_relationships.items())[:3]:
            if related_ids:
                print(f"  • {element_id}: {len(related_ids)} related elements")
    
    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*60}")
    print(f"Total interactive elements processed: {len(result.interactive_elements)}")
    print(f"Total processing time: {result.processing_time:.4f} seconds")
    
    return result


if __name__ == "__main__":
    # Run the comprehensive example
    asyncio.run(comprehensive_dom_analysis())