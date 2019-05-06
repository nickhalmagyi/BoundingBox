"""
@author: Nick Halmagyi
@company: ClimateRisk

This module contains methods to filter lat-lon pairs based on a bounding box around a source
and compute distances between a source and a pandas df of targets.
"""

import numpy as np
import pandas as pd
from math import radians
from math import degrees
from haversine import haversine
from importlib import reload

import boundingbox.validations; reload(boundingbox.validations)
from boundingbox.validations.numbers import validate_positive_number
from boundingbox.validations.coordinates import validate_latlons_degrees, validate_units


import boundingbox.coordinates; reload(boundingbox.coordinates)
from boundingbox.coordinates import convert_latlon_degrees_to_radians, mod_longitude_radians

from boundingbox.settings import EARTH_RADIUS, NORTH, SOUTH, EAST, WEST, KM, MILES, FRONT, REVERSE

class BoundingBox:
    def __init__(self, source, length, units=KM):
        self.source_degrees = source
        self.length = length
        self.units = units
        self.source_radians = convert_latlon_degrees_to_radians(self.source_degrees)
        self.bbox = self.make_bounding_box(self.source_radians, self.length)
        self.earth_radius = EARTH_RADIUS[units]


    @property
    def source_degrees(self):
        return self.__source_degrees

    @source_degrees.setter
    def source_degrees(self, source_degrees):
        validate_latlon_degrees(source_degrees)
        self.__source_degrees = source_degrees

    @property
    def length(self):
        return self.__length

    @length.setter
    def length(self, length):
        validate_positive_number(length)
        self.__length = length

    @property
    def units(self):
        return self.__units

    @units.setter
    def units(self, units):
        validate_units(units)
        self.__units = units
    
    
    def make_max_latitude_diff(self, length):
        return length / self.earth_radius


    def make_max_longitude_diff(self, source_radians, length):
        """
        :param source: lat-lon pair in radians
        :param length: 
        :return: 
        """
        d = length / self.earth_radius
        max_longitude_arg = np.cos(source_radians[0]) ** (-1) * \
                            (np.cos(d) ** 2 - np.sin(source_radians[0]) ** 2) ** (1 / 2)
        return np.abs(np.arccos(max_longitude_arg))


    def make_bounding_box(self, source_radians, length):
        """
        :return: dict with keys = [north, south, east, west] in degrees
        """
        bbox = {}
        bbox_front = {}
        bbox_reverse = {}

        max_latitude_diff = make_max_latitude_diff(length)
        max_longitude_diff = make_max_longitude_diff(source_radians, length)

        if np.abs(source_radians[0]) + max_latitude_diff <= np.pi / 2:
            max_longitude_diff = make_max_longitude_diff(source_radians, length)
            bbox_front[NORTH] = source_radians[0] + max_latitude_diff
            bbox_front[SOUTH] = source_radians[0] - max_latitude_diff
            bbox_front[EAST] = mod_longitude_radians(source_radians[1] + max_longitude_diff)
            bbox_front[WEST] = mod_longitude_radians(source_radians[1] - max_longitude_diff)
            
        else
            bbox_front[EAST] = np.pi / 2
            bbox_front[WEST] = -np.pi / 2
            bbox_reverse[EAST] = -np.pi / 2
            bbox_reverse[WEST] = np.pi / 2

            if (source_radians[0] + max_latitude_diff > np.pi / 2 and \
                source_radians[0] - max_latitude_diff < -np.pi / 2):
                bbox_front[NORTH] = np.pi / 2
                bbox_front[SOUTH] = -np.pi / 2
        
            elif source_radians[0] + max_latitude_diff > np.pi / 2:
                bbox_front[NORTH] = np.pi / 2
                bbox_front[SOUTH] = source_radians[0] - max_latitude_diff
                bbox_reverse[NORTH] = np.pi / 2
                bbox_reverse[SOUTH] = np.arcsin( np.cos(length / self.earth_radius) / np.sin(source_radians[0]))


            elif source_radians[0] - max_latitude_diff < -np.pi / 2:
                bbox_front[NORTH] = source_radians[0] + max_latitude_diff
                bbox_front[SOUTH] = -np.pi / 2
                bbox_reverse[NORTH] = np.arcsin( np.cos(length / self.earth_radius) / np.sin(source_radians[0]))
                bbox_reverse[SOUTH] = -np.pi / 2


        # bounding lat-lon of the box in degrees
        bbox_front = {k: degrees(v) for k, v in bbox_front.items()}
        bbox_reverse = {k: degrees(v) for k, v in bbox_reverse.items()}
        
        return bbox_front, bbox_reverse


    def target_in_bounding_box(self, bbox, target):
        """
        :param bbox: dict with keys = [north, south, east, west]
        :param target_degrees: tuple (lat, lon) in degrees
        :return: boolean for source living within the bounding box
        """
        lat = (target[0] >= bbox[SOUTH]) and (target[0] <= bbox[NORTH])
        if bbox[WEST] <= bbox[EAST]:
            lon = (target[1] >= bbox[WEST]) and (target[1] <= bbox[EAST])
        else:
            lon = (target[1] >= bbox[EAST]) or (target[1] <= bbox[WEST])

        return lat and lon


    def filter_targets_in_bounding_box(self, bbox, targets):
        """
        :param targets: An iterable of lat-lon pairs. 
        Each pair must be itself an iterable just containing the numerical values
        :return: An iterable of booleans corresponding to whether or not the lat-lon pairs lie within the bounding box.
        """
        targets_filtered = [target for target in targets if self.target_in_bounding_box(bbox, target)]
        return targets_filtered


    def compute_distances_from_source(self, targets):
        targets_distance = np.array([[target, haversine(self.source_degrees, target)] for target in targets])
        # sort by distance
        targets_dist_sorted = targets_distance[targets_distance[:,1].argsort()]
        return targets_dist_sorted


    def get_points_within_bbox(self, bbox, targets):
        targets_filtered = self.filter_targets_in_bounding_box(bbox, targets)
        targets_dist = self.compute_distances_from_source(targets_filtered)
        return targets_dist
