import pandas as pd
import numpy as np

from generate_default_data_files_helper import generate_defaults, remove_end_blank_line, generate_rootdepths
from download_and_format_input_files_helper import (
    extend_from_daily_to_hourly_by_copy, extend_from_daily_to_hourly_by_divide,
    create_list_of_files_in_directory, fix_path, calculate_wind_speed_at_two_meters,
    replace_empty_data_entries_with_mean, calc_percent_unavailable_data
)
from pet_calculation_helper import net_and_pet
from gridded_data import process_and_save_gridded_data

from geopackage_area import GeopackageArea
from soil_param import SoilParam
from mod_files import ModFiles
from geopackage_to_flush import GeopackageToFlush


class PreProcess():
    def __init__(self, settings):
        files, filenames = create_list_of_files_in_directory(settings.temp_folder, file_type=f"{settings.year}.nc")

        if str(settings.year) not in filenames[0]:
            raise RuntimeError("Please download new gridded data. Your existing data \
                correspond to a different year.")

        daily_humid_df, daily_temp_df, daily_temp_df, daily_glod_rad_df = process_and_save_gridded_data(files, filenames, settings)

        weather_daily_data = pd.read_csv(fix_path(settings.temp_folder)+f"weather_data_{settings.year}.csv")
        no_data = calc_percent_unavailable_data(weather_daily_data)

        weather_daily_data = replace_empty_data_entries_with_mean(weather_daily_data)

        # Add wind speed data
        extended_df = extend_from_daily_to_hourly_by_copy(
            calculate_wind_speed_at_two_meters(weather_daily_data["Wind speed"]),
            input_data_column_name = None
        )
        out_txt = fix_path(settings.input_folder) + 'dt_wind_01.txt'
        extended_df.to_csv(out_txt, sep='\t', header=False)
        remove_end_blank_line(out_txt)

        # Generate files with default data
        generate_defaults(extended_df, fix_path(settings.input_folder), settings)

        # Generate dt_rootdepths_01.txt
        generate_rootdepths(
            extended_df,
            fix_path(settings.input_folder),
            settings.veg_season,
            global_start_time = settings.start_time
        )

        print("Calculating net radiation and PET...")

        # Make sure that all pandas DataFrames have the same column names for `net_and_pet()`:
        wind_speed_df = pd.DataFrame(
            index=daily_temp_df.index,
            data=np.array(weather_daily_data["Wind speed"]),
            columns=['daily_accums']
        )
        net, long_in, pet = net_and_pet(
            settings.coordinates,
            daily_humid_df,
            daily_temp_df,
            daily_glod_rad_df,
            wind_speed_df
        )

        net.to_csv(fix_path(settings.temp_folder)+'net.csv', date_format='%Y-%m-%d')
        long_in.to_csv(fix_path(settings.temp_folder)+'long_in.csv', date_format='%Y-%m-%d')
        pet.to_csv(fix_path(settings.temp_folder)+'pet.csv', date_format='%Y-%m-%d')

        extended_df = extend_from_daily_to_hourly_by_divide(long_in)
        out_txt = fix_path(settings.input_folder) + 'dt_radiat_long_01.txt'
        extended_df.to_csv(out_txt, sep='\t', header=False)
        remove_end_blank_line(out_txt)

        extended_df = extend_from_daily_to_hourly_by_divide(pet)
        out_txt = fix_path(settings.input_folder) + 'dt_pet_01.txt'
        extended_df.to_csv(out_txt, sep='\t', header=False)
        remove_end_blank_line(out_txt)

        GeopackageArea(settings)
        if not settings.is_custom_soils:
            SoilParam(settings)
        ModFiles(settings)
        GeopackageToFlush(settings)
