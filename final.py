import numpy as np
from tkinter import *
from tkinter import font as tkfont
import time
import random

ROWS = 6
COLS = 7
CANVAS_H = 500
CANVAS_W = 600

left_gap = 50
right_gap = 43
top_gap = 40
middle_gap = 24
bottom_gap = 40
spacing = 69
radius = 50

def create_board():
    return np.zeros((ROWS, COLS), dtype=int)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROWS-1][col] == 0

def get_next_open_row(board, col):
    # Select the next open row in the given column.
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    # Is this board a winning position for the player with the given piece?
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

def score_position(board, piece):
    # Heuristic. Detect all the ways the given position has at least 3 in a row for the player with the given piece,
    # and the fourth is open. If there are three in a row, count 10 points; if 4 in a row, count 100.
    score = 0

    # Score horizontal
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLS - 3):
            window = row_array[c:c+4]
            if window.count(piece) == 4:
                score += 100
            elif window.count(piece) == 3 and window.count(0) == 1:
                score += 10
    
    # Score vertical
    for c in range(COLS):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROWS - 3):
            window = col_array[r:r+4]
            if window.count(piece) == 4:
                score += 100
            elif window.count(piece) == 3 and window.count(0) == 1:
                score += 10
    
    # Score diagonal
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r+i][c+i] for i in range(4)]
            if window.count(piece) == 4:
                score += 100
            elif window.count(piece) == 3 and window.count(0) == 1:
                score += 10
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r+3-i][c+i] for i in range(4)]
            if window.count(piece) == 4:
                score += 100
            elif window.count(piece) == 3 and window.count(0) == 1:
                score += 10

    return score

def get_valid_locations(board):
    # Get all the valid columns where a player could play.
    valid_locations = []
    for col in range(COLS):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def minimax(board, depth, alpha, beta, maximizing_player):
    # Get all valid columns where a piece can be dropped
    valid_locations = get_valid_locations(board)
    
    # Check if the game is in win/loss/tie
    is_terminal = winning_move(board, 1) or winning_move(board, 2) or len(valid_locations) == 0

    # Base case: if depth is 0 or the game is over
    if depth == 0 or is_terminal:
        if is_terminal:
            # If the game is over and player 1 (change this if maximizing piece changes) wins
            if winning_move(board, 1):
                return (None, float('inf'))
            # If the game is over and player 2 (change this if maximizing piece changes) wins
            elif winning_move(board, 2):
                return (None, float('-inf'))
            else:
                # Game is over with no valid moves left, which means it's a tie
                return (None, 0)
        else:
            # Subtracting the score of player 2 from player 1 to prioritize maximizing player 1's position
            return (None, score_position(board, 1) - score_position(board, 2))

    # If it's the maximizing player's turn
    if maximizing_player:
        value = float('-inf') 
        best_col = random.choice(valid_locations)  #Random best move to start

        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()  
            drop_piece(temp_board, row, col, 1)  #drop simulation piece

            #Recursively call minimax for the minimizing player's turn with decreased depth
            _, new_score = minimax(temp_board, depth - 1, alpha, beta, False)

            #Update the best score and best column if a better score is found
            if new_score > value:
                value = new_score
                best_col = col

            # Alpha-beta pruning: update alpha and prune the search if possible
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Prune the remaining branches

        return best_col, value

    # If it's the minimizing player's turn 
    else:
        value = float('inf')  
        best_col = random.choice(valid_locations)  # Random best move to start

        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()  # Copy the current board to simulate the move
            drop_piece(temp_board, row, col, 2)  # Simulate dropping a piece for player 2

            #Recursively call minimax for the maximizing player's turn with decreased depth
            _, new_score = minimax(temp_board, depth - 1, alpha, beta, True)

            #Update the best score and best column if a better score is found
            if new_score < value:
                value = new_score
                best_col = col

            #Alpha-beta pruning
            beta = min(beta, value)
            if beta <= alpha:
                break  #Prune the remaining branches

        return best_col, value

def pick_best_move(board, player, pause):
    piece = player['piece']
    if pause:
        # Wait a little.
        time.sleep(0.7)

    # Minimax algorithm parameters
    depth = 7  # You can adjust the depth for performance vs. accuracy
    maximizing_player = (piece == 1) #adjust which piece is being maximized 1 or 2(adjust the conditions in minimax if doing this as well)

    best_col = minimax(board, depth, float('-inf'), float('inf'), maximizing_player)[0]

    return best_col

def draw_board(board):
    # Draw the board, including an indication if the game is over, and a "button" to play again.
    w.delete('all')  # Clear canvas
    w.configure(bg='black')
    w.create_rectangle(left_gap, top_gap, CANVAS_W - right_gap, CANVAS_H - bottom_gap, fill='lightgreen')

    for i in range(ROWS):
        for j in range(COLS):
            fill = False
            if board[i][j] == 1:
                fill = 'red'
            if board[i][j] == 2:
                fill = 'blue'
            if fill:
                top = top_gap + (ROWS - i - 1) * spacing + radius / 2 - 4
                side = left_gap + j * spacing + radius / 2 - 4
                w.create_oval(side, top, side + radius, top + radius, fill=fill)

    # Rows. Put the game board in front of the pieces.
    for i in range(ROWS + 1):
        top = top_gap + spacing * i
        w.create_rectangle(left_gap, top, CANVAS_W - right_gap, top + middle_gap, fill='#ffe333', width=0)

    # Game board columns.
    for j in range(COLS + 1):
        side = left_gap + j * spacing
        bottom = top_gap + spacing * ROWS + middle_gap
        bottom = CANVAS_H - bottom_gap
        if j == 0 or j == COLS:
            # Make little feet.
            bottom = CANVAS_H
        w.create_rectangle(side, top_gap, side + middle_gap, bottom, fill='#ffe333', width=0)

    if game['winner'] > '':
        if game['winner'] == 'tie':
            w.create_text(CANVAS_W / 2, CANVAS_H - bottom_gap, text='Tie game',
                      fill='black', font=tkfont.Font(family='Helvetica', size=30))
        else:
            w.create_text(CANVAS_W / 2, CANVAS_H - bottom_gap, text=game['winner'].title() + ' wins',
                      fill=game['winner'], font=tkfont.Font(family='Helvetica', size=30))
        w.create_rectangle(CANVAS_W - right_gap, CANVAS_H - bottom_gap, CANVAS_W, CANVAS_H, fill='white')
        w.create_text(CANVAS_W - right_gap / 2, CANVAS_H - bottom_gap / 2, text='Play\nagain')
    w.update()

def play_move(event):
    # User has selected a move. Play it if possible.
    board = game['board']
    if event.y > top_gap or event.x < left_gap or event.x > CANVAS_W + right_gap:
        # Invalid position.
        w.create_text(CANVAS_W / 2, 30, font=tkfont.Font(family='Helvetica', size=20), fill='red',
                      text='Please click up here')
        return
    col = (event.x - left_gap) // spacing
    if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, game['player']['piece'])
        draw_board(board)
        master.quit()

def user_settings(event):
    # Check if user is changing players, or if they're ready to start.
    if buttons['red_y'] >= event.y >= buttons['red_y'] - buttons['h']:
        players[0]['player'] = 'user' if players[0]['player'] == 'computer' else 'computer'
        draw_labels()
    if buttons['blue_y'] >= event.y >= buttons['blue_y'] - buttons['h']:
        players[1]['player'] = 'user' if players[1]['player'] == 'computer' else 'computer'
        draw_labels()
    if buttons['start_y'] >= event.y >= buttons['start_y'] - buttons['h']:
        game['status'] = 'playing'
        # Terminate mainloop().
        master.quit()

def draw_labels():
    # Show the heading and the descriptions for the player selection buttons.
    w.delete('all')  # Clear canvas
    w.configure(bg='white')
    w.create_text(CANVAS_W / 2, 80, text='Connect 4',
                  font=tkfont.Font(family='Helvetica', size=30, weight='bold'))
    w.create_rectangle(buttons['x'] - 10, buttons['red_y'], buttons['x'] + buttons['w'],
                       buttons['red_y'] - buttons['h'], fill="lightgray")
    w.create_text(100, buttons['red_y'], text='Red Player', font=tkfont.Font(family='Helvetica', size=15), anchor='sw')
    w.create_rectangle(buttons['x'] - 10, buttons['blue_y'], buttons['x'] + buttons['w'],
                       buttons['blue_y'] - buttons['h'], fill="lightgray")
    w.create_text(100, buttons['blue_y'], text='Blue Player',
                  font=tkfont.Font(family='Helvetica', size=15), anchor='sw')
    w.create_rectangle(buttons['x'] - 10, buttons['start_y'], buttons['x'] + buttons['w'], buttons['start_y'] - buttons['h'],
                       fill="lightgray")

    w.create_text(buttons['x'], buttons['red_y'], text=players[0]['player'].title(), fill='red', font=buttons['font'], anchor='sw')
    w.create_text(buttons['x'], buttons['blue_y'], text=players[1]['player'].title(), fill='blue', font=buttons['font'], anchor='sw')
    w.create_text(buttons['x'], buttons['start_y'], text='Start', font=buttons['font'], anchor='sw')
    w.update()

def wait(event):
    if event.x > CANVAS_W - right_gap and event.y > top_gap:
        # Continue with a new game.
        master.quit()

def main():
    # Initialize canvas, ask user who will play.
    master.title("Connect 4")
    w.pack(expand=YES, fill=BOTH)
    # Show initial settings menu.
    draw_labels()
    w.bind("<Button-1>", user_settings)
    # Wait for user to select their settings.
    w.mainloop()

    # Start the game.
    game['board'] = create_board()
    draw_board(game['board'])

    while True:
        player = players[game['player_no']]
        if player['player'] == 'user':
            w.bind("<Button-1>", play_move)
            w.mainloop()
        else:
            # Now play. Tell it to pause if both players are the computer.
            col = pick_best_move(game['board'], player, players[0]['player'] == players[1]['player'])
            row = get_next_open_row(game['board'], col)
            drop_piece(game['board'], row, col, player['piece'])
        draw_board(game['board'])

        if winning_move(game['board'], player['piece']):
            game['winner'] = player['color']
            # Show the winner.
            draw_board(game['board'])

        # Check for a tie.
        tie = True
        for c in range(COLS):
            if game['board'][ROWS - 1][c] == 0:
                tie = False
        if tie:
            game['winner'] = 'tie'
            draw_board(game['board'])

        # Change players.
        game['player_no'] = 1 - game['player_no']
        game['player'] = players[game['player_no']]

        if game['winner'] > '':
            # Give the user a chance to choose to play again.
            w.bind("<Button-1>", wait)
            mainloop()
            # Take them back to the settings screen to play again.
            game['board'] = create_board()
            game['winner'] = ''
            draw_labels()
            w.bind("<Button-1>", user_settings)
            mainloop()

if __name__ == "__main__":
    master = Tk()
    w = Canvas(master, width=CANVAS_W, height=CANVAS_H)
    buttons = {'x': 250, 'red_y': 160, 'blue_y': 200, 'h': 30, 'w': 150,
               'font': tkfont.Font(family='Helvetica', size=15),
               'start_y': 300}
    players = [{'piece': 1, 'color': 'red', 'player': 'user'}, {'piece': 2, 'color': 'blue', 'player': 'computer'}]
    game = {'status': 'settings', 'board': create_board(), 'player_no': 0, 'player': players[0], 'winner': ''}
    main()
