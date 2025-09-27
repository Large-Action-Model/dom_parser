"""
Element Type Enumerations for DOM Parser

Defines different types of elements, interactions, and semantic categories
used throughout the DOM analysis process.
"""

from enum import Enum, auto
from typing import Set


class ElementType(Enum):
    """Classification of HTML element types."""
    
    # Interactive Elements
    BUTTON = "button"
    LINK = "link"
    INPUT = "input"
    TEXTAREA = "textarea"
    SELECT = "select"
    CHECKBOX = "checkbox"
    RADIO = "radio"
    FILE_INPUT = "file_input"
    SUBMIT = "submit"
    FORM = "form"
    
    # Content Elements
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    TABLE = "table"
    LIST = "list"
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    
    # Structural Elements
    NAVIGATION = "navigation"
    HEADER = "header"
    FOOTER = "footer"
    MAIN = "main"
    ASIDE = "aside"
    SECTION = "section"
    ARTICLE = "article"
    DIV = "div"
    SPAN = "span"
    
    # Other
    UNKNOWN = "unknown"


class InteractionType(Enum):
    """Types of interactions possible with elements."""
    
    CLICK = "click"
    TYPE = "type"
    SELECT = "select"
    HOVER = "hover"
    SCROLL = "scroll"
    DRAG = "drag"
    DROP = "drop"
    FOCUS = "focus"
    BLUR = "blur"
    SUBMIT = "submit"
    UPLOAD = "upload"
    DOWNLOAD = "download"
    NAVIGATE = "navigate"
    
    # Complex interactions
    MULTI_SELECT = "multi_select"
    DATE_PICK = "date_pick"
    COLOR_PICK = "color_pick"
    RANGE_SELECT = "range_select"


class SemanticType(Enum):
    """Semantic classification of page content."""
    
    # Navigation
    PRIMARY_NAV = "primary_navigation"
    SECONDARY_NAV = "secondary_navigation"
    BREADCRUMB = "breadcrumb"
    PAGINATION = "pagination"
    
    # Content Areas
    MAIN_CONTENT = "main_content"
    SIDEBAR = "sidebar"
    RELATED_CONTENT = "related_content"
    COMMENTS = "comments"
    REVIEWS = "reviews"
    
    # Forms and Actions
    SEARCH_FORM = "search_form"
    LOGIN_FORM = "login_form"
    REGISTRATION_FORM = "registration_form"
    CONTACT_FORM = "contact_form"
    CHECKOUT_FORM = "checkout_form"
    
    # UI Components
    MODAL = "modal"
    DROPDOWN = "dropdown"
    TABS = "tabs"
    ACCORDION = "accordion"
    CAROUSEL = "carousel"
    TOOLTIP = "tooltip"
    ALERT = "alert"
    
    # E-commerce
    PRODUCT_LISTING = "product_listing"
    PRODUCT_DETAILS = "product_details"
    CART = "cart"
    WISHLIST = "wishlist"
    
    # Other
    ADVERTISEMENT = "advertisement"
    SOCIAL_MEDIA = "social_media"
    COOKIE_BANNER = "cookie_banner"
    UNKNOWN = "unknown"


class FormFieldType(Enum):
    """Types of form fields with their expected input."""
    
    # Text inputs
    TEXT = "text"
    EMAIL = "email"
    PASSWORD = "password"
    PHONE = "phone"
    URL = "url"
    SEARCH = "search"
    
    # Numeric inputs
    NUMBER = "number"
    RANGE = "range"
    
    # Date/Time inputs
    DATE = "date"
    TIME = "time"
    DATETIME = "datetime"
    MONTH = "month"
    WEEK = "week"
    
    # Selection inputs
    SELECT = "select"
    MULTISELECT = "multiselect"
    RADIO = "radio"
    CHECKBOX = "checkbox"
    
    # File inputs
    FILE = "file"
    IMAGE = "image"
    
    # Other inputs
    COLOR = "color"
    HIDDEN = "hidden"
    TEXTAREA = "textarea"
    
    # Action buttons
    SUBMIT = "submit"
    RESET = "reset"
    BUTTON = "button"


class AccessibilityRole(Enum):
    """ARIA roles for accessibility analysis."""
    
    # Landmark roles
    BANNER = "banner"
    COMPLEMENTARY = "complementary"
    CONTENTINFO = "contentinfo"
    MAIN = "main"
    NAVIGATION = "navigation"
    REGION = "region"
    SEARCH = "search"
    
    # Document structure roles
    APPLICATION = "application"
    ARTICLE = "article"
    DOCUMENT = "document"
    
    # Widget roles
    BUTTON = "button"
    CHECKBOX = "checkbox"
    DIALOG = "dialog"
    GRIDCELL = "gridcell"
    LINK = "link"
    LOG = "log"
    MARQUEE = "marquee"
    MENUITEM = "menuitem"
    MENUITEMCHECKBOX = "menuitemcheckbox"
    MENUITEMRADIO = "menuitemradio"
    OPTION = "option"
    PROGRESSBAR = "progressbar"
    RADIO = "radio"
    SCROLLBAR = "scrollbar"
    SLIDER = "slider"
    SPINBUTTON = "spinbutton"
    STATUS = "status"
    TAB = "tab"
    TABPANEL = "tabpanel"
    TEXTBOX = "textbox"
    TIMER = "timer"
    TOOLTIP = "tooltip"
    TREEITEM = "treeitem"
    
    # Composite roles
    COMBOBOX = "combobox"
    GRID = "grid"
    LISTBOX = "listbox"
    MENU = "menu"
    MENUBAR = "menubar"
    RADIOGROUP = "radiogroup"
    TABLIST = "tablist"
    TREE = "tree"
    TREEGRID = "treegrid"
    
    # Live region roles
    ALERT = "alert"
    ALERTDIALOG = "alertdialog"
    
    # Other
    PRESENTATION = "presentation"
    NONE = "none"


# Helper functions and mappings

def get_interactive_element_types() -> Set[ElementType]:
    """Get all element types that are interactive."""
    return {
        ElementType.BUTTON,
        ElementType.LINK,
        ElementType.INPUT,
        ElementType.TEXTAREA,
        ElementType.SELECT,
        ElementType.CHECKBOX,
        ElementType.RADIO,
        ElementType.FILE_INPUT,
        ElementType.SUBMIT,
        ElementType.FORM,
    }


def get_content_element_types() -> Set[ElementType]:
    """Get all element types that are primarily content."""
    return {
        ElementType.TEXT,
        ElementType.IMAGE,
        ElementType.VIDEO,
        ElementType.AUDIO,
        ElementType.TABLE,
        ElementType.LIST,
        ElementType.HEADING,
        ElementType.PARAGRAPH,
    }


def get_structural_element_types() -> Set[ElementType]:
    """Get all element types that are structural."""
    return {
        ElementType.NAVIGATION,
        ElementType.HEADER,
        ElementType.FOOTER,
        ElementType.MAIN,
        ElementType.ASIDE,
        ElementType.SECTION,
        ElementType.ARTICLE,
        ElementType.DIV,
        ElementType.SPAN,
    }


def get_form_field_types() -> Set[FormFieldType]:
    """Get all form field types that can accept user input."""
    return {
        FormFieldType.TEXT,
        FormFieldType.EMAIL,
        FormFieldType.PASSWORD,
        FormFieldType.PHONE,
        FormFieldType.URL,
        FormFieldType.SEARCH,
        FormFieldType.NUMBER,
        FormFieldType.RANGE,
        FormFieldType.DATE,
        FormFieldType.TIME,
        FormFieldType.DATETIME,
        FormFieldType.MONTH,
        FormFieldType.WEEK,
        FormFieldType.SELECT,
        FormFieldType.MULTISELECT,
        FormFieldType.RADIO,
        FormFieldType.CHECKBOX,
        FormFieldType.FILE,
        FormFieldType.IMAGE,
        FormFieldType.COLOR,
        FormFieldType.TEXTAREA,
    }


# Element type mappings for HTML tags
HTML_TAG_TO_ELEMENT_TYPE = {
    # Interactive elements
    'button': ElementType.BUTTON,
    'a': ElementType.LINK,
    'input': ElementType.INPUT,
    'textarea': ElementType.TEXTAREA,
    'select': ElementType.SELECT,
    'form': ElementType.FORM,
    
    # Content elements
    'img': ElementType.IMAGE,
    'video': ElementType.VIDEO,
    'audio': ElementType.AUDIO,
    'table': ElementType.TABLE,
    'ul': ElementType.LIST,
    'ol': ElementType.LIST,
    'li': ElementType.LIST,
    'h1': ElementType.HEADING,
    'h2': ElementType.HEADING,
    'h3': ElementType.HEADING,
    'h4': ElementType.HEADING,
    'h5': ElementType.HEADING,
    'h6': ElementType.HEADING,
    'p': ElementType.PARAGRAPH,
    
    # Structural elements
    'nav': ElementType.NAVIGATION,
    'header': ElementType.HEADER,
    'footer': ElementType.FOOTER,
    'main': ElementType.MAIN,
    'aside': ElementType.ASIDE,
    'section': ElementType.SECTION,
    'article': ElementType.ARTICLE,
    'div': ElementType.DIV,
    'span': ElementType.SPAN,
}


# Input type to form field type mapping
INPUT_TYPE_TO_FORM_FIELD_TYPE = {
    'text': FormFieldType.TEXT,
    'email': FormFieldType.EMAIL,
    'password': FormFieldType.PASSWORD,
    'tel': FormFieldType.PHONE,
    'url': FormFieldType.URL,
    'search': FormFieldType.SEARCH,
    'number': FormFieldType.NUMBER,
    'range': FormFieldType.RANGE,
    'date': FormFieldType.DATE,
    'time': FormFieldType.TIME,
    'datetime-local': FormFieldType.DATETIME,
    'month': FormFieldType.MONTH,
    'week': FormFieldType.WEEK,
    'radio': FormFieldType.RADIO,
    'checkbox': FormFieldType.CHECKBOX,
    'file': FormFieldType.FILE,
    'color': FormFieldType.COLOR,
    'hidden': FormFieldType.HIDDEN,
    'submit': FormFieldType.SUBMIT,
    'reset': FormFieldType.RESET,
    'button': FormFieldType.BUTTON,
}