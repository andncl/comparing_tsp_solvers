"""Module containing SimulatedAnnealer class"""
import copy
import logging
import itertools

import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact
import ipywidgets as widgets

from .tsp_solver_base import TspSolverBase

class BruteForceSolver(TspSolverBase):
    """ 
    The SimulatedAnnealer class formulates and solves the traveling salesman
    problem with the classical simulated annealing algorithm
    """
    def __init__(self) -> None:
        super().__init__()
        self.current_order = None
        self.current_distance = None

    def solve_tsp(self, coordinates: np.ndarray = None) -> dict:
        """
        Calculates all possible combinations of paths and finds the minimum
        
        Args:
            coordinates (numpy.ndarray): Coordinates of the given cities
        """
        index_list = list(self.cities.keys())
        permutations = list(itertools.permutations(index_list[1:]))
        all_seq = ['0'+''.join(perm) for perm in permutations]
        all_paths={seq: self.get_total_travel_distance(seq) for seq in all_seq}
        sorted_paths=dict(sorted(all_paths.items(), key=lambda item: item[1]))
        return list(sorted_paths.keys())[0]
