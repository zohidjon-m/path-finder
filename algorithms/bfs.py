import json, collections

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

def bfs(nodes, start, goal):
    """Breadth-First Search (fewest edges)"""
    if start not in nodes or goal not in nodes:
        raise ValueError("Start/goal not found in graph")

    queue = collections.deque([start])
    parent = {}
    visited = {start}

    while queue:
        u = queue.popleft()
        if u == goal:
            path = reconstruct(parent, goal)
            return path, len(path)-1
        for v in nodes[u]["edges"].keys():
            if v not in visited:
                visited.add(v)
                parent[v] = u
                queue.append(v)
    return None, None

# if __name__ == "__main__":
#     nodes = load_graph("uzbekistan_cities_graph_extended.json")
#     start, goal = "Tashkent", "Bukhara"
#     path, hops = bfs(nodes, start, goal)
#     print("BFS path:", " -> ".join(path))
#     print("Number of hops:", hops)
