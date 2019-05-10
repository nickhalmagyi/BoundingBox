paris = (48.8566, 2.3522)
vincennes = (48.8283, 2.4330)
boulogne = (48.8624, 2.2492)
st_denis = (48.9362, 2.3574)
orleans = (47.9030, 1.9093)
targets_paris = [vincennes, boulogne, st_denis, orleans]

locations_paris = {'source': paris, 'targets': targets_paris}


# This edge case has the following properties
# -- consider a bbox of size 1100 around edge_1_0
# -- Then the only pt inside this box is edge_1_2
# -- However the closest pt is in fact edge_1_1, which is outside this box
edge_1_0 = (0,0)
edge_1_1 = (0,10)
edge_1_2 = (4,9.88)
edge_1_3 = (10,0)
edge_1_4 = (0,10.1)

targets_edgecase_1 = [edge_1_1, edge_1_2, edge_1_3, edge_1_4]
locations_edgecase_1 = {'source': edge_1_0, 'targets': targets_edgecase_1}