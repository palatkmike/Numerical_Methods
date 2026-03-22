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


PIV = 1 # 0 - Выключить
		# 1 - Включить рассчёт с сортировкой по максимальному элементу в столбце
		# 2 - Включить рассчёт с сортировкой по макс элементу в столбце и строке (пока не реализовано)


POG = 1 # Включить рассчёт погрешностей. Нужно задать правильный результат!

X_true = [-12, 30, 5, -4]
X_true2 = [9,1,-1,1]
#
############################

import re # для регулярных выражений
import sys # для вывода ошибки и остановки программы

def check0(A): # Проверка отсутствия нулей на главной диагонали
	for i in range(len(A)):
		if A[i][i] == 0:
			print("Error: 0 on main diagonal")
			return True
	return False


def printMatrix(A): # более красивый вывод матрицы чем в print()
	for i in range(len(A)):
		for j in range(len(A[i])):
			print(A[i][j], end=" ")
		print()
	print('\n')



def forward(A): # прямой ход метода Гаусса
	n = len(A)
	for i in range(n-1):
		if (PIV == 1):
			pivot(A,i)
		#if (PIV == 2):
		#	fullpivot(A,i)
		for j in range(i + 1, n ):
			factor = A[j][i] / A[i][i]
		
			for k in range(len(A[j])):
				A[j][k] = A[j][k] - factor * A[i][k]
		print("Промежуточный шаг:  ")	
		printMatrix(A)



def back(A): # Обратный ход метода Гаусса
	n = len(A)
	X = [0]*n
	X[n-1] = A[n-1][n]/A[n-1][n-1]
	for i in range(n-2, -1, -1):
		a=0
		for j in range(i+1, n):
			a=a+A[i][j]*X[j]
		X[i] = (A[i][n]-a)/A[i][i]
	return X

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

def pivot(A,i): # Меняет местами строку i
	#  матрицы на строку которая ниже i и у которой элемент главной диагонали больше
	n=len(A)
	max_i = i
	max = A[i][i]
	for j in range(i,n):
		if (abs(A[j][i]) > abs(A[max_i][i])):
			max_i = j
			max = A[max_i][i]
	temp = A[i]
	A[i] = A[max_i]
	A[max_i] = temp

	return A

def nevyaska(A,X): # Невязка. Вектор разностей правых частей
	n = len(A)
	B = [0]*n
	for i in range(n):
		s = 0
		for j in range(n):
			s += A[i][j]*X[j]
		B[i] = s - A[i][n]
	return B

def norm1(v): # 1-норма
    return sum(abs(x) for x in v)

def norm_inf(v): # Инфинити норма
    return max(abs(x) for x in v)

def copy_matrix(A):
    return [row[:] for row in A]


def abs_err(X,X_true):
	D = [0]*len(X) 
	for i in range(len(X)):
		D[i] = abs(X[i] - X_true[i])
	return D

def rel_err(X,X_true):
	D = abs_err(X,X_true)
	Do = [0]*len(X) 
	for i in range(len(X)):
		Do[i] = D[i]/abs(X_true[i])
	return Do

#################################################
# def get_A_only(A):
#     return [row[:-1] for row in A]
# 
# 
# def solve(A, b):
#     M = [A[i][:] + [b[i]] for i in range(len(A))]
#     forward(M)
#     return back(M)
# 
# 
# def inverse_matrix(A):
#     n = len(A)
#     A_only = get_A_only(A)
#     
#     inv = []n
# 
#     for i in range(n):
#         e = [0]*n
#         e[i] = 1
# 
#         x = solve(copy_matrix(A_only), e)
#         inv.append(x)
# 
#     # транспонирование
#    return [[inv[j][i] for j in range(n)] for i in range(n)]
###############################################


### Ввод из консоли
# row = input("Enter 1st eq: ")
# parts = row.split(",")
# n = len(parts) - 1
# nums = []
# for i in parts:
# 	nums.append(float(i))
# A.append(nums)
# 	 
# for i in range(n-1):
# 	row = input("Enter the next eq: ")
# 	parts = row.split(",")
# 	n1 = len(parts)
# 	if n1 != n + 1:
# 		sys.exit("Invalid input")
# 	nums = []
# 	for i1 in parts:
# 		nums.append(float(i1))
#	A.append(nums)


A = []
X = []

A = matfromstr(SLAU)
A1 = copy_matrix(A)

if check0(A):
   sys.exit("Invalid matrix. Zeros on main diagonal")
print("input matrix")
printMatrix(A)

forward(A)
printMatrix(A)
X = back(A)
print("Result:  ")
print(X)

nev = nevyaska(A1,X)
print("\nnevyaska:  ")
print(nev)

print("\nNorma 1:  ")
print(norm1(nev))


print("\nInfinity norma:  ")
print(norm_inf(nev))

if(POG == 1):
	print("\nAbsolut error:  ")
	print(abs_err(X,X_true))
	print(norm1(abs_err(X,X_true)))
	
	print("\nRelative error:  ")
	print(rel_err(X,X_true))
	print(norm1(rel_err(X,X_true)))
print("##########################################################")
A = []
X = []

A = matfromstr(SLAU2)
A1 = copy_matrix(A)

if check0(A):
   sys.exit("Invalid matrix. Zeros on main diagonal")
print("input matrix")
printMatrix(A)

forward(A)
printMatrix(A)
X = back(A)
print("Result:  ")
print(X)

nev = nevyaska(A1,X)
print("\nnevyaska:  ")
print(nev)

print("\nNorma 1:  ")
print(norm1(nev))


print("\nInfinity norma:  ")
print(norm_inf(nev))

if(POG == 1):
	print("\nAbsolut error:  ")
	print(abs_err(X,X_true2))
	print(norm1(abs_err(X,X_true2)))
	
	
	print("\nRelative error:  ")
	print(rel_err(X,X_true2))

	print(norm1(rel_err(X,X_true2)))

