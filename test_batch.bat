@echo off
cd %~dp0
echo === Python Test Batch Script ===
echo Current directory: %cd%
echo.

rem Check Python version
python --version 2>&1
echo.

rem Try to run the simplest test
echo Running test_env.py...
python test_env.py

echo.
echo Exit code: %errorlevel%
echo === Test Complete ===