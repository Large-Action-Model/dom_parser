# Getting Started

This guide will help you get up and running with the DOM Parser & Analyzer component quickly.

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager
- Basic understanding of HTML and web development
- (Optional) Browser Controller component for full integration

## 🚀 Installation

### Step 1: Set Up Environment

First, create a virtual environment for your project:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

This will install:
- BeautifulSoup 4.12.0+ (HTML parsing)
- lxml 4.9.0+ (Fast XML/HTML processing)
- Pydantic 2.0.0+ (Data validation)
- html5lib 1.1+ (Standards-compliant parsing)
- loguru 0.7.0+ (Logging)

### Step 3: Verify Installation

Run the example integration to verify everything works:

```bash
python example_integration.py
```

You should see output showing successful DOM analysis of example HTML content.

## 🎯 Basic Usage

### Simple HTML Analysis

```python
from dom_parser import DOMParser

# Initialize the parser
parser = DOMParser()

# Sample HTML content
html_content = """
<!DOCTYPE html>
<html>
<head><title>Test Page</title></head>
<body>
    <nav>
        <a href="/">Home</a>
        <a href="/about">About</a>
    </nav>
    <main>
        <h1>Welcome</h1>
        <form action="/search" method="GET">
            <input type="search" name="q" placeholder="Search...">
            <button type="submit">Search</button>
        </form>
    </main>
</body>
</html>
"""

# Analyze the HTML
async def analyze():
    analysis = await parser.parse_page(
        html_source=html_content,
        url="https://example.com"
    )
    
    # Access results
    print(f"Found {len(analysis.interactive_elements)} interactive elements")
    print(f"Found {len(analysis.form_structures)} forms")
    
    # Get clickable elements
    clickable = analysis.get_clickable_elements()
    for element in clickable:
        print(f"Clickable: {element.visible_text} ({element.element_type})")

# Run the analysis
import asyncio
asyncio.run(analyze())
```

### Working with Results

```python
# Analyze the page
analysis = await parser.parse_page(html_content, "https://example.com")

# Access different types of elements
buttons = analysis.get_elements_by_type(ElementType.BUTTON)
links = analysis.get_elements_by_type(ElementType.LINK)
form_fields = analysis.get_form_fields()

# Work with forms
for form in analysis.form_structures:
    print(f"Form action: {form.action}")
    print(f"Form method: {form.method}")
    print(f"Number of fields: {len(form.fields)}")
    
    for field in form.fields:
        print(f"  Field type: {field.form_field_type}")
        print(f"  Field text: {field.visible_text}")
        print(f"  CSS selector: {field.locators['css']}")

# Access semantic content
for block in analysis.semantic_blocks:
    print(f"Content type: {block.semantic_type}")
    print(f"Text: {block.text_content[:100]}...")

# Check page structure
structure = analysis.page_structure
print(f"Layout type: {structure.layout_type}")
print(f"Main content areas: {len(structure.content_sections)}")
```

## 🔧 Configuration

### Basic Configuration

```python
# Configure the parser
config = {
    'enable_cache': True,           # Cache analysis results
    'confidence_threshold': 0.7,    # Minimum confidence for elements
    'include_hidden_elements': False, # Skip hidden elements
    'max_cache_size': 50           # Maximum cached analyses
}

parser = DOMParser(config)
```

### Performance Tuning

```python
# For faster processing of large pages
fast_config = {
    'confidence_threshold': 0.8,    # Higher threshold = fewer elements
    'max_depth': 30,               # Limit DOM traversal depth
    'include_hidden_elements': False,
    'timeout_seconds': 15          # Shorter timeout
}

# For comprehensive analysis
detailed_config = {
    'confidence_threshold': 0.5,    # Lower threshold = more elements
    'include_hidden_elements': True,
    'max_depth': 100,              # Deeper traversal
    'enable_cache': True
}
```

## 🌐 Browser Integration

If you have a browser controller component, you can integrate directly:

```python
from dom_parser import DOMParser
# from browser_controller import BrowserController  # Your browser component

async def analyze_live_page():
    # Initialize components
    parser = DOMParser()
    # browser = BrowserController(config)
    
    # Get page info from browser
    # async with browser:
    #     session = await browser.create_session()
    #     await session.navigate_to("https://example.com")
    #     page_info = await session.get_page_info()
    #     
    #     # Analyze with DOM parser
    #     analysis = await parser.parse_page_from_browser_info(page_info)
    
    # For this example, simulate with direct HTML
    analysis = await parser.parse_page(html_content, "https://example.com")
    
    return analysis
```

## 📊 Understanding Results

### Element Types

The parser classifies elements into several types:

```python
# Interactive elements
ElementType.BUTTON      # <button>, <input type="button">
ElementType.LINK        # <a href="...">
ElementType.INPUT       # <input> fields
ElementType.SELECT      # <select> dropdowns
ElementType.CHECKBOX    # <input type="checkbox">
ElementType.RADIO       # <input type="radio">

# Structural elements
ElementType.FORM        # <form> containers
ElementType.NAVIGATION  # <nav> elements
ElementType.MAIN        # <main> content areas
ElementType.HEADER      # <header> sections
ElementType.FOOTER      # <footer> sections
```

### Interaction Types

Elements are also classified by interaction capabilities:

```python
InteractionType.CLICK        # Clickable elements
InteractionType.TEXT_INPUT   # Text input fields
InteractionType.SELECTION    # Dropdowns, checkboxes
InteractionType.FORM_SUBMIT  # Submit buttons
InteractionType.NAVIGATION   # Navigation links
```

### Form Field Types

Form inputs are specifically classified:

```python
FormFieldType.TEXT      # text inputs
FormFieldType.EMAIL     # email inputs
FormFieldType.PASSWORD  # password inputs
FormFieldType.SEARCH    # search inputs
FormFieldType.SELECT    # dropdown selects
FormFieldType.CHECKBOX  # checkboxes
FormFieldType.RADIO     # radio buttons
FormFieldType.TEXTAREA  # text areas
FormFieldType.FILE      # file uploads
```

## 🎯 Common Use Cases

### Finding Specific Elements

```python
# Find all buttons
buttons = [elem for elem in analysis.interactive_elements 
           if elem.element_type == ElementType.BUTTON]

# Find search boxes
search_boxes = [elem for elem in analysis.interactive_elements 
                if elem.form_field_type == FormFieldType.SEARCH]

# Find submit buttons
submit_buttons = [elem for elem in analysis.interactive_elements 
                  if elem.interaction_type == InteractionType.FORM_SUBMIT]

# Find navigation links
nav_links = analysis.get_navigation_elements()
```

### Working with Locators

Each interactive element comes with multiple locator strategies:

```python
for element in analysis.interactive_elements:
    print(f"Element: {element.visible_text}")
    print(f"  CSS: {element.locators.get('css', 'N/A')}")
    print(f"  XPath: {element.locators.get('xpath', 'N/A')}")
    print(f"  ID: {element.locators.get('id', 'N/A')}")
    print(f"  Class: {element.locators.get('class', 'N/A')}")
```

### Form Processing

```python
# Process all forms on the page
for form in analysis.form_structures:
    print(f"\nForm: {form.action}")
    
    # Required fields
    required_fields = [f for f in form.fields 
                      if f.attributes.get('required') == 'true']
    print(f"Required fields: {len(required_fields)}")
    
    # Input types
    field_types = [f.form_field_type for f in form.fields]
    print(f"Field types: {set(field_types)}")
    
    # Submit buttons
    print(f"Submit buttons: {len(form.submit_buttons)}")
```

### Content Analysis

```python
# Analyze page content structure
for block in analysis.semantic_blocks:
    if block.semantic_type == SemanticType.HEADING:
        print(f"Heading (level {block.heading_level}): {block.text_content}")
    elif block.semantic_type == SemanticType.NAVIGATION:
        print(f"Navigation: {len(block.elements)} items")
    elif block.semantic_type == SemanticType.MAIN_CONTENT:
        print(f"Main content: {len(block.text_content)} characters")
```

## 🚫 Common Pitfalls

### 1. Async/Await Usage
Always use `await` with parser methods:

```python
# ❌ Wrong
analysis = parser.parse_page(html_content)

# ✅ Correct
analysis = await parser.parse_page(html_content)
```

### 2. Element Visibility
Check element visibility before interaction:

```python
# Filter for visible elements only
visible_elements = [elem for elem in analysis.interactive_elements 
                   if elem.is_visible and elem.is_enabled]
```

### 3. Confidence Scores
Consider confidence scores for reliability:

```python
# Use high-confidence elements only
reliable_elements = [elem for elem in analysis.interactive_elements 
                    if elem.confidence_score > 0.8]
```

## ✅ Next Steps

1. **Explore the [Configuration Guide](configuration.md)** - Learn about advanced configuration options
2. **Review the [API Reference](api-reference.md)** - Detailed documentation of all classes and methods
3. **Check the [Integration Guide](integration.md)** - Learn how to integrate with browser controllers
4. **Try the [Examples](examples.md)** - More practical examples and use cases

## 🆘 Need Help?

- Check the [Troubleshooting Guide](troubleshooting.md) for common issues
- Review the [API Reference](api-reference.md) for detailed method documentation
- Run `python example_integration.py` to see a working example
- Examine the example code in the `example_integration.py` file

Happy parsing! 🚀