#!/usr/bin/env python3
"""
DOM Analysis Example using Sample HTML

This example demonstrates comprehensive DOM analysis using dom_sample_2.html
which contains the Example Domain page with various HTML elements, CSS styling,
and semantic structure.

The example showcases:
- DOM parsing and element extraction
- Structure analysis and hierarchy mapping
- Form detection and analysis
- Accessibility analysis
- Element classification
- CSS selector and XPath generation
- Semantic content extraction
"""

import asyncio
import sys
import os
from pathlib import Path
from pprint import pprint

# Add the parent directory to the Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import DOM Parser components
from dom_parser import DOMParser


async def load_sample_html() -> str:
    """Load the sample HTML file for analysis."""
    sample_path = Path(__file__).parent / "samples" / "dom_sample_3.html"
    
    if not sample_path.exists():
        raise FileNotFoundError(f"Sample file not found: {sample_path}")
    
    with open(sample_path, 'r', encoding='utf-8') as file:
        return file.read()


async def basic_dom_analysis(html_content: str):
    """Perform basic DOM parsing and element extraction."""
    print("=" * 60)
    print("BASIC DOM ANALYSIS")
    print("=" * 60)
    
    # Initialize the DOM parser
    parser = DOMParser()
    sample_path = Path(__file__).parent / "samples" / "dom_sample_2.html"
    
    # Parse the HTML content
    result = await parser.parse_page(html_content, f"file://{sample_path}")
    
    print(f"Document Title: {result.source_title or 'Not available'}")
    print(f"Document URL: {result.source_url}")
    print(f"Interactive Elements: {len(result.interactive_elements)}")
    print(f"Processing Time: {result.processing_time:.3f}s")
    
    # Display document metadata
    if result.metadata:
        print("\nDocument Metadata:")
        for key, value in result.metadata.items():
            if isinstance(value, list):
                print(f"  {key}: {', '.join(value)}")
            else:
                print(f"  {key}: {value}")
    
    return result


async def analyze_document_structure(analysis_result):
    """Analyze the document structure and hierarchy."""
    print("\n" + "=" * 60)
    print("DOCUMENT STRUCTURE ANALYSIS")
    print("=" * 60)
    
    # Count elements by type
    element_counts = {}
    for element in analysis_result.interactive_elements:
        tag_name = element.tag_name
        element_counts[tag_name] = element_counts.get(tag_name, 0) + 1
    
    print("\nElement Distribution:")
    for tag, count in sorted(element_counts.items()):
        print(f"  {tag}: {count}")
    
    # Find semantic elements
    semantic_elements = ['header', 'nav', 'main', 'article', 'section', 'aside', 'footer']
    found_semantic = []
    
    for element in analysis_result.interactive_elements:
        if element.tag_name in semantic_elements:
            found_semantic.append(element.tag_name)
    
    if found_semantic:
        print(f"\nSemantic Elements Found: {', '.join(set(found_semantic))}")
    else:
        print("\nNo HTML5 semantic elements found")
    
    # Analyze document sections
    headings = [e for e in analysis_result.interactive_elements if e.tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']]
    if headings:
        print(f"\nDocument Headings ({len(headings)}):")
        for heading in headings:
            print(f"  {heading.tag_name}: {heading.text_content[:50]}")
    
    return element_counts


async def classify_elements(analysis_result):
    """Classify elements by their type and functionality."""
    print("\n" + "=" * 60)
    print("ELEMENT CLASSIFICATION")
    print("=" * 60)
    
    # Use the already classified elements from the analysis result
    classified_elements = {
        'interactive': [],
        'content': [],
        'structural': [],
        'media': [],
        'form': []
    }
    
    for element in analysis_result.interactive_elements:
        # Classify based on element type and tag name
        if element.tag_name in ['input', 'button', 'select', 'textarea']:
            classified_elements['form'].append(element)
        elif element.tag_name in ['a', 'button']:
            classified_elements['interactive'].append(element)
        elif element.tag_name in ['img', 'video', 'audio']:
            classified_elements['media'].append(element)
        elif element.tag_name in ['p', 'span', 'div']:
            classified_elements['content'].append(element)
        else:
            classified_elements['structural'].append(element)
    
    # Display classification results
    for category, elements in classified_elements.items():
        if elements:
            print(f"\n{category.upper()} ELEMENTS ({len(elements)}):")
            for element in elements[:5]:  # Show first 5 elements
                attrs_str = ", ".join([f"{k}='{v}'" for k, v in list(element.attributes.items())[:2]])
                if attrs_str:
                    attrs_str = f" ({attrs_str})"
                print(f"  {element.tag_name}{attrs_str}")
            if len(elements) > 5:
                print(f"  ... and {len(elements) - 5} more")
    
    return classified_elements


async def analyze_links_and_navigation(analysis_result):
    """Analyze links and navigation elements."""
    print("\n" + "=" * 60)
    print("LINKS AND NAVIGATION ANALYSIS")
    print("=" * 60)
    
    # Find all links
    links = [e for e in analysis_result.interactive_elements if e.tag_name == 'a']
    
    if links:
        print(f"Total Links Found: {len(links)}")
        
        # Categorize links
        internal_links = []
        external_links = []
        anchor_links = []
        
        for link in links:
            href = link.attributes.get('href', '')
            if href:
                if href.startswith('#'):
                    anchor_links.append(link)
                elif href.startswith('http') and 'example.org' not in href:
                    external_links.append(link)
                else:
                    internal_links.append(link)
        
        print(f"  Internal Links: {len(internal_links)}")
        print(f"  External Links: {len(external_links)}")
        print(f"  Anchor Links: {len(anchor_links)}")
        
        # Display link details
        if internal_links:
            print("\nInternal Links:")
            for link in internal_links[:3]:  # Show first 3
                href = link.attributes.get('href', '')
                text = link.text_content.strip()[:30]
                print(f"  {href} -> '{text}'")
        
        if external_links:
            print("\nExternal Links:")
            for link in external_links[:3]:  # Show first 3
                href = link.attributes.get('href', '')
                text = link.text_content.strip()[:30]
                print(f"  {href} -> '{text}'")
    
    else:
        print("No links found in the document")


async def accessibility_analysis(analysis_result):
    """Perform accessibility analysis on the DOM."""
    print("\n" + "=" * 60)
    print("ACCESSIBILITY ANALYSIS")
    print("=" * 60)
    
    # Use the accessibility information from the analysis result
    accessibility_info = analysis_result.accessibility_tree
    
    print("Accessibility Features Found:")
    print(f"  Role: {accessibility_info.role.name if accessibility_info.role else 'None'}")
    print(f"  Label: {accessibility_info.label or 'None'}")
    print(f"  Description: {accessibility_info.description or 'None'}")
    
    # Check for images with alt text
    images = [e for e in analysis_result.interactive_elements if e.tag_name == 'img']
    images_with_alt = [e for e in images if e.attributes.get('alt')]
    
    print(f"  Images: {len(images)} total, {len(images_with_alt)} with alt text")
    
    # Check for form labels
    labels = [e for e in analysis_result.interactive_elements if e.tag_name == 'label']
    inputs = [e for e in analysis_result.interactive_elements if e.tag_name == 'input']
    
    print(f"  Form Labels: {len(labels)}")
    print(f"  Form Inputs: {len(inputs)}")
    
    # Check for ARIA attributes
    aria_elements = []
    for element in analysis_result.interactive_elements:
        aria_attrs = [attr for attr in element.attributes.keys() if attr.startswith('aria-')]
        if aria_attrs:
            aria_elements.append((element, aria_attrs))
    
    if aria_elements:
        print(f"  Elements with ARIA attributes: {len(aria_elements)}")
        for element, attrs in aria_elements[:3]:  # Show first 3
            print(f"    {element.tag_name}: {', '.join(attrs)}")
    
    # Check for heading hierarchy
    headings = [e for e in analysis_result.interactive_elements if e.tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']]
    if headings:
        heading_levels = [int(h.tag_name[1]) for h in headings]
        print(f"  Heading Structure: {' -> '.join([f'H{level}' for level in heading_levels])}") 
    
    return accessibility_info
async def css_and_xpath_generation(analysis_result):
    """Generate CSS selectors and XPaths for key elements."""
    print("\n" + "=" * 60)
    print("CSS SELECTORS AND XPATH GENERATION")
    print("=" * 60)
    
    # Show existing locators from the analysis result
    interesting_elements = []
    
    # Add title, headings, and links
    for element in analysis_result.interactive_elements:
        class_attr = element.attributes.get('class', '')
        # Handle class attribute whether it's a string or list
        if isinstance(class_attr, list):
            class_str = ' '.join(class_attr)
        else:
            class_str = class_attr
            
        if element.tag_name in ['title', 'h1', 'h2', 'h3', 'a'] or \
           element.attributes.get('id') or \
           'nav' in class_str.lower():
            interesting_elements.append(element)
    
    if interesting_elements:
        print("CSS Selectors and XPaths for Key Elements:")
        print()
        
        for element in interesting_elements[:5]:  # Show first 5
            # Use existing locators from the element
            css_selector = element.locators.get('css', 'Not generated')
            xpath = element.locators.get('xpath', 'Not generated')
            
            # Display information
            tag_info = element.tag_name
            if element.attributes.get('id'):
                tag_info += f"#{element.attributes['id']}"
            elif element.attributes.get('class'):
                class_attr = element.attributes['class']
                if isinstance(class_attr, list):
                    classes = class_attr[:2]  # First 2 classes
                else:
                    classes = class_attr.split()[:2]  # First 2 classes
                tag_info += f".{'.'.join(classes)}"
            
            text = element.text_content.strip()[:40]
            if text:
                tag_info += f" ('{text}')"
            
            print(f"Element: {tag_info}")
            print(f"  CSS: {css_selector}")
            print(f"  XPath: {xpath}")
            print()


async def form_analysis(analysis_result):
    """Analyze forms and form elements."""
    print("\n" + "=" * 60)
    print("FORM ANALYSIS")
    print("=" * 60)
    
    # Use form structures from the analysis result
    forms = analysis_result.form_structures
    
    if forms:
        print(f"Forms Found: {len(forms)}")
        
        for i, form in enumerate(forms, 1):
            print(f"\nForm {i}:")
            print(f"  Form ID: {form.form_id}")
            print(f"  Method: {form.method}")
            print(f"  Action: {form.action if form.action else '(current page)'}")
            print(f"  Fields: {len(form.fields)}")
            
            if form.fields:
                # Categorize field types based on tag names and types
                field_types = {}
                for field in form.fields:
                    # Get field type from the InteractiveElement
                    if hasattr(field, 'form_field_type') and field.form_field_type:
                        field_type = field.form_field_type.name
                    else:
                        # Fallback to tag name and input type
                        if field.tag_name == 'input':
                            input_type = field.attributes.get('type', 'text')
                            field_type = f"input[{input_type}]"
                        else:
                            field_type = field.tag_name
                    
                    field_types[field_type] = field_types.get(field_type, 0) + 1
                
                for field_type, count in field_types.items():
                    print(f"    {field_type}: {count}")
    else:
        print("No forms found in the document")


async def semantic_content_extraction(analysis_result):
    """Extract semantic content from the document."""
    print("\n" + "=" * 60)
    print("SEMANTIC CONTENT EXTRACTION")
    print("=" * 60)
    
    # Use semantic blocks from the analysis result
    semantic_blocks = analysis_result.semantic_blocks
    
    if semantic_blocks:
        print(f"Semantic Blocks Found: {len(semantic_blocks)}")
        for i, block in enumerate(semantic_blocks[:3], 1):
            print(f"\nBlock {i}:")
            print(f"  Type: {block.semantic_type.name if block.semantic_type else 'Unknown'}")
            print(f"  Content: {block.text_content[:100]}...")
            print(f"  Elements: {len(block.element_ids)}")
    
    # Extract main content from interactive elements
    main_content = []
    
    # Look for main content indicators
    content_elements = [e for e in analysis_result.interactive_elements if e.tag_name in ['p', 'div', 'article', 'section']]
    
    # Find elements with substantial text content
    for element in content_elements:
        text = element.text_content.strip()
        if len(text) > 50:  # Substantial text content
            main_content.append((element.tag_name, text[:100]))
    
    if main_content:
        print("Main Content Sections:")
        for tag, text in main_content[:3]:  # Show first 3
            print(f"  {tag}: {text}...")
    
    # Extract metadata from analysis result
    metadata = analysis_result.metadata
    
    print(f"\nMetadata Available: {len(metadata) if metadata else 0}")
    if metadata:
        print("Available Metadata:")
        for key, value in list(metadata.items())[:5]:
            print(f"  {key}: {str(value)[:50]}...")
    
    # Also check interactive elements for meta tags
    meta_elements = [e for e in analysis_result.interactive_elements if e.tag_name == 'meta']
    
    print(f"\nMetadata Elements: {len(meta_elements)}")
    
    important_meta = []
    for meta in meta_elements:
        name = meta.attributes.get('name', '')
        property_attr = meta.attributes.get('property', '')
        content = meta.attributes.get('content', '')
        
        if name in ['description', 'keywords', 'author', 'viewport']:
            important_meta.append((f"name='{name}'", content))
        elif property_attr.startswith('og:'):
            important_meta.append((f"property='{property_attr}'", content))
    
    if important_meta:
        print("Important Metadata:")
        for attr, content in important_meta:
            print(f"  {attr}: {content}")


async def performance_metrics(analysis_result, html_content: str):
    """Display performance and complexity metrics."""
    print("\n" + "=" * 60)
    print("PERFORMANCE METRICS")
    print("=" * 60)
    
    # Basic metrics
    print(f"HTML Size: {len(html_content):,} characters")
    print(f"Interactive Elements: {len(analysis_result.interactive_elements):,}")
    print(f"Processing Time: {analysis_result.processing_time:.4f} seconds")
    
    # Use performance hints from analysis result
    performance_hints = analysis_result.performance_hints
    
    if performance_hints:
        print("\nPerformance Analysis:")
        for hint_type, hint_value in performance_hints.items():
            print(f"  {hint_type}: {hint_value}")
    
    # Page structure complexity
    page_structure = analysis_result.page_structure
    print(f"\nPage Complexity: {page_structure.estimated_complexity}")
    print(f"Layout Type: {page_structure.layout_type}")
    print(f"Dynamic Content: {page_structure.has_dynamic_content}")
    
    # CSS and JavaScript resources
    stylesheets = [e for e in analysis_result.interactive_elements if e.tag_name == 'link' and 
                   e.attributes.get('rel') == 'stylesheet']
    scripts = [e for e in analysis_result.interactive_elements if e.tag_name == 'script']
    
    print(f"External Stylesheets: {len(stylesheets)}")
    print(f"Script Elements: {len(scripts)}")
    
    # Image resources
    images = [e for e in analysis_result.interactive_elements if e.tag_name == 'img']
    print(f"Images: {len(images)}")


async def main():
    """Main function to run the DOM analysis example."""
    print("DOM Parser - Comprehensive Analysis Example")
    print("Using dom_sample_2.html (Example Domain page)")
    print()
    
    try:
        # Load sample HTML
        print("Loading sample HTML file...")
        html_content = await load_sample_html()
        print(f"Loaded HTML content ({len(html_content):,} characters)")
        
        # Perform comprehensive DOM analysis
        analysis_result = await basic_dom_analysis(html_content)
        
        await analyze_document_structure(analysis_result)
        
        classified_elements = await classify_elements(analysis_result)
        
        await analyze_links_and_navigation(analysis_result)
        
        await accessibility_analysis(analysis_result)
        
        await css_and_xpath_generation(analysis_result)
        
        await form_analysis(analysis_result)
        
        await semantic_content_extraction(analysis_result)
        
        await performance_metrics(analysis_result, html_content)
        
        print("\n" + "=" * 60)
        print("ANALYSIS COMPLETE")
        print("=" * 60)
        print("\nThis example demonstrates the comprehensive DOM analysis")
        print("capabilities of the DOM Parser library. The analysis covers:")
        print("- Document structure and hierarchy")
        print("- Element classification and categorization") 
        print("- Accessibility features and compliance")
        print("- Navigation and link analysis")
        print("- Form detection and analysis")
        print("- CSS selector and XPath generation")
        print("- Semantic content extraction")
        print("- Performance and complexity metrics")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    # Run the async example
    exit_code = asyncio.run(main())
    sys.exit(exit_code)