$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.venv')) { python -m venv .venv }
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if (-not (Test-Path '.env')) { Copy-Item .env.example .env }
Write-Host ''
Write-Host '1) Put your Gemini API key in .env as GOOGLE_API_KEY=...' -ForegroundColor Yellow
Write-Host '2) Build the ChromaDB index: python input.py' -ForegroundColor Yellow
Write-Host '3) Start the app: uvicorn app.main:app --reload' -ForegroundColor Yellow
Write-Host ''
