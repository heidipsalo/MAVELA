# Script for comparing flush simulation results

import pandas as pd
import matplotlib.pyplot as plt

def read_and_convert(input_file_path, year, drain_spacing):
    # Read the log file using pandas
    df = pd.read_csv(input_file_path, delimiter='\t')
    df['Date'] = pd.Timestamp(f'{year}-01-01') + pd.to_timedelta(df['time'], unit='H')

    # Converting to [mm]
    df['oPrecSi'] = (df['oPrecSi'] / drain_spacing**2) * 1000
    df['oEvap'] = (df['oEvap'] / drain_spacing**2) * 1000
    df['sEtM'] = (df['sEtM'] / drain_spacing**2) * 1000
    df['sEtF'] = (df['sEtF'] / drain_spacing**2) * 1000
    df['sDit_0'] = (df['sDit_0'] / drain_spacing**2) * 1000
    df['sDit_1'] = (df['sDit_1'] / drain_spacing**2) * 1000
    df['sDra_0'] = (df['sDra_0'] / drain_spacing**2) * 1000
    df['sDra_1'] = (df['sDra_1'] / drain_spacing**2) * 1000
    df['oDit_0'] = (df['oDit_0'] / drain_spacing**2) * 1000

    # Extract data for the plot
    time_hours = df['time']
    precip_data = df['oPrecSi']
    evap_data = df[['oEvap','sEtM','sEtF']].sum(axis=1)
    discharge_to_open_ditch_data = df[['sDit_0','sDit_1']].sum(axis=1)
    drain_discharge_data = df[['sDra_0','sDra_1']].sum(axis=1)
    surface_runoff_data = df['oDit_0']
    snow_water_eq = df['oSnWaVo']

    return (
        df, precip_data, evap_data, discharge_to_open_ditch_data,
        drain_discharge_data, surface_runoff_data, snow_water_eq
    )

# Read base simulation results (log.txt) and data (report.txt)
fp_input_base = "../../flush_03_cd/Release/output_base/report.txt"
fp_output_base = "../../flush_03_cd/Release/output_base/log.txt"

df_report_base = pd.read_csv(fp_input_base, index_col=0)
year_base = df_report_base['year'].values[0]
ds_base = df_report_base['drain_spacing'].values[0]

df_log_base, prec_base, et_base, gwf_base, dra_base, dit_base, swe_base = read_and_convert(fp_output_base, year_base, ds_base)


# Read second simulation results (log.txt) and data (report.txt)
fp_input_second = "../../flush_03_cd/Release/data/input/report.txt"
fp_output_second = "../../flush_03_cd/Release/output/log.txt"

df_report_second = pd.read_csv(fp_input_second, index_col=0)
year_second = df_report_second['year'].values[0]
ds_second = df_report_second['drain_spacing'].values[0]

df_log_second, prec_second, et_second, gwf_second, dra_second, dit_second, swe_seconde = read_and_convert(fp_output_second, year_second, ds_second)

# Plot drain discharge
fig, ax = plt.subplots()
plt.plot(dra_base, label='Drain discharge (base)')
plt.plot(dra_second, label='Drain discharge (second)')
plt.legend()

fig, ax = plt.subplots()
plt.plot(df_log_base['sGw_0'], label='GW depth (base)')
plt.plot(df_log_base['sGw_1'], label='GW depth (base)')
plt.plot(df_log_second['sGw_0'], label='GW depth (second)')
plt.plot(df_log_second['sGw_1'], label='GW depth (second)')
plt.legend()
ax.set_ylim(2,0)
plt.show()