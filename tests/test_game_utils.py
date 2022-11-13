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
    print(pretty_print_board(board))

    assert "O O O O O O O" in pretty_print_board(board)


def test_string_to_board():
    board = np.full((6, 7), NO_PLAYER)
    board[:4 :2] = PLAYER2
    print(board)

    pp_str = pretty_print_board(board)
    print(string_to_board(pp_str))

def test_apply_player_action():
    board = np.full((6, 7), 0)
    apply_player_action(board, PlayerAction(1), PLAYER1)
    apply_player_action(board, PlayerAction(1), PLAYER1)
    apply_player_action(board, PlayerAction(1), PLAYER2)

    print(board)
    print(pretty_print_board(board))
    assert board[5, 1] == PLAYER1

    #testing to see that when the collumn is full you get a ValueError
def test_apply_player_action22():
    with pytest.raises(ValueError):
        board = np.full((6, 7), 0)
        board[5,1] = PLAYER1
        board[4,1] = PLAYER1
        board[3,1] = PLAYER1
        board[2,1] = PLAYER1
        apply_player_action(board, PlayerAction(1), PLAYER1)
        apply_player_action(board, PlayerAction(1), PLAYER1)
        apply_player_action(board, PlayerAction(1), PLAYER1)



def test_apply_player_action2():
    with pytest.raises(ValueError):
        board = np.full((6, 7), NO_PLAYER)
        board[:, 0] = PLAYER2
        print(board)
        apply_player_action(board, PlayerAction(0), PLAYER1)


def test_apply_player_action3():
    with pytest.raises(ValueError):
        board = np.full((6, 7), NO_PLAYER)
        apply_player_action(board, PlayerAction(7), PLAYER1)



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


def test_connectd_four2():
    board = np.full((6, 7), NO_PLAYER)
    board[1, 2] = PLAYER2
    board[1, 3] = PLAYER2
    board[1, 4] = PLAYER2

    assert connected_four(board, PLAYER2) == False


# checking horinzotal win for player2
def test_connectd_four3():
    board = np.full((6, 7), NO_PLAYER)
    for i in range(4):
        apply_player_action(board,i,PLAYER2)
    print(board)
    assert connected_four(board, PLAYER2) == True


def test_check_end_state():
    board = np.full((6, 7), NO_PLAYER)
    assert check_end_state(board, PLAYER1) == GameState.STILL_PLAYING


def test_check_end_state2():
    board = np.full((6, 7), NO_PLAYER)
    for i in range(4):
        apply_player_action(board,i,PLAYER2)
    print(board)
    assert check_end_state(board, PLAYER1) == GameState.IS_WIN

def test_check_end_state11():
    board = np.full((6, 7), NO_PLAYER)

    print(board)
    assert check_end_state(board, PLAYER1) == GameState.IS_DRAW
def test_check_end_state11():
    board = np.full((6, 7), NO_PLAYER)
    for i in range(4):
        apply_player_action(board, i, PLAYER2)
    ppprint = pretty_print_board(board)
    string_to_board(ppprint)
    assert True
def test_check():
    board = np.full((6, 7), PLAYER1)
    assert GameState.IS_DRAW == check_end_state(board, PLAYER2)

