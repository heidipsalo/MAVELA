import numpy as np
import pandas as pd
from download_and_format_input_files_helper import fix_path
from generate_default_data_files_helper import remove_end_blank_line
import settings


# HardCode data of soil parameters
soil_dict = {
        'Layer':['Top soils', 'Top soils', 'Top soils','Top soils','Top soils','Top soils', 'Bottom soils', 'Bottom soils', 'Bottom soils', 'Bottom soils','Bottom soils', 'Bottom soils'],
        'Type':['Clay', 'Clay', 'Silt', 'Silt', 'Peat', 'Peat', 'Clay', 'Clay', 'Silt', 'Silt', 'Peat','Peat'],
        'Macros':['High', 'Low', 'High', 'Low', 'High', 'Low', 'High', 'Low', 'High', 'Low', 'High', 'Low',],
        'ThetaS':[0.543, 0.5507, 0.450205, 0.398460, 0.8212,0.3838, 0.590900, 0.590900, 0.362565, 0.384737, 0.56, 0.3838],
        'Compr.':[0.0001, 0.0001, 0.0001, 0.0001,0.0001, 0.0001,0.0001, 0.0001,0.0001, 0.0001, 0.0001, 0.0001],
        'w':[0.0331, 0.0014, 0.087187, 0.053806, 0.092021, 0.001, 0.0015, 0.0006, 0.042015, 0.03032, 0.05, 0.005],
        'Dry we.':[1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500,1500, 1500],
        'Density':[2650, 2650, 2650, 2650, 2650, 2650, 2650, 2650, 2650, 2650, 2650, 2650],
        'ThetaRm':[0.1, 0.1, 0.1, 0.1,0.044, 0.1429, 0.1, 0.1, 0.1, 0.1, 0.1429, 0.1429],
        'AlphaM':[2.548, 0.273, 8.79381675, 4.18752912, 7.6779, 0.36751, 1.072, 1.072, 1.471577346, 0.180226675, 0.3675,0.3675],
        'nM':[ 1.15, 1.15, 1.279763, 1.22899, 1.1643, 1.7947, 1.1, 1.1, 1.644877, 2.746524, 1.7947, 1.7947],
        'KvM':[0.0032, 0.0001, 0.0001, 0.0001, 0.00019, 0.001, 0.0001, 0.0001, 0.0001, 0.0001, 0.001, 0.001],
        'KhM-mul':[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        'ThetaRF':[0.01, 0.01, 0.1, 0.1,0.1, 0.1, 0.01, 0.01, 0.1, 0.1, 0.1, 0.1],
        'AlphaF':[7, 7, 10, 10, 10, 10, 7, 7, 10, 10, 10, 10],
        'nF':[2, 2, 1.8, 1.8, 1.8, 1.8, 2, 2, 1.8, 1.8, 1.8, 1.8],
        'KvF':[2.979, 0.126, 1.743746, 1.076128, 1.7437, 1.7437, 0.135, 0.054, 0.840296, 0.606396, 1.7437, 1.7437],
        'KhF-mul':[0.002, 0.002, 1, 1, 1, 1, 0.83, 1, 1, 1, 1, 1],
        'Gamma':[0.08, 0.08, 0.01, 0.01, 0.9, 0.9, 0.08, 0.08, 0.01, 0.01, 0.1, 0.1],
        'ConMulF':[90, 90, 10, 10, 19, 19, 90, 90, 10, 10, 5, 5]
       }

df = pd.DataFrame(soil_dict)

# Creating dt_soillib_water_01.txt and dt_soillib_geom_01.txt
first_row = df.query("Layer.str.startswith('Top') & Type == @settings.top_layer_soil & Macros == @settings.macros_top_soil")
second_row = df.query("Layer.str.startswith('Bot') & Type == @settings.bottom_layer_soil & Macros == @settings.macros_bottom_soil")
#print(second_row)
output_line = pd.concat([first_row, second_row], ignore_index = True)
#print(output_line)
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
crack_lib = pd.DataFrame({'shrink': [1, 1],
'alphaK': [0.74302, 0.62356],
'betaK': [1.30565, 1.23687],
'gammaK': [0.82922, 0.93178]})

out_txt = fix_path(settings.input_folder) + 'dt_soillib_crack_01.txt'
crack_lib.to_csv(out_txt, sep='\t', header=True)
remove_end_blank_line(out_txt)

#creating default dt_soillib_heat_01.txt for top and bottom soil in one file
heat_lib = pd.DataFrame({'H.cap.': [0.711, 0.711],
'cond': [2.772, 2.772],
'C.mul': [1, 1]})

out_txt = fix_path(settings.input_folder) + 'dt_soillib_heat_01.txt'
heat_lib.to_csv(out_txt, sep='\t', header=True)
remove_end_blank_line(out_txt)

#creating default dt_soillib_solute_01.txt for top and bottom soil in one file
solute_lib = pd.DataFrame({'Di.L.M': [0.1, 0.1],
'Di.L.M.': [0.01, 0.01],
'Di.L.F': [0.1, 0.1],
'Di.L.F.': [0.01, 0.01],
'Mol.dif': [3.6e-6, 3.6e-6],
'Gamma': [0, 0]}, dtype=np.float64)

out_txt = fix_path(settings.input_folder) + 'dt_soillib_solute_01.txt'
solute_lib.to_csv(out_txt, sep='\t', header=True)
remove_end_blank_line(out_txt)

#creating geom_layers_01.txt
def generate_geom_layers(user_depth, input_folder):
    second_col = [0.02, 0.05, 0.08, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.25, 0.25, 0.35, 0.5]
    depth = second_col[0]
    i = 1
    while depth < user_depth:
        depth += second_col[i]
        i += 1

    third_col = [0] * i  + [1] * (len(second_col) - i)
    df = pd.DataFrame(data=[second_col, third_col]).T

    out_txt = fix_path(input_folder) + 'geom_layers_01.txt'
    df.to_csv(out_txt, sep='\t', header=False)
    remove_end_blank_line(out_txt)

generate_geom_layers(settings.user_depth, settings.input_folder)


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


print("Soil files generated in output folder!" )


