@echo off

REM Content-Type Fix Tool
REM Date: 2024

echo ==========================
echo   Content-Type Fix Tool   
echo ==========================
echo.
echo Preparing fix environment...

REM Try to open the fixed AI report page
start %cd%\fixed_ai_report.html

echo.
echo The fixed page should now open automatically.
echo Please use this page for file uploads.

echo.
echo ==========================
echo Fix operation completed!
echo ==========================
echo.
echo If you still need help, please refer to:
echo - CONTENT_TYPE_FIX_README.md

echo.
pause
