import sympy as sp

# Создаем символическую переменную для x
x = sp.symbols('x')

# Определяем функцию f(x), которую вы хотите исследовать
f_x = x**3 - 6*x**2 + 9*x + 3

# Находим производную f'(x)
f_prime = sp.diff(f_x, x)

# Находим точки, где производная равна нулю на интервале (-10, 10)
candidates = sp.solve(f_prime, x, domain=sp.Interval(-10, 10))

# Для каждой кандидатской точки вычисляем вторую производную f''(x)
local_minima = []
for candidate in candidates:
    f_double_prime = sp.diff(f_prime, x)
    second_derivative_at_candidate = f_double_prime.subs(x, candidate)
    if second_derivative_at_candidate > 0:
        local_minima.append((candidate, f_x.subs(x, candidate)))

# Выводим результаты
print("Кандидаты на локальные минимумы:")
for candidate in candidates:
    print(f"x = {candidate}")

print("\nЛокальные минимумы:")
for minimum in local_minima:
    print(f"x = {minimum[0]}, f(x) = {minimum[1]}")
