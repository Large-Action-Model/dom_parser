"""
Basic tests to verify package structure.
"""

def test_package_structure():
    """Test that the package structure is correct."""
    import os
    
    # Check that main directories exist
    base_path = os.path.dirname(os.path.dirname(__file__))
    
    expected_dirs = [
        "dom_parser", 
        "dom_parser/core",
        "dom_parser/analyzers", 
        "dom_parser/types",
        "dom_parser/utils",
        "tests",
        "examples",
        "docs",
        "scripts"
    ]
    
    for dir_path in expected_dirs:
        full_path = os.path.join(base_path, dir_path)
        assert os.path.exists(full_path), f"Directory {dir_path} does not exist"

def test_init_files_exist():
    """Test that __init__.py files exist in package directories."""
    import os
    
    base_path = os.path.dirname(os.path.dirname(__file__))
    
    init_files = [
        "dom_parser/__init__.py",
        "dom_parser/core/__init__.py", 
        "dom_parser/analyzers/__init__.py",
        "dom_parser/types/__init__.py",
        "dom_parser/utils/__init__.py"
    ]
    
    for init_file in init_files:
        full_path = os.path.join(base_path, init_file)
        assert os.path.exists(full_path), f"Init file {init_file} does not exist"

def test_main_files_exist():
    """Test that main module files exist."""
    import os
    
    base_path = os.path.dirname(os.path.dirname(__file__))
    
    main_files = [
        "dom_parser/core/dom_parser.py",
        "dom_parser/core/element_classifier.py",
        "dom_parser/analyzers/html_analyzer.py",
        "dom_parser/types/dom_data_types.py",
        "setup.py",
        "requirements.txt"
    ]
    
    for main_file in main_files:
        full_path = os.path.join(base_path, main_file)
        assert os.path.exists(full_path), f"Main file {main_file} does not exist"