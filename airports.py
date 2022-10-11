import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from shapely.geometry import Point, LineString


def main():

    airports = pd.read_csv("resources/airports", delimiter=",",
                           names=["id", "name", "country", "iata",
                                  "icao", "lat", "long", "altitude",
                                  "timezone", "dst", "tz", "type", "source"])

    airports_geometry = [Point(xy) for xy in zip(airports["long"], airports["lat"])]

    airports_geodata = gpd.GeoDataFrame(airports, crs="EPSG:4326", geometry=airports_geometry)

    routes = pd.read_csv("resources/routes", delimiter=",",
                         names=["airline", "id", "source_airport",
                                "source_airport_id", "destination_airport",
                                "destination_airport_id", "codeshare",
                                "stops", "equitment"])

    source_airports = airports[["name", "iata", "icao", "lat", "long"]]
    destination_airports = source_airports.copy()
    source_airports.columns = [str(col) + "_source" for col in source_airports.columns]
    destination_airports.columns = [str(col) + "_destination" for col in destination_airports.columns]

    routes = routes[["source_airport", "destination_airport"]]

    routes = pd.merge(routes,
                      source_airports,
                      left_on="source_airport",
                      right_on="iata_source")

    routes = pd.merge(routes,
                      destination_airports,
                      left_on="destination_airport",
                      right_on="iata_destination")

    routes_geometry = [LineString([[routes.iloc[i]["long_source"],
                                    routes.iloc[i]["lat_source"]],
                                   [routes.iloc[i]["long_destination"],
                                    routes.iloc[i]["lat_destination"]]])
                       for i in range(routes.shape[0])]

    routes_geodata = gpd.GeoDataFrame(routes, geometry=routes_geometry, crs="EPSG:4326")

    fig, ax = plt.subplots(figsize=(20, 20), subplot_kw={"projection": ccrs.Robinson()})
    ax.patch.set_facecolor("black")

    routes_geodata.plot(ax=ax, color="white", linewidth=0.1,
                        transform=ccrs.Geodetic(),
                        alpha=0.1)

    plt.setp(ax.spines.values(), color="black")
    plt.setp([ax.get_xticklines(), ax.get_yticklines()], color="black")
    ax.set_ylim(-7000000, 8800000)
    plt.show()


if __name__ == "__main__":

    main()
