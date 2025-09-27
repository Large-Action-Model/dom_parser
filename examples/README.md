# DOM Parser Examples

This directory contains example files demonstrating how to use the DOM Parser library to analyze HTML documents.

## Sample HTML Files

The `samples/` directory contains three sample HTML files for testing:

### 1. dom_sample_1.html
- **Content**: Moby-Dick literary text excerpt
- **Complexity**: Basic
- **Features**: Simple structure with h1, div, and p elements
- **Use case**: Basic DOM parsing and text extraction

### 2. dom_sample_2.html ⭐ (Selected for examples)
- **Content**: Example Domain page
- **Complexity**: Moderate
- **Features**: 
  - Well-structured HTML5 document
  - CSS styling and responsive design
  - Navigation links and semantic elements
  - Meta tags and proper document structure
- **Use case**: Comprehensive DOM analysis demonstration

### 3. dom_sample_3.html
- **Content**: Google homepage (complex)
- **Complexity**: Advanced
- **Features**: 
  - Extensive JavaScript and CSS
  - Dynamic forms and search functionality
  - Complex navigation and interactive elements
  - Advanced web technologies
- **Use case**: Testing with real-world complex websites

## Example Scripts

### simple_example.py ✅ (Working)
A straightforward example demonstrating basic DOM parsing functionality:

```bash
cd examples
python simple_example.py
```

**Features demonstrated:**
- Loading HTML from file using the correct API
- DOM parsing with `parse_page()` method
- Interactive element analysis and distribution
- Document information extraction (title, processing time)
- Semantic blocks and navigation structure

### working_comprehensive_example.py ✅ (Working)
A complete working example showcasing all DOM analysis capabilities:

```bash
cd examples  
python working_comprehensive_example.py
```

**Features demonstrated:**
- Complete DOM analysis using the actual API
- Interactive element classification and interaction types  
- Page structure analysis (layout, sections, complexity)
- Form structure detection and field analysis
- Semantic block identification and content extraction
- Navigation structure and accessibility analysis
- Performance hints and quality metrics
- Element relationships mapping

### dom_analysis_example.py ✅ (Working - Updated API)
A comprehensive analysis example now updated to work with the current API:

```bash
cd examples
python dom_analysis_example.py
```

**Features demonstrated:**
- Complete document structure analysis
- Element classification by type and functionality
- Accessibility analysis and compliance checking
- Link and navigation analysis
- Form detection and analysis  
- CSS selector and XPath display (using existing locators)
- Semantic content extraction from analysis results
- Performance metrics and complexity assessment

## Running the Examples

### Prerequisites
1. Ensure the DOM Parser package is properly installed:
   ```bash
   # From the project root directory
   pip install -e .
   ```

2. Or make sure the src directory is in your Python path.

### Basic Usage

1. **Simple Analysis:**
   ```bash
   cd examples
   python simple_example.py
   ```

2. **Comprehensive Analysis:**
   ```bash
   cd examples
   python dom_analysis_example.py
   ```

### Expected Output

The examples will analyze `dom_sample_2.html` and provide detailed information about:

- Document metadata and structure
- Element distribution and hierarchy  
- Links and navigation elements
- Accessibility features
- Form elements and controls
- Performance metrics
- CSS selectors and XPath expressions

## Sample Analysis Results

When you run the examples with dom_sample_2.html, you can expect to see:

```
Document Title: Example Domain
Total Elements: ~15-20 elements
Element Types: html, head, title, meta, style, body, div, h1, p, a
Links Found: 1 external link to iana.org
Accessibility: Basic structure with proper headings
```

## Customization

You can easily modify the examples to:

1. **Use different HTML files:**
   ```python
   # Change the sample file path
   sample_path = Path(__file__).parent / "samples" / "dom_sample_1.html"
   ```

2. **Add custom analysis:**
   ```python
   # Add your own analysis functions
   async def custom_analysis(dom_tree):
       # Your analysis code here
       pass
   ```

3. **Filter specific elements:**
   ```python
   # Find elements with specific attributes
   specific_elements = [
       e for e in dom_tree.elements 
       if e.attributes.get('class') == 'target-class'
   ]
   ```

## Integration with Your Code

To use the DOM Parser in your own projects:

```python
import asyncio
from dom_parser import DOMParser

async def analyze_html(html_content):
    parser = DOMParser()
    dom_tree = await parser.parse_html(html_content)
    
    # Your analysis code here
    print(f"Found {len(dom_tree.elements)} elements")
    
    return dom_tree

# Usage
html = "<html><body><h1>Hello World</h1></body></html>"
result = asyncio.run(analyze_html(html))
```

## Troubleshooting

### Import Errors
If you encounter import errors:

1. **Install the package:**
   ```bash
   pip install -e .
   ```

2. **Check Python path:**
   ```python
   import sys
   sys.path.insert(0, '/path/to/dom_parser/src')
   ```

3. **Verify package structure:**
   ```bash
   ls dom_parser/
   # Should show __init__.py and other modules
   ```

### File Not Found Errors
Ensure you're running the examples from the correct directory:

```bash
# Should be in the examples directory
pwd  # Should show .../dom_parser/examples
ls   # Should show simple_example.py, dom_analysis_example.py, samples/
```

## Next Steps

After running these examples, you can:

1. Explore the full DOM Parser API documentation
2. Create custom analyzers for specific use cases
3. Integrate DOM parsing into web scraping projects
4. Build automated accessibility testing tools
5. Develop content extraction and analysis pipelines

For more information, see the main project documentation and API reference.