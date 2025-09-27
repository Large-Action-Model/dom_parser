# DOM Parser Project

## Development Setup

### Installing in Development Mode

1. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install the package in development mode:**
```bash
pip install -e .
```

3. **Install development dependencies:**
```bash
pip install -e .[dev]
```

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black src/ tests/ examples/
```

### Type Checking

```bash
mypy src/dom_parser/
```

## Project Structure

```
dom_parser/
├── src/
│   └── dom_parser/
│       ├── __init__.py          # Package initialization
│       ├── core/                # Core parsing logic
│       │   ├── __init__.py
│       │   ├── dom_parser.py    # Main parser class
│       │   ├── element_classifier.py
│       │   ├── semantic_extractor.py
│       │   └── structure_mapper.py
│       ├── analyzers/           # Specialized analyzers
│       │   ├── __init__.py
│       │   ├── accessibility_analyzer.py
│       │   ├── form_analyzer.py
│       │   └── html_analyzer.py
│       ├── types/               # Data types and models
│       │   ├── __init__.py
│       │   ├── dom_data_types.py
│       │   └── element_data_types.py
│       └── utils/               # Utility functions
│           ├── __init__.py
│           ├── css_selector_generator.py
│           └── xpath_generator.py
├── tests/                       # Test files
├── examples/                    # Example usage
├── docs/                        # Documentation
├── scripts/                     # Build/deployment scripts
├── requirements.txt
├── setup.py
└── README.md
```