import pandas as pd
import numpy as np
from pyproj import Transformer
import datetime as dt


ALBEDO = 0.23
ALTITUDE = 10.0  # [m]
DEG_TO_RAD = np.pi / 180.0
SIGMA = 4.903e-9  # [MJ K-4 m-2 day-1] Stefan-Boltzmann constant


def calc_e_sat(daily_temp_df):
    """
    Saturated water vapor pressure [kPa].
    """
    return 0.6108 * np.exp(17.27 * daily_temp_df/(237.3 + daily_temp_df))


def calc_e_a(e_sat, daily_humid_df):
    """
    Water vapor pressure [kPa].
    """
    return e_sat * daily_humid_df / 100


def clear_sky_emissivity(e_a, daily_temp_df):
    """
    Clear sky Emissivity.
    """
    return 1.08 * (1 - np.exp(-((10 * e_a)**((daily_temp_df + 273.16 )/2016))))


def atm_pres(z=ALTITUDE):
    """
    Args:
        z: [m] elevation of the meteo station above sea level
    Returns:
        atmospheric pressure in [kPa]
    """
    return 101.3 * ((293 - 0.0065*z)/293)**5.26


def phychometric_const():
    """
    Calculates phychometric constant [kPa] as a function of atmospheric pressure.
    """
    return 0.665 * 1e-3 * atm_pres()


def delta(daily_temp_df):
    return (
        4098 * (0.6108 * np.exp(17.27 * daily_temp_df / (daily_temp_df + 237.3) ))
            / ((daily_temp_df + 237.3)**2)
        )


def clear_sky_radiation(Ra, z=ALTITUDE):
    """
    Clear-sky radiation calculation from daily extraterrestrial radiation.
    Args:
        Ra: [MJ m-2 d-1] daily extraterrestrial radiation at top of atm.
        z: [m] elevation above sea level
    Returns:
        Rs0: [MJ m-2 d-1] clear sky radiation
    """
    return (0.75 + 2e-5 * z) * Ra


def convert_coordinates(poi, crs_from="EPSG:3067", crs_to="EPSG:4326"):
    """
    Conversion of geographical coordinates.
    Args:
        poi: list of strings of input coordinates, for example,
            in format [N, E] EPSG:3067, it will be ['7008018', '229667']
        crs_from: format to convert from
        crs_to: format to convert to
    Returns:
        lat: latitude in new reference system, by default in [deg]
        lon: longitude in new reference system, by default in [deg]
    """
    trans = Transformer.from_crs(crs_from, crs_to, always_xy=True)
    lon, lat = trans.transform(xx=float(poi[1]), yy=float(poi[0]), errcheck=True)
    return lat, lon


def daily_extraterrestrial_radiation(lat, dayofyear):
    """
    Daily solar radiation at top of atmosphere. FAO Allen eq.21-26
    Args:
        lat: latitude in [deg]
        dayofyear: day of year 1..365 or 1..366

    Returns:
        Ra: [MJ m-2 d-1] daily radiation at top of atm.
    """
    lat = lat * DEG_TO_RAD
    J = dayofyear
    # J = dt.datetime.strptime(date, date_format).timetuple().tm_yday

    dr = 1.0 + 0.033 * np.cos(2.0 * np.pi / 365.0 * J)
    delta = 0.409 * np.sin(2.0 * np.pi / 365.0 * J - 1.39)
    ws = np.arccos(-np.tan(lat) * np.tan(delta))

    Ra = ( 24 * 60 * 0.0820 / np.pi * dr *
            (ws * np.sin(lat)*np.sin(delta) + np.cos(lat)*np.cos(delta)*np.sin(ws))
        )
    return Ra


def calc_cloud_factor(Rs0, Rs):
    cloud_factor = 1 - Rs / Rs0
    cloud_factor[cloud_factor < 0] = 0
    cloud_factor[cloud_factor > 1] = 1
    return cloud_factor


def calc_pet(daily_temp_df, wind_speed, net, e_sat, e_a):
    Cn = 900
    Cd = 0.34
    G = 0
    return (
        (0.408 * delta(daily_temp_df) * (net-G) + phychometric_const() * Cn / (daily_temp_df + 273) * wind_speed * (e_sat - e_a))
        / (delta(daily_temp_df) + phychometric_const() * (1+ Cd * wind_speed))
    )


def net_and_pet(poi, daily_humid_df, daily_temp_df, daily_glod_rad_df, wind_speed):
    """
    Master function to calculate net radiation and PET.
    """
    lat, _ = convert_coordinates(poi)
    dates_dayofyear = daily_temp_df.index.dayofyear
    Ra = daily_extraterrestrial_radiation(lat, dates_dayofyear)
    Rs0 = clear_sky_radiation(Ra, z=ALTITUDE)

    Rs0 = pd.DataFrame(index=daily_temp_df.index, data=np.array(Rs0), columns=['daily_accums'])
    e_sat = calc_e_sat(daily_temp_df)
    e_a = calc_e_a(e_sat, daily_humid_df)
    em_clr = clear_sky_emissivity(e_a, daily_temp_df)

    cloud_factor = calc_cloud_factor(Rs0, daily_glod_rad_df)
    emissivity = cloud_factor + (1 - cloud_factor) * em_clr

    long_in = emissivity * SIGMA * (daily_temp_df + 273.16)**4
    long_out = SIGMA * (daily_temp_df + 273.16)**4

    net_short = daily_glod_rad_df * (1 - ALBEDO)  # incoming > 0
    net_long = long_out - long_in  # outgoing > 0
    net = net_short - net_long

    pet = calc_pet(daily_temp_df, wind_speed, net, e_sat, e_a)

    # forcing PET to non-negative values
    pet[pet['daily_accums']<0] = 0

    return net, long_in, pet







