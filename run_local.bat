@echo off
echo ========================================================
echo  Lanna Power Distribution - AI Power Outage Dashboard
echo  ระบบวิเคราะห์ความน่าเชื่อถือระบบไฟฟ้าดับ (SAIFI/SAIDI)
echo ========================================================
echo.
echo [1/2] Checking Node.js environment...
node -v
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not found. Please install Node.js v18+.
    pause
    exit /b %errorlevel%
)
echo.
echo [2/2] Starting Local Production Server on http://localhost:3000 ...
echo Press Ctrl+C to stop the server.
echo.
npx next start -p 3000
