from Dominoes.task.dominoes.controller import DominoesGameController
from Dominoes.task.dominoes.domino_game import DominoGame
from Dominoes.task.dominoes.views import DominoesGameView

game = DominoGame()
view = DominoesGameView()
controller = DominoesGameController(game, view)

controller.start_game()
