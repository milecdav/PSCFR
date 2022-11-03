from FOSG import FOSG, State
import numpy as np
from utils import CHANCE, NO_ACTION, NO_VALUE

ROCK = 0
PAPER = 1
SCISSORS = 2


class RepeatedRPS(FOSG):

    def __init__(self, rounds=2, bias=1):
        self.rounds = rounds
        self.reward_matrix = [
            [0, -bias, 1],
            [bias, 0, -1],
            [-1, 1, 0]
        ]

    def get_initial_state(self):
        return RepeatedRPSState(self.rounds, self)


class RepeatedRPSState(State):
    def __init__(self, rounds: int, game: RepeatedRPS):
        self.rounds = rounds
        self.actions_played = np.full((self.rounds, 2), fill_value=NO_ACTION, dtype=int)
        self.round = 0
        self.terminal = False
        self.game = game
        self.value = NO_VALUE

    def get_possible_actions(self):
        if self.terminal:
            return [[], [], []]
        else:
            return [[ROCK, PAPER, SCISSORS], [ROCK, PAPER, SCISSORS], [(NO_ACTION, 1)]]

    def get_possible_joint_actions(self):
        actions = self.get_possible_actions()
        joint_actions = []
        for first_player_action in actions[0]:
            for second_player_action in actions[1]:
                for chance_player_action in actions[2]:
                    joint_actions.append([first_player_action, second_player_action, chance_player_action])
        return joint_actions

    def can_play(self, player: int):
        if player == CHANCE:
            return False
        return not self.terminal

    def apply_actions(self, actions):
        assert not self.terminal
        for action, possible_actions in zip(actions, self.get_possible_actions()):
            assert action in possible_actions, "Invalid action selected"
        self.actions_played[self.round] = actions[:2]
        self.round += 1
        if self.round == self.rounds:
            value = 0
            self.terminal = True
            for action_pair in self.actions_played:
                value += self.game.reward_matrix[action_pair[0]][action_pair[1]]
            self.value = value

    def get_private_information(self, player: int):
        return (self.actions_played[self.round - 1][player] if self.terminal else NO_ACTION),

    def get_public_information(self):
        return tuple(map(tuple, self.actions_played[:self.round - (1 if self.terminal else 0)])), self.round

    def get_state_string(self):
        return f"Repeated RPS state - Round: {self.round} Actions played: {self.actions_played}"

    def is_terminal(self):
        return self.terminal

    def get_value(self):
        assert self.is_terminal()
        return self.value

    def __str__(self):
        return self.get_state_string()
