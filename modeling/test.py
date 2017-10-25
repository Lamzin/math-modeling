from sympy import *
import numpy as np
x = Symbol('x')
y = Symbol('y')
t = Symbol('t')
u = eval('y*x**2 + y*x')
# yprime = diff(u,x,y)
# F
# yprime = eval('diff(y*x**2 + y*x, x, y) ')

q = eval('Abs(x)')
qq = lambdify(x, q, 'numpy')
print(qq(2))

L = '2*x*diff(f, x, y) + diff(f, x)'
Y = eval('y*x**2 + x*y')
f = Y
LU = eval(L)
print(LU)
I = integrate('x*y', (x,0,Y))
print(I)


f = lambdify((x, y), LU, 'numpy')

f_la = lambda x,y :f(x, y)
print(f_la(5, 1))

a,b=1,0
x_A,x_B = 1,2
I = integrate('x',(y, 0, b+a*x),(x,x_B,x_A))
print(I)


