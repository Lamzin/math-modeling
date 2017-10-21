#  -*- coding: utf-8 -*-

class MathModelingSolver(object):
    def __init__(
            self,
            differential_operator,
            greens_function,
            exact_solution,
            perturbation,
            spatial_area,
            initial_conditions,
    ):
        '''
        Continuously analytical modeling of the dynamics of linearly distributed systems with discretely observed
        initial-boundary state.
        :param(lambda x, y, t) differential_operator: L(x, y, t).
        :param(lambda x, y, t) greens_function: G(x, y, t).
        :param(lambda x, y, t) exact_solution: Y(x, y, t).
        :param(lambda x, y, t) perturbation: U(x, y, t).
        :param(array of (x, y) tuples) spatial_area: array with coordinates of spatial area vertexes.
        :param(array of (x, y, f) tuples) initial_conditions: array with initial conditions(t=0), i. e. tuple contains
            (x, y) - point coordinates and f - function value at the moment of time t=0.
        '''
        pass

    def solve(self):
        '''
        Will be called from `main` code.
        :return(lambda x, y, t): math modeling solution.
        '''
        pass
