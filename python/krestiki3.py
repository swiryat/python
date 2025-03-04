import pygame
import sys

# Инициализация Pygame
pygame.init()

# Размеры окна и цвета
WINDOW_SIZE = 400
BG_COLOR = (255, 255, 255)
CELL_COLOR = (0, 0, 0)

# Создание окна
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Белый квадрат")

# Положение и размер квадрата
square_x = 100
square_y = 100
square_size = 200
square_color = BG_COLOR  # Изначально белый

# Функция для отрисовки квадрата
def draw_square():
    pygame.draw.rect(screen, square_color, (square_x, square_y, square_size, square_size))

# Основной цикл программы
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                if square_x <= x <= square_x + square_size and square_y <= y <= square_y + square_size:
                    square_color = CELL_COLOR  # Изменить цвет на черный

    # Заполняем фон
    screen.fill(BG_COLOR)
    draw_square()

    pygame.display.flip()

# Завершение программы
pygame.quit()
sys.exit()
