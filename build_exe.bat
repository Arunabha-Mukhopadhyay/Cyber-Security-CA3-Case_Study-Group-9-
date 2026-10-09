@echo off
REM Builds a standalone Windows executable (dist\wazirx_multisig_simulation.exe)
pip install pyinstaller
pyinstaller --onefile wazirx_multisig_simulation.py
echo.
echo Done. Run: dist\wazirx_multisig_simulation.exe
pause
