# Troubleshooting Guide

Common issues, solutions, and debugging tips for the DOM Parser & Analyzer.

## 🚨 Common Issues

### Import Errors

#### Problem: ModuleNotFoundError for DOM Parser modules

```
ModuleNotFoundError: No module named 'dom_parser'
```

**Solution:**
```python
# Ensure you're importing from the correct path
import sys
sys.path.append('/path/to/your/project')

from dom_parser import DOMParser
```

**Alternative Solution:**
```python
# Use absolute imports
from dom_parser.dom_parser import DOMParser
from dom_parser.data_types import ElementType, InteractionType
```

#### Problem: BeautifulSoup import errors

```
ImportError: bs4 module not found
```

**Solution:**
```bash
# Install required dependencies
pip install beautifulsoup4 lxml html5lib

# Verify installation
python -c "from bs4 import BeautifulSoup; print('BeautifulSoup installed successfully')"
```

#### Problem: lxml parser not available

```
FeatureNotFound: Couldn't find a tree builder with the features you requested: lxml
```

**Solution:**
```bash
# Install lxml
pip install lxml

# On Ubuntu/Debian
sudo apt-get install libxml2-dev libxslt-dev

# On macOS
brew install libxml2 libxslt

# On Windows
pip install lxml
```

### Configuration Issues

#### Problem: Invalid configuration values

```
ValueError: confidence_threshold must be between 0.0 and 1.0
```

**Solution:**
```python
# Valid configuration
config = {
    'confidence_threshold': 0.7,  # Must be 0.0 to 1.0
    'max_depth': 50,             # Must be positive integer
    'timeout_seconds': 30,       # Must be positive integer
    'max_cache_size': 100        # Must be positive integer or -1
}

parser = DOMParser(config)
```

#### Problem: Memory issues with large cache

```
MemoryError: Unable to allocate memory
```

**Solution:**
```python
# Reduce cache size or disable caching
config = {
    'enable_cache': False,      # Disable caching
    # OR
    'max_cache_size': 10       # Smaller cache
}
```

### Analysis Issues

#### Problem: No elements found in analysis

```python
analysis = await parser.parse_page(html_source)
print(len(analysis.interactive_elements))  # Returns 0
```

**Debugging Steps:**

1. **Check HTML content:**
```python
print(f"HTML length: {len(html_source)}")
print(f"HTML preview: {html_source[:500]}")
```

2. **Lower confidence threshold:**
```python
config = {'confidence_threshold': 0.3}  # Lower threshold
parser = DOMParser(config)
```

3. **Include hidden elements:**
```python
config = {'include_hidden_elements': True}
parser = DOMParser(config)
```

4. **Check for parsing errors:**
```python
try:
    analysis = await parser.parse_page(html_source)
except Exception as e:
    print(f"Parsing error: {e}")
```

#### Problem: Low confidence scores

```python
# Elements found but with low confidence
for element in analysis.interactive_elements:
    print(f"Confidence: {element.confidence_score}")  # < 0.5
```

**Solutions:**

1. **Adjust threshold:**
```python
config = {'confidence_threshold': 0.4}  # Lower threshold
```

2. **Check HTML quality:**
```python
# Look for missing attributes, poor structure
print("Elements without IDs:", [e for e in analysis.interactive_elements if not e.attributes.get('id')])
print("Elements without classes:", [e for e in analysis.interactive_elements if not e.attributes.get('class')])
```

3. **Use custom classifiers:**
```python
config = {
    'custom_classifiers': {
        'button_patterns': [r'btn.*', r'button.*', r'click.*'],
        'form_patterns': [r'form.*', r'input.*']
    }
}
```

### Performance Issues

#### Problem: Slow analysis

```python
# Analysis takes > 30 seconds
analysis = await parser.parse_page(large_html_source)
```

**Solutions:**

1. **Reduce analysis depth:**
```python
config = {'max_depth': 25}  # Shallow traversal
```

2. **Set timeout:**
```python
config = {'timeout_seconds': 15}  # Faster timeout
```

3. **Use faster parser:**
```python
config = {'parser_preference': ['lxml']}  # Fastest parser only
```

4. **Filter large HTML:**
```python
# Pre-filter HTML content
if len(html_source) > 1000000:  # 1MB limit
    html_source = html_source[:1000000]
```

#### Problem: High memory usage

```python
# Memory usage grows with each analysis
```

**Solutions:**

1. **Disable caching:**
```python
config = {'enable_cache': False}
```

2. **Limit cache size:**
```python
config = {'max_cache_size': 25}
```

3. **Clear cache periodically:**
```python
parser._clear_cache()  # Clear internal cache
```

4. **Process in batches:**
```python
# Process pages in smaller batches
for batch in page_batches:
    results = []
    for page in batch:
        analysis = await parser.parse_page(page.html)
        results.append(analysis)
    
    # Process results
    process_batch_results(results)
    
    # Clear memory
    del results
    gc.collect()
```

## 🔧 Debugging Techniques

### Enable Debug Logging

```python
import logging
from loguru import logger

# Enable debug logging
logger.add("dom_parser_debug.log", level="DEBUG")

# Or configure standard logging
logging.basicConfig(level=logging.DEBUG)
```

### Analyze HTML Structure

```python
def debug_html_structure(html_source):
    """Debug HTML structure issues."""
    
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html_source, 'lxml')
    
    print(f"Total elements: {len(soup.find_all())}")
    print(f"Interactive elements: {len(soup.find_all(['button', 'input', 'a', 'select', 'textarea']))}")
    print(f"Forms: {len(soup.find_all('form'))}")
    print(f"Links: {len(soup.find_all('a'))}")
    print(f"Buttons: {len(soup.find_all('button'))}")
    print(f"Inputs: {len(soup.find_all('input'))}")
    
    # Check for common issues
    elements_without_text = soup.find_all(lambda tag: tag.name in ['button', 'a'] and not tag.get_text(strip=True))
    print(f"Elements without text: {len(elements_without_text)}")
    
    forms_without_action = soup.find_all('form', action=lambda x: not x)
    print(f"Forms without action: {len(forms_without_action)}")

# Usage
debug_html_structure(html_source)
```

### Test with Simple HTML

```python
async def test_with_simple_html():
    """Test parser with known good HTML."""
    
    simple_html = """
    <html>
    <body>
        <button id="test-btn">Test Button</button>
        <a href="/test" id="test-link">Test Link</a>
        <form action="/submit" method="POST">
            <input type="text" name="username" placeholder="Username">
            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    """
    
    parser = DOMParser()
    analysis = await parser.parse_page(simple_html, "https://test.example")
    
    print(f"Elements found: {len(analysis.interactive_elements)}")
    for element in analysis.interactive_elements:
        print(f"  {element.element_type}: {element.visible_text} (confidence: {element.confidence_score})")
    
    return analysis

# Run test
test_analysis = await test_with_simple_html()
```

### Validate Analysis Results

```python
def validate_analysis(analysis):
    """Validate analysis results for consistency."""
    
    issues = []
    
    # Check for elements without locators
    for element in analysis.interactive_elements:
        if not element.locators:
            issues.append(f"Element {element.element_id} has no locators")
        
        if not element.locators.get('css'):
            issues.append(f"Element {element.element_id} has no CSS selector")
    
    # Check form consistency
    for form in analysis.form_structures:
        for field in form.fields:
            if field.element_id not in [e.element_id for e in analysis.interactive_elements]:
                issues.append(f"Form field {field.element_id} not found in interactive elements")
    
    # Check confidence scores
    low_confidence = [e for e in analysis.interactive_elements if e.confidence_score < 0.3]
    if low_confidence:
        issues.append(f"{len(low_confidence)} elements with very low confidence")
    
    return issues

# Usage
issues = validate_analysis(analysis)
if issues:
    print("Analysis issues found:")
    for issue in issues:
        print(f"  - {issue}")
```

## 🐛 Error Handling

### Graceful Error Handling

```python
async def robust_analysis(parser, html_source, url):
    """Perform analysis with comprehensive error handling."""
    
    try:
        analysis = await parser.parse_page(html_source, url)
        return analysis
        
    except TimeoutError:
        logger.warning(f"Analysis timeout for {url}")
        # Try with reduced configuration
        quick_config = {
            'timeout_seconds': 10,
            'max_depth': 20,
            'confidence_threshold': 0.8
        }
        parser = DOMParser(quick_config)
        return await parser.parse_page(html_source, url)
        
    except MemoryError:
        logger.warning(f"Memory error for {url}")
        # Try with memory-optimized config
        memory_config = {
            'enable_cache': False,
            'max_depth': 15,
            'include_hidden_elements': False
        }
        parser = DOMParser(memory_config)
        return await parser.parse_page(html_source[:500000], url)  # Limit HTML size
        
    except Exception as e:
        logger.error(f"Unexpected error analyzing {url}: {e}")
        # Return minimal analysis
        return create_empty_analysis(url)

def create_empty_analysis(url):
    """Create empty analysis result for failed parsing."""
    from dom_parser.data_types import DOMAnalysisResult
    
    return DOMAnalysisResult(
        source_url=url,
        source_title="",
        analysis_timestamp=time.time(),
        processing_time=0.0,
        interactive_elements=[],
        semantic_blocks=[],
        form_structures=[],
        page_structure=None,
        navigation_structure=None,
        accessibility_info=None,
        confidence_scores={},
        performance_hints={"error": "Analysis failed"}
    )
```

### Retry Logic

```python
import asyncio
from functools import wraps

def retry_analysis(max_retries=3, delay=1.0):
    """Decorator to retry analysis on failure."""
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logger.warning(f"Analysis attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                        await asyncio.sleep(delay)
                    else:
                        logger.error(f"Analysis failed after {max_retries} attempts: {e}")
            
            raise last_exception
        
        return wrapper
    return decorator

# Usage
@retry_analysis(max_retries=3, delay=2.0)
async def analyze_with_retry(parser, html_source, url):
    return await parser.parse_page(html_source, url)
```

## 🧪 Testing and Validation

### Unit Testing

```python
import unittest
from unittest.mock import Mock, patch

class TestDOMParser(unittest.TestCase):
    
    def setUp(self):
        self.parser = DOMParser()
        self.sample_html = """
        <html>
        <body>
            <button id="btn1">Click me</button>
            <form action="/submit">
                <input type="text" name="field1">
                <input type="submit" value="Submit">
            </form>
        </body>
        </html>
        """
    
    async def test_basic_parsing(self):
        """Test basic HTML parsing functionality."""
        analysis = await self.parser.parse_page(self.sample_html, "https://test.com")
        
        self.assertGreater(len(analysis.interactive_elements), 0)
        self.assertEqual(len(analysis.form_structures), 1)
        
        button_elements = [e for e in analysis.interactive_elements if e.element_type == ElementType.BUTTON]
        self.assertEqual(len(button_elements), 2)  # button + submit input
    
    async def test_empty_html(self):
        """Test handling of empty HTML."""
        analysis = await self.parser.parse_page("", "https://test.com")
        
        self.assertEqual(len(analysis.interactive_elements), 0)
        self.assertEqual(len(analysis.form_structures), 0)
    
    async def test_malformed_html(self):
        """Test handling of malformed HTML."""
        malformed_html = "<html><body><button>Unclosed button<div>Unclosed div</body></html>"
        
        # Should not raise exception
        analysis = await self.parser.parse_page(malformed_html, "https://test.com")
        self.assertIsNotNone(analysis)
    
    def test_configuration_validation(self):
        """Test configuration validation."""
        
        with self.assertRaises(ValueError):
            DOMParser({'confidence_threshold': 1.5})  # Invalid threshold
        
        with self.assertRaises(ValueError):
            DOMParser({'max_depth': -1})  # Invalid depth
        
        # Valid configuration should not raise
        parser = DOMParser({'confidence_threshold': 0.7, 'max_depth': 50})
        self.assertIsNotNone(parser)

# Run tests
if __name__ == '__main__':
    unittest.main()
```

### Integration Testing

```python
async def test_browser_integration():
    """Test integration with browser controller."""
    
    # Mock browser controller
    class MockBrowserController:
        async def __aenter__(self):
            return self
        
        async def __aexit__(self, *args):
            pass
        
        async def create_session(self):
            return MockSession()
    
    class MockSession:
        async def navigate_to(self, url):
            pass
        
        async def get_page_info(self):
            return Mock(
                url="https://test.com",
                title="Test Page",
                source="""<html><body><button>Test</button></body></html>""",
                timestamp=time.time(),
                metadata={}
            )
    
    # Test integration
    browser = MockBrowserController()
    parser = DOMParser()
    
    async with browser:
        session = await browser.create_session()
        await session.navigate_to("https://test.com")
        page_info = await session.get_page_info()
        
        analysis = await parser.parse_page_from_browser_info(page_info)
        
        assert len(analysis.interactive_elements) > 0
        assert analysis.source_url == "https://test.com"
        assert analysis.source_title == "Test Page"

# Run integration test
await test_browser_integration()
```

## 🔍 Performance Profiling

### Memory Profiling

```python
import tracemalloc
import gc

async def profile_memory_usage():
    """Profile memory usage during analysis."""
    
    tracemalloc.start()
    
    parser = DOMParser()
    
    # Baseline memory
    snapshot1 = tracemalloc.take_snapshot()
    
    # Perform analysis
    analysis = await parser.parse_page(large_html_source, "https://test.com")
    
    # Memory after analysis
    snapshot2 = tracemalloc.take_snapshot()
    
    # Calculate difference
    top_stats = snapshot2.compare_to(snapshot1, 'lineno')
    
    print("Memory usage increase:")
    for stat in top_stats[:10]:
        print(stat)
    
    # Force garbage collection
    gc.collect()
    
    # Memory after cleanup
    snapshot3 = tracemalloc.take_snapshot()
    cleanup_stats = snapshot3.compare_to(snapshot2, 'lineno')
    
    print("\nMemory freed after GC:")
    for stat in cleanup_stats[:5]:
        print(stat)
```

### Time Profiling

```python
import cProfile
import pstats

async def profile_analysis_time():
    """Profile analysis execution time."""
    
    def sync_analysis():
        """Wrapper for profiling async function."""
        import asyncio
        parser = DOMParser()
        return asyncio.run(parser.parse_page(html_source, "https://test.com"))
    
    # Profile the analysis
    profiler = cProfile.Profile()
    profiler.enable()
    
    result = sync_analysis()
    
    profiler.disable()
    
    # Print stats
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions
    
    return result
```

## 📞 Getting Help

### Enable Detailed Logging

```python
import logging
from loguru import logger

# Configure loguru for detailed debugging
logger.add(
    "dom_parser_debug.log",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
    rotation="10 MB"
)

# Log analysis details
parser = DOMParser({
    'debug_mode': True,  # If supported
    'log_element_details': True
})
```

### Create Minimal Reproduction

```python
async def create_minimal_repro():
    """Create minimal reproduction for bug reports."""
    
    # Minimal HTML that demonstrates the issue
    minimal_html = """
    <!DOCTYPE html>
    <html>
    <head><title>Bug Reproduction</title></head>
    <body>
        <!-- Include only elements that demonstrate the issue -->
        <button id="problem-button">Problem Button</button>
    </body>
    </html>
    """
    
    # Minimal configuration
    config = {
        'confidence_threshold': 0.7,
        'enable_cache': False
    }
    
    parser = DOMParser(config)
    
    try:
        analysis = await parser.parse_page(minimal_html, "https://repro.example")
        
        # Show the issue
        print(f"Expected: Button should be found")
        print(f"Actual: Found {len(analysis.interactive_elements)} elements")
        
        for element in analysis.interactive_elements:
            print(f"  - {element.element_type}: {element.visible_text}")
            
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()

# Run reproduction
await create_minimal_repro()
```

### System Information

```python
def collect_system_info():
    """Collect system information for bug reports."""
    
    import sys
    import platform
    
    try:
        from bs4 import BeautifulSoup
        bs4_version = BeautifulSoup.__version__
    except ImportError:
        bs4_version = "Not installed"
    
    try:
        import lxml
        lxml_version = lxml.__version__
    except ImportError:
        lxml_version = "Not installed"
    
    info = {
        'python_version': sys.version,
        'platform': platform.platform(),
        'beautifulsoup_version': bs4_version,
        'lxml_version': lxml_version,
        'memory_available': get_available_memory(),
        'dom_parser_version': get_dom_parser_version()
    }
    
    print("System Information:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    return info

def get_available_memory():
    """Get available system memory."""
    try:
        import psutil
        return f"{psutil.virtual_memory().available / (1024**3):.1f} GB"
    except ImportError:
        return "Unknown (psutil not installed)"

def get_dom_parser_version():
    """Get DOM Parser version if available."""
    try:
        from dom_parser import __version__
        return __version__
    except ImportError:
        return "Development version"
```

---

**Need more help?**
- Check the [API Reference](api-reference.md) for detailed method documentation
- Review [Configuration Guide](configuration.md) for advanced settings
- See [Integration Guide](integration.md) for integration patterns
- Run the example integration: `python example_integration.py`