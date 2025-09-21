# DOM Parser & Analyzer

> **Intelligent HTML analysis component for Large Action Model (LAM) web automation systems**

A powerful, production-ready DOM parser that transforms raw HTML into structured, analyzable data for AI-driven web automation. Built for seamless integration with browser controllers and LAM systems.

## 🌟 Features

### Core Capabilities
- **🔍 Multi-Parser HTML Processing** - BeautifulSoup + lxml + html5lib with intelligent fallbacks
- **🎯 Interactive Element Detection** - Automatic classification of clickable, form, and navigation elements
- **🧠 Semantic Content Analysis** - Intelligent extraction of headings, paragraphs, navigation, and content blocks
- **📋 Advanced Form Analysis** - Comprehensive form structure detection with field type classification
- **♿ Accessibility Analysis** - ARIA roles, labels, and accessibility compliance checking
- **🏗️ Page Structure Mapping** - Layout detection and hierarchical content organization
- **🔗 Robust Element Locators** - CSS selectors and XPath generation for reliable element targeting

### Integration Features
- **🤖 Browser Controller Ready** - Direct integration with existing browser automation systems
- **⚡ Async/Await Support** - Non-blocking operations for high-performance automation
- **💾 Smart Caching** - Configurable caching to optimize repeated analysis
- **📊 Performance Insights** - Page complexity analysis and optimization recommendations
- **🔄 Similarity Detection** - Find similar elements for pattern-based automation

## 🚀 Quick Start

### Installation

1. **Clone or copy the DOM Parser component:**
```bash
cd your-lam-project
# Copy the dom_parser directory to your project
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Basic usage:**
```python
from dom_parser import DOMParser

# Initialize parser
parser = DOMParser()

# Analyze HTML content
analysis = await parser.parse_page(
    html_source="<html>...</html>",
    url="https://example.com"
)

# Access structured results
clickable_elements = analysis.get_clickable_elements()
forms = analysis.form_structures
semantic_blocks = analysis.semantic_blocks
```

### Browser Controller Integration

```python
from dom_parser import DOMParser
from browser_controller import BrowserController

# Initialize components
browser = BrowserController(config)
parser = DOMParser()

async with browser:
    session = await browser.create_session()
    await session.navigate_to("https://example.com")
    
    # Get page info from browser
    page_info = await session.get_page_info()
    
    # Analyze with DOM parser
    analysis = await parser.parse_page_from_browser_info(page_info)
    
    # Use results for automation
    for element in analysis.get_clickable_elements():
        print(f"Found clickable: {element.visible_text}")
```

## 📁 Project Structure

```
dom_parser/
├── __init__.py                     # Main exports
├── dom_parser.py                   # Core orchestration class
├── html_analyzer.py               # HTML parsing & cleaning
├── element_classifier.py          # Element type detection
├── semantic_extractor.py          # Content structure analysis
├── form_analyzer.py              # Form structure analysis
├── accessibility_analyzer.py      # Accessibility features
├── structure_mapper.py            # Page layout analysis
├── data_types/
│   ├── __init__.py
│   ├── dom_data_types.py          # Core data structures
│   └── element_data_types.py      # Element enums & types
├── utils/
│   ├── __init__.py
│   ├── css_selector_generator.py  # CSS selector creation
│   └── xpath_generator.py         # XPath expression generation
├── docs/                          # Documentation
├── example_integration.py         # Usage examples
└── requirements.txt               # Dependencies
```

## 🎯 Key Components

### DOMParser Class
The main orchestration class that coordinates all analysis components.

```python
parser = DOMParser({
    'enable_cache': True,
    'include_hidden_elements': False,
    'confidence_threshold': 0.7,
    'max_cache_size': 100
})
```

### Data Types
Comprehensive data structures for all analysis results:

- **`DOMAnalysisResult`** - Complete analysis output
- **`InteractiveElement`** - Clickable elements with locators
- **`FormStructure`** - Form analysis with field classification
- **`SemanticBlock`** - Content blocks with semantic meaning
- **`PageStructure`** - Layout and hierarchical organization
- **`AccessibilityInfo`** - ARIA and accessibility data

### Element Classification
Intelligent element type detection:

```python
# Element types
ElementType.BUTTON, ElementType.LINK, ElementType.FORM
ElementType.INPUT, ElementType.NAVIGATION, ElementType.MAIN

# Interaction types
InteractionType.CLICK, InteractionType.FORM_SUBMIT
InteractionType.TEXT_INPUT, InteractionType.SELECTION
```

## 🔧 Configuration

### Parser Configuration
```python
config = {
    'enable_cache': True,              # Cache analysis results
    'max_cache_size': 100,            # Maximum cached analyses
    'include_hidden_elements': False,  # Include display:none elements
    'confidence_threshold': 0.7,       # Minimum confidence for classification
    'max_depth': 50,                   # Maximum DOM traversal depth
    'timeout_seconds': 30,             # Analysis timeout
}

parser = DOMParser(config)
```

### HTML Parser Backends
- **lxml** (primary) - Fast C-based parser
- **BeautifulSoup** - Robust Python parser
- **html5lib** - Standards-compliant fallback

## 📊 Analysis Results

### Interactive Elements
```python
for element in analysis.interactive_elements:
    print(f"Type: {element.element_type}")
    print(f"Text: {element.visible_text}")
    print(f"CSS: {element.locators['css']}")
    print(f"XPath: {element.locators['xpath']}")
    print(f"Confidence: {element.confidence_score}")
```

### Form Analysis
```python
for form in analysis.form_structures:
    print(f"Form type: {form.form_type}")
    print(f"Action: {form.action}")
    print(f"Fields: {len(form.fields)}")
    
    for field in form.fields:
        print(f"  {field.form_field_type}: {field.visible_text}")
```

### Semantic Blocks
```python
for block in analysis.semantic_blocks:
    print(f"Type: {block.semantic_type}")
    print(f"Content: {block.text_content[:100]}...")
    print(f"Elements: {len(block.elements)}")
```

## 🧪 Testing

Run the example integration to test functionality:

```bash
# Activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run example
python example_integration.py
```

## 🤝 Integration Examples

### LAM System Integration
```python
class WebAutomationAgent:
    def __init__(self):
        self.browser = BrowserController()
        self.dom_parser = DOMParser()
    
    async def analyze_page(self, url: str):
        async with self.browser:
            session = await self.browser.create_session()
            await session.navigate_to(url)
            
            page_info = await session.get_page_info()
            analysis = await self.dom_parser.parse_page_from_browser_info(page_info)
            
            return self._extract_actionable_elements(analysis)
    
    def _extract_actionable_elements(self, analysis):
        """Extract elements suitable for AI decision-making"""
        return {
            'buttons': [elem for elem in analysis.get_clickable_elements() 
                       if elem.element_type == ElementType.BUTTON],
            'forms': analysis.form_structures,
            'navigation': analysis.navigation_structure.primary_navigation,
            'content': analysis.semantic_blocks
        }
```

### Custom Element Detection
```python
# Find specific elements
search_boxes = [elem for elem in analysis.interactive_elements 
                if elem.form_field_type == FormFieldType.SEARCH]

submit_buttons = [elem for elem in analysis.interactive_elements 
                  if elem.interaction_type == InteractionType.FORM_SUBMIT]

# Use similarity detection
similar_elements = await parser.find_similar_elements(target_element_id)
```

## 📈 Performance

- **Fast Analysis**: ~50-100ms for typical web pages
- **Memory Efficient**: Smart caching with configurable limits
- **Scalable**: Async processing for concurrent analysis
- **Robust**: Multiple parser fallbacks for reliability

## 🛠️ Dependencies

- **BeautifulSoup 4.12.0+** - HTML parsing and DOM manipulation
- **lxml 4.9.0+** - Fast XML/HTML processing backend
- **Pydantic 2.0.0+** - Data validation and type safety
- **html5lib 1.1+** - Standards-compliant HTML parsing
- **loguru 0.7.0+** - Structured logging

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[Getting Started](docs/getting-started.md)** - Installation and basic usage
- **[API Reference](docs/api-reference.md)** - Complete API documentation
- **[Configuration](docs/configuration.md)** - Configuration options and customization
- **[Integration Guide](docs/integration.md)** - Browser controller and LAM integration
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions

## 🤝 Contributing

This DOM Parser was built as part of a Large Action Model web automation system. For questions, improvements, or integration support, please refer to the documentation or create an issue.

## 📄 License

This project is part of a LAM automation system. Please refer to your project's license terms.

---

**Built for intelligent web automation** 🤖 | **Powered by advanced DOM analysis** 🔍 | **Ready for LAM integration** 🚀