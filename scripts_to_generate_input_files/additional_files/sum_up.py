import pandas as pd

input_file_path = r'\\home.org.aalto.fi\porokht1\data\Desktop\data_modelled\Otaniemi_2022\clay\input\dt_precip_01.txt'
df = pd.read_csv(input_file_path, delimiter='\t')

DRAIN_SPACING = 15

print(df.iloc[:,1].sum())