import numpy as np

ROWS = 6
COLS = 7

def create_board():
    return np.zeros((ROWS, COLS), dtype=int)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROWS-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

def print_board(board):
    flipped_board = np.flip(board, 0)
    for row in flipped_board:
        print(' '.join(['B' if x == 1 else 'R' if x == 2 else '.' for x in row]))

def winning_move(board, piece):
    for c in range(COLS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    for c in range(COLS-3):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def play_game():
    board = create_board()
    print_board(board)
    game_over = False
    turn = 0
    while not game_over:
        if turn == 0:
            col = int(input("Blue Player (1-7), Make your Selection: ")) - 1
            piece = 1
        else:
            col = int(input("Red Player (1-7), Make your Selection: ")) - 1
            piece = 2

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, piece)
            if winning_move(board, piece):
                print_board(board)
                print(f"{'Blue' if piece == 1 else 'Red'} Player wins!")
                game_over = True
                break

        print_board(board)
        turn += 1
        turn = turn % 2

def main():
    while True:
        play_game()
        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again == 'n':
            break

if __name__ == "__main__":
    main()
