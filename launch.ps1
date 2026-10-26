$ErrorActionPreference = 'Stop'
$projectRoot = Join-Path $PSScriptRoot 'gold_price_forecasting'
$pythonPath = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) {
    throw 'Set up Python first: py -m venv .venv, then .\.venv\Scripts\python.exe -m pip install -r gold_price_forecasting\requirements.txt'
}
& $pythonPath -m streamlit run (Join-Path $PSScriptRoot 'streamlit_app.py')
