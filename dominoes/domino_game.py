import random
import itertools
from typing import List, Tuple, Dict, Union, Optional
from collections import Counter

from Dominoes.task.dominoes.domino_set import DominoSet, DominoSnake
from Dominoes.task.dominoes.enums import GamePlayer, GameState

MOVE_CANDIDATES = List[
    Dict[str, Union[List[int], int]]
]


class GameScreenStatistics:
    def __init__(
        self,
        player_set_size: int,
        computer_set_size: int,
        stock_size: int
    ):
        self.player_set_size = player_set_size
        self.computer_set_size = computer_set_size
        self.stock_size = stock_size


class DominoGame:
    def __init__(self):
        self._stock_set = DominoSet.get_full_set()
        self._player_set = self._stock_set.extract_player_set(
            GamePlayer.PLAYER
        )
        self._computer_set = self._stock_set.extract_player_set(
            GamePlayer.COMPUTER
        )
        self._state, max_double = self._determine_initial_game_state()

        if self._state == GameState.UNDETERMINED_START:
            self.__init__()

        self._current_player = self._get_current_player_by_game_state()
        self._next_player = self._get_next_player_by_game_state()

        self._snake = DominoSnake([max_double])

        self._remove_max_double_from_set(max_double)

    def _remove_max_double_from_set(self, max_double):
        if self._next_player == GamePlayer.PLAYER:
            self._remove_piece_from_domino_set(self._player_set, max_double)
        else:
            self._remove_piece_from_domino_set(self._computer_set, max_double)

    def _determine_initial_game_state(self) -> Tuple[
        GameState,
        Optional[
            List[int]
        ]
    ]:
        player_max_double, computer_max_double = \
            self._get_max_doubles()
        has_none_values = \
            computer_max_double is None or player_max_double is None

        if has_none_values:
            return self._determine_game_state_with_lacking_doubles()
        elif computer_max_double > player_max_double:
            return GameState.PLAYER_MOVES, computer_max_double
        elif player_max_double > computer_max_double:
            return GameState.COMPUTER_MOVES, player_max_double
        else:
            return GameState.UNDETERMINED_START, None

    def _determine_game_state_with_lacking_doubles(self):
        player_max_double, computer_max_double = \
            self._get_max_doubles()

        if player_max_double is None and computer_max_double is None:
            return GameState.UNDETERMINED_START, None
        elif player_max_double is None and computer_max_double:
            return GameState.PLAYER_MOVES, computer_max_double
        elif computer_max_double is None and player_max_double:
            return GameState.COMPUTER_MOVES, player_max_double
        else:
            return GameState.UNDETERMINED_START, None

    def _get_max_doubles(self):
        return self._player_set.get_max_double(), \
               self._computer_set.get_max_double()

    def _get_next_player_by_game_state(self) -> GamePlayer:
        if self._state == GameState.PLAYER_MOVES:
            return GamePlayer.COMPUTER
        elif self._state == GameState.COMPUTER_MOVES:
            return GamePlayer.PLAYER
        else:
            return GamePlayer.UNKNOWN

    def _get_current_player_by_game_state(self):
        if self._state == GameState.PLAYER_MOVES:
            return GamePlayer.PLAYER
        elif self._state == GameState.COMPUTER_MOVES:
            return GamePlayer.COMPUTER
        else:
            return GamePlayer.UNKNOWN

    def get_stock_size(self) -> int:
        return len(self._stock_set)

    def get_computer_set_size(self) -> int:
        return len(self._computer_set)

    def get_player_set(self) -> DominoSet:
        return self._player_set

    def get_player_set_size(self):
        return len(self._player_set)

    def get_game_state(self):
        return self._state

    def get_snake_as_str_list(self) -> List[str]:
        return self._snake.get_snake_as_str_list()

    def get_game_screen_stats(self) -> GameScreenStatistics:
        return GameScreenStatistics(
            self.get_player_set_size(),
            self.get_computer_set_size(),
            self.get_stock_size()
        )

    def get_current_player_set(self) -> DominoSet:
        if self._current_player == GamePlayer.PLAYER:
            return self._player_set
        else:
            return self._computer_set

    def is_game_finished(self) -> bool:
        return self._state in [
            GameState.DRAW,
            GameState.COMPUTER_WON,
            GameState.PLAYER_WON
        ]

    def has_player_won(self) -> bool:
        return len(self._player_set) == 0

    def has_computer_won(self) -> bool:
        return len(self._computer_set) == 0

    def has_draw_condition_been_reached(self) -> bool:
        return self._snake.is_in_draw_condition()

    def _switch_player_state(self) -> None:
        if self._state == GameState.PLAYER_MOVES:
            self._state = GameState.COMPUTER_MOVES
        else:
            self._state = GameState.PLAYER_MOVES

        self._current_player = self._get_current_player_by_game_state()
        self._next_player = self._get_next_player_by_game_state()

    def update_game_state(self) -> None:
        player_wins = self.has_player_won()
        computer_wins = self.has_computer_won()
        is_draw = self.has_draw_condition_been_reached()

        if player_wins:
            self._state = GameState.PLAYER_WON
        elif computer_wins:
            self._state = GameState.COMPUTER_WON
        elif is_draw:
            self._state = GameState.DRAW
        else:
            self._switch_player_state()

    def calculate_valid_input_range(
        self,
    ) -> List[int]:
        current_player_set = self.get_current_player_set()
        set_size = len(current_player_set)

        return list(range(set_size * -1, set_size + 1))

    def get_stock_piece(self) -> List[int]:
        return self._stock_set.pop_random_piece()

    def _calculate_domino_number_counts(self):
        combined_computer_stack_iterator = itertools.chain(
            *self._computer_set,
            *self._snake
        )
        return Counter(combined_computer_stack_iterator)

    def _calculate_computer_move_scores(self):
        number_counts = self._calculate_domino_number_counts()
        scores = dict()

        for piece in self._computer_set:
            score = number_counts[piece[0]] + number_counts[piece[1]]
            scores[tuple(piece)] = score

        return scores

    @staticmethod
    def _sort_computer_move_candidates(move_candidates: MOVE_CANDIDATES):
        return list(
            sorted(
                move_candidates,
                key=lambda candidate: candidate["score"],
                reverse=True
            )
        )

    def generate_computer_move(self) -> int:
        left_edge_number = self._snake.get_left_edge_number()
        right_edge_number = self._snake.get_right_edge_number()
        piece_scores = self._calculate_computer_move_scores()
        move_candidates = []

        for index, (piece, score) in enumerate(piece_scores.items(), 1):
            move_candidate = {
                "piece": piece,
                "score": score
            }

            if left_edge_number in piece:
                move_candidate["move_number"] = -1 * index
                move_candidates.append(move_candidate)
            elif right_edge_number in piece:
                move_candidate["move_number"] = index
                move_candidates.append(move_candidate)

        if len(move_candidates) == 0:
            return 0
        else:
            sorted_computer_move_candidates = \
                self._sort_computer_move_candidates(move_candidates)

            return sorted_computer_move_candidates[0]["move_number"]

    def get_random_move(self) -> int:
        move_range = self.calculate_valid_input_range()
        return random.choice(move_range)

    @staticmethod
    def convert_move_number_to_index(move_number: int) -> int:
        return abs(move_number) - 1

    def make_move(self, move_number: int) -> None:
        player_set = self.get_current_player_set()
        stock_size = self.get_stock_size()

        if move_number == 0 and stock_size > 0:
            stock_piece = self.get_stock_piece()
            player_set.add_piece(stock_piece)
        elif move_number == 0 and stock_size == 0:
            return None
        elif move_number < 0:
            piece_index = self.convert_move_number_to_index(move_number)
            domino_piece = player_set.pop_piece(piece_index)
            self._snake.add_to_left(domino_piece)
        else:
            piece_index = self.convert_move_number_to_index(move_number)
            domino_piece = player_set.pop_piece(piece_index)
            self._snake.add_to_right(domino_piece)

    def add_piece_to_current_player_set(
        self,
        domino_piece: List[int],
        index: int
    ) -> None:
        player_set = self.get_current_player_set()
        player_set.add_piece_at_index(domino_piece, index)

    @staticmethod
    def _remove_piece_from_domino_set(
        domino_set: DominoSet,
        piece: List[int]
    ):
        domino_set.remove_piece(piece)
