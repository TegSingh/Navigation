from heapq import heappush, heappop

# uses the lowest length of the node divided by the speed you can move on that node. If there is no speed for the node, the nodes speed is assumed to be
# a walking speed of 2.5 km/h
def calc_weight(node):
    length = min([v.get("length", 1) for v in node.values()])
    speeds = [v.get("maxspeed", "2.5") for v in node.values()]
    speed = float(speeds[0]) if isinstance(speeds[0], str) else float(min(speeds[0]))

    return length/speed, length

def dijkstras(osm_graph, start, end):
    # a dictionary of possible paths. By default, the path consists only of the start node
    paths = {start: [start]}

    """
    Example of how paths are built

    start = 5
    paths = { 5: [ 5 ] }

    node = 7

    paths[7]  = paths[5], 7

    paths = { 5: [5], 7: [5, 7]} 

    paths[9] = paths[7], 9

    paths = { 5: [5], 7: [5, 7], 9: [5, 7, 9]} 

    end = 9
    """

    # a dictionary of costs for each node used
    costs = {}

    # stores the actual length of each node for distance calculation
    distances = {}

    # a dictionary of visited nodes
    visited = {}

    # an array containing cost to a node, distance to a node and the nodes id. By default the start node is the only node
    nodes = [(0, 0, start)]

    # iterate until there are no more nodes to be used
    while nodes:
        # pop node from heapq
        (dist, l, node_id) = heappop(nodes)

        # skip node if already been visited
        if node_id in costs:
            continue

        # add nodes distance to costs dict
        costs[node_id] = dist
        distances[node_id] = l

        # iterate over nodes in graph
        for u, node in osm_graph[node_id].items():

            # calculate cost
            cost, length = calc_weight(node)


            # set new_distance of the node to be current distance + new cost
            new_distance = costs[node_id] + cost
            new_length = distances[node_id] + length

            # if the node hasn't been visited or the new distance is less than the previous cost to get to that node
            # set the nodes new lowest cost, push it onto the heap and add it to the nodes path
            if u not in visited or new_distance < visited[u]:
                distances[u] = new_length # updates actual distance in meters to get to each node. Used for checking pathing accuracy but has no effect on algorithm
                visited[u] = new_distance
                heappush(nodes, (new_distance, new_length, u))
                paths[u] = paths[node_id] + [u]

    # return the shortest path from the dictionary of possible paths
    # and the real distance to the end node in meters
    return paths[end], distances[end]