@echo off
cd /d "C:\Users\tomng\Downloads\Ai Agentcy for 2M Construction"
echo === Xoa lock file neu co ===
del /f /q ".git\index.lock" 2>nul
del /f /q ".git\MERGE_HEAD" 2>nul
echo === Config git ===
git config user.email "tuannguyen44526@gmail.com"
git config user.name "Tuan Nguyen"
echo === Push len GitHub voi token ===
git remote remove origin 2>nul
git remote add origin https://tuannguyen44526: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@github.com/tuannguyen44526/2m-agency-ai.git
git add -A
git commit -m "Fix: FB token moi + them image upload + fix Instagram" 2>nul || echo (Khong co thay doi moi)
git push -u origin main
echo.
echo === HOAN TAT — https://github.com/tuannguyen44526/2m-agency-ai ===
pause
