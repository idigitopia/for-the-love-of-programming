from math import sin, cos, sqrt, atan2, radians, ceil
from network_data import NetworkSpec
MAXCHARGE = 320 #km



class CITY():
    def __init__(self, name, lat, lon, charge_rate):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.charge_rate =charge_rate
        self.neighbor_dist = {}
        self.potential_charges = []

    @staticmethod
    def distance_in_km(city1, city2):
        R = 6356.752  #km
        lat1, lat2, lon1, lon2 = [radians(x) for x in [city1.lat, city2.lat, city1.lon, city2.lon]]

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = (sin(dlat / 2)) ** 2 + cos(lat1) * cos(lat2) * (sin(dlon / 2)) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        return distance


    def neighbors_within(self,radius):
        return {n_id:dist for n_id, dist in self.neighbor_dist if dist<=radius}




# Define all cities
# ALL_CITIES = {d[0]:CITY(*d) for d in NetworkSpec}
#
def distance_by_id(city_id1, city_id2):
    return CITY.distance_in_km(ALL_CITIES[city_id1], ALL_CITIES[city_id2])

def reahcable_by_id(city_id1, city_id2):
    return  distance_by_id(city_id1, city_id2) < MAXCHARGE

# Define all neighbor_ids
for city_id in ALL_CITIES:
    for neighbor_id in ALL_CITIES:
        dist = distance_by_id(city_id, neighbor_id)
        if dist < MAXCHARGE and neighbor_id != city_id:
            ALL_CITIES[city_id].neighbor_dist[neighbor_id] = distance_by_id(city_id, neighbor_id)

# populate potential charge list
for city_id in ALL_CITIES:
    ALL_CITIES[city_id].potential_charge_list = [ceil(distance_by_id(city_id, neighbor_id))
                                                 for neighbor_id in ALL_CITIES[city_id].neighbor_dist]


