@echo off
cd /d "C:\Users\tomng\Downloads\Ai Agentcy for 2M Construction"
echo === Xoa lock files ===
del /f /q ".git\index.lock" 2>nul
del /f /q ".git\config.lock" 2>nul
del /f /q ".git\objects\maintenance.lock" 2>nul
echo === Xoa GitHub credentials khoi Windows Credential Manager ===
cmdkey /delete:git:https://github.com 2>nul
cmdkey /delete:git:https://tuannguyen44526@github.com 2>nul
echo === Config git ===
git config user.email "tuannguyen44526@gmail.com"
git config user.name "Tuan Nguyen"
git config credential.helper ""
echo === Set remote voi token moi ===
git remote remove origin 2>nul
git remote add origin https://tuannguyen44526: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@github.com/tuannguyen44526/2m-agency-ai.git
git add -A
git commit -m "Fix: disable credential helper for token push" 2>nul || echo (No new changes)
git -c credential.helper= push -u origin main
echo.
echo === HOAN TAT === https://github.com/tuannguyen44526/2m-agency-ai ===
pause
