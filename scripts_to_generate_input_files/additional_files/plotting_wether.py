import pandas as pd
import matplotlib.pyplot as plt
from download_and_format_input_files_helper import fix_path


folder = r'\\home.org.aalto.fi\porokht1\data\Desktop\data_modelled\Jyvaskyla\2018\Conv\download'
year = 2018

weather_list = ['rrday', 'tday', 'weather_data','pet']
label_list = ['Precipitation [mm]', 'Temperature [o,C]', 'Wind speed [m/s]','PET [mm]']
#weather_list = ['rh', 'rrday', 'tday', 'weather_data']
radiation_list = ['net', 'long_in'], #'globrad']
#radiation_list = ['pet', 'net', 'long_in'] #, 'globrad']

fig = plt.figure()
for name, label in zip(weather_list, label_list):
    if name == "pet":
        df = pd.read_csv(fix_path(folder) + name + '.csv')
    else:
        df = pd.read_csv(fix_path(folder) + name + f'_{year}.csv')
    if name != 'weather_data':
        plt.plot(df['daily_accums'], label=label)
    else:
        plt.plot(df['Wind speed'], label=label)
    plt.xlabel('Days')
    plt.ylabel('Weather data')
    plt.legend()
plt.savefig(fix_path(folder) + 'weather_plot.png', dpi=300)
plt.show()



fig = plt.figure()
for name in radiation_list:
    if name == 'globrad':
        df = pd.read_csv(fix_path(folder) + name + f'_{year}.csv')
    else:
        df = pd.read_csv(fix_path(folder) + name + '.csv')
    plt.plot(df['daily_accums'], label=name)
    plt.xlabel('Days')
    plt.ylabel('Radiation data, [MJ m-2 d-1]')
    plt.legend()
plt.savefig(fix_path(folder) + 'radiation.png', dpi=300)
plt.show()

