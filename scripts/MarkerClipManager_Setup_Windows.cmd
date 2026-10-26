@echo off
REM Prepara l'ambiente Python per MarkerClipManager su Windows.
REM Serve solo se PySide6 manca o si e' rotto: l'installer lo fa gia' da solo.
setlocal
echo == MarkerClipManager - Python Environment Setup ==
echo.
where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: python not found. Install Python 3 from https://www.python.org/downloads/
    echo and make sure "Add Python to PATH" is checked during setup.
    pause
    exit /b 1
)
python --version
echo Installing/updating PySide6 (requires an internet connection)...
python -m pip install --user --upgrade pip PySide6
if errorlevel 1 (
    echo.
    echo ERROR: PySide6 installation failed. Check your internet connection.
    pause
    exit /b 1
)
echo.
echo Done. Launch from DaVinci Resolve: Workspace ^> Scripts ^> Comp ^> MarkerClipManager
pause
