import pygame
import sys

# Инициализация Pygame
pygame.init()

# Размеры окна и цвета
WINDOW_SIZE = 400
BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
LINE_WIDTH = 5
GRID_SIZE = 3
CELL_SIZE = WINDOW_SIZE // GRID_SIZE

# Создание окна
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Крестики-нолики")

# Создание игрового поля
grid = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_player = 'X'  # Начинает игрок X

# Функция для отрисовки игрового поля
def draw_board():
    # Очистка фона
    screen.fill(BG_COLOR)

    # Рисование сетки
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE), LINE_WIDTH)

    # Рисование крестиков и ноликов
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            cell = grid[row][col]
            if cell == 'X':
                draw_x(row, col)
            elif cell == 'O':
                draw_o(row, col)

# Функция для отрисовки крестика
def draw_x(row, col):
    x = col * CELL_SIZE
    y = row * CELL_SIZE
    pygame.draw.line(screen, LINE_COLOR, (x, y), (x + CELL_SIZE, y + CELL_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (x + CELL_SIZE, y), (x, y + CELL_SIZE), LINE_WIDTH)

# Функция для отрисовки нолика
def draw_o(row, col):
    x = col * CELL_SIZE + CELL_SIZE // 2
    y = row * CELL_SIZE + CELL_SIZE // 2
    radius = CELL_SIZE // 2 - LINE_WIDTH // 2
    pygame.draw.circle(screen, LINE_COLOR, (x, y), radius, LINE_WIDTH)

# Функция для проверки победы
def check_win(player):
    # Проверка строк и столбцов
    for i in range(GRID_SIZE):
        if all(grid[i][j] == player for j in range(GRID_SIZE)) or all(grid[j][i] == player for j in range(GRID_SIZE)):
            return True

    # Проверка диагоналей
    if all(grid[i][i] == player for i in range(GRID_SIZE)) or all(grid[i][GRID_SIZE - 1 - i] == player for i in range(GRID_SIZE)):
        return True

    return False

# Основной цикл программы
game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_player == 'X':
                player = 'X'
            else:
                player = 'O'
            
            x, y = event.pos
            col = x // CELL_SIZE
            row = y // CELL_SIZE

            if grid[row][col] == ' ':
                grid[row][col] = player
                if check_win(player):
                    print(f"Игрок {player} выиграл!")
                    game_over = True
                elif ' ' not in [cell for row in grid for cell in row]:
                    print("Ничья!")
                    game_over = True
                else:
                    current_player = 'X' if current_player == 'O' else 'O'

    draw_board()
    pygame.display.flip()

# Завершение программы
pygame.quit()
sys.exit()
