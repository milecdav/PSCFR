from FOSG import FOSG, State
import numpy as np
from utils import opponent, NO_ACTION, NO_VALUE

EMPTY = 0
PLAYER_PRESENT = [1, -1]


class TickTacToe(FOSG):

    def __init__(self, board_size=3):
        self.board_size = board_size

    def get_initial_state(self):
        return TickTacToeState(board_size=self.board_size)


class TickTacToeState(State):
    def __init__(self, board_size):
        self.board = np.zeros((board_size, board_size))
        self.active_player = 0
        self.action_history = []
        self.winner = -1
        self.terminal = False
        self.value = NO_VALUE

    def get_possible_actions(self):
        if self.terminal:
            return [[], [], []]
        else:
            actions = [[], [], [NO_ACTION], [1]]
            actions[opponent(self.active_player)].append(NO_ACTION)
            actions[self.active_player] = list(np.where(self.board.reshape(-1) == EMPTY)[0])
            return actions

    def get_possible_joint_actions(self):
        actions = self.get_possible_actions()
        joint_actions = []
        for first_player_action in actions[0]:
            for second_player_action in actions[1]:
                for chance_player_action in actions[2]:
                    joint_actions.append([first_player_action, second_player_action, chance_player_action])
        return joint_actions

    def can_play(self, player: int):
        if self.terminal:
            return False
        return player == self.active_player

    def player_won(self):
        for i in range(len(self.board)):
            if np.all(self.board[i] == self.board[i][0]) and self.board[i][0] != EMPTY:
                return True
            if np.all(self.board[:, i] == self.board[0][i]) and self.board[0][i] != EMPTY:
                return True
            diagonal = np.diag(self.board)
            if np.all(diagonal == diagonal[0]) and diagonal[0] != EMPTY:
                return True
            other_diagonal = np.diag(np.fliplr(self.board))
            if np.all(other_diagonal == other_diagonal[0]) and other_diagonal[0] != EMPTY:
                return True
        return False

    def apply_actions(self, actions):
        assert not self.terminal
        for action, possible_actions in zip(actions, self.get_possible_actions()):
            assert action in possible_actions, f"Invalid action selected {action}. Possible actions {possible_actions}."
        self.board.reshape(-1)[actions[self.active_player]] = PLAYER_PRESENT[self.active_player]
        self.action_history.append(actions[self.active_player])
        if self.player_won():
            self.terminal = True
            self.winner = self.active_player
            self.value = (1 if self.winner == 0 else -1)
        if np.all(self.board):
            self.terminal = True
            self.value = 0
        self.active_player = opponent(self.active_player)

    def get_private_information(self, player: int):
        return ()

    def get_public_information(self):
        return self.winner, tuple(map(tuple, self.board)), tuple(self.action_history)

    def get_state_string(self):
        return f"Tick Tack Toe state - Board: {[str(row) for row in self.board]}" + (" Value: " + str(self.value) if self.is_terminal() else f" Active player: {self.active_player}")

    def is_terminal(self):
        return self.terminal

    def get_value(self):
        assert self.is_terminal()
        return self.value

    def __str__(self):
        return self.get_state_string()
