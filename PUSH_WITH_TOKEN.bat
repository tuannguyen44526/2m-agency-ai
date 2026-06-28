@echo off
cd /d "C:\Users\tomng\Downloads\Ai Agentcy for 2M Construction"
echo === Xoa lock files ===
del /f /q ".git\index.lock" 2>nul
del /f /q ".git\config.lock" 2>nul
echo === Luu credentials vao git-credentials ===
echo https://tuannguyen44526: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@github.com> "%USERPROFILE%\.git-credentials"
echo === Config git ===
git config user.email "tuannguyen44526@gmail.com"
git config user.name "Tuan Nguyen"
git config credential.helper store
git config --global credential.helper store
echo === Set remote ===
git remote remove origin 2>nul
git remote add origin https://github.com/tuannguyen44526/2m-agency-ai.git
echo === Commit va Push ===
git add -A
git commit -m "Fix: store credential approach" 2>nul || echo (No changes)
set GIT_TERMINAL_PROMPT=0
git push -u origin main
echo.
echo === HOAN TAT === https://github.com/tuannguyen44526/2m-agency-ai ===
pause
