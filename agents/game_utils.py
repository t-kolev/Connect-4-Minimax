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
    """A class used to represent the GameStates.

    Attributes:
        IS_WIN
        IS_DRAW
        STILL_PLAYIN
    """
    IS_WIN = 1
    IS_DRAW = -1
    STILL_PLAYING = 0


GenMove = Callable[
    [np.ndarray, BoardPiece, Optional[SavedState]],  # Arguments for the generate_move function
    tuple[PlayerAction, Optional[SavedState]]  # Return type of the generate_move function
]


def initialize_game_state() -> np.ndarray:
    """Returns a boad  with shape (6, 7) and data type (dtype) BoardPiece, initialized to 0 (NO_PLAYER).

    Returns:
        np.ndarray: The board with correct attributes

    """

    return np.full((6, 7), NO_PLAYER)


def pretty_print_board(board: np.ndarray) -> str:
    """Converts a board state into a human readable string representation.

    Args:
        board: The current state of the game.

    Returns:
        str: The human readable string representation of the board.
    """

    row_size, col_size = board.shape
    row = '|==============|'
    for i in range(row_size):
        row += "\n" + '|'
        for j in range(col_size):
            row += piece_recognition(board, i, j)
        row += '|'
    row += '\n' + '|==============|' + '\n' + '| 0 1 2 3 4 5 6|'
    return row


# bei dem test nicht richtig, aber in main schon


def piece_recognition(board: np.ndarray, i: int, j: int) -> str:
    """Converts the Player piece into the player's piece print.

    Args:
        board : The current state of the game.
        i: The row index of the board.
        j: The column index of the board.

    Returns:
        str: The player's print.
    """
    if board[i, j] == PLAYER1:
        return ' ' + PLAYER1_PRINT
    elif board[i, j] == PLAYER2:
        return ' ' + PLAYER2_PRINT
    else:
        return ' ' + NO_PLAYER_PRINT


def string_to_board(pp_board: str) -> np.ndarray:
    """Converts a string representation of a bord into a np.ndarray.

    Args:
        pp_board: The string representation of a board.

    Returns:
        The converted board as a np.ndarray.
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
    """Applies a wanted move to the board.

    Args:
        board: The current state of the game.
        action: The column to be played.
        player: The current player to place a piece.

    Returns:
        np.ndarray: The state of the game after applying the move.

    """

    if action > 6 or action < 0:
        raise ValueError
    new_board = board.copy()
    row = lowest_row(new_board, action)
    new_board[row, action] = player
    return new_board


def lowest_row(board: np.ndarray, action: PlayerAction) -> int:
    """Gets the correct row, where the move should be executed.

    Args:
        board: The current state of the game.
        action: The column to be played.

    Returns:
        int: The lowest possible row.
    """
    row_size, col_size = board.shape
    for r in range(row_size)[::-1]:
        if board[r, action] == NO_PLAYER:
            return r
        if r == 0:
            raise ValueError


def connected_four(board: np.ndarray, player: BoardPiece) -> bool:
    """Checks if there is 4 adjacent pieces equal to `player` arranged in either a horizontal, vertical, or diagonal line.

    Args:
        board: The current state of the game.
        player: The current player to place a piece.

    Returns:
        bool: True if there are four adjacent pieces equal to `player` in one of the 4 directions, False otherwise.
    """

    row_kernel = np.ones((4, 1), player)
    column_kernel = np.transpose(row_kernel)
    dia_kernel = np.eye(4, dtype=player)
    flipped_dia_kernel = np.fliplr(dia_kernel)
    kernels = [row_kernel, column_kernel, dia_kernel, flipped_dia_kernel]

    for kernel in kernels:
        result = (convolve2d(board == player, kernel, mode="full") == 4)
        if result.any():
            return True
    return False


def check_end_state(board: np.ndarray, player: BoardPiece) -> GameState:
    """Checks what the current game state for the current `player` is.

    Args:
        board: The current state of the game.
        player: The current player to place a piece.

    Returns:
        GameState:  GameState.IS_WIN if the player's move won with ther last action won, (GameState.IS_DRAW) if it caused a drawn or (GameState.STILL_PLAYING) if the game is play still on-going .
    """

    if connected_four(board, player):
        return GameState.IS_WIN
    elif np.all(board != NO_PLAYER):
        return GameState.IS_DRAW
    else:
        return GameState.STILL_PLAYING
