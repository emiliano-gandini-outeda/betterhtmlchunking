# tests/test_main.py
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from betterhtmlchunking.main import DomRepresentation
from betterhtmlchunking.tree_regions_system import ReprLengthComparisionBy

class TestMainIntegration:
    """Test the complete DomRepresentation pipeline integration"""
    
    def test_complete_pipeline_execution(self):
        """Test the complete three-phase pipeline"""
        html_content = """
            <html>
                <body>
                    <h1>Test Document</h1>
                    <p>This is a test paragraph with some content.</p>
                </body>
            </html>
        """
        
        dom_repr = DomRepresentation(
            MAX_NODE_REPR_LENGTH=50,
            website_code=html_content,
            repr_length_compared_by=ReprLengthComparisionBy.TEXT_LENGTH
        )
        
        # Execute complete pipeline
        dom_repr.start(verbose=False)
        
        # Verify all components are initialized
        assert dom_repr.tree_representation is not None
        assert dom_repr.tree_regions_system is not None
        assert dom_repr.render_system is not None
        
        # Verify pipeline produced results
        assert len(dom_repr.tree_regions_system.sorted_roi_by_pos_xpath) > 0
    
    @pytest.mark.parametrize("max_length,comparison_mode", [
        (10, ReprLengthComparisionBy.TEXT_LENGTH),
        (100, ReprLengthComparisionBy.HTML_LENGTH),
    ])
    def test_constructor_parameters(self, max_length, comparison_mode):
        """Test different constructor parameter combinations"""
        html_content = "<div>Test content</div>"
        
        dom_repr = DomRepresentation(
            MAX_NODE_REPR_LENGTH=max_length,
            website_code=html_content,
            repr_length_compared_by=comparison_mode
        )
        
        assert dom_repr.MAX_NODE_REPR_LENGTH == max_length
        assert dom_repr.repr_length_compared_by == comparison_mode
    
    def test_tag_filtering_integration(self):
        """Test tag filtering in the complete pipeline"""
        html_content = """
            <html>
                <script>console.log('ignore')</script>
                <body>Actual content</body>
            </html>
        """
        
        dom_repr = DomRepresentation(
            MAX_NODE_REPR_LENGTH=100,
            website_code=html_content,
            repr_length_compared_by=ReprLengthComparisionBy.TEXT_LENGTH,
            tag_list_to_filter_out=["script"]
        )
        
        dom_repr.start(verbose=False)
        
        # Filtered tags should not appear in the tree
        tree_tags = [dom_repr.tree_representation.tree.get_node(xpath).data.bs4_elem.name 
                    for xpath in dom_repr.tree_representation.pos_xpaths_list]
        
        assert "script" not in tree_tags
    
    def test_state_management(self):
        """Verify internal state after each computation phase"""
        html_content = "<div>Test</div>"
        dom_repr = DomRepresentation(
            MAX_NODE_REPR_LENGTH=100,
            website_code=html_content,
            repr_length_compared_by=ReprLengthComparisionBy.TEXT_LENGTH
        )
        
        # Components are initialized during start(), not before
        dom_repr.start(verbose=False)
        
        # After start(), all components should be initialized
        assert dom_repr.tree_representation is not None
        assert dom_repr.tree_regions_system is not None
        assert dom_repr.render_system is not None