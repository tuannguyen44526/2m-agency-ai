@echo off
title Push code len GitHub
cd /d "%~dp0.."
echo ================================================
echo   DAY CODE MOI LEN GITHUB (2m-agency-ai)
echo ================================================
echo.
echo === Dong GitHub Desktop + xoa khoa git (neu co) ===
taskkill /F /IM GitHubDesktop.exe /T 2>nul
timeout /t 2 /nobreak >nul
del /f /q ".git\index.lock" 2>nul
echo.
git add -A
git commit -m "Update: cau truc moi + sua loi ThinkingBlock/re/website + Sonnet 5 + scripts"
echo.
echo === Dang push len GitHub ===
git push origin main
if errorlevel 1 (
    echo.
    echo Push truc tiep that bai — thu qua GitHub CLI...
    gh auth setup-git 2>nul
    git push origin main
)
echo.
echo === XONG! Kiem tra: https://github.com/tuannguyen44526/2m-agency-ai ===
pause
