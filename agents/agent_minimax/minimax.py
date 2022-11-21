import random
from typing import Tuple

from agents.game_utils import *
import numpy as np


def pick_best_move(board: np.ndarray, player: PlayerAction) -> PlayerAction:
    """
    Picks the best move for the board at depth == 0
    :param board:
    :param player:
    :return:
    """
    best_score = -10000
    best_col = random.choice(valid_moves(board))
    for col in valid_moves(board):
        temp_board = board.copy()
        temp_board = apply_player_action(temp_board, col, player)
        score = eval_pos(temp_board, player)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col


def count_elements(four_piece: list, player: PlayerAction) -> int:
    """

    :param four_piece:
    :param player:
    :return:
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
    if player2 == 3 and no_player == 1:
        return -100
    if player2 == 2 and no_player == 2:
        return -5

    else:
        return 0


def eval_pos(board: np.ndarray, player: PlayerAction) -> int:
    """
    adds the score for all directions

    :param board:
    :param player:
    :return:
    """
    score = score_for_rows(board, player)
    score += score_for_cols(board, player)
    score += score_for_dias1(board, player)
    score += score_for_dias2(board, player)
    return score


def score_for_rows(board: np.ndarray, player) -> int:
    """
    takes whole rows of the board and calculates the score with the check4_of_row function
    :param board:
    :param player:
    :return:
    """
    score_for_row = 0
    for rows in range(6):
        whole_row = board[rows, :]
        score_for_row += check4_of_row(whole_row, player)
    return score_for_row


def score_for_cols(board: np.ndarray, player: PlayerAction) -> int:
    """
    takes whole columns of the board and calculates the score with the check4_of_col function
    :param board:
    :param player:
    :return:
    """
    score_for_col = 0
    for col in range(7):
        whole_col = board[:, col]
        score_for_col += check4_of_col(whole_col, player)
    return score_for_col


def score_for_dias1(board: np.ndarray, player: PlayerAction) -> int:
    """
     calculates the score for all the diagonals pointing from down left  to right up

    :param board:
    :param player:
    :return:
    """
    score = 0
    for r in range(3):
        for c in range(4):
            window = [board[r + i][c + i] for i in range(4)]
            score += count_elements(window, player)
    return score


def score_for_dias2(board: np.ndarray, player: PlayerAction) -> int:
    """
     calculates the score for all the diagonals pointing from down right to left up

    :param board:
    :param player:
    :return:
    """
    score = 0

    for r in range(3):
        for c in range(4):
            window = [board[r + 3 - i][c + i] for i in range(4)]
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


def check4_of_row(row: np.ndarray, player: PlayerAction) -> int:
    """
    checks all the subarrays with length 4 in each row
    :param row:
    :param player:
    :return:
    """
    score = 0
    for i in range(3):
        four_piece = row[i:i + 4].tolist()
        score += count_elements(four_piece, player)
    return score


def check4_of_col(col: np.ndarray, player: PlayerAction) -> int:
    """
    checks all the subarrays with length 4 in each column
    :param col:
    :param player:
    :return:
    """
    score = 0
    for i in range(3):
        four_piece = col[i:i + 4].tolist()
        score += count_elements(four_piece, player)
    return score


def minimax(board: np.ndarray, depth: int, maximizingPlayer: bool) -> Tuple[PlayerAction, int]:

    if depth == 0 or GameState == GameState.IS_WIN:
        if not valid_moves(board):
            return None, 0
        else:
            return pick_best_move(board, PLAYER1), eval_pos(board, PLAYER1)
    else:
        if maximizingPlayer:
            return maxPlayer(board, depth)
        else:
            return minPlayer(board, depth)


def maxPlayer(board: np.ndarray, depth: int):
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
    """
    creates a list of all the valid moves for the board
    :param board:
    :return:
    """
    all_v_moves = []
    for c in range(7):
        if board[0, c] == NO_PLAYER:
            all_v_moves.append(PlayerAction(c))
    return all_v_moves


class SavedState:
    def __init__(self, computational_result):
        self.computational_result = computational_result


def generate_move_minimax(
        board: np.ndarray, player: BoardPiece, saved_state: Optional[SavedState]
) -> Tuple[PlayerAction, Optional[SavedState]]:
    return minimax(board, 4 ,True)[0], saved_state
