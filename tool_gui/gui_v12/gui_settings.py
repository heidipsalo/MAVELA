import pandas as pd
from download_and_format_input_files_helper import fix_path
import os
from datetime import datetime


class Settings():
    def create_folders_and_file_paths(self):
        # self.temp_folder = fr"{self.flush_folder}\data\temp"
        # self.input_folder = fr"{self.flush_folder}\data\input"
        # self.plots_folder = fr"{self.flush_folder}\data\plots\\"
        # self.output_folder = fr"{self.flush_folder}\output"

        self.temp_folder = fr"{self.flush_folder}/data/temp"
        self.input_folder = fr"{self.flush_folder}/data/input"
        self.plots_folder = fr"{self.flush_folder}/data/plots/"
        self.output_folder = fr"{self.flush_folder}/output"
        try:
            os.makedirs(self.temp_folder)
            os.makedirs(self.input_folder)
            os.makedirs(self.plots_folder)
            os.makedirs(self.output_folder)
        except OSError as iex:
            print(f"Creation of directories failed! The folders might already exist. {iex}")
        # self.flush_results_file = fr"{self.output_folder}\log.txt"
        self.flush_results_file = fr"{self.output_folder}/log.txt"
        self.settings_file = fix_path(self.input_folder) + "report.txt"

    def create_flush_bat_file(self):
        flush_bat_str = "mpiexec -n 1 Flush_03.exe data/input/ output/"
        run_bat_file = self.flush_folder + "\\run.bat"
        with open(run_bat_file, "w") as bat:
            bat.write(flush_bat_str)

    def convert_to_backend_settings(self):
        self.slope = self.slope/100

        self.veg_start = datetime.strptime(self.veg_start, "%d.%m").strftime("%m-%d")
        self.veg_stop = datetime.strptime(self.veg_stop, "%d.%m").strftime("%m-%d")
        self.veg_season = [f"{self.year}-{self.veg_start}", f"{self.year}-{self.veg_stop}"]

        if self.drain_type == 'Control Drainage':
            control_start = datetime.strptime(self.control_time[0], "%d.%m").strftime("%m.%d")
            control_end = datetime.strptime(self.control_time[1], "%d.%m").strftime("%m.%d")
            self.control_time = f"{control_start} {control_end}"

    def load_settings_from_file(self):
        df = pd.read_csv(self.settings_file)

        self.year = df['year'].values[0]
        self.location_name = df['location'].values[0]
        self.coordinates = [df['coordinates'].values[0], df['coordinates'].values[1]]
        self.veg_start = df['veg_start'].values[0]
        self.veg_stop = df['veg_stop'].values[0]
        self.veg_season = [f"{self.year}-{self.veg_start}", f"{self.year}-{self.veg_stop}"]
        self.drain_spacing = df['drain_spacing'].values[0]
        self.slope = df['slope'].values[0]
        self.drain_type = df['drain_type'].values[0]

        if self.drain_type == 'Control Drainage':
            self.control_level = df['control_level'].values[0]
            self.control_time = df['control_time'].values[0]
        else:
            self.control_level = None
            self.control_time = None

        self.is_open_ditch = df['is_open_ditch'].values[0]
        if self.is_open_ditch == "On":
            self.open_ditch_dist = df['open_ditch_dist'].values[0]
        else:
            self.open_ditch_dist = None

        self.user_depth = df['user_depth'].values[0]
        self.is_custom_soils = df['is_custom_soils'].values[0]
        if not self.is_custom_soils:
            self.top_soil_layer = df['top_soil_layer'].values[0]
            self.top_soil_macros = df['top_soil_macros'].values[0]
            self.bottom_soil_layer = df['bottom_soil_layer'].values[0]
            self.bottom_soil_macros = df['bottom_soil_macros'].values[0]
        else:
            self.top_soil_layer = None
            self.top_soil_macros = None
            self.bottom_soil_layer = None
            self.bottom_soil_macros = None

    def validate(self):
        try:
            if self.flush_folder == '':
                raise ValueError('Flush folder path is not provided!')
            try:
                self.year = int(self.year)
            except ValueError as verr:
                return 'Modeling year must be an integer number. Please fix year input.'
            try:
                self.coordinates = [float(self.coordinates[0]), float(self.coordinates[1])]
            except ValueError as verr:
                return 'Field coordinates must be float numbers. Please fix coordinates input.'
            try:
                self.drain_spacing = float(self.drain_spacing)
            except ValueError as verr:
                return 'Drain spacing must be a float number. Please fix drain spacing input.'
            try:
                self.user_depth = float(self.user_depth)
            except ValueError as verr:
                return 'Depth of subsurface drainage must be a float number. Please fix depth of subsurface drainage input.'
            try:
                self.slope = float(self.slope)
            except ValueError as verr:
                return 'Slope must be a float number. Please fix slope input.'
            if self.drain_type == 'Control Drainage':
                try:
                    self.control_level = float(self.control_level)
                except ValueError as verr:
                    return 'Control level must be a float number. Please fix control level input.'
            else:
                self.control_level = None
                self.control_time = None
            if self.is_open_ditch == 'On':
                try:
                    self.open_ditch_dist = float(self.open_ditch_dist)
                except ValueError as verr:
                    return 'Distance to open ditch must be a float number. Please fix distance to open ditch input.'
            else:
                self.open_ditch_dist = None
        except ValueError as verr:
            return verr.args[0]
        return 1

    def define_weather_start_stop_download_time(self):
        self.start_time = f"{self.year}-01-01 00:00"
        self.end_time = f"{self.year}-12-31 23:00"

    def create_settings_file(self):
        user_inputs = {}
        user_inputs["year"] = self.year
        user_inputs["location"] = self.location_name
        user_inputs["coordinates"] = self.coordinates
        user_inputs["veg_start"] = self.veg_start
        user_inputs["veg_stop"] = self.veg_stop
        user_inputs["drain_spacing"] = self.drain_spacing
        user_inputs["slope"] = self.slope
        user_inputs["user_depth"] = self.user_depth
        user_inputs["drain_type"] = self.drain_type

        if self.drain_type == 'Control Drainage':
            user_inputs["control_level"] = self.control_level
            user_inputs["control_time"] = self.control_time

        user_inputs["is_open_ditch"] = self.is_open_ditch
        if self.is_open_ditch == 'On':
            user_inputs["open_ditch_dist"] = self.open_ditch_dist

        user_inputs["is_custom_soils"] = self.is_custom_soils
        if not self.is_custom_soils:
            user_inputs["top_soil_layer"] = self.top_soil_layer
            user_inputs["top_soil_macros"] = self.top_soil_macros
            user_inputs["bottom_soil_layer"] = self.bottom_soil_layer
            user_inputs["bottom_soil_macros"] = self.bottom_soil_macros

        df = pd.DataFrame(data=user_inputs)
        df.to_csv(self.settings_file, index=False)
