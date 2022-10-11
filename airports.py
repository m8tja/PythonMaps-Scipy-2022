import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from shapely.geometry import Point


def main():

    airports = pd.read_csv("resources/airports", delimiter=",",
                           names=["id", "name", "country", "iata",
                                  "icao", "lat", "long", "altitude",
                                  "timezone", "dst", "tz", "type", "source"])

    airports_geometry = [Point(xy) for xy in zip(airports["long"], airports["lat"])]

    airports_geodata = gpd.GeoDataFrame(airports, crs="EPSG:4326", geometry=airports_geometry)

    fig, ax = plt.subplots(subplot_kw={"projection": ccrs.Robinson()},
                           figsize=(20, 20),
                           facecolor='black')

    ax.patch.set_facecolor('black')

    airports_geodata.plot(ax=ax, transform=ccrs.PlateCarree(),
                      markersize=4, edgecolors='none')

    plt.show()


if __name__ == "__main__":

    main()