from settings import KM, MILES


def validate_strictly_positive_integer(N):
    try:
        val = int(N)
    except ValueError as e:
        print(str(e) + "\nError: N must be numerical")
    else:
        if val != N:
            raise ValueError("N must be an integer.")
        if val <= 0:
            raise ValueError("N must be strictly positive.")


def validate_positive_number(N):
    try:
        val = float(N)
    except ValueError as e:
        print(str(e) + "\nError: The argument must be numerical")
    else:
        if val < 0:
            raise ValueError("The argument must be positive.")


def validate_latlon_degrees(latlon):
    if len(latlon) != 2:
        raise ValueError("The latlon pair must be length two")
    for num in latlon:
        try:
            float(num)
        except:
            raise ValueError('Entries in lat-lon should be numerical')
    if not (latlon[0] >= -180 and latlon[0] <= 180):
        raise ValueError('Latitude must be in degrees')

    if not (latlon[1] >= -90 and latlon[1] <= 90):
        raise ValueError('Longitude must be in degrees')


def validate_latlons_degrees(latlons):
    for latlon in latlons:
        validate_latlon_degrees(latlon)


def validate_units(units):
    if units not in [KM, MILES]:
        raise ValueError("Units must be {} or {}".format(KM, MILES))