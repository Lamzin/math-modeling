#  -*- coding: utf-8 -*-

# from scipy.integrate import tplquad
from sympy import *

x = Symbol('x')
y = Symbol('y')
t = Symbol('t')
a = Symbol('a')
b = Symbol('b')
c = Symbol('c')


class MathModelingSolver(object):
    def __init__(
            self,
            differential_operator,
            exact_solution,
            greens_function=None,
            perturbation=None,
            spatial_area=[],
            initial_conditions=[],
            boundary_conditions=[],
            T=100
    ):
        '''
        Continuously analytical modeling of the dynamics of linearly distributed systems with discretely observed
        initial-boundary state.
        :param(array of  (x, y, t,lambda p : (x, y, t)) differential_operator: L(x, y, t).
        :param(lambda x, y, t) greens_function: G(x, y, t).
        :param(lambda x, y, t) exact_solution: Y(x, y, t).
        :param(lambda x, y, t) perturbation: U(x, y, t).
        :param(array of (x, y) tuples) spatial_area: array with coordinates of spatial area vertexes.
        :param(array of (x, y, f) tuples) initial_conditions: array with initial conditions(t=0), i. e. tuple contains
            (x, y) - point coordinates and f - function value at the moment of time t=0.
        :param(array of (x, y, t, f) tuples) boundary_conditions: array with boundary conditions, i. e. tuple contains
            (x, y) - point coordinates and f - function value at the moment of time t.
        :param(const T) right border of time interval
        '''
        self.differential_operator = differential_operator
        self.exact_solution = eval(exact_solution)
        self.greens_function = greens_function
        self.calc_perturbation()
        self.spatial_area = spatial_area
        self.initial_conditions = initial_conditions
        self.boundary_conditions = boundary_conditions
        self.T = T

    def calc_perturbation(self):
        f = self.exact_solution
        self.perturbation = eval(self.differential_operator)

    def exact_solution_at_point(self, x_, y_, t_=0):
        return lambdify((x, y, t), self.exact_solution, 'numpy')(x_, y_, t_)

    def solve(self):
        count_vertex = len(self.spatial_area)
        y_infinity = 0
        for i in range(count_vertex):
            func = self.greens_function * self.perturbation
            y_infinity += integrate(func, ())
        '''
        Will be called from `main` code.
        :return(lambda x, y, t): math modeling solution.
        '''
        pass


# L = '2*x*diff(f, x, y) + diff(f, x)'
# G = 't*abs(t)'
# Y = eval('y*x**2 + x*y + t')
# f = Y
# print(Y* Y)
# model = MathModelingSolver(L, Y, greens_function=G)
# print(model.perturbation)
# print(model.greens_function)
# print(model.exact_solution_at_point(x_=1, y_=2))
