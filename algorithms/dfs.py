import json, math

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

def dfs(nodes, start, goal):
    """Depth-First Search (not guaranteed shortest)"""
    if start not in nodes or goal not in nodes:
        raise ValueError("Start/goal not found in graph")

    stack = [start]
    parent = {}
    visited = {start}

    while stack:
        u = stack.pop()
        if u == goal:
            path = reconstruct(parent, goal)
            cost = 0
            for a, b in zip(path, path[1:]):
                cost += nodes[a]["edges"][b]
            return path, cost
        for v in nodes[u]["edges"].keys():
            if v not in visited:
                visited.add(v)
                parent[v] = u
                stack.append(v)
    return None, math.inf

if __name__ == "__main__":
    nodes = load_graph("uzbekistan_cities_graph_extended.json")
    start, goal = "Tashkent", "Bukhara"
    path, cost = dfs(nodes, start, goal)
    print("DFS path:", " -> ".join(path))
    print("Approx. cost:", round(cost, 1))
