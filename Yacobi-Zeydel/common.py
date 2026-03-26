# Общая программа для сравнения методов

# ------------- Системы уравнений ---------------------------

SLAU1 = """
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

# ---------------- Настройка метода Гаусса -----------------
PIV = 1 # 0 - Выключить
		# 1 - Включить рассчёт с сортировкой по максимальному элементу в столбце
		# 2 - Включить рассчёт с сортировкой по макс элементу в столбце и строке (пока не реализовано)

POG = 1 # Включить рассчёт погрешностей. Нужно задать правильный результат!
X_true1 = [-12, 30, 5, -4]
X_true2 = [9,1,-1,1]


# -------- Настройка итерационных методов ------------

X_start1 = [0]*4 # Задание начального приближения для иетрационных методов
X_start2 = [0]*4
eps = 1e-6
max_iter = 1000

# -----------------------------------------------------



import re # для регулярных выражений
import sys # для вывода ошибки и остановки программы
import time # для подсчёта времени


# -------------- Ввод вывод -------------------------------

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


def print_table(result):
    print(f"{'Метод':^10} | {'Решение':^40} | {'Отн.погрешность':^15} | {'Число итераций':^15} | {'Время':^10}")
    print(100*"=")

    print(f"{'Гаусс':^10} | "
          f"{format_vec(result.get('gauss')):^40} | "
          f"{(f'{result.get('gauss_rel_err'):.3e}' if result.get('gauss_rel_err') is not None else '-'):^15} | "
          f"{'-':^15} | "
          f"{(f'{result.get('gauss_time'):.6f}' if result.get('gauss_time') is not None else '-'):^10}")

    print(100*"-")

    print(f"{'Якоби':^10} | "
          f"{format_vec(result.get('yacobi')):^40} | "
          f"{(f'{result.get('yacobi_rel_err'):.3e}' if result.get('yacobi_rel_err') is not None else '-'):^15} | "
          f"{(str(result.get('yacobi_iter')) if result.get('yacobi_iter') is not None else '-'):^15} | "
          f"{(f'{result.get('yacobi_time'):.6f}' if result.get('yacobi_time') is not None else '-'):^10}")

    print(100*"-")

    print(f"{'Зейдель':^10} | "
          f"{format_vec(result.get('zeydel')):^40} | "
          f"{(f'{result.get('zeydel_rel_err'):.3e}' if result.get('zeydel_rel_err') is not None else '-'):^15} | "
          f"{(str(result.get('zeydel_iter')) if result.get('zeydel_iter') is not None else '-'):^15} | "
          f"{(f'{result.get('zeydel_time'):.6f}' if result.get('zeydel_time') is not None else '-'):^10}")

def format_vec(v, precision=3):
    if v is None:
        return "-"
    return "[" + ", ".join(f"{x:.{precision}f}" for x in v) + "]"


# -------------- Математические операции -------------------------------

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

def eq(v1, v2): # Приравнивание векторов
	for i in range(len(v1)):
		v1[i] = v2[i]

def delt(v1, v2): # Вектор разности векторов
	v3 = [0]*len(v1)
	for i in range(len(v1)):
		v3[i] = v1[i] - v2[i]
	return v3

def copy_matrix(A): # Копирование матрицы
    return [row[:] for row in A]


# ---------- Вычисление ошибки -----------------------------

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



# ------------- Проверки -------------------------------

def check0(A): # Проверка отсутствия нулей на главной диагонали
	for i in range(len(A)):
		if A[i][i] == 0:
			print("Error: 0 on main diagonal")
			return True
	return False


def diagdom(A): # Проверка сходимости
	f = 1
	for i in range(len(A)):
		s = 0
		for j in range(len(A)): 
			if (i != j):
				s += abs(A[i][j])
		if (abs(A[i][i]) < s):
			f = 0
	return f

# --------------------- Метод Якоби -------------------

def yacob_calc(A,X): # Подстановка по Якоби
	n = len(A)
	X1 = [0]*n
	eq(X1, X)
	
	for i in range(n):
		s = 0
		for j in range(n):
			if i != j: 
				s += A[i][j]*X[j]
		X1[i] = (A[i][n]-s)/A[i][i]
	
	return X1




def yacobi(A,X): # Реализация метода Якоби
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


# --------------------- Метод Зейделя -------------------




def zeydel_calc(A,X): # Подстановка по Зейделю
	n = len(A)
	
	for i in range(n):
		s = 0
		for j in range(n):
			if i != j: 
				s += A[i][j]*X[j]
		X[i] = (A[i][n]-s)/A[i][i]
	
	return X





def zeydel(A,X): # Реализация метода Зейделя
	Xpr = [0]*len(X)
	
	eq(Xpr,X)
	X = zeydel_calc(A,X)
	iter_count = 1
	while (  (norm_inf(delt(X,Xpr)) > eps) ):
		eq(Xpr,X)
		X = zeydel_calc(A,X)
		iter_count += 1
		
		if iter_count > max_iter:
			print("Превышено максимальное количество итераций")
			break
	return X,iter_count


# ------------ Метод Гаусса ----------------------

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
		# print("Промежуточный шаг:  ")
		# printMatrix(A)



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


# --------------- Основная программа -------------------------287

def all_solver(SLAU,X_true,X_start):
	result = {}
	A = []
	X = []
	X_start_z = [0]*len(X_start)
	eq(X_start_z , X_start)
	A = matfromstr(SLAU)
	A1 = copy_matrix(A)
	
	
	print("input matrix")
	printMatrix(A)
	start = time.time()
	if check0(A):
		print("Матрица содержит ноль на главной диагонали. Метод Гаусса не выполняется")
		result["gauss"] = None
		result["gauss_time"] = None
		result["gauss_nev"] = None
	else:
		print("Матрица не содержит 0 на диагонали. Метод Гаусса применим")
		forward(A)
		# print("Окончание прямого метода: ")
		# printMatrix(A)
		X = back(A)
		result["gauss"] = X
		result["gauss_time"] = time.time() - start
		result["gauss_nev"] = nevyaska(A1,X)
		if(POG == 1):
			result["gauss_rel_err"] = norm1(rel_err(X,X_true))
			result["gauss_abs_err"] = norm1(abs_err(X,X_true))
		else:
			result["gauss_rel_err"] = None
			result["gauss_abs_err"] = None
	if (diagdom(A1) == 0):
		print("Матрица не сходится. Итерационный метод не применим")
		result["yacobi"] = None
		result["yacobi_nev"] = None
		result["yacobi_time"] = None
		result["yacobi_iter"] = None
		result["yacobi_rel_err"] = None
		result["yacobi_abs_err"] = None
		result["zeydel"] = None
		result["zeydel_nev"] = None
		result["zeydel_time"] = None
		result["zeydel_iter"] = None
		result["zeydel_rel_err"] = None
		result["zeydel_abs_err"] = None
		
	else:
		print("Матрица сходится. Можно применить итерационные методы")
		start = time.time()
		X, iter_count = yacobi(A1,X_start)
		result["yacobi"] = X
		result["yacobi_time"] = time.time() - start
		result["yacobi_iter"] = iter_count
		result["yacobi_nev"] = nevyaska(A1,result["yacobi"])
		result["yacobi_rel_err"] = norm1(rel_err(X,X_true))
		result["yacobi_abs_err"] = norm1(abs_err(X,X_true))
		
		
		start = time.time()
		X, iter_count = zeydel(A1,X_start_z)
		result["zeydel"] = X
		result["zeydel_time"] = time.time() - start
		result["zeydel_iter"] = iter_count
		result["zeydel_nev"] = nevyaska(A1,result["zeydel"])
		result["zeydel_rel_err"] = norm1(rel_err(X,X_true))
		result["zeydel_abs_err"] = norm1(abs_err(X,X_true))
		
		print("\n\n\n")
	return result




result = all_solver(SLAU1,X_true1,X_start1)
print_table(result)
print("\n\n","#"*100,"\n\n")
result = all_solver(SLAU2,X_true2,X_start2)
print_table(result)
