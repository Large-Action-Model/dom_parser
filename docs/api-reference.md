# API Reference

Complete API documentation for the DOM Parser & Analyzer component.

## Core Classes

### DOMParser

The main orchestration class for DOM analysis.

```python
class DOMParser:
    """Main DOM Parser class for analyzing HTML content from Browser Controller."""
```

#### Constructor

```python
def __init__(self, config: Optional[Dict[str, Any]] = None)
```

**Parameters:**
- `config` (Optional[Dict[str, Any]]): Configuration dictionary

**Configuration Options:**
- `enable_cache` (bool): Enable analysis result caching (default: True)
- `max_cache_size` (int): Maximum number of cached analyses (default: 100)
- `include_hidden_elements` (bool): Include hidden elements in analysis (default: False)
- `confidence_threshold` (float): Minimum confidence for element classification (default: 0.7)
- `max_depth` (int): Maximum DOM traversal depth (default: 50)
- `timeout_seconds` (int): Analysis timeout in seconds (default: 30)

#### Methods

##### parse_page

```python
async def parse_page(
    self,
    html_source: str,
    url: str = "",
    metadata: Optional[Dict[str, Any]] = None
) -> DOMAnalysisResult
```

Analyze HTML content and return structured results.

**Parameters:**
- `html_source` (str): Raw HTML content to analyze
- `url` (str): Source URL of the HTML (optional)
- `metadata` (Optional[Dict[str, Any]]): Additional metadata

**Returns:**
- `DOMAnalysisResult`: Complete analysis results

**Example:**
```python
analysis = await parser.parse_page(
    html_source="<html>...</html>",
    url="https://example.com",
    metadata={"page_type": "product"}
)
```

##### parse_page_from_browser_info

```python
async def parse_page_from_browser_info(self, page_info) -> DOMAnalysisResult
```

Analyze page using browser controller's PageInfo object.

**Parameters:**
- `page_info`: PageInfo object from browser controller

**Returns:**
- `DOMAnalysisResult`: Complete analysis results

**Example:**
```python
page_info = await session.get_page_info()
analysis = await parser.parse_page_from_browser_info(page_info)
```

##### find_similar_elements

```python
async def find_similar_elements(
    self,
    target_element_id: str,
    similarity_threshold: float = 0.8
) -> List[InteractiveElement]
```

Find elements similar to the target element.

**Parameters:**
- `target_element_id` (str): ID of the target element
- `similarity_threshold` (float): Minimum similarity score (default: 0.8)

**Returns:**
- `List[InteractiveElement]`: List of similar elements

## Data Classes

### DOMAnalysisResult

Complete result of DOM analysis.

```python
@dataclass
class DOMAnalysisResult:
    source_url: str
    source_title: str
    analysis_timestamp: float
    processing_time: float
    interactive_elements: List[InteractiveElement]
    semantic_blocks: List[SemanticBlock]
    form_structures: List[FormStructure]
    page_structure: PageStructure
    navigation_structure: NavigationStructure
    accessibility_info: AccessibilityInfo
    confidence_scores: Dict[str, float]
    performance_hints: Dict[str, Any]
```

#### Methods

```python
def get_clickable_elements(self) -> List[InteractiveElement]
```
Get all clickable elements (buttons, links, etc.).

```python
def get_form_fields(self) -> List[InteractiveElement]
```
Get all form input fields.

```python
def get_navigation_elements(self) -> List[InteractiveElement]
```
Get all navigation-related elements.

```python
def get_elements_by_type(self, element_type: ElementType) -> List[InteractiveElement]
```
Get elements filtered by type.

### InteractiveElement

Represents a single interactive element on the page.

```python
@dataclass
class InteractiveElement:
    element_id: str
    element_type: ElementType
    tag_name: str
    attributes: Dict[str, str]
    visible_text: str
    interaction_type: Optional[InteractionType]
    form_field_type: Optional[FormFieldType]
    locators: Dict[str, str]
    bounding_box: Optional[Dict[str, float]]
    is_visible: bool
    is_enabled: bool
    confidence_score: float
    accessibility_info: AccessibilityInfo
    parent_form_id: Optional[str]
    semantic_context: Optional[str]
```

### FormStructure

Represents form structure and metadata.

```python
@dataclass
class FormStructure:
    form_id: str
    action: str
    method: str
    form_type: Optional[FormType]
    fields: List[InteractiveElement]
    submit_buttons: List[InteractiveElement]
    validation_info: Dict[str, Any]
    accessibility_info: AccessibilityInfo
```

### SemanticBlock

Represents a semantic content block.

```python
@dataclass
class SemanticBlock:
    block_id: str
    semantic_type: SemanticType
    elements: List[str]
    text_content: str
    heading_level: Optional[int]
    importance_score: float
    parent_block_id: Optional[str]
```

### PageStructure

Represents overall page layout and structure.

```python
@dataclass
class PageStructure:
    layout_type: str
    main_content_area: Optional[ContentArea]
    sidebar_areas: List[SidebarArea]
    navigation_areas: List[NavigationArea]
    header_footer: HeaderFooterInfo
    content_sections: List[PageSection]
```

### AccessibilityInfo

Accessibility information for elements.

```python
@dataclass
class AccessibilityInfo:
    role: Optional[str]
    label: Optional[str]
    description: Optional[str]
    keyboard_accessible: bool
    screen_reader_text: Optional[str]
    contrast_ratio: Optional[float]
    has_focus_indicator: bool
```

## Enumerations

### ElementType

Classification of HTML elements.

```python
class ElementType(Enum):
    BUTTON = "button"
    LINK = "link"
    INPUT = "input"
    TEXTAREA = "textarea"
    SELECT = "select"
    CHECKBOX = "checkbox"
    RADIO = "radio"
    FORM = "form"
    NAVIGATION = "navigation"
    MAIN = "main"
    HEADER = "header"
    FOOTER = "footer"
    ASIDE = "aside"
    ARTICLE = "article"
    SECTION = "section"
    DIV = "div"
    SPAN = "span"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    UNKNOWN = "unknown"
```

### InteractionType

Types of interactions possible with elements.

```python
class InteractionType(Enum):
    CLICK = "click"
    DOUBLE_CLICK = "double_click"
    RIGHT_CLICK = "right_click"
    HOVER = "hover"
    TEXT_INPUT = "text_input"
    SELECTION = "selection"
    FORM_SUBMIT = "form_submit"
    NAVIGATION = "navigation"
    DRAG_DROP = "drag_drop"
    FILE_UPLOAD = "file_upload"
    TOGGLE = "toggle"
```

### SemanticType

Semantic classification of content blocks.

```python
class SemanticType(Enum):
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    LIST = "list"
    TABLE = "table"
    NAVIGATION = "navigation"
    MAIN_CONTENT = "main_content"
    SIDEBAR = "sidebar"
    FOOTER = "footer"
    HEADER = "header"
    ARTICLE = "article"
    SECTION = "section"
    ASIDE = "aside"
    BLOCKQUOTE = "blockquote"
    CODE = "code"
    MEDIA = "media"
    ADVERTISEMENT = "advertisement"
    BREADCRUMB = "breadcrumb"
    SEARCH = "search"
    SOCIAL = "social"
    CONTACT = "contact"
    COPYRIGHT = "copyright"
    UNKNOWN = "unknown"
```

### FormFieldType

Types of form input fields.

```python
class FormFieldType(Enum):
    TEXT = "text"
    EMAIL = "email"
    PASSWORD = "password"
    NUMBER = "number"
    SEARCH = "search"
    URL = "url"
    TEL = "tel"
    DATE = "date"
    TIME = "time"
    DATETIME = "datetime"
    CHECKBOX = "checkbox"
    RADIO = "radio"
    SELECT = "select"
    TEXTAREA = "textarea"
    FILE = "file"
    HIDDEN = "hidden"
    SUBMIT = "submit"
    BUTTON = "button"
    RESET = "reset"
    COLOR = "color"
    RANGE = "range"
```

### AccessibilityRole

ARIA roles for accessibility.

```python
class AccessibilityRole(Enum):
    BUTTON = "button"
    LINK = "link"
    TEXTBOX = "textbox"
    CHECKBOX = "checkbox"
    RADIO = "radio"
    COMBOBOX = "combobox"
    LISTBOX = "listbox"
    MENU = "menu"
    MENUITEM = "menuitem"
    TAB = "tab"
    TABPANEL = "tabpanel"
    DIALOG = "dialog"
    ALERT = "alert"
    STATUS = "status"
    NAVIGATION = "navigation"
    MAIN = "main"
    BANNER = "banner"
    CONTENTINFO = "contentinfo"
    COMPLEMENTARY = "complementary"
    SEARCH = "search"
    FORM = "form"
    REGION = "region"
    ARTICLE = "article"
    SECTION = "section"
    HEADING = "heading"
    LIST = "list"
    LISTITEM = "listitem"
    TABLE = "table"
    ROW = "row"
    CELL = "cell"
    COLUMNHEADER = "columnheader"
    ROWHEADER = "rowheader"
```

## Utility Classes

### CSSSelectorsGenerator

Generates robust CSS selectors for elements.

```python
class CSSSelectorsGenerator:
    @staticmethod
    def generate_selector(element: Tag, soup: BeautifulSoup) -> str
```

### XPathGenerator

Generates XPath expressions for elements.

```python
class XPathGenerator:
    @staticmethod
    def generate_xpath(element: Tag, soup: BeautifulSoup) -> str
```

## Error Handling

The DOM Parser includes comprehensive error handling:

```python
try:
    analysis = await parser.parse_page(html_source)
except Exception as e:
    logger.error(f"DOM analysis failed: {e}")
    # Handle error appropriately
```

Common exceptions:
- `ValueError`: Invalid HTML or configuration
- `TimeoutError`: Analysis timeout exceeded
- `MemoryError`: HTML too large for processing

## Performance Considerations

- Use caching for repeated analysis of similar pages
- Set appropriate `confidence_threshold` to filter low-quality elements
- Configure `max_depth` to limit DOM traversal for very deep pages
- Use `include_hidden_elements=False` for faster processing

## Examples

### Basic Usage
```python
from dom_parser import DOMParser

parser = DOMParser()
analysis = await parser.parse_page(html_source, url)

for element in analysis.get_clickable_elements():
    print(f"Clickable: {element.visible_text} - {element.locators['css']}")
```

### Configuration
```python
config = {
    'enable_cache': True,
    'confidence_threshold': 0.8,
    'include_hidden_elements': False
}

parser = DOMParser(config)
```

### Form Analysis
```python
for form in analysis.form_structures:
    print(f"Form: {form.action}")
    for field in form.fields:
        print(f"  {field.form_field_type}: {field.visible_text}")
```