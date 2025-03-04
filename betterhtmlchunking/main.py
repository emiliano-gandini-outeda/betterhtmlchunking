#!/usr/bin/env python3

import attrs

from attrs_strict import type_validator

from betterhtmlchunking.utils import remove_unwanted_tags

from betterhtmlchunking.tree_representation import\
    DOMTreeRepresentation

from betterhtmlchunking.tree_regions_system import\
    TreeRegionsSystem
from betterhtmlchunking.tree_regions_system import\
    ReprLengthComparisionBy

from betterhtmlchunking.render_system import\
    RenderSystem

from typing import Optional

import html


tag_list_to_filter_out: list[str] = [
    "/head",
    "/select",
    # "/form",
    "/footer",
    "/svg",
    "/defs",
    "/g",
    "/header",
    "/footer",
    "/script",
    "/style"
]


@attrs.define()
class DomRepresentation:
    # Input:
    MAX_NODE_REPR_LENGTH: int = attrs.field(
        validator=type_validator()
    )
    website_code: str = attrs.field(
        validator=type_validator(),
        repr=False
    )
    repr_length_compared_by: ReprLengthComparisionBy = attrs.field(
        validator=type_validator()
    )

    # Optional inputs:
    tag_list_to_filter_out: Optional[list[str]] = attrs.field(
        validator=type_validator(),
        default=None
    )
    html_unescape: bool = attrs.field(
        validator=type_validator(),
        default=True
    )

    # Result:
    tree_representation: DOMTreeRepresentation = attrs.field(
        validator=type_validator(),
        init=False,
        repr=False
    )
    tree_regions_system: TreeRegionsSystem = attrs.field(
        validator=type_validator(),
        init=False,
        repr=False
    )
    render_system: RenderSystem = attrs.field(
        validator=type_validator(),
        init=False,
        repr=False
    )

    def __attrs_post_init__(self):
        if self.tag_list_to_filter_out is None:
            self.tag_list_to_filter_out = tag_list_to_filter_out

        if self.html_unescape is True:
            self.website_code: str = html.unescape(self.website_code)

    def compute_tree_representation(self):
        self.tree_representation = DOMTreeRepresentation(
            website_code=self.website_code,
        )
        self.tree_representation = remove_unwanted_tags(
            tree_representation=self.tree_representation,
            tag_list_to_filter_out=self.tag_list_to_filter_out
        )
        self.tree_representation.recompute_representation()

    def compute_tree_regions_system(self):
        self.tree_regions_system = TreeRegionsSystem(
            tree_representation=self.tree_representation,
            max_node_repr_length=self.MAX_NODE_REPR_LENGTH,
            repr_length_compared_by=self.repr_length_compared_by
        )

    def compute_render_system(self):
        self.render_system = RenderSystem(
            tree_regions_system=self.tree_regions_system,
            tree_representation=self.tree_representation
        )

    def start(self):
        print("--- DOM REPRESENTATION ---")
        print(" > Computing tree representation:")
        self.compute_tree_representation()
        print(" > Computing tree regions system:")
        self.compute_tree_regions_system()
        print(" > Computing render:")
        self.compute_render_system()
