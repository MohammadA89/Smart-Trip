$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

$PythonPath = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $PythonPath)) {
    python -m venv .venv
}

& $PythonPath -m pip install -r requirements.txt
& $PythonPath -m flask --app app run --host 127.0.0.1 --port 5000
