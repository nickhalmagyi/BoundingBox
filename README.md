# Bounding Box

The main purpose of this repo is to efficiently perform certain geographic computations.
Specfically, taking a list of lat-lon pairs (targets) and a single lat-lon pair (source), using this code one can compute
the N-closest locations from targets to the source. One can also compute all locations in targets within a given distance.


This is performed efficiently by creating a bounding box and only computing distances from the source to the
locations within the box.  


Example:  

paris = (48.8566, 2.3522)  
vincennes = (48.8283, 2.4330)  
boulogne = (48.8624, 2.2492)  
st_denis = (48.9362, 2.3574)  
orleans = (47.9030, 1.9093)  
places_paris = [vincennes, boulogne, st_denis, orleans]  


This is an algorithm supplied to compute the initial length of the bounding box.  
```
from boundingbox.distances import make_bounding_box_length

N=2
>>> length = make_bounding_box_length(paris, places_paris, N)
>>> length
[out] 6.698235303709655
```
Here we compute all elements of places_paris closer than length to paris:  
```
from boundingbox.distances import get_points_within_distance

>>> get_points_within_distance(paris, places_paris, bbox_length)
[out] [array([(48.8283, 2.433), 6.698235303709655], dtype=object)]
```

Here we compute the two points in places_paris closest to paris
```
N=2
length = make_bounding_box_length(paris, places_paris, N)
get_closest_points(paris, places_paris, N, length)
[out] array([[(48.8283, 2.433), 6.698235303709655],
       [(48.8624, 2.2492), 7.562627816217736]], dtype=object)
```