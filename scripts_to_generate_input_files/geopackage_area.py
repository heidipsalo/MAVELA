"""Creating geopkg layers for Flush input"""
import geopandas as gpd
from shapely.geometry import Point, Polygon, LineString
from download_and_format_input_files_helper import fix_path
import rasterio as rio
import numpy as np
from rasterio.transform import Affine
import pandas as pd
from generate_default_data_files_helper import remove_end_blank_line
import settings


OFFSET = 0.25  # [m]
IMPACT_DIST_OPEN_DITCH = 230  # [m]

def calculate_area_coords(point, size):
    coords = []

    # Bottom left
    coords.append(point)

    # Top left
    x = point[0]
    y = point[1] + size
    coords.append((x, y))

    # Top right
    x = point[0] + size
    y = point[1] + size
    coords.append((x, y))

    # Bottom right
    x = point[0] + size
    y = point[1]
    coords.append((x, y))

    # Bottom left as end point
    coords.append(point)

    return coords


ca_x = float(settings.coordinates[1])  # lower left corner
ca_y = float(settings.coordinates[0])  # ca - computational area

# Give size for area polygons size(croptill) > size(soils) > size(field)
# Computational area = settings.drain_spacing

# Field area, bottom left corner
fa_x = ca_x - OFFSET
fa_y = ca_y - OFFSET
fa_length = settings.drain_spacing + 2*OFFSET
fa_coords = calculate_area_coords((fa_x, fa_y), fa_length)
fa_poly = Polygon(fa_coords)

# Network details (nd) area, bottom left corner
nd_x = ca_x - OFFSET
nd_y = ca_y - OFFSET
nd_length = settings.drain_spacing + 2*OFFSET
nd_coords = calculate_area_coords((nd_x, nd_y), nd_length)
nd_poly = Polygon(nd_coords)

# Solute initial (si) area, bottom left corner
si_x = ca_x - OFFSET
si_y = ca_y - OFFSET
si_length = settings.drain_spacing + 2*OFFSET
si_coords = calculate_area_coords((si_x, si_y), si_length)
si_poly = Polygon(si_coords)

# Soils area, bottom left corner
sa_x = ca_x - 2*OFFSET
sa_y = ca_y - 2*OFFSET
sa_length = settings.drain_spacing + 4*OFFSET
sa_coords = calculate_area_coords((sa_x, sa_y), sa_length)
sa_poly = Polygon(sa_coords)

# Croptill area, bottom left corner
# Widen croptill area to include ghost cells around computational area
cra_x = ca_x - settings.drain_spacing
cra_y = ca_y - settings.drain_spacing
cra_length = 3 * settings.drain_spacing
cra_coords = calculate_area_coords((cra_x, cra_y), cra_length)
cra_poly = Polygon(cra_coords)

# Create DataFrames for the field geopkg layers
gdf_field = gpd.GeoDataFrame(columns=['Id', 'Included', 'geometry'], crs='epsg:3067')
gdf_field.loc[0] = [1, 1, fa_poly]
gdf_field.set_geometry(col='geometry', inplace=True)
gdf_field.to_file(fix_path(settings.temp_folder)+'ar_field_01.gpkg', driver='GPKG', layer='field', crs='epsg:3067')

# Create DataFrames for the soils geopkg layers
gdf_soils = gpd.GeoDataFrame(columns=['Id', 'Area', 'geometry'], crs='epsg:3067')
gdf_soils.loc[0] = [1, 0, sa_poly]
gdf_soils.set_geometry(col='geometry', inplace=True)
gdf_soils.to_file(fix_path(settings.temp_folder)+'ar_soils_01.gpkg', driver='GPKG', layer='soils', crs='epsg:3067')

# Create DataFrames for the croptill geopkg layers
gdf_croptill = gpd.GeoDataFrame(columns=['Id', 'Area', 'geometry'], crs='epsg:3067')
gdf_croptill.loc[0] = [1, 0, cra_poly]
gdf_croptill.set_geometry(col='geometry', inplace=True)
gdf_croptill.to_file(fix_path(settings.temp_folder)+'ar_croptill_01.gpkg', driver='GPKG', layer='croptill', crs='epsg:3067')

# Create DataFrames for the network details geopkg layers
gdf_network_details = gpd.GeoDataFrame(columns=['Id', 'Area', 'geometry'], crs='epsg:3067')
gdf_network_details.loc[0] = [0, 0, nd_poly]
gdf_network_details.set_geometry(col='geometry', inplace=True)
gdf_network_details.to_file(fix_path(settings.temp_folder)+'ar_network_details_01.gpkg', driver='GPKG', layer='network_details', crs='epsg:3067')

# Create DataFrames for the solute initial geopkg layers
gdf_solute_initial = gpd.GeoDataFrame(columns=['Id', 'Area', 'geometry'], crs='epsg:3067')
gdf_solute_initial.loc[0] = [0, 0, si_poly]
gdf_solute_initial.set_geometry(col='geometry', inplace=True)
gdf_solute_initial.to_file(fix_path(settings.temp_folder)+'ar_solute_initial_01.gpkg', driver='GPKG', layer='solute_initial', crs='epsg:3067')


# Line Drains, representing subsurface drain pipe
resist = 0.5 * settings.drain_spacing
od_x1 = ca_x + 2
od_y1 = ca_y - 1
od_x2 = od_x1
od_y2 = ca_y + settings.drain_spacing + 1
od_line = LineString([[od_x1, od_y1],[od_x2, od_y2]])
gdf_od = gpd.GeoDataFrame(columns=['id', 'network', 'depth', 'diam', 'press','resis','control', 'geometry'], crs='epsg:3067')
if settings.drain_type == "Control":
    gdf_od.loc[0] = [0, 0, settings.user_depth, 0.05, 0, resist, settings.control_level, od_line]
else:
    gdf_od.loc[0] = [0, 0, settings.user_depth, 0.05, 0, resist, 1, od_line]
gdf_od.set_geometry(col='geometry', inplace=True)
gdf_od.to_file(fix_path(settings.temp_folder)+'ln_drains_01.gpkg', driver='GPKG', layer='ln_drains_01', crs='epsg:3067')

# Line Ditch Sub Surf domain of open ditch
ssd_x1 = ca_x + settings.drain_spacing - 2
ssd_y1 = od_y1
ssd_x2 = ssd_x1
ssd_y2 = od_y2
ssd_line = LineString([[ssd_x1, ssd_y1],[ssd_x2, ssd_y2]])
gdf_ssd = gpd.GeoDataFrame(columns=['id', 'network', 'depth', 'width', 'wat_level','resis', 'geometry'], crs='epsg:3067')
if settings.open_ditch == "N":
    gdf_ssd.loc[0] = [0, 0, 1, 1, 1, 1, ssd_line]
else:
    if settings.open_ditch_dist >= IMPACT_DIST_OPEN_DITCH:
        gdf_ssd.loc[0] = [0, 0, 1, 1, 1, 1, ssd_line]
    else:
        val1 = 1/IMPACT_DIST_OPEN_DITCH * settings.open_ditch_dist
        gdf_ssd.loc[0] = [0, 0, 1, 1, val1, 1, ssd_line]

gdf_ssd.set_geometry(col='geometry', inplace=True)
gdf_ssd.to_file(fix_path(settings.temp_folder)+'ln_ditch_sub_01.gpkg', driver='GPKG', layer='ln_ditch_sub_01', crs='epsg:3067')

# Line Ditch Surf domain of open ditch
sd_x1 = ca_x + settings.drain_spacing - 2
sd_y1 = od_y1
sd_x2 = sd_x1
sd_y2 = od_y2
sd_line = LineString([[sd_x1, sd_y1],[sd_x2, sd_y2]])
gdf_sd = gpd.GeoDataFrame(columns=['id', 'network', 'depth', 'width', 'wat_level','resis', 'geometry'], crs='epsg:3067')
if settings.open_ditch == "N":
    gdf_sd.loc[0] = [0, 0, 1, 1, 1, 1, sd_line]
else:
    if settings.open_ditch_dist >= IMPACT_DIST_OPEN_DITCH:
        gdf_sd.loc[0] = [0, 0, 1, 1, 1, 1, sd_line]
    else:
        val2 = 1/IMPACT_DIST_OPEN_DITCH * settings.open_ditch_dist
        gdf_sd.loc[0] = [0, 0, 1, 1, val2, 1, sd_line]

gdf_sd.set_geometry(col='geometry', inplace=True)
gdf_sd.to_file(fix_path(settings.temp_folder)+'ln_ditch_surf_01.gpkg', driver='GPKG', layer='ln_ditch_surf_01', crs='epsg:3067')



# Line Densified Network
dn_x1 = ca_x + settings.drain_spacing + 1
dn_y1 = ca_y - 1
dn_x2 = dn_x1
dn_y2 = ca_y + settings.drain_spacing + 1
dn_line = LineString([[dn_x1, dn_y1],[dn_x2, dn_y2]])
gdf_dn = gpd.GeoDataFrame(columns=['branch_id', 'cross_sec', 'depth', 'geometry'], crs='epsg:3067')
gdf_dn.loc[0] = [0, 0, 0, dn_line]
gdf_dn.set_geometry(col='geometry', inplace=True)
gdf_dn.to_file(fix_path(settings.temp_folder)+'ln_densified_network_01.gpkg', driver='GPKG', layer='ln_densified_network_01', crs='epsg:3067')


# Line Network Surf
ns_x1 = ca_x + settings.drain_spacing + 1
ns_y1 = ca_y - 1
ns_x2 = ns_x1
ns_y2 = ca_y + settings.drain_spacing + 1
ns_line = LineString([[ns_x1, ns_y1],[ns_x2, ns_y2]])
gdf_ns = gpd.GeoDataFrame(columns=['id', 'geometry'], crs='epsg:3067')
gdf_ns.loc[0] = [0, dn_line]
gdf_ns.set_geometry(col='geometry', inplace=True)
gdf_ns.to_file(fix_path(settings.temp_folder)+'ln_network_surf_01.gpkg', driver='GPKG', layer='ln_network_surf_01', crs='epsg:3067')


# 1 Point Ground Water Tubes
gwt_x = ca_x + 4
gwt_y = ca_y + settings.drain_spacing - 4
gwt_point = Point(gwt_x, gwt_y)
gdf_gwt = gpd.GeoDataFrame(columns=['id', 'geometry'], crs='epsg:3067')
gdf_gwt.loc[0] = [0, gwt_point]
gdf_gwt.set_geometry(col='geometry', inplace=True)
gdf_gwt.to_file(fix_path(settings.temp_folder)+'pnt_gwtubes_01.gpkg', driver='GPKG', layer='pnt_gwtubes_01', crs='epsg:3067')

# 2 Point Moist Sens is the same spot as Ground Water Tubes
gdf_gwt_2 = gpd.GeoDataFrame(columns=['id', 'depth', 'geometry'], crs='epsg:3067')
gdf_gwt_2.loc[0] = [0, 0.3, gwt_point]
gdf_gwt_2.set_geometry(col='geometry', inplace=True)
gdf_gwt_2.to_file(fix_path(settings.temp_folder)+'pnt_moistsens_01.gpkg', driver='GPKG', layer='pnt_moistsens_01', crs='epsg:3067')

# 3 Point Nwlogger in the same spot as Ground Water Tubes
gdf_gwt_3 = gpd.GeoDataFrame(columns=['id', 'geometry'], crs='epsg:3067')
gdf_gwt_3.loc[0] = [0, gwt_point]
gdf_gwt_3.set_geometry(col='geometry', inplace=True)
gdf_gwt_3.to_file(fix_path(settings.temp_folder)+'pnt_nwlogger_01.gpkg', driver='GPKG', layer='pnt_nwlogger_01', crs='epsg:3067')

# 4 Point Snow Sensor in the same spot as Ground Water Tubes
gdf_gwt_4 = gpd.GeoDataFrame(columns=['id', 'geometry'], crs='epsg:3067')
gdf_gwt_4.loc[0] = [0, gwt_point]
gdf_gwt_4.set_geometry(col='geometry', inplace=True)
gdf_gwt_4.to_file(fix_path(settings.temp_folder)+'pnt_snowsens_01.gpkg', driver='GPKG', layer='pnt_snowsens_01', crs='epsg:3067')

# 5 Point Soil Frost in the same spot as Ground Water Tubes
gdf_gwt_5 = gpd.GeoDataFrame(columns=['id', 'geometry'], crs='epsg:3067')
gdf_gwt_5.loc[0] = [0, gwt_point]
gdf_gwt_5.set_geometry(col='geometry', inplace=True)
gdf_gwt_5.to_file(fix_path(settings.temp_folder)+'pnt_soilfrost_01.gpkg', driver='GPKG', layer='pnt_soilfrost_01', crs='epsg:3067')

# 6 Point Thermo in the same spot as Ground Water Tubes
gdf_gwt_6 = gpd.GeoDataFrame(columns=['id', 'depth', 'geometry'], crs='epsg:3067')
gdf_gwt_6.loc[0] = [0, 0.3,  gwt_point]
gdf_gwt_6.set_geometry(col='geometry', inplace=True)
gdf_gwt_6.to_file(fix_path(settings.temp_folder)+'pnt_thermo_01.gpkg', driver='GPKG', layer='pnt_thermo_01', crs='epsg:3067')

# Creating a raster file with an even settings.slope for DEM
res = settings.drain_spacing / 5
grid_size = 10 * settings.drain_spacing
x = np.arange(cra_x-0.5*grid_size, cra_x+0.5*grid_size, res)
y = np.arange(cra_y+0.5*grid_size, cra_y-0.5*grid_size, -res)
X, Y = np.meshgrid(x, y)
Z = 10 + X * settings.slope

# DEM resolution (pixel size = settings.drain_spacing/5)
res = settings.drain_spacing / 5

transform = Affine.translation(x[0]-res/2, y[0]-res/2) * Affine.scale(res, res)

with rio.open(
    fix_path(settings.temp_folder)+'geom_dem_01.tif', 'w', driver='GTiff', height=Z.shape[0],
    width=Z.shape[1], count=1, dtype=Z.dtype, crs='epsg:3067',
    transform=transform) as new_dataset:

    new_dataset.write(Z, 1)


with rio.open(
    fix_path(settings.temp_folder)+'ditch_dem_01.tif', 'w', driver='GTiff', height=Z.shape[0],
    width=Z.shape[1], count=1, dtype=Z.dtype, crs='epsg:3067',
    transform=transform) as new_dataset:

    new_dataset.write(Z, 1)


# Creating txt Control files

# Create: st_geometry_01.txt
data = pd.DataFrame(index=range(9), columns=['data', 'comments'])
data['data'].iloc[0] = '-'
data['data'].iloc[1] = ca_x
data['data'].iloc[2] = ca_y
data['data'].iloc[3] = settings.drain_spacing
data['data'].iloc[4:8] = 1
data['data'].iloc[8] = 0

data['comments'].iloc[0] = '# Grid settings'
data['comments'].iloc[1] = '# x-coordinate of the lower left corner of the grid [m]'
data['comments'].iloc[2] = '# y-coordinate of the lower left corner of the grid [m]'
data['comments'].iloc[3] = '# Cell width and length [m]'
data['comments'].iloc[4] = '# Number of cells in x-dimension [-] 4'
data['comments'].iloc[5] = '# Number of cells in y-dimension [-] 4'
data['comments'].iloc[6] = '# Number of processes in x-dimension [-]16'
data['comments'].iloc[7] = '# Number of processes in y-dimension [-]17'
data['comments'].iloc[8] = '# Grid rotation angle'

out_txt = fix_path(settings.input_folder) + 'st_geometry_01.txt'
data.to_csv(out_txt, sep='\t', header=False)
remove_end_blank_line(out_txt)


# Create: st_general_01.txt
data = pd.DataFrame(index=range(6), columns=['data', 'comments'])
data['data'].iloc[0] = '-'
data['data'].iloc[1] = 0
data['data'].iloc[2] = 8759
data['data'].iloc[3] = 1
data['data'].iloc[4] = 4
data['data'].iloc[5] = 6

data['comments'].iloc[0] = '# General settings'
data['comments'].iloc[1] = '# Start time [h] 5856'
data['comments'].iloc[2] = '# End time [h] 8784'
data['comments'].iloc[3] = '# Global time step [h]'
data['comments'].iloc[4] = '# Min time step subdivisions [-], 0 = 1 h, 10 = 3.52 s'
data['comments'].iloc[5] = '# Max time step subdivisions [-], 0 = 1 h, 10 = 3.52 s'

out_txt = fix_path(settings.input_folder) + 'st_general_01.txt'
data.to_csv(out_txt, sep='\t', header=False)
remove_end_blank_line(out_txt)


print("Geopackages generated!")
