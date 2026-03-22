SLAU = """
2x - 1y = 1
-1x + 2y - 1z = 0
-1y + 2z - 1v = 0
-1z + 2v = 1
"""



import re # для регулярных выражений
import sys # для вывода ошибки и остановки программы


def printMatrix(A): # более красивый вывод матрицы чем в print()
	for i in range(len(A)):
		for j in range(len(A[i])):
			print(A[i][j], end=" ")
		print()
	print('\n')



# def matfromstr(SLAU): # Парсер матрицы из строки SLAU на уравнения и коэффициенты (в матрицу)
# 	A = []
# 	B = []
# 
# 
# 	for line in SLAU.strip().split("\n"):
# 		left, right = line.replace(" ", "").split("=")
# 		coeffs = [float(x) for x in re.findall(r'[-+]?\d*\.?\d+', left)]
# 		A.append(coeffs)
# 		B.append(float(right))
# 	
# 	n = len(A)
# 	a = [0]*n
# 	b = [0]*n
# 	c = [0]*n
# 	d = [0]*n
# 	
# 	for i in range(len(A)):
# 		b[i] = A[i][i]
# 		if (i > 0):
# 			a[i] = A[i][i-1]
# 		if (i < n-1):
# 			c[i] = A[i][i+1]
# 		d[i] = B[i]
# 	A = []
# 	A.append(a)
# 	A.append(b)
# 	A.append(c)
# 	A.append(d)
# 	return A



def forward_progonka(A): # Прямая прогонка
	
	# распаковка матрицы A. Элементы с 0ого индекса!
	a = A[0]
	b = A[1]
	c = A[2]
	d = A[3]
	n = len(a)
	# массивы коэффициентов
	alf = [0]*n
	bet = [0]*n
	gam = [0]*n
	
	# первая итерация
	gam[0] = b[0]
	alf[0] = - c[0]/gam[0]
	bet[0] = d[0]/gam[0]
	
	# последующие итерации до последней (не включая)
	for i in range(1, n-1):
		gam[i] = b[i] + a[i]*alf[i-1]
		alf[i] = -c[i]/gam[i]
		bet[i] = (d[i] - a[i]*bet[i-1])/gam[i]
	
	# последняя итерация
	gam[n-1] = b[n-1] + a[n-1]*alf[n-2]
	bet[n-1] = (d[n-1] - a[n-1]*bet[n-2])/gam[n-1]
	
	A = []
	A.append(alf)
	A.append(bet)
	return A




def back_progonka(A): # Обратная прогонка
	alf = A[0]
	bet = A[1]
	n = len(alf)
	x = [0]*n
	x[n-1] = bet[n-1]
	for i in range(n-2, -1, -1): # идём с шагом -1 до -1, тк последнее число не включается (до 0 по факту)
		x[i] = bet[i] + alf[i]*x[i+1]
	return x

def check(A):
	a = A[0]
	b = A[1]
	c = A[2]
	f = 0
	for i in range(len(a)):
		if (b[i] > abs(a[i]) + abs(c[i])):
			f = 1
	return f





# A = matfromstr(SLAU)

a = [0, -1, -1, -1]  # нижняя диагональ (a[0] = 0)
b = [2, 2, 2, 2]     # главная диагональ
c = [-1, -1, -1, 0]  # верхняя диагональ (c[-1] = 0)
d = [1, 0, 0, 1]     # правая часть

A = [ a, b, c, d ]
if (check(A) == 0):
	sys.exit("Invalid matrix. No one diagonal element is greater than sum of other two")

A = forward_progonka(A)
X = back_progonka(A)
print(X)

