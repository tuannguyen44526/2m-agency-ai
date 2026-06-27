@echo off
cd /d "C:\Users\tomng\Downloads\Ai Agentcy for 2M Construction"
echo === Khoi tao Git repo ===
git init
git branch -M main
echo === Them remote origin ===
git remote remove origin 2>nul
git remote add origin https://github.com/tuannguyen44526/2m-agency-ai.git
echo === Add tat ca files ===
git add -A
echo === Commit ===
git commit -m "Initial deploy: 2M Marketing Agency AI"
echo === Push len GitHub ===
git push -u origin main
echo.
echo === HOAN TAT — kiem tra https://github.com/tuannguyen44526/2m-agency-ai ===
pause
