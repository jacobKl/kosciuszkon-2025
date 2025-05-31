from shapely.geometry import Polygon
import requests
import json
from pydantic import BaseModel
from shapely.geometry import Polygon, shape
from shapely.ops import transform
from geopy.distance import geodesic


class Address(BaseModel):
    street: str | None = None
    number: str | None = None
    postalcode: str | None = None
    city: str | None = None
    external_garage_count: str | None = None

    def __str__(self):
        return f"{self.street} {self.number}, {self.postalcode} {self.city}"

    def as_dict(self):
        return {
            "street": self.street,
            "number": self.number,
            "postalcode": self.postalcode,
            "city": self.city,
            "external_garage_count": self.external_garage_count
        }


def filter_buildings(osm_data):
    if not osm_data or "elements" not in osm_data:
        return
    for element in osm_data["elements"]:
        print(element)


def add_bbox_to_properties(feature_collection):
    for feature in feature_collection["features"]:
        geometry = feature.get("geometry", {})
        if geometry.get("type") != "Polygon":
            continue

        coordinates = geometry.get("coordinates", [])
        if not coordinates:
            continue

        polygon = Polygon(coordinates[0])
        rotated_bbox = polygon.minimum_rotated_rectangle

        coords = list(rotated_bbox.exterior.coords)[:-1]
        corners = [[x, y] for x, y in coords]

        feature.setdefault("properties", {})["bbox"] = corners

    return feature_collection


def find_nearest_feature(data, lat, lon):
    nearest_feature = None
    min_distance = float('inf')

    for feature in data["features"]:
        # Zakładamy typ Polygon
        coordinates = feature["geometry"]["coordinates"][0]
        polygon = Polygon(coordinates)
        centroid = polygon.centroid
        centroid_latlon = (centroid.y, centroid.x)

        dist = geodesic((lat, lon), centroid_latlon).meters
        if dist < min_distance:
            min_distance = dist
            nearest_feature = feature

    return nearest_feature


def find_main_and_n_nearest_without_housenumber(data, lat, lon, n=5):
    n = int(n)
    all_features = []

    for feature in data["features"]:
        coordinates = feature["geometry"]["coordinates"][0]
        polygon = Polygon(coordinates)
        centroid = polygon.centroid
        feature["_centroid"] = (centroid.y, centroid.x)
        all_features.append(feature)

    # Znajdź najbliższy budynek
    main_feature = min(
        all_features,
        key=lambda f: geodesic((lat, lon), f["_centroid"]).meters
    )
    main_centroid = main_feature["_centroid"]

    # Znajdź n najbliższych bez addr_housenumber, pomijając główny
    others = []
    for feature in all_features:
        if feature == main_feature:
            continue
        if "addr_housenumber" in feature.get("properties", {}):
            continue
        distance = geodesic(main_centroid, feature["_centroid"]).meters
        others.append({
            "feature": feature,
            "distance_m": distance
        })

    others.sort(key=lambda f: f["distance_m"])
    nearest_without_housenumber = [item["feature"] for item in others[:n]]

    # Usuń pomocnicze "_centroid" przed zwrotem
    for feature in [main_feature] + nearest_without_housenumber:
        feature.pop("_centroid", None)

    return {
        "type": "FeatureCollection",
        "features": [main_feature] + nearest_without_housenumber
    }


def calculate_average_centroid(feature_collection):
    lat_sum = 0
    lon_sum = 0
    count = 0

    for feature in feature_collection["features"]:
        geometry = feature.get("geometry", {})
        if geometry.get("type") != "Polygon":
            continue

        coordinates = geometry.get("coordinates", [])
        if not coordinates:
            continue

        polygon = Polygon(coordinates[0])  # pierwszy pierścień
        centroid = polygon.centroid
        lat_sum += centroid.y
        lon_sum += centroid.x
        count += 1

    if count == 0:
        return None  # brak poligonów

    avg_lat = lat_sum / count
    avg_lon = lon_sum / count

    return (avg_lat, avg_lon)


def check_address(address: dict[str, str]) -> bool:
    if not address or not isinstance(address, dict):
        return False
    if "street" not in address or not isinstance(address["street"], str):
        return False
    if "number" not in address or not isinstance(address["number"], str):
        return False
    if "postalcode" not in address or not isinstance(address["postalcode"], str):
        return False
    if "city" not in address or not isinstance(address["city"], str):
        return False
    return True


def geocode_address(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json", "limit": 1, "addressdetails": 1}
    headers = {"User-Agent": "3D-Map-Visual"}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    return float(data[0]["lat"]), float(data[0]["lon"])


def create_bbox(lat, lon, delta=0.001):
    return lat - delta, lon - delta, lat + delta, lon + delta


def query_buildings(bbox):
    south, west, north, east = bbox
    query = f"""
    [out:json][timeout:25];
    (
      way["building"]({south},{west},{north},{east});
    );
    out body;
    >;
    out skel qt;
    """
    url = "http://overpass-api.de/api/interpreter"
    response = requests.post(url, data={"data": query})
    return response.json()


def osm_to_geojson(osm_data):
    nodes = {el["id"]: (el["lon"], el["lat"])
             for el in osm_data["elements"] if el["type"] == "node"}
    features = []

    for el in osm_data["elements"]:
        if el["type"] == "way" and "nodes" in el:
            coords = [nodes[n] for n in el["nodes"] if n in nodes]
            if len(coords) >= 3:
                coords.append(coords[0])
                props = {}
                tags = el.get("tags", {})

                # Wysokość budynku
                if "height" in tags:
                    props["height"] = float(tags["height"])
                elif "building:levels" in tags:
                    props["height"] = int(tags["building:levels"]) * 3
                else:
                    props["height"] = 10  # domyślna

                # Dach
                for roof_tag in ["roof:shape", "roof:height", "roof:angle", "roof:direction", "roof:material"]:
                    if roof_tag in tags:
                        props[roof_tag.replace(
                            "roof:", "roof_")] = tags[roof_tag]

                # Adres i nazwa
                for addr_tag in ["addr:street", "addr:housenumber", "addr:city", "name"]:
                    if addr_tag in tags:
                        props[addr_tag.replace(
                            "addr:", "addr_")] = tags[addr_tag]

                features.append({
                    "type": "Feature",
                    "properties": props,
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[list(c) for c in coords]]
                    }
                })

    return {
        "type": "FeatureCollection",
        "features": features
    }
