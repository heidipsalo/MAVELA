import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import rasterio as rio
from rasterio.plot import show
from download_and_format_input_files_helper import fix_path
import settings


def coord_lister(geom):
    coords = []
    if geom.geom_type == 'Polygon':
        coords = list(geom.exterior.coords)
    elif geom.geom_type == 'LineString':
        coords = list(geom.coords)
    elif geom.geom_type == 'Point':
        coords = list(geom.coords)
    else:
        print('Unknown geometry type.')

    return (coords)


def parse_poly_verts(list_of_verts):
    polys = []  # list of polygons by index of vertices
    verts = []  # Indexed list of all vertices
    polId = 0
    for pol in list_of_verts:
        verts_in_poly = []  # indexes of vertices in one polygon

        for vert in pol:
            verts_in_poly.append(polId)
            verts.append(vert)
            polId += 1

        polys.append(verts_in_poly)

    return (polys, verts)


vecdatafiles = ['ar_croptill_01', 'ar_field_01', 'ar_soils_01',
                'ar_network_details_01', 'ar_solute_initial_01',
                'ln_drains_01', 'ln_ditch_surf_01', 'ln_ditch_sub_01',
                'ln_densified_network_01',"ln_network_surf_01",
                'pnt_gwtubes_01', 'pnt_moistsens_01', 'pnt_nwlogger_01',
                'pnt_snowsens_01', 'pnt_soilfrost_01', 'pnt_thermo_01']

rasterfiles = ['geom_dem_01', 'ditch_dem_01']

vecfiletype = '.gpkg'
rastertype = '.tif'


for file in rasterfiles:
    try:
        geom = rio.open(fix_path(settings.temp_folder) + file + rastertype)
    except:
        print("Could not read file:", file)
        continue

    rasWidth = geom.width
    rasHeight = geom.height
    rasRes = geom.res[0]
    rasLeftX, rasLeftY = geom.transform * (0, 0)
    geomtofile = []
    band = geom.read(1)

    geomtofile.append(rasLeftX)
    geomtofile.append(rasLeftY)
    geomtofile.append(rasWidth)
    geomtofile.append(rasHeight)
    geomtofile.append(rasRes)

    for i in range(0, rasHeight):
        for j in range(0, rasWidth):
            geomtofile.append(band[i, j])

    df_geom = pd.DataFrame(geomtofile)

    try:
        df_geom.to_csv(fix_path(settings.input_folder) + file + '.txt', sep='\t', header=False)
        file_data = open(fix_path(settings.input_folder) + file + '.txt', 'rb').read()
        open(fix_path(settings.input_folder) + file + '.txt', 'wb').write(file_data[:-2])
    except:
        print("Could not write file: ", file)

    plt.figure(num='modset')
    #show(geom)

for file in vecdatafiles:
    try:
        geom = gpd.read_file(fix_path(settings.temp_folder) + file + vecfiletype)
    except:
        print("Could not read file:", file)
        continue

    num_of_polys = 0
    num_of_datacols = 0
    num_of_verts = 0
    list_of_datacols = []
    list_of_verts = []
    list_of_polys = []
    data = geom.drop(columns=['geometry'])

    num_of_datacols = len(data.columns)
    list_of_datacols = list(data.columns.values)
    list_of_verts = geom.geometry.apply(coord_lister)
    polys, verts = parse_poly_verts(list_of_verts)
    num_of_verts = len(verts)
    num_of_polys = len(polys)
    list_of_hdr = [(2, '# Grid type'),
                   (num_of_verts, '# Number of verts'),
                   (num_of_polys, '# Number of polys'),
                   (0, '# Number of volys'),
                   (0, '# Regular grid dimensions x'),
                   (0, '# Regular grid dimensions y'),
                   (0, '# Regular grid dimensions z'),
                   (100, '# Color R'),
                   (100, '# Color G'),
                   (100, '# Color B'),
                   (num_of_datacols, '# Number of attached data columns')]

    df_dat = pd.DataFrame(data)
    df_dty = pd.DataFrame(list_of_datacols)
    df_hdr = pd.DataFrame(list_of_hdr)
    df_pol = pd.DataFrame(polys)
    df_vtx = pd.DataFrame(verts)

    filetypes = ['.dat', '.dty', '.hdr', '.pol', '.vtx']
    dfs = [df_dat, df_dty, df_hdr, df_pol, df_vtx]

    for i in range(0, len(dfs)):
        try:
            dfs[i].to_csv(fix_path(settings.input_folder) + file + filetypes[i], sep='\t', header=False)
            file_data = open(fix_path(settings.input_folder) + file + filetypes[i], 'rb').read()
            open(fix_path(settings.input_folder) + file + filetypes[i], 'wb').write(file_data[:-2])
        except:
            print("Could not write file: ", file)
