import numpy as np
import pytest
from agents.agent_minimax.minimax import *
from agents.game_utils import *


def test_minimax():
    board = np.full((6, 7), NO_PLAYER)

    expected_score = 0
    score = minimax(board, 1, True)
    assert score == expected_score


def test_minimax2():
    board = np.full((6, 7), NO_PLAYER)
    expected_score = 0
    score = minimax(board, 1, True)
    assert score == expected_score

def evaluation_function(self, state):
    if self.current_move == 1:
        o_color = 2
    elif self.current_move == 2:
        o_color = 1
    my_fours = self.checkForStreak(state, self.current_move, 4)
    my_threes = self.checkForStreak(state, self.current_move, 3)
    my_twos = self.checkForStreak(state, self.current_move, 2)
    comp_fours = self.checkForStreak(state, o_color, 4)
    comp_threes = self.checkForStreak(state, o_color, 3)
    comp_twos = self.checkForStreak(state, o_color, 2)
    return (my_fours * 10 + my_threes * 5 + my_twos * 2) - (comp_fours * 10 + comp_threes * 5 + comp_twos * 2)


def checkForStreak(self, state, color, streak):
    count = 0
    for i in range(6):
        for j in range(7):
            if state[i][j] == color:
                count += self.verticalStreak(i, j, state, streak)
                count += self.horizontalStreak(i, j, state, streak)
                count += self.diagonalCheck(i, j, state, streak)
    return count
