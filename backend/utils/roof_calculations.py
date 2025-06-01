import math
import numpy as np

from utils.solar_panel import calculate_panel_output


def scale_values(values, center):
    """
    Przekształca współrzędne geograficzne (lon, lat) względem punktu odniesienia do metrów.

    Args:
        values (list): Lista [lon, lat] punktów.
        center (list): Punkt odniesienia [lon, lat].

    Returns:
        list: Lista punktów [x, y] w metrach względem punktu odniesienia.
    """
    R = 6371000  # promień Ziemi w metrach
    center_lon, center_lat = map(math.radians, center)

    scaled = []
    for lon, lat in values:
        lon_rad = math.radians(lon)
        lat_rad = math.radians(lat)

        delta_lon = lon_rad - center_lon
        delta_lat = lat_rad - center_lat

        x = delta_lon * math.cos((lat_rad + center_lat) / 2) * R
        y = delta_lat * R

        scaled.append([x, y])

    return scaled


def distance(point1, point2):
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)


def average_point(p1, p2, p3, p4):
    x = (p1[0] + p2[0] + p3[0] + p4[0]) / 4
    y = (p1[1] + p2[1] + p3[1] + p4[1]) / 4
    return [x, y]


def get_roof_top_coordinates(roof_data, center, house_height, roof_type='flat'):
    center = [center['lon'], center['lat']]
    roof_data = scale_values(roof_data, center)
    """
    Extract the roof top coordinates from the roof data.

    Args:
        roof_data (dict): Dictionary containing roof data with 'coordinates' key.

    Returns:
        list: List of roof top coordinates.
    """
    if roof_type == 'flat':
        house_data = {
            "corners": {
                "most_northern": sorted(roof_data, key=lambda x: x[1], reverse=True)[0],
                "most_southern": sorted(roof_data, key=lambda x: x[1])[0],
                "most_western": sorted(roof_data, key=lambda x: x[0])[0],
                "most_eastern": sorted(roof_data, key=lambda x: x[0], reverse=True)[0]
            }
        }
        solar_panels = place_solar_panel_on_roof_planes(
            {'corners': house_data['corners'], 'type': 'flat'})
        solar_panels_output = {
            'clear': calculate_panel_output(
                center[1], center[0], 30, 180, solar_panels['solar_area'], 0.18, 'clear', None),
            'partly_cloudy': calculate_panel_output(
                center[1], center[0], 30, 180, solar_panels['solar_area'], 0.18, 'partly_cloudy', None),
            'cloudy': calculate_panel_output(
                center[1], center[0], 30, 180, solar_panels['solar_area'], 0.18, 'cloudy', None),
            'rain': calculate_panel_output(
                center[1], center[0], 30, 180, solar_panels['solar_area'], 0.18, 'rain', None)
        }
        house_data['corners']['most_northern'].append(
            house_data['corners']['most_northern'][1])
        house_data['corners']['most_southern'].append(
            house_data['corners']['most_southern'][1])
        house_data['corners']['most_western'].append(
            house_data['corners']['most_western'][1])
        house_data['corners']['most_eastern'].append(
            house_data['corners']['most_eastern'][1])

        house_data['corners']['most_northern'][1] = house_height
        house_data['corners']['most_southern'][1] = house_height
        house_data['corners']['most_western'][1] = house_height
        house_data['corners']['most_eastern'][1] = house_height

        roof_bounding_points = {
            1: [
                [house_data['corners']['most_northern'], house_data['corners']
                    ['most_western'], house_data['corners']['most_southern']],
                [house_data['corners']['most_southern'], house_data['corners']
                    ['most_eastern'], house_data['corners']['most_northern']]
            ]
        }
        solar_panels = {
            "coordinates": solar_panels['rectangles'],
            "solar_area": solar_panels['solar_area'],
            "slope_deg": solar_panels['slope_deg'],
            "solar_output": solar_panels_output
        }
        return {"roof": roof_bounding_points, "solar_panels": solar_panels}
    elif roof_type == 'gable':
        house_data = {
            "corners": {
                "most_northern": sorted(roof_data, key=lambda x: x[1], reverse=True)[0],
                "most_southern": sorted(roof_data, key=lambda x: x[1])[0],
                "most_western": sorted(roof_data, key=lambda x: x[0])[0],
                "most_eastern": sorted(roof_data, key=lambda x: x[0], reverse=True)[0]
            }
        }

        house_data['roof_edges'] = {
            1: [[(house_data['corners']['most_northern'][0] + house_data['corners']['most_western'][0]) / 2, distance([(house_data['corners']['most_northern'][0] + house_data['corners']['most_western'][0]) / 2, (house_data['corners']['most_northern'][1] + house_data['corners']['most_western'][1]) / 2], [house_data['corners']['most_western'][0], house_data['corners']['most_western'][1]]) + house_height, (house_data['corners']['most_northern'][1] + house_data['corners']['most_western'][1]) / 2],
                [(house_data['corners']['most_southern'][0] + house_data['corners']['most_eastern'][0]) / 2, distance([(house_data['corners']['most_southern'][0] + house_data['corners']['most_eastern'][0]) / 2, (house_data['corners']['most_southern'][1] + house_data['corners']['most_eastern'][1]) / 2], [house_data['corners']['most_eastern'][0], house_data['corners']['most_eastern'][1]]) + house_height, (house_data['corners']['most_southern'][1] + house_data['corners']['most_eastern'][1]) / 2]],
            2: [[(house_data['corners']['most_northern'][0] + house_data['corners']['most_eastern'][0]) / 2, distance([(house_data['corners']['most_northern'][0] + house_data['corners']['most_eastern'][0]) / 2, (house_data['corners']['most_northern'][1] + house_data['corners']['most_eastern'][1]) / 2], [house_data['corners']['most_eastern'][0], house_data['corners']['most_eastern'][1]]) + house_height, (house_data['corners']['most_northern'][1] + house_data['corners']['most_eastern'][1]) / 2],
                [(house_data['corners']['most_southern'][0] + house_data['corners']['most_western'][0]) / 2, distance([(house_data['corners']['most_southern'][0] + house_data['corners']['most_western'][0]) / 2, (house_data['corners']['most_southern'][1] + house_data['corners']['most_western'][1]) / 2], [house_data['corners']['most_western'][0], house_data['corners']['most_western'][1]]) + house_height, (house_data['corners']['most_southern'][1] + house_data['corners']['most_western'][1]) / 2]]
        }
        house_data['corners']['most_northern'].append(
            house_data['corners']['most_northern'][1])
        house_data['corners']['most_southern'].append(
            house_data['corners']['most_southern'][1])
        house_data['corners']['most_western'].append(
            house_data['corners']['most_western'][1])
        house_data['corners']['most_eastern'].append(
            house_data['corners']['most_eastern'][1])

        house_data['corners']['most_northern'][1] = house_height
        house_data['corners']['most_southern'][1] = house_height
        house_data['corners']['most_western'][1] = house_height
        house_data['corners']['most_eastern'][1] = house_height
        roof_bounding_points = {
            1: [
                [house_data['corners']['most_northern'], house_data['corners']
                    ['most_western'], house_data['roof_edges'][1][0]],
                [house_data['corners']['most_southern'], house_data['corners']
                    ['most_eastern'], house_data['roof_edges'][1][1]],
                [house_data['corners']['most_northern'], house_data['corners']
                    ['most_eastern'], house_data['roof_edges'][1][1]],
                [house_data['corners']['most_northern'], house_data['roof_edges']
                    [1][0], house_data['roof_edges'][1][1]],
                [house_data['corners']['most_western'], house_data['roof_edges']
                    [1][0], house_data['roof_edges'][1][1]],
                [house_data['corners']['most_southern'],
                    house_data['corners']['most_western'], house_data['roof_edges'][1][1]],
            ],
            2: [
                [house_data['corners']['most_northern'], house_data['corners']
                    ['most_eastern'], house_data['roof_edges'][2][0]],
                [house_data['corners']['most_southern'], house_data['corners']
                    ['most_western'], house_data['roof_edges'][2][1]],
                [house_data['corners']['most_northern'], house_data['corners']
                    ['most_western'], house_data['roof_edges'][2][1]],
                [house_data['corners']['most_northern'], house_data['roof_edges']
                    [2][0], house_data['roof_edges'][2][1]],
                [house_data['corners']['most_eastern'], house_data['roof_edges']
                    [2][0], house_data['roof_edges'][2][1]],
                [house_data['corners']['most_southern'],
                    house_data['corners']['most_eastern'], house_data['roof_edges'][2][1]],
            ]
        }
        return {"roof": roof_bounding_points, "solar_panels": None}
    elif roof_type == 'hip':
        house_data = {
            "corners": {
                "most_northern": sorted(roof_data, key=lambda x: x[1], reverse=True)[0],
                "most_southern": sorted(roof_data, key=lambda x: x[1])[0],
                "most_western": sorted(roof_data, key=lambda x: x[0])[0],
                "most_eastern": sorted(roof_data, key=lambda x: x[0], reverse=True)[0]
            }
        }

        print(house_data['corners'])

        middle_point = average_point(*roof_data)
        distance_to_middle = distance(middle_point, roof_data[0])
        middle_point.append(middle_point[1])  # Copy y-coordinate
        middle_point[1] = house_height + (distance_to_middle/2)
        house_data['corners']['most_northern'].append(
            house_data['corners']['most_northern'][1])
        house_data['corners']['most_southern'].append(
            house_data['corners']['most_southern'][1])
        house_data['corners']['most_western'].append(
            house_data['corners']['most_western'][1])
        house_data['corners']['most_eastern'].append(
            house_data['corners']['most_eastern'][1])

        house_data['corners']['most_northern'][1] = house_height
        house_data['corners']['most_southern'][1] = house_height
        house_data['corners']['most_western'][1] = house_height
        house_data['corners']['most_eastern'][1] = house_height
        roof_bounding_points = {
            1: [
                [house_data['corners']['most_northern'], house_data['corners']
                    ['most_western'], middle_point],
                [house_data['corners']['most_southern'], house_data['corners']
                    ['most_eastern'], middle_point],
                [house_data['corners']['most_northern'], house_data['corners']
                    ['most_eastern'], middle_point],
                [house_data['corners']['most_southern'], house_data['corners']
                    ['most_western'], middle_point]
            ],
            2: [
                [house_data['corners']['most_northern'], house_data['corners']
                    ['most_western'], middle_point],
                [house_data['corners']['most_southern'], house_data['corners']
                    ['most_eastern'], middle_point],
                [house_data['corners']['most_northern'], house_data['corners']
                    ['most_eastern'], middle_point],
                [house_data['corners']['most_southern'], house_data['corners']
                    ['most_western'], middle_point]
            ]
        }
        return {"roof": roof_bounding_points, "solar_panels": None}
    else:
        raise ValueError(
            "Roof type not supported. Use 'flat', 'gable', or 'hip'.")


def place_solar_panel_on_roof_planes(roof_data):
    if roof_data["type"] == "flat":
        subrects_data = fit_rotated_rects_in_geobounds(
            roof_data["corners"],  rect_w=1.0, rect_h=1.65, angle_deg=compute_longitude_deviation_deg(roof_data['corners']), padding=0.5, vertical_margin=1.0, slope_deg=30.0)
        return subrects_data


def compute_longitude_deviation_deg(geo_bounds):
    lat1, lon1 = geo_bounds['most_western']
    lat2, lon2 = geo_bounds['most_eastern']

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    angle_rad = np.arctan2(delta_lat, delta_lon)
    angle_deg = np.degrees(angle_rad)

    return angle_deg


def rotate_shape(shape_points, angle_deg):
    angle_rad = np.radians(angle_deg)
    rot_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad),  np.cos(angle_rad)]
    ])
    return np.dot(shape_points, rot_matrix.T)


def is_inside_container(points, west, east, south, north):
    xs, ys = points[:, 0], points[:, 1]
    return np.all((west <= xs) & (xs <= east) & (south <= ys) & (ys <= north))


def fit_rotated_rects_in_geobounds(geo_bounds, rect_w, rect_h, angle_deg, padding, vertical_margin, slope_deg
                                   ):
    west = min(geo_bounds['most_western'][1], geo_bounds['most_eastern'][1])
    east = max(geo_bounds['most_western'][1], geo_bounds['most_eastern'][1])
    south = min(geo_bounds['most_southern'][0], geo_bounds['most_northern'][0])
    north = max(geo_bounds['most_southern'][0], geo_bounds['most_northern'][0])

    # prostokąt wokół (0,0)
    half_w, half_h = rect_w / 2, rect_h / 2
    local_shape = np.array([
        [-half_w, -half_h],
        [half_w, -half_h],
        [half_w,  half_h],
        [-half_w,  half_h]
    ])

    rotated_shape = rotate_shape(local_shape, angle_deg)

    min_x, min_y = np.min(rotated_shape, axis=0)
    max_x, max_y = np.max(rotated_shape, axis=0)
    bbox_w = max_x - min_x
    bbox_h = max_y - min_y

    usable_w = (east - west) - 2 * padding
    usable_h = (north - south) - 2 * padding

    if usable_w <= 0 or usable_h <= 0:
        return []

    cols = int(usable_w // bbox_w)
    rows = int((usable_h + vertical_margin) // (bbox_h + vertical_margin))

    if cols == 0 or rows == 0:
        return []

    used_w = cols * bbox_w
    used_h = rows * bbox_h + (rows - 1) * vertical_margin

    offset_x = west + padding + (usable_w - used_w) / 2
    offset_y = south + padding + (usable_h - used_h) / 2

    slope_scale = np.tan(np.radians(slope_deg))

    # jednostkowy wektor osi nachylenia (czyli lokalny "południe")
    south_vector = rotate_shape(np.array([[0, -1]]), angle_deg)[0]
    south_vector /= np.linalg.norm(south_vector)

    rectangles_3d = []
    for row in range(rows):
        y = offset_y + bbox_h / 2 + row * (bbox_h + vertical_margin)
        for col in range(cols):
            x = offset_x + bbox_w / 2 + col * bbox_w
            translated = rotated_shape + np.array([x, y])

            if is_inside_container(translated, west, east, south, north):
                center = np.mean(translated, axis=0)
                # delta wzdłuż osi nachylenia (czyli lokalnego południa)
                delta = np.dot(translated - center, south_vector)
                z = delta * slope_scale
                rectangle_3d = np.column_stack((translated, z))
                rectangles_3d.append(rectangle_3d)

    solar_area = 1.0*1.65 * len(rectangles_3d)
    rectangles_3d = [r3d.tolist() for r3d in rectangles_3d]
    for i, rect in enumerate(rectangles_3d):
        rectangles_3d[i] = [[rect[0], rect[1], rect[2]],
                            [rect[1], rect[2], rect[3]]]

    return {"rectangles": rectangles_3d, "solar_area": solar_area, "slope_deg": slope_deg}
