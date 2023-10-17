import numpy as np


class BoardState:
    def __init__(self) -> None:
        ##chang board to 9*9
        self.board = board = ["x"] * 81
        # mill state of every position of board
        self.mill_board_state = [False for _ in range(81)]
