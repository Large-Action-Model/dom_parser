"""
Form Analyzer for analyzing form structures and field relationships.

Identifies form elements, field types, validation requirements,
and form submission patterns for automated form interaction.
"""

from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup, Tag

from ..types.dom_data_types import (
    FormStructure, InteractiveElement, AccessibilityInfo
)
from ..types.element_data_types import (
    FormFieldType, SemanticType
)


class FormAnalyzer:
    """
    Analyzes form structures and field relationships.
    
    Identifies form patterns, field groupings, validation rules,
    and submission mechanisms for intelligent form automation.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize Form Analyzer."""
        self.config = config or {}
    
    async def analyze_forms(self, soup: BeautifulSoup) -> List[FormStructure]:
        """Analyze all forms in the document."""
        forms = []
        form_elements = soup.find_all('form')
        
        for idx, form_element in enumerate(form_elements):
            form_structure = await self._analyze_single_form(form_element, idx)
            forms.append(form_structure)
        
        return forms
    
    async def _analyze_single_form(self, form_element: Tag, idx: int) -> FormStructure:
        """Analyze a single form element."""
        form_id = f"form_{idx}"
        
        # Extract form attributes
        action = form_element.get('action', '')
        method = form_element.get('method', 'GET').upper()
        enctype = form_element.get('enctype', 'application/x-www-form-urlencoded')
        
        # Find form fields
        field_elements = form_element.find_all(['input', 'textarea', 'select', 'button'])
        fields = []
        submit_buttons = []
        required_fields = []
        
        for field_idx, field_element in enumerate(field_elements):
            field_id = f"field_{idx}_{field_idx}"
            
            # Create basic InteractiveElement for the field
            field = InteractiveElement(
                element_id=field_id,
                element_type=self._get_field_element_type(field_element),
                tag_name=field_element.name,
                text_content=field_element.get_text(strip=True),
                form_field_type=self._get_form_field_type(field_element)
            )
            
            fields.append(field)
            
            # Check for submit buttons
            if (field_element.name == 'button' or 
                (field_element.name == 'input' and field_element.get('type') in ['submit', 'button'])):
                submit_buttons.append(field_id)
            
            # Check for required fields
            if field_element.has_attr('required'):
                required_fields.append(field_id)
        
        # Determine form type
        form_type = self._determine_form_type(form_element, fields)
        
        # Create form structure
        form_structure = FormStructure(
            form_id=form_id,
            form_element_id=f"form_elem_{idx}",
            action=action,
            method=method,
            encoding_type=enctype,
            fields=fields,
            submit_buttons=submit_buttons,
            required_fields=required_fields,
            form_type=form_type
        )
        
        return form_structure
    
    def _get_field_element_type(self, element: Tag):
        """Get element type for form field."""
        from ..types.element_data_types import ElementType
        
        if element.name == 'input':
            input_type = element.get('type', 'text').lower()
            if input_type == 'checkbox':
                return ElementType.CHECKBOX
            elif input_type == 'radio':
                return ElementType.RADIO
            elif input_type in ['submit', 'button']:
                return ElementType.SUBMIT
            else:
                return ElementType.INPUT
        elif element.name == 'textarea':
            return ElementType.TEXTAREA
        elif element.name == 'select':
            return ElementType.SELECT
        elif element.name == 'button':
            return ElementType.BUTTON
        
        return ElementType.UNKNOWN
    
    def _get_form_field_type(self, element: Tag) -> Optional[FormFieldType]:
        """Determine form field type."""
        if element.name == 'input':
            input_type = element.get('type', 'text').lower()
            mapping = {
                'text': FormFieldType.TEXT,
                'email': FormFieldType.EMAIL,
                'password': FormFieldType.PASSWORD,
                'tel': FormFieldType.PHONE,
                'url': FormFieldType.URL,
                'search': FormFieldType.SEARCH,
                'number': FormFieldType.NUMBER,
                'date': FormFieldType.DATE,
                'time': FormFieldType.TIME,
                'checkbox': FormFieldType.CHECKBOX,
                'radio': FormFieldType.RADIO,
                'file': FormFieldType.FILE,
                'submit': FormFieldType.SUBMIT,
                'button': FormFieldType.BUTTON,
            }
            return mapping.get(input_type, FormFieldType.TEXT)
        elif element.name == 'textarea':
            return FormFieldType.TEXTAREA
        elif element.name == 'select':
            return FormFieldType.MULTISELECT if element.has_attr('multiple') else FormFieldType.SELECT
        elif element.name == 'button':
            return FormFieldType.BUTTON
        
        return None
    
    def _determine_form_type(self, form_element: Tag, fields: List[InteractiveElement]) -> Optional[SemanticType]:
        """Determine the semantic type of the form."""
        # Analyze form attributes and field types
        form_classes = ' '.join(form_element.get('class', [])).lower()
        form_id = form_element.get('id', '').lower()
        
        # Check for login forms
        if any(keyword in form_classes or keyword in form_id 
               for keyword in ['login', 'signin', 'auth']):
            return SemanticType.LOGIN_FORM
        
        # Check for search forms
        if any(keyword in form_classes or keyword in form_id 
               for keyword in ['search', 'query']):
            return SemanticType.SEARCH_FORM
        
        # Check for registration forms
        if any(keyword in form_classes or keyword in form_id 
               for keyword in ['register', 'signup', 'create']):
            return SemanticType.REGISTRATION_FORM
        
        # Check for contact forms
        if any(keyword in form_classes or keyword in form_id 
               for keyword in ['contact', 'message', 'feedback']):
            return SemanticType.CONTACT_FORM
        
        # Analyze field types
        field_types = [field.form_field_type for field in fields if field.form_field_type]
        
        # Login form patterns
        if (FormFieldType.EMAIL in field_types or FormFieldType.TEXT in field_types) and FormFieldType.PASSWORD in field_types:
            return SemanticType.LOGIN_FORM
        
        # Search form patterns
        if FormFieldType.SEARCH in field_types or (len(field_types) == 1 and FormFieldType.TEXT in field_types):
            return SemanticType.SEARCH_FORM
        
        return None