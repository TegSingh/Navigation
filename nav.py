import geopy
import math
import osmnx as ox
from pathing import dijkstras
import folium
import matplotlib.pyplot as plt
from sklearn.neighbors import KDTree

# optimize this later to get a better box
def calc_box_points(start, end):

    # add 3 kilometers to each furthest point as long/lat points
    N = max(start[0], end[0]) + 3 / 111.321543
    S = min(start[0], end[0]) - 3 / 111.321543
    E = max(start[1], end[1]) + abs(3 / (math.cos(max(start[1], end[1])) * 111.321543))
    W = min(start[1], end[1]) - abs(3 / (math.cos(min(start[1], end[1])) * 111.321543))

    return N, S, E, W

def generate_route(start_address, end_address):
    start_geocode = ox.geocode(start_address)
    end_geocode = ox.geocode(end_address)

    # get bounding box coordinates
    N, S, E, W = calc_box_points(start_geocode, end_geocode)

    # generate multi digraph from osm data
    osm_graph = ox.graph_from_bbox(north=N, south=S, east=E, west=W, truncate_by_edge=True)

    # get nodes from osm_graph
    nodes, _ = ox.graph_to_gdfs(osm_graph)

    # convert nodes into KDTree, uses euclidean distance by default
    kd_tree = KDTree(nodes[['y', 'x']])

    start_index = kd_tree.query([start_geocode], return_distance=False)[0]
    end_index = kd_tree.query([end_geocode], return_distance=False)[0]

    start_node = nodes.iloc[start_index].index.values[0]
    end_node = nodes.iloc[end_index].index.values[0]

    # display route on graph
    route = dijkstras(osm_graph, start_node, end_node)

    # overlay route onto map and set icons to show start and end
    route_map = ox.plot_route_folium(osm_graph, route)
    folium.Marker(location=start_geocode, icon=folium.Icon(color='red')).add_to(route_map)
    folium.Marker(location=end_geocode, icon=folium.Icon(color='green')).add_to(route_map)
    route_map.save('templates/route.html')