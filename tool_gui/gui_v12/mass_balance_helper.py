import pandas as pd
import numpy as np


def calc_balance(input_file_path, drain_spacing):
    df = pd.read_csv(input_file_path, delimiter='\t')

    df['oPrecSi'] = (df['oPrecSi'] / drain_spacing**2) * 1000
    df['oEvap'] = (df['oEvap'] / drain_spacing**2) * 1000
    df['sEtM'] = (df['sEtM'] / drain_spacing**2) * 1000
    df['sEtF'] = (df['sEtF'] / drain_spacing**2) * 1000
    df['sDit_0'] = (df['sDit_0'] / drain_spacing**2) * 1000
    df['sDit_1'] = (df['sDit_1'] / drain_spacing**2) * 1000
    df['sDra_0'] = (df['sDra_0'] / drain_spacing**2) * 1000
    df['sDra_1'] = (df['sDra_1'] / drain_spacing**2) * 1000
    df['oDit_0'] = (df['oDit_0'] / drain_spacing**2) * 1000
    df['oWatVol'] = (df['oWatVol'] / drain_spacing**2) * 1000
    df['oSnWaVo'] = (df['oSnWaVo'] / drain_spacing**2) * 1000
    df['sWatVoM'] = (df['sWatVoM'] / drain_spacing**2) * 1000
    df['sWatVoF'] = (df['sWatVoF'] / drain_spacing**2) * 1000

    balance = df['oPrecSi'].iloc[-1] - df['oEvap'].iloc[-1]- df['sEtM'].iloc[-1]- df['sEtF'].iloc[-1]  \
    - (df['sDit_0'].iloc[-1]) - (df['sDit_1'].iloc[-1]) - (df['sDra_0'].iloc[-1]) - (df['sDra_1'].iloc[-1]) \
    - (df['oDit_0'].iloc[-1]) - ((df['oWatVol'].iloc[-1]) - (df['oWatVol'].iloc[0])) - ((df['oSnWaVo'].iloc[-1]) - (df['oSnWaVo'].iloc[0])) \
    - ((df['sWatVoM'].iloc[-1]) - (df['sWatVoM'].iloc[0])) - ((df['sWatVoF'].iloc[-1]) - (df['sWatVoF'].iloc[0]))

    # print(f"Mass balance error is {100*np.abs(balance/df['oPrecSi'].iloc[-1])} %. \n")

    return 100*np.abs(balance/df['oPrecSi'].iloc[-1])


