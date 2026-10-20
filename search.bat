@echo off
REM Lets the marker run: search <filename> <method>
REM %~dp0 is this batch file's folder, so it works from any directory.
python "%~dp0search.py" %*
