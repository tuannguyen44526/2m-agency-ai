@echo off
cd /d "C:\Users\tomng\Downloads\Ai Agentcy for 2M Construction"
echo === Push len GitHub voi token ===
git remote remove origin 2>nul
git remote add origin https://tuannguyen44526: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@github.com/tuannguyen44526/2m-agency-ai.git
git add -A
git commit -m "Deploy: 2M Marketing Agency AI" 2>nul
git push -u origin main
echo.
echo === HOAN TAT — https://github.com/tuannguyen44526/2m-agency-ai ===
pause
