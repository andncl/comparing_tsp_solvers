"""Module containing SimulatedAnnealer class"""
import copy
import logging

import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact
import ipywidgets as widgets

from .tsp_solver_base import TspSolverBase

class SimulatedAnnealer(TspSolverBase):
    """ 
    The SimulatedAnnealer class formulates and solves the traveling salesman
    problem with the classical simulated annealing algorithm
    """
    def __init__(self) -> None:
        super().__init__()
        self.current_order = None
        self.current_distance = None
        self.temperature_decay = 0.0001
        self.temperature = np.sqrt(2)
        self.optimization_history = None

    def solve_tsp(self, t_0: float, dt: float, 
                  coordinates: np.ndarray = None) -> dict:
        """
        Optimizes the travelling salesman problem with simulated annealing for
        the given coordinates
        
        Args:
            coordinates (np.ndarray): City coodinates to navigate to
            t_0 (float): Initial 'temperature'
            dt (float): 'Temperature' decay per iteration

        Returns:
            dict: Dict with order as key and the respective city coords as value
        """
        if coordinates is not None:
            self._cities = coordinates
        self.optimization_history = []
        self.temperature = t_0
        self.temperature_decay = dt
        self.current_order = {i: city for i, city in enumerate(self._cities)}
        while self.temperature > dt:
            new_order = self._get_new_order()
            if self._approve_new_order(new_order):
                self.current_order = new_order
                self.current_distance = self.get_travelling_distance(new_order)
                self.temperature -= dt
            self.optimization_history.append(
                self.get_path_plot_coords(self.current_order))
            logging.debug(
                "Current distance: %s, Temp: %s",
                self.current_distance,
                self.temperature
                )
        return self.current_order

    def plot_last_optimization_history(self) -> None:
        """Plots the steps of the last optimization run """
        if self.optimization_history is None:
            raise ValueError("optimization_history is None, run solver first")
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        line, = ax.plot([], [], color = 'red')
        ax.grid()
        ax.scatter(self.cities[:,0], self.cities[:,1], color = 'black')
        def update(idx: int = 0):
            idx_path = self.optimization_history[idx]
            line.set_ydata(idx_path[:,1])
            line.set_xdata(idx_path[:,0])
            fig.canvas.draw_idle()
        interact(
            update, 
            idx=widgets.IntSlider(
                min=0, max=len(self.optimization_history)-1, step=1000, value=0)
            )
            
    def _get_new_order(self) -> dict:
        """Returns a new ordering based on the current given last order"""
        new_order = copy.copy(self.current_order)
        swap_indices = np.random.randint(0, len(self.current_order), 2)
        new_order[swap_indices[0]] = self.current_order[swap_indices[1]]
        new_order[swap_indices[1]] = self.current_order[swap_indices[0]]
        return new_order
    
    def _approve_new_order(self, new_order: dict) -> bool:
        """Returns True if new_order has a shorter travel distance than previous 
        result"""
        distance_change = self.get_travelling_distance(new_order) - \
            self.get_travelling_distance(self.current_order)
        probability = np.exp(- distance_change / self.temperature)
        logging.debug("dL: %s, prob: %s}", distance_change, probability)
        if probability > np.random.uniform():
            logging.debug("New order accepted")
            return True
        return False
    