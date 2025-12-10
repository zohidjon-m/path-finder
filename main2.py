import time
import streamlit as st
from utils.graph_io import load_country_list, get_graph
from utils.mapping import path_to_lonlat, viewport_for
import pydeck as pdk

# algorithms
from algorithms.ucs import ucs
from algorithms.greedy import greedy_best_first
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.a_star_algo import a_star, create_Nodes_from_graph


# ---------------------------------------------------------
# Build full graph edges for visualization
# ---------------------------------------------------------
def build_full_graph_edges(nodes):
    edges = []
    for city, info in nodes.items():
        if "coords" not in info:
            continue
        lat1, lon1 = info["coords"]

        for nb, w in info["edges"].items():
            if nb not in nodes:
                continue
            if "coords" not in nodes[nb]:
                continue
            lat2, lon2 = nodes[nb]["coords"]

            # avoid duplicates (A → B and B → A)
            if city < nb:
                edges.append({
                    "path": [
                        [lon1, lat1],
                        [lon2, lat2]
                    ]
                })
    return edges


# ---------------------------------------------------------
# Run one algorithm
# ---------------------------------------------------------
def run_one(algoname, graph, nodes, start, goal):
    t0 = time.perf_counter()
    if algoname == "Dijkstra(UCS)":
        path, cost = ucs(nodes, start, goal)
    elif algoname == "Greedy":
        path, cost = greedy_best_first(nodes, start, goal)
    elif algoname == "A*":
        path, cost = a_star(graph, start, goal)
    elif algoname == "BFS":
        path, cost = bfs(nodes, start, goal)
    elif algoname == "DFS":
        path, cost = dfs(nodes, start, goal)
    else:
        path, cost = None, None
    t1 = time.perf_counter()

    return {
        "algo": algoname,
        "path": path,
        "cost": cost,
        "time_ms": (t1 - t0) * 1000.0
    }


# ---------------------------------------------------------
# Complexity dict
# ---------------------------------------------------------
COMPLEXITY = {
    "BFS": {
        "Time": "O(V + E)",
        "Space": "O(V)",
        "Optimal?": "Yes on unweighted graphs"
    },
    "DFS": {
        "Time": "O(V + E)",
        "Space": "O(V)",
        "Optimal?": "No"
    },
    "Dijkstra(UCS)": {
        "Time": "O((V + E) log V)  [binary heap]",
        "Space": "O(V)",
        "Optimal?": "Yes (non-negative weights)"
    },
    "Greedy": {
        "Time": "≈ O((V + E) log V)",
        "Space": "O(V)",
        "Optimal?": "No"
    },
    "A*": {
        "Time": "≈ O((V + E) log V)",
        "Space": "O(V)",
        "Optimal?": "Yes if h is admissible"
    }
}


# ---------------------------------------------------------
# Sidebar UI
# ---------------------------------------------------------
st.set_page_config(page_title="Pathfinding Map", layout="wide")

st.sidebar.title("Controls")

countries = load_country_list("data/countries.json")
country = st.sidebar.selectbox("Country", countries, index=0)

nodes = get_graph(country, dir_path="data")
cities = sorted(nodes.keys())
graph_a_star = create_Nodes_from_graph(nodes)

col1, col2 = st.sidebar.columns(2)
start = col1.selectbox("Start", cities, index=0)
goal  = col2.selectbox("Goal", cities, index=min(1, len(cities)-1))

algos = st.sidebar.multiselect(
    "Algorithms",
    ["A*", "Dijkstra(UCS)", "Greedy", "BFS", "DFS"],
    default=["A*", "Dijkstra(UCS)", "Greedy"]
)

run = st.sidebar.button("Run")


# ---------------------------------------------------------
# Main UI
# ---------------------------------------------------------
st.title("Pathfinding Map")

if start == goal:
    st.info("Start and goal are the same. Path cost is 0.")

elif run:
    results = [run_one(a, graph_a_star, nodes, start, goal) for a in algos]

    # Precompute the full-graph edges
    full_graph_edges = build_full_graph_edges(nodes)

    for res in results:
        with st.container(border=True):
            st.subheader(res["algo"])

            if res["path"] is None:
                st.warning("No path found.")
                continue

            # metrics
            m1, m2, m3 = st.columns(3)
            m1.metric("Total cost (or hops)", f"{res['cost']}")
            m2.metric("Time taken (ms)", f"{res['time_ms']:.2f}")
            cx = COMPLEXITY.get(res["algo"], {})
            m3.metric("Theoretical time", cx.get("Time", "?"))

            st.write(" → ".join(res["path"]))

            # Map drawing
            lonlat = path_to_lonlat(nodes, res["path"])
            if lonlat:
                view = pdk.ViewState(**viewport_for(lonlat))

                # full graph (black)
                graph_layer = pdk.Layer(
                    "PathLayer",
                    data=full_graph_edges,
                    get_path="path",
                    get_color=[0, 0, 0],
                    width_min_pixels=2
                )

                # shortest path (red)
                line = pdk.Layer(
                    "PathLayer",
                    data=[{"path": lonlat}],
                    get_path="path",
                    get_color=[255, 0, 0],
                    width_min_pixels=4
                )

                start_marker = pdk.Layer(
                    "ScatterplotLayer",
                    data=[{"pos": lonlat[0]}],
                    get_position="pos",
                    get_radius=7000,
                )

                goal_marker = pdk.Layer(
                    "ScatterplotLayer",
                    data=[{"pos": lonlat[-1]}],
                    get_position="pos",
                    get_radius=7000,
                )

                st.pydeck_chart(
                    pdk.Deck(
                        map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
                        layers=[graph_layer, line, start_marker, goal_marker],
                        initial_view_state=view
                    )
                )

            else:
                st.caption("No coordinates available for one or more cities; map omitted.")
