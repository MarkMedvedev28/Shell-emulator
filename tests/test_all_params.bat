@echo off
rem Stage 2: all command-line parameters
cd /d "%~dp0.."
echo ===== no parameters
echo exit | python src\main.py
echo ===== --help
python src\main.py --help
echo ===== --vfs only
echo exit | python src\main.py --vfs C:\my_vfs
echo ===== --vfs and --script
python src\main.py --vfs C:\my_vfs --script scripts\start.txt
echo exit code: %errorlevel%
echo ===== unknown parameter
python src\main.py --bad
