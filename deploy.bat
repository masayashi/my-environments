@echo off

cd /d %~dp0

rem 管理者権限を取得
for /f "tokens=3 delims=\ " %%i in ('whoami /groups^|find "Mandatory"') do set LEVEL=%%i
if NOT "%LEVEL%"=="High" (
    echo 管理者権限を要求
    powershell -NoProfile -ExecutionPolicy unrestricted -Command "Start-Process %~f0 -Verb runas"
exit
)

echo シンボリックリンク作成
echo on
mklink C:\tools\keyhac\config.py .\keyhac\config.py

pause
