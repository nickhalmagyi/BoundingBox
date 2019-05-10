import unittest
import numpy as np
from boundingbox.distances import get_points_within_distance, get_closest_points
from boundingbox.coordinates import convert_latlon_degrees_to_radians
from tests.resources.locations import locations_paris, locations_edgecase_1


source_paris = locations_paris['source']
targets_paris = np.array(locations_paris['targets'])
paris_distances_7 = np.array([6.698235303709655])
paris_distances_200 = np.array([6.698235303709655, 7.562627816217736, 8.859287406231937,110.96572196425218])


source_edgecase_1 = locations_edgecase_1['source']
targets_edgecase_1= np.array(locations_edgecase_1['targets'])
distances_edgecase_1_1 = np.array([1111.950802335329, 1111.950802335329])
distances_edgecase_1_2 = np.array([1111.950802335329, 1111.950802335329, 1123.0703103586823])

class TestDistances(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_get_points_within_distance_7(self):
        distances = get_points_within_distance(source_paris, targets_paris, 7)[:,1]
        arrays_equal = np.array_equal(distances, paris_distances_7)
        self.assertEqual(arrays_equal, True)
    
    def test_get_points_within_distance_200(self):
        distances = get_points_within_distance(source_paris, targets_paris, 200)[:,1]
        arrays_equal = np.array_equal(distances, paris_distances_200)
        self.assertEqual(arrays_equal, True)

    def test_get_points_within_distance_edge_case_1(self):
        distances = get_points_within_distance(source_edgecase_1, targets_edgecase_1, 1120)[:,1]
        arrays_equal = np.array_equal(distances, distances_edgecase_1_1)
        self.assertEqual(arrays_equal, True)

    def test_get_closest_points_edge_case_1(self):
        distances = get_closest_points(source_edgecase_1, targets_edgecase_1, 3, 1100)[:,1]
        arrays_equal = np.array_equal(distances, distances_edgecase_1_2)
        self.assertEqual(arrays_equal, True)


if __name__ == '__main__':
    unittest.main()