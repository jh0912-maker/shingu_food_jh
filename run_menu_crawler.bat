@echo off
title Shingu Menu Notifier
cls
echo.
echo ===========================================
echo   Shingu College Today's Menu Notifier
echo ===========================================
echo.

REM Python script starts here
python menu_crawler.py

echo.
echo ===========================================
echo   Done! Press any key to close the window.
echo ===========================================
pause > nul
