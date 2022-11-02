from enum import Enum
import numpy as np

BoardPiece = np.int8  # The data type (dtype) of the board
NO_PLAYER = BoardPiece(0)  # board[i, j] == NO_PLAYER where the position is empty
PLAYER1 = BoardPiece(1)  # board[i, j] == PLAYER1 where player 1 (player to move first) has a piece
PLAYER2 = BoardPiece(2)  # board[i, j] == PLAYER2 where player 2 (player to move second) has a piece

BoardPiecePrint = str  # dtype for string representation of BoardPiece
NO_PLAYER_PRINT = BoardPiecePrint(' ')
PLAYER1_PRINT = BoardPiecePrint('X')
PLAYER2_PRINT = BoardPiecePrint('O')

PlayerAction = np.int8  # The column to be played


class GameState(Enum):
    IS_WIN = 1
    IS_DRAW = -1
    STILL_PLAYING = 0


def initialize_game_state() -> np.ndarray:
    """
    Returns an ndarray, shape (6, 7) and data type (dtype) BoardPiece, initialized to 0 (NO_PLAYER).
    """
    return np.full((6, 7), NO_PLAYER)


def pretty_print_board(board: np.ndarray) -> str:
    """
    Should return `board` converted to a human readable string representation,
    to be used when playing or printing diagnostics to the console (stdout). The piece in
    board[0, 0] should appear in the lower-left. Here's an example output, note that we use
    PLAYER1_Print to represent PLAYER1 and PLAYER2_Print to represent PLAYER2):
    |==============|
    |              |
    |              |
    |    X X       |
    |    O X X     |
    |  O X O O     |
    |  O O X X     |
    |==============|
    |0 1 2 3 4 5 6 |
    """

    row_size, col_size = board.shape
    row = '|==============|'
    for i in range(row_size)[::-1]:
        row += "\n"
        for j in range(col_size):
            if board[i, j] == PLAYER1:
                row += ' ' +PLAYER1_PRINT
            elif board[i, j] == PLAYER2:
                row += ' ' + PLAYER2_PRINT
            else:
                row += ' ' + NO_PLAYER_PRINT
    row += '\n' + '|==============|' + '\n' + '|0 1 2 3 4 5 6 |'
    return row

def string_to_board(pp_board: str) -> np.ndarray:
    """
    Takes the output of pretty_print_board and turns it back into an ndarray.
    This is quite useful for debugging, when the agent crashed and you have the last
    board state as a string.
    """



def apply_player_action(board: np.ndarray, action: PlayerAction, player: BoardPiece) -> np.ndarray:
    """
    Sets board[i, action] = player, where i is the lowest open row. Raises a ValueError
    if action is not a legal move. If it is a legal move, the modified version of the
    board is returned and the original board should remain unchanged (i.e., either set
    back or copied beforehand).
    """

    if action > 6 or action < 1:
        raise ValueError
    old_board = board.copy()
    row_size, col_size = board.shape
    for r in range(row_size)[::-1]:
        if board[r, action] == NO_PLAYER:
            board[r, action] = player
            break
        else:
            raise ValueError
    return board

def connected_four(board: np.ndarray, player: BoardPiece) -> bool:
    """
    Returns True if there are four adjacent pieces equal to `player` arranged
    in either a horizontal, vertical, or diagonal line. Returns False otherwise.
    """

    row_size, col_size = board.shape
    for c in range(col_size - 3):
        for r in range(row_size):
            print(board[r][c])
            if board[r][c] == player and board[r][c + 1] == player and board[r][c + 2] == player and board[r][
                c + 3] == player:
                return True

            # Check vertical locations for win
        for c in range(col_size):
            for r in range(row_size - 3):
                if board[r][c] == player and board[r + 1][c] == player and board[r + 2][c] == player and board[r + 3][                    c] == player:
                    return True

            # Check positively sloped diagonals
        for c in range(col_size - 3):
            for r in range(row_size - 3):
                if board[r][c] == player and board[r + 1][c + 1] == player and board[r + 2][c + 2] == player and \
                        board[r + 3][c + 3] == player:
                    return True

            # Check negatively sloped diagonals
        for c in range(col_size - 3):
            for r in range(3, row_size):
                if board[r][c] == player and board[r - 1][c + 1] == player and board[r - 2][c + 2] == player and \
                        board[r - 3][c + 3] == player:
                    return True
        return False


def check_end_state(board: np.ndarray, player: BoardPiece) -> GameState:
    """
    Returns the current game state for the current `player`, i.e. has their last
    action won (GameState.IS_WIN) or drawn (GameState.IS_DRAW) the game,
    or is play still on-going (GameState.STILL_PLAYING)?
    """
    if (connected_four(board,player) == True) or (connected_four(board,player)==True):
        GameState = 1
    elif(board.all() != NO_PLAYER):
        GameState = -1
    else:
        GameState = 0
    return GameState


from typing import Callable, Optional

class SavedState:
    pass


GenMove = Callable[
    [np.ndarray, BoardPiece, Optional[SavedState]],  # Arguments for the generate_move function
    tuple[PlayerAction, Optional[SavedState]]  # Return type of the generate_move function
]

