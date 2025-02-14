```markdown
# betterhtmlchunking

A Python library for intelligently chunking HTML documents into structured, size-limited segments based on DOM tree analysis.

## Overview

This library processes HTML content to split it into semantically coherent chunks while respecting specified size constraints. It analyzes the DOM structure to identify optimal split points, preserving contextual information and document hierarchy.

## Key Features

- Custom DOM tree representation. 
- Configurable chunk size limits (counting by text or HTML length).
- Intelligent region-of-interest detection.
- Dual output formats: HTML and plain text chunks.  
- Preservation of structure relationships.
- Customizable tag filtering.

## Installation

```bash
pip install betterhtmlchunking
```

### Dependencies
- Python 3.12+
- attrs
- treelib
- beautifulsoup4
- parsel-text
- lxml
- attrs-strict

## Usage

### Basic Example

```python
from betterhtmlchunking import DomRepresentation
from betterhtmlchunking.main import ReprLengthComparisionBy
from betterhtmlchunking.main import tag_list_to_filter_out

html_content = """
<html>
  <body>
    <div id="content">
      <h1>Document Title</h1>
      <p>First paragraph...</p>
      <p>Second paragraph...</p>
    </div>
  </body>
</html>
"""

# Create document representation with 20 character chunks.
dom_repr = DomRepresentation(
    MAX_NODE_REPR_LENGTH=20,
    website_code=html_content,
    repr_length_compared_by=ReprLengthComparisionBy.HTML_LENGTH
    # tag_list_to_filter_out=["/head", "/header", "..."]  # By default tag_list_to_filter_out is used.
)
dom_repr.start()

# Render HTML:
for idx in dom_repr.tree_regions_system.sorted_roi_by_pos_xpath:
    print("*" * 50)
    print(f"IDX: {idx}")
    roi_html_render: str =\
        dom_repr.render_system.get_roi_html_render_with_pos_xpath(
            roi_idx=idx
        )
    print(roi_html_render)


# Render text:
for idx in dom_repr.tree_regions_system.sorted_roi_by_pos_xpath:
    print("*" * 50)
    print(f"IDX: {idx}")
    roi_text_render: str =\
        dom_repr.render_system.get_roi_text_render_with_pos_xpath(
            roi_idx=idx
        )
    print(roi_text_render)

```

Render output (HTML):
```
**************************************************
IDX: 0
<h1>
 Document Title
</h1>

**************************************************
IDX: 1
<p>
 First paragraph...
</p>

**************************************************
IDX: 2
<p>
 Second paragraph...
</p>
```

Render output (text):
```
**************************************************
IDX: 0
Document Title

**************************************************
IDX: 1
First paragraph...

**************************************************
IDX: 2
Second paragraph...
```


## Configuration

### Key Parameters
- `MAX_NODE_REPR_LENGTH`: Maximum allowed length for each chunk (in characters)
- `repr_length_compared_by`: Length calculation method:
  - ReprLengthComparisionBy.HTML_LENGTH: HTML source length
  - ReprLengthComparisionBy.TEXT_LENGTH: Rendered text length
- `website_code`: Input HTML content

### Advanced Features
```python
# Access the DOM tree structure
tree = dom_repr.tree_representation.tree

# Get node metadata:
for node in tree.all_nodes():
    if node.data is not None:
        print(f"XPath: {node.identifier}")
        print(f"Text length: {node.data.text_length}")
        print(f"HTML length: {node.data.html_length}")

```

## How It Works

1. **DOM Parsing**  
   - Builds a tree representation of the HTML document.
   - Calculates metadata (text length, HTML length) for each node.

2. **Region Detection**  
   - Uses **Breadth First Search (BFS)** to traverse the DOM tree in a level-order fashion, ensuring that each node is processed systematically.
   - Combines nodes until the specified size limit is reached.
   - Preserves parent-child relationships to maintain contextual integrity.

3. **Chunk Generation**  
   - Creates HTML chunks with original markup.
   - Generates parallel text-only chunks.
   - Maintains chunk order based on document structure.

## Comparison to popular Chunking Techniques

The actual practice (Feb. 2025) is to use **plain-text** or **token-based** chunking strategies, primarily aimed at keeping prompts within certain token limits for large language models. This approach is ideal for quick semantic retrieval or QA tasks on *unstructured* text.

By contrast, **betterhtmlchunking** preserves the **HTML DOM structure**, calculating chunk boundaries based on each node’s text or HTML length. This approach is especially useful when you want to:
- Retain or leverage the **hierarchical relationships** in the HTML (e.g., headings, nested divs)  
- Filter out undesired tags or sections (like `<script>` or `<style>`)  
- Pinpoint exactly where each chunk originated in the document (via positional XPaths)

You can even combine the two techniques if you need both **structured extraction** (via betterhtmlchunking) and **LLM-friendly text chunking** (via LangChain) for advanced tasks such as summarization, semantic search, or large-scale QA pipelines.

## License

MIT License

## Contributing
Feel free to open issues or submit pull requests if you have suggestions or improvements.
