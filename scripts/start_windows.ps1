$ErrorActionPreference = "Stop"
Set-Location "$PSScriptRoot\..\backend"

if (!(Test-Path ".venv")) {
    Write-Host "Creating Python virtual environment..."
    python -m venv .venv
}

$venvPython = ".\.venv\Scripts\python.exe"

Write-Host "Ensuring dependencies are installed..."
& $venvPython -m pip install -r requirements-local.txt

if (!(Test-Path ".env")) {
    Write-Host "Creating .env from .env.example..."
    Copy-Item .env.example .env
}

Write-Host "Starting NyayaAI on http://127.0.0.1:8000 ..."
& $venvPython -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
