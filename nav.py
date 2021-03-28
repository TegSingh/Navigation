import geopy
import math
import osmnx as ox
from pathing import dijkstra_path
import folium
import matplotlib.pyplot as plt
from sklearn.neighbors import KDTree

# optimize this later to get a better box
def calc_box_points(start, end):

    # add a kilometer to each furthest point as long/lat points
    N = max(start[0], end[0]) + 3 / 111.321543
    S = min(start[0], end[0]) - 3 / 111.321543
    E = max(start[1], end[1]) + abs(5 / (math.cos(max(start[1], end[1])) * 111.321543))
    W = min(start[1], end[1]) - abs(5 / (math.cos(min(start[1], end[1])) * 111.321543))

    return N, S, E, W

def generate_route(start_address, end_address):
    start_geocode = ox.geocode(start_address)
    end_geocode = ox.geocode(end_address)

    # get bounding box coordinates
    N, S, E, W = calc_box_points(start_geocode, end_geocode)

    # generate multi digraph from osm data
    osm_graph = ox.graph_from_bbox(north=N, south=S, east=E, west=W, truncate_by_edge=True)

    # show both geocodes on map
    fig, ax = ox.plot_graph(osm_graph, figsize=(10, 10), show=False, close=False, edge_color='black')
    ax.scatter(start_geocode[1], start_geocode[0], c='red', s=100)
    ax.scatter(end_address[1], end_address[0], c='blue', s=100)

    # not sure what this does yet
    nodes, _ = ox.graph_to_gdfs(osm_graph)
    # nodes.head()

    tree = KDTree(nodes[['y', 'x']], metric='euclidean')

    start_index = tree.query([start_geocode], k=1, return_distance=False)[0]
    end_index = tree.query([end_geocode], k=1, return_distance=False)[0]

    start_node = nodes.iloc[start_index].index.values[0]
    end_node = nodes.iloc[end_index].index.values[0]

    # display route on graph
    route = dijkstra_path(osm_graph, start_node, end_node)

    #plot using folium -- needs to be sent to html and opened in browser.
    m = ox.plot_route_folium(osm_graph, route, route_color='green')
    folium.Marker(location=start_geocode, icon=folium.Icon(color='red')).add_to(m)
    folium.Marker(location=end_geocode, icon=folium.Icon(color='blue')).add_to(m)
    m.save('templates/route.html')

    return True

if __name__ == '__main__':
    start_address = "21 Marblehead Rd, Etobicoke, Ontario"
    end_address = "552 Mount Pleasant Rd, Toronto, Ontario"
    generate_route(start_address, end_address)