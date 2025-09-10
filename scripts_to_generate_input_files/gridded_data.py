import pandas as pd
import settings
from functools import partial
import time
from concurrent.futures import ThreadPoolExecutor
from generate_default_data_files_helper import remove_end_blank_line
from download_and_format_input_files_helper import (
    construct_gridded_urls, read_nc_file, find_nearest, fix_path,
    extend_from_daily_to_hourly_by_copy,extend_from_daily_to_hourly_by_divide,
    download_file
)


def download_gridded_data():
    print("Downloading gridded data from FMI web...")

    urls = construct_gridded_urls(settings.year)
    download_func = partial(download_file, save_path=settings.temp_folder)
    start_downloading_time = time.time()
    with ThreadPoolExecutor() as executor:
        executor.map(download_func, urls)
    end_downloading_time = time.time()
    print("Gridded data downloaded in {} s".format(end_downloading_time-start_downloading_time))

    # urls = construct_gridded_urls(settings.year)
    # start_downloading_time = time.time()

    # for i in range (0,len(urls)):
    #     start = time.time()
    #     download_file(urls[i], settings.temp_folder)
    #     end = time.time()
    #     print("Gridded {} data downloaded in {} s".format(urls[i].split('/')[-1], end-start))
    # end_downloading_time = time.time()
    # print("Gridded data downloaded in {} s".format(end_downloading_time-start_downloading_time))


def process_and_save_gridded_data(files, filenames):
    for file, filename in zip(files, filenames):
        dates, latitudes, longitutes, observations, fd = read_nc_file(file)

        # Get index for the settings.coordinates
        x_idx = find_nearest(latitudes[:], float(settings.coordinates[0]))
        y_idx = find_nearest(longitutes[:], float(settings.coordinates[1]))

        # Get daily accumulations for the settings.coordinates
        daily_accums = observations[:, x_idx, y_idx]

        # Transform to pandas dataframe
        df = pd.DataFrame(list(zip(dates, daily_accums)), columns=['Date', 'daily_accums'])
        df.set_index('Date', inplace=True)
        df.to_csv(fix_path(settings.temp_folder)+filename.replace(".nc", ".csv"), date_format='%Y-%m-%d')

        if 'rrday' in filename:
            extended_df = extend_from_daily_to_hourly_by_divide(df)
            out_txt = fix_path(settings.input_folder) + 'dt_precip_01.txt'
            extended_df.to_csv(out_txt, sep='\t', header=False)
            remove_end_blank_line(out_txt)
        elif 'rh' in filename:
            daily_humid_df = df
            extended_df = extend_from_daily_to_hourly_by_copy(df)
            out_txt = fix_path(settings.input_folder) + 'dt_humid_01.txt'
            extended_df.to_csv(out_txt, sep='\t', header=False)
            remove_end_blank_line(out_txt)
        elif 'tday' in filename:
            daily_temp_df = df
            extended_df = extend_from_daily_to_hourly_by_copy(df)
            out_txt = fix_path(settings.input_folder) + 'dt_temp_01.txt'
            extended_df.to_csv(out_txt, sep='\t', header=False)
            remove_end_blank_line(out_txt)
        elif 'globrad' in filename:
            # Convert initial data from kJ/m^2 to MJ/m^2 by dividing by 1000
            daily_glod_rad_df = df/1000
            extended_df = extend_from_daily_to_hourly_by_divide(df)/1000
            out_txt = fix_path(settings.input_folder) + 'dt_radiat_short_01.txt'
            extended_df.to_csv(out_txt, sep='\t', header=False)
            remove_end_blank_line(out_txt)
        elif 'snow' in filename:
            snow_depth = df['daily_accums'].iloc[0] * 10  # to [mm]
            # print(f"The snow depth on the 1st of January was {snow_depth} mm.")
        fd.close()

    return daily_humid_df, daily_temp_df, daily_temp_df, daily_glod_rad_df


def calc_swe():
    """
    Calculates Snow Water Equivalent based on snow depth at 01.01.xxxx data.
    Given Snow depth is in [mm]
    """
    df = pd.read_csv(fix_path(settings.temp_folder) + f"snow_{settings.year}.csv")
    snow_depth = df['daily_accums'].iloc[0] * 10  # to [mm]
    return snow_depth/1000/4
    #return 0.146 * snow_depth**1.102
