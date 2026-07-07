@echo off
cd /d "%~dp0"
py check_ig.py
type ig_check_result.txt
timeout /t 5
