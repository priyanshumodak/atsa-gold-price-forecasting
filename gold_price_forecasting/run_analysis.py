"""Execute the complete notebook and write a report from actual results."""
import os
from pathlib import Path

os.environ.setdefault("IPYTHONDIR", str(Path(__file__).resolve().parent / ".ipython"))
os.environ.setdefault("JUPYTER_RUNTIME_DIR", str(Path(__file__).resolve().parent / ".jupyter_runtime"))

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parent


def main():
    os.chdir(ROOT)
    notebook = nbformat.read(ROOT / "gold_price_forecasting.ipynb", as_version=4)
    client = NotebookClient(notebook, timeout=1800, kernel_name="python3")
    try:
        client.execute(cwd=str(ROOT))
    finally:
        nbformat.write(notebook, ROOT / "gold_price_forecasting.executed.ipynb")
    from make_report import make_report
    make_report()
    print("Analysis complete: outputs/, figures/, models/, report/RESULTS.md")


if __name__ == "__main__":
    main()
