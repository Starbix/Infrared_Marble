REM WARNING:::: !!!!!! UNCHECKED AI SLOP !!!!!!
REM I COULDN'T BE BOTHERED WRITING CMD BATCH SCRIPTS, SO I LET AI TRANSLATE MY BASH SCRIPT!!!
REM IF THIS SCRIPT BRICKS YOUR SYSTEM, I TAKE NO RESPONSIBILITY!!!!!

@echo off
setlocal enabledelayedexpansion

REM Configuration variables
set TIMEOUT=180
set COMPOSEFILE=docker-compose.prod.yaml
set HEALTH_ENDPOINT=http://localhost:8000/health

REM Function to check Docker installation and status
:check_docker
where docker >nul 2>nul
if errorlevel 1 (
    echo Docker not installed. To run the app with docker, please make sure 'docker' and 'docker compose' are installed.
    echo We suggest using Docker Desktop.
    exit /b 1
)

docker compose version >nul 2>nul
if errorlevel 1 (
    echo Docker Compose not installed or not found in PATH.
    exit /b 1
)

docker info >nul 2>nul
if errorlevel 1 (
    echo It appears that Docker is not running. Please start Docker (e.g., Docker Desktop) and try again.
    exit /b 1
)
goto :eof

REM Function to run logs and shutdown on Ctrl+C
:run_app
docker compose -f %COMPOSEFILE% logs --follow
docker compose -f %COMPOSEFILE% down
exit /b 0

REM Main script starts here
call :check_docker

docker compose -f %COMPOSEFILE% up --pull=always -d

echo Waiting for the server to be ready...

set i=0
:waitloop
set /a i+=1
if !i! gtr %TIMEOUT% goto fail

timeout /t 1 /nobreak >nul

curl -i %HEALTH_ENDPOINT% 2>nul | findstr /i "ok" >nul
if not errorlevel 1 (
    echo Server healthy, opening frontend
    call :run_app
    exit /b 0
)
<nul set /p=.

goto waitloop

:fail
echo.
echo Failed to connect in %TIMEOUT% seconds, exiting...
exit /b 1
