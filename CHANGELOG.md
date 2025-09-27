# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-09-27

### Changed
- **BREAKING**: Moved package from `src/dom_parser/` to `dom_parser/` in project root
- Updated all import paths in examples and tests to use parent directory
- Simplified package structure for easier development and deployment
- Fixed all example scripts to work with new package location
- Updated documentation to reflect new structure

### Fixed
- Resolved lint issues with package imports
- Fixed AttributeError in example scripts with correct API usage
- Updated test suite import paths for new structure
- Corrected class attribute handling in comprehensive examples

## [1.0.0] - 2025-09-21

### Added
- Initial release of DOM Parser & Analyzer component
- Multi-parser HTML processing with BeautifulSoup, lxml, and html5lib
- Interactive element detection and classification
- Semantic content analysis and extraction
- Advanced form analysis with field type classification
- Accessibility analysis with ARIA roles and compliance checking
- Page structure mapping and layout detection
- CSS selector and XPath generation for element targeting
- Browser Controller integration support
- Async/await support for non-blocking operations
- Smart caching for performance optimization
- Comprehensive test suite
- Full documentation and API reference

### Project Structure Reorganization
- Moved core modules to `dom_parser/core/`
- Organized analyzers in `dom_parser/analyzers/`
- Separated data types into `dom_parser/types/`
- Consolidated utilities in `dom_parser/utils/`
- Added proper package structure with `setup.py`
- Created development guidelines and documentation