import sympy as sp

# Создаем символическую переменную для x
x = sp.symbols('x')

# Определяем функцию f(x), которую вы хотите исследовать
f_x = x**3 - 6*x**2 + 9*x + 3

# Находим производную f'(x)
f_prime = sp.diff(f_x, x)

# Находим точки, где производная равна нулю на интервале (-10, 10)
candidates = sp.solve(f_prime, x, domain=sp.Interval(-10, 10))

# Пороговое значение углового коэффициента (например, если касательная параллельна y = kx)
threshold_slope = 2  # Задайте ваше пороговое значение

# Для каждой кандидатской точки вычисляем угловой коэффициент касательной
local_minima = []
for candidate in candidates:
    f_prime_at_candidate = f_prime.subs(x, candidate)
    
    # Проверяем, соответствует ли угловой коэффициент пороговому значению
    if abs(f_prime_at_candidate) <= threshold_slope:
        local_minima.append((candidate, f_x.subs(x, candidate)))

# Выводим результаты
print("Кандидаты на локальные минимумы:")
for candidate in candidates:
    print(f"x = {candidate}")

print("\nЛокальные минимумы с учетом угловых коэффициентов:")
for minimum in local_minima:
    print(f"x = {minimum[0]}, f(x) = {minimum[1]}")
