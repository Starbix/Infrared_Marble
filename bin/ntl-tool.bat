@echo off
setlocal

REM Get the directory of the current script
for %%I in (.) do set "PROJECT_ROOT=%%~dpI"

REM Go up two directories
cd ..\..

REM Go to the src directory
cd src

REM Execute the python script
python -m main %*

endlocal

