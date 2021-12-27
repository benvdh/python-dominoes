from typing import Union, List

from Dominoes.task.dominoes.domino_game import GameScreenStatistics
import re

from Dominoes.task.dominoes.domino_set import DominoSet


class DominoesGameView:
    SEPARATOR = "=" * 70
    STOCK_SIZE_FIELD = "Stock size"
    COMPUTER_PIECES_FIELD = "Computer pieces"
    STATUS_FIELD = "Status"
    PLAYER_PIECES_HEADER = "Your pieces"
    INPUT_ERROR_MESSAGE = "Invalid input. Please try again."
    IS_INT_STRING = re.compile(r'^-?[1-9]*[0-9]+$')

    def show_separator(self):
        print(self.SEPARATOR)

    @classmethod
    def show_stock_size(cls, stock_size: int):
        print(f"{cls.STOCK_SIZE_FIELD}: {stock_size}")

    @classmethod
    def show_computer_set_size(cls, computer_set_size: int):
        print(
            f"{cls.COMPUTER_PIECES_FIELD}: "
            f"{computer_set_size}"
        )

    @staticmethod
    def show_snake(snake: List[str]):
        if len(snake) < 7:
            snake_as_str = "".join(snake)
        else:
            snake_as_str = f'{"".join(snake[0:3])}...{"".join(snake[-3:])}'
        print(snake_as_str)

    @classmethod
    def show_player_pieces(cls, player_set: DominoSet):
        print(f"{cls.PLAYER_PIECES_HEADER}:")

        for option_number, piece in enumerate(player_set, 1):
            print(f"{option_number}:{piece}")

    @classmethod
    def show_game_status(cls, game_status_message: str):
        print(f"{cls.STATUS_FIELD}: {game_status_message}")

    def show_game_screen(
        self,
        game_screen_stats: GameScreenStatistics,
        snake: List[str],
        player_pieces: DominoSet,
        game_status_message: str
    ):
        self.show_separator()
        self.show_stock_size(game_screen_stats.stock_size)
        self.show_computer_set_size(game_screen_stats.computer_set_size)

        print("")

        self.show_snake(snake)

        print("")

        self.show_player_pieces(player_pieces)

        print("")

        self.show_game_status(game_status_message)

    @classmethod
    def _try_str_to_int(cls, input_str: str) -> Union[str, int]:
        if cls.IS_INT_STRING.match(input_str):
            return int(input_str)

        return input_str

    def get_player_input(self, valid_range: List[int]) -> Union[int, str]:
        player_input = input()
        parsed_input = self._try_str_to_int(player_input)

        if player_input == "":
            return player_input

        while parsed_input not in valid_range:
            print(self.INPUT_ERROR_MESSAGE)
            player_input = input()
            parsed_input = self._try_str_to_int(player_input)

        return parsed_input
