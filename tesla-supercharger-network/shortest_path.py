from math import sin, cos, sqrt, atan2, radians, ceil
from network_data import NetworkSpec
from collections import defaultdict, namedtuple
from tqdm import tqdm
import pickle as pk
import os
from heapdict import heapdict

# Helper functions
def inf_fxn ():
    return float("inf")

def def_dict_inf():
    return defaultdict(inf_fxn)

def distance_in_km(city1, city2):
    R = 6356.752  #km
    lat1, lat2, lon1, lon2 = [radians(x) for x in [city1.lat, city2.lat, city1.lon, city2.lon]]
    dlon, dlat = lon2 - lon1, lat2 - lat1
    a = (sin(dlat / 2)) ** 2 + cos(lat1) * cos(lat2) * (sin(dlon / 2)) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

CITY = namedtuple('CITY', ['name','lat','lon', 'charge_rate'])
CITY_STATE = namedtuple('CITY_STATE', ['city','charge'])

# Define Problem Statement
ALL_CITIES = [CITY(*d) for d in NetworkSpec]
START_CITY_NAME = "Council_Bluffs_IA"
END_CITY_NAME = "Cadillac_MI"
MAXCHARGE = 320 #km


# Get New Graph with Discrete charge states, m to set the level of discreteness
m = 32 # Number of distinct charge states.
ceil_to_m = lambda x: ceil(ceil((x*m/MAXCHARGE))*MAXCHARGE/m)
ALL_CITY_STATES_DICT = {c:[CITY_STATE(c,(m-i)*MAXCHARGE/m) for i in range(m+1)] for c in ALL_CITIES}
CITY_Neighborrs = {c:[n for n in ALL_CITIES if distance_in_km(c,n)<MAXCHARGE] for c in ALL_CITIES}
CITY_STATE_GRAPH = defaultdict(def_dict_inf)

if os.path.exists(f"prebuilt_graphs/city_state_graph_m{m}.pk"):
    CITY_STATE_GRAPH = pk.load(open(f"prebuilt_graphs/city_state_graph_m{m}.pk","rb"))
else:
    for c1 in tqdm(ALL_CITIES):
        for c2 in CITY_Neighborrs[c1]:
            distance = distance_in_km(c1, c2)
            for u in ALL_CITY_STATES_DICT[c1]:
                for  v in ALL_CITY_STATES_DICT[c2]:
                    if u.city.name == v.city.name and u.charge < v.charge:
                        CITY_STATE_GRAPH[u][v] = (v.charge - u.charge)/u.city.charge_rate # hrs
                    if u.city.name != v.city.name and ceil_to_m(distance)==(u.charge-v.charge):
                        CITY_STATE_GRAPH[u][v] = distance/105 # hrs
    pk.dump(CITY_STATE_GRAPH,open(f"prebuilt_graphs/city_state_graph_m{m}.pk","wb"))

print("Graph Creation Complete")
time_betn = lambda x, y: CITY_STATE_GRAPH[x][y] # hrs


# Get Start City State
START_CITY_STATE =[CITY_STATE(CITY(*d),MAXCHARGE) for d in NetworkSpec if d[0]==START_CITY_NAME][0]

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
candidate_end_cities ={c:t for c, t in shortest_time_to.items() if c.city.name == END_CITY_NAME}
END_CITY_STATE = min(candidate_end_cities, key = candidate_end_cities.get)
path = [dest_:=END_CITY_STATE]
while (came_from_city:=prev_city[dest_]) != "unknown":
    path.append(came_from_city)
    dest_ = prev_city[dest_]

print(f"Source:{START_CITY_STATE} \nDestination:{END_CITY_STATE}\n {'- ' * 20}")
print("\n".join([f"Go to City {_city}" for _city in reversed(path)]))
print(" -" * 20,"\nTotal time for the trip:", shortest_time_to[END_CITY_STATE])



# Time Complexity:O((|V|*MAXCHARGE)^2)
# Where |V| is the total number of cities in the MAP,
# and |E| is the total number of connecting roads in the MAP