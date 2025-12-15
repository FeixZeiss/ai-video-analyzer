#!/usr/bin/env bash
set -e

echo "🔧 Setting up ai-video-analyzer..."

# Check Python
if ! command -v python3 &> /dev/null; then
  echo "Python 3 is required but not found."
  exit 1
fi

# Optional: create virtual environment
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment (.venv)..."
  python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Installation complete."
echo ""
echo "Next steps:"
echo "1) Activate the venv: source .venv/bin/activate"
echo "2) Create secrets/: openai_key.txt, client_secret.json, template.txt"
echo "3) Run: PYTHONPATH=src AIVA_SECRETS_DIR=secrets python scripts/pipeline.py"
