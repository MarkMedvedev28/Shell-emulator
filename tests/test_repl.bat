@echo off
rem Stage 1: REPL demo with all commands and errors
cd /d "%~dp0.."
(
echo ls -l $HOME
echo cd "my folder" ${USERNAME}
echo ls
echo unknown_command arg
echo ls "unclosed
echo exit 1 2
echo exit abc
echo exit 3
) | python src\main.py
echo exit code: %errorlevel%
