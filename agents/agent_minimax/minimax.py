import random
from typing import Tuple

import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4
from agents.game_utils import *


def count_elements(four_piece):
    player1 = four_piece.count(PLAYER1)
    player2 = four_piece.count(PLAYER2)
    no_player = four_piece.count(NO_PLAYER)

    if player1 == 3 and no_player == 1:
        return 10
    if player1 == 2 and no_player == 2:
        return 5
    if player2 == 3 and no_player == 1:
        return -10
    if player2 == 2 and no_player == 2:
        return -5
    else:
        return 0


def eval_pos(board: np.ndarray, action: PlayerAction):
    score = score_for_rows(board) + score_for_cols(board) + score_for_dias1(board) + score_for_dias2(board)
    return score


def score_for_rows(board: np.ndarray):
    score_for_row = 0
    for rows in range(6):
        whole_row = board[rows, :]
        score_for_row += check4_of_row(whole_row)
    return score_for_row


def score_for_cols(board: np.ndarray):
    score_for_col = 0
    for col in range(7):
        whole_col = board[:, col]
        score_for_col += check4_of_col(whole_col)
    return score_for_col

def score_for_dias1(board: np.ndarray):
    score = 0
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += count_elements(window)
    return score


''''
def score_for_dias1(board: np.ndarray):
    score_for_dia1 = 0
    for dia in range(-2,4):
        whole_dia = np.dia(board,dia)
        score_for_dia1 +=  check4_of_dia1(whole_dia)
    return score_for_dia1


'''

def score_for_dias2(board: np.ndarray):
    score_for_dia2 = 0

    return score_for_dia2

def check4_of_row(row: np.ndarray):
    score = 0
    for i in range(3):
        four_piece = row[i:i + 4].tolist()
        score += count_elements(four_piece)
    return score

def check4_of_col(col: np.ndarray):
    score = 0
    for i in range(2):
        four_piece = col[i:i + 4].tolist()
        score += count_elements(four_piece)
    return score

def check4_of_dia1(dia: np.ndarray):
    score = 0
    for i in range(2):
        four_piece = dia[i:i + 4].tolist()
        score += count_elements(four_piece)
    return score

def minimax(board: np.ndarray, depth: int, maximazingPlayer: bool):
    if depth == 0 or GameState == GameState.IS_WIN:
        if connected_four(board, PLAYER1):
            return 1000000
        if connected_four(board, PLAYER2):
            return -1000000
        if not valid_moves(board):
            return 0
        else:
            return eval_pos(board, PLAYER1)
    else:
        if maximazingPlayer:
            return maxPlayer(board, depth)
        else:
            return minPlayer(board, depth)


def maxPlayer(board: np.ndarray, depth: int):
    max_eval = -np.inf
    for mov in valid_moves(board):
        board_copy = board.copy()
        board_copy = apply_player_action(board_copy, mov, PLAYER1)
        evaluation = minimax(board_copy, depth - 1, False)
        max_eval = max(evaluation, max_eval)
    return max_eval


def minPlayer(board: np.ndarray, depth: int):
    min_eval = np.inf
    for mov in valid_moves(board):
        board_copy = board.copy()
        board_copy = apply_player_action(board_copy, mov, PLAYER1)
        evaluation = minimax(board_copy, depth - 1, True)
        min_eval = min(evaluation, min_eval)
    return min_eval


def valid_moves(board: np.ndarray) -> list[PlayerAction]:
    all_v_moves = []
    for c in range(7):
        if board[0, c] == NO_PLAYER:
            all_v_moves.append(PlayerAction(c))
    return all_v_moves
