import random
from typing import Tuple

from agents.game_utils import *


class SavedState:
    def __init__(self, computational_result):
        self.computational_result = computational_result


def generate_move_random(
        board: np.ndarray, player: BoardPiece, saved_state: Optional[SavedState]
) -> Tuple[PlayerAction, Optional[SavedState]]:
    # Choose a valid, non-full column randomly and return it as `action`
    while True:
        random_col = PlayerAction(random.randint(0, 6))
        try:
            apply_player_action(board, random_col, player)
            break
        except:
            ValueError("The column is full")

    return PlayerAction(random_col), saved_state
