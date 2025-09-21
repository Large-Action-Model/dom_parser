"""
HTML Analyzer for robust HTML parsing and DOM tree creation.

Provides core HTML parsing functionality using BeautifulSoup and lxml,
with error handling for malformed HTML and various document types.
"""

import re
from typing import Optional, Dict, Any, List
from bs4 import BeautifulSoup, Comment
import lxml
from lxml import etree


class HTMLAnalyzer:
    """
    Core HTML parsing and analysis component.
    
    Handles HTML parsing with multiple parsers for robustness,
    cleans and normalizes content, and provides DOM tree access.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize HTML Analyzer with configuration.
        
        Args:
            config: Configuration dictionary for analyzer behavior
        """
        self.config = config or {}
        
        # Parser preferences (in order of preference)
        self.parsers = self.config.get('parsers', ['lxml', 'html.parser', 'html5lib'])
        self.remove_comments = self.config.get('remove_comments', True)
        self.remove_scripts = self.config.get('remove_scripts', True)
        self.remove_styles = self.config.get('remove_styles', True)
        self.normalize_whitespace = self.config.get('normalize_whitespace', True)
        
        # Parser options
        self.parser_options = self.config.get('parser_options', {
            'lxml': {'features': 'lxml'},
            'html.parser': {'features': 'html.parser'},
            'html5lib': {'features': 'html5lib'}
        })
    
    async def parse_html(self, html_source: str) -> BeautifulSoup:
        """
        Parse HTML source into BeautifulSoup DOM tree.
        
        Args:
            html_source: Raw HTML source code
            
        Returns:
            BeautifulSoup DOM tree object
            
        Raises:
            Exception: If all parsers fail to parse the HTML
        """
        if not html_source or not html_source.strip():
            raise ValueError("HTML source is empty or None")
        
        # Try parsers in order of preference
        last_error = None
        for parser in self.parsers:
            try:
                soup = self._parse_with_parser(html_source, parser)
                if soup:
                    # Clean and normalize the parsed tree
                    await self._clean_dom_tree(soup)
                    return soup
            except Exception as e:
                last_error = e
                continue
        
        # If all parsers failed, raise the last error
        if last_error:
            raise Exception(f"All HTML parsers failed. Last error: {str(last_error)}")
        else:
            raise Exception("Failed to parse HTML with any available parser")
    
    def _parse_with_parser(self, html_source: str, parser: str) -> Optional[BeautifulSoup]:
        """
        Parse HTML with a specific parser.
        
        Args:
            html_source: Raw HTML source
            parser: Parser name to use
            
        Returns:
            BeautifulSoup object or None if parsing failed
        """
        parser_opts = self.parser_options.get(parser, {})
        
        try:
            # Handle encoding issues
            if isinstance(html_source, bytes):
                html_source = html_source.decode('utf-8', errors='replace')
            
            # Create BeautifulSoup object
            soup = BeautifulSoup(html_source, **parser_opts)
            
            # Basic validation
            if not soup or not soup.find():
                return None
            
            return soup
            
        except Exception as e:
            # Log parser-specific errors if needed
            return None
    
    async def _clean_dom_tree(self, soup: BeautifulSoup) -> None:
        """
        Clean and normalize the DOM tree.
        
        Args:
            soup: BeautifulSoup DOM tree to clean
        """
        # Remove comments
        if self.remove_comments:
            for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
                comment.extract()
        
        # Remove script tags
        if self.remove_scripts:
            for script in soup.find_all('script'):
                script.decompose()
        
        # Remove style tags
        if self.remove_styles:
            for style in soup.find_all('style'):
                style.decompose()
        
        # Normalize whitespace in text content
        if self.normalize_whitespace:
            await self._normalize_text_content(soup)
        
        # Remove empty elements that serve no purpose
        await self._remove_empty_elements(soup)
        
        # Fix common HTML issues
        await self._fix_common_issues(soup)
    
    async def _normalize_text_content(self, soup: BeautifulSoup) -> None:
        """
        Normalize whitespace in text content.
        
        Args:
            soup: BeautifulSoup DOM tree
        """
        for element in soup.find_all(string=True):
            if element.parent.name in ['script', 'style']:
                continue
            
            # Normalize whitespace
            normalized = re.sub(r'\s+', ' ', str(element).strip())
            if normalized != str(element):
                element.replace_with(normalized)
    
    async def _remove_empty_elements(self, soup: BeautifulSoup) -> None:
        """
        Remove elements that are empty and serve no purpose.
        
        Args:
            soup: BeautifulSoup DOM tree
        """
        # Elements that can be empty and still meaningful
        self_closing_tags = {'img', 'input', 'br', 'hr', 'meta', 'link', 'area', 'base', 'col', 'embed', 'source', 'track', 'wbr'}
        
        # Find empty elements
        for element in soup.find_all():
            if element.name in self_closing_tags:
                continue
            
            # Check if element is truly empty (no text, no children with content)
            if not element.get_text(strip=True) and not element.find_all():
                # Check if it has important attributes
                important_attrs = {'id', 'class', 'data-*', 'aria-*'}
                has_important_attrs = any(
                    attr in element.attrs for attr in important_attrs
                ) or any(
                    attr.startswith('data-') or attr.startswith('aria-') 
                    for attr in element.attrs
                )
                
                if not has_important_attrs:
                    element.decompose()
    
    async def _fix_common_issues(self, soup: BeautifulSoup) -> None:
        """
        Fix common HTML structure issues.
        
        Args:
            soup: BeautifulSoup DOM tree
        """
        # Fix missing alt attributes on images
        for img in soup.find_all('img'):
            if not img.get('alt'):
                img['alt'] = ''
        
        # Ensure form elements have proper structure
        for form in soup.find_all('form'):
            if not form.get('action'):
                form['action'] = ''
            if not form.get('method'):
                form['method'] = 'GET'
        
        # Add missing type attributes to input elements
        for input_elem in soup.find_all('input'):
            if not input_elem.get('type'):
                input_elem['type'] = 'text'
    
    def get_dom_statistics(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Get statistics about the DOM tree.
        
        Args:
            soup: BeautifulSoup DOM tree
            
        Returns:
            Dictionary with DOM statistics
        """
        stats = {
            'total_elements': len(soup.find_all()),
            'text_nodes': len(soup.find_all(string=True)),
            'tag_counts': {},
            'depth': 0,
            'interactive_elements': 0,
            'form_elements': 0,
            'image_elements': len(soup.find_all('img')),
            'link_elements': len(soup.find_all('a')),
        }
        
        # Count tags
        for element in soup.find_all():
            tag = element.name
            stats['tag_counts'][tag] = stats['tag_counts'].get(tag, 0) + 1
        
        # Count interactive elements
        interactive_tags = {'button', 'input', 'select', 'textarea', 'a'}
        for tag in interactive_tags:
            stats['interactive_elements'] += stats['tag_counts'].get(tag, 0)
        
        # Count form elements
        form_tags = {'form', 'input', 'select', 'textarea', 'button'}
        for tag in form_tags:
            stats['form_elements'] += stats['tag_counts'].get(tag, 0)
        
        # Calculate maximum depth
        stats['depth'] = self._calculate_max_depth(soup)
        
        return stats
    
    def _calculate_max_depth(self, soup: BeautifulSoup) -> int:
        """
        Calculate the maximum depth of the DOM tree.
        
        Args:
            soup: BeautifulSoup DOM tree
            
        Returns:
            Maximum depth as integer
        """
        def get_depth(element, current_depth=0):
            if not hasattr(element, 'children'):
                return current_depth
            
            max_child_depth = current_depth
            for child in element.children:
                if hasattr(child, 'name') and child.name:
                    child_depth = get_depth(child, current_depth + 1)
                    max_child_depth = max(max_child_depth, child_depth)
            
            return max_child_depth
        
        return get_depth(soup)
    
    def validate_html_structure(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Validate HTML structure and identify potential issues.
        
        Args:
            soup: BeautifulSoup DOM tree
            
        Returns:
            Dictionary with validation results
        """
        issues = []
        warnings = []
        
        # Check for missing title
        if not soup.find('title'):
            warnings.append("Missing <title> element")
        
        # Check for missing doctype
        if not any(isinstance(item, type(soup.contents[0])) for item in soup.contents):
            warnings.append("Missing DOCTYPE declaration")
        
        # Check for missing meta charset
        charset_meta = soup.find('meta', attrs={'charset': True}) or \
                     soup.find('meta', attrs={'http-equiv': 'Content-Type'})
        if not charset_meta:
            warnings.append("Missing charset declaration")
        
        # Check for forms without labels
        forms = soup.find_all('form')
        for form in forms:
            inputs = form.find_all('input', attrs={'type': lambda x: x not in ['hidden', 'submit', 'button']})
            for input_elem in inputs:
                input_id = input_elem.get('id')
                label = form.find('label', attrs={'for': input_id}) if input_id else None
                if not label and not input_elem.get('aria-label') and not input_elem.get('aria-labelledby'):
                    warnings.append(f"Input element missing label: {input_elem}")
        
        # Check for images without alt text
        for img in soup.find_all('img'):
            if not img.get('alt') and img.get('alt') != '':
                warnings.append(f"Image missing alt attribute: {img.get('src', 'unknown')}")
        
        # Check for links without text
        for link in soup.find_all('a'):
            if not link.get_text(strip=True) and not link.get('aria-label'):
                warnings.append(f"Link without text or aria-label: {link.get('href', 'unknown')}")
        
        return {
            'is_valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings,
            'total_issues': len(issues),
            'total_warnings': len(warnings)
        }
    
    def extract_metadata(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Extract metadata from HTML document.
        
        Args:
            soup: BeautifulSoup DOM tree
            
        Returns:
            Dictionary with extracted metadata
        """
        metadata = {
            'title': None,
            'description': None,
            'keywords': None,
            'author': None,
            'charset': None,
            'viewport': None,
            'canonical_url': None,
            'open_graph': {},
            'twitter_card': {},
            'language': None,
            'robots': None
        }
        
        # Extract title
        title_elem = soup.find('title')
        if title_elem:
            metadata['title'] = title_elem.get_text(strip=True)
        
        # Extract meta tags
        for meta in soup.find_all('meta'):
            name = meta.get('name', '').lower()
            property_attr = meta.get('property', '').lower()
            content = meta.get('content', '')
            
            if name == 'description':
                metadata['description'] = content
            elif name == 'keywords':
                metadata['keywords'] = content
            elif name == 'author':
                metadata['author'] = content
            elif name == 'viewport':
                metadata['viewport'] = content
            elif name == 'robots':
                metadata['robots'] = content
            elif meta.get('charset'):
                metadata['charset'] = meta.get('charset')
            elif property_attr.startswith('og:'):
                metadata['open_graph'][property_attr[3:]] = content
            elif name.startswith('twitter:'):
                metadata['twitter_card'][name[8:]] = content
        
        # Extract canonical URL
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        if canonical:
            metadata['canonical_url'] = canonical.get('href')
        
        # Extract language
        html_elem = soup.find('html')
        if html_elem:
            metadata['language'] = html_elem.get('lang')
        
        return metadata