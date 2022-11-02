import numpy as np
import pytest

from agents.game_utils import *


def test_initialize_game_state():
    ret = initialize_game_state()
    assert isinstance(ret, np.ndarray)
    assert ret.dtype == BoardPiece
    assert ret.shape == (6, 7)
    assert np.all(ret == NO_PLAYER)


# split test

def test_pretty_print_board_forboardplayer1():
    board = np.full((6, 7), NO_PLAYER)
    board[0, 0] = PLAYER1
    assert PLAYER1_PRINT in pretty_print_board(board)


def test_pretty_print_board_forboardplayer2():
    board = np.full((6, 7), NO_PLAYER)
    board[0, 0] = PLAYER2
    assert PLAYER2_PRINT in pretty_print_board(board)


def test_pretty_print_board_forboardplayer3():
    board = np.full((6, 7), PLAYER1)
    board[0, 0] = NO_PLAYER
    assert NO_PLAYER_PRINT in pretty_print_board(board)


def test_pretty_print_board_forboardplayer4():
    board = np.full((6, 7), NO_PLAYER)
    board[0, :] = PLAYER2
    assert "O O O O O O O" in pretty_print_board(board)


# def test_string_to_board():

def test_apply_player_action():
    board = np.full((6, 7), 0)
    apply_player_action(board, PlayerAction(1), PLAYER1)
    assert board[5, 1] == PLAYER1


def test_apply_player_action2():
    with pytest.raises(ValueError):
        board = np.full((6, 7), 0)
        board[:,0] = PLAYER2
        print(board)
        apply_player_action(board, PlayerAction(0), PLAYER1)

def test_apply_player_action3():
    with pytest.raises(ValueError):
        board = np.full((6, 7), NO_PLAYER)
        apply_player_action(board,PlayerAction(7),PLAYER1)


def test_connected_four():
    board = np.full((6, 7), NO_PLAYER)
    assert connected_four(board, PLAYER1) == False


def test_connectd_four():
    board = np.full((6, 7), NO_PLAYER)
    board[1, 2] = PLAYER1
    board[1, 3] = PLAYER1
    board[1, 4] = PLAYER1
    board[1, 5] = PLAYER1
    assert connected_four(board, 1) == True
# def test_checke_end_state():
