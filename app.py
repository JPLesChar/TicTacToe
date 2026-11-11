import random

import streamlit as st

from tic_tac_toe import WINNING_LINES, get_winner


HUMAN = "X"
AI = "O"


def reset_game():
    st.session_state.board = [" "] * 9
    st.session_state.winner = None
    st.session_state.game_over = False
    st.session_state.winning_cells = []
    st.session_state.celebrated = False


def finish_if_over():
    board = st.session_state.board
    winner = get_winner(board)
    if winner:
        st.session_state.winner = winner
        st.session_state.game_over = True
        st.session_state.winning_cells = next(
            list(line)
            for line in WINNING_LINES
            if board[line[0]] == board[line[1]] == board[line[2]] == winner
        )
    elif " " not in board:
        st.session_state.winner = "Draw"
        st.session_state.game_over = True


def minimax(board, is_ai_turn, depth=0):
    """Return the best possible score for the AI from this board position."""
    winner = get_winner(board)
    if winner == AI:
        return 10 - depth
    if winner == HUMAN:
        return depth - 10
    if " " not in board:
        return 0

    scores = []
    mark = AI if is_ai_turn else HUMAN
    for index, cell in enumerate(board):
        if cell == " ":
            board[index] = mark
            scores.append(minimax(board, not is_ai_turn, depth + 1))
            board[index] = " "

    return max(scores) if is_ai_turn else min(scores)


def find_ai_move(board):
    best_score = float("-inf")
    best_moves = []
    for index, cell in enumerate(board):
        if cell == " ":
            board[index] = AI
            score = minimax(board, False, 1)
            board[index] = " "
            if score > best_score:
                best_score = score
                best_moves = [index]
            elif score == best_score:
                best_moves.append(index)
    return random.choice(best_moves)


def play_turn(index):
    board = st.session_state.board
    if st.session_state.game_over or board[index] != " ":
        return

    board[index] = HUMAN
    finish_if_over()
    if st.session_state.game_over:
        return

    board[find_ai_move(board)] = AI
    finish_if_over()


st.set_page_config(page_title="Tic Tac Toe", page_icon="⭕", layout="centered")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

    .stApp {
        background: radial-gradient(ellipse at 50% 0%, #202a48 0%, #111827 48%, #0b1020 100%);
        color: #f8fafc;
        font-family: 'DM Sans', sans-serif;
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stAppViewContainer"] .main .block-container {
        max-width: 560px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    h1 { text-align: center; font-weight: 800 !important; letter-spacing: -0.05em; }
    .subtitle { text-align: center; color: #aab5cc; margin: -0.5rem 0 1.8rem; }
    .status-card {
        text-align: center;
        background: rgba(30, 41, 59, .76);
        border: 1px solid rgba(148, 163, 184, .2);
        border-radius: 16px;
        padding: 14px 18px;
        margin: 0 0 18px;
        color: #e2e8f0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, .18);
    }
    [data-testid="stButton"] > button {
        min-height: 112px;
        border: 1px solid rgba(148, 163, 184, .24);
        border-radius: 18px;
        background: linear-gradient(145deg, rgba(38, 51, 77, .98), rgba(24, 34, 55, .98));
        color: #f8fafc;
        font-family: 'DM Sans', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        box-shadow: 0 8px 18px rgba(0, 0, 0, .2);
        transition: transform .16s ease, border-color .16s ease, box-shadow .16s ease, background .16s ease;
    }
    [data-testid="stButton"] > button:hover:not(:disabled) {
        transform: translateY(-3px) scale(1.02);
        border-color: #60a5fa;
        box-shadow: 0 12px 26px rgba(59, 130, 246, .2);
        color: #fff;
    }
    [data-testid="stButton"] > button:active:not(:disabled) { transform: scale(.97); }
    [data-testid="stButton"] > button:disabled { opacity: 1; cursor: default; }
    [data-testid="stButton"] > button[kind="primary"] {
        min-height: 48px;
        border: 0;
        border-radius: 12px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        font-size: 1rem;
        box-shadow: 0 8px 20px rgba(59, 130, 246, .22);
    }
    @keyframes mark-pop {
        0% { transform: scale(.55); opacity: .25; }
        70% { transform: scale(1.12); }
        100% { transform: scale(1); opacity: 1; }
    }
    [data-testid="stButton"] > button:disabled { animation: mark-pop .24s ease-out; }
    .footer { text-align: center; color: #8390a8; font-size: .85rem; margin-top: 1rem; }
    @media (max-width: 520px) {
        [data-testid="stButton"] > button { min-height: 88px; font-size: 2.2rem; border-radius: 14px; }
        [data-testid="stAppViewContainer"] .main .block-container { padding: 2rem 1rem; }
    }
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "board" not in st.session_state:
    reset_game()

st.title("Tic Tac Toe")
st.markdown('<p class="subtitle">You are <b style="color:#60a5fa">X</b>. Can you outsmart the AI?</p>', unsafe_allow_html=True)

if st.session_state.winner == "Draw":
    status = "🤝 It's a draw! Nice game."
elif st.session_state.winner == HUMAN:
    status = "🎉 You win! Incredible move."
elif st.session_state.winner == AI:
    status = "🤖 The AI wins this round. Try again!"
else:
    status = "Your turn — choose a square"
st.markdown(f'<div class="status-card">{status}</div>', unsafe_allow_html=True)

for row in range(3):
    columns = st.columns(3, gap="small")
    for column, index in zip(columns, range(row * 3, row * 3 + 3)):
        mark = st.session_state.board[index]
        if index in st.session_state.winning_cells:
            label = f"✨ {mark}"
        elif mark == HUMAN:
            label = "❌"
        elif mark == AI:
            label = "⭕"
        else:
            label = "　"
        column.button(
            label,
            key=f"cell_{index}",
            use_container_width=True,
            disabled=st.session_state.game_over or mark != " ",
            on_click=play_turn,
            args=(index,),
        )

if st.session_state.winner and not st.session_state.celebrated:
    if st.session_state.winner == HUMAN:
        st.balloons()
    st.session_state.celebrated = True

st.button("↻  New game", on_click=reset_game, type="primary", use_container_width=True)
st.markdown('<p class="footer">A perfect-play AI — a draw is the best you can do!</p>', unsafe_allow_html=True)
