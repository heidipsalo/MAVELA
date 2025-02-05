import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import settings

# Define the input and output file paths
input_file_path = r'\\home.org.aalto.fi\porokht1\data\Desktop\data_modelled\Jyvaskyla\2018\Cont\log\log_cont.txt'
output_file_path = r'\\home.org.aalto.fi\porokht1\data\Desktop\data_modelled\Jyvaskyla\2018\Cont\plots\wat_storage_cony.png'

# Read the log file using pandas
df = pd.read_csv(input_file_path, delimiter='\t')

# Extract data for the plot
time_hours = df['time']
overland_water_storage_data = df['oWatVol']

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(time_hours, overland_water_storage_data, label='Water storage(oWatVol)')

# Set labels and title
plt.xlabel('Time (hours)'),
plt.ylabel('mm'),
plt.title("annual water storage"),
plt.legend()

# Save the plot
plt.savefig(output_file_path)

# Display the plot (optional)
plt.show()