def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

def is_board_full(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    while True:
        print_board(board)
        row = int(input(f"Игрок {current_player}, введите номер строки (0, 1, 2): "))
        col = int(input(f"Игрок {current_player}, введите номер столбца (0, 1, 2): "))

        if board[row][col] == " ":
            board[row][col] = current_player
        else:
            print("Эта клетка уже занята. Попробуйте снова.")
            continue

        if check_winner(board, current_player):
            print_board(board)
            print(f"Игрок {current_player} победил!")
            break

        if is_board_full(board):
            print_board(board)
            print("Ничья!")
            break

        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    main()
