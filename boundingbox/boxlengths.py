import numpy as np
from haversine import haversine

def closest_latitude(source, targets):
    lat_targets = np.array(targets)[:,0]
    lat_source = np.array(source)[0]
    lat_diffs = np.abs(lat_targets - lat_source)
    lat_lons = np.concatenate([targets, lat_diffs], axis=1)
    closest_lats = lat_lons[lat_lons[:, 2].argsort()][:,:2][:N]
    return closest_lats

def closest_latitude(source, targets):
    lat_targets = np.array(targets)[:, 0]
    lat_source = np.array(source)[0]
    lat_diffs = np.abs(lat_targets - lat_source)
    lat_lons = np.concatenate([targets, lat_diffs], axis=1)
    closest_lons = lat_lons[lat_lons[:, 3].argsort()][:,:2][:N]
    return closest_lats


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