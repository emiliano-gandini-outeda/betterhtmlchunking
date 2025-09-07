#!/usr/bin/env python3

import sys

import typer
from .main import DomRepresentation, ReprLengthComparisionBy

app = typer.Typer(help="Chunk HTML documents from the command line")

@app.command()
def chunk(
    max_length: int = typer.Option(
        32768,
        "--max-length",
        "-l",
        help="Maximum length for a region of interest",
    ),
    chunk_index: int = typer.Option(
        0,
        "--chunk-index",
        "-c",
        help="Index of the chunk to output",
    ),
    by_text: bool = typer.Option(
        False,
        "--text",
        help="Compare length using text instead of HTML",
    ),
):
    """Read HTML from stdin and output the selected chunk as HTML."""
    html_input = sys.stdin.read()
    compare = ReprLengthComparisionBy.TEXT_LENGTH if by_text else ReprLengthComparisionBy.HTML_LENGTH
    dom = DomRepresentation(
        MAX_NODE_REPR_LENGTH=max_length,
        website_code=html_input,
        repr_length_compared_by=compare,
    )
    dom.start(verbose=False)
    chunk_html = dom.render_system.html_render_roi.get(chunk_index, "")
    typer.echo(chunk_html)

if __name__ == "__main__":
    app()
