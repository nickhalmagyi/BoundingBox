from boundingbox.boundingbox import BoundingBox
from haversine import haversine
import numpy as np
import time
from importlib import reload

import boundingbox.validations; reload(boundingbox.validations)
from boundingbox.validations.numbers import validate_strictly_positive_integer, validate_positive_number


def get_points_within_distance(source, targets, length):
    """
    It is possible for a point to be within the bbox but further than length from source.
    Here we remove such points.
    :param source: lat-lon tuple
    :param targets: iterable of the form [(lat, lon), dist]
    :param length: positive number
    :return: list of targets whose distance to source is less than length.
    """
    validate_positive_number(length)
    boundingbox = BoundingBox(source, length)
    targets_in_bbox = boundingbox.get_points_within_bboxs(targets, boundingbox.bbox)
    targets_within_distance = targets_in_bbox[np.transpose(targets_in_bbox)[1] <= length]
    return targets_within_distance


def closest_points_are_within_length(targets_distance, N, length):
    """
    :param targets_dist: iterable of the form [(lat, lon), dist]
    :param N: strictly positive integer
    :param length: positive number
    :return: boolean, whether the distance from source to the N-th point in targets_dist is leq to length
    """
    return targets_distance[:N][-1][1] <= length


def get_closest_points(source_degrees, targets, N, length=None):
    validate_strictly_positive_integer(N)
    if N > len(targets):
        N = len(targets)

    boundingbox = BoundingBox(source_degrees, length)
    targets_filtered = boundingbox.filter_targets_in_bboxs(targets, boundingbox.bbox)
    targets_distance = boundingbox.compute_distances_from_source(source_degrees, targets_filtered)

    while (len(targets_distance) < N) or not closest_points_are_within_length(targets_distance, N, boundingbox.length):
        print('Rescaling box, consider using a larger initial length')
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
        targets_filtered = boundingbox.filter_targets_in_bboxs(targets, boundingbox.bbox)
        targets_distance = boundingbox.compute_distances_from_source(source_degrees, targets_filtered)
        
    return targets_distance[:N]
