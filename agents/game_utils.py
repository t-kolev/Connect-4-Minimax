from enum import Enum
import numpy as np
from scipy.signal import convolve2d
from typing import Callable, Optional


class SavedState:
    pass


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


GenMove = Callable[
    [np.ndarray, BoardPiece, Optional[SavedState]],  # Arguments for the generate_move function
    tuple[PlayerAction, Optional[SavedState]]  # Return type of the generate_move function
]


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
    for i in range(row_size):
        row += "\n" + '|'
        for j in range(col_size):
            if board[i, j] == PLAYER1:
                row += ' ' + PLAYER1_PRINT
            elif board[i, j] == PLAYER2:
                row += ' ' + PLAYER2_PRINT
            else:
                row += ' ' + NO_PLAYER_PRINT
        row += '|'
    row += '\n' + '|==============|' + '\n' + '| 0 1 2 3 4 5 6|'
    return row


def string_to_board(pp_board: str) -> np.ndarray:
    """
    Takes the output of pretty_print_board and turns it back into an ndarray.
    This is quite useful for debugging, when the agent crashed and you have the last
    board state as a string.
    """
    board = np.full((6, 7), NO_PLAYER)
    split_string = pp_board.split('\n')
    sliced_str = slice(1, 7)

    for row_num, row in enumerate(split_string[sliced_str]):
        for col_num, col_piece in enumerate(row[2:15:2]):
            if col_piece == PLAYER1_PRINT:
                board[row_num, col_num] = PLAYER1
            if col_piece == PLAYER2_PRINT:
                board[row_num, col_num] = PLAYER2
    return board


def apply_player_action(board: np.ndarray, action: PlayerAction, player: BoardPiece) -> np.ndarray:
    """
    Sets board[i, action] = player, where i is the lowest open row. Raises a ValueError
    if action is not a legal move. If it is a legal move, the modified version of the
    board is returned and the original board should remain unchanged (i.e., either set
    back or copied beforehand).
    """

    if action > 6 or action < 0:
        raise ValueError
    board_modified = board.copy()
    row_size, col_size = board.shape
    for r in range(row_size)[::-1]:
        if board_modified[r, action] == NO_PLAYER:
            board_modified[r, action] = player
            break
        if r == 0:
            raise ValueError
    return board_modified


def connected_four(board: np.ndarray, player: BoardPiece) -> bool:
    """
    Returns True if there are four adjacent pieces equal to `player` arranged
    in either a horizontal, vertical, or diagonal line. Returns False otherwise.
    """

    horizontal_kernel = np.array([[1, 1, 1, 1]])
    vertical_kernel = np.transpose(horizontal_kernel)
    diag1_kernel = np.eye(4, dtype=np.uint8)
    diag2_kernel = np.fliplr(diag1_kernel)
    detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]

    for kernel in detection_kernels:
        if (convolve2d(board == player, kernel, mode="valid") == 4).any():
            return True
    return False


def check_end_state(board: np.ndarray, player: BoardPiece) -> GameState:
    """
    Returns the current game state for the current `player`, i.e. has their last
    action won (GameState.IS_WIN) or drawn (GameState.IS_DRAW) the game,
    or is play still on-going (GameState.STILL_PLAYING)?
    """

    if connected_four(board, player):
        return GameState.IS_WIN
    elif np.all(board != NO_PLAYER):
        return GameState.IS_DRAW
    else:
        return GameState.STILL_PLAYING
