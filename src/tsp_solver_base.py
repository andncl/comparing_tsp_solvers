""" Module containing the TspSolver class """
from abc import ABC, abstractmethod

import numpy as np
import matplotlib.pyplot as plt

class TspSolverBase(ABC):
    """ TspSolverBase class formulating the TSP problem """

    def __init__(self):
        self._cities = None

    @property
    def cities(self):
        """ Cities for which we want to find the shortest path """
        return self._cities

    @abstractmethod
    def solve_tsp(self, coordinates):
        pass

    def set_cities_coordinates(self, nr_of_cities: int) -> np.ndarray:
        """Generates a set of city coordinates"""
        coordinates = np.random.rand(nr_of_cities, 2)
        self._cities = coordinates
        return self._cities
    
    def get_travelling_distance(self, ordered_cities: dict) -> float:
        """
        Calculates and returns the total travel distance for a given solution

        Args:
            ordered_cities (dict): Dict with respective order (int) as key and 
                city coordinates (np.ndarray) as values

        Returns:
            float: total travel distance of salesman
        """
        total_distance = 0
        for idx, location in ordered_cities.items():
            vec = location - ordered_cities[(idx+1)%len(ordered_cities)]
            city_distance = np.linalg.norm(vec)
            total_distance += city_distance
        return total_distance
    
    def get_path_plot_coords(self, ordered_cities) -> np.ndarray:
        """
        Returns the plotting coordinates (essentially adding the first result 
        to the end)
        
        Args:
            ordered_cities (dict)

        Returns:
            np.array: Array with plotting coordinates
        """
        coords = list(ordered_cities.values())
        coords.append(coords[0])
        return np.array(coords)
    
    def plot_result(self, ordered_cities) -> plt.figure:
        """Plots the given path between cities"""
        coords = self.get_path_plot_coords(ordered_cities)
        fig, axs = plt.subplots()
        axs.plot(coords[:,0], coords[:,1])
        axs.scatter(coords[:,0], coords[:,1], color = 'red')
        return fig, axs
