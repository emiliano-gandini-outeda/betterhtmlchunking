# tests/test_tree_regions_system.py
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from betterhtmlchunking.tree_regions_system import TreeRegionsSystem, RegionOfInterest, ReprLengthComparisionBy
from betterhtmlchunking.tree_representation import DOMTreeRepresentation

class TestTreeRegionsSystem:
    """Test BFS-based region detection and chunk boundary logic"""
    
    @pytest.fixture
    def sample_tree(self):
        """Create a sample DOM tree for testing"""
        html_content = """
            <html>
                <body>
                    <div id="short">Short</div>
                    <div id="medium">This is a medium length text node</div>
                    <div id="long">This is a very long text node that should exceed typical chunk boundaries when combined with other content</div>
                </body>
            </html>
        """
        tree_repr = DOMTreeRepresentation(website_code=html_content)
        return tree_repr
    
    @pytest.mark.parametrize("chunk_size,expected_min_regions", [
        (10, 3),   # Very small chunks
        (50, 2),   # Medium chunks  
        (500, 1),  # Large chunks
    ])
    def test_chunk_size_boundaries(self, sample_tree, chunk_size, expected_min_regions):
        """Test region detection with various chunk sizes"""
        regions_system = TreeRegionsSystem(
            tree_representation=sample_tree,
            max_node_repr_length=chunk_size,
            repr_length_compared_by=ReprLengthComparisionBy.TEXT_LENGTH
        )
        
        # Should create at least expected number of regions
        assert len(regions_system.sorted_roi_by_pos_xpath) >= expected_min_regions
        
    @pytest.mark.parametrize("comparison_mode", [
        ReprLengthComparisionBy.TEXT_LENGTH,
        ReprLengthComparisionBy.HTML_LENGTH
    ])
    def test_length_comparison_modes(self, sample_tree, comparison_mode):
        """Test both length comparison modes"""
        regions_system = TreeRegionsSystem(
            tree_representation=sample_tree,
            max_node_repr_length=100,
            repr_length_compared_by=comparison_mode
        )
        
        regions = regions_system.sorted_roi_by_pos_xpath
        assert len(regions) > 0
        
        # Single nodes can exceed max length - that's expected behavior
        for region in regions.values():
            if len(region.pos_xpath_list) == 1:
                # Single nodes can exceed max length
                continue
            # Multi-node regions should respect the limit
            if comparison_mode == ReprLengthComparisionBy.TEXT_LENGTH:
                assert region.repr_length <= 100
    
    def test_roi_creation_logic(self, sample_tree):
        """Test region of interest creation and properties"""
        regions_system = TreeRegionsSystem(
            tree_representation=sample_tree,
            max_node_repr_length=30,
            repr_length_compared_by=ReprLengthComparisionBy.TEXT_LENGTH
        )
        
        regions = regions_system.sorted_roi_by_pos_xpath
        
        for region_idx, region in regions.items():
            assert isinstance(region, RegionOfInterest)
            assert len(region.pos_xpath_list) > 0
            assert region.repr_length > 0
    
    def test_sorted_output(self, sample_tree):
        """Test that regions are sorted by document order"""
        regions_system = TreeRegionsSystem(
            tree_representation=sample_tree,
            max_node_repr_length=50,
            repr_length_compared_by=ReprLengthComparisionBy.TEXT_LENGTH
        )
        
        regions = regions_system.sorted_roi_by_pos_xpath
        
        # Regions should be in document order
        region_xpaths = []
        for region in regions.values():
            region_xpaths.extend(region.pos_xpath_list)
        
        # Verify xpaths maintain document order
        original_xpaths = sample_tree.pos_xpaths_list
        filtered_original = [xpath for xpath in original_xpaths if xpath in region_xpaths]
        # Check that region xpaths are a subsequence of original xpaths in order
        assert all(rx == fo for rx, fo in zip(region_xpaths, filtered_original[:len(region_xpaths)]))
    
    def test_single_large_node(self):
        """Test handling of single node that exceeds chunk size"""
        html_content = "<div>" + "A" * 100 + "</div>"  # Long content
        tree_repr = DOMTreeRepresentation(website_code=html_content)
        
        regions_system = TreeRegionsSystem(
            tree_representation=tree_repr,
            max_node_repr_length=50,  # Smaller than single node
            repr_length_compared_by=ReprLengthComparisionBy.TEXT_LENGTH
        )
        
        # Should still create regions for the large node
        regions = regions_system.sorted_roi_by_pos_xpath
        assert len(regions) > 0
        
    def test_empty_tree_handling(self):
        """Test region detection with empty DOM tree"""
        tree_repr = DOMTreeRepresentation(website_code="")
        
        regions_system = TreeRegionsSystem(
            tree_representation=tree_repr,
            max_node_repr_length=100,
            repr_length_compared_by=ReprLengthComparisionBy.TEXT_LENGTH
        )
        
        # Should handle empty tree gracefully
        assert len(regions_system.sorted_roi_by_pos_xpath) == 0