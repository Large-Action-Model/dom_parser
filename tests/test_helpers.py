"""
Test utilities and helper functions.
"""

import sys
from pathlib import Path

def setup_test_imports():
    """Add parent directory to sys.path for testing."""
    parent_path = Path(__file__).parent.parent
    if str(parent_path) not in sys.path:
        sys.path.insert(0, str(parent_path))

# Sample HTML content for testing
SIMPLE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Simple Test</title>
</head>
<body>
    <h1>Simple Page</h1>
    <p>This is a simple test page.</p>
    <a href="/test">Test Link</a>
    <button onclick="alert('clicked')">Click Me</button>
</body>
</html>
"""

FORM_HTML = """
<!DOCTYPE html>
<html>
<body>
    <form id="test-form" method="post" action="/submit">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required>
        
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>
        
        <label for="email">Email:</label>
        <input type="email" id="email" name="email">
        
        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""

COMPLEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Complex Page</title>
</head>
<body>
    <header role="banner">
        <h1>Complex Test Page</h1>
        <nav role="navigation" aria-label="Main navigation">
            <ul>
                <li><a href="/home">Home</a></li>
                <li><a href="/about">About</a></li>
                <li><a href="/services">Services</a></li>
            </ul>
        </nav>
    </header>
    
    <main role="main">
        <article>
            <h2>Article Title</h2>
            <p>This is an article with some content.</p>
        </article>
        
        <section id="interactive">
            <h3>Interactive Elements</h3>
            <button id="btn1" onclick="doSomething()">Action Button</button>
            <input type="checkbox" id="check1" name="options">
            <label for="check1">Option 1</label>
            
            <select name="dropdown" id="dropdown">
                <option value="1">Option 1</option>
                <option value="2">Option 2</option>
            </select>
        </section>
    </main>
    
    <aside role="complementary">
        <h3>Sidebar</h3>
        <ul>
            <li><a href="/related1">Related Link 1</a></li>
            <li><a href="/related2">Related Link 2</a></li>
        </ul>
    </aside>
    
    <footer role="contentinfo">
        <p>&copy; 2024 Test Company</p>
    </footer>
</body>
</html>
"""