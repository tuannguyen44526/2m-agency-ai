@echo off
cd /d "C:\Users\tomng\Downloads\Ai Agentcy for 2M Construction"

echo === Kiem tra gh CLI ===
gh --version
if errorlevel 1 (
    echo gh CLI chua cai dat. Thu push bang git...
    goto :GIT_PUSH
)

echo === Kiem tra tai khoan gh ===
gh auth status

echo.
echo === Tao repo moi tren GitHub va push ===
gh repo create 2m-agency-ai --private --description "2M Marketing Agency AI - Huntsville AL" --source . --remote origin --push
if not errorlevel 1 (
    echo.
    echo === HOAN TAT! ===
    echo Kiem tra: https://github.com/$(gh api user --jq .login)/2m-agency-ai
    pause
    exit /b 0
)

:GIT_PUSH
echo === Thu push bang git truc tiep ===
git remote remove origin 2>nul
git remote add origin https://github.com/tuannguyen44526/2m-agency-ai.git
git add -A
git commit -m "Initial deploy: 2M Marketing Agency AI" 2>nul
git push -u origin main
pause
