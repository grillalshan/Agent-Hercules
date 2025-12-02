@echo off
echo ==========================================
echo Agent Hercules - Docker Deployment
echo ==========================================
echo.
echo Checking Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed!
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo Docker found!
echo.
echo Starting Agent Hercules with Docker Compose...
echo.
docker-compose up --build

pause
