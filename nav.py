import math
import osmnx as ox
from pathing import dijkstras
import folium
from sklearn.neighbors import KDTree
import requests
from colorama import Fore, Style
import time

# optimize this later to get a better box
def calc_box_points(start, end):

    # add 3 kilometers to each furthest point as long/lat points
    N = max(start[0], end[0]) + 3 / 111.321543
    S = min(start[0], end[0]) - 3 / 111.321543
    E = max(start[1], end[1]) + abs(3 / (math.cos(max(start[1], end[1])) * 111.321543))
    W = min(start[1], end[1]) - abs(3 / (math.cos(min(start[1], end[1])) * 111.321543))

    return N, S, E, W

def generate_route(start_address, end_address):
    # read in api key
    api_file = open("api_key.txt", "r")
    api_key = api_file.read()
    api_file.close()

    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&"

    # get distance google maps finds for path
    res = requests.get(url + "origins=" + start_address + "&destinations=" + end_address + "&key=" + api_key)
    google_dist = res.json()['rows'][0]['elements'][0]['distance']['value']

    start_geocode = ox.geocode(start_address)
    end_geocode = ox.geocode(end_address)

    # get bounding box coordinates
    N, S, E, W = calc_box_points(start_geocode, end_geocode)

    print(f"\n{Fore.BLUE}Creating osm graph...{Style.RESET_ALL}")
    # generate multi digraph from osm data
    start = time.time()
    osm_graph = ox.graph_from_bbox(north=N, south=S, east=E, west=W, truncate_by_edge=True)
    end = time.time()
    print(f"{Fore.GREEN}Osm graph created in {round(end - start, 2)} seconds!{Style.RESET_ALL}\n")

    # get nodes from osm_graph
    nodes, _ = ox.graph_to_gdfs(osm_graph)

    # convert nodes into KDTree, uses euclidean distance by default
    kd_tree = KDTree(nodes[['y', 'x']])

    # use tree structure to quickly find nearest node
    start_index = kd_tree.query([start_geocode], return_distance=False)[0]
    end_index = kd_tree.query([end_geocode], return_distance=False)[0]

    start_node = nodes.iloc[start_index].index.values[0]
    end_node = nodes.iloc[end_index].index.values[0]

    # display route on graph
    print(f"{Fore.BLUE}Calculating route...{Style.RESET_ALL}")
    start = time.time()
    route, distance = dijkstras(osm_graph, start_node, end_node)
    end = time.time()
    print(f"{Fore.GREEN}Route calculated in {round((end - start) * 1000, 2)} ms!{Style.RESET_ALL}")

    print()
    print(f"Distance: {distance}m")
    print(f"Google distance: {google_dist}")

    # calculate accuracy of pathing
    accuracy = 100 - abs(((distance - google_dist) / (google_dist)) * 100)
    if accuracy >= 90.0:
        print(f"{Fore.GREEN}Accuracy: {round(accuracy, 2)}% {Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Accuracy: {round(accuracy, 2)}% {Style.RESET_ALL}")

    print()

    # overlay route onto map and set icons to show start and end
    route_map = ox.plot_route_folium(osm_graph, route)
    folium.Marker(location=start_geocode, icon=folium.Icon(color='red')).add_to(route_map)
    folium.Marker(location=end_geocode, icon=folium.Icon(color='green')).add_to(route_map)
    route_map.save('templates/route.html')