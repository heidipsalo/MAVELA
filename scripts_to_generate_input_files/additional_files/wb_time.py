import pandas as pd
import matplotlib.pyplot as plt

input_file_path = r'\\home.org.aalto.fi\porokht1\data\Desktop\data_modelled\Otaniemi_2022\clay\try_model_18.03\modelled results\log.txt'
output_file_path = r'\\home.org.aalto.fi\porokht1\data\Desktop\data_modelled\Otaniemi_2022\clay\try_model_18.03\plots\swe.png'

df = pd.read_csv(input_file_path, delimiter='\t')

DRAIN_SPACING = 15

# Converting to [mm]
df['oPrecSi'] = (df['oPrecSi'] / DRAIN_SPACING**2) * 1000
df['oEvap'] = (df['oEvap'] / DRAIN_SPACING**2) * 1000
df['sDit_0'] = (df['sDit_0'] / DRAIN_SPACING**2) * 1000
df['sDit_1'] = (df['sDit_1'] / DRAIN_SPACING**2) * 1000
df['sDra_0'] = (df['sDra_0'] / DRAIN_SPACING**2) * 1000
df['sDra_1'] = (df['sDra_1'] / DRAIN_SPACING**2) * 1000
df['oDit_0'] = (df['oDit_0'] / DRAIN_SPACING**2) * 1000
df['oWatVol'] = (df['oWatVol'] / DRAIN_SPACING**2) * 1000
df['oSnWaVo'] = (df['oSnWaVo'] / DRAIN_SPACING**2) * 1000
df['sWatVoM'] = (df['sWatVoM'] / DRAIN_SPACING**2) * 1000
df['sWatVoF'] = (df['sWatVoF'] / DRAIN_SPACING**2) * 1000


prec_dt = df['oPrecSi'].diff().fillna(df['oPrecSi'][0])
evap_dt = df['oEvap'].diff().fillna(df['oEvap'][0]) + df['sEtM'].diff().fillna(df['sEtM'][0])  + df['sEtF'].diff().fillna(df['sEtF'][0])
ditch_dt = df['oDit_0'].diff().fillna(df['oDit_0'][0]) + df['sDit_0'].diff().fillna(df['sDit_0'][0])  + df['sDit_1'].diff().fillna(df['sDit_1'][0])
drains_dt = df['sDra_0'].diff().fillna(df['sDra_0'][0]) + df['sDra_1'].diff().fillna(df['sDra_1'][0])
storchange_dt = df['oWatVol'].diff().fillna(df['oWatVol'][0]) + df['oSnWaVo'].diff().fillna(-0.015571) \
    + df['sWatVoM'].diff().fillna(-0.011252) + df['sWatVoF'].diff().fillna(-0.000016)

bal = prec_dt - evap_dt - ditch_dt - drains_dt - storchange_dt
bal.plot()
plt.show()
# Save the plot
plt.savefig(output_file_path)