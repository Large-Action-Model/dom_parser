#!/usr/bin/env python3
"""
DOM Parser Integration Example

Demonstrates how to use the DOM Parser component with the Browser Controller
for complete web page analysis and AI-driven interaction.

This example shows:
1. Setting up both Browser Controller and DOM Parser
2. Navigating to a webpage 
3. Extracting HTML content
4. Performing comprehensive DOM analysis
5. Accessing structured results for AI decision-making
"""

import asyncio
import sys
import os
from pathlib import Path
from typing import Dict, Any


# Add the parent directory to the Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import DOM Parser
from dom_parser import DOMParser
from dom_parser.types.element_data_types import ElementType, SemanticType

# Browser Controller imports (adjust path as needed)
try:
    # Assuming browser_controller is in parent directory or installed
    from browser_controller import BrowserController, BrowserConfig, BrowserType
    BROWSER_CONTROLLER_AVAILABLE = True
except ImportError:
    print("⚠️  Browser Controller not found. Running DOM Parser in standalone mode.")
    BROWSER_CONTROLLER_AVAILABLE = False
    
    # Create mock classes for demonstration
    class BrowserController:
        def __init__(self, config): pass
        async def __aenter__(self): return self
        async def __aexit__(self, *args): pass
        async def create_session(self): return MockSession()
    
    class MockSession:
        async def navigate_to(self, url): pass
        async def get_page_info(self): return MockPageInfo()
    
    class MockPageInfo:
        url = "https://example.com"
        title = "Example Page"
        source = """
        <!DOCTYPE html>
        <html>
        <head><title>Example Page</title></head>
        <body>
            <header>
                <nav>
                    <a href="/">Home</a>
                    <a href="/about">About</a>
                </nav>
            </header>
            <main>
                <h1>Welcome to Example</h1>
                <form action="/search" method="GET">
                    <input type="search" name="q" placeholder="Search...">
                    <button type="submit">Search</button>
                </form>
                <article>
                    <h2>Main Content</h2>
                    <p>This is the main content of the page.</p>
                </article>
            </main>
            <aside>
                <h3>Sidebar</h3>
                <div>Related links</div>
            </aside>
            <footer>
                <p>&copy; 2024 Example Site</p>
            </footer>
        </body>
        </html>
        """
        timestamp = 1234567890.0
        metadata = {}


async def demo_basic_usage():
    """Basic DOM Parser usage demonstration."""
    print("🔍 DOM Parser - Basic Usage Demo")
    print("=" * 50)
    
    # Initialize DOM Parser
    dom_parser = DOMParser({
        'enable_cache': True,
        'include_hidden_elements': False,
        'confidence_threshold': 0.7
    })
    
    # Sample HTML for analysis
    sample_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>E-commerce Demo Page</title>
        <meta charset="UTF-8">
    </head>
    <body>
        <header>
            <nav role="navigation">
                <a href="/" id="home-link">Home</a>
                <a href="/products">Products</a>
                <a href="/cart" class="cart-link">Cart (2)</a>
            </nav>
        </header>
        
        <main role="main">
            <h1>Featured Products</h1>
            
            <form action="/search" method="GET" class="search-form">
                <input type="search" name="query" placeholder="Search products..." required>
                <button type="submit">Search</button>
            </form>
            
            <section class="product-grid">
                <article class="product-card">
                    <h2>Wireless Headphones</h2>
                    <p>High-quality wireless headphones with noise cancellation.</p>
                    <button class="add-to-cart" data-product-id="123">Add to Cart</button>
                </article>
                
                <article class="product-card">
                    <h2>Smartphone</h2>
                    <p>Latest smartphone with advanced features.</p>
                    <button class="add-to-cart" data-product-id="456">Add to Cart</button>
                </article>
            </section>
            
            <form action="/newsletter" method="POST" class="newsletter-form">
                <h3>Subscribe to Newsletter</h3>
                <input type="email" name="email" placeholder="Your email" required>
                <input type="checkbox" name="terms" required>
                <label for="terms">I agree to terms and conditions</label>
                <button type="submit">Subscribe</button>
            </form>
        </main>
        
        <aside class="sidebar">
            <h3>Categories</h3>
            <ul>
                <li><a href="/electronics">Electronics</a></li>
                <li><a href="/clothing">Clothing</a></li>
            </ul>
        </aside>
        
        <footer>
            <p>&copy; 2024 Demo Store. All rights reserved.</p>
            <nav class="footer-nav">
                <a href="/privacy">Privacy Policy</a>
                <a href="/contact">Contact</a>
            </nav>
        </footer>
    </body>
    </html>
    """
    
    # Perform DOM analysis
    print("📝 Analyzing HTML content...")
    analysis_result = await dom_parser.parse_page(
        html_source=sample_html,
        url="https://demo-store.com",
        metadata={"page_type": "ecommerce", "demo": True}
    )
    
    # Display results
    print(f"✅ Analysis completed in {analysis_result.processing_time:.2f} seconds")
    print(f"📊 Found {len(analysis_result.interactive_elements)} interactive elements")
    print(f"🏗️  Page structure: {analysis_result.page_structure.layout_type}")
    print(f"📝 Semantic blocks: {len(analysis_result.semantic_blocks)}")
    print(f"📋 Forms: {len(analysis_result.form_structures)}")
    
    return analysis_result


async def demo_element_analysis(analysis_result):
    """Demonstrate element analysis capabilities."""
    print("\n🎯 Interactive Elements Analysis")
    print("=" * 50)
    
    # Group elements by type
    element_groups: Dict[ElementType, int] = {}
    for element in analysis_result.interactive_elements:
        element_groups[element.element_type] = element_groups.get(element.element_type, 0) + 1
    
    print("📊 Element Types Found:")
    for element_type, count in element_groups.items():
        print(f"   • {element_type.value}: {count}")
    
    # Find clickable elements
    clickable_elements = analysis_result.get_clickable_elements()
    print(f"\n🖱️  Clickable Elements: {len(clickable_elements)}")
    for element in clickable_elements[:3]:  # Show first 3
        print(f"   • {element.tag_name}: '{element.visible_text}' (ID: {element.element_id})")
    
    # Find form fields
    form_fields = analysis_result.get_form_fields()
    print(f"\n📝 Form Fields: {len(form_fields)}")
    for field in form_fields[:3]:  # Show first 3
        print(f"   • {field.form_field_type.value if field.form_field_type else 'unknown'}: {field.attributes.get('placeholder', field.visible_text) or 'No label'}")


async def demo_semantic_analysis(analysis_result):
    """Demonstrate semantic analysis capabilities."""
    print("\n🧠 Semantic Analysis")
    print("=" * 50)
    
    # Analyze semantic blocks
    print("📦 Semantic Blocks:")
    for block in analysis_result.semantic_blocks:
        print(f"   • {block.semantic_type.value}: {block.text_content[:50]}...")
    
    # Analyze forms by type
    print(f"\n📋 Form Analysis:")
    for form in analysis_result.form_structures:
        form_type = form.form_type.value if form.form_type else "unknown"
        print(f"   • {form_type} form: {len(form.fields)} fields, action='{form.action}'")
        
        # Show field details
        for field in form.fields[:2]:  # First 2 fields
            field_type = field.form_field_type.value if field.form_field_type else "unknown"
            print(f"     - {field_type}: {field.attributes.get('placeholder', field.visible_text) or 'No label'}")
    
    # Navigation structure
    nav_structure = analysis_result.navigation_structure
    if nav_structure.primary_navigation:
        print(f"\n🧭 Navigation: {len(nav_structure.primary_navigation.links)} links in primary nav")


async def demo_browser_integration():
    """Demonstrate integration with Browser Controller."""
    if not BROWSER_CONTROLLER_AVAILABLE:
        print("\n🤖 Browser Integration Demo (Mock Mode)")
        print("=" * 50)
        print("Using mock browser session...")
        
        # Create mock browser session
        controller = BrowserController(None)
        dom_parser = DOMParser()
        
        async with controller:
            session = await controller.create_session()
            await session.navigate_to("https://example.com")
            page_info = await session.get_page_info()
            
            # Analyze with DOM Parser
            analysis_result = await dom_parser.parse_page_from_browser_info(page_info)
            
            print(f"✅ Analyzed page: {analysis_result.source_title}")
            print(f"📊 Found {len(analysis_result.interactive_elements)} interactive elements")
        
        return
    
    print("\n🤖 Browser Controller Integration Demo")
    print("=" * 50)
    
    # Configure browser
    config = BrowserConfig(
        browser_type=BrowserType.CHROME,
        headless=True,
        window_size=(1280, 720)
    )
    
    # Initialize components
    controller = BrowserController(config)
    dom_parser = DOMParser({
        'enable_cache': True,
        'max_cache_size': 50
    })
    
    try:
        async with controller:
            # Create browser session
            session = await controller.create_session()
            
            # Navigate to a test page
            print("🌐 Navigating to test page...")
            await session.navigate_to("https://httpbin.org/forms/post")
            
            # Get page information
            page_info = await session.get_page_info()
            print(f"📄 Page loaded: {page_info.title}")
            
            # Analyze with DOM Parser
            print("🔍 Performing DOM analysis...")
            analysis_result = await dom_parser.parse_page_from_browser_info(page_info)
            
            # Display integrated results
            print(f"✅ Analysis completed")
            print(f"📊 Interactive elements: {len(analysis_result.interactive_elements)}")
            print(f"📋 Forms found: {len(analysis_result.form_structures)}")
            
            # Show some actionable elements
            clickable = analysis_result.get_clickable_elements()
            print(f"🖱️  Clickable elements: {len(clickable)}")
            
            for element in clickable[:3]:
                locators = ", ".join([f"{k}: {v}" for k, v in element.locators.items() if k in ['id', 'css']])
                print(f"   • {element.visible_text or element.tag_name} ({locators})")
            
    except Exception as e:
        print(f"❌ Browser integration failed: {e}")
        print("This is expected if browser drivers are not properly installed.")


async def demo_advanced_features(analysis_result):
    """Demonstrate advanced DOM Parser features."""
    print("\n🚀 Advanced Features Demo")
    print("=" * 50)
    
    # Element similarity analysis
    if analysis_result.interactive_elements:
        target_element = analysis_result.interactive_elements[0]
        dom_parser = DOMParser()
        dom_parser._last_analysis = analysis_result  # Set for similarity search
        
        similar_elements = await dom_parser.find_similar_elements(target_element.element_id)
        print(f"🔍 Similar elements to '{target_element.visible_text}': {len(similar_elements)}")
    
    # Performance insights
    hints = analysis_result.performance_hints
    print(f"\n⚡ Performance Insights:")
    print(f"   • Page complexity: {hints.get('complexity', 'unknown')}")
    print(f"   • Total elements: {hints.get('total_elements', 0)}")
    print(f"   • Interactive elements: {hints.get('interactive_elements', 0)}")
    
    # Quality metrics
    if analysis_result.confidence_scores:
        avg_confidence = sum(analysis_result.confidence_scores.values()) / len(analysis_result.confidence_scores)
        print(f"   • Average confidence: {avg_confidence:.2f}")
    
    # Accessibility insights
    print(f"\n♿ Accessibility Features:")
    accessibility_count = sum(1 for elem in analysis_result.interactive_elements 
                            if elem.accessibility_info.label or elem.accessibility_info.role)
    print(f"   • Elements with accessibility info: {accessibility_count}")


async def main():
    """Main demonstration function."""
    print("🎯 DOM Parser & Browser Controller Integration Demo")
    print("=" * 60)
    print("This demo shows how to use the DOM Parser component")
    print("for intelligent web page analysis and AI automation.")
    print("=" * 60)
    
    try:
        # Basic usage demo
        analysis_result = await demo_basic_usage()
        
        # Element analysis
        await demo_element_analysis(analysis_result)
        
        # Semantic analysis
        await demo_semantic_analysis(analysis_result)
        
        # Advanced features
        await demo_advanced_features(analysis_result)
        
        # Browser integration
        await demo_browser_integration()
        
        print("\n✅ Demo completed successfully!")
        print("\n💡 Next Steps:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Install browser controller component")
        print("   3. Integrate DOM Parser into your LAM system")
        print("   4. Customize configuration for your use case")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("Starting DOM Parser Demo...")
    asyncio.run(main())