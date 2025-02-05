"""generate_gis_files.py"""
import pandas as pd
from generate_default_data_files_helper import remove_end_blank_line
from download_and_format_input_files_helper import fix_path
import settings


# Create: st_geometry_01.txt
#ll_x = settings.drain_spacing
#ll_y = -2* settings.drain_spacing

#data = pd.DataFrame(index=range(9), columns=['data', 'comments'])
#data['data'].iloc[0] = '-'
#data['data'].iloc[1] = ll_x
#data['data'].iloc[2] = ll_y
#data['data'].iloc[3] = settings.drain_spacing
#data['data'].iloc[4:8] = 1
#data['data'].iloc[8] = 0

#data['comments'].iloc[0] = '# Grid settings'
#data['comments'].iloc[1] = '# x-coordinate of the lower left corner of the grid [m]'
#data['comments'].iloc[2] = '# y-coordinate of the lower left corner of the grid [m]'
#data['comments'].iloc[3] = '# Cell width and length [m]'
#data['comments'].iloc[4] = '# Number of cells in x-dimension [-] 4'
#data['comments'].iloc[5] = '# Number of cells in y-dimension [-] 4'
#data['comments'].iloc[6] = '# Number of processes in x-dimension [-]16'
#data['comments'].iloc[7] = '# Number of processes in y-dimension [-]17'
#data['comments'].iloc[8] = '# Grid rotation angle'

#out_txt = fix_path(settings.output_folder) + 'st_geometry_01_from_gengisf.txt'
#data.to_csv(out_txt, sep='\t', header=False)
#remove_end_blank_line(out_txt)


# Create: st_general_01.txt

#data = pd.DataFrame(index=range(6), columns=['data', 'comments'])
#data['data'].iloc[0] = '-'
#data['data'].iloc[1] = 0
#data['data'].iloc[2] = 8759
#data['data'].iloc[3] = 1
#data['data'].iloc[4] = 4
#data['data'].iloc[5] = 6

#data['comments'].iloc[0] = '# General settings'
#data['comments'].iloc[1] = '# Start time [h] 5856'
#data['comments'].iloc[2] = '# End time [h] 8784'
#data['comments'].iloc[3] = '# Global time step [h]'
#data['comments'].iloc[4] = '# Min time step subdivisions [-], 0 = 1 h, 10 = 3.52 s'
#data['comments'].iloc[5] = '# Max time step subdivisions [-], 0 = 1 h, 10 = 3.52 s'

#out_txt = fix_path(settings.output_folder) + 'st_general_01_from_gengisfile.txt'
#data.to_csv(out_txt, sep='\t', header=False)
#remove_end_blank_line(out_txt)


# Create: geom_dem_01.txt. It is a script for manual generation of a file (slope does not work correctly for bigger matrix)

#data = pd.DataFrame(index=range(5+3*3), columns=['data', 'comments'])
#data['data'].iloc[0] = 0
#data['data'].iloc[1] = 0
#data['data'].iloc[2] = 3
#data['data'].iloc[3] = 3
#data['data'].iloc[4] = settings.drain_spacing

#data['comments'].iloc[0] = '# X-coordinate of the upper left corner [m]'
#data['comments'].iloc[1] = '# Y-coordinate of the upper left corner [m]'
#data['comments'].iloc[2] = '# Number of columns'
#data['comments'].iloc[3] = '# Number of rows'
#data['comments'].iloc[4] = '# Pixel dimensions [m]'

#data['data'].iloc[5:8] = 10
#data['data'].iloc[8:11] = 10 - settings.drain_spacing * settings.slope
#data['data'].iloc[11:14] = 10 - 2* settings.drain_spacing * settings.slope


#out_txt = fix_path(settings.temp_folder) + 'geom_dem_01.txt'
#data.to_csv(out_txt, sep='\t', header=False)
#remove_end_blank_line(out_txt)

#print("GIS control files generated!")
