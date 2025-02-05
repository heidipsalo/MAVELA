import pandas as pd
import matplotlib.pyplot as plt

# Define the input and output file paths
input_file_path = r'\\home.org.aalto.fi\porokht1\data\Desktop\data_modelled\Jyvaskyla\2018\Conv\log\log_04.txt'
output_file_path = r'\\home.org.aalto.fi\porokht1\data\Desktop\data_modelled\Jyvaskyla\2018\Conv\plots\gw_conv_04.png'

# Read the log file using pandas
df = pd.read_csv(input_file_path, delimiter='\t')

# Change the sign from + to - of sGw_1
df['sGw_1'] = -df['sGw_1']
#df['sMoi_0'] = 1 - df['sMoi_0']
df['sGw_0'] = -df['sGw_0']
#df['sMoi_1'] = 1 - df['sMoi_1']


# Extract data for the plot
time_hours = df['time']
sGw_1_data = df['sGw_1']
#sMoi_0_data = df['sMoi_0']
sGw_0_data = df['sGw_0']
#sMoi_1_data = df['sMoi_1']

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(time_hours, sGw_1_data, label='Groundwater depth - macropores(sGw_1)')
plt.plot(time_hours, sGw_0_data, label='Groundwater depth - soil matrix(sGw_0)')
#plt.plot(time_hours, sMoi_0_data, label='Soil moisture - soil matrix(sMoi_0)')
#plt.plot(time_hours, sMoi_1_data, label='Soil moisture - macropores(sMoi_1)')

# Set labels and title
plt.xlabel('Time (hours)')
plt.ylabel('m')
plt.title("annual change of sGw_1 and sGw_0")
#plt.title('annual change of sGw_1, sGw_0, sMoi_1 and sMoi_0')
plt.legend()

# Save the plot
plt.savefig(output_file_path)

# Display the plot (optional)
plt.show()
