import random
from typing import Tuple

from agents.game_utils import *
import numpy as np

#Mainly for testing
def best_move(board: np.ndarray, player: PlayerAction) -> PlayerAction:
    """Picks the best move to take for a board.

    Args:
        board: The current state of the game.
        player: The current player to place a piece.

    Returns:
        PlayerAction: The best column to play at.
    """
    max_score = -10000
    col_to_play = random.choice(valid_moves(board))
    for col in valid_moves(board):
        new_board = board.copy()
        new_board = apply_player_action(new_board, col_to_play, player)
        score = eval_pos(new_board, player)
        if score > max_score:
            max_score = score
            col_to_play = col
    return col_to_play


def count_elements(four_piece: list, player: PlayerAction) -> int:
    """Counts how elements each player has in 4 adjacent places in the board and sets the score accordingly

    Args:
        four_piece: A list with 4 elements
        player: The current player to place a piece.

    Returns:
        int: The score of the list with 4 elements
    """
    if player == PLAYER1:
        player1 = four_piece.count(PLAYER1)
        player2 = four_piece.count(PLAYER2)
    else:
        player1 = four_piece.count(PLAYER2)
        player2 = four_piece.count(PLAYER1)
    no_player = four_piece.count(NO_PLAYER)

    if player1 == 4:
        return 1000
    if player1 == 3 and no_player == 1:
        return 10
    if player1 == 2 and no_player == 2:
        return 5
    if player2 == 4:
        return -1000
    if player2 == 3 and no_player == 1:
        return -100
    if player2 == 2 and no_player == 2:
        return -5
    else:
        return 0


def eval_pos(board: np.ndarray, player: PlayerAction) -> int:
    """Adds the score for all directions.

    Args:
        board: The current state of the game.
        player: The current player to place a piece.

    Returns:
        int: The score for the whole board.
    """
    score = score_for_rows(board, player)
    score += score_for_cols(board, player)
    score += score_for_dias1(board, player)
    score += score_for_dias2(board, player)
    return score


def score_for_rows(board: np.ndarray, player) -> int:
    """Takes whole rows of the board and sums their score.

    Args:
        board: The current state of the game.
        player:

    Returns:
        int: The score for each row.
    """
    score_for_row = 0
    for rows in range(6):
        whole_row = board[rows, :]
        score_for_row += check_4_pieces_of_row(whole_row, player)
    return score_for_row


def score_for_cols(board: np.ndarray, player: PlayerAction) -> int:
    """Takes whole columns of the board and sums their score.

    Args:
        board: The current state of the game.
        player:

    Returns:
        int: The score for each column.
    """
    score_for_col = 0
    for col in range(7):
        whole_col = board[:, col]
        score_for_col += check_4_pieces_of_col(whole_col, player)
    return score_for_col


def score_for_dias1(board: np.ndarray, player: PlayerAction) -> int:
    """Calculates the score for all anti-diagonals with 4 pieces.

    Args:
        board: The current state of the game.
        player: The current player to place a piece.

    Returns:
        int: The score for each diagonal with 4 elements.
    """

    score = 0
    for r in range(3):
        for c in range(4):
            window = []
            for i in range(4):
                piece = board[r + i, c + i]
                window.append(piece)
            score += count_elements(window, player)

    return score


def score_for_dias2(board: np.ndarray, player: PlayerAction) -> int:
    """Checks all the main diagonals with length 4 and sums their score.

        Args:
        board: The current state of the game.
        player: The current player to place a piece.

    Returns:
        int: The score for all  diagonal with 4 elements.
    """
    score = 0

    for r in range(3):
        for c in range(4):
            window = []
            for i in range(4):
                piece = board[r + 3 - i, c + i]
                window.append(piece)
            score += count_elements(window, player)
    return score


''''

def score_for_dias1(board: np.ndarray):
    score_for_dia1 = 0
    for dia in range(-2,4):
        whole_dia = np.dia(board,dia)
        score_for_dia1 +=  check4_of_dia1(whole_dia)
    return score_for_dia1

'''


def check_4_pieces_of_row(row: np.ndarray, player: PlayerAction) -> int:
    """Checks all the subarrays with length 4 in the row and sums their score.

    Args:
        row: A row in the board.
        player: The current player to place a piece.

    Returns:
        int: The score for all the subarrays in the row.
    """
    score = 0
    for i in range(3):
        four_piece = row[i:i + 4].tolist()
        score += count_elements(four_piece, player)
    return score


def check_4_pieces_of_col(col: np.ndarray, player: PlayerAction) -> int:
    """Checks all the subarrays with length 4 in the column and sums their score.

    Args:
        col: A column in the board.
        player: The current player to place a piece.

    Returns:
        int: The score for all subarrays in the column
    """
    score = 0
    for i in range(3):
        four_piece = col[i:i + 4].tolist()
        score += count_elements(four_piece, player)
    return score


def minimax(board: np.ndarray, depth: int, maximizingPlayer: bool) -> Tuple[PlayerAction, int]:
    """Calculates the best move and the best score for a board

    Args:
        board: The current state of the game.
        depth: How many moves in the future you want to see
        maximizingPlayer (bool): True, if it's the maximizing player turn, False otherwise

    Returns:
        Playeraction: The best column to play at for the current board, that the player can chose.
        max_eval: The best score, that the  player can get.
    """

    if depth == 0 or GameState == GameState.IS_WIN:
        if not valid_moves(board):
            print("There are no more free spaces to play. End of game.")
            return None, 0
        else:
            return None, eval_pos(board, PLAYER1)
    else:
        if maximizingPlayer:
            return maxPlayer(board, depth)
        else:
            return minPlayer(board, depth)


def maxPlayer(board: np.ndarray, depth: int):
    """Calculates the best move and the best score for tha maximizing player.

    Args:
        board: The current state of the game.
        depth:

    Returns:
        col: The best column to play at for the current board, that the maximizing player can chose.
        max_eval: The best score, that the maximizing player can get.

    """
    col = 0
    max_eval = -np.inf
    for mov in valid_moves(board):
        board_copy = board.copy()
        board_copy = apply_player_action(board_copy, mov, PLAYER1)
        evaluation = minimax(board_copy, depth - 1, False)[1]
        if evaluation > max_eval:
            max_eval = evaluation
            col = mov
    return col, max_eval


def minPlayer(board: np.ndarray, depth: int):
    """Calculates the best move and the best score for tha minimizing Player.

    Args:
        board: The current state of the game.
        depth:

    Returns:
        col: The best column to play at for the current board that the minimizing player can chose.
        min_eval: The best score, that the minimizing player can get.
    """
    col = 0
    min_eval = np.inf
    for mov in valid_moves(board):
        board_copy = board.copy()
        board_copy = apply_player_action(board_copy, mov, PLAYER2)
        evaluation = minimax(board_copy, depth - 1, True)[1]
        if evaluation < min_eval:
            min_eval = evaluation
            col = mov
    return col, min_eval


def valid_moves(board: np.ndarray) -> list[PlayerAction]:
    """Creates a list of all the valid moves for the board

    Args:
        board: The current state of the game.

    Returns:
        list: The list with all the valid moves.

    """
    all_v_moves = []
    for c in range(7):
        if board[0, c] == NO_PLAYER:
            all_v_moves.append(PlayerAction(c))
    return all_v_moves


def generate_move_minimax(
        board: np.ndarray, player: BoardPiece, saved_state: Optional[SavedState]
) -> Tuple[PlayerAction, Optional[SavedState]]:

    return minimax(board, 4, True)[0], saved_state
