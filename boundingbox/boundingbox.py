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

from boundingbox.settings import EARTH_RADIUS, NORTH, SOUTH, EAST, WEST, KM, MILES

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


    def make_bounding_box(self, source_radians, length):
        """
        :return: dict with keys = [north, south, east, west] in degrees
        """

        # lon_diff, lat_diff are half of the length of a side of the bounding box,
        # in latitude and longitude (radians)
        # These formulae arises from simplifying the Haversine formula when two lats or two lons are equal

        lon_arg = np.sin(length / (2 * EARTH_RADIUS_KM)) * (np.cos(source_radians[0])) ** (-1)
        lon_arg_cutoff = min(1, lon_arg)
        lon_diff = 2 * np.abs(np.arcsin(lon_arg_cutoff))

        lat_diff = length / EARTH_RADIUS_KM

        # bounding lat-lon of the box in radians
        bbox = {}
        bbox[NORTH] = min(np.pi/2, self.source_radians[0] + lat_diff)
        bbox[SOUTH] = max(-np.pi/2, self.source_radians[0] - lat_diff)
        bbox[EAST] = mod_longitude_radians(source_radians[1] + lon_diff)
        bbox[WEST] = mod_longitude_radians(source_radians[1] - lon_diff)

        # bounding lat-lon of the box in degrees
        return {k: degrees(v) for k, v in bbox.items()}


    def target_in_bounding_box(self, target):
        """
        :param bbox: dict with keys = [north, south, east, west]
        :param target_degrees: tuple (lat, lon) in degrees
        :return: boolean for source living within the bounding box
        """
        lat = (target[0] >= self.bbox[SOUTH]) and (target[0] <= self.bbox[NORTH])
        if self.bbox[WEST] <= self.bbox[EAST]:
            lon = (target[1] >= self.bbox[WEST]) and (target[1] <= self.bbox[EAST])
        else:
            lon = (target[1] >= self.bbox[EAST]) or (target[1] <= self.bbox[WEST])

        return lat and lon


    def filter_targets_in_bounding_box(self, targets):
        """
        :param targets: An iterable of lat-lon pairs. 
        Each pair must be itself an iterable just containing the numerical values
        :return: An iterable of booleans corresponding to whether or not the lat-lon pairs lie within the bounding box.
        """
        targets_filtered = [target for target in targets if self.target_in_bounding_box(target)]
        return targets_filtered


    def compute_distances_from_source(self, targets):
        targets_distance = np.array([[target, haversine(self.source_degrees, target)] for target in targets])
        # sort by distance
        targets_dist_sorted = targets_distance[targets_distance[:,1].argsort()]
        return targets_dist_sorted


    def get_points_within_bbox(self, targets):
        targets_filtered = self.filter_targets_in_bounding_box(targets)
        targets_dist = self.compute_distances_from_source(targets_filtered)
        return targets_dist
