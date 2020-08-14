# 1st attempt: DFT
from collections import deque

# def dft(world):
#     s = deque()
#     visited = set()
#     traversal = list()
#     starting_point = world.starting_room
#     s.append([starting_point.id])

#     while len(s) > 0:
#         if len(visited) == 3:
#             break
#         path = s.pop()
#         if len(path) >= 2:
#             for direction in world.rooms[path[-2]].get_exits():
#                 if world.rooms[path[-2]].get_room_in_direction(direction) == world.rooms[path[-1]]:
#                     traversal.append(str(direction))
#         if path[-1] not in visited:
#             visited.add(path[-1])
        
#             for direction in world.rooms[path[-1]].get_exits():
#                 exfil = world.rooms[path[-1]].get_room_in_direction(direction).id
#                 next_path = list(path)
#                 next_path.append(exfil)
#                 s.append(next_path)

#     return traversal
# This was just completely the wrong idea.

# 2nd attmept: Traversal with BFS to next unexplored node

def bfs(world, graph, starting_id):
    q = deque()
    q.append([starting_id])
    # store visited nodes
    visited = set()

    # while the queue is not empty:
    while len(q) > 0:
        # Get the next item from the queue
        path = q.popleft()
        # Check if this last node has already been visited
        next_node = path[-1]
        if next_node not in visited:
            # mark next_node as visited
            visited.add(next_node)
            # get next available exit
            for direction in world.rooms[next_node].get_exits():
                # add this path to the queue
                new_path = path.copy()
                new_path.append(world.rooms[next_node].get_room_in_direction(direction).id)
                # check if this is unknown in the graph
                if graph[next_node][direction] == '?':
                    # We've found the next unknown, return this path
                    return new_path[1:] # exclude starting point
                else:
                    # Add this new path to the queue
                    q.append(new_path)
    return None

def traverse(world, starting_id, size):
    # create map for known locations
    graph = dict()
    # set to hold all visited nodes
    visited = set()
    # create an entry for the starting point
    graph[starting_id] = {x : '?' for x in world.rooms[starting_id].get_exits()}
    # create new variable to contain the current working node
    last_node = starting_id
    path = list()

    # add the starting location to the path
    path.append(starting_id)

    while len(visited) < size:
        # mark current node as visited
        visited.add(last_node)
        # Find the next unknown node
        next_path = bfs(world, graph, last_node)
        # if this is none, we are done.
        if next_path == None:
            break
        # set variable for the next node
        next_node = next_path[-1]
        # if the length of next path is greater than 2, update last_node
        if len(next_path) >= 2:
            last_node = next_path[-2]
        # create a graph entry for the new node
        graph[next_node] = {x : '?' for x in world.rooms[next_node].get_exits()}
        # create list for possible connection directions
        connections = world.rooms[last_node].get_exits()
        # enter entry for direction from previous node
        for direction in connections:
            # find direction cooresponding to the next_node value
            if world.rooms[last_node].get_room_in_direction(direction).id == next_node:
                graph[last_node][direction] = next_node
        # get the connections for the next node
        next_connections = world.rooms[next_node].get_exits()
        # check each direction in next connections
        for direction in next_connections:
            # check if the node in this direction has been visited
            if world.rooms[next_node].get_room_in_direction(direction).id in visited:
                # update graph entry to show the node -> direction relationship
                graph[next_node][direction] = world.rooms[next_node].get_room_in_direction(direction).id

        # add the path to next unknown to the current path
        path = path + next_path

        # update the last node to be the next node in the sequence
        last_node = next_node

    print("Path: ", path)
    # create list of directions
    t_list = list()
    for i in range(len(path)):
        # ignore the first value
        if i > 0:
            # get key value pairs from graph
            for key, value in graph[path[i-1]].items():
                # if the value is equal to the next index:
                if value == path[i]:
                    # record the key for that value
                    t_list.append(key)
    return t_list

# Solves the main maze in 1003 moves