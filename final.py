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
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

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
            
def score_position(board, piece):
    #score horizontally
    score = 0
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLS - 3):
            window = row_array[c:c+4]

            if window.count(piece) == 4:
                score += 100
            elif window.count(piece) == 3 and window.count(0) == 1:
                score += 10
    
    #score vertically
    for c in range(COLS):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROWS - 3):
            window = col_array[r:r+4]

            if window.count(piece) == 4:
                score += 100
            elif window.count(piece) == 3 and window.count(0) == 1:
                score += 10
    
    #score diagonal
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
    valid_locations = []
    for col in range(COLS):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board, player, pause):
    piece = player['piece']
    if pause:
        # Wait a little.
        time.sleep(0.7)

    # Test code
    # Need to generate a real move.
    col = random.randint(0, COLS-1)
    row = get_next_open_row(board, col)
    drop_piece(board, row, col, player['piece'])

    valid_locations = get_valid_locations(board)
    best_score = 0
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col

def draw_board(board):
    w.configure(bg='black')
    w.delete('all')
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
        w.create_text(CANVAS_W / 2, CANVAS_H - bottom_gap, text=game['winner'].title() + ' wins', fill=game['winner'],
                      font=tkfont.Font(family='Helvetica', size=30))
        w.create_rectangle(CANVAS_W - right_gap, CANVAS_H - bottom_gap, CANVAS_W, CANVAS_H, fill = 'white')
        w.create_text(CANVAS_W - right_gap / 2, CANVAS_H - bottom_gap / 2, text='Play\nagain')
    w.pack()
    w.update()

def play_move(event):
    # User has selected a move. Play it if possible.
    board = game['board']
    if event.y > top_gap or event.x < left_gap or event.x > CANVAS_W + right_gap:
        # Invalid position.
        w.create_text(CANVAS_W / 2, 30, font=tkfont.Font(family='Helvetica', size=20), fill='red',
                      text='Please click up here to select a column.')
        return False

    col = (event.x - left_gap) // spacing
    if board[ROWS - 1][col] > 0:
        # This row is full. Let them pick another row. The binding to the click event is still in place.
        w.create_text(CANVAS_W / 2, 30, font=tkfont.Font(family='Helvetica', size=20), fill='red',
                      text='That column is full.')
        return False

    row = get_next_open_row(board, col)
    board[row][col] = game['player']['piece']
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
    w.delete('all')
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
            pick_best_move(game['board'], player, players[0]['player'] == players[1]['player'])
        draw_board(game['board'])

        if winning_move(game['board'], player['piece']):
            game['winner'] = player['color']
            # Show the winner.
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
