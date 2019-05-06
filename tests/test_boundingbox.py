import unittest
from boundingbox.boundingbox import BoundingBox
from boundingbox.coordinates import convert_latlon_degrees_to_radians

paris = (48.8566, 2.3522)
vincennes = (48.8283, 2.4330)
boulogne = (48.8624, 2.2492)
st_denis = (48.9362, 2.3574)
orleans = (47.9030, 1.9093)
places = [vincennes, boulogne, st_denis, orleans]
distance_100 = 100

class TestBoundingBox(unittest.TestCase):

    def setUp(self):
        self.boundingbox_paris = BoundingBox(paris, distance_100)
    
    def test_make_max_latitude_diff(self):
        self.assertEqual(self.boundingbox_paris.make_max_latitude_diff(6371), 1)

    def test_make_max_longitude_diff(self):
        paris_rad = convert_latlon_degrees_to_radians(paris)
        max_lat_diff = self.boundingbox_paris.make_max_longitude_diff(paris_rad, distance_100)
        self.assertEqual(max_lat_diff, 0.023857536799503094)
        
if __name__ == '__main__':
    unittest.main()