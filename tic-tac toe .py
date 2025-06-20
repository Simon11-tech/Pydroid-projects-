import tkinter as tk
import random

# Game state
current_player = 'X'
board = [''] * 9
buttons = []
scores = {'X': 0, 'O': 0}
game_mode = 'AI'
difficulty = 'Medium'  # Change to Easy / Medium / Hard

# Winning patterns
def check_winner():
    win = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for a,b,c in win:
        if board[a] == board[b] == board[c] != '':
            return board[a]
    return 'Draw' if '' not in board else None

# Score update
def update_scores():
    x_label.config(text=f"X: {scores['X']}")
    o_label.config(text=f"O: {scores['O']}")

# Handle click
def handle_click(i):
    global current_player
    if board[i] or check_winner():
        return
    board[i] = current_player
    buttons[i].config(text=current_player, bg='lightblue' if current_player == 'X' else 'lightgreen')

    winner = check_winner()
    if winner:
        if winner != 'Draw':
            scores[winner] += 1
            status_label.config(text=f"{winner} wins!")
        else:
            status_label.config(text="It's a draw!")
        update_scores()
        return

    current_player = 'O' if current_player == 'X' else 'X'
    status_label.config(text=f"Turn: {current_player}")

    if game_mode == 'AI' and current_player == 'O':
        root.after(500, ai_turn)

# AI moves
def ai_turn():
    if difficulty == 'Easy':
        move = random.choice([i for i, val in enumerate(board) if val == ''])
    elif difficulty == 'Medium':
        if random.random() < 0.5:
            move = best_move()
        else:
            move = random.choice([i for i, val in enumerate(board) if val == ''])
    else:
        move = best_move()
    handle_click(move)

# Minimax algorithm
def best_move():
    def minimax(b, player):
        winner = check_winner_state(b)
        if winner == 'O':
            return 1
        elif winner == 'X':
            return -1
        elif '' not in b:
            return 0

        if player == 'O':
            best = -float('inf')
            for i in range(9):
                if b[i] == '':
                    b[i] = player
                    score = minimax(b, 'X')
                    b[i] = ''
                    best = max(score, best)
            return best
        else:
            best = float('inf')
            for i in range(9):
                if b[i] == '':
                    b[i] = player
                    score = minimax(b, 'O')
                    b[i] = ''
                    best = min(score, best)
            return best

    best_score = -float('inf')
    move = None
    for i in range(9):
        if board[i] == '':
            board[i] = 'O'
            score = minimax(board, 'X')
            board[i] = ''
            if score > best_score:
                best_score = score
                move = i
    return move

def check_winner_state(b):
    win = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for a,b_,c in win:
        if b[a] == b[b_] == b[c] != '':
            return b[a]
    return 'Draw' if '' not in b else None

# Reset board
def reset_board():
    global board, current_player
    board = [''] * 9
    current_player = 'X'
    for btn in buttons:
        btn.config(text='', bg='white')
    status_label.config(text=f"Turn: {current_player}")

# Toggle AI / 2P
def toggle_mode():
    global game_mode
    game_mode = '2P' if game_mode == 'AI' else 'AI'
    mode_button.config(text=f"Mode: {game_mode}")
    reset_board()

# Change difficulty
def toggle_difficulty():
    global difficulty
    options = ['Easy', 'Medium', 'Hard']
    index = (options.index(difficulty) + 1) % 3
    difficulty = options[index]
    diff_button.config(text=f"AI: {difficulty}")
    reset_board()

# GUI Setup
root = tk.Tk()
root.title("Tic-Tac-Toe AI")
root.geometry("300x420")

frame = tk.Frame(root)
frame.pack(pady=10)
for i in range(9):
    btn = tk.Button(frame, text='', font=('Helvetica', 18), width=5, height=2, bg='white',
                    command=lambda i=i: handle_click(i))
    btn.grid(row=i//3, column=i%3)
    buttons.append(btn)

status_label = tk.Label(root, text="Turn: X", font=('Helvetica', 14))
status_label.pack()

score_frame = tk.Frame(root)
score_frame.pack()
x_label = tk.Label(score_frame, text="X: 0", font=('Helvetica', 12))
x_label.pack(side='left', padx=10)
o_label = tk.Label(score_frame, text="O: 0", font=('Helvetica', 12))
o_label.pack(side='right', padx=10)

control_frame = tk.Frame(root)
control_frame.pack(pady=10)

reset_button = tk.Button(control_frame, text="Reset", command=reset_board)
reset_button.grid(row=0, column=0, padx=5)

mode_button = tk.Button(control_frame, text=f"Mode: {game_mode}", command=toggle_mode)
mode_button.grid(row=0, column=1, padx=5)

diff_button = tk.Button(control_frame, text=f"AI: {difficulty}", command=toggle_difficulty)
diff_button.grid(row=0, column=2, padx=5)

root.mainloop()