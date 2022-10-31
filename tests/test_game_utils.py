import numpy as np
import pytest

from agents.game_utils import *



def test_initialize_game_state():
    ret = initialize_game_state()
    assert isinstance(ret, np.ndarray)
    assert ret.dtype == BoardPiece
    assert ret.shape == (6, 7)
    assert np.all(ret == NO_PLAYER)

#split test

#def test_pretty_print_board():

# def test_string_to_board():

#def test_apply_player_action():
 #   with pytest.raises(ValueError):
  #      for i in range(6) apply_player_action(initialize_game_state(),i,PLAYER1 )

def test_connected_four():
    board = np.array([[BoardPiece(1),BoardPiece(1),BoardPiece(1),BoardPiece(1)]])
    connected_four()
# def test_checke_end_state():