@echo off
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM streamlit.exe /T 2>nul
timeout /t 2 /nobreak
cd /d "C:\Users\tomng\Downloads\Ai Agentcy for 2M Construction"
call 2_RUN.bat
