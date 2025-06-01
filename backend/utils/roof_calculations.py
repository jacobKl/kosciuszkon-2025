import math
import numpy as np

from utils.solar_panel import calculate_panel_output


def scale_values(values, center):
    R = 6371000
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
    house_roof_geographic_data = roof_data.copy()
    house_roof_local_data = scale_values(roof_data, center)
    roof_data = scale_values(roof_data, center)
    if roof_type == 'flat':
        house_data = {
            "corners": {
                "most_northern": sorted(roof_data, key=lambda x: x[1], reverse=True)[0],
                "most_southern": sorted(roof_data, key=lambda x: x[1])[0],
                "most_western": sorted(roof_data, key=lambda x: x[0])[0],
                "most_eastern": sorted(roof_data, key=lambda x: x[0], reverse=True)[0]
            }
        }
        print(house_data['corners'])
        solar_panels = place_solar_panel_on_roof_planes(
            {'corners': house_data['corners'], 'type': 'flat'}, house_roof_geo=house_roof_geographic_data, house_roof_local=house_roof_local_data)
        solar_panels_output = {
            'clear': calculate_panel_output(
                center[1], center[0], 30, 180, 1.65, 0.18, 'clear', None),
            'partly_cloudy': calculate_panel_output(
                center[1], center[0], 30, 180, 1.65, 0.18, 'partly_cloudy', None),
            'cloudy': calculate_panel_output(
                center[1], center[0], 30, 180, 1.65, 0.18, 'cloudy', None),
            'rain': calculate_panel_output(
                center[1], center[0], 30, 180, 1.65, 0.18, 'rain', None)
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

        middle_point = average_point(*roof_data)
        distance_to_middle = distance(middle_point, roof_data[0])
        middle_point.append(middle_point[1])
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


def place_solar_panel_on_roof_planes(roof_data, house_roof_geo, house_roof_local):
    if roof_data["type"] == "flat":
        subrects_data = fit_solar_panels_local(
            house_roof_geo, house_roof_local,  panel_w=1.0, panel_h=1.65, padding=2.0, vertical_margin=1.0, slope_deg=30.0)
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


def compute_south_vector_local(bbox_geo, bbox_local):
    geo = np.array(bbox_geo)
    local = np.array(bbox_local)

    center_geo = np.mean(geo, axis=0)
    center_local = np.mean(local, axis=0)

    south_geo = [center_geo[0], center_geo[1] - 0.0001]

    def find_nearest_local(target):
        distances = np.linalg.norm(geo - target, axis=1)
        return local[np.argmin(distances)]

    p0 = find_nearest_local(center_geo)
    p1 = find_nearest_local(south_geo)

    vec = p1 - p0
    norm = np.linalg.norm(vec)

    if norm == 0:
        return np.array([0.0, -1.0])

    return vec / norm


def rotate_shape(shape_points, angle_deg):
    angle_rad = np.radians(angle_deg)
    rot_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad),  np.cos(angle_rad)]
    ])
    return np.dot(shape_points, rot_matrix.T)


def is_inside_bounds(points, width, height):
    half_w, half_h = width / 2, height / 2
    xs, ys = points[:, 0], points[:, 1]
    return np.all((-half_w <= xs) & (xs <= half_w) & (-half_h <= ys) & (ys <= half_h))


def fit_solar_panels_local(bbox_corners_geo, bbox_local_points,
                           panel_w=1.0, panel_h=1.65, padding=2.0,
                           vertical_margin=0.5, slope_deg=30):
    south_vector = compute_south_vector_local(
        bbox_corners_geo, bbox_local_points)
    angle_rad = np.arctan2(south_vector[0], -south_vector[1])
    south_angle_deg = np.degrees(angle_rad)
    local = np.array(bbox_local_points)
    xs = local[:, 0]
    zs = local[:, 1]
    area_width_m = xs.max() - xs.min()
    area_height_m = zs.max() - zs.min()

    half_w, half_h = panel_w / 2, panel_h / 2
    panel_shape = np.array([
        [-half_w, -half_h],
        [half_w, -half_h],
        [half_w,  half_h],
        [-half_w,  half_h]
    ])
    rotated_panel = rotate_shape(panel_shape, south_angle_deg)

    min_x, min_y = np.min(rotated_panel, axis=0)
    max_x, max_y = np.max(rotated_panel, axis=0)
    bbox_w = max_x - min_x
    bbox_h = max_y - min_y

    usable_w = area_width_m - 2 * padding
    usable_h = area_height_m - 2 * padding

    if usable_w <= 0 or usable_h <= 0:
        return {"rectangles": [], "solar_area": 0, "panel_count": 0}

    cols = max(1, int(usable_w // bbox_w))
    rows = max(1, int((usable_h + vertical_margin) //
               (bbox_h + vertical_margin)))

    used_w = cols * bbox_w
    used_h = rows * bbox_h + (rows - 1) * vertical_margin

    start_x = -used_w / 2 + bbox_w / 2
    start_y = -used_h / 2 + bbox_h / 2

    slope_scale = np.tan(np.radians(slope_deg))

    rectangles_3d = []
    panel_count = 0

    for row in range(rows):
        y = start_y + row * (bbox_h + vertical_margin)
        for col in range(cols):
            x = start_x + col * bbox_w
            translated = rotated_panel + np.array([x, y])

            if is_inside_bounds(translated, area_width_m, area_height_m):
                center = np.mean(translated, axis=0)
                delta = np.dot(translated - center, south_vector)
                z_coords = delta * slope_scale

                panel_3d = []
                for i, point in enumerate(translated):
                    panel_3d.append([
                        float(point[0]),
                        float(z_coords[i]-0.5),
                        float(point[1])
                    ])

                rectangles_3d.append(panel_3d)
                panel_count += 1

    total_area = panel_count * panel_w * panel_h

    for i, rect in enumerate(rectangles_3d):
        rectangles_3d[i] = [[rect[0], rect[1], rect[2]],
                            [rect[0], rect[2], rect[3]]]

    return {
        "rectangles": rectangles_3d,
        "solar_area": total_area,
        "panel_count": panel_count,
        "slope_deg": slope_deg,
        "south_vector": south_vector.tolist(),
        "south_angle_deg": south_angle_deg,
        "area_dimensions": [area_width_m, area_height_m],
        "grid_size": [cols, rows]
    }
