import pytest
import numpy as np

from src.tsp_solver_base import TspSolverBase

class DummySolver(TspSolverBase):
    def solve_tsp(self, coordinates):
        solution = {i: city for i, city in enumerate(coordinates)}
        return solution

@pytest.mark.parametrize([3,4,6,9,12,99], [8,4,12,59,7,99])
def test_set_cities_coordinates(nr_cities, size) -> None:
    solver = DummySolver()
    cities = solver.set_cities_coordinates(nr_cities, grid_size = size)
    assert isinstance(cities, dict)
    assert all(len(coord) for coord in cities.values())
    assert set(range(len(cities))).issubset(list(cities.keys()))

    for coords in cities.values():
        assert all(coord < size for coord in coords)

def test_get_total_travel_distance(dummy_solver) -> None:
    cities = 4
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
