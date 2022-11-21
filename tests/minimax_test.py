import numpy as np
import pytest
from agents.agent_minimax.minimax import *
from agents.game_utils import *


def test_minimax():
    board = np.full((6, 7), NO_PLAYER)
    for i in range(6):
        for j in range(7):
            board[i,j] = random.randint(0,100)
    board[0,:] = NO_PLAYER
    expected_score = 0
    score = minimax(board, 1, True)
    assert score == expected_score


def test_minimax2():
    board = np.full((6, 7), NO_PLAYER)
    expected_score = 0
    score = minimax(board, 2, True)
    assert score == expected_score

def test_best_move():
    board = np.full((6, 7), NO_PLAYER)
    board[5,0] = PLAYER1
    board[5,1] = PLAYER1
    board[5,2] = PLAYER1
    board[5,4] = PLAYER2

    expected_score = 100
    score = pick_best_move(board,PLAYER1)
    assert score == expected_score
def test_best_move2():
    board = np.full((6, 7), NO_PLAYER)
    board[5,0] = PLAYER1
    board[5,1] = PLAYER1
    board[5,2] = PLAYER1
    board[5,4] = PLAYER2

    expected_move = PlayerAction(3)
    score = pick_best_move(board,PLAYER1)
    assert score == expected_move
def test_best_move3():
    board = np.full((6, 7), NO_PLAYER)
    board[5,0] = PLAYER1
    board[5,1] = PLAYER1
    board[5,2] = PLAYER1
    board[5,4] = PLAYER2

    expected_move = PlayerAction(3)
    score = pick_best_move(board,PLAYER1)
    assert score == expected_move

def test_minimax3():
    board = np.full((6, 7), NO_PLAYER)
    expected_score = 0
    score = minimax(board, 2, True)[0]
    assert score == expected_score

def test_minimax4():
    board = np.full((6, 7), NO_PLAYER)
    board[5, 0] = PLAYER1
    board[5, 1] = PLAYER1
    board[5, 2] = PLAYER1
    board[5, 4] = PLAYER2

    expected_move = PlayerAction(3)
    assert minimax(board,4,True)[0] == expected_move