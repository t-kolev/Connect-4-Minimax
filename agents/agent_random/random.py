from typing import Tuple

from agents.game_utils import *



class SavedState:
    def __init__(self, computational_result):
        self.computational_result = computational_result

def generate_move_random(
    board: np.ndarray, player: BoardPiece, saved_state: Optional[SavedState]
) -> Tuple[PlayerAction, Optional[SavedState]]:
    # Choose a valid, non-full column randomly and return it as `action`
    return action, saved_state

