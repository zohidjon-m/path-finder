import math, heapq, json

# ----- distance / heuristic -----
def haversine_km(a, b):
    if a is None or b is None:  # fallback if coords missing
        return 0.0
    R = 6371.0
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    s = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(s))


# ----- graph model -----
class Node:
    __slots__ = ("name","coords","adj","g","f","parent")
    def __init__(self, name, coords):
        self.name   = name
        self.coords = coords      # (lat, lon) or None
        self.adj    = []          # list[(neighbor_node, cost)]
        self.g      = float('inf')
        self.f      = float('inf')
        self.parent = None
    def __lt__(self, other):  # heap by f
        return self.f < other.f
    def __hash__(self):       # allow set/dict by identity (name unique assumed)
        return hash(id(self))

def create_Nodes_from_graph(data):
    # create nodes
    nodes = { name: Node(name, info.get("coords"))
              for name, info in data.items() }
    # wire edges
    for name, info in data.items():
        u = nodes[name]
        for nb_name, cost in info["edges"].items():
            u.adj.append((nodes[nb_name], float(cost)))
    return nodes

def reconstruct_path(goal_node):
    path = []
    cur = goal_node
    total_cost = cur.g
    while cur:
        path.append(cur.name)
        cur = cur.parent
    return path[::-1], total_cost

def a_star(graph, start_name, goal_name):
    nodes = create_Nodes_from_graph(graph)
    if start_name not in nodes or goal_name not in nodes:
        raise ValueError("Start or goal not in graph.")
    start, goal = nodes[start_name], nodes[goal_name]

    # reset
    for n in nodes.values():
        n.g = float('inf'); n.f = float('inf'); n.parent = None

    def h(node):  # heuristic depends on the chosen goal
        return haversine_km(node.coords, goal.coords)

    start.g = 0.0
    start.f = h(start)

    open_heap = [start]
    closed = set()

    while open_heap:
        cur = heapq.heappop(open_heap)
        if cur in closed:  # skip stale
            continue
        if cur is goal:
            return reconstruct_path(cur)

        closed.add(cur)

        for nb, w in cur.adj:
            if nb in closed:
                continue
            tentative_g = cur.g + w
            if tentative_g < nb.g:
                nb.parent = cur
                nb.g = tentative_g
                nb.f = tentative_g + h(nb)
                heapq.heappush(open_heap, nb)

    return None, float('inf')  # no path

# --- example usage ---
# nodes = load_graph_from_json(r"D:\sejong_major\ai\projects\mini_map\data\uzbekistan_cities.json")
# nodes = load_graph_from_json(r"D:\sejong_major\ai\projects\mini_map\data\romania.json")
# start, goal = "Oradea", "Iasi"          # <- user choices
# path, cost = a_star(nodes, start, goal)
# print("Path:", " -> ".join(path) if path else "No path")
# print("Cost:", cost if path else "∞")