import random

from typing import List
from collections import deque
import itertools

from Dominoes.task.dominoes.enums import GamePlayer


class DominoSet:
    PLAYER_SET_SIZE = 7

    @classmethod
    def get_full_set(cls) -> 'DominoSet':
        dominoes_set = []

        for i in range(0, 7):
            for j in range(0, 7):
                if not sorted([i, j]) in dominoes_set:
                    dominoes_set.append([i, j])

        return cls(dominoes_set, GamePlayer.STOCK)

    def __init__(self, dominoes: List[List[int]], player: GamePlayer):
        self.set = dominoes
        self.player = player

    def __iter__(self):
        return self.set.__iter__()

    def __len__(self):
        return self.set.__len__()

    def extract_player_set(self, set_owner: GamePlayer) -> 'DominoSet':
        player_set = DominoSet(random.sample(self.set, k=7), set_owner)
        self.remove_pieces(player_set.get_set())
        return player_set

    def remove_pieces(self, to_remove: List[List[int]]) -> None:
        for element in to_remove:
            self.set.remove(element)

    def remove_piece(self, to_remove: List[int]) -> None:
        self.set.remove(to_remove)

    def pop_random_piece(self) -> List[int]:
        random_index = random.randint(0, len(self.set) - 1)
        return self.set.pop(random_index)

    def pop_piece(self, piece_index: int) -> List[int]:
        return self.set.pop(piece_index)

    def add_piece(self, piece: List[int]) -> None:
        self.set.append(piece)

    def add_piece_at_index(self, piece: List[int], index: int):
        self.set.insert(index, piece)

    def get_max_double(self):
        return max(
            list(
                filter(self._is_double_domino, self.set)
            ),
            default=None
        )

    @staticmethod
    def _is_double_domino(domino: List[int]):
        return domino[0] == domino[1]

    def get_set(self) -> List[List[int]]:
        return self.set

    def get_player(self):
        return self.player


class DominoSnake:
    _LEFT_POSITION = "left"
    _RIGHT_POSITION = "right"
    ILLEGAL_MOVE_ERROR = "Illegal move. Please try again."

    def __init__(self, snake: List[List[int]]):
        self._snake = deque(snake)

    def __iter__(self):
        return self._snake.__iter__()

    def head(self) -> List[int]:
        return self._snake[0]

    def tail(self) -> List[int]:
        return self._snake[-1]

    def get_left_edge_number(self) -> int:
        return self.head()[0]

    def get_right_edge_number(self) -> int:
        return self.tail()[1]

    def is_valid_move(self, position: str, domino_piece: List[int]) -> bool:
        if position == self._LEFT_POSITION:
            snake_edge_number = self.get_left_edge_number()
        else:
            snake_edge_number = self.get_right_edge_number()

        return snake_edge_number in domino_piece

    def orient_left(
        self,
        domino_piece: List[int]
    ) -> List[int]:
        edge_number = self.get_left_edge_number()

        if edge_number != domino_piece[1]:
            return sorted(domino_piece, reverse=True)
        else:
            return domino_piece

    def add_to_left(self, domino_piece: List[int]) -> None:
        if self.is_valid_move(self._LEFT_POSITION, domino_piece):
            oriented_piece = self.orient_left(domino_piece)
            self._snake.appendleft(oriented_piece)
        else:
            raise ValueError(self.ILLEGAL_MOVE_ERROR, domino_piece)

    def orient_right(
        self,
        domino_piece
    ) -> List[int]:
        edge_number = self.get_right_edge_number()

        if edge_number != domino_piece[0]:
            return sorted(domino_piece, reverse=True)
        else:
            return domino_piece

    def add_to_right(self, domino_piece: List[int]):
        if self.is_valid_move(self._RIGHT_POSITION, domino_piece):
            oriented_piece = self.orient_right(domino_piece)
            self._snake.append(oriented_piece)
        else:
            raise ValueError(self.ILLEGAL_MOVE_ERROR, domino_piece)

    def get_snake_as_str_list(self) -> List[str]:
        return [str(domino) for domino in self._snake]

    def is_in_draw_condition(self):
        start_piece = self.head()
        end_piece = self.tail()
        start_end_are_equal = start_piece[0] == end_piece[1]

        last_snake_value = end_piece[1]

        last_snake_value_count = list(itertools.chain(*self._snake))\
            .count(last_snake_value)

        return start_end_are_equal and last_snake_value_count == 8
