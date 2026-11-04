"""A simple two-player Tic Tac Toe game for the terminal."""


WINNING_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


def display_board(board):
    """Print the board, using cell numbers for unplayed squares."""
    cells = [mark if mark != " " else str(index + 1) for index, mark in enumerate(board)]
    print()
    print(" " + " | ".join(cells[0:3]))
    print("---+---+---")
    print(" " + " | ".join(cells[3:6]))
    print("---+---+---")
    print(" " + " | ".join(cells[6:9]))
    print()


def get_winner(board):
    """Return the winning mark, or None if nobody has won."""
    for first, second, third in WINNING_LINES:
        if board[first] != " " and board[first] == board[second] == board[third]:
            return board[first]
    return None


def play_game():
    global x_wins, o_wins, draws
    
    board = [" "] * 9
    player = "X"

    while True:
        display_board(board)
        choice = input("Player {}, choose a square (1-9): ".format(player)).strip()

        if not choice.isdigit() or not 1 <= int(choice) <= 9:
            print("Please enter a number from 1 to 9.")
            continue

        square = int(choice) - 1
        if board[square] != " ":
            print("That square is already taken. Choose another one.")
            continue

        board[square] = player
        winner = get_winner(board)
        if winner:
            display_board(board)
            print("Player {} wins!".format(winner))
            return

        if " " not in board:
            display_board(board)
            print("It's a draw!")
            return

        player = "O" if player == "X" else "X"


def main():
    print("Welcome to Tic Tac Toe!")
    try:
        play_game()
    except (EOFError, KeyboardInterrupt):
        print("\nGame ended.")


if __name__ == "__main__":
    main()