# DOM Parser & Analyzer Component - Implementation Prompt

## Context
You are building a DOM Parser & Analyzer component for a Large Action Model (LAM) web automation system. This component processes HTML content from the Browser Controller and provides structured analysis for AI-driven web interaction.

**Integration Point**: The Browser Controller (already implemented) provides HTML content via:
- `session.get_page_source()` - Raw HTML string
- `session.get_page_info()` - Complete page data with metadata
- `session.find_elements()` - Located web elements

**Your Task**: Create a production-ready DOM Parser & Analyzer that transforms raw HTML into intelligent, structured data for AI agents to understand and interact with web pages.

## Component Requirements

### Core Responsibilities
1. **HTML Structure Analysis**: Parse DOM hierarchy, element relationships, and document structure
2. **Element Classification**: Identify interactive elements (buttons, forms, links) vs content elements
3. **Semantic Content Extraction**: Extract meaningful content blocks, navigation areas, headers, footers
4. **Accessibility Analysis**: Parse ARIA attributes, roles, labels for better element understanding
5. **Form Structure Mapping**: Analyze forms, field types, validation requirements, submit actions
6. **Performance Metadata**: Extract page characteristics that affect interaction strategies

### Key Features to Implement
```python
class DOMParser:
    async def parse_page(self, html_source: str, url: str, metadata: dict) -> DOMAnalysisResult
    async def extract_interactive_elements(self, dom_tree) -> List[InteractiveElement]  
    async def analyze_page_structure(self, dom_tree) -> PageStructure
    async def extract_semantic_blocks(self, dom_tree) -> List[SemanticBlock]
    async def analyze_forms(self, dom_tree) -> List[FormStructure]
    async def get_element_hierarchy(self, element) -> ElementHierarchy
    async def find_similar_elements(self, target_element) -> List[Element]
    async def extract_navigation_elements(self, dom_tree) -> NavigationStructure
    async def get_accessibility_info(self, element) -> AccessibilityInfo
```

### Data Structures to Create
```python
@dataclass
class DOMAnalysisResult:
    page_structure: PageStructure
    interactive_elements: List[InteractiveElement]
    semantic_blocks: List[SemanticBlock]
    form_structures: List[FormStructure]
    navigation_structure: NavigationStructure
    accessibility_tree: AccessibilityInfo
    performance_hints: Dict[str, Any]
    element_relationships: Dict[str, List[str]]

@dataclass  
class InteractiveElement:
    element_id: str
    element_type: str  # button, link, input, select, etc.
    locators: Dict[str, str]  # multiple ways to find this element
    properties: Dict[str, Any]
    interaction_hints: List[str]
    accessibility_info: AccessibilityInfo
    
@dataclass
class PageStructure:
    sections: List[PageSection]
    navigation_areas: List[NavigationArea] 
    content_areas: List[ContentArea]
    sidebar_areas: List[SidebarArea]
    header_footer: HeaderFooterInfo
```

### Integration with Browser Controller
```python
# Input from Browser Controller
page_info = await browser_session.get_page_info()

# DOM Parser processes the content  
dom_analysis = await dom_parser.parse_page(
    html_source=page_info.source,
    url=page_info.url,
    metadata=page_info.metadata
)

# Output for other LAM components
interactive_map = dom_analysis.interactive_elements
page_structure = dom_analysis.page_structure
forms = dom_analysis.form_structures
```

## Implementation Structure

Create this folder structure:
```
dom_parser/
├── __init__.py
├── dom_parser.py              # Main parser class
├── html_analyzer.py           # Core HTML parsing logic
├── element_classifier.py      # Element type identification  
├── semantic_extractor.py      # Content meaning extraction
├── form_analyzer.py           # Form structure analysis
├── accessibility_analyzer.py  # A11y information extraction
├── structure_mapper.py        # Page layout and hierarchy
├── types/
│   ├── __init__.py
│   ├── dom_types.py          # Data structures and types
│   └── element_types.py      # Element classification types
└── utils/
    ├── __init__.py
    ├── css_selector_generator.py
    ├── xpath_generator.py
    └── dom_utils.py
```

## Key Implementation Challenges

### 1. Element Classification Intelligence
- Distinguish between clickable buttons vs decorative elements
- Identify form fields and their purposes (email, password, search, etc.)
- Recognize navigation elements vs content links
- Handle dynamic elements that load after initial page load

### 2. Semantic Understanding
- Extract meaningful content blocks (articles, product info, user reviews)
- Identify page sections (header, main content, sidebar, footer)
- Understand element relationships and dependencies
- Handle single-page applications with dynamic content

### 3. Robust Parsing
- Handle malformed HTML gracefully
- Work with various HTML5 semantic elements
- Process complex nested structures
- Handle internationalization and RTL layouts

### 4. Performance Optimization
- Efficient parsing of large HTML documents
- Caching of analysis results for similar page structures
- Lazy loading of detailed analysis for better performance
- Memory-efficient processing of complex DOM trees

## Technical Requirements

### Dependencies to Use
```python
# Required libraries
beautifulsoup4>=4.12.0    # HTML parsing
lxml>=4.9.0               # Fast XML/HTML processing  
html5lib>=1.1            # HTML5 compliant parsing
cssselect>=1.2.0         # CSS selector support
selenium>=4.15.0         # Integration with browser controller
pydantic>=2.0.0          # Data validation
loguru>=0.7.0            # Logging
```

### Integration Points
- **Input**: HTML source from `browser_session.get_page_source()`
- **Processing**: Parse, analyze, and structure the HTML content
- **Output**: Structured data for Semantic Element Mapper, Action Executor, etc.
- **Error Handling**: Graceful degradation when parsing fails

### Performance Targets
- Parse typical web pages (< 1MB HTML) in under 2 seconds
- Memory usage under 100MB for large pages
- Concurrent processing of multiple pages
- Incremental analysis for dynamic content updates

## Testing Requirements

Create comprehensive tests for:
1. **HTML Parsing**: Various HTML structures and edge cases
2. **Element Classification**: Different types of interactive elements
3. **Form Analysis**: Complex forms with validation and dynamic fields
4. **Error Handling**: Malformed HTML, missing elements, timeout scenarios
5. **Performance**: Large pages, concurrent processing, memory usage
6. **Integration**: Seamless data flow from Browser Controller

## Success Criteria

Your DOM Parser should:
- ✅ Parse any valid HTML document without errors
- ✅ Correctly identify 95%+ of interactive elements
- ✅ Extract semantic content blocks with high accuracy
- ✅ Provide multiple locator strategies for each element
- ✅ Handle dynamic content and SPA applications
- ✅ Integrate seamlessly with existing Browser Controller
- ✅ Provide rich accessibility information for AI decision-making
- ✅ Be production-ready with comprehensive error handling and logging

**Start with the main `DOMParser` class and `dom_types.py` data structures, then build the supporting analysis modules. Focus on robust HTML parsing first, then add intelligence layers for classification and semantic understanding.**

---

This DOM Parser will give your LAM system the "eyes" to understand web page structure - essential before adding AI decision-making and autonomous interaction capabilities!