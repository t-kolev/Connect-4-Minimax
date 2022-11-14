import random
from typing import Tuple

import numpy as np

from agents.game_utils import *


def eval_pos(board: np.ndarray, player: BoardPiece):
    pass


def minimax(board: np.ndarray, depth: int, maximazingPlayer: bool):
    global col
    if depth == 0 or GameState == GameState.IS_WIN:
        if connected_four(board, PLAYER1):
            return 10000
        if connected_four(board, PLAYER2):
            return -10000
        if not valid_moves(board):
            return 0
        else:
            return eval_pos(board, PLAYER1)

    else:
        if maximazingPlayer:
            maxEval = -np.inf
            for mov in valid_moves(board):
                c_board = board.copy()
                apply_player_action(c_board, mov, PLAYER1)
                evaluation = minimax(c_board, depth - 1, False)[1]
                #maxEval = max(evaluation, maxEval)
                if maxEval > evaluation:
                    maxEval = evaluation
                    col = mov
            return col, maxEval
        else:
            minEval = np.inf
            for mov in valid_moves(board):
                c_board = board.copy()
                apply_player_action(c_board, mov, PLAYER2)
                evaluation = minimax(c_board, depth - 1, True)[1]
                #minEval = min(evaluation, minEval)
                if minEval < evaluation:
                    minEval = evaluation
                    col = mov
            return col, minEval


def valid_moves(board: np.ndarray):
    all_v_moves = []
    for c in range(6):
        if board[0, c] == NO_PLAYER:
            all_v_moves.append(PlayerAction(c))
    return all_v_moves

def generate_move_minimax(
        board: np.ndarray, player: BoardPiece, saved_state: Optional[SavedState]
) -> Tuple[PlayerAction, Optional[SavedState]]:
    new_board = board.copy()
    apply_player_action(new_board, minimax(board, 4, True)[0], player)

    return minimax(board, 4, True)[0], saved_state