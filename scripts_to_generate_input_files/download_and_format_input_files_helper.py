"""
Module with useful functions for downloading and creating input data files.
"""
import numpy as np
import pandas as pd
import netCDF4 as nc
import datetime as dt
import cftime
import os
import requests
from pyproj import Transformer
from fmiopendata.wfs import download_stored_query


GRIDDED_DATA_TO_DOWNLOAD = ["Tday/tday_", "RRday/rrday_", "Globrad/globrad_", "Rh/rh_", "Snow/snow_"]
GRIDDED_DATA_URL = "https://fmi-gridded-obs-daily-1km.s3-eu-west-1.amazonaws.com/Netcdf/"
HOURS_IN_DAY = 24
CHUNK_SIZE = 8192
TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"  # Time format for the FMI queries.
DOWNLOAD_LIMIT_HOURS = 744
SECONDS_IN_HOUR = 3600
DOWNLOAD_LIMIT_SECONDS = DOWNLOAD_LIMIT_HOURS * SECONDS_IN_HOUR


def find_nearest(array, value):
    """Function searches for the closest grid to poi (user input).
    Args:
        array: input array of data.
        value: user input value for which you want to find the closest correspondence in array.
    Returns:
        idx: index of the closest correspondence in array.
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


def to_datetime(d):
    """Checks and formats the dates to suitable format"""
    # https://github.com/MetOffice/forest/blob/master/forest/util.py
    if isinstance(d, dt.datetime):
        return d
    if isinstance(d, cftime.DatetimeNoLeap):
        return dt.datetime(d.year, d.month, d.day, d.hour, d.minute, d.second)
    elif isinstance(d, cftime.DatetimeGregorian):
        return dt.datetime(d.year, d.month, d.day, d.hour, d.minute, d.second)
    elif isinstance(d, str):
        errors = []
        for fmt in (
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%SZ"):
            try:
                return dt.datetime.strptime(d, fmt)
            except ValueError as e:
                errors.append(e)
                continue
        raise Exception(errors)
    elif isinstance(d, np.datetime64):
        return d.astype(dt.datetime)
    else:
        raise Exception("Unknown value: {} type: {}".format(d, type(d)))


def extend_from_daily_to_hourly_by_copy(
        df,
        input_data_column_name = 'daily_accums',
        output_data_column_name = 'hourly_accums'
):
    """Extends the daily values by repeating the value 24 times.
            Use for air temperature and relative humidity. """
    extended_df = pd.DataFrame(
        index=range(df.index.size*HOURS_IN_DAY), columns=[output_data_column_name]
    )
    hour = 0
    if input_data_column_name is None:
        series = df
    else:
        series = df[input_data_column_name]
    for daily in series:
        extended_df.iloc[hour:hour+HOURS_IN_DAY] = daily
        hour += HOURS_IN_DAY
    return extended_df


def extend_from_daily_to_hourly_by_divide(
        df,
        input_data_column_name = 'daily_accums',
        output_data_column_name = 'hourly_accums'
):
    """Extends the daily values by dividing the value by 24 and repeat new value 24 times.
            Use for precipitation """
    extended_df = pd.DataFrame(
        index=range(df.index.size*HOURS_IN_DAY), columns=[output_data_column_name]
    )
    hour = 0
    for daily in df[input_data_column_name]:
        extended_df.iloc[hour:hour+HOURS_IN_DAY] = daily/HOURS_IN_DAY
        hour += HOURS_IN_DAY
    return extended_df


def create_list_of_files_in_directory(directory, file_type=".nc"):
    """Creates the list of the FMI files in given directory"""
    file_list_full_path = []
    filename_list =[]
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(file_type):
            file_path = os.path.join(directory, filename)
            file_list_full_path.append(file_path)
            filename_list.append(filename)
    return file_list_full_path, filename_list


def read_nc_file(file):
    """Read .nc files, extract latitude, longitude, observation and time,
    also, convert time to standard time format"""
    f = nc.Dataset(file)
    dimensions = set(f.dimensions.keys())
    time_series = f.variables['Time']
    longitutes = f.variables['Lon']
    latitudes = f.variables['Lat']
    observation_key = set(f.variables.keys()) - dimensions
    observations = f.variables[observation_key.pop()]
    # Convert time to more meaningful format
    tmp_dates = nc.num2date(time_series[:], time_series.units)
    dates = [to_datetime(date) for date in tmp_dates]
    return dates, latitudes, longitutes, observations, f


def fix_path(path):
    if path[-1] != "/":
        path = path + "/"
    return path


def download_file(url, save_path=None):
    try:
        local_filename = url.split('/')[-1]
        if save_path is not None:
            local_filename = fix_path(save_path) + local_filename

        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
                    f.write(chunk)
    except Exception as e:
        print(e)


def construct_gridded_urls(year_start, year_end=None):
    urls = []
    if year_end is None:
        year_end = year_start
    for var in GRIDDED_DATA_TO_DOWNLOAD:
        for year in range(year_start, year_end+1):
            urls.append(GRIDDED_DATA_URL + var + str(year) + ".nc")
    return urls


def delete_downloaded_files(urls):
    for url in urls:
        if os.path.isfile(url):
            os.remove(url)


def get_all_stations():
    # Get all active observation stations
    ret = download_stored_query("fmi::ef::stations")

    stations = pd.DataFrame(
        data = list(
            zip(
                ret.identifiers, ret.latitudes, ret.longitudes,
                ret.begin_dates, ret.types, ret.names
            )
        ),
        columns = ['fmisid', 'lat', 'lon', 'begin', 'type', 'name']
    )
    trans = Transformer.from_crs(
        "EPSG:4326",
        "EPSG:3067",
        always_xy=True,
    )
    xx, yy = trans.transform(stations["lon"].values, stations["lat"].values)
    stations['X'] = xx
    stations['Y'] = yy
    return stations


def find_nearest_station(poi, print_message=True):
    stations = get_all_stations()
    station_positions = np.column_stack((stations['Y'], stations['X']))
    leftbottom = np.array(poi)
    distances = np.linalg.norm(station_positions-leftbottom, axis=1)
    sorted_distances = sorted(enumerate(distances), key=lambda i: i[1])  # returns sorted tuples with prev id and val

    return stations, sorted_distances


def download_weather_data(poi, start_time, end_time, time_format="%Y-%m-%d %H:%M", nearest_station=0):
    stations, sorted_distances_asc = find_nearest_station([float(poi[0]), float(poi[1])])
    station_index = sorted_distances_asc[nearest_station][0]
    station_id = stations.iloc[station_index]['fmisid']

    #print(f"Chosen station is {stations.iloc[station_index]}, at a distance of {sorted_distances_asc[nearest_station][1]}")

    start_time = dt.datetime.strptime(start_time, time_format)
    end_time = dt.datetime.strptime(end_time, time_format)

    n_full_loops = (end_time - start_time).total_seconds()//DOWNLOAD_LIMIT_SECONDS

    df_merged = pd.DataFrame()

    for n in range(int(n_full_loops)+1):
        if n == n_full_loops:
            end_time_loop = end_time
        else:
            end_time_loop = start_time + dt.timedelta(0, DOWNLOAD_LIMIT_SECONDS)

        obs = download_stored_query(
            query_id = "fmi::observations::weather::hourly::multipointcoverage",  # No more than 744.000000 hours allowed!
            args = [
                        f"fmisid={station_id}",
                        f"starttime={start_time.strftime(TIME_FORMAT)}",
                        f"endtime={end_time_loop.strftime(TIME_FORMAT)}",
                        "timeseries=True"
                    ]
        )
        start_time = end_time_loop + dt.timedelta(1)
        station_name = list(obs.data)[0]
        parameters = list(obs.data[station_name].keys())[1:]
        times = obs.data[station_name]['times']
        data = [obs.data[station_name][par]['values'] for par in parameters]
        data.append(times)
        parameters.append('Datetime')
        df = pd.DataFrame(data).transpose()
        df.columns = parameters
        df.set_index('Datetime', inplace=True)  # Use dates as index column.
        df.dropna(inplace=True, how='all')  # Drop rows with only nan values.
        daily_df = df.resample('24H').mean()
        df_merged = pd.concat([df_merged, daily_df], ignore_index=False, sort=False)

    return df_merged


def calculate_wind_speed_at_two_meters(given_wind_speed, given_height=10):
    """
    If the measurement is made at 10 m above a short grass surface,
    you can use the equation of a logarithmic wind speed profile to obtain
    the velocity at 2m.
    See FAO Irrigation and Drainage Paper No. 56 Crop Evapotranspiration
    (guidelines for computing crop water requirements) by ALLEN et al.
    """
    return given_wind_speed * 4.87 / np.log(67.8 * given_height - 5.42)


def replace_empty_data_entries_with_mean(df, name='Wind speed', print_message=True):
    if print_message:
        print(f'{df[name].isna().sum()} days have no data on {name}. ' \
            'Replacing them with average values over the requested period.')

    df.loc[df[name].isna()==True, name] = df[name].mean()
    return df


def calc_percent_unavailable_data(df, name='Wind speed', print_message=True):
    no_data = 100 * df[name].isna().sum()/df[name].size
    if print_message:
        no_data_srt = '{:.2f}'.format(no_data)
        print(f'{no_data_srt} % of {name} data are missing.')
    return no_data
