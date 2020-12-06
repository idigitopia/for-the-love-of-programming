from collections import defaultdict
from graph_data import defaultGraph

# Get Graph
GRAPH = defaultGraph()
time_betn = lambda x, y: GRAPH[x][y]

# Define Problem Statement
CITIES = list(GRAPH.keys())
REFILL_TIME = 2
MAX_FUEL = 4
START_CITY = "A"
END_CITY = "H"

# Initialize Variables
shortest_time_to = defaultdict(lambda: float("inf"))
fuel_at = defaultdict(lambda: 0)
visited_cities, unvisited_cities = [], CITIES
shortest_time_to["A"] = 0
fuel_at["A"] = 4
refuel_at = defaultdict(lambda: False)
prev_city = defaultdict(lambda: "unknown")

# Time complexity calculated for HeapQ implementation of the dictionary.
def get_nearest_unvisited_city():
    _dists = {c: shortest_time_to[c] - fuel_at[c] for c in unvisited_cities}
    return min(_dists, key = _dists.get) if _dists else False

# ---------  PseudoCode Start ---------
# Define Update Function
def update_shortest_path(city):
    for neighbor in GRAPH[city]:
        time_to_neighbor = float("inf") if time_betn(neighbor, city) > MAX_FUEL else time_betn(neighbor, city)
        time_without_refill = time_to_neighbor + shortest_time_to[city]
        refuel_needed = time_to_neighbor > fuel_at[city]
        estimated_time = time_without_refill + REFILL_TIME if refuel_needed else time_without_refill
        start_fuel = MAX_FUEL if refuel_needed else fuel_at[city]

        if estimated_time < shortest_time_to[neighbor]:
            shortest_time_to[neighbor] = estimated_time
            fuel_at[neighbor] = start_fuel - time_to_neighbor
            prev_city[neighbor], refuel_at[city] = city, refuel_needed

# Calculate Shortest Time
while _city:= get_nearest_unvisited_city():
    update_shortest_path(_city)
    visited_cities.append(_city)
    unvisited_cities.remove(_city)
# ---------  PseudoCode End ---------

# Pretty Print Output
path = [(dest_:=END_CITY,fuel_at[END_CITY], False)]
while (came_from_city:=prev_city[dest_]) != "unknown":
    path.append((came_from_city, fuel_at[came_from_city], refuel_at[came_from_city]))
    dest_ = prev_city[dest_]

print(f"Source:{START_CITY} \nDestination:{END_CITY}\n {'- '*20}")
print("\n".join([f"Go to City {_city} with fuel {_fuel_at}, {'Refuel' if _refuel else ''}"
                for _city, _fuel_at, _refuel in reversed(path)]))
print(" -"*20,"\nTotal time for the trip:", shortest_time_to[END_CITY])


# Time Complexity:O((|V|+|E|)*log(|V|))
# Where |V| is the total number of cities in the MAP,
# and |E| is the total number of connecting roads in the MAP