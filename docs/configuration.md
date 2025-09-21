# Configuration Guide

Complete guide to configuring the DOM Parser & Analyzer for optimal performance and functionality.

## 🔧 Configuration Overview

The DOM Parser accepts a configuration dictionary that controls various aspects of HTML analysis, performance, and behavior.

```python
from dom_parser import DOMParser

config = {
    'enable_cache': True,
    'max_cache_size': 100,
    'confidence_threshold': 0.7,
    'include_hidden_elements': False,
    'max_depth': 50,
    'timeout_seconds': 30
}

parser = DOMParser(config)
```

## 📋 Configuration Options

### Core Settings

#### `enable_cache` (bool)
**Default:** `True`

Enables caching of analysis results to improve performance for repeated analysis.

```python
# Enable caching (recommended)
config = {'enable_cache': True}

# Disable caching (for memory-constrained environments)
config = {'enable_cache': False}
```

**When to use:**
- ✅ Enable for production environments
- ✅ Enable when analyzing similar pages repeatedly
- ❌ Disable for one-off analysis or memory-constrained systems

#### `max_cache_size` (int)
**Default:** `100`

Maximum number of analysis results to cache in memory.

```python
# Small cache for limited memory
config = {'max_cache_size': 25}

# Large cache for high-volume processing
config = {'max_cache_size': 500}

# Unlimited cache (use with caution)
config = {'max_cache_size': -1}
```

**Guidelines:**
- Each cached result uses ~1-5MB of memory
- Monitor memory usage with large cache sizes
- Consider page similarity when sizing cache

#### `confidence_threshold` (float)
**Default:** `0.7`

Minimum confidence score for element classification (0.0 to 1.0).

```python
# High precision (fewer elements, higher quality)
config = {'confidence_threshold': 0.9}

# Balanced (default)
config = {'confidence_threshold': 0.7}

# High recall (more elements, some false positives)
config = {'confidence_threshold': 0.5}

# Include all detected elements
config = {'confidence_threshold': 0.0}
```

**Impact:**
- Higher values = fewer, more reliable elements
- Lower values = more elements, potentially lower quality
- Adjust based on your accuracy vs completeness needs

### Element Detection

#### `include_hidden_elements` (bool)
**Default:** `False`

Whether to include elements that are hidden via CSS (display: none, visibility: hidden).

```python
# Skip hidden elements (faster, typical use case)
config = {'include_hidden_elements': False}

# Include hidden elements (comprehensive analysis)
config = {'include_hidden_elements': True}
```

**Consider including hidden elements when:**
- Analyzing single-page applications (SPAs)
- Elements might be shown dynamically
- Comprehensive security analysis needed

**Skip hidden elements when:**
- Focused on user-visible interactions
- Performance is critical
- Working with static content

#### `max_depth` (int)
**Default:** `50`

Maximum depth for DOM tree traversal.

```python
# Shallow traversal (faster, good for simple pages)
config = {'max_depth': 20}

# Default depth
config = {'max_depth': 50}

# Deep traversal (slower, comprehensive for complex pages)
config = {'max_depth': 100}

# Unlimited depth (use with caution)
config = {'max_depth': -1}
```

**Guidelines:**
- Most web pages work well with default (50)
- Increase for complex, deeply nested pages
- Decrease for performance on simple pages
- Monitor processing time with high values

### Performance Settings

#### `timeout_seconds` (int)
**Default:** `30`

Maximum time allowed for complete analysis.

```python
# Quick timeout for fast environments
config = {'timeout_seconds': 10}

# Extended timeout for complex pages
config = {'timeout_seconds': 60}

# No timeout (not recommended for production)
config = {'timeout_seconds': -1}
```

**Recommendations:**
- Use shorter timeouts in real-time systems
- Increase for batch processing of complex pages
- Always set a reasonable limit in production

#### `parser_preference` (list)
**Default:** `['lxml', 'html.parser', 'html5lib']`

Order of HTML parser preference.

```python
# Prefer speed (lxml first)
config = {'parser_preference': ['lxml', 'html.parser', 'html5lib']}

# Prefer accuracy (html5lib first)
config = {'parser_preference': ['html5lib', 'lxml', 'html.parser']}

# Use only specific parser
config = {'parser_preference': ['lxml']}
```

**Parser characteristics:**
- **lxml**: Fastest, good for well-formed HTML
- **html.parser**: Balanced, built-in Python parser
- **html5lib**: Most accurate, slowest

## 🎯 Configuration Profiles

### Development Profile

Optimized for development and testing:

```python
development_config = {
    'enable_cache': False,           # Fresh analysis each time
    'confidence_threshold': 0.6,     # Include more elements for testing
    'include_hidden_elements': True, # Comprehensive analysis
    'timeout_seconds': 60,          # Allow longer processing
    'max_depth': 100,               # Deep analysis
    'debug_mode': True              # Enable detailed logging
}
```

### Production Profile

Optimized for production performance:

```python
production_config = {
    'enable_cache': True,           # Cache for performance
    'max_cache_size': 200,          # Generous cache
    'confidence_threshold': 0.8,    # High-quality elements only
    'include_hidden_elements': False, # Focus on visible elements
    'timeout_seconds': 15,          # Quick timeout
    'max_depth': 50,                # Balanced depth
    'parser_preference': ['lxml']   # Fastest parser
}
```

### High-Accuracy Profile

Optimized for comprehensive analysis:

```python
accuracy_config = {
    'enable_cache': True,
    'confidence_threshold': 0.5,     # Include more elements
    'include_hidden_elements': True, # Comprehensive coverage
    'timeout_seconds': 45,          # Allow thorough analysis
    'max_depth': 80,                # Deep traversal
    'parser_preference': ['html5lib', 'lxml'], # Accuracy first
    'accessibility_analysis': True  # Detailed accessibility
}
```

### Memory-Constrained Profile

Optimized for limited memory environments:

```python
memory_config = {
    'enable_cache': False,          # No caching
    'confidence_threshold': 0.8,    # Fewer elements
    'include_hidden_elements': False,
    'timeout_seconds': 20,
    'max_depth': 30,               # Shallow traversal
    'max_elements': 500,           # Limit total elements
    'parser_preference': ['html.parser'] # Lower memory usage
}
```

## 🔄 Dynamic Configuration

### Runtime Configuration Updates

```python
parser = DOMParser(base_config)

# Update configuration for specific analysis
analysis = await parser.parse_page(
    html_source=html,
    url=url,
    override_config={
        'confidence_threshold': 0.9,  # Temporary higher threshold
        'include_hidden_elements': True
    }
)
```

### Conditional Configuration

```python
def get_config_for_page_type(page_type: str) -> dict:
    """Get configuration based on page type."""
    
    if page_type == 'spa':
        return {
            'include_hidden_elements': True,
            'confidence_threshold': 0.6,
            'max_depth': 80
        }
    elif page_type == 'ecommerce':
        return {
            'confidence_threshold': 0.8,
            'enable_cache': True,
            'timeout_seconds': 30
        }
    elif page_type == 'form':
        return {
            'confidence_threshold': 0.7,
            'form_analysis_enabled': True,
            'accessibility_analysis': True
        }
    else:
        return {}  # Use defaults

# Usage
page_type = detect_page_type(url)
config = get_config_for_page_type(page_type)
parser = DOMParser(config)
```

## 🎛️ Advanced Configuration

### Custom Element Classifiers

```python
config = {
    'custom_classifiers': {
        'button_patterns': [
            r'btn-.*',           # Custom button class patterns
            r'.*-button',
            r'cta-.*'           # Call-to-action patterns
        ],
        'form_patterns': [
            r'form-.*',
            r'.*-form',
            r'search-.*'
        ]
    }
}
```

### Locator Generation Settings

```python
config = {
    'locator_settings': {
        'prefer_id': True,           # Prefer ID selectors
        'prefer_class': False,       # Avoid class selectors
        'use_text_content': True,    # Include text in selectors
        'max_selector_length': 100,  # Limit selector complexity
        'generate_xpath': True,      # Generate XPath expressions
        'xpath_prefer_attributes': ['id', 'name', 'class']
    }
}
```

### Performance Monitoring

```python
config = {
    'performance_monitoring': {
        'enable_timing': True,       # Track processing times
        'enable_memory_tracking': True, # Monitor memory usage
        'log_slow_operations': True, # Log operations > threshold
        'slow_operation_threshold': 5.0 # Seconds
    }
}
```

## 📊 Configuration Validation

The parser validates configuration on initialization:

```python
# Invalid configuration will raise ValueError
try:
    parser = DOMParser({
        'confidence_threshold': 1.5,  # Invalid: > 1.0
        'max_depth': -5,             # Invalid: negative depth
        'timeout_seconds': 0         # Invalid: zero timeout
    })
except ValueError as e:
    print(f"Configuration error: {e}")
```

### Configuration Schema

```python
VALID_CONFIG_SCHEMA = {
    'enable_cache': bool,
    'max_cache_size': int,  # -1 for unlimited, > 0 for limit
    'confidence_threshold': float,  # 0.0 to 1.0
    'include_hidden_elements': bool,
    'max_depth': int,  # -1 for unlimited, > 0 for limit
    'timeout_seconds': int,  # -1 for no timeout, > 0 for limit
    'parser_preference': list,  # List of valid parser names
    'custom_classifiers': dict,  # Custom classification patterns
    'locator_settings': dict,  # Locator generation settings
    'performance_monitoring': dict  # Performance tracking settings
}
```

## 🔍 Configuration Testing

Test your configuration with sample content:

```python
def test_configuration(config: dict, sample_html: str):
    """Test configuration with sample HTML."""
    
    parser = DOMParser(config)
    
    start_time = time.time()
    analysis = await parser.parse_page(sample_html, "https://test.example")
    end_time = time.time()
    
    print(f"Processing time: {end_time - start_time:.2f}s")
    print(f"Elements found: {len(analysis.interactive_elements)}")
    print(f"Average confidence: {sum(e.confidence_score for e in analysis.interactive_elements) / len(analysis.interactive_elements):.2f}")
    
    return analysis

# Test different configurations
configs = [
    {'confidence_threshold': 0.5},
    {'confidence_threshold': 0.7},
    {'confidence_threshold': 0.9}
]

for config in configs:
    print(f"\nTesting config: {config}")
    test_configuration(config, sample_html)
```

## 📝 Configuration Examples

### E-commerce Site Configuration

```python
ecommerce_config = {
    'confidence_threshold': 0.8,     # High precision for product interactions
    'include_hidden_elements': False, # Focus on visible products
    'enable_cache': True,            # Cache product page analyses
    'max_cache_size': 300,           # Large cache for many products
    'timeout_seconds': 20,           # Quick processing for user experience
    'custom_classifiers': {
        'product_buttons': [r'add-to-cart.*', r'buy-.*', r'purchase-.*'],
        'price_elements': [r'price.*', r'cost.*', r'.*-price']
    }
}
```

### Form-Heavy Application

```python
form_config = {
    'confidence_threshold': 0.7,
    'include_hidden_elements': True,  # Forms may have hidden fields
    'accessibility_analysis': True,   # Important for form usability
    'form_analysis_enabled': True,
    'locator_settings': {
        'prefer_name_attribute': True, # Forms often use name attributes
        'generate_label_selectors': True
    }
}
```

### Single Page Application (SPA)

```python
spa_config = {
    'confidence_threshold': 0.6,     # SPAs can have dynamic content
    'include_hidden_elements': True, # Elements may be shown/hidden dynamically
    'max_depth': 80,                # SPAs can be deeply nested
    'timeout_seconds': 45,          # Allow time for complex analysis
    'enable_cache': False,          # Content changes frequently
    'custom_classifiers': {
        'dynamic_buttons': [r'ng-.*', r'react-.*', r'vue-.*']
    }
}
```

## 🚀 Performance Optimization

### Memory Optimization

```python
memory_optimized_config = {
    'max_cache_size': 10,           # Small cache
    'confidence_threshold': 0.8,    # Fewer elements
    'max_elements': 200,            # Limit total elements processed
    'include_hidden_elements': False,
    'max_depth': 30,               # Shallow traversal
    'parser_preference': ['html.parser'] # Lower memory parser
}
```

### Speed Optimization

```python
speed_optimized_config = {
    'confidence_threshold': 0.9,    # Quick, high-confidence classification
    'timeout_seconds': 10,          # Short timeout
    'max_depth': 25,               # Shallow traversal
    'include_hidden_elements': False,
    'parser_preference': ['lxml'],  # Fastest parser
    'enable_cache': True,          # Cache for repeated content
    'skip_complex_analysis': True  # Skip time-consuming analysis
}
```

## 🔧 Environment-Specific Configuration

### Docker Container

```python
docker_config = {
    'timeout_seconds': 20,          # Conservative timeout
    'max_cache_size': 50,          # Limited memory
    'parser_preference': ['lxml', 'html.parser'], # Avoid html5lib overhead
    'enable_cache': True,
    'confidence_threshold': 0.75
}
```

### Serverless Function

```python
serverless_config = {
    'enable_cache': False,          # No persistent cache
    'timeout_seconds': 10,          # Quick execution
    'confidence_threshold': 0.8,    # High precision, fewer elements
    'max_depth': 30,               # Limit processing
    'include_hidden_elements': False
}
```

### High-Traffic Production

```python
production_config = {
    'enable_cache': True,
    'max_cache_size': 1000,         # Large cache for many pages
    'confidence_threshold': 0.8,
    'timeout_seconds': 15,
    'max_depth': 40,
    'parser_preference': ['lxml'],  # Fastest parser
    'performance_monitoring': {
        'enable_timing': True,
        'log_slow_operations': True,
        'slow_operation_threshold': 3.0
    }
}
```

---

**Next:** Check out the [Integration Guide](integration.md) to learn how to integrate with browser controllers and LAM systems.