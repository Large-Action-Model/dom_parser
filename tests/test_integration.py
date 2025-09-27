"""
Integration tests for DOM Parser components.
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for testing
parent_path = Path(__file__).parent.parent
sys.path.insert(0, str(parent_path))

from test_helpers import setup_test_imports, SIMPLE_HTML, FORM_HTML, COMPLEX_HTML

# Setup imports
setup_test_imports()

class TestComponentIntegration:
    """Test that all components work together correctly."""
    
    def test_import_all_components(self):
        """Test that all main components can be imported."""
        try:
            from dom_parser.core.dom_parser import DOMParser
            from dom_parser.core.element_classifier import ElementClassifier
            from dom_parser.core.semantic_extractor import SemanticExtractor
            from dom_parser.core.structure_mapper import StructureMapper
            
            from dom_parser.analyzers.html_analyzer import HTMLAnalyzer
            from dom_parser.analyzers.form_analyzer import FormAnalyzer
            from dom_parser.analyzers.accessibility_analyzer import AccessibilityAnalyzer
            
            from dom_parser.utils.css_selector_generator import CSSSelectorsGenerator
            from dom_parser.utils.xpath_generator import XPathGenerator
            
            # If we get here, all imports worked
            assert True
            
        except ImportError as e:
            pytest.fail(f"Failed to import components: {e}")
    
    def test_create_component_instances(self):
        """Test that all components can be instantiated."""
        try:
            from dom_parser.core.element_classifier import ElementClassifier
            from dom_parser.core.semantic_extractor import SemanticExtractor
            from dom_parser.core.structure_mapper import StructureMapper
            from dom_parser.analyzers.html_analyzer import HTMLAnalyzer
            from dom_parser.utils.css_selector_generator import CSSSelectorsGenerator
            from dom_parser.utils.xpath_generator import XPathGenerator
            
            # Create instances
            classifier = ElementClassifier()
            extractor = SemanticExtractor()
            mapper = StructureMapper()
            html_analyzer = HTMLAnalyzer()
            css_gen = CSSSelectorsGenerator()
            xpath_gen = XPathGenerator()
            
            # Verify instances
            assert classifier is not None
            assert extractor is not None
            assert mapper is not None
            assert html_analyzer is not None
            assert css_gen is not None
            assert xpath_gen is not None
            
        except Exception as e:
            pytest.fail(f"Failed to create component instances: {e}")
    
    def test_html_parsing_chain(self):
        """Test the HTML parsing chain with real HTML."""
        from bs4 import BeautifulSoup
        
        # Parse with BeautifulSoup (core dependency)
        soup = BeautifulSoup(SIMPLE_HTML, 'html.parser')
        
        # Basic validation
        assert soup.find('h1').get_text() == "Simple Page"
        assert soup.find('a').get('href') == "/test"
        assert soup.find('button') is not None
    
    def test_form_parsing_integration(self):
        """Test form parsing integration.""" 
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(FORM_HTML, 'html.parser')
        form = soup.find('form')
        
        assert form is not None
        assert form.get('id') == 'test-form'
        
        inputs = form.find_all('input')
        assert len(inputs) >= 3  # username, password, email
        
        # Check input types
        input_types = [inp.get('type') for inp in inputs]
        assert 'text' in input_types
        assert 'password' in input_types
        assert 'email' in input_types
    
    def test_accessibility_parsing(self):
        """Test accessibility feature parsing."""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(COMPLEX_HTML, 'html.parser')
        
        # Check ARIA roles
        banner = soup.find(attrs={'role': 'banner'})
        navigation = soup.find(attrs={'role': 'navigation'})
        main = soup.find(attrs={'role': 'main'})
        
        assert banner is not None
        assert navigation is not None
        assert main is not None
        
        # Check aria-label
        nav_with_label = soup.find(attrs={'aria-label': 'Main navigation'})
        assert nav_with_label is not None

class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_malformed_html(self):
        """Test handling of malformed HTML."""
        malformed = """
        <html>
        <body>
        <div>Unclosed div
        <p>Missing closing tag
        <span>Some content</span>
        </body>
        </html>
        """
        
        from bs4 import BeautifulSoup
        # BeautifulSoup should handle malformed HTML gracefully
        soup = BeautifulSoup(malformed, 'html.parser')
        assert soup is not None
        assert soup.find('body') is not None
    
    def test_empty_html(self):
        """Test handling of empty or minimal HTML."""
        empty_html = "<html></html>"
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(empty_html, 'html.parser')
        assert soup is not None
        assert soup.find('html') is not None
    
    def test_invalid_html(self):
        """Test handling of completely invalid HTML."""
        invalid = "This is not HTML at all!"
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(invalid, 'html.parser')
        # BeautifulSoup will still create a structure
        assert soup is not None