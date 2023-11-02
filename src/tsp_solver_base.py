""" Module containing the TspSolver class """
from abc import ABC, abstractmethod

import numpy as np
import matplotlib.pyplot as plt

class TspSolverBase(ABC):
    """ TspSolverBase class formulating the TSP problem """

    def __init__(self):
        """Constructor class for TspSolverBase"""
        self._cities = None
        self.grid_size = None

    @property
    def cities(self) -> dict:
        """Cities for which we want to find the shortest path"""
        return self._cities

    @cities.setter
    def cities(self, city_dict):
        keys = [int(i) for i in city_dict.keys()]

        if not set(keys).issubset(list(range(len(city_dict)))):
            raise ValueError(
                "Each index from 0 to nr_of_cities in city dict must occur"
                )
        self._cities = city_dict

    @abstractmethod
    def solve_tsp(self, coordinates):
        """Abstract method to be implemented on the inhereting solver classes"""
        raise NotImplementedError

    def set_cities_coordinates(
        self, nr_of_cities: int, grid_size: int = 10) -> dict:
        """
        Generates a dict with city index as keys and coordinates as values

        Args:
            nr_of_cities (int): Number of cities
            gridsize(int): Mesh size of map

        Returns:
            dict: Keys are city indices and values coordinates
        """
        cities = {}
        for idx in range(nr_of_cities):
            cities[str(idx)] = np.random.randint(
                low = 0, high = grid_size, size = 2)
        self._cities = cities
        self.grid_size = grid_size
        return cities
    
    def get_total_travel_distance(self, sequence: str) -> int:
        """
        Calculates the rounded total traveling distance of the salesman
        
        Args:
            sequence (str): Sequence from all given city keys in one string

        Returns:
            int: Total travelling distance

        """
        if not self.is_sequence_valid(sequence):
            return 'Invalid'
        total_dist = 0
        sequence = list(sequence)
        for i, city_idx in enumerate(sequence):
            total_dist += self.get_inter_city_distance(
                city_idx, sequence[(i+1)%len(sequence)])
        return total_dist

    def get_inter_city_distance(self, city_1_idx, city_2_idx) -> int:
        """
        Returns the distance between two cities
        
        Args:
            city_1 (str | int): First city
            city_2 (str | int): Second city

        Returns:
            int: Distance between cities
        """
        city_1_idx = str(city_1_idx)
        city_2_idx = str(int(city_2_idx)%len(self.cities))
        if not set([city_1_idx, city_2_idx]).issubset(list(self.cities.keys())):
            raise ValueError(
                "Both given indices must be within city indices. city_1"
                f"{city_1_idx}, city_2 {city_2_idx}, cities {self.cities.keys()}"
                ) 
        vec = self.cities[city_1_idx] - self.cities[city_2_idx]
        return int(round(np.linalg.norm(vec)))

    def is_sequence_valid(self, sequence: str) -> bool:
        """
        Checks if given sequence is valid 

        Args:
            sequence (str): Sequence of cities

        Returns:
            bool: True if sequence is valid

        Raises:
            ValueError: if city index is missing from sequence, if index is 
                double, if 
        """
        if not isinstance(sequence, str):
            raise ValueError(f"sequence must be str but is {type(sequence)}")
        given_indices = list(self.cities.keys())
        if len(sequence) != len(set(sequence)):
            return False
        return set(list(sequence)).issubset(given_indices)

    def calculate_distances(self, cities: dict):
        """
        Calculates a dictionairy with city index combinations as keys and their
        distances as value
        
        Args:
            cities (dict): Dictionairy with cities and their coordinates

        Returns:
            dict: Dict giving inter city distances
        """
        distances = {}
        for first_city_idx in list(cities.keys()):
            if int(first_city_idx) < 1:
                continue
            for sec_city_idx in range(int(first_city_idx)):
                if int(sec_city_idx) > int(first_city_idx):
                    continue
                distances[
                    str(first_city_idx)+str(sec_city_idx)
                    ] = self.get_inter_city_distance(
                        first_city_idx, sec_city_idx)
        return distances

    def plot_cities_on_grid(self):
        """Plots the set cities on a map"""
        fig, ax = plt.subplots(figsize = (5,5))
        coords = np.array(list(self.cities.values()))
        ax.set_xlim((0,self.grid_size))
        ax.set_ylim((0,self.grid_size))
        ax.set_xticks(range(self.grid_size))
        ax.set_yticks(range(self.grid_size))
        ax.grid()
        ax.scatter(coords[:,0], coords[:,1], color = 'red')
        return fig, ax

    def plot_sequence(self, sequence):
        fig, axs = self.plot_cities_on_grid()
        coords = [self.cities[idx] for idx in list(sequence)]
        coords.append(self.cities['0'])
        coords = np.array(coords)
        axs.plot(coords[:,0], coords[:,1])
