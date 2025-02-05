import pandas as pd
import matplotlib.pyplot as plt
import settings

DRAIN_SPACING = 15
#need to be replased with settings.drain_spacing and evap_data should be converted

# Define the input and output file paths
#input_file_path = r'\home.org.aalto.fi\porokht1\data\Desktop\data_modelled\Otaniemi_2022\clay\modelled_log\log.txt'
input_file_path = r'\\home.org.aalto.fi\porokht1\data\Desktop\data_modelled\Jyvaskyla\2018\Conv\log\log_04.txt'
output_file_path = r'\\home.org.aalto.fi\porokht1\data\Desktop\data_modelled\Jyvaskyla\2018\Conv\plots\wb_conv_04.png'

# Read the log file using pandas
df = pd.read_csv(input_file_path, delimiter='\t')

# Converting to [mm]
df['oPrecSi'] = (df['oPrecSi'] / DRAIN_SPACING**2) * 1000
#df['oPrecSi'] = (df['oPrecSi'] / DRAIN_SPACING**2) * 1000
df['oEvap'] = (df['oEvap'] / DRAIN_SPACING**2) * 1000
df['sEtM'] = (df['sEtM'] / DRAIN_SPACING**2) * 1000
df['sEtF'] = (df['sEtF'] / DRAIN_SPACING**2) * 1000
df['sDit_0'] = (df['sDit_0'] / DRAIN_SPACING**2) * 1000
df['sDit_1'] = (df['sDit_1'] / DRAIN_SPACING**2) * 1000
df['sDra_0'] = (df['sDra_0'] / DRAIN_SPACING**2) * 1000
df['sDra_1'] = (df['sDra_1'] / DRAIN_SPACING**2) * 1000
df['oDit_0'] = (df['oDit_0'] / DRAIN_SPACING**2) * 1000

# Extract data for the plot
time_hours = df['time']
precip_data = df['oPrecSi']
evap_data = df[['oEvap','sEtM','sEtF']].sum(axis=1)
discharge_to_open_ditch_data = df[['sDit_0','sDit_1']].sum(axis=1)
drain_discharge_data = df[['sDra_0','sDra_1']].sum(axis=1)
surface_runoff_data = df['oDit_0']

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(time_hours, precip_data, label='Precipitation(oPrecSi)')
plt.plot(time_hours, evap_data, label='Evaporation(oEvap, sEtM, sEtF)')
plt.plot(time_hours, discharge_to_open_ditch_data, label="Open ditch(sDit_0,sDit_1)")
plt.plot(time_hours, drain_discharge_data, label="Drains(sDra_0,sDra_1)")
plt.plot(time_hours, surface_runoff_data, label='Surface runoff(oDit_0)')


# Set labels and title
plt.xlabel('Time (hours)'),
plt.ylabel('mm'),
plt.title("annual water balance components"),
plt.legend()

# Save the plot
plt.savefig(output_file_path)

# Display the plot (optional)
plt.show()