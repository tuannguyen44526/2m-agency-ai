@echo off
cd /d "C:\Users\tomng\Downloads\Ai Agentcy for 2M Construction"
echo === Git user info ===
git config user.name
git config user.email
echo === Remote URL ===
git remote -v
echo === Test gh CLI ===
gh auth status
echo === DONE ===
pause
