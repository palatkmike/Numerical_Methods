SLAU = """
-106.4000x - 7.0000y - 4.9900z + 0.2600u = 1040.8100
3.6100x + 22.2000y - 8.5900z - 8.9200u = 615.4100
2.2800x + 7.7500y + 52.2000z + 9.6500u = 427.5400
-9.0000x + 5.8100y - 0.0900z + 136.8000u = -265.3500
"""

SLAU2 = """
0.2910x + 1.8100y + 9.3110z + 9.1100u = 4.2280
1.4500x + 8.5790y + 44.1950z + 42.9950u = 20.4290
-0.2900x - 1.7980y - 9.2500z - 9.0500u = -4.2080
0.0000x + 0.0820y + 0.4100z + 0.4500u = 0.1220
"""


X = [0]*4 # Задание начального приближения

eps = 1e-6
max_iter = 1000


import re # для регулярных выражений
import sys # для вывода ошибки и остановки программы





def matfromstr(SLAU): # Парсер матрицы из строки SLAU на уравнения и коэффициенты (в матрицу)
	A = []
	B = []

#	for eq in SLAU:
#		eq = eq.replace(" ", "")
#		eq = eq.replace("\n", "")
#		eq = eq.replace("-", "+-")
	
	for line in SLAU.strip().split("\n"):
		left, right = line.replace(" ", "").split("=")
		coeffs = [float(x) for x in re.findall(r'[-+]?\d*\.?\d+', left)]
		A.append(coeffs)
		B.append(float(right))
	for i in range(len(A)):
	    A[i].append(B[i])
	return A


def printMatrix(A): # более красивый вывод матрицы чем в print()
	for i in range(len(A)):
		for j in range(len(A[i])):
			if (abs(A[i][j]) > 10e-3):
				print(f"{A[i][j]:9.3f}", end=" ")
			else:
				print(f"{0:9.3f}", end=" ")
		print()
	print('\n')


def nevyaska(A,X): # Невязка. Вектор разностей правых частей
	n = len(A)
	B = [0]*n
	for i in range(n):
		s = 0
		for j in range(n):
			s += A[i][j]*X[j]
		B[i] = s - A[i][n]
	return B



def yacob_calc(A,X):
	n = len(A)
	X1 = [0]*n
	eq(X1, X)
	
	for i in range(n):
		s = 0
		for j in range(n):
			if i != j: 
				s += A[i][j]*X1[j]
		X1[i] = (A[i][n]-s)/A[i][i]
	
	return X1

def norm1(v): # 1-норма
	return sum(abs(x) for x in v)

def norm_inf(v): # Инфинити норма
	return max(abs(x) for x in v)

def eq(v1, v2):
	for i in range(len(v1)):
		v1[i] = v2[i]

def delt(v1, v2):
	v3 = [0]*len(v1)
	for i in range(len(v1)):
		v3[i] = v1[i] - v2[i]
	return v3

def diagdom(A):
	f = 1
	for i in range(len(A)):
		s = 0
		for j in range(len(A)): 
			if (i != j):
				s += abs(A[i][j])
		if (abs(A[i][i]) < s):
			f = 0
	return f

def yacobi(A,X):
	if diagdom(A) == 0:
		print("Не выполняется условие сходимости")
	else:
		print("Условие сходимости выполнено")
	
	Xpr = [0]*len(X)
	
	eq(Xpr,X)
	X = yacob_calc(A,Xpr)
	iter_count = 1
	while (  (norm_inf(delt(X,Xpr)) > eps) ):
		eq(Xpr,X)
		X = yacob_calc(A,X)
		iter_count += 1
		
		if iter_count > max_iter:
			print("Превышено максимальное количество итераций")
			break
	return X,iter_count




A = matfromstr(SLAU)
printMatrix(A)

X,iter_count = yacobi(A,X)
print(X)
print("1-норма невязки решения", norm1(nevyaska(A,X)))
print("Решение найдено за ", iter_count, " итераций")

