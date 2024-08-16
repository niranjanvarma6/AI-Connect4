import numpy as np
import random

ROWS = 6
COLS = 7

PLAYER = 0
AI = 1

PLAYER_PIECE = 1
AI_PIECE = 2

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
        print(' '.join(['P' if x == PLAYER_PIECE else 'A' if x == AI_PIECE else '.' for x in row]))

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
    turn = random.randint(PLAYER, AI)  # Randomize who starts

    while not game_over:
        # Player's turn
        if turn == PLAYER:
            col = int(input("Player (1-7), Make your Selection: ")) - 1

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_PIECE)

                if winning_move(board, PLAYER_PIECE):
                    print_board(board)
                    print("Player wins!")
                    game_over = True

        # AI's turn
        else:
            col = random.randint(0, COLS-1)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    print_board(board)
                    print("AI wins!")
                    game_over = True

        print_board(board)

        # Alternate turns
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
