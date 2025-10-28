# tests/test_utils.py
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from betterhtmlchunking.utils import remove_unwanted_tags
from betterhtmlchunking.tree_representation import DOMTreeRepresentation

class TestUtils:
    """Test utility functions"""
    
    def test_remove_unwanted_tags(self):
        """Test tag filtering utility"""
        html_content = """
            <html>
                <script>console.log('test')</script>
                <body>Actual content</body>
            </html>
        """
        
        tree_repr = DOMTreeRepresentation(website_code=html_content)
        
        original_count = len(tree_repr.pos_xpaths_list)
        
        # Filter multiple tags
        filtered_tree = remove_unwanted_tags(
            tree_representation=tree_repr,
            tag_list_to_filter_out=["script"]
        )
        
        filtered_count = len(filtered_tree.pos_xpaths_list)
        
        # Should have fewer nodes after filtering
        assert filtered_count < original_count
        
        # Filtered tags should be removed
        filtered_tags = [filtered_tree.tree.get_node(xpath).data.bs4_elem.name 
                        for xpath in filtered_tree.pos_xpaths_list]
        
        assert "script" not in filtered_tags
    
    def test_empty_tag_list_handling(self):
        """Test tag filtering with empty filter list"""
        html_content = "<div>Content</div>"
        
        tree_repr = DOMTreeRepresentation(website_code=html_content)
        
        original_count = len(tree_repr.pos_xpaths_list)
        
        # Empty filter list should not change anything
        filtered_tree = remove_unwanted_tags(
            tree_representation=tree_repr,
            tag_list_to_filter_out=[]
        )
        
        assert len(filtered_tree.pos_xpaths_list) == original_count
    
    def test_nonexistent_tag_filtering(self):
        """Test filtering tags that don't exist in document"""
        html_content = "<div>Content</div>"
        
        tree_repr = DOMTreeRepresentation(website_code=html_content)
        
        original_count = len(tree_repr.pos_xpaths_list)
        
        # Filter tags that don't exist
        filtered_tree = remove_unwanted_tags(
            tree_representation=tree_repr,
            tag_list_to_filter_out=["nonexistent", "fake"]
        )
        
        # Should not change anything
        assert len(filtered_tree.pos_xpaths_list) == original_count

