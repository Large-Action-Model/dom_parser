"""
Test configuration and fixtures for DOM Parser tests.
"""

import pytest
from pathlib import Path

# Test data directory
TEST_DATA_DIR = Path(__file__).parent / "data"

@pytest.fixture
def sample_html():
    """Sample HTML content for testing."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Test Page</title>
    </head>
    <body>
        <header>
            <h1>Welcome to Test Page</h1>
            <nav>
                <ul>
                    <li><a href="/home">Home</a></li>
                    <li><a href="/about">About</a></li>
                    <li><a href="/contact">Contact</a></li>
                </ul>
            </nav>
        </header>
        
        <main>
            <section class="content">
                <h2>Main Content</h2>
                <p>This is a test paragraph with some content.</p>
                
                <form id="contact-form" method="post" action="/submit">
                    <label for="name">Name:</label>
                    <input type="text" id="name" name="name" required>
                    
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email" required>
                    
                    <label for="message">Message:</label>
                    <textarea id="message" name="message" rows="4" cols="50"></textarea>
                    
                    <button type="submit">Send Message</button>
                </form>
            </section>
            
            <aside class="sidebar">
                <h3>Related Links</h3>
                <ul>
                    <li><a href="/blog">Blog</a></li>
                    <li><a href="/news">News</a></li>
                </ul>
            </aside>
        </main>
        
        <footer>
            <p>&copy; 2024 Test Company. All rights reserved.</p>
        </footer>
    </body>
    </html>
    """

@pytest.fixture
def complex_html():
    """Complex HTML content for advanced testing."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Complex Test Page</title>
    </head>
    <body>
        <div class="container">
            <header role="banner">
                <h1>Complex Page</h1>
            </header>
            
            <nav role="navigation" aria-label="Main navigation">
                <ul>
                    <li><a href="#section1">Section 1</a></li>
                    <li><a href="#section2">Section 2</a></li>
                </ul>
            </nav>
            
            <main role="main">
                <article id="section1">
                    <h2>Article Title</h2>
                    <p>Article content goes here.</p>
                </article>
                
                <section id="section2">
                    <h2>Interactive Elements</h2>
                    <button id="btn1" onclick="doSomething()">Click Me</button>
                    <input type="checkbox" id="check1" name="option1">
                    <label for="check1">Option 1</label>
                </section>
            </main>
        </div>
    </body>
    </html>
    """