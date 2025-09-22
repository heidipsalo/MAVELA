"""Generate files with default data."""
import pandas as pd
import numpy as np
import datetime as dt
from download_and_format_input_files_helper import SECONDS_IN_HOUR, HOURS_IN_DAY


DAYS_IN_MONTH = 30


def modify_data(df, year, period):
    start, end = period.split(" ")
    start_day, start_month = start.split(".")
    end_day, end_month = end.split(".")

    start_pd = pd.Timestamp(year=int(year), month=int(start_month), day=int(start_day))
    end_pd = pd.Timestamp(year=int(year), month=int(end_month), day=int(end_day))

    mask = (df['Date']>start_pd) & (df['Date']<=end_pd)
    df.loc[mask, 0] = 1


def remove_end_blank_line(path):
    with open(path) as f:
        lines = f.readlines()
        last = len(lines) - 1
        lines[last] = lines[last].replace('\r','').replace('\n','')
    with open(path, 'w') as wr:
        wr.writelines(lines)


def generate_default_data(
        num_of_rows,
        first_column_value,
        second_column_value = None,
        first_header_value = None,
        second_header_value = None
):
    """Generates predefined data sets"""
    if second_column_value is None:
        data_list = [first_column_value] * num_of_rows
        if first_header_value is not None:
            data_list[0] = first_header_value
        return pd.DataFrame(data=data_list)
    else:
        first_column = [first_column_value] * num_of_rows
        second_column = [second_column_value] * num_of_rows
        if first_header_value is not None and second_header_value is None:
            first_column[0] = first_header_value
        elif first_header_value is not None and second_header_value is not None:
            first_column[0] = first_header_value
            second_column[0] = second_header_value
        elif first_header_value is None and second_header_value is not None:
            second_column[0] = second_header_value
        return pd.DataFrame(data=[first_column, second_column]).T


def generate_defaults(extended_df, output_directory, settings):

    # 1. Generate dt_solutes_fertil_01.txt
    df = generate_default_data(
            num_of_rows = extended_df.size,
            first_column_value = 0.001,
            second_column_value = 0
    )
    out_txt = output_directory + 'dt_solutes_fertil_01.txt'
    df.to_csv(out_txt, sep='\t', header=False)
    remove_end_blank_line(out_txt)

    # 2. Generate dt_temp_soil_bottom_01.txt
    df = generate_default_data(
            num_of_rows = extended_df.size,
            first_column_value = 5.9,
    )
    out_txt = output_directory + 'dt_temp_soil_bottom_01.txt'
    df.to_csv(out_txt, sep='\t', header=False)
    remove_end_blank_line(out_txt)


    # 3. Generate dt_draincontrol_01.txt
    df = generate_default_data(
            num_of_rows = extended_df.size,
            first_column_value = -1,
    )
    if settings.drain_type == "Control Drainage":
        df['Date'] = pd.Timestamp(f'{settings.year}-01-01') + pd.to_timedelta(df.index, unit='H')
        # periods = settings.control_time.split(" ")
        # for period in periods:
            # modify_data(df, settings.year, period)
        period = settings.control_time
        modify_data(df, settings.year, period)
        df = df.drop('Date', axis=1)

    out_txt = output_directory + 'dt_draincontrol_01.txt'
    df.to_csv(out_txt, sep='\t', header=False)
    remove_end_blank_line(out_txt)

    # 4. Generate dt_macropmult_01.txt
    df = generate_default_data(
            num_of_rows = extended_df.size,
            first_column_value = -1,
            second_column_value = -1,
            first_header_value = 1,
            second_header_value= 2.5

    )
    out_txt = output_directory + 'dt_macropmult_01.txt'
    df.to_csv(out_txt, sep='\t', header=False)
    remove_end_blank_line(out_txt)

    # 5. Generate dt_gridsavepnts_01.txt
    df = generate_default_data(
            num_of_rows = extended_df.size,
            first_column_value = -1,
    )
    out_txt = output_directory + 'dt_gridsavepnts_01.txt'
    df.to_csv(out_txt, sep='\t', header=False)
    remove_end_blank_line(out_txt)

    # 6. Generate dt_overflowthr_01.txt
    df = generate_default_data(
            num_of_rows = extended_df.size,
            first_column_value = -1,
            first_header_value = 0.01,

    )
    out_txt = output_directory + 'dt_overflowthr_01.txt'
    df.to_csv(out_txt, sep='\t', header=False)
    remove_end_blank_line(out_txt)

    # 7. Generate dt_erosrain_01.txt
    df = generate_default_data(
            num_of_rows = extended_df.size,
            first_column_value = -1,
            first_header_value = 0.2,

    )
    out_txt = output_directory + 'dt_erosrain_01.txt'
    df.to_csv(out_txt, sep='\t', header=False)
    remove_end_blank_line(out_txt)

    # 8. Generate dt_mann_01.txt
    df = generate_default_data(
            num_of_rows = extended_df.size,
            first_column_value = -1,
            first_header_value = 0.1,

    )
    out_txt = output_directory + 'dt_mann_01.txt'
    df.to_csv(out_txt, sep='\t', header=False)
    remove_end_blank_line(out_txt)

    # 9. Generate dt_eroshydr_01.txt
    df = generate_default_data(
            num_of_rows = extended_df.size,
            first_column_value = -1,
            first_header_value = 1.5E-07,

    )
    out_txt = output_directory + 'dt_eroshydr_01.txt'
    df.to_csv(out_txt, sep='\t', header=False)
    remove_end_blank_line(out_txt)

    # 10. Generate dt_solutes_depos_01.txt
    df = generate_default_data(
            num_of_rows = extended_df.size,
            first_column_value = -1,
    )
    out_txt = output_directory + 'dt_solutes_depos_01.txt'
    df.to_csv(out_txt, sep='\t', header=False)
    remove_end_blank_line(out_txt)


def generate_rootdepths(
        extended_df,
        output_directory,
        veg_season,
        global_start_time,
        time_format="%Y-%m-%d"
    ):
    num_of_rows = extended_df.size
    data_list = [0.05] * num_of_rows

    start_time = dt.datetime.strptime(veg_season[0], time_format)
    stop_time = dt.datetime.strptime(veg_season[1], time_format)
    global_start_time = dt.datetime.strptime(global_start_time, "%Y-%m-%d %H:%M")

    hour_start = int((start_time - global_start_time).total_seconds()//SECONDS_IN_HOUR + 24)
    hour_stop = int((stop_time - global_start_time).total_seconds()//SECONDS_IN_HOUR)
    add = (0.75 - 0.05) / DAYS_IN_MONTH / HOURS_IN_DAY

    if (stop_time - start_time).days > DAYS_IN_MONTH:
        hour_mid = hour_start + DAYS_IN_MONTH * HOURS_IN_DAY

        for i in range(DAYS_IN_MONTH * HOURS_IN_DAY):
            data_list[hour_start+i] += add * i
        data_list[hour_mid:hour_stop] = [0.75] * len(data_list[hour_mid:hour_stop])
    else:
        for i in range(hour_stop-hour_start):
            data_list[hour_start + i] += add * i

    df = pd.DataFrame(data=data_list, dtype=np.float64)
    out_txt = output_directory + 'dt_rootdepths_01.txt'
    df.to_csv(out_txt, sep='\t', header=False)
    remove_end_blank_line(out_txt)




