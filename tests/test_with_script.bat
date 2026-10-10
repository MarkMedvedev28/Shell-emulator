@echo off
rem Stage 2: start script, script with error, missing script
cd /d "%~dp0.."
echo ===== good script
python src\main.py --script scripts\start.txt
echo exit code: %errorlevel%
echo ===== script with error
python src\main.py --script scripts\error.txt
echo exit code: %errorlevel%
echo ===== missing script
python src\main.py --script scripts\no_such_file.txt
echo exit code: %errorlevel%
