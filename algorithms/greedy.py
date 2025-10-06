import json, math, heapq

def haversine_km(a, b):
    R = 6371.0
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    s = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(s))

def load_graph(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["nodes"]

def reconstruct(parent, goal):
    path = [goal]
    while path[-1] in parent:
        path.append(parent[path[-1]])
    path.reverse()
    return path

def greedy_best_first(nodes, start, goal):
    """Greedy Best-First Search (f = h)"""
    if start not in nodes or goal not in nodes:
        raise ValueError("Start/goal not found in graph")

    def h(city):
        return haversine_km(nodes[city]["coords"], nodes[goal]["coords"])

    parent = {}
    visited = set()
    heap = [(h(start), start)]

    while heap:
        _, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        if u == goal:
            cost = 0
            path = reconstruct(parent, goal)
            for a, b in zip(path, path[1:]):
                cost += nodes[a]["edges"][b]
            return path, cost

        for v in nodes[u]["edges"].keys():
            if v not in visited:
                parent[v] = u
                heapq.heappush(heap, (h(v), v))
    return None, math.inf

if __name__ == "__main__":
    nodes = load_graph("uzbekistan_cities_graph_extended.json")
    start, goal = "Tashkent", "Bukhara"
    path, cost = greedy_best_first(nodes, start, goal)
    print("Greedy path:", " -> ".join(path))
    print("Approx. cost:", round(cost, 1))
