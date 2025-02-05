import numpy as np
import pandas as pd
from download_and_format_input_files_helper import fix_path
from generate_default_data_files_helper import remove_end_blank_line
import settings


# HardCode data of soil parameters
soil_dict = {
        'Layer': [],
        'Type': [],
        'Macros': [],
        'ThetaS': [],
        'Compr.': [],
        'w': [],
        'Dry we.': [],
        'Density': [],
        'ThetaRm': [],
        'AlphaM': [],
        'nM': [],
        'KvM': [],
        'KhM-mul': [],
        'ThetaRF': [],
        'AlphaF': [],
        'nF': [],
        'KvF': [],
        'KhF-mul': [],
        'Gamma': [],
        'ConMulF': []
       }

df = pd.DataFrame(soil_dict)

# Creating dt_soillib_water_01.txt and dt_soillib_geom_01.txt
output_line = df.copy()

output_line.drop(['Layer', 'Type', 'Macros'], axis=1, inplace=True)
geom_params = output_line[['ThetaS', 'Compr.', 'w', 'Dry we.', 'Density']].copy()
water_params = output_line.drop(['ThetaS', 'Compr.', 'w', 'Dry we.', 'Density'], axis=1)

out_txt = fix_path(settings.input_folder) + 'dt_soillib_geom_01.txt'
geom_params.to_csv(out_txt, sep='\t', header=True)
remove_end_blank_line(out_txt)

out_txt = fix_path(settings.input_folder) + 'dt_soillib_water_01.txt'
water_params.to_csv(out_txt, sep='\t', header=True)
remove_end_blank_line(out_txt)

#creating default dt.soillib_crack_01.txt for top and bottom soil in one file
crack_lib = pd.DataFrame({'shrink': [],
'alphaK': [],
'betaK': [],
'gammaK': []})

out_txt = fix_path(settings.input_folder) + 'dt_soillib_crack_01.txt'
crack_lib.to_csv(out_txt, sep='\t', header=True)
remove_end_blank_line(out_txt)

#creating default dt_soillib_heat_01.txt for top and bottom soil in one file
heat_lib = pd.DataFrame({'H.cap.': [],
'cond': [],
'C.mul': []})

out_txt = fix_path(settings.input_folder) + 'dt_soillib_heat_01.txt'
heat_lib.to_csv(out_txt, sep='\t', header=True)
remove_end_blank_line(out_txt)

#creating default dt_soillib_solute_01.txt for top and bottom soil in one file
solute_lib = pd.DataFrame({'Di.L.M': [],
'Di.L.M.': [],
'Di.L.F': [],
'Di.L.F.': [],
'Mol.dif': [],
'Gamma': []}, dtype=np.float64)

out_txt = fix_path(settings.input_folder) + 'dt_soillib_solute_01.txt'
solute_lib.to_csv(out_txt, sep='\t', header=True)
remove_end_blank_line(out_txt)

#creating geom_layers_01.txt
def generate_geom_layers(input_folder):
    second_col = [0.02, 0.05, 0.08, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.25, 0.25, 0.35, 0.5]

    df = pd.DataFrame(data=[second_col]).T

    out_txt = fix_path(input_folder) + 'geom_layers_01.txt'
    df.to_csv(out_txt, sep='\t', header=False)
    remove_end_blank_line(out_txt)

generate_geom_layers(settings.input_folder)


#creating default cross_section.txt for top and bottom soil in one file
data = """#Ind\t# x,y-coordinates of points (arbitrary number) in cross-section from left to right.
0\t0\t20\t0\t1.2\t0.1\t0.689118409\t0.2\t0.491480417\t0.3\t0.349705933\t0.4\t0.238750813\t
0.5\t0.148810198\t0.6\t0.074833346\t
0.725\t0.000364639\t1.075\t0.000364639\t1.2\t0.074833346\t1.3\t0.148810198\t1.4\t
0.238750813\t1.5\t0.349705933\t1.6\t0.491480417\t1.7\t0.689118409\t1.8\t1.2\t1.8\t20
1\t0\t20\t0.5\t0\t1\t0\t1.5\t20
"""

out_txt = fix_path(settings.input_folder) + 'cross_section.txt'

with open(out_txt, 'w') as file:
    file.write(data)

message = (
    "Empty soil files are generated in the output folder. Please add your soil parameters in: \n"
    "geom_layers_01.txt \n"
    "dt_soillib_geom_01.txt \n"
    "dt_soillib_water_01.txt \n"
    "dt.soillib_crack_01.txt \n"
    "dt_soillib_solute_01.txt \n"
    "dt_soillib_heat_01.txt \n"
    )
print(message)
