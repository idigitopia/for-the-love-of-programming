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
shortest_time_to["A"] = 0
fuel_at["A"] = 4

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

# Calculate Shortest Time
for city in CITIES:
    for city_ in CITIES:
        update_shortest_path(city_)

print("Source:", START_CITY, "\nDestination:", END_CITY)
print("Time Taken:", shortest_time_to[END_CITY], "\nFuel Left:", fuel_at[END_CITY])
