import pandas as pd
import numpy as np
import time
from generate_default_data_files_helper import generate_defaults, remove_end_blank_line, generate_rootdepths
from download_and_format_input_files_helper import (extend_from_daily_to_hourly_by_copy, extend_from_daily_to_hourly_by_divide,
    create_list_of_files_in_directory, fix_path,
    download_weather_data, calculate_wind_speed_at_two_meters, replace_empty_data_entries_with_mean,
    calc_percent_unavailable_data)
from pet_calculation_helper import net_and_pet
import settings
from gridded_data import download_gridded_data, process_and_save_gridded_data
from subprocess import Popen


NO_DATA_WEATHER_THRESHOLD = 20  # percentage of missing weather data (Wind speed) from FMI
FMI_STATION_LIMIT = 50

def main():
    settings.init()  # asking user for input parameters

    download_now = input("Do you want to download FMI gridded data now? (Y/N): ").capitalize()
    if download_now == 'Y':
        download_gridded_data()  # downloading gridded data

    files, filenames = create_list_of_files_in_directory(settings.temp_folder, file_type=f"{settings.year}.nc")

    # conducting check on the gridded data availability for requested year
    if download_now != 'Y' and str(settings.year) not in filenames[0]:
        raise RuntimeError("Please download new gridded data. Your existing data \
            correspond to a different year.")

    # extracting data for requested location
    daily_humid_df, daily_temp_df, daily_temp_df, daily_glod_rad_df = process_and_save_gridded_data(files, filenames)

    # generating time stamp for calendar year
    start_time = f"{settings.year}-01-01 00:00"
    end_time = f"{settings.year}-12-31 23:00"

    # downloading station based weather data (wind)
    if (download_now == 'Y' or download_now == 'N'):
        fmi_attempts = 0
        while fmi_attempts <= FMI_STATION_LIMIT:
            if fmi_attempts == FMI_STATION_LIMIT:
                raise RuntimeError("No data available for searched weather stations!")

            print(f"Downloading wind data from FMI...(attempt #{fmi_attempts+1})")
            start_downloading_time = time.time()
            try:
                weather_daily_data = download_weather_data(
                    settings.coordinates,
                    start_time, end_time,
                    time_format = "%Y-%m-%d %H:%M",
                    nearest_station = fmi_attempts
                )
            except IndexError:
                print("No data available for this weather station!\n")
                fmi_attempts += 1
                continue

            end_downloading_time = time.time()
            print("Weather data downloaded in {} s".format(end_downloading_time-start_downloading_time))

            # check time series length for gridded and station based data
            if weather_daily_data.index.size != daily_temp_df.index.size:
                print("Gridded FMI and weather data have different number of total days!\n")
                fmi_attempts += 1
                continue
            break
        # calculating data gaps
        no_data_first = calc_percent_unavailable_data(weather_daily_data)

        # comparing data gaps with the threshold level
        if no_data_first > NO_DATA_WEATHER_THRESHOLD:
            print("Downloading weather data from FMI again using the next closest station...")
            start_downloading_time = time.time()
            weather_daily_data_second = download_weather_data(
                settings.coordinates,
                start_time, end_time,
                time_format="%Y-%m-%d %H:%M",
                nearest_station=fmi_attempts+1
            )
            end_downloading_time = time.time()
            print("Weather data downloaded in {} s".format(end_downloading_time-start_downloading_time))

            no_data_second = calc_percent_unavailable_data(weather_daily_data_second)
            if no_data_second > no_data_first:
                print("Next closest station have even less data available. Switching back to the previous station.")
            else:
                weather_daily_data = weather_daily_data_second

        # saving station based data to the same folder with gridded data
        weather_daily_data.to_csv(fix_path(settings.temp_folder)+f"weather_data_{settings.year}.csv", date_format='%Y-%m-%d')

    else:
        weather_daily_data = pd.read_csv(fix_path(settings.temp_folder)+f"weather_data_{settings.year}.csv")
        calc_percent_unavailable_data(weather_daily_data)

    # replace data gaps with mean values
    weather_daily_data = replace_empty_data_entries_with_mean(weather_daily_data)

    # add wind speed data as an input file
    extended_df = extend_from_daily_to_hourly_by_copy(
        calculate_wind_speed_at_two_meters(weather_daily_data["Wind speed"]),
        input_data_column_name = None
    )
    out_txt = fix_path(settings.input_folder) + 'dt_wind_01.txt'
    extended_df.to_csv(out_txt, sep='\t', header=False)
    remove_end_blank_line(out_txt)

    # generate files with default data
    generate_defaults(extended_df, fix_path(settings.input_folder))

    # generate dt_rootdepths_01.txt file
    generate_rootdepths(
        extended_df,
        fix_path(settings.input_folder),
        settings.veg_season,
        global_start_time = start_time
    )

    print("Calculating net radiation and PET...")

    wind_speed_df = pd.DataFrame(
        index=daily_temp_df.index,
        data=np.array(weather_daily_data["Wind speed"]),
        columns=['daily_accums']
    )
    # calculating net radiation, long-wave radiation, PET
    net, long_in, pet = net_and_pet(
        settings.coordinates,
        daily_humid_df,
        daily_temp_df,
        daily_glod_rad_df,
        wind_speed_df
    )
    # saving as csv files
    net.to_csv(fix_path(settings.temp_folder)+'net.csv', date_format='%Y-%m-%d')
    long_in.to_csv(fix_path(settings.temp_folder)+'long_in.csv', date_format='%Y-%m-%d')
    pet.to_csv(fix_path(settings.temp_folder)+'pet.csv', date_format='%Y-%m-%d')

    # extending to hourly, saving as an input files
    extended_df = extend_from_daily_to_hourly_by_divide(long_in)
    out_txt = fix_path(settings.input_folder) + 'dt_radiat_long_01.txt'
    extended_df.to_csv(out_txt, sep='\t', header=False)
    remove_end_blank_line(out_txt)

    extended_df = extend_from_daily_to_hourly_by_divide(pet)
    out_txt = fix_path(settings.input_folder) + 'dt_pet_01.txt'
    extended_df.to_csv(out_txt, sep='\t', header=False)
    remove_end_blank_line(out_txt)

    # calling other modules from import
    import geopackage_area
    if settings.user_soil == "Y":
        import soil_param
    import mod_files
    import geopackage_to_flush

    # running FLUSH
    p = Popen(fr"{settings.dir_flush}\run.bat", cwd=settings.dir_flush)
    p.communicate()

    # calling plotting module from import
    import start_plotting

if __name__ == '__main__':
    main()
