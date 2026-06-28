@echo off
cd /d "C:\Users\tomng\Downloads\Ai Agentcy for 2M Construction"
echo === Xoa lock files ===
del /f /q ".git\index.lock" 2>nul
del /f /q ".git\config.lock" 2>nul
del /f /q ".git\objects\maintenance.lock" 2>nul
echo === Config git ===
git config user.email "tuannguyen44526@gmail.com"
git config user.name "Tuan Nguyen"
echo === Set remote ===
git remote remove origin 2>nul
git remote add origin https://github.com/tuannguyen44526/2m-agency-ai.git
git add -A
git commit -m "Fix: use header auth" 2>nul || echo (No changes)
echo === Push voi Authorization header ===
git -c http.extraHeader="Authorization: Basic dHVhbm5ndXllbjQ0NTI2OmdocF90NEluZFdjZnRoYTNGcnZsZVA0UXg5Z2d2MzVMbDYwZ2VDRVM=" -c credential.helper= push -u origin main
echo.
echo === HOAN TAT === https://github.com/tuannguyen44526/2m-agency-ai ===
pause
