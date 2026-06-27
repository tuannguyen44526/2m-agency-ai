Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c cd ""%USERPROFILE%\Downloads\Ai Agentcy for 2M Construction"" && py check_ig.py", 0, True
