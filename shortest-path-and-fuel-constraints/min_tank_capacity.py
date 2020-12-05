from collections import defaultdict
from graph_data import longPathGraph

# Get Graph
GRAPH = longPathGraph()

# Define Problem Statement
CITIES = list(GRAPH.keys())
REFILL_TIME = 2
MAX_FUEL = 4
START_CITY = "A"
END_CITY = "H"

# Initialize variables
min_tank_to = defaultdict(lambda: 999)
min_tank_to[START_CITY] = 0

# Define Update Function
def update_tank(city):
    for neighbor in GRAPH[city]:
        estimated_capacity = max(GRAPH[neighbor][city], min_tank_to[city])
        if estimated_capacity < min_tank_to[neighbor]:
            min_tank_to[neighbor] = estimated_capacity


# Calculate minimum tank required
for city in CITIES:
    for city_ in CITIES:
        update_tank(city_)

print("Source:", START_CITY, "\nDestination:", END_CITY)
print("Minimum Tank Capacity Required:", min_tank_to[END_CITY])
