from boundingbox.boundingbox import BoundingBox
from haversine import haversine
import numpy as np
from importlib import reload

import boundingbox.validations; reload(boundingbox.validations)
from boundingbox.validations.numbers import validate_strictly_positive_integer
from boundingbox.validations.coordinates import validate_latlons_degrees

from boundingbox.settings import EARTH_RADIUS, NORTH, SOUTH, EAST, WEST, KM, MILES


def closest_points_lat_lon(source, targets, N):
    """
    :param source: lat-lon tuple
    :param lat_lons: iterable of lat-lon tuples
    :param N: integer greater than zero
    :return: A pair of iterables of lat-lon tuples.
    closest_lats is the closest N elements of lat_lons to source measured by latitude
    closest_lons is the closest N elements of lat_lons to source measured by longitude
    """
    lat_lon_diffs = np.abs(np.array(targets) - np.array(source))
    lat_lons = np.concatenate([targets, lat_lon_diffs], axis=1)
    closest_lats = lat_lons[lat_lons[:, 2].argsort()][:,:2][:N]
    closest_lons = lat_lons[lat_lons[:, 3].argsort()][:,:2][:N]
    return closest_lats, closest_lons


def make_bounding_box_length(source, lat_lons, N=1):
    len_lat_lons = len(lat_lons)
    if N > len_lat_lons:
        N = len_lat_lons
    closest_points = closest_points_lat_lon(source, lat_lons, N)
    distance_lat = haversine(source, closest_points[0][-1])
    distance_lon = haversine(source, closest_points[1][-1])
    bbox_length = (distance_lat + distance_lon)/2
    return bbox_length


def get_all_points_within_distance(source, targets, length):
    """
    It is possible for a point to be within the bbox but further than length from source.
    Here we remove such points.
    :param source: lat-lon tuple
    :param targets: iterable of the form [(lat, lon), dist]
    :param length: positive number
    :return: list of targets whose distance to source is less than length.
    """
    validate_latlons_degrees(targets)

    boundingbox = BoundingBox(source, length)
    targets_in_bbox = boundingbox.get_points_within_bbox(targets)
    targets_within_distance = []
    for target in targets_in_bbox:
        if target[1] <= length:
            targets_within_distance.append(target)
        else:
            return targets_within_distance
    return targets_within_distance


def closest_points_are_within_length(targets_distance, N, length):
    """
    :param targets_dist: iterable of the form [(lat, lon), dist]
    :param N: strictly positive integer
    :param length: positive number
    :return: boolean, whether the distance from source to the N-th point in targets_dist is leq to length
    """
    return targets_distance[:N][-1][1] <= length


def get_closest_N_points(source, targets, N, length):
    validate_strictly_positive_integer(N)
    validate_latlons_degrees(targets)

    if N > len(targets):
        # should just return all targets with distance and sorted by distance
        N = len(targets)

    boundingbox = BoundingBox(source, length)
    targets_filtered = boundingbox.filter_targets_in_bounding_box(targets)
    targets_distance = boundingbox.compute_distances_from_source(targets_filtered)
    
    i = 0
    while (len(targets_distance) < N) or not closest_points_are_within_length(targets_distance, N, boundingbox.length):
        
    # rescale 
        if len(targets_distance) < N:
            boundingbox.length *= 1.25
        else:
            # set length to be the distance from source to the N-th point. 
            Nth_point_distance = targets_distance[:N][-1][1]
            if Nth_point_distance <= boundingbox.length:
                boundingbox.length *= 1.25
            else:
                boundingbox.length = Nth_point_distance

        boundingbox.bbox = boundingbox.make_bounding_box(boundingbox.source_radians, boundingbox.length)
        targets_filtered = boundingbox.filter_targets_in_bounding_box(targets)
        targets_distance = boundingbox.compute_distances_from_source(targets_filtered)
        
        i += 1
        if i == 4:
            break

    return targets_distance[:N]
