import unittest
import numpy as np

from boundingbox.boundingbox import BoundingBox
from boundingbox.coordinates import convert_latlon_degrees_to_radians

latlon_degrees_1 = (0,0)
latlon_degrees_2 = (45, 45)
latlon_degrees_3 = (-45, -60)


class TestCoordinates(unittest.TestCase):

    def setUp(self):
        pass

    def test_convert_latlon_degrees_to_radians(self):
        self.assertEqual(convert_latlon_degrees_to_radians(latlon_degrees_1), (0,0))
        self.assertEqual(convert_latlon_degrees_to_radians(latlon_degrees_2), (np.pi/4, np.pi/4))
        self.assertEqual(convert_latlon_degrees_to_radians(latlon_degrees_3), (-np.pi/4, -np.pi/3))

if __name__ == '__main__':
    unittest.main()