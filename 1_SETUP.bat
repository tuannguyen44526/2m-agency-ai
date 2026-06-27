@echo off
title 2M Agency AI — Setup
color 0A
echo.
echo ====================================================
echo   2M MARKETING AGENCY AI — SETUP
echo   Cai dat mot lan, dung mai mai
echo ====================================================
echo.

:: Check Python (thu nhieu cach)
python --version >nul 2>&1
if %errorlevel% equ 0 goto :have_python
py --version >nul 2>&1
if %errorlevel% equ 0 goto :have_py
echo [CANH BAO] Chua co Python!
echo.
echo Vui long cai Python tu: https://python.org/downloads
echo Tick chon "Add Python to PATH" khi cai!
echo.
pause
start https://python.org/downloads
exit

:have_py
echo [OK] Python (py launcher) da co san
echo.
echo Dang cai cac thu vien can thiet...
echo.
py -m pip install streamlit anthropic python-dotenv --quiet
goto :done

:have_python
echo [OK] Python da co san
echo.
echo Dang cai cac thu vien can thiet...
echo.
py -m pip install streamlit anthropic python-dotenv --quiet

:done
echo.
echo ====================================================
echo   CAI DAT HOAN TAT!
echo   Chay file "2_RUN.bat" de bat dau
echo ====================================================
echo.
pause
