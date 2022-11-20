import numpy as np
import pytest

from agents.game_utils import *


# Test for func initialize_game_state()
def test_initialize_game_state():
    ret = initialize_game_state()
    assert isinstance(ret, np.ndarray)


def test_initialize_game_state2():
    ret = initialize_game_state()
    assert ret.dtype == BoardPiece


def test_initialize_game_state3():
    ret = initialize_game_state()
    assert ret.shape == (6, 7)


def test_initialize_game_state4():
    ret = initialize_game_state()
    assert np.all(ret == NO_PLAYER)


# Test for func initialize_game_state()

def test_pretty_print_board_for_player1():
    board = np.full((6, 7), NO_PLAYER)
    board[0, 0] = PLAYER1
    assert PLAYER1_PRINT in pretty_print_board(board)


def test_pretty_print_board_for_player2():
    board = np.full((6, 7), NO_PLAYER)
    board[5, 0] = PLAYER2
    print(board)
    print(pretty_print_board(board))
    assert PLAYER2_PRINT in pretty_print_board(board)


def test_pretty_print_board_for_noplayer():
    board = np.full((6, 7), PLAYER1)
    board[0, 0] = NO_PLAYER
    newboard = np.flipud(board)
    print(board)
    print(newboard)
    print(pretty_print_board(board))
    assert NO_PLAYER_PRINT in pretty_print_board(board)


def test_pretty_print_board_for_row_player2():
    board = np.full((6, 7), NO_PLAYER)
    board[5, :] = PLAYER2
    print(pretty_print_board(board))

    assert "O O O O O O O" in pretty_print_board(board)


def test_pretty_print_board_for_row_player1():
    board = np.full((6, 7), NO_PLAYER)
    board[5, :] = PLAYER1
    print(pretty_print_board(board))

    assert "X X X X X X X" in pretty_print_board(board)


def test_pretty_print_board_for_col_player1():
    board = np.full((6, 7), NO_PLAYER)
    board[:, 0] = PLAYER1
    print(pretty_print_board(board))

    assert "O O O O O O O" in pretty_print_board(board)


def test_pretty_print_board_for_col_player2():
    board = np.full((6, 7), NO_PLAYER)
    board[:, 2] = PLAYER1
    print(pretty_print_board(board))

    assert "X X X X X X X" in pretty_print_board(board)


# Test for func initialize_game_state()

def test_string_to_board():
    board = np.full((6, 7), NO_PLAYER)
    board[:4:2] = PLAYER2
    print(board)

    pp_str = pretty_print_board(board)
    print(string_to_board(pp_str))


# Test for func apply_player_action()

def test_apply_player_action():
    board = np.full((6, 7), NO_PLAYER)
    new_board = apply_player_action(board, PlayerAction(1), PLAYER1)

    assert new_board[5, 1] == PLAYER1

    # testing to see that when the column is full you get a ValueError


def test_apply_player_action22():
    with pytest.raises(ValueError):
        board = np.full((6, 7), NO_PLAYER)
        board[:, 1] = PLAYER1
        apply_player_action(board, PlayerAction(1), PLAYER1)


def test_apply_player_action2():
    with pytest.raises(ValueError):
        board = np.full((6, 7), NO_PLAYER)
        board[:, 0] = PLAYER2

        apply_player_action(board, PlayerAction(0), PLAYER1)


def test_apply_player_action3():
    with pytest.raises(ValueError):
        board = np.full((6, 7), NO_PLAYER)
        apply_player_action(board, PlayerAction(7), PLAYER1)


# Test for func lowest_row()


# Test for func connected_four()

def test_connected_four():
    board = np.full((6, 7), NO_PLAYER)
    assert connected_four(board, PLAYER1) == False


def test_connected_four0():
    board = np.full((6, 7), NO_PLAYER)
    board[1, 2] = PLAYER1
    board[1, 3] = PLAYER1
    board[1, 4] = PLAYER1
    board[1, 5] = PLAYER1
    assert connected_four(board, PLAYER1) == True


def test_connected_four1():
    board = np.full((6, 7), NO_PLAYER)
    board[1, 2] = PLAYER2
    board[1, 3] = PLAYER2
    board[1, 4] = PLAYER2

    assert connected_four(board, PLAYER2) == False


# checking horinzotal win for player2
def test_connected_four2():
    board = np.full((6, 7), NO_PLAYER)
    for i in range(4):
        board[i, i] = PLAYER2

    assert connected_four(board, PLAYER2) == True


def test_connected_four3():
    board = np.full((6, 7), NO_PLAYER)
    for i in range(4):
        board[i, i] = PLAYER1
    flipped_board = np.fliplr(board)

    assert connected_four(flipped_board, PLAYER1) == True

    # Test for func check_end_state()


def test_check_end_state():
    board = np.full((6, 7), NO_PLAYER)
    assert check_end_state(board, PLAYER1) == GameState.STILL_PLAYING


def test_check_end_state2():
    board = np.full((6, 7), NO_PLAYER)
    for i in range(4):
        board[i, i] = PLAYER1
    assert check_end_state(board, PLAYER1) == GameState.IS_WIN


def test_check():
    board = np.full((6, 7), PLAYER1)
    assert GameState.IS_DRAW == check_end_state(board, PLAYER2)
