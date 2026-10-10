@echo off
rem Stage 2: VFS name in the prompt for different paths
cd /d "%~dp0.."
echo ls | python src\main.py --vfs C:\data\first_vfs
echo ls | python src\main.py --vfs D:\second_vfs\
echo ls | python src\main.py --vfs relative\third
