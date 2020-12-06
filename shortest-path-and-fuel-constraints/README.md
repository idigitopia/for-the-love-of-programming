# Shortest Path and Fuel Constraints
Requirements: Python 3.8, Matplotlib and Networkx 

## 1. Shortest Path
You are given a map of cities and time for travel between them in minutes
as a weighted undirected graph. You want to go from city s to city t. However, your
car tank can only hold enough fuel to drive for C minutes. There are gas stations
in all cities, but no gas stations between cities.

You need to find the shortest time without running out of gas. You can refuel as many times as you want, but each
refueling takes R minutes.

![](graph_plots/defaultGraph.png)
### Command
python shortest_path.py
### Sample Output 
Source:A \
Destination:H \
_ - - - - - - - - - - - - - - - - - - - -  \
Go to City A with fuel 4,  \
Go to City B with fuel 0, Refuel \
Go to City E with fuel 1,  \
Go to City G with fuel 0, Refuel \
Go to City H with fuel 3,  \
_ - - - - - - - - - - - - - - - - - - - - \
Total time for the trip: 13 




## 2. Minimum Tank Capacity
You are given a map of cities and time for travel between them in minutes
as a weighted undirected graph. You want to go from city s to city t. However, your
car tank can only hold enough fuel to drive for C minutes. There are gas stations
in all cities, but no gas stations between cities.

Suppose you want to buy a car that has the minimum tank
capacity (measured in C minutes) needed to be able to drive from s to t.


![](graph_plots/longPathGraph.png)
### Command:
python min_tank_capacity.py
### Sample Output 
Source:A \
Destination:H \
_ - - - - - - - - - - - - - - - - - - - -  \
Go to City A, tank capacity required:0 \
Go to City I1, tank capacity required:2 \
Go to City I2, tank capacity required:2 \
Go to City I3, tank capacity required:2 \
Go to City I4, tank capacity required:2 \
Go to City I5, tank capacity required:2 \
Go to City I6, tank capacity required:2 \
Go to City H, tank capacity required:3 \
_ - - - - - - - - - - - - - - - - - - - - \
 Minimum Tank required for the trip: 3 

