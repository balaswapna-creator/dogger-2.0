@echo off
cd /d "C:\Users\DR BALASUBRAMANI\Documents\Projects\dogger-2.0\backend"
call venv\Scripts\activate.bat
python run_waitress.py > logs\nssm_stdout.log 2> logs\nssm_stderr.log