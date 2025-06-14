from flask import Flask, render_template, request, redirect, url_for, session
import math

app = Flask(__name__)
app.secret_key = 'secret-key'

def check_winner(brd, player):
    win = [(0,1,2), (3,4,5), (6,7,8),
           (0,3,6), (1,4,7), (2,5,8),
           (0,4,8), (2,4,6)]
    return any(brd[i] == brd[j] == brd[k] == player for i,j,k in win)

def empty_cells(brd):
    return [i for i, x in enumerate(brd) if x == ' ']

def is_full(brd):
    return ' ' not in brd

def minimax(brd, is_maximizing):
    if check_winner(brd, 'O'):
        return 1
    if check_winner(brd, 'X'):
        return -1
    if is_full(brd):
        return 0

    if is_maximizing:
        best = -math.inf
        for i in empty_cells(brd):
            brd[i] = 'O'
            score = minimax(brd, False)
            brd[i] = ' '
            best = max(best, score)
        return best
    else:
        best = math.inf
        for i in empty_cells(brd):
            brd[i] = 'X'
            score = minimax(brd, True)
            brd[i] = ' '
            best = min(best, score)
        return best

def best_move(brd):
    best_score = -math.inf
    move = None
    for i in empty_cells(brd):
        brd[i] = 'O'
        score = minimax(brd, False)
        brd[i] = ' '
        if score > best_score:
            best_score = score
            move = i
    return move

@app.route('/')
def index():
    if 'board' not in session:
        session['board'] = [' '] * 9
        session['message'] = ''
    return render_template('index.html', board=session['board'], message=session.get('message', ''))

@app.route('/move/<int:cell>')
def move(cell):
    board = session.get('board', [' '] * 9)

    if board[cell] != ' ' or check_winner(board, 'X') or check_winner(board, 'O') or is_full(board):
        return redirect(url_for('index'))

    board[cell] = 'X'

    if check_winner(board, 'X'):
        session['message'] = "You win!"
    elif is_full(board):
        session['message'] = "It's a draw!"
    else:
        ai = best_move(board)
        if ai is not None:
            board[ai] = 'O'
            if check_winner(board, 'O'):
                session['message'] = "AI wins!"
            elif is_full(board):
                session['message'] = "It's a draw!"
            else:
                session['message'] = ''

    session['board'] = board
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    session['board'] = [' '] * 9
    session['message'] = ''
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
