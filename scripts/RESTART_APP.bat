@echo off
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM streamlit.exe /T 2>nul
timeout /t 2 /nobreak
cd /d "%~dp0.."
call 2_RUN.bat
