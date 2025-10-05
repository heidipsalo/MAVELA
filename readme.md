# MAVELA - a computational tool for simulating field water management
This tool simulated field water management at any location in Finland. 
The tool uses open data sources to generate meteorological inputs.
User can define the following parameters for the simulated field:
- Year of simulation
- Drainage type
- Drain spacing
- Drain depth
- Slope of the field


# Requirements
- Python packages:
	- customtkinter==5.2.2
	- future==0.18.3
	- numpy==1.24.2
	- pandas==2.0.2
	- datetime==5.4
	- geopandas==0.14.3
	- rasterio==1.3.9
	- shapely==2.0.2
	- plotly==5.15.0
	- matplotlib==3.6.3
	- pyproj==3.6.1
	- netcdf4==1.6.5
	- cftime==1.6.3
	- requests==2.28.2
	- defusedxml==0.7.1
- [Flush-model](https://github.com/heidipsalo/Flush)

# Running the MAVELA tool (Windows)

Open run_mavela_tool.bat in text editor (e.g., Notepad++)
Set correct paths for 
- fp_activate ([your path]\AppData\Local\miniconda3\Scripts\activate.bat)
- fp_environment ([your path]\AppData\Local\miniconda3\envs\geo)
- fp_script ([your path]\mavela\scripts_to_generate_input_files)
double click the run_mavela_tool.bat


Give the path to your Flush folder ([your path]/flush_03_cd/Release/)

There are three option to do a simulation: 1) You can create a new simulation input, 2) download input information from a previous simulation, or 3) run multiple simulations and compare results.  

## New simulation  
1. Select the year you want to simulate (1961-2024)
2. Give the name of your location  
2. Give the coordinates of your location in EPSG_3067 (you can search your coordinated by using e.g., Paikkatietoikkuna)  
3. Give the start of the growing season (month-day format)
5. Give the end of the growing season (month-day format)
6. Give the size of the drain spacing (in meters)
7. Give the slope of your field (in %)
8. Give the depth of the subsurface drainage (in meters, min. 0.02 m and max 1.9 m)
9. Select if you want to simulate conventional or controlled drainage (type conventional/control)
9. If you selected control, give the control period (MM-DD MM-DD)
10. Select if you want to include open ditch in your simulation.
10. Give the distance from field to open ditch
11.Select if you want to use available soil libraries?
11.If you select no (N), Empty soil files are generated in the input folder. Please add your soil parameters in: 
- geom_layers_01.txt 
- dt_soillib_geom_01.txt 
- dt_soillib_water_01.txt 
- dt.soillib_crack_01.txt 
- dt_soillib_solute_01.txt 
- dt_soillib_heat_01.txt 
11. If you select yes (Y), you can choose from the given options the soil type for top soil (above the drain depth) and bottom soil (below the drain depth).
12. Select if you want to download FMI gridded data now. NOTE that the downloading takes a moment and depends on your internet connection. You do not need to download the gridded data if you already have downloaded the data for the simulated year previously. You can check if you have that data from Release/data/temp-folder.
13. The Flush simulation will be run automatically after the input files are created based on your choices made for the model run. 
14. After the model run is finished, you can determine which variables you want to plot by following the instructions given by the tool.
## Redo previous simulation
1. Give the path to the report-file (by default it is saved to your Flush directory data/input/report.txt)  
2. Select what parameter you want to change from the previous simulation round.
3. Select if you want to download FMI gridded data now. NOTE that the downloading takes a moment and depends on your internet connection. You do not need to download the gridded data if you already have downloaded the data for the simulated year previously. You can check if you have that data from Release/data/temp-folder.
4. The Flush simulation will be run automatically after the input files are created based on your choices made for the model run. 
5. After the model run is finished, you can determine which variables you want to plot by following the instructions given by the tool.
## Run multiple simulations and compare results
1. Open run_mavela_tool_serial.bat in text editor (e.g., Notepad++)
2. Set correct paths for 
- fp_activate ([your path]\AppData\Local\miniconda3\Scripts\activate.bat)
- fp_environment ([your path]\AppData\Local\miniconda3\envs\geo)
- fp_script ([your path]\mavela\scripts_to_generate_input_files)
- Flush Release-folder ([your path]\flush_03_cd\Release\)
3. Double click the run_mavela_tool_serial.bat
4. Follow the New simulation instructions.
5. Do not close the command prompt window, you are asked if you want to run the tool again: Press Enter for running the tool again.
6. You can create a new simulation with new parameters or redo the previous simulation with changing the selected parameter from the previous simulation. 
7. After the second simulation is done the tool produces graphs showing results from both simulations.

