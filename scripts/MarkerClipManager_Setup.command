#!/bin/bash
# ============================================================
# MarkerClipManager_Setup.command
# Prepara l'ambiente Python necessario per eseguire MarkerClipManager.py
# (crea un virtualenv dedicato con PySide6, senza toccare il Python di sistema)
#
# Autore: Tommaso Feraboli — Film Editor
# ============================================================

set -e

VENV_DIR="$HOME/.venvs/resolve_pyside6"

echo "== MarkerClipManager - Python Environment Setup =="
echo ""

if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: python3 not found on this system."
    echo "Install Python 3 from https://www.python.org/downloads/ or with Homebrew"
    echo "(brew install python3), then run this script again."
    read -p "Press ENTER to close..." _ || true
    exit 1
fi

echo "python3 found: $(command -v python3) ($(python3 --version))"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating the virtualenv at $VENV_DIR ..."
    python3 -m venv "$VENV_DIR"
else
    echo "Virtualenv already present at $VENV_DIR"
fi

echo "Installing/updating PySide6 in the virtualenv (requires an internet connection)..."
"$VENV_DIR/bin/pip" install --upgrade pip PySide6

echo ""
echo "Done. You can now launch MarkerClipManager from DaVinci Resolve:"
echo "  Workspace > Scripts > Comp > MarkerClipManager"
echo ""
read -p "Press ENTER to close..." _ || true
