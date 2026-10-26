"""Cloud entry point for the ATSA gold forecasting app."""
import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).resolve().parent / "gold_price_forecasting" / "app.py"), run_name="__main__")
