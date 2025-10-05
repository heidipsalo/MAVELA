@echo off 

set fp_activate=C:\Users\hpsalo\AppData\Local\miniconda3\Scripts\activate.bat
set fp_environment="C:\Users\hpsalo\AppData\Local\miniconda3\envs\geo"
set fp_script="C:\Users\hpsalo\Mavela\mavela\scripts_to_generate_input_files"

REM 	Activate the environment.
call %fp_activate% %fp_environment%
REM 	Change directory (for example where your script is located)
cd %fp_script%

python runner.py

pause