# 🧭 PathFinder — Interactive Graph Search Platform

**PathFinder** is an interactive **graph-search visualization system** built with **Streamlit**.  
It demonstrates how classical search algorithms explore real geographic networks and compute optimal routes between cities.

---

# 🚀 Core Idea

Real-world maps behave like weighted graphs:  
cities → nodes, roads → edges, distances → weights.

This app exposes how different algorithms navigate these structures.

---

# 🔥 Key Features

### Multi-Country Graphs
JSON-based graphs for Uzbekistan, Romania, USA, and others.

---

### Example Node
```json
{
  "nodes": {
    "Tashkent": {
      "coords": [41.3111, 69.2797],
      "edges": { "Samarkand": 310 }
    }
  }
}
```

### Countries List
```json
{ "countries": ["Uzbekistan", "Romania", "USA"] }
```

---


### Algorithm Benchmarks
A*, Dijkstra/UCS, Greedy Best-First, BFS, DFS.

### Visual Exploration
PyDeck-rendered maps, interactive route display.

### Performance Analytics
Nodes expanded, relaxations, total cost/hops, runtime, time complexity.

---

# 🧠 Algorithms Overview

| Algorithm | Strategy | Optimal? | Heuristic | Complexity | Notes |
|----------|----------|-----------|-----------|------------|-------|
| A* | Best-first + heuristic | Yes | Yes (Haversine) | ~O((V+E) log V) | Most efficient optimal search |
| Dijkstra / UCS | Uniform cost | Yes | No | O((V+E) log V) | A* improves by steering the search |
| Greedy Best-First | Heuristic only | No | Yes | ~O((V+E) log V) | Fast, not reliable |
| BFS | Layered search | Yes (unweighted) | No | O(V+E) | Minimizes hops |
| DFS | Depth search | No | No | O(V+E) | For reachability tests |

---

# 📍 Haversine Distance (A* Heuristic)

The **Haversine formula** computes great‑circle distance between two latitude–longitude points on Earth.  
Used as the heuristic for A*.

### Formula

For points  
(φ₁, λ₁) and (φ₂, λ₂) in radians:

```
d = 2R * arcsin(
        sqrt(
            sin²((φ₂ - φ₁)/2) +
            cos(φ₁) * cos(φ₂) * sin²((λ₂ - λ₁)/2)
        )
    )
```

Where  
R = 6371 km.

### Why it works
- Always ≤ true road distance  
- Does not break optimality  
- Strong guidance toward goal  

---

# 🗂 Project Architecture

```
PathFinder-Lab/
│
├── app.py
├── data/
│   ├── countries.json
│   ├── Uzbekistan.json
│   ├── Romania.json
│   └── ...
│
├── algorithms/
│   ├── a_star_algo.py
│   ├── dijkstra.py
│   ├── greedy.py
│   ├── bfs.py
│   └── dfs.py
│
├── utils/
│   ├── graph_io.py
│   └── mapping.py
│
└── README.md
```

---

# 🔧 Execution Pipeline

### 1. Load Graph
Load countries → load selected country graph.

### 2. User Input
Select country, start node, goal node, algorithms.

### 3. Run Algorithms
Returns path, cost, runtime metrics, expansions, relaxations.

### 4. Visualization
Interactive map + metrics display.


# 📊 Tech Stack

- Python 3  
- Streamlit  
- PyDeck / deck.gl  
- Custom graph + search algorithms  
- Haversine heuristic  

---

# ▶️ Run Locally

```bash
pip install streamlit pydeck
streamlit run app.py
```

---

# 📈 Future Roadmap

- Step-by-step A* visualization  
- Real road integration (OpenStreetMap)  
- Random graph generator  
- Export results (CSV/PNG)  
