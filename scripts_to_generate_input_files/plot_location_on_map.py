# Script to show the simulation location on a map.

import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

def show_location_on_map(N, E):
    
    # Define the coordinate in EPSG:3067
    point_epsg3067 = Point(E,N)  # Replace with your own coordinates
    
    # Create a GeoDataFrame with the point
    gdf_point = gpd.GeoDataFrame(geometry=[point_epsg3067], crs="EPSG:3067")
    
    # Load the map of Finland (replace 'path_to_finland_shapefile.shp' with the actual path to Finland's shapefile)
    # You may need to download the shapefile, for example from http://www.naturalearthdata.com/downloads/10m-cultural-vectors/
    finland_shapefile = '../../fi_shp/fi.shp'
    gdf_finland = gpd.read_file(finland_shapefile)
    
    # Ensure the coordinate system of the Finland shapefile is EPSG:3067
    gdf_finland = gdf_finland.to_crs("EPSG:3067")
    
    # Plot the map of Finland and the point
    fig, ax = plt.subplots(figsize=(10, 10))
    gdf_finland.plot(ax=ax, color='lightblue', edgecolor='black')
    gdf_point.plot(ax=ax, color='red', markersize=100)
    
    plt.title("Point on Map of Finland (EPSG:3067)")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    
    # Display the plot
    plt.show()
    

