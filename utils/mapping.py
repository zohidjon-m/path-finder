
def path_to_lonlat(nodes, path):
    coords = []
    for city in path:
        lat, lon = nodes[city].get("coords", [None, None])
        if lat is None or lon is None:
            return []  # skip map if missing coords
        coords.append([lon, lat])  # note: [lon, lat]
    return coords

def viewport_for(coords):
    # simple average center
    if not coords: return {"latitude": 41.0, "longitude": 69.0, "zoom": 5}
    lats = [c[1] for c in coords]
    lons = [c[0] for c in coords]
    return {
        "latitude": sum(lats)/len(lats),
        "longitude": sum(lons)/len(lons),
        "zoom": 5
    }
