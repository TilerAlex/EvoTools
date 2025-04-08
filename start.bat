@echo off
REM Ensure using Python 3.12.x and pip 25.x
py -3.12 -m pip install pip==25.0

REM Install all modules from requirements.txt
py -3.12 -m pip install -r requirements.txt || pause

REM Launch main.pyc from the dist folder
py -3.12 dist\main.pyc || pause

REM Pause at the end to read any remaining messages
pause