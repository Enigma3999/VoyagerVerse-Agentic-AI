@echo off
echo Starting VoyagerVerse Demo...
echo.
echo Please wait while the system initializes...

start /b python main_v2.py

echo Waiting for server to start...
timeout /t 5 /nobreak > nul

echo Opening demo interfaces in your browser...
start http://localhost:8000/simple-chat
timeout /t 2 /nobreak > nul
start http://localhost:8000/simple-agent

echo.
echo =====================================================
echo VoyagerVerse Demo is now running!
echo.
echo Tab 1: Traveler Experience (simple-chat)
echo Tab 2: Behind the Scenes (simple-agent)
echo.
echo When you're done, press Ctrl+C to stop the server
echo =====================================================
echo.

cmd /k
