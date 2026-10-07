"""Print a Colab notebook as a compact PDF for the quiz.

In Colab, as a new cell at the end of a notebook whose cells have all been run:

    !wget -q -N https://raw.githubusercontent.com/UM-Data-Science-101/data/main/Tools/print_notebook.py
    from print_notebook import print_notebook
    # print_notebook(two_columns=True, summary=True)

The call stays commented out so that Run All checks the notebook without
printing it. The student removes the # to print.

With summary=True the PDF holds the headings of the notebook, so a student
can find each question, and under them the student's own code and every
output. Question text, check cells, empty stubs, error tracebacks and the
tail of very long outputs are left out; the quiz restates whatever text an
item needs. With summary=False every cell prints in full. two_columns=False
prints one wide column. Nothing is re-run.

The master copy is scripts/print_notebook.py in the course materials
repository; Tools/ in the public data repository holds the published copy.

Locally, for testing:
    python print_notebook.py NOTEBOOK.ipynb [--one-column] [--full]
"""

import json
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

QUARTO_VERSION = "1.10.19"
MAX_OUTPUT_LINES = 25

LAYOUT = """---
title: "Notebook printout"
format:
  typst:
    papersize: us-letter
    fontsize: 9pt
    columns: COLUMNS
    highlight-style: none
    margin:
      x: 0.5in
      y: 0.5in
    include-in-header:
      text: |
        #set image(width: IMAGE)
        #show raw: set text(size: 7pt)
        #show raw.where(block: true): set par(justify: false)
---
"""


def trim(text):
    """Keep the first lines of a long output, as a list of lines, which is
    the form Quarto expects."""
    lines = "".join(text).splitlines(keepends=True)
    if len(lines) > MAX_OUTPUT_LINES:
        lines = lines[:MAX_OUTPUT_LINES] + ["...\n"]
    return lines


def curate(nb, two_columns=True, summary=True):
    width = 60 if two_columns else 115
    cells = []
    for cell in nb["cells"]:
        source = "".join(cell["source"])
        lines = [l.strip() for l in source.splitlines() if l.strip()]
        # The notebook's own settings, which would override the layout, and
        # the printing cell itself.
        if cell["cell_type"] == "raw" or source.startswith("---") or "print_notebook" in source:
            continue
        if summary and cell["cell_type"] == "markdown":
            # Keep only the headings, as a list of lines: Quarto drops the
            # line breaks of a single string.
            cell["source"] = [l + "\n\n" for l in lines if l.startswith("#")]
        elif summary and all(l.startswith(("#", "assert")) for l in lines):
            continue  # check cells, live or commented out, and empty stubs
        elif cell["cell_type"] == "code":
            # Wrap long lines, which would otherwise run off the page.
            cell["source"] = [w + "\n" for l in source.splitlines()
                              for w in textwrap.wrap(l, width, subsequent_indent="      ") or [""]]
            if summary:
                outputs = []
                for out in cell.get("outputs", []):
                    if out["output_type"] == "error" or out.get("name") == "stderr":
                        continue
                    if "text" in out:
                        out["text"] = trim(out["text"])
                    elif list(out.get("data", {})) == ["text/plain"]:
                        out["data"]["text/plain"] = trim(out["data"]["text/plain"])
                    outputs.append(out)
                cell["outputs"] = outputs
        if cell["source"]:
            cells.append(cell)
    # The print settings go in a first raw cell, which Quarto reads as front
    # matter.
    layout = (LAYOUT.replace("COLUMNS", "2" if two_columns else "1")
                    .replace("IMAGE", "90%" if two_columns else "50%"))
    nb["cells"] = [{"cell_type": "raw", "metadata": {},
                    "source": layout.splitlines(keepends=True)}] + cells
    return nb


def quarto_command():
    if shutil.which("quarto"):
        return "quarto"
    folder = f"quarto-{QUARTO_VERSION}"
    if not Path(folder).exists():
        url = (f"https://github.com/quarto-dev/quarto-cli/releases/download/"
               f"v{QUARTO_VERSION}/{folder}-linux-amd64.tar.gz")
        subprocess.run(f"wget -q -nc {url} && tar -xzf {folder}-linux-amd64.tar.gz",
                       shell=True, check=True)
    return f"{folder}/bin/quarto"


def render(nb, two_columns=True, summary=True, name="notebook"):
    Path(f"{name}.ipynb").write_text(json.dumps(curate(nb, two_columns, summary)))
    subprocess.run([quarto_command(), "render", f"{name}.ipynb", "--to", "typst"], check=True)
    return f"{name}.pdf"


def print_notebook(two_columns=True, summary=True):
    """Make a PDF of the open Colab notebook and download it."""
    from google.colab import _message, files
    nb = _message.blocking_request("get_ipynb", timeout_sec=60)["ipynb"]
    files.download(render(nb, two_columns, summary))


if __name__ == "__main__":
    source = Path(sys.argv[1])
    print(render(json.loads(source.read_text()),
                 two_columns="--one-column" not in sys.argv,
                 summary="--full" not in sys.argv,
                 name=source.stem + "_print"))
