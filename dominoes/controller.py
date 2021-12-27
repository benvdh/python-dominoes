from typing import Union

from Dominoes.task.dominoes.domino_game import DominoGame
from Dominoes.task.dominoes.enums import GameState
from Dominoes.task.dominoes.views import DominoesGameView


class DominoesGameController:
    def __init__(self, game: DominoGame, view: DominoesGameView):
        self.game = game
        self.view = view

    def start_game(self):
        while not self.game.is_game_finished():
            self.show_game_screen()
            move = self.get_move()

            if self.game.get_game_state() == GameState.PLAYER_MOVES:
                self.make_move(move)
            elif move == "" and self.game.get_game_state() == \
                    GameState.COMPUTER_MOVES:

                move = self.game.generate_computer_move()
                self.game.make_move(move)
            else:
                self.show_game_screen()

            self.game.update_game_state()

        self.show_game_screen()

    def make_move(self, move: Union[int, str]) -> None:
        try:
            self.game.make_move(move)
        except ValueError as err:
            print(err.args[0])

            # put piece back on original position
            index = self.game.convert_move_number_to_index(move)
            self.game.add_piece_to_current_player_set(err.args[1], index)

            move = self.get_move()
            self.make_move(move)
        else:
            return None

    def show_game_screen(self):
        game_screen_stats = self.game.get_game_screen_stats()
        snake = self.game.get_snake_as_str_list()
        player_pieces = self.game.get_player_set()
        game_state_message = self.game.get_game_state().value

        self.view.show_game_screen(
            game_screen_stats,
            snake,
            player_pieces,
            game_state_message
        )

    def get_move(self) -> Union[int, str]:
        valid_input_range = self.game.calculate_valid_input_range()

        return self.view.get_player_input(valid_input_range)
