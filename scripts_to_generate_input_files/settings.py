import pandas as pd
from download_and_format_input_files_helper import fix_path
import os
from plot_location_on_map import show_location_on_map


def init():
    print("Hi! Welcome to the FLUSH modeling tool!")
    print("I can model your field hydrology for a whole year now")

    global flush_bat_str, dir_flush, input_file_path_plots, plots_folder, location, year, coordinates, veg_season, drain_spacing, slope, temp_folder, input_folder, drain_type, control_level, control_time
    global top_layer_soil, macros_top_soil, bottom_layer_soil, macros_bottom_soil, user_depth, user_soil, open_ditch, open_ditch_dist

    folder_exists = False
    while (folder_exists == False):
        dir_flush = input("Give path to the Flush folder:\n")
        if os.path.exists(dir_flush):
            folder_exists = True
        else:
            print("Folder does not exist. Check the folder path.")
    

    #dir_flush = r"C:\Users\hpsalo\Mavela\flush_03_cd\Release"
    temp_folder, input_folder, plots_folder, output_dir = create_folders(dir_flush)

    input_file_path_plots = fr"{output_dir}\log.txt"
    input_file_path = fix_path(input_folder) + "report.txt"

    flush_bat_str = "mpiexec -n 1 Flush_03.exe data/input/ output/"
    run_bat_file = dir_flush + "\\run.bat"
    with open(run_bat_file, "w") as bat:
        bat.write(flush_bat_str)


    use_file = input("Load user inputs from the file? (Y/N):\n").capitalize()
    if use_file == 'Y':
      
      file_exists = False
      while (file_exists == False):
          input_file_path = input("Give the path to the file:\n")
          if os.path.isfile(input_file_path):
              file_exists = True
          else:
              print("File does not exist. Check the file path.")
      
      open_ditch_dist, open_ditch, location, year, coordinates, veg_season, drain_spacing, slope, drain_type, control_level, control_time, user_depth, user_soil, top_layer_soil, macros_top_soil, bottom_layer_soil, macros_bottom_soil, df_user_inputs = download_input_from_file(input_file_path)
      
      # Print information for the user about the current parameters.
      print("Current parameters are: ")
      print(df_user_inputs)
      
      # Ask user which parameter will be changed.
      change_param = input("What parameter you want to change? (0 - Drain spacing, 1- Drain depth, 2 - Drain type, 3 - Ditch, 4 - Soil type): ")
      if change_param == '0':
          drain_spacing = float(input("Drain spacing in [m]:\n"))
          df_user_inputs["drain_spacing"] = drain_spacing
      elif change_param == '1':
          user_depth = float(input("What is the depth of the subsurface drainage? (0.02m - 1.9m available) \n"))
          df_user_inputs["user_depth"] = user_depth
      elif change_param == '2':
          drain_type = input("Do you want to model control or conventional drainage? (Type control or conventional)\n").capitalize()
          df_user_inputs["drain_type"] = drain_type

          if drain_type == "Control":
            control_level = float(input("What is the control level in the control wells (m)? (0 - surface level, 2.4 - deepest soil layer)\n"))
            if control_level > user_depth:
              pass  # print warning and try again
            df_user_inputs["control_level"] = control_level
            control_time = input("What is drainage control time in month-day format via space? Press Enter when finished.\n")  # list of min one to max three values; time range within the year
            df_user_inputs["control_time"] = control_time
      elif change_param == '3':
          open_ditch = input("Do you have open ditch? (Y/N):\n ").capitalize()
          df_user_inputs["open_ditch"] = open_ditch
          if open_ditch == "Y":
            open_ditch_dist = float(input("What is the distance to open ditch (m)?\n"))
            df_user_inputs["open_ditch_dist"] = open_ditch_dist
      elif change_param == '4':
          user_soil = input("Do you want to use available soil libraries? (Y/N):\n ").capitalize()
          df_user_inputs["user_soil"] = user_soil
          if user_soil == "Y":
            top_layer_soil = input("Select top layer soil type.\n").capitalize()
            df_user_inputs["top_layer_soil"] = top_layer_soil

            macros_top_soil = input("What is the share of macropores of the total pore volume?\n").capitalize()
            df_user_inputs["macros_top_soil"] = macros_top_soil
            
            ksat_top_soil = input("What is the saturated hydraulic conductivity of top soil (give the value in m/h)?")
            df_user_inputs["ksat_top_soil"] = ksat_top_soil

            bottom_layer_soil = input("Select bottom layer soil type.\n").capitalize()
            df_user_inputs["bottom_layer_soil"] = bottom_layer_soil

            macros_bottom_soil = input("What is the share of macropores of the total pore volume?\n").capitalize()
            df_user_inputs["macros_bottom_soil"] = macros_bottom_soil
            
            ksat_bottom_soil = input("What is the saturated hydraulic conductivity of bottom soil (give the value in m/h)?")
            df_user_inputs["ksat_bottom_soil"] = ksat_bottom_soil


    else:
      user_inputs = {}

      year = int(input("Which year do you want to simulate (available years from 1961 - 2023)?\n"))
      user_inputs["year"] = year

      location = input("What was your location (name)?\n")
      user_inputs["location"] = location

      coordinates = str(input("Please, insert the coordinates of your field separated by comma\n in format [N, E] in EPSG:3067, for example 7008018,229667)?\n"))
      user_inputs["coordinates"] = coordinates
      coordinates = coordinates.split(",")

      veg_start = input("Start of growing season in month-day format:\n")
      veg_end = input("End of growing season in month-day format:\n")
      veg_season = [f"{year}-{veg_start}", f"{year}-{veg_end}"]
      user_inputs["veg_start"] = veg_start
      user_inputs["veg_end"] = veg_end

      drain_spacing = float(input("Drain spacing in [m]:\n"))
      user_inputs["drain_spacing"] = drain_spacing

      slope = float(input("Slope [%]:\n"))/100
      user_inputs["slope"] = slope

      user_depth = float(input("What is the depth of the subsurface drainage? (0.02m - 1.9m available) \n"))
      user_inputs["user_depth"] = user_depth

      drain_type = input("Do you want to model control or conventional drainage? (Type control or conventional)\n").capitalize()
      user_inputs["drain_type"] = drain_type

      if drain_type == "Control":
        control_level = float(input("What is the control level in the control wells (m)? (0 - surface level, 2.4 - deepest soil layer)\n"))
        if control_level > user_depth:
          pass  # print warning and try again
        user_inputs["control_level"] = control_level
        control_time = input("What is drainage control time in month-day format via space? Press Enter when finished.\n")  # list of min one to max three values; time range within the year
        user_inputs["control_time"] = control_time

      open_ditch = input("Do you have open ditch? (Y/N):\n ").capitalize()
      user_inputs["open_ditch"] = open_ditch
      if open_ditch == "Y":
        open_ditch_dist = float(input("What is the distance to open ditch (m)?\n"))
        user_inputs["open_ditch_dist"] = open_ditch_dist
      
      ## TODO: replace this part with the three options in LUKE's soil library.
      user_soil = input("Do you want to use available soil libraries? (Y/N):\n ").capitalize()
      user_inputs["user_soil"] = user_soil
      if user_soil == "Y":
        
        print("Available soil types, range of macropores and saturated hydraulic conductivities:\n")
        df_available_soils = pd.read_csv('soil_library/available_soiltypes.csv')
        print(df_available_soils.iloc[:,1:])
        ## TODO: Add here table that shows the available soil types, suggested macroporosities and Ksats.
        top_layer_soil = input("Select top layer soil type.\n").capitalize()
        user_inputs["top_layer_soil"] = top_layer_soil

        macros_top_soil = input("What is the share of macropores of the total pore volume?\n").capitalize()
        user_inputs["macros_top_soil"] = macros_top_soil
        
        ksat_top_soil = input("What is the saturated hydraulic conductivity of top soil (give the value in m/h)?")
        user_inputs["ksat_top_soil"] = ksat_top_soil

        bottom_layer_soil = input("Select bottom layer soil type.\n").capitalize()
        user_inputs["bottom_layer_soil"] = bottom_layer_soil

        macros_bottom_soil = input("What is the share of macropores of the total pore volume?\n").capitalize()
        user_inputs["macros_bottom_soil"] = macros_bottom_soil
        
        ksat_bottom_soil = input("What is the saturated hydraulic conductivity of bottom soil (give the value in m/h)?")
        user_inputs["ksat_bottom_soil"] = ksat_bottom_soil


      df_user_inputs = pd.DataFrame(data=user_inputs, index=[0])
    
    # User inputs will be saved to a report-file. 
    # Also modified parameters will be saved, if parameters are loaded from file.
    df_user_inputs.to_csv(fix_path(input_folder) + "report.txt")
    
    #show_location_on_map(coordinates[1], coordinates[0])

    if user_soil == "N":
      import soil_param_user


def download_input_from_file(input_file_path):
  df = pd.read_csv(input_file_path, index_col=0)

  year = df['year'].values[0]
  location = df['location'].values[0]
  coordinates = df['coordinates'].values[0]
  coordinates = coordinates.split(",")
  veg_start = df['veg_start'].values[0]
  veg_end = df['veg_end'].values[0]
  veg_season = [f"{year}-{veg_start}", f"{year}-{veg_end}"]
  drain_spacing = df['drain_spacing'].values[0]
  slope = df['slope'].values[0]
  drain_type = df['drain_type'].values[0]

  if drain_type == 'Control':
    control_level = df['control_level'].values[0]
    control_time = df['control_time'].values[0]
  else:
    control_level = None
    control_time = None

  open_ditch = df['open_ditch'].values[0]
  if open_ditch == "Y":
    open_ditch_dist = df['open_ditch_dist'].values[0]
  else:
    open_ditch_dist = None

  user_depth = df['user_depth'].values[0]
  user_soil = df['user_soil'].values[0]
  if user_soil == "Y":
    top_layer_soil = df['top_layer_soil'].values[0]
    macros_top_soil = df['macros_top_soil'].values[0]
    bottom_layer_soil = df['bottom_layer_soil'].values[0]
    macros_bottom_soil = df['macros_bottom_soil'].values[0]
  else:
    top_layer_soil = None
    macros_top_soil = None
    bottom_layer_soil = None
    macros_bottom_soil = None

  return (open_ditch_dist, open_ditch, location, year, coordinates, veg_season, drain_spacing, slope, drain_type,
    control_level, control_time, user_depth, user_soil, top_layer_soil,
    macros_top_soil, bottom_layer_soil, macros_bottom_soil, df)


def create_folders(flush_dir):
    temp_dir = fr"{flush_dir}\data\temp"
    input_dir = fr"{flush_dir}\data\input"
    plots_dir = fr"{flush_dir}\data\plots\\"
    output_dir = fr"{flush_dir}\output"

    try:
        os.makedirs(temp_dir)
        os.makedirs(input_dir)
        os.makedirs(plots_dir)
        os.makedirs(output_dir)
    except FileExistsError:
        # directory already exists
        pass
    except OSError as iex:
        print(f"Creation of directories failed! {iex}")

    return temp_dir, input_dir, plots_dir, output_dir
