from gpxencode import gpx
import pyproj
import pandas as pd
import mercantile
import shapely
from xml.dom import minidom as xdmd
from datetime import datetime
from dataclasses import dataclass


wgs84 = pyproj.CRS.from_epsg(4326)
webmerc = pyproj.CRS.from_epsg(3857)
wgs84_2_webmerc = pyproj.Transformer.from_crs(wgs84, webmerc)

@dataclass
class point:
    latitude: float
    longitude: float
    altitude: float

class FlightAwareKML:
    def __init__(self, kml_str):
        self.xml_doc = xdmd.parseString(kml_str)
        self.find_airports()
        self.decode_flight()
        self.to_shapely()
        self.mapstats()
        self.datestats()
    def find_airports(self):
        self.airports = {}
        mode = "origin"
        for placemark in self.xml_doc.getElementsByTagName("Placemark")[:-1]:
            airport_code = placemark.getElementsByTagName("name")[0].firstChild.nodeValue
            self.airports[mode] = {}
            self.airports[mode]["code"] = airport_code
            airport_coords_str = placemark.getElementsByTagName("Point")[0].getElementsByTagName("coordinates")[0].firstChild.nodeValue
            airport_wgs84 = [float(x) for x in airport_coords_str.split(",")]
            self.airports[mode]["point"] = point(airport_wgs84[1], airport_wgs84[0], airport_wgs84[2])
            mode = "destination"
    def decode_flight(self):
        for placemark in self.xml_doc.getElementsByTagName("Placemark")[-1:]:
            self.flight_id = placemark.getElementsByTagName("name")[0].firstChild.nodeValue
            gxtrack = placemark.getElementsByTagName("gx:Track")[0]
            times = gxtrack.getElementsByTagName("when")
            coords = gxtrack.getElementsByTagName("gx:coord")
            times = [datetime.strptime(x.firstChild.nodeValue, "%Y-%m-%dT%H:%M:%SZ") for x in times]
            # coords = [point(*x.firstChild.nodeValue.split(" ")) for x in coords]
            coords = [x.firstChild.nodeValue.split(" ") for x in coords]
            coords = [[float(y) for y in x] for x in coords]
            coords = [point(x[1], x[0], x[2]) for x in coords]
            self.times_count = len(times)
            self.coords_count = len(coords)
            self.flight_path = pd.DataFrame(zip(times, coords), columns=["time", "point"])
            self.flight_path["latitude"] = [x.latitude for x in self.flight_path["point"]]
            self.flight_path["longitude"] = [x.longitude for x in self.flight_path["point"]]
            self.flight_path["altitude"] = [x.altitude for x in self.flight_path["point"]]
    def to_gpx(self):
        gpx_doc = gpx(f"{self.flight_id} - {self.flight_path["time"][0].date()}")
        for ix, row in self.flight_path.iterrows():
            gpx_doc.add_point_to_track(row.latitude, row.longitude, row.time, row.altitude)
        return gpx_doc.doc.toprettyxml()
    def to_shapely(self):
        self.point_airport_origin = shapely.Point([self.airports["origin"]["point"].longitude, self.airports["origin"]["point"].latitude])
        self.point_airport_destination = shapely.Point([self.airports["destination"]["point"].longitude, self.airports["destination"]["point"].latitude])
        self.line = shapely.LineString(self.flight_path[["longitude", "latitude", "altitude"]])
        self.geojson = shapely.to_geojson(self.line)
    def mapstats(self):
        self.latitude_stats = (self.flight_path["latitude"].min(), self.flight_path["latitude"].max())
        self.longitude_stats = (self.flight_path["longitude"].min(), self.flight_path["longitude"].max())
        self.line_mean = list(self.flight_path[["latitude", "longitude"]].mean())
    def datestats(self):
        self.flight_path["date"] = [x.date() for x in self.flight_path["time"]]
        self.date_range = [self.flight_path["date"].min(), self.flight_path["date"].max()]
        self.time_range = [self.flight_path["time"].min(), self.flight_path["time"].max()]
    def zoom(self, height, width):
        ll = [mercantile.tile(self.longitude_stats[0], self.latitude_stats[0], x) for x in range(20)]
        ur = [mercantile.tile(self.longitude_stats[1], self.latitude_stats[1], x) for x in range(20)]
        tile_diffs = list(zip(ll, ur))
        tile_diffs = [[abs(t[1].x - t[0].x) * 256, abs(t[1].y - t[0].y) * 256, abs(t[1].z - t[0].z) * 256] for t in tile_diffs]
        tile_diffs = [t for t in tile_diffs if t[0] < height and t[1] < width]
        zoom = len(tile_diffs)-1
        return zoom