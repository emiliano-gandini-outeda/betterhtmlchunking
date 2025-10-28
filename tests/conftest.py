# tests/conftest.py
import pytest
import tempfile
import os

@pytest.fixture
def sample_html_content():
    """Provide sample HTML content for tests"""
    return """
        <html>
            <head>
                <title>Test Page</title>
            </head>
            <body>
                <h1>Main Heading</h1>
                <p>This is a paragraph with some text content for testing purposes.</p>
                <div>
                    <span>Nested content</span>
                    <ul>
                        <li>Item 1</li>
                        <li>Item 2</li>
                        <li>Item 3</li>
                    </ul>
                </div>
            </body>
        </html>
    """

@pytest.fixture
def temp_html_file():
    """Create a temporary HTML file for file-based tests"""
    content = """
        <html>
            <body>
                <h1>Temporary File Test</h1>
                <p>Content from temporary file for testing file input functionality.</p>
            </body>
        </html>
    """
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(content)
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    os.unlink(temp_path)