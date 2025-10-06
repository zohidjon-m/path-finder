# 🧭 PathFinder Lab

**PathFinder Lab** is an interactive **graph-search visualization app** built with **Streamlit**.  
It demonstrates how classical pathfinding algorithms explore and find optimal routes between cities on real-world maps.

Users can select a country, choose start and goal cities, run multiple algorithms (A*, Dijkstra, Greedy, BFS, DFS), and instantly see:
- the discovered path on an interactive map,
- the total cost or hops,
- time complexity,
- and the actual runtime each algorithm took.

---

## 🚀 Features

✅ **Multi-Country Support**  
Load different countries from JSON files (e.g., Uzbekistan, Romania, USA). Each file defines cities, coordinates, and road connections.

✅ **Algorithm Comparison**  
Run and compare classic search algorithms:
- **A\*** — optimal with heuristic (Haversine distance)  
- **Dijkstra (UCS)** — optimal cost without heuristic  
- **Greedy Best-First Search** — fast but not guaranteed optimal  
- **BFS / DFS** — explore graphs by layers or depth  

✅ **Visualization**  
- View the best path plotted on an interactive map (PyDeck).  
- Start and goal cities are highlighted with markers.  
- Compare algorithm performance metrics side-by-side.

✅ **Performance Metrics**  
- Nodes expanded  
- Relaxations (edge updates)  
- Total path cost or number of hops  
- Runtime in milliseconds  
- Theoretical time complexity (O-notation)

---

## 🗂 Project Structure

```
PathFinder-Lab/
│
├── app.py                     # Streamlit UI
├── data/
│   ├── countries.json         # list of countries
│   ├── Uzbekistan.json        # each country's graph
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
│   ├── graph_io.py            # data loaders & caching
│   └── mapping.py             # coordinate & map helpers
│
└── README.md
```

---

## ⚙️ How It Works

1. **Load Data**  
   The app loads available countries from `data/countries.json` and then fetches each country's city graph from its `.json` file.

2. **Select Options**  
   Use the sidebar to pick:
   - A country  
   - Start and goal cities  
   - One or more algorithms  

3. **Run Search**  
   Each algorithm runs independently and returns:
   - `path` (list of city names)
   - `cost` (sum of edge weights or hops)
   - `stats` (expansions, relaxations, time taken)

4. **Visualize**  
   Results are displayed as summary cards with metrics and an interactive map view.

---

## 🧠 Algorithms Used

| Algorithm | Type | Optimal | Heuristic | Time Complexity | Space |
|------------|------|----------|------------|-----------------|-------|
| **A\*** | Informed | ✅ | ✅ Haversine | ≈ O((V + E) log V); often faster with good h | O(V) |
| **Dijkstra / UCS** | Uninformed | ✅ | ❌ | O((V + E) log V) | O(V) |
| **Greedy Best-First** | Informed | ❌ | ✅ Haversine | ≈ O((V + E) log V) | O(V) |
| **BFS** | Uninformed | ✅ (Unweighted) | ❌ | O(V + E) | O(V) |
| **DFS** | Uninformed | ❌ | ❌ | O(V + E) | O(V) |

---

## 🧩 Example JSON Structure

Each country JSON defines cities (nodes) and roads (edges):

```json
{
  "nodes": {
    "Tashkent": {
      "coords": [41.3111, 69.2797],
      "edges": { "Samarkand": 310, "Jizzakh": 175 }
    },
    "Samarkand": {
      "coords": [39.6542, 66.9597],
      "edges": { "Tashkent": 310 }
    }
  }
}
```

And `countries.json` lists available countries:
```json
{ "countries": ["Uzbekistan", "Romania", "USA"] }
```

---

## 🧱 Tech Stack

- **Frontend/UI:** [Streamlit](https://streamlit.io/)
- **Backend Logic:** Python 3 (Algorithms implemented from scratch)
- **Visualization:** PyDeck / deck.gl (interactive maps)
- **Data:** JSON graph files (city coordinates + road weights)
- **Math:** Haversine formula for heuristic distance

---

## ▶️ How to Run

```bash
# 1. Install dependencies
pip install streamlit pydeck

# 2. Run the app
streamlit run app.py
```

Then open the local URL (usually `http://localhost:8501`) in your browser.

---

## 🧮 Future Enhancements

- Add **A\*** visualization (step-by-step frontier expansion)
- Integrate **real road data** from OpenStreetMap
- Support **dynamic heuristic tuning**
- Add **weighted random graph generator**
- Export results to CSV or PNG


