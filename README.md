# comparing_tsp_solvers
Comparing the quantum computational approaches of Grover via 
qiskit and quantum annealing on d-wave systems ocean SDK with classical
simulated annealing

## Installation
This package is installed by navigating to the top folder of this repo (where
this README file is stored) and running pip as follows. NOTE: do not forget the
dot after `-e`
```bash
pip install -e .
```
The required python packages are installed by running the following command in
the same directory:
```bash
pip install -r requirements.txt
```

## Program specification
Program name: TSP solver
Function: find the shortest route to travel through all the locations (https://en.wikipedia.org/wiki/Travelling_salesman_problem)
Input: number of cities, distances between cities, maximum acceptable distance
Output: optimal routes connecting all cities below the maximum acceptable distance
Description: The program assigns numerical indices to all cities, then calculates the length of all possible routes using the distances. All routes are encoded as quantum states, and the quantum state amplitude of the optimal routes are amplified using Grover algorithm
Error checking:
If a number does not conform to the input specs, the program prints the message “invalid number ‘X’”, where X is replaced by the offending number
If there is no optimal route satisfying the threshold, the program prints the message “No optimal found”

## Grover
After taking the input cities and distances, the program encodes all cities as quantum states and precalculates the overall distances of all routes. It then uses Grover algorithm to amplify the optimal states whose distances are below the user-defined threshold. The optimal states will appear with high probabilities in the measurement. Reference: https://github.com/Naphann/Solving-TSP-Grover.

## Adiabatic quantum computation (AQC)
