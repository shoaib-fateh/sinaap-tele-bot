@echo off

:: Activate virtual environment
call sinaap-env\Scripts\activate.bat

:: Start bot in background and save its PID
start "SINAAP_BOT" /min cmd /c "python bot.py"

:loop
:: Wait for keypress (blocking)
choice /c QR /n /m "[Q] Quit bot and close terminal, [R] Restart bot: "
if errorlevel 2 goto restart
if errorlevel 1 goto kill_and_exit

:restart
:: Kill all Python processes (you can refine this to target bot.py specifically)
echo Restarting bot...
taskkill /F /IM python.exe >nul 2>&1
ping 127.0.0.1 -n 3 >nul
start "SINAAP_BOT" /min cmd /c "python bot.py"
goto loop

:kill_and_exit
:: Kill Python and close
 echo Killing bot and closing terminal...
taskkill /F /IM python.exe >nul 2>&1
exit
