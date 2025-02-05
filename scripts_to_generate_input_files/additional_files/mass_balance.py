import pandas as pd

input_file_path = r'\\home.org.aalto.fi\porokht1\data\Desktop\data_modelled\Jyvaskyla\2018\Conv\log\log_04.txt'
#input_file_path = r'C:\Users\porokht1\gitlab\new_model\Flush_03(current)\Release\output\log.txt'
#input_file_path = r'C:\Users\porokht1\gitlab\flush_controlled_drainage_18_03\Release\output\log.txt'

df = pd.read_csv(input_file_path, delimiter='\t')

DRAIN_SPACING = 15

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

# Balance equation

#balance = df['oPrecSi'].iloc[-1] - df['oEvap'].iloc[-1]- df['sEtM'].iloc[-1]- df['sEtF'].iloc[-1]  \
#- (df['sDit_0'].iloc[-1]) - (df['sDit_1'].iloc[-1]) - (df['sDra_0'].iloc[-1]) - (df['sDra_1'].iloc[-1]) \
#- (df['oDit_0'].iloc[-1]) - ((df['oWatVol'].iloc[-1]) - (df['oWatVol'].iloc[0])) - ((df['oSnWaVo'].iloc[-1]) - (df['oSnWaVo'].iloc[0])) \
#- ((df['sWatVoM'].iloc[-1]) - (df['sWatVoM'].iloc[0])) - ((df['sWatVoF'].iloc[-1]) - (df['sWatVoF'].iloc[0]))

balance = df['oPrecSi'].iloc[-1] - df['oEvap'].iloc[-1]- df['sEtM'].iloc[-1]- df['sEtF'].iloc[-1]  \
- (df['sDit_0'].iloc[-1]) - (df['sDit_1'].iloc[-1]) - (df['sDra_0'].iloc[-1]) - (df['sDra_1'].iloc[-1]) \
- (df['oDit_0'].iloc[-1]) - ((df['oWatVol'].iloc[-1]) - (df['oWatVol'].iloc[0])) - ((df['oSnWaVo'].iloc[-1]) - (df['oSnWaVo'].iloc[0])) \
- ((df['sWatVoM'].iloc[-1]) - (df['sWatVoM'].iloc[0])) - ((df['sWatVoF'].iloc[-1]) - (df['sWatVoF'].iloc[0]))

print(balance)

print("oPrecSi - precipitation =", df['oPrecSi'].iloc[-1])
print("oEvap - evapotranspiration overland =",df['oEvap'].iloc[-1])
print("sEtM - evapotranspiration soil matrix =",df['sEtM'].iloc[-1])
print("sEtF - evapotranspiration macropores=",df['sEtF'].iloc[-1])
print("sDit_0  - open ditch discharge soil matrix=",df['sDit_0'].iloc[-1])
print("sDit_1  - open ditch discharge macropores=",df['sDit_1'].iloc[-1])
print("sDra_0 - drain discharge soil matrix=",df['sDra_0'].iloc[-1])
print("sDra_1 - drain discharge macropores=",df['sDra_1'].iloc[-1])
print("oDit_0 - open ditch discharge overland =",df['oDit_0'].iloc[-1])
print("oWatVol - overland water storage last value =",df['oWatVol'].iloc[-1])
print("oWatVol - overland water storage first value =",df['oWatVol'].iloc[0])
print("oSnWaVo - swe last value =",df['oSnWaVo'].iloc[-1])
print("oSnWaVo - swe first value =",df['oSnWaVo'].iloc[0])
print("sWatVoM - subsurface water storage matrix last value =",df['sWatVoM'].iloc[-1])
print("sWatVoM - subsurface water storage matrix first value =",df['sWatVoM'].iloc[0])
print("sWatVoF - subsurface water storage macropores last value =",df['sWatVoF'].iloc[-1])
print("sWatVoF - subsurface water storage macropores first value =",df['sWatVoF'].iloc[0])
