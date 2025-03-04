import turtle

def koch_snowflake(turtle, order, size):
    if order == 0:
        turtle.forward(size)
    else:
        for angle in [60, -120, 60, 0]:
            koch_snowflake(turtle, order-1, size/3)
            turtle.left(angle)

def draw_koch_snowflake(order, size):
    window = turtle.Screen()
    window.bgcolor("white")

    fractal_turtle = turtle.Turtle()
    fractal_turtle.speed(2)

    for _ in range(3):
        koch_snowflake(fractal_turtle, order, size)
        fractal_turtle.right(120)

    window.exitonclick()

# Пример использования
order_input = int(input("Введите порядок кривой Коха: "))
size_input = int(input("Введите размер: "))

draw_koch_snowflake(order_input, size_input)
