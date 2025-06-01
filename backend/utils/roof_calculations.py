import math


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
    print("dupa", point1, point2)
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
    elif roof_type == 'gable':
        print(roof_data)
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
        print(roof_bounding_points)
        return roof_bounding_points
    elif roof_type == 'hip':
        print(roof_data)
        middle_point = average_point(*roof_data)
        print(middle_point)
        distance_to_middle = distance(middle_point, roof_data[0])
        middle_point.append(house_height + distance_to_middle)
        house_data = {
            "corners": {
                "most_northern": sorted(roof_data, key=lambda x: x[1], reverse=True)[0],
                "most_southern": sorted(roof_data, key=lambda x: x[1])[0],
                "most_western": sorted(roof_data, key=lambda x: x[0])[0],
                "most_eastern": sorted(roof_data, key=lambda x: x[0], reverse=True)[0]
            }
        }
        house_data['corners']['most_northern'].append(house_height)
        house_data['corners']['most_southern'].append(house_height)
        house_data['corners']['most_western'].append(house_height)
        house_data['corners']['most_eastern'].append(house_height)
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
        return roof_bounding_points
    else:
        raise ValueError(
            "Roof type not supported. Use 'flat', 'gable', or 'hip'.")
