from FOSG import FOSG, State
from utils import CHANCE, NO_ACTION, NO_VALUE
import numpy as np
from itertools import product


class Goofspiel(FOSG):

    def __init__(self, num_cards=3):
        self.num_cards = num_cards

    def get_initial_state(self):
        return GoofspielState(self)


class GoofspielState(State):
    def __init__(self, game: Goofspiel):
        self.num_cards = game.num_cards
        self.p1_cards = [i for i in range(1, game.num_cards + 1)]
        self.p2_cards = [i for i in range(1, game.num_cards + 1)]
        self.chance_cards = [i for i in range(1, game.num_cards + 1)]

        self.chances_order = []
        self.actions_played = [[], []]

        self.winner = []
        self.tie_card = []
        self.points = [0, 0]

        self.terminal = False
        self.value = NO_VALUE
        self.game = game
        self.plays_chance = True

    def get_possible_actions(self):
        if self.terminal:
            return [[], [], []]
        elif self.plays_chance:
            return [[NO_ACTION], [NO_ACTION], self.chance_cards, np.full(len(self.chance_cards), fill_value=1. / len(self.chance_cards), dtype=float)]
        else:
            return [self.p1_cards, self.p2_cards, [NO_ACTION], [1.0]]

    def get_possible_joint_actions(self):
        if self.plays_chance:
            return list(product(*[[NO_ACTION], [NO_ACTION], self.chance_cards]))
        else:
            return list(product(*[self.p1_cards, self.p2_cards, [NO_ACTION]]))

    def can_play(self, player: int):
        if self.plays_chance and player == CHANCE:
            return True
        elif (player == 0 or player == 1) and not self.plays_chance and not self.terminal:
            return True

        return False

    def apply_actions(self, actions):
        assert not self.terminal
        for action, possible_actions in zip(actions, self.get_possible_actions()):
            assert action in possible_actions, f"Invalid action selected {action}. Possible actions {possible_actions}."
        if self.plays_chance:
            self.plays_chance = False

            self.chances_order.append(actions[2])
            self.chance_cards = [i for i in self.chance_cards if i != actions[2]]
        else:
            self.plays_chance = True
            self.actions_played[0].append(actions[0])
            self.actions_played[1].append(actions[1])

            if actions[0] > actions[1]:
                self.points[0] += self.chances_order[-1]
                self.winner.append(1)
                self.tie_card.append(-1)
            elif actions[0] < actions[1]:
                self.points[1] += self.chances_order[-1]
                self.winner.append(-1)
                self.tie_card.append(-1)
            else:
                self.winner.append(0)
                self.tie_card.append(self.chances_order[-1])

            self.p1_cards = [i for i in self.p1_cards if i != actions[0]]
            self.p2_cards = [i for i in self.p2_cards if i != actions[1]]
            if len(self.chance_cards) == 1:
                assert len(self.p1_cards) == 1
                assert len(self.p2_cards) == 1
                assert len(self.actions_played[0]) == self.num_cards - 1
                assert len(self.actions_played[1]) == self.num_cards - 1
                assert len(self.chances_order) == self.num_cards - 1
                assert len(self.winner) == self.num_cards - 1
                assert len(self.tie_card) == self.num_cards - 1
                self.terminal = True
                if self.p1_cards[0] > self.p2_cards[0]:
                    self.points[0] += self.chance_cards[0]
                elif self.p1_cards[0] < self.p2_cards[0]:
                    self.points[1] += self.chance_cards[0]
                if self.points[0] > self.points[1]:
                    self.value = 1
                elif self.points[0] < self.points[1]:
                    self.value = -1
                else:
                    self.value = 0

    def get_private_information(self, player: int):
        return tuple(self.actions_played[player]),

    def get_public_information(self):
        return tuple(self.chance_cards), tuple(self.winner), tuple(self.tie_card), tuple(self.points)

    def get_state_string(self):
        return f"Terminal - Actions: {self.actions_played} Value: " + str(self.value) if self.terminal else "Root"

    def is_terminal(self):
        return self.terminal

    def get_value(self):
        assert self.is_terminal()
        return self.value
