import unittest
import numpy as np

from boundingbox.boundingbox import BoundingBox
from boundingbox.coordinates import convert_latlon_degrees_to_radians

paris = (48.8566, 2.3522)
vincennes = (48.8283, 2.4330)
boulogne = (48.8624, 2.2492)
st_denis = (48.9362, 2.3574)
orleans = (47.9030, 1.9093)
places = [vincennes, boulogne, st_denis, orleans]
distance_100 = 100

distances_paris_places = [[(48.8283, 2.433), 6.698235303709655],
       [(48.8624, 2.2492), 7.562627816217736],
       [(48.9362, 2.3574), 8.859287406231937],
       [(47.903, 1.9093), 110.96572196425218]]

bbox_paris_100 = {'front': {'north': 49.75592160591873,
  'south': 47.957278394081264,
  'east': 3.7191361681895785,
  'west': 0.9852638318104142}}

class TestBoundingBox(unittest.TestCase):

    def setUp(self):
        self.boundingbox_paris = BoundingBox(paris, distance_100)
    
    def test_make_max_latitude_diff(self):
        self.assertEqual(self.boundingbox_paris.make_max_latitude_diff(6371), 1)

    def test_make_max_longitude_diff(self):
        paris_rad = convert_latlon_degrees_to_radians(paris)
        max_lat_diff = self.boundingbox_paris.make_max_longitude_diff(paris_rad, distance_100)
        self.assertEqual(max_lat_diff, 0.023857536799503094)
    
    def test_compute_distances_from_source(self):
        dists = self.boundingbox_paris.compute_distances_from_source(paris, places)
        self.assertEqual(np.testing.assert_array_equal(dists, np.array(distances_paris_places)), None)

    def test_make_bounding_box(self):
        paris_radians = convert_latlon_degrees_to_radians(paris)
        bbox = self.boundingbox_paris.make_bounding_box(paris_radians, 100)
        self.assertEqual(bbox, bbox_paris_100)
        
        
        
if __name__ == '__main__':
    unittest.main()