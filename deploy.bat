@echo off

cd /d %~dp0

rem �Ǘ��Ҍ������擾
for /f "tokens=3 delims=\ " %%i in ('whoami /groups^|find "Mandatory"') do set LEVEL=%%i
if NOT "%LEVEL%"=="High" (
    echo �Ǘ��Ҍ�����v��
    powershell -NoProfile -ExecutionPolicy unrestricted -Command "Start-Process %~f0 -Verb runas"
exit
)

echo �V���{���b�N�����N�쐬
echo on
mklink C:\tools\keyhac\config.py .\keyhac\config.py

pause
