# comparing_tsp_solvers
Universal platform to quantify different traveling salesman
problem (TSP) solvers. Two different approaches are demonstrated her. Namely a brute force algorim and the quantum Grover algorithm

## Traveling Salesman Problem
The traveling salesman is the seemingly simple task to find a minimum route to connect a number of N cities on a map, such that the total distance to pass to
visit all cities is minimal. One can find (N-1)! possible paths for a round 
tour through all available stops. This is feasible for a hand full of cities
e.g for 5  we find 4!=24  paths. However only doubling the cities to 8 already 
yields 7! = 5040 possible trips. Therefore economists have been showing
interest in solving this problem with the lowest possible computational cost
since many centuries.
## Installation
This package is installed by navigating to the top folder of this repo (where
this README file is stored) and running pip as follows. NOTE: do not forget the
dot after `-e`
```bash
pip install -e .
```
The required python packages are installed automatically as they are
specified in the pyproject.toml file.

### Tests
Tests are written with the pytest package and can be executed by running the
following command in the repositories top folder.

```bash
python -m pytest ./tests
```

## Program specification
**Program name:** Comparing TSP solvers
**Function:** Universal platform to quantify different traveling salesman
problem (TSP) solvers 
**Inputs:** number of cities, grid-size of city map, type of solver
**Output:** optimal routes connecting all cities on a round trip
**Description:** The python modules provides a uniform test bed for different
TSP solvers. An abstract base class handling city generation on a map is
implemented calculating total and inter-city distances while validating output
sequences.
Here two different approaches are implemented. Namely a brute
force algorim and the quantum Grover algorithm
**Error checking**:
- Cities dictionaries are checked for their uniformity and coordinates
- Possible sequences are checked for their validity 


### Grover
After taking the input cities and distances, the program encodes all cities as quantum states and precalculates the overall distances of all routes. It then uses Grover algorithm to amplify the optimal states whose distances are below the user-defined threshold. The optimal states will appear with high probabilities in the measurement. Reference: https://github.com/Naphann/Solving-TSP-Grover.

### Brute force solver
The brute force solver finds all (n-1)! possible tours for the traveling
salesman and calculates their distances. The most optimal route is returned by
searching for the entry with the shortest distsance.
## Contribution
This project has been written by Jonathan Huang and Andreas Nickl within the
course 'Quantum Software and Programming' at University of Technology Sydney.

**Jonathan Huang**

- Research on Grover algorithm and its application on the traveling salesman
problem
- Implementation of the Grover algorithm in qiskit

**Andreas Nickl**
- Setup and structuring of the given python module
- Class implementation of the Grover algorithm
- Unit tests in pytest
