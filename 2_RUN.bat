@echo off
title 2M Agency AI — Dang khoi dong...
color 0B
echo.
echo ====================================================
echo   2M MARKETING AGENCY AI
echo   2M Construction LLC - Huntsville, AL
echo ====================================================
echo.
echo Dang khoi dong... Trinh duyet se tu dong mo.
echo De dung: Nhan Ctrl+C hoac dong cua so nay.
echo.

cd /d "%~dp0"
py -m streamlit run 2m_agency_ai.py --server.port 8501 --server.headless false --browser.gatherUsageStats false

pause
