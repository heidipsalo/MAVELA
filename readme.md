# MAVELA - a computational tool for simulating field water managment
This tool simulated field water managment at any location in Finland. 
The tool uses open data sources to generate metheorological inputs.
User can define the following parameters for the simulated field:
- Year of simulation
- Drainage type
- Drain spacing
- Drain depth
- Slope of the field

# Download and installation

# Windows

# Linux


# Requirements
- Python packages
- MPI library

# Running the MAVELA tool

Windows
double click the run_mavela_tool.bat

Linux
In terminal navigate to Mavela folder and launch the tool with a command
python scripts_to_generate_input_files/runner.py



Give the path to your Flush folder ([your path]/flush_03_cd/Release/)

There are two option to do a simulation: 1) You can create a new simulation input or 2) download input information from a previous simulation.  

New simulation  
1. Select the year you want to simulate (1961-2024)
2. Give the name of your localtion  
2. Give the coordinates of your location in EPSG_3067 (you can search your coordinated by using e.g., Paikkatietoikkuna)  
3. Give the start of the growing season (month-day format)
5. Give the end of the growing season (month-day format)
6. Give the size of the drain spacing (in meters)
7. Give the slope of your field (in %)
8. Give the depth of the subsurface drainage (in meters, min. 0.02 m and max 1.9 m)
9a. Select if you want to simulate conventional or controlled dranage (type conventional/control)
9b. If you selected control, give the 
10a. Select if you want to include open ditch in your simulation.
10b. Give the distance from field to open ditch
11a.Select if you want to use available soil libraries?
11b.If you select no (N), Empty soil files are generated in the input folder. Please add your soil parameters in: 
- geom_layers_01.txt (explain variables needed)
- dt_soillib_geom_01.txt (explain variables needed) 
- dt_soillib_water_01.txt (explain variables needed)
- dt.soillib_crack_01.txt (explain variables needed)
- dt_soillib_solute_01.txt (explain variables needed)
- dt_soillib_heat_01.txt (explain variables needed)
11c. If you select yes (Y)
12. Select if you want to download FMI gridded data now. NOTE that the downloading takes a moment and depends on your internet connection. You do not need to download the gridded dara if you already have downloaded the data for the simulated year previously. You can check if you have that data from Release/data/temp-folder.
13. 

Redo previous simulation
1. Give the path to that report-file (by default it is saved to your Flush directory data/input/report.txt)  
2. 


