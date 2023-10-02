@echo off
REM if conda doesn't coooperate run before:
REM conda init cmd.exe

REM replace your env
call conda activate  myenv01

REM replace your path
cd G:\Altri computer\Horizon\horizon_workspace
jupyter lab