# Integration Guide

Complete guide for integrating the DOM Parser & Analyzer with browser controllers and Large Action Model (LAM) systems.

## 🎯 Integration Overview

The DOM Parser is designed to seamlessly integrate with browser automation systems, providing structured HTML analysis for AI-driven web interaction. This guide covers integration patterns, best practices, and common use cases.

## 🤖 Browser Controller Integration

### Basic Integration Pattern

```python
from dom_parser import DOMParser
from browser_controller import BrowserController, BrowserConfig, BrowserType

class WebAutomationSystem:
    def __init__(self):
        # Initialize browser controller
        self.browser_config = BrowserConfig(
            browser_type=BrowserType.CHROME,
            headless=True,
            window_size=(1280, 720)
        )
        self.browser = BrowserController(self.browser_config)
        
        # Initialize DOM parser
        self.dom_parser = DOMParser({
            'enable_cache': True,
            'confidence_threshold': 0.8,
            'include_hidden_elements': False
        })
    
    async def analyze_page(self, url: str):
        """Analyze a web page and return structured data."""
        async with self.browser:
            session = await self.browser.create_session()
            
            # Navigate to page
            await session.navigate_to(url)
            
            # Get page information from browser
            page_info = await session.get_page_info()
            
            # Analyze with DOM parser
            analysis = await self.dom_parser.parse_page_from_browser_info(page_info)
            
            return analysis
```

### PageInfo Integration

The DOM Parser can directly consume PageInfo objects from browser controllers:

```python
# Browser controller provides PageInfo
page_info = await session.get_page_info()

# PageInfo structure (adjust to match your browser controller)
class PageInfo:
    url: str              # Current page URL
    title: str            # Page title
    source: str           # Raw HTML content
    timestamp: float      # When page was loaded
    metadata: dict        # Additional metadata

# DOM Parser consumes PageInfo directly
analysis = await dom_parser.parse_page_from_browser_info(page_info)
```

### Custom PageInfo Adapter

If your browser controller uses a different PageInfo structure:

```python
class PageInfoAdapter:
    """Adapter to convert custom PageInfo to DOM Parser format."""
    
    @staticmethod
    def adapt(custom_page_info) -> dict:
        """Convert custom PageInfo to DOM Parser compatible format."""
        return {
            'url': custom_page_info.current_url,
            'title': custom_page_info.page_title,
            'source': custom_page_info.html_content,
            'timestamp': custom_page_info.load_time,
            'metadata': {
                'user_agent': custom_page_info.user_agent,
                'viewport': custom_page_info.viewport_size,
                'load_time': custom_page_info.page_load_duration
            }
        }

# Usage
adapted_info = PageInfoAdapter.adapt(browser_page_info)
analysis = await dom_parser.parse_page(
    html_source=adapted_info['source'],
    url=adapted_info['url'],
    metadata=adapted_info['metadata']
)
```

## 🧠 LAM System Integration

### Action Planning Integration

```python
class ActionPlanner:
    """Plans actions based on DOM analysis for LAM systems."""
    
    def __init__(self):
        self.dom_parser = DOMParser()
        self.action_history = []
    
    async def plan_next_action(self, page_info, goal: str):
        """Plan the next action based on page analysis and goal."""
        
        # Analyze current page
        analysis = await self.dom_parser.parse_page_from_browser_info(page_info)
        
        # Extract actionable elements
        actionable_elements = self._extract_actionable_elements(analysis)
        
        # Use AI/ML to select best action
        planned_action = self._select_action(actionable_elements, goal)
        
        return planned_action
    
    def _extract_actionable_elements(self, analysis):
        """Extract elements suitable for automation actions."""
        elements = {
            'clickable': [],
            'fillable': [],
            'navigational': []
        }
        
        for element in analysis.interactive_elements:
            if element.interaction_type == InteractionType.CLICK:
                elements['clickable'].append({
                    'id': element.element_id,
                    'type': element.element_type,
                    'text': element.visible_text,
                    'locator': element.locators['css'],
                    'confidence': element.confidence_score
                })
            elif element.interaction_type == InteractionType.TEXT_INPUT:
                elements['fillable'].append({
                    'id': element.element_id,
                    'field_type': element.form_field_type,
                    'placeholder': element.attributes.get('placeholder', ''),
                    'required': element.attributes.get('required', False),
                    'locator': element.locators['css']
                })
            elif element.interaction_type == InteractionType.NAVIGATION:
                elements['navigational'].append({
                    'id': element.element_id,
                    'text': element.visible_text,
                    'href': element.attributes.get('href', ''),
                    'locator': element.locators['css']
                })
        
        return elements
    
    def _select_action(self, elements, goal):
        """Select best action using AI/ML logic."""
        # This would contain your AI/ML logic for action selection
        # For example, using embeddings, rule-based systems, or ML models
        pass
```

### Conversational AI Integration

```python
class ConversationalWebAgent:
    """AI agent that can interact with web pages through conversation."""
    
    def __init__(self, llm_client):
        self.dom_parser = DOMParser()
        self.llm_client = llm_client
        self.conversation_history = []
    
    async def process_user_request(self, request: str, page_info):
        """Process user request and interact with the page."""
        
        # Analyze current page
        analysis = await self.dom_parser.parse_page_from_browser_info(page_info)
        
        # Create context for LLM
        context = self._create_page_context(analysis)
        
        # Generate response with LLM
        response = await self._generate_response(request, context)
        
        return response
    
    def _create_page_context(self, analysis):
        """Create structured context for LLM."""
        context = {
            'page_title': analysis.source_title,
            'page_url': analysis.source_url,
            'available_actions': [],
            'forms': [],
            'content_summary': []
        }
        
        # Add interactive elements
        for element in analysis.interactive_elements:
            if element.confidence_score > 0.7:
                context['available_actions'].append({
                    'action': element.interaction_type.value,
                    'target': element.visible_text or element.tag_name,
                    'description': self._describe_element(element)
                })
        
        # Add form information
        for form in analysis.form_structures:
            form_info = {
                'purpose': self._infer_form_purpose(form),
                'fields': [f.form_field_type.value for f in form.fields],
                'required_fields': [f.visible_text for f in form.fields 
                                  if f.attributes.get('required')]
            }
            context['forms'].append(form_info)
        
        # Add semantic content
        for block in analysis.semantic_blocks:
            if block.semantic_type in [SemanticType.HEADING, SemanticType.MAIN_CONTENT]:
                context['content_summary'].append({
                    'type': block.semantic_type.value,
                    'content': block.text_content[:200]  # Truncate for context
                })
        
        return context
    
    def _describe_element(self, element):
        """Generate human-readable description of element."""
        descriptions = {
            ElementType.BUTTON: f"Button '{element.visible_text}'",
            ElementType.LINK: f"Link to '{element.visible_text}'",
            ElementType.INPUT: f"Input field for {element.form_field_type.value if element.form_field_type else 'text'}",
        }
        return descriptions.get(element.element_type, f"{element.element_type.value} element")
```

### Multi-Page Workflow Integration

```python
class WorkflowExecutor:
    """Execute multi-page workflows using DOM analysis."""
    
    def __init__(self):
        self.dom_parser = DOMParser()
        self.workflow_state = {}
    
    async def execute_workflow(self, workflow_steps, browser_session):
        """Execute a multi-step workflow."""
        results = []
        
        for step in workflow_steps:
            # Get current page state
            page_info = await browser_session.get_page_info()
            analysis = await self.dom_parser.parse_page_from_browser_info(page_info)
            
            # Execute step based on analysis
            step_result = await self._execute_step(step, analysis, browser_session)
            results.append(step_result)
            
            # Update workflow state
            self._update_workflow_state(step, analysis, step_result)
        
        return results
    
    async def _execute_step(self, step, analysis, session):
        """Execute a single workflow step."""
        step_type = step['type']
        
        if step_type == 'fill_form':
            return await self._fill_form(step, analysis, session)
        elif step_type == 'click_element':
            return await self._click_element(step, analysis, session)
        elif step_type == 'extract_data':
            return await self._extract_data(step, analysis)
        elif step_type == 'navigate':
            return await self._navigate(step, analysis, session)
        
    async def _fill_form(self, step, analysis, session):
        """Fill form based on step configuration and analysis."""
        form_data = step['data']
        
        # Find appropriate form
        target_form = None
        for form in analysis.form_structures:
            if self._form_matches_criteria(form, step.get('form_criteria', {})):
                target_form = form
                break
        
        if not target_form:
            raise Exception("No matching form found")
        
        # Fill form fields
        for field in target_form.fields:
            field_name = field.attributes.get('name', '')
            if field_name in form_data:
                locator = field.locators['css']
                value = form_data[field_name]
                await session.fill_field(locator, value)
        
        return {'status': 'success', 'form_id': target_form.form_id}
```

## 🔄 Real-time Integration Patterns

### Event-Driven Analysis

```python
class EventDrivenAnalyzer:
    """Analyze pages in response to browser events."""
    
    def __init__(self):
        self.dom_parser = DOMParser()
        self.analysis_cache = {}
    
    async def on_page_loaded(self, event):
        """Handle page load events."""
        page_info = event.page_info
        
        # Quick analysis for immediate needs
        quick_analysis = await self.dom_parser.parse_page_from_browser_info(
            page_info,
            override_config={'confidence_threshold': 0.8}
        )
        
        # Cache for later use
        self.analysis_cache[page_info.url] = quick_analysis
        
        # Trigger downstream processing
        await self._process_page_loaded(quick_analysis)
    
    async def on_dom_changed(self, event):
        """Handle DOM mutation events."""
        # Re-analyze changed portions
        if event.url in self.analysis_cache:
            # Incremental analysis if supported
            updated_analysis = await self._incremental_analysis(event)
            self.analysis_cache[event.url] = updated_analysis
    
    async def _incremental_analysis(self, change_event):
        """Perform incremental analysis of DOM changes."""
        # Implementation depends on change detection capabilities
        pass
```

### Streaming Analysis

```python
class StreamingAnalyzer:
    """Stream analysis results as they become available."""
    
    def __init__(self):
        self.dom_parser = DOMParser()
    
    async def stream_analysis(self, page_info, callback):
        """Stream analysis results to callback function."""
        
        # Start analysis
        analysis_task = asyncio.create_task(
            self.dom_parser.parse_page_from_browser_info(page_info)
        )
        
        # Stream intermediate results if available
        async for partial_result in self._stream_partial_results(analysis_task):
            await callback(partial_result)
        
        # Final result
        final_result = await analysis_task
        await callback(final_result)
    
    async def _stream_partial_results(self, analysis_task):
        """Generate partial results during analysis."""
        # This would require internal modifications to DOM Parser
        # to support streaming results
        yield {"status": "html_parsed"}
        yield {"status": "elements_classified"}
        yield {"status": "semantic_analysis_complete"}
```

## 🔌 Plugin Architecture

### Custom Analyzer Plugins

```python
class PluginManager:
    """Manage custom analyzer plugins."""
    
    def __init__(self):
        self.dom_parser = DOMParser()
        self.plugins = {}
    
    def register_plugin(self, name: str, plugin_class):
        """Register a custom analyzer plugin."""
        self.plugins[name] = plugin_class()
    
    async def analyze_with_plugins(self, page_info):
        """Run analysis with all registered plugins."""
        
        # Base DOM analysis
        base_analysis = await self.dom_parser.parse_page_from_browser_info(page_info)
        
        # Run plugins
        plugin_results = {}
        for name, plugin in self.plugins.items():
            plugin_results[name] = await plugin.analyze(base_analysis)
        
        # Combine results
        enhanced_analysis = self._combine_results(base_analysis, plugin_results)
        return enhanced_analysis

class EcommerceAnalyzerPlugin:
    """Plugin for e-commerce specific analysis."""
    
    async def analyze(self, base_analysis):
        """Analyze e-commerce specific elements."""
        ecommerce_data = {
            'products': [],
            'cart_elements': [],
            'price_elements': [],
            'review_elements': []
        }
        
        for element in base_analysis.interactive_elements:
            # Detect product add-to-cart buttons
            if self._is_add_to_cart_button(element):
                ecommerce_data['cart_elements'].append(element)
            
            # Detect price elements
            if self._is_price_element(element):
                ecommerce_data['price_elements'].append(element)
        
        return ecommerce_data
    
    def _is_add_to_cart_button(self, element):
        """Detect add-to-cart buttons."""
        text = element.visible_text.lower()
        classes = element.attributes.get('class', '').lower()
        
        return any(phrase in text for phrase in ['add to cart', 'buy now', 'purchase']) or \
               any(phrase in classes for phrase in ['add-cart', 'buy-button', 'purchase-btn'])
```

## 📊 Performance Integration

### Monitoring and Metrics

```python
class PerformanceMonitor:
    """Monitor DOM Parser performance in integrated systems."""
    
    def __init__(self):
        self.metrics = {
            'analysis_times': [],
            'element_counts': [],
            'memory_usage': [],
            'error_rates': []
        }
    
    async def monitored_analysis(self, dom_parser, page_info):
        """Perform analysis with performance monitoring."""
        
        start_time = time.time()
        start_memory = self._get_memory_usage()
        
        try:
            analysis = await dom_parser.parse_page_from_browser_info(page_info)
            
            # Record metrics
            end_time = time.time()
            end_memory = self._get_memory_usage()
            
            self.metrics['analysis_times'].append(end_time - start_time)
            self.metrics['element_counts'].append(len(analysis.interactive_elements))
            self.metrics['memory_usage'].append(end_memory - start_memory)
            
            return analysis
            
        except Exception as e:
            self.metrics['error_rates'].append(1)
            raise
        else:
            self.metrics['error_rates'].append(0)
    
    def get_performance_summary(self):
        """Get performance summary statistics."""
        return {
            'avg_analysis_time': statistics.mean(self.metrics['analysis_times']),
            'avg_element_count': statistics.mean(self.metrics['element_counts']),
            'avg_memory_usage': statistics.mean(self.metrics['memory_usage']),
            'error_rate': statistics.mean(self.metrics['error_rates'])
        }
```

### Load Balancing

```python
class AnalysisLoadBalancer:
    """Load balance DOM analysis across multiple parser instances."""
    
    def __init__(self, num_parsers: int = 4):
        self.parsers = [DOMParser() for _ in range(num_parsers)]
        self.current_parser = 0
        self.lock = asyncio.Lock()
    
    async def analyze(self, page_info):
        """Distribute analysis across parser instances."""
        
        async with self.lock:
            parser = self.parsers[self.current_parser]
            self.current_parser = (self.current_parser + 1) % len(self.parsers)
        
        return await parser.parse_page_from_browser_info(page_info)
```

## 🛡️ Security Integration

### Content Validation

```python
class SecureAnalyzer:
    """Secure wrapper for DOM analysis with content validation."""
    
    def __init__(self):
        self.dom_parser = DOMParser()
        self.content_validator = ContentValidator()
    
    async def secure_analyze(self, page_info):
        """Perform analysis with security validation."""
        
        # Validate content before analysis
        if not self.content_validator.is_safe(page_info.source):
            raise SecurityError("Unsafe content detected")
        
        # Sanitize if needed
        sanitized_source = self.content_validator.sanitize(page_info.source)
        
        # Create sanitized page info
        safe_page_info = PageInfo(
            url=page_info.url,
            title=page_info.title,
            source=sanitized_source,
            timestamp=page_info.timestamp,
            metadata=page_info.metadata
        )
        
        return await self.dom_parser.parse_page_from_browser_info(safe_page_info)

class ContentValidator:
    """Validate and sanitize HTML content."""
    
    def is_safe(self, html_content: str) -> bool:
        """Check if HTML content is safe to analyze."""
        # Implement security checks
        dangerous_patterns = [
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'vbscript:',
            r'data:.*?base64'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, html_content, re.IGNORECASE | re.DOTALL):
                return False
        
        return True
    
    def sanitize(self, html_content: str) -> str:
        """Sanitize HTML content for safe analysis."""
        # Remove potentially dangerous elements
        sanitized = re.sub(r'<script.*?>.*?</script>', '', html_content, flags=re.IGNORECASE | re.DOTALL)
        sanitized = re.sub(r'<style.*?>.*?</style>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)
        sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
        
        return sanitized
```

## 🔧 Testing Integration

### Integration Testing Framework

```python
class IntegrationTestSuite:
    """Test DOM Parser integration with browser controllers."""
    
    def __init__(self):
        self.dom_parser = DOMParser()
        self.test_pages = []
    
    async def run_integration_tests(self, browser_controller):
        """Run comprehensive integration tests."""
        
        results = []
        
        for test_page in self.test_pages:
            result = await self._test_page_analysis(test_page, browser_controller)
            results.append(result)
        
        return self._summarize_results(results)
    
    async def _test_page_analysis(self, test_page, browser_controller):
        """Test analysis of a specific page."""
        
        async with browser_controller:
            session = await browser_controller.create_session()
            await session.navigate_to(test_page['url'])
            
            page_info = await session.get_page_info()
            analysis = await self.dom_parser.parse_page_from_browser_info(page_info)
            
            # Validate expected elements
            validation_result = self._validate_analysis(analysis, test_page['expected'])
            
            return {
                'url': test_page['url'],
                'success': validation_result['success'],
                'details': validation_result['details']
            }
```

## 🚀 Deployment Integration

### Container Integration

```dockerfile
# Dockerfile for integrated system
FROM python:3.11-slim

# Install system dependencies for DOM parsing
RUN apt-get update && apt-get install -y \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy DOM Parser
COPY dom_parser/ /app/dom_parser/

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

# Set up integrated application
COPY integration/ /app/integration/
WORKDIR /app

CMD ["python", "integration/main.py"]
```

### Kubernetes Integration

```yaml
# kubernetes-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-automation-system
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-automation
  template:
    metadata:
      labels:
        app: web-automation
    spec:
      containers:
      - name: automation-agent
        image: your-registry/web-automation:latest
        env:
        - name: DOM_PARSER_CACHE_SIZE
          value: "100"
        - name: DOM_PARSER_CONFIDENCE_THRESHOLD
          value: "0.8"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

---

**Next Steps:**
- Review [Troubleshooting Guide](troubleshooting.md) for common integration issues
- Check [Performance Guide](performance.md) for optimization tips
- Explore [API Reference](api-reference.md) for detailed method documentation