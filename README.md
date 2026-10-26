# Gold Price Prediction Mini Project

The complete project is in [gold_price_forecasting/](gold_price_forecasting/README.md).

The analysis has been executed on real Yahoo Finance GC=F data. Read the generated
[results report](gold_price_forecasting/report/RESULTS.md) and open the
[executed notebook](gold_price_forecasting/gold_price_forecasting.executed.ipynb).

Launch the app from PowerShell:

```powershell
.\.venv\Scripts\python.exe -m streamlit run gold_price_forecasting\app.py
```

Or run `launch.ps1`. See the inner README for installation on another machine.
Team: Priyanshu Modak (I080), Vishesh Dokania (I019), Parth Zanwar (I074). Review your interpretation before submission.

## Deploy

Cloud entry point: `streamlit_app.py`; Python 3.12.11; runtime dependencies: root `requirements.txt`.
The committed real dataset allows the app to run when Yahoo Finance is unavailable.

**Render:** connect this GitHub repository and create a Blueprint using `render.yaml`.
It configures a free Python web service and the Streamlit health endpoint.

**Streamlit Community Cloud:** choose this repository, branch `main`, entry point
`streamlit_app.py`, and Python 3.12.

Local cloud-entry-point check:

```powershell
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

## Professor presentation pack

[PowerPoint with speaker notes](presentation/ATSA_Gold_Presentation.pptx), [slides PDF](presentation/ATSA_Gold_Presentation.pdf), and [full walkthrough](presentation/FULL_PROJECT_WALKTHROUGH.pdf) cover the actual results, code, demo, model combinations and 42 viva answers. See [pack contents](presentation/README.md).
