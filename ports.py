import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from shapely.geometry import Point


def main():

    ports = pd.read_csv("resources/ports.csv")

    port_geometry = [Point(xy) for xy in zip(ports['lon'], ports['lat'])]
    port_geodata = gpd.GeoDataFrame(ports, crs="EPSG:4236", geometry=port_geometry)

    fig, ax = plt.subplots(subplot_kw={"projection": ccrs.Robinson()},
                           figsize=(20, 20),
                           facecolor='black')

    ax.patch.set_facecolor('black')

    port_geodata.plot(ax=ax, transform=ccrs.PlateCarree(),
                      markersize=4, edgecolors='none')

    plt.show()


if __name__ == "__main__":

    main()