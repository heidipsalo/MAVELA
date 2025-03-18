@echo off 

set fp_activate=C:\Users\hpsalo\AppData\Local\miniconda3\Scripts\activate.bat
set fp_environment="C:\Users\hpsalo\AppData\Local\miniconda3\envs\geo"
set fp_script="C:\Users\hpsalo\Mavela\mavela\scripts_to_generate_input_files"

REM 	Activate the environment.
call %fp_activate% %fp_environment%
REM 	Change directory (for example where your script is located)
cd %fp_script%

python runner.py

mkdir "..\..\flush_03_cd\Release\output_base\"
copy "..\..\flush_03_cd\Release\output\log.txt" "..\..\flush_03_cd\Release\output_base\"
copy "..\..\flush_03_cd\Release\data\input\report.txt" "..\..\flush_03_cd\Release\output_base\"
REM ren "output\log.txt" "log_base.txt"

echo Run again [Enter], quit [CTRL-c]

pause

python runner.py

REM compare the simulation results between the base simulation and the modified setup

python ..\compare_results.py

echo Run again [Enter], quit [CTRL-c]

pause