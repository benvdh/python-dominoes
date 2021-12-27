import enum


class GamePlayer(enum.Enum):
    PLAYER = 'player'
    COMPUTER = 'Computer'
    STOCK = 'stock'
    UNKNOWN = None


class GameState(enum.Enum):
    PLAYER_MOVES = "It's your turn to make a move. Enter your command."
    COMPUTER_MOVES = \
        "Computer is about to make a move. Press Enter to continue..."
    PLAYER_WON = "The game is over. You won!"
    COMPUTER_WON = "The game is over. The computer won!"
    DRAW = "The game is over. It's a draw!"
    UNDETERMINED_START = \
        "Cannot determine who is allowed to start, reshuffling dominoes."
