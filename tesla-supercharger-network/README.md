# Tesla Supercharger Network Puzzle.

Your objective is to construct a search algorithm to find the minimum time path through the tesla
network of supercharging stations. Each supercharger will refuel the vehicle at a different rate
given in km/hr of charge time. Your route does not have to fully charge at every visited charger,
so long as it never runs out of charge between two chargers. You should expect to need no more 
than 4-6 hours to solve this problem. We suggest implementing a quick brute force method before
attempting to find an optimal routine.


You will be provided with a code skeleton which includes a header with the charger network data
in the format:

	name, latitude in degrees, longitude in degrees, charge rate in km/hr


You may compare your solutions against our reference implementation using the provided
"checker" programs in either OSX or linux, make sure to use it to check your submission output
against several different start and end chargers


Input: Your program should take as input two strings: “start charger name”, “end charger name"


Output: Your program’s only output should be a print to std::out of a string in the format:

		initial charger name, first charger name, charge time in hrs, 
		second charger name, charge time in hrs, …, …, goal charger name

	this is the format required by the checker program as well, for example the command

		./solution Council_Bluffs_IA Cadillac_MI 

	might return:

		Council_Bluffs_IA, Worthington_MN, 1.18646, Albert_Lea_MN, 1.90293, Onalaska_WI, 
		0.69868, Mauston_WI, 1.34287, Sheboyan_WI, 1.69072, Cadillac_MI
	
	You can check the solution by providing your output to the included checker, for example
		
		./checker_osx “Council_Bluffs_IA, Worthington_MN, 1.18646, Albert_Lea_MN, 1.90293, 
		Onalaska_WI, 0.69868, Mauston_WI, 1.34287, Sheboygan_WI, 1.69072, Cadillac_MI”
	
	will return 
		
		Finding Path Between Council_Bluffs_IA and Cadillac_MI
		Reference result: Success, cost was 17.2531
		Candidate result: Success, cost was 17.2548


### Example Output
Graph Creation Complete
Node Count: 5151 Edge Count: 10302
Search for Approximate Path Complete

Source: Council_Bluffs_IA
Destination: Cadillac_MI

Go to City Council_Bluffs_IA    with Charge 320.000 \
Go to City Worthington_MN       with Charge 51.575 , Charge up to 320.000 \
Go to City Albert_Lea_MN        with Charge 140.287 , Charge up to 175.069 \
Go to City Onalaska_WI          with Charge 0.000 , Charge up to 90.828 \
Go to City Mauston_WI           with Charge 0.000 , Charge up to 320.000 \
Go to City Sheboygan_WI         with Charge 134.684 , Charge up to 196.123 \
Go to City Cadillac_MI          with Charge 0.000 \
Total Approximate time for the trip: 17.428835312923873 \
Total Optimal time for the trip: 16.84375527109261 \
