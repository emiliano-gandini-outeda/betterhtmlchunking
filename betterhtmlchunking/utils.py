#!/usr/bin/env python3

import treelib

from betterhtmlchunking.tree_representation import DOMTreeRepresentation


def wanted_xpath(
    xpath: str,
    tag_list_to_filter_out: list[str]
        ) -> bool:
    # Check if any of the unwanted tags are present in the given XPath
    return not any(tag in xpath for tag in tag_list_to_filter_out)


def remove_unwanted_tags(
    tree_representation: DOMTreeRepresentation,
    tag_list_to_filter_out: list[str]
        ):
    for pos_xpath in tree_representation.pos_xpaths_list:
        if wanted_xpath(
            xpath=pos_xpath,
            tag_list_to_filter_out=tag_list_to_filter_out
                ) is False:
            try:
                tree_representation.delete_node(pos_xpath=pos_xpath)
            except treelib.exceptions.NodeIDAbsentError:
                ...
    return tree_representation
