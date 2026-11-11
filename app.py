import streamlit as st

from tic_tac_toe import get_winner


def reset_game():
    st.session_state.board = [" "] * 9
    st.session_state.current_player = "X"
    st.session_state.winner = None
    st.session_state.game_over = False


def handle_move(index):
    board = st.session_state.board
    if board[index] != " " or st.session_state.game_over:
        return

    board[index] = st.session_state.current_player
    winner = get_winner(board)

    if winner:
        st.session_state.winner = winner
        st.session_state.game_over = True
    elif " " not in board:
        st.session_state.winner = "Draw"
        st.session_state.game_over = True
    else:
        st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"


st.set_page_config(page_title="Tic Tac Toe", page_icon="❌", layout="centered")

if "board" not in st.session_state:
    reset_game()

st.title("Tic Tac Toe")

cols = st.columns(3)
for index, col in enumerate(cols):
    label = st.session_state.board[index] if st.session_state.board[index] != " " else " "
    disabled = st.session_state.game_over or st.session_state.board[index] != " "
    if col.button(label, key=f"cell_{index}", use_container_width=True, disabled=disabled):
        handle_move(index)

if st.session_state.winner == "Draw":
    st.success("It's a draw!")
elif st.session_state.winner:
    st.success(f"Player {st.session_state.winner} wins!")
else:
    st.info(f"Player {st.session_state.current_player}'s turn")

st.button("Restart game", on_click=reset_game)
