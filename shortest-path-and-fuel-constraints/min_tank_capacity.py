from collections import defaultdict
from graph_data import longPathGraph

# Get Graph
GRAPH = longPathGraph()

# Define Problem Statement
CITIES = list(GRAPH.keys())
START_CITY = "A"
END_CITY = "H"

# Initialize variables
min_tank_to = defaultdict(lambda: 999)
min_tank_to[START_CITY] = 0
visited_cities, unvisited_cities = [], CITIES
prev_city = defaultdict(lambda: "unknown")

# Time complexity calculated for HeapQ implementation of the dictionary.
def get_nearest_unvisited_city():
    _dists = {c: min_tank_to[c] for c in unvisited_cities}
    return min(_dists, key = _dists.get) if _dists else False

# ---------  PseudoCode Start ---------
# Define Update Function
def update_tank(city):
    for neighbor in GRAPH[city]:
        estimated_capacity = max(GRAPH[neighbor][city], min_tank_to[city])
        if estimated_capacity < min_tank_to[neighbor]:
            min_tank_to[neighbor] = estimated_capacity
            prev_city[neighbor] = city

# Calculate minimum tank required
while _city:= get_nearest_unvisited_city():
    update_tank(_city)
    visited_cities.append(_city)
    unvisited_cities.remove(_city)
# ---------  PseudoCode End ---------

# Pretty Print Output
path = [(dest_:=END_CITY,min_tank_to[END_CITY])]
while (came_from_city:=prev_city[dest_]) != "unknown":
    path.append((came_from_city, min_tank_to[came_from_city]))
    dest_ = prev_city[dest_]

print(f"Source:{START_CITY} \nDestination:{END_CITY}\n {'- '*20}")
print("\n".join([f"Go to City {_city}, tank capacity required:{_tank_at}"
                for _city, _tank_at in reversed(path)]))
print(" -"*20,"\n Minimum Tank required for the trip:", min_tank_to[END_CITY])

# Time Complexity:O((|V|+|E|)*log(|V|))
# Where |V| is the total number of cities in the MAP,
# and |E| is the total number of connecting roads in the MAP