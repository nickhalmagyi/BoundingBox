from math import radians
from math import degrees

from boundingbox.validations.coordinates import validate_latlon_degrees


def convert_latlon_degrees_to_radians(latlon_degrees):
    """
    :param latlon_degrees: lat-lon tuple in degrees
    :return: lat-lon tuple in radians
    """
    validate_latlon_degrees(latlon_degrees)
    latlon_radians = (radians(latlon_degrees[0]), radians(latlon_degrees[1]))
    return latlon_radians


def mod_longitude_degrees(lon_degrees):
    """
    :param lon_degrees: float for longitude in degrees
    :return: float for longitude in degrees but shifted to the fundamental domain.
    """
    return ((lon_degrees + 180) % 360) - 180


def mod_longitude_radians(lon_radians):
    """
    :param lon_radians: float for longitude in radians
    :return: float for longitude in radians but shifted to the fundamental domain.
    """
    return radians(mod_longitude_degrees(degrees(lon_radians)))