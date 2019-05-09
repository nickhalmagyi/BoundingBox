import unittest
import numpy as np
from boundingbox.distances import get_points_within_distance
from boundingbox.coordinates import convert_latlon_degrees_to_radians


paris = (48.8566, 2.3522)
vincennes = (48.8283, 2.4330)
boulogne = (48.8624, 2.2492)
st_denis = (48.9362, 2.3574)
orleans = (47.9030, 1.9093)
places_paris = np.array([vincennes, boulogne, st_denis, orleans])

paris_distances_200 = np.array([6.698235303709655, 7.562627816217736, 8.859287406231937,110.96572196425218])
# 
class TestDistances(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_get_points_within_distance(self):
        distances = get_points_within_distance(paris, places_paris, 200)[:,1]
        arrays_equal = np.array_equal(distances, paris_distances_200)
        self.assertEqual(arrays_equal, True)
    

if __name__ == '__main__':
    unittest.main()