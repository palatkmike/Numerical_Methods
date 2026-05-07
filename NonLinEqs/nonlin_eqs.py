import math
import time
import numpy as np
import matplotlib.pyplot as plt

# ===================== НАСТРОЙКИ =====================

eps = 1e-5

# ===================== ФУНКЦИЯ =======================

# Пример:
# 2^(x-0.1) - 1 = 0

def f(x):
	# return 2**(x - 0.1) - 1
	return x**3-4*x**2+2*x+2
# Производная для метода Ньютона
# d/dx [2^(x-0.1)] = ln(2) * 2^(x-0.1)

def df(x):
	# return math.log(2) * 2**(x - 0.1)
	return 3*x**2-8*x+2


# ===================== ГРАФИК ========================

def draw_graph(a, b):

	x = np.linspace(a, b, 1000)
	y = [f(i) for i in x]

	plt.plot(x, y)
	plt.axhline(0)
	plt.grid()

	plt.xlabel("x")
	plt.ylabel("f(x)")
	plt.title("График функции")

	plt.show()


# ================== ПОЛОВИННОЕ ДЕЛЕНИЕ ==================

def bisection(a, b, eps):

	iter_count = 0
	start = time.time()

	while abs(b - a) > eps:
		c = (a + b) / 2
		if f(a) * f(c) < 0:
			b = c
		else:
			a = c
		iter_count += 1
	x = (a + b) / 2

	work_time = time.time() - start

	return x, iter_count, work_time


# ===================== НЬЮТОН =====================

def newton(x0, eps):
	iter_count = 0
	start = time.time()

	while True:
		x1 = x0 - f(x0) / df(x0)
		if abs(x1 - x0) < eps:
			break
		x0 = x1
		iter_count += 1
	work_time = time.time() - start
	return x1, iter_count, work_time


# ===================== СЕКУЩИЕ =====================

def secant(x0, x1, eps):
	iter_count = 0
	start = time.time()

	while True:
		x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
		if abs(x2 - x1) < eps:
			break
		x0 = x1
		x1 = x2
		iter_count += 1
	work_time = time.time() - start
	return x2, iter_count, work_time


# ===================== ТАБЛИЦА =====================

def print_table():
	print()
	print("=" * 95)
	print(f"{'Метод':^25} | {'Корень':^20} | {'Итерации':^15} | {'Время':^15}")
	print("=" * 95)

	# -------- Половинное деление --------

	x, it, t = bisection(0, 1, eps)
	print(f"{'Половинное деление':^25} | "
	   f"{x:^20.10f} | "
	   f"{it:^15} | "
	   f"{t:^15.6f}")
	print("-" * 95)

	# -------- Ньютон --------

	x, it, t = newton(1, eps)
	print(f"{'Ньютон':^25} | "
	   f"{x:^20.10f} | "
	   f"{it:^15} | "
	   f"{t:^15.6f}")
	print("-" * 95)

	# -------- Секущие --------

	x, it, t = secant(0, 1, eps)
	print(f"{'Секущие':^25} | "
	   f"{x:^20.10f} | "
	   f"{it:^15} | "
	   f"{t:^15.6f}")
	print("=" * 95)


# ===================== ЗАПУСК =====================

draw_graph(-3, 3)

print_table()

