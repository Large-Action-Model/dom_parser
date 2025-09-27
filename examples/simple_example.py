#!/usr/bin/env python3
"""
Simple DOM Analysis Example

This is a simplified example showing basic DOM analysis functionality
using the Example Domain sample HTML file (dom_sample_2.html).

This example demonstrates:
- Loading and parsing HTML
- Extracting basic document information
- Finding specific elements
- Analyzing document structure
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dom_parser import DOMParser


async def simple_dom_analysis():
    """Perform a simple DOM analysis of the example domain page."""
    
    # Load the sample HTML file
    sample_path = Path(__file__).parent / "samples" / "dom_sample_3.html" 
    
    print("Simple DOM Analysis Example")
    print("=" * 40)
    print(f"Loading HTML from: {sample_path.name}")
    
    with open(sample_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    print(f"HTML content size: {len(html_content):,} characters")
    
    # Parse the HTML using DOM Parser
    parser = DOMParser()
    result = await parser.parse_page(html_content, f"file://{sample_path}")
    
    print(f"\nDocument Analysis Results:")
    print(f"- Title: {result.source_title or 'Not available'}")
    print(f"- Interactive elements: {len(result.interactive_elements)}")
    print(f"- Processing time: {result.processing_time:.3f} seconds")
    
    # Count elements by tag type
    element_counts = {}
    for element in result.interactive_elements:
        tag = element.tag_name
        element_counts[tag] = element_counts.get(tag, 0) + 1
    
    print(f"\nInteractive Element Distribution:")
    for tag, count in sorted(element_counts.items()):
        print(f"- {tag}: {count}")
    
    # Find specific elements of interest
    print(f"\nSpecific Elements Found:")
    
    # Find all links
    links = [e for e in result.interactive_elements if e.tag_name == 'a']
    print(f"- Links: {len(links)}")
    for link in links[:3]:  # Show first 3 links
        href = link.attributes.get('href', '')
        text = link.text_content.strip()
        print(f"  • {text} -> {href}")
    
    # Find all paragraphs with content
    paragraphs = [e for e in result.interactive_elements if e.tag_name == 'p']
    print(f"- Paragraphs: {len(paragraphs)}")
    for p in paragraphs[:2]:  # Show first 2 paragraphs
        text = p.text_content.strip()[:60]
        if text:
            print(f"  • {text}...")
    
    # Show form structures
    print(f"- Forms: {len(result.form_structures)}")
    for form in result.form_structures:
        print(f"  • Form ID: {form.form_id}")
        print(f"    Fields: {len(form.fields)}")
    
    # Show semantic blocks
    if result.semantic_blocks:
        print(f"- Semantic blocks: {len(result.semantic_blocks)}")
        for block in result.semantic_blocks[:3]:
            semantic_type_name = block.semantic_type.name if block.semantic_type else 'Unknown'
            print(f"  • {semantic_type_name}: {block.text_content[:60]}...")
    
    # Show navigation structure
    if result.navigation_structure.primary_navigation:
        print(f"- Primary navigation found")
    if result.navigation_structure.breadcrumbs:
        print(f"- Breadcrumbs found")
    
    print(f"\nAnalysis complete!")
    return result


if __name__ == "__main__":
    # Run the simple example
    asyncio.run(simple_dom_analysis())