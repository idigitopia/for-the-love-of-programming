from collections import defaultdict
from graph_data import defaultGraph, testGraph1
from collections import namedtuple
import heapq
from heapdict import heapdict
from tqdm import tqdm

CITY = namedtuple("CITY", ("name", "fuel_at", "fuel_rate"))

# Get Graph and problem setup
input_graph = testGraph1()
REFILL_TIME = 5
MAX_FUEL = 10
START_CITY_NAME = "A"
END_CITY_NAME = "E"



# Get New Graph with Discrete fuel states
def get_graph_with_fuel(graph):
    new_node_list = [CITY(u,f,REFILL_TIME) for u in graph for f in range(MAX_FUEL+1)]
    new_graph = defaultdict( lambda: defaultdict(lambda: float("inf")))

    for u in new_node_list:
        for v in new_node_list:
            if u.name == v.name and u.fuel_at < MAX_FUEL and v.fuel_at == MAX_FUEL:
                new_graph[u][v] = REFILL_TIME #  u.fuel_rate * (v.fuel_at - u.fuel_at)
            if u.name != v.name and graph[u.name][v.name]<=MAX_FUEL and (u.fuel_at - graph[u.name][v.name]) == v.fuel_at:
                new_graph[u][v] = graph[u.name][v.name]
    return new_graph

CITY_STATE_GRAPH = get_graph_with_fuel(input_graph)
time_betn = lambda x, y: CITY_STATE_GRAPH[x][y]



# Define Problem Statementi
START_CITY_STATE = CITY(START_CITY_NAME, MAX_FUEL, REFILL_TIME)

# Initialize Variables
print("Node Count:", node_count:=len(CITY_STATE_GRAPH), "Edge Count:", edge_count:=sum([len(n) for n in CITY_STATE_GRAPH]))
shortest_time_heap, shortest_time_to = heapdict(), defaultdict(lambda :float('inf'))
shortest_time_heap[START_CITY_STATE], shortest_time_to[START_CITY_STATE] = 0, 0
prev_city = defaultdict(lambda: "unknown")
visited = defaultdict(lambda: False)

# Time complexity calculated for HeapQ implementation of the dictionary.
def get_nearest_unvisited_city():
   return shortest_time_heap.popitem()[0] if shortest_time_heap else False

# ------------------------------------  PseudoCode Start ------------------------------------
# Define Update Function
def update_shortest_path(city):
    for neighbor in CITY_STATE_GRAPH[city]:
        estimated_time = time_betn(city,neighbor) + shortest_time_to[city]
        if not visited[neighbor]:
            shortest_time_heap[neighbor] = estimated_time
        if estimated_time < shortest_time_to[neighbor]:
            shortest_time_to[neighbor] = estimated_time
            prev_city[neighbor] = city


# Calculate Shortest Time
for _ in tqdm(range(node_count)):
    _city = get_nearest_unvisited_city()
    visited[_city]= True
    update_shortest_path(_city)
# ------------------------------------  PseudoCode End ------------------------------------


# Pretty Print Output
candidate_end_cities ={c:t for c, t in shortest_time_to.items() if c.name == END_CITY_NAME}
END_CITY_STATE = min(candidate_end_cities, key = candidate_end_cities.get)
path = [dest_:=END_CITY_STATE]
while (came_from_city:=prev_city[dest_]) != "unknown":
    path.append(came_from_city)
    dest_ = prev_city[dest_]

print(f"Source:{START_CITY_STATE} \nDestination:{END_CITY_STATE}\n {'- ' * 20}")
print("\n".join([f"Go to City {_city}" for _city in reversed(path)]))
print(" -" * 20,"\nTotal time for the trip:", shortest_time_to[END_CITY_STATE])


# Time Complexity:O(|V|^2 + (|V|+|E|)*MAXFUEL*log(|V|))
# Where |V| is the total number of cities in the MAP,
# and |E| is the total number of connecting roads in the MAP