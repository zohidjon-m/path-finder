import json, math, heapq, collections

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

def ucs(nodes, start, goal):
    """Uniform Cost Search it is same as (Dijkstra)"""
    if start not in nodes or goal not in nodes:
        raise ValueError("Start/goal not found in graph")

    g = collections.defaultdict(lambda: math.inf)
    g[start] = 0
    parent = {}
    heap = [(0, start)]
    closed = set()

    while heap:
        cost, u = heapq.heappop(heap)
        if u in closed:
            continue
        if u == goal:
            return reconstruct(parent, goal), cost

        closed.add(u)
        for v, w in nodes[u]["edges"].items():
            w = float(w)
            new_cost = cost + w
            if new_cost < g[v]:
                g[v] = new_cost
                parent[v] = u
                heapq.heappush(heap, (new_cost, v))
    return None, math.inf

if __name__ == "__main__":
    nodes = load_graph(r"D:\sejong_major\ai\projects\mini_map\data\uzbekistan.json")
    start, goal = "Tashkent", "Bukhara"
    path, cost = ucs(nodes, start, goal)
    print("Dijkstra path:", " -> ".join(path))
    print("Total cost:", round(cost, 1))
