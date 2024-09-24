from FOSG import FOSG, State
from utils import CHANCE, NO_ACTION, NO_VALUE
import numpy as np
from itertools import product


class Battleships(FOSG):

    def __init__(self, x_size, y_size, ship_size):
        self.x_size = x_size
        self.y_size = y_size
        self.ship_size = ship_size

    def get_initial_state(self):
        return BattleshipsState(self)


class BattleshipsState(State):
    def __init__(self, game: Battleships):
        self.x_size = game.x_size
        self.y_size = game.y_size
        self.ship_size = game.ship_size
        self.ships_placed = [False, False]

        self.ships_cells = [
            set(),
            set()
        ]

        self.shooting_history = []

        self.possible_shots = [
            np.arange(self.x_size * self.y_size),
            np.arange(self.x_size * self.y_size)
        ]

        self.terminal = False
        self.value = NO_VALUE
        self.game = game
        self.current_player = 0

    def get_possible_actions(self):
        if self.terminal:
            return [[], [], []]
        else:
            if self.ships_placed[self.current_player]:
                actions = [[NO_ACTION], [NO_ACTION], [NO_ACTION], [1.0]]
                actions[self.current_player] = self.possible_shots[self.current_player]
                return actions
            else:
                if self.ship_size == 1:
                    actions = [[NO_ACTION], [NO_ACTION], [NO_ACTION], [1.0]]
                    actions[self.current_player] = self.possible_shots[self.current_player]
                    return actions
                elif self.ship_size == 2:
                    actions = [[NO_ACTION], [NO_ACTION], [NO_ACTION], [1.0]]
                    actions[self.current_player] = np.arange(self.x_size * (self.y_size - 1) + (self.x_size - 1) * self.y_size)
                    return actions
                else:
                    raise "Unexpected ship size"

    def get_possible_joint_actions(self):
        actions = self.get_possible_actions()
        joint_actions = []
        for first_player_action in actions[0]:
            for second_player_action in actions[1]:
                for chance_player_action in actions[2]:
                    joint_actions.append([first_player_action, second_player_action, chance_player_action])
        return joint_actions

    def can_play(self, player: int):
        return self.current_player == player

    def apply_actions(self, actions):
        assert not self.terminal
        for action, possible_actions in zip(actions, self.get_possible_actions()):
            assert action in possible_actions, f"Invalid action selected {action}. Possible actions {possible_actions}."
        action = actions[self.current_player]
        opponent = 1 - self.current_player
        if self.ships_placed[self.current_player]:
            self.shooting_history.append(action)
            self.possible_shots[self.current_player] = np.delete(self.possible_shots[self.current_player], np.where(self.possible_shots[self.current_player] == action))
            if action in self.ships_cells[opponent]:
                self.shooting_history.append(-1)
                self.ships_cells[opponent].remove(action)
                if not self.ships_cells[opponent]:
                    self.terminal = True
                    self.value = 1 if self.current_player == 0 else -1
                    self.current_player = -1
                else:
                    self.current_player = opponent
            else:
                self.current_player = opponent

        else:
            if self.ship_size == 1:
                self.ships_cells[self.current_player].add(action)
            elif self.ship_size == 2:
                if action < self.x_size * (self.y_size - 1):
                    self.ships_cells[self.current_player].add(action)
                    self.ships_cells[self.current_player].add(action + self.x_size)
                else:
                    transformed_action = action - self.x_size * (self.y_size - 1)
                    col = int(transformed_action/self.y_size)
                    row = transformed_action % self.y_size
                    real_action = row * self.x_size + col
                    self.ships_cells[self.current_player].add(real_action)
                    self.ships_cells[self.current_player].add(real_action + 1)
            else:
                raise "Wrong ship size"
            self.ships_placed[self.current_player] = True
            self.current_player = opponent

    def get_private_information(self, player: int):
        return tuple(self.ships_cells[player]),

    def get_public_information(self):
        ret = ()
        if self.terminal:
            ret += tuple("T")
        return tuple(self.ships_placed) + tuple(self.shooting_history) + ret

    def get_state_string(self):
        return "Battleships state - " + (f"Terminal - Actions: {self.shooting_history} Value: " + str(
            self.value) if self.terminal else f"Player: {self.current_player} Ships: {[sorted(self.ships_cells[0]), sorted(self.ships_cells[1])]} Actions: {self.shooting_history}")

    def is_terminal(self):
        return self.terminal

    def get_value(self):
        assert self.is_terminal()
        return self.value
