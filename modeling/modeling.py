#  -*- coding: utf-8 -*-

# from scipy.integrate import tplquad
from sympy import *

x1 = Symbol('x1')
x2 = Symbol('x2')
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
        :param(array of  (x1, x2, t,lambda p : (x1, x2, t)) differential_operator: L(x1, x2, t).
        :param(lambda x1, x2, t) greens_function: G(x1, x2, t).
        :param(lambda x1, x2, t) exact_solution: Y(x1, x2, t).
        :param(lambda x1, x2, t) perturbation: U(x1, x2, t).
        :param(array of (x1, x2) tuples) spatial_area: array with coordinates of spatial area vertexes.
        :param(array of (x1, x2, f) tuples) initial_conditions: array with initial conditions(t=0), i. e. tuple contains
            (x1, x2) - point coordinates and f - function value at the moment of time t=0.
        :param(array of (x1, x2, t, f) tuples) boundary_conditions: array with boundary conditions, i. e. tuple contains
            (x1, x2) - point coordinates and f - function value at the moment of time t.
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

    def exact_solution_at_point(self, x1_, x2_, t_=0):
        return lambdify(
            (x1, x2, t), self.exact_solution, 'numpy'
        )(x1_, x2_, t_)

    def solve(self):
        count_vertex = len(self.spatial_area)
        y_infinity = 0
        for i in range(count_vertex):
            func = self.greens_function * self.perturbation
            y_infinity += integrate(func, ())
        '''
        Will be called from `main` code.
        :return(lambda x1, x2, t): math modeling solution.
        '''
        pass


# L = '2*x1*diff(f, x1, x2) + diff(f, x1)'
# G = 't*abs(t)'
# Y = eval('x2*x1**2 + x1*x2 + t')
# f = Y
# print(Y* Y)
# model = MathModelingSolver(L, Y, greens_function=G)
# print(model.perturbation)
# print(model.greens_function)
# print(model.exact_solution_at_point(x1_=1, x2_=2))
