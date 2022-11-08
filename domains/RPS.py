from FOSG import FOSG, State
from utils import CHANCE, NO_ACTION, NO_VALUE

ROCK = 0
PAPER = 1
SCISSORS = 2


class RPS(FOSG):

    def __init__(self, bias=1):
        self.reward_matrix = [
            [0, -bias, 1],
            [bias, 0, -1],
            [-1, 1, 0]
        ]

    def get_initial_state(self):
        return RPSState(self)


class RPSState(State):
    def __init__(self, game: RPS):
        self.actions_played = [NO_ACTION, NO_ACTION]
        self.terminal = False
        self.value = NO_VALUE
        self.game = game

    def get_possible_actions(self):
        if self.terminal:
            return [[], [], []]
        else:
            return [[ROCK, PAPER, SCISSORS], [ROCK, PAPER, SCISSORS], [NO_ACTION], [1]]

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
            assert action in possible_actions,  f"Invalid action selected {action}. Possible actions {possible_actions}."
        self.actions_played = actions[:2]
        self.terminal = True
        self.value = self.game.reward_matrix[self.actions_played[0]][self.actions_played[1]]

    def get_private_information(self, player: int):
        return self.actions_played[player],

    def get_public_information(self):
        return self.terminal,

    def get_state_string(self):
        return "Terminal" if self.terminal else "Root" + (" Value: " + str(self.value) if self.is_terminal() else "")

    def is_terminal(self):
        return self.terminal

    def get_value(self):
        assert self.is_terminal()
        return self.value
