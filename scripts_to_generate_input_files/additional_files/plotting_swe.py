import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import settings

# Define the input and output file paths
input_file_path = r'\\home.org.aalto.fi\porokht1\data\Desktop\data_modelled\Jyvaskyla\2018\Cont\log\log_cont.txt'
output_file_path = r'\\home.org.aalto.fi\porokht1\data\Desktop\data_modelled\Jyvaskyla\2018\Cont\plots\swe_cont.png'

DRAIN_SPACING = 15

# Read the log file using pandas
df = pd.read_csv(input_file_path, delimiter='\t')

# Extract data for the plot
time_hours = df['time']
swe = df['oSnWaVo'] = (df['oSnWaVo'] / DRAIN_SPACING**2) * 1000


# Plotting
plt.figure(figsize=(10, 6))
plt.plot(time_hours, swe, label='swe(oSnWaVo)')

# Set labels and title
plt.xlabel('Time (hours)'),
plt.ylabel('mm'),
plt.title("swe"),
plt.legend()

# Save the plot
plt.savefig(output_file_path)

# Display the plot (optional)
plt.show()