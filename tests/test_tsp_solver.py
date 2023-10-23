import pytest
import numpy as np

from src.tsp_solver_base import TspSolverBase

class DummySolver(TspSolverBase):

    def solve_tsp(self, coordinates):
        solution = {i: city for i, city in enumerate(coordinates)}
        return solution

def test_generate_cities_coordinates() -> None:
    cities = 10
    solver = DummySolver()
    coordinates = solver.set_cities_coordinates(nr_of_cities=cities)
    assert np.shape(coordinates) == (cities,2)
    coordinates_in_range = np.logical_and(
        coordinates.flatten() < 1,
        coordinates.flatten() >= 0
    )
    assert all(coordinates_in_range)

def test_calculate_travelling_distance() -> None:
    cities = 10
    solver = DummySolver()
    coordinates = solver.set_cities_coordinates(nr_of_cities=cities)
    ordered_cities = solver.solve_tsp(coordinates)
    distance = solver.get_travelling_distance(ordered_cities)
    assert isinstance(distance, float)
    assert distance > 0 and distance < cities*np.sqrt(2)
    overlapping_cities = {i: np.array([0,0]) for i in range(cities)}
    distance = solver.get_travelling_distance(overlapping_cities)
    assert distance == 0
    alternating_cities = {}
    for i in range(cities):
        alternating_cities[i] = np.array([0,0]) if i%2==0 else np.array([0,1])
    assert solver.get_travelling_distance(alternating_cities) == cities
    diagonal_cities = {}
    for i in range(cities):
        diagonal_cities[i] = np.array([0,0]) if i%2==0 else np.array([1,1])
    diag_distance = solver.get_travelling_distance(diagonal_cities)
    assert diag_distance == pytest.approx(cities*np.sqrt(2))
