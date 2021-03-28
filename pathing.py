from heapq import heappush, heappop
from itertools import count
import networkx as nx

# uses node lowest node length to determine cost of node. If there is no length, it is assumed the length is 1 (houses etc.)
def calc_weight(node):
    return min([v.get("length", 1) for v in node.values()])

def dijkstras(osm_graph, start, end):
    # a dictionary of possible paths. By default, the path consists only of the start node
    paths = {start: [start]}

    """
    Example of how paths are built

    start = 5
    paths = { 5: [ 5 ] }

    node = 7

    paths[7]  = paths[5], 7

    paths = { 5: [5], 7: [5, 7], 9: [5, 7, 9]} 

    end = 9
    """

    # a dictionary of distances for each node used
    distances = {}

    # a dictionary of visited nodes
    visited = {}

    # an array containing distance to a node and the nodes id. By default the start node is the only node
    nodes = [(0, start)]

    # iterate until there are no more nodes to be used
    while nodes:
        # pop node from heapq
        (dist, node_id) = heappop(nodes)

        # skip node if already been visited
        if node_id in distances:
            continue

        # add nodes distance to distances dict
        distances[node_id] = dist

        # iterate over nodes in graph
        for u, node in osm_graph[node_id].items():

            # calculate cost
            cost = calc_weight(node)

            # set new_distance to be current distance + new cost
            new_distance = distances[node_id] + cost

            # if the node hasn't been visited or the new distance is less than the previous cost to get to that node
            # set the nodes new lowest cost, push it onto the heap and add it to the nodes path
            if u not in visited or new_distance < visited[u]:
                visited[u] = new_distance
                heappush(nodes, (new_distance, u))
                paths[u] = paths[node_id] + [u]

    # return the shortest path from the dictionary of possible paths
    return paths[end]