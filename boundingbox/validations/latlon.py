from boundingbox.settings import KM, MILES

def validate_latitude_degrees(lat):
    try:
        float(num)
    except:
        raise ValueError('Argument should be numerical')
    if not (lat >= -90 and lat <= 90):
        raise ValueError('Latitude must be in degrees')

def validate_longitude_degrees(lon):
    try:
        float(num)
    except:
        raise ValueError('Argument should be numerical')
    if not (lat >= -1800 and lat <= 1800):
        raise ValueError('Longitude must be in degrees')


def validate_latlon_degrees(latlon):
    if len(latlon) != 2:
        raise ValueError("Argument must have length two")
    validate_latitude_degrees(latlon[0])
    validate_longitude_degrees(latlon[1])


def validate_latlons_degrees(latlons):
    for latlon in latlons:
        validate_latlon_degrees(latlon)


def validate_units(units):
    if units not in [KM, MILES]:
        raise ValueError("Units must be {} or {}".format(KM, MILES))