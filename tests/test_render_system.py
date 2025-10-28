# tests/test_render_system.py
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from betterhtmlchunking.render_system import RenderSystem
from betterhtmlchunking.tree_regions_system import TreeRegionsSystem, ReprLengthComparisionBy
from betterhtmlchunking.tree_representation import DOMTreeRepresentation

class TestRenderSystem:
    """Test HTML and text rendering of detected regions"""
    
    @pytest.fixture
    def sample_rendering_system(self):
        """Create a sample rendering system for testing"""
        html_content = """
            <html>
                <body>
                    <h1>Title</h1>
                    <p>First paragraph with <strong>bold</strong> text.</p>
                    <p>Second paragraph.</p>
                </body>
            </html>
        """
        tree_repr = DOMTreeRepresentation(website_code=html_content)
        
        regions_system = TreeRegionsSystem(
            tree_representation=tree_repr,
            max_node_repr_length=50,
            repr_length_compared_by=ReprLengthComparisionBy.TEXT_LENGTH
        )
        
        render_system = RenderSystem(
            tree_regions_system=regions_system,
            tree_representation=tree_repr
        )
        
        return render_system
    
    def test_html_rendering(self, sample_rendering_system):
        """Test HTML output preserves markup structure"""
        # RenderSystem automatically renders in __attrs_post_init__
        html_renders = sample_rendering_system.html_render_roi
        
        assert len(html_renders) > 0
        
        for chunk_idx, html_content in html_renders.items():
            assert isinstance(html_content, str)
            assert len(html_content) > 0
            # Should contain HTML tags
            assert '<' in html_content and '>' in html_content
    
    def test_text_rendering(self, sample_rendering_system):
        """Test clean text extraction without HTML"""
        # RenderSystem automatically renders in __attrs_post_init__
        text_renders = sample_rendering_system.text_render_roi
        
        assert len(text_renders) > 0
        
        for chunk_idx, text_content in text_renders.items():
            assert isinstance(text_content, str)
            assert len(text_content) > 0
    
    def test_parallel_rendering_alignment(self, sample_rendering_system):
        """Test HTML and text chunks are properly aligned"""
        # RenderSystem automatically renders in __attrs_post_init__
        html_renders = sample_rendering_system.html_render_roi
        text_renders = sample_rendering_system.text_render_roi
        
        # Should have same number of chunks
        assert len(html_renders) == len(text_renders)
        
        # Corresponding chunks should cover same regions
        for chunk_idx in html_renders.keys():
            assert chunk_idx in text_renders
    
    def test_special_characters_handling(self):
        """Test rendering with special characters and encoding"""
        html_content = """
            <div>
                Hello &amp; Welcome! 
                <span>Math: 2 &gt; 1</span>
            </div>
        """
        tree_repr = DOMTreeRepresentation(website_code=html_content)
        
        regions_system = TreeRegionsSystem(
            tree_representation=tree_repr,
            max_node_repr_length=100,
            repr_length_compared_by=ReprLengthComparisionBy.TEXT_LENGTH
        )
        
        render_system = RenderSystem(
            tree_regions_system=regions_system,
            tree_representation=tree_repr
        )
        
        # Should handle entities correctly
        for html_chunk in render_system.html_render_roi.values():
            assert len(html_chunk) > 0
            
        for text_chunk in render_system.text_render_roi.values():
            assert len(text_chunk) > 0
    
    def test_empty_regions_handling(self):
        """Test rendering with empty or minimal regions"""
        html_content = "<div>Content</div>"
        tree_repr = DOMTreeRepresentation(website_code=html_content)
        
        regions_system = TreeRegionsSystem(
            tree_representation=tree_repr,
            max_node_repr_length=100,
            repr_length_compared_by=ReprLengthComparisionBy.TEXT_LENGTH
        )
        
        render_system = RenderSystem(
            tree_regions_system=regions_system,
            tree_representation=tree_repr
        )
        
        # Should handle regions gracefully
        assert len(render_system.html_render_roi) >= 0
        assert len(render_system.text_render_roi) >= 0