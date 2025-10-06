import json
from pathlib import Path
import streamlit as st

@st.cache_data(show_spinner=False)
def load_country_list(index_path="data/countries.json"):
    p = Path(index_path)
    if p.exists():
        data = json.loads(p.read_text(encoding="utf-8"))
        countries = data.get("countries", [])
        if countries:
            return sorted(countries)

    return []

@st.cache_data(show_spinner=False)
def get_graph(country, dir_path="data"):
    """
    Returns nodes dict: { city: {"coords":[lat,lon], "edges":{...}}, ... }
    """
    p = Path(dir_path) / f"{country}.json"
    if not p.exists():
        raise FileNotFoundError(f"Country file not found: {p}")   
     
    data = json.loads(p.read_text(encoding="utf-8"))
    if "nodes" not in data:
        raise KeyError(f"File {p} is missing top-level 'nodes'")
    return data["nodes"]
