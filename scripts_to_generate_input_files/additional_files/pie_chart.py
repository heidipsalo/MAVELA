import plotly.graph_objs as go
import pandas as pd
import numpy as np



DRAIN_SPACING = 15
YEAR = 2018
LOCATION = "Jyvaskyla"

input_file_path = r'\\home.org.aalto.fi\porokht1\data\Desktop\data_modelled\Jyvaskyla\2018\Conv\log\log_04.txt'
output_file_path = r'\\home.org.aalto.fi\porokht1\data\Desktop\data_modelled\Jyvaskyla\2018\Conv\plots\wb_cont_o4_pie.html'
# Read the log file using pandas
df = pd.read_csv(input_file_path, delimiter='\t')

# Converting to [mm]
df['oPrecSi'] = (df['oPrecSi'] / DRAIN_SPACING**2) * 1000
df['oEvap'] = (df['oEvap'] / DRAIN_SPACING**2) * 1000
df['sEtM'] = (df['sEtM'] / DRAIN_SPACING**2) * 1000
df['sEtF'] = (df['sEtF'] / DRAIN_SPACING**2) * 1000
df['sDit_0'] = (df['sDit_0'] / DRAIN_SPACING**2) * 1000
df['sDit_1'] = (df['sDit_1'] / DRAIN_SPACING**2) * 1000
df['sDra_0'] = (df['sDra_0'] / DRAIN_SPACING**2) * 1000
df['sDra_1'] = (df['sDra_1'] / DRAIN_SPACING**2) * 1000
df['oDit_0'] = (df['oDit_0'] / DRAIN_SPACING**2) * 1000
df['oWatVol'] = (df['oWatVol'] / DRAIN_SPACING**2) * 1000
df['oSnWaVo'] = (df['oSnWaVo'] / DRAIN_SPACING**2) * 1000
df['sWatVoM'] = (df['sWatVoM'] / DRAIN_SPACING**2) * 1000
df['sWatVoF'] = (df['sWatVoF'] / DRAIN_SPACING**2) * 1000

# Data
labels = ['Evapotranspiration', 'Discharge to the open ditch', 'Drain discharge', 'Change in water storage']
values = [((df['oEvap'].iloc[-1]+ df['sEtM'].iloc[-1]+ df['sEtF'].iloc[-1])), ((df['sDra_0'].iloc[-1]) + (df['sDra_1'].iloc[-1]) + (df['oDit_0'].iloc[-1])), np.abs((df['sWatVoF'].iloc[-1]) - (df['sWatVoF'].iloc[0]) + (df['sWatVoM'].iloc[-1]) - (df['sWatVoM'].iloc[0]) + ((df['oWatVol'].iloc[-1]) - (df['oWatVol'].iloc[0])))]

# Create the pie chart
fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

# Update layout for better visualization
fig.update_layout(
    title_text=f"Water Balance Components, {LOCATION}, {YEAR} <br> control drainage with open ditch",  # Title of the pie chart
    title_font_size=20,  # Adjust the font size of the title
    title_x=0.5)  # Adjust the title position

# Save the plot
fig.write_html(output_file_path)

# Show the plot
fig.show()

