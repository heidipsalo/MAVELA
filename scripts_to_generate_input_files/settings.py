import pandas as pd
from download_and_format_input_files_helper import fix_path
import os


def init():
    print("Hi! Welcome to the FLUSH modeling tool!")
    print("I can model your field hydrology for a whole year now")

    global flush_bat_str, dir_flush, input_file_path_plots, plots_folder, location, year, coordinates, veg_season, drain_spacing, slope, temp_folder, input_folder, drain_type, control_level, control_time
    global top_layer_soil, macros_top_soil, bottom_layer_soil, macros_bottom_soil, user_depth, user_soil, open_ditch, open_ditch_dist

    dir_flush = r"C:\Users\hpsalo\src\Flush_03_CD\Flush_03_CD\Release"
    temp_folder, input_folder, plots_folder, output_dir = create_folders(dir_flush)

    input_file_path_plots = fr"{output_dir}\log.txt"
    input_file_path = fix_path(input_folder) + "report.txt"

    flush_bat_str = "mpiexec -n 1 Flush_03.exe data/input/ output/"
    run_bat_file = dir_flush + "\\run.bat"
    with open(run_bat_file, "w") as bat:
        bat.write(flush_bat_str)


    use_file = input("Load user inputs from the file? (Y/N):\n").capitalize()
    if use_file == 'Y':
      open_ditch_dist, open_ditch, location, year, coordinates, veg_season, drain_spacing, slope, drain_type, control_level, control_time, user_depth, user_soil, top_layer_soil, macros_top_soil, bottom_layer_soil, macros_bottom_soil = download_input_from_file(input_file_path)

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

      user_soil = input("Do you want to use available soil libraries? (Y/N):\n ").capitalize()
      user_inputs["user_soil"] = user_soil
      if user_soil == "Y":
        top_layer_soil = input("What is your top layer soil type (clay, silt and peat soils are available at the moment)?\n").capitalize()
        user_inputs["top_layer_soil"] = top_layer_soil

        macros_top_soil = input("What is your top layer soil macropores size (sizes available high and low)?\n").capitalize()
        user_inputs["macros_top_soil"] = macros_top_soil

        bottom_layer_soil = input("What is your bottom layer soil type (clay, silt and peat soils are available at the moment)?\n").capitalize()
        user_inputs["bottom_layer_soil"] = bottom_layer_soil

        macros_bottom_soil = input("What is your bottom layer soil macropores size (sizes available high and low)?\n").capitalize()
        user_inputs["macros_bottom_soil"] = macros_bottom_soil

      df = pd.DataFrame(data=user_inputs, index=[0])
      df.to_csv(fix_path(input_folder) + "report.txt")

    if user_soil == "N":
      import soil_param_user


def download_input_from_file(input_file_path):
  df = pd.read_csv(input_file_path)

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
    macros_top_soil, bottom_layer_soil, macros_bottom_soil)


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
    except OSError as iex:
        print(f"Creation of directories failed! {iex}")

    return temp_dir, input_dir, plots_dir, output_dir
