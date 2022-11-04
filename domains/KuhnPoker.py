from FOSG import FOSG, State
import numpy as np
from utils import opponent, CHANCE, NO_ACTION, NO_VALUE

CARDS_DEALT = -3
NO_CARD = -1
ANTE = 1
FOLD = 0
CALL = 1
BET = 2
CARD_TO_STRING = {-1: "", 0: "J", 1: "Q", 2: "K"}


class KuhnPoker(FOSG):

    @staticmethod
    def get_initial_state():
        return KuhnPokerState()


class KuhnPokerState(State):
    def __init__(self):
        self.private_cards_dealt = False
        self.private_cards = np.asarray([NO_CARD, NO_CARD])
        self.public_sequence = []
        self.deck = np.arange(0, 3)
        self.pot = ANTE * 2
        self.player_on_turn = CHANCE
        self.call_needed = False
        self.terminal = False
        self.player_folded = -1
        self.first_action_after_chance = False
        self.pot_contributions = [1, 1]
        self.showdown = False
        self.value = NO_VALUE

    def get_possible_actions(self):
        if self.terminal:
            return [[], [], []]
        if self.player_on_turn == CHANCE:
            chance_actions = []
            if self.private_cards_dealt:
                for card in self.deck:
                    chance_actions.append(card)
            else:
                for card_one in self.deck:
                    for card_two in self.deck:
                        if card_one != card_two:
                            chance_actions.append(card_one * 3 + card_two)
            return [[NO_ACTION], [NO_ACTION], chance_actions, np.full(len(chance_actions), fill_value=1. / len(chance_actions), dtype=float)]
        else:
            actions = [[], [], [NO_ACTION], [1]]
            if self.call_needed:
                actions[opponent(self.player_on_turn)] = [NO_ACTION]
                actions[self.player_on_turn] = [FOLD, CALL]
            else:
                actions[opponent(self.player_on_turn)] = [NO_ACTION]
                actions[self.player_on_turn] = [CALL, BET]
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
        return player == self.player_on_turn

    def apply_actions(self, actions):
        assert not self.terminal
        for action, possible_actions in zip(actions, self.get_possible_actions()):
            assert action in possible_actions, "Invalid action selected"
        if self.player_on_turn == CHANCE:
            chance_action = actions[2]
            cards = np.asarray([int(chance_action / 3), chance_action % 3])
            self.private_cards = cards
            self.deck = np.delete(self.deck, np.where(self.deck == cards[0]))
            self.deck = np.delete(self.deck, np.where(self.deck == cards[1]))
            self.private_cards_dealt = True
            self.first_action_after_chance = True
            self.public_sequence.append(CARDS_DEALT)
            self.player_on_turn = 0
        else:
            player_action = actions[self.player_on_turn]
            self.public_sequence.append(player_action)
            if player_action == FOLD:
                self.terminal = True
                self.player_folded = self.player_on_turn
                self.value = (-1 if self.player_on_turn == 0 else 1)
                self.player_on_turn = -1
            elif player_action == CALL:
                if self.call_needed:
                    self.pot += 1
                    self.pot_contributions[self.player_on_turn] += 1
                    self.call_needed = False
                if self.first_action_after_chance:
                    self.player_on_turn = opponent(self.player_on_turn)
                else:
                    self.player_on_turn = -1
                    self.showdown = True
                    self.terminal = True
                    if self.private_cards[0] < self.private_cards[1]:
                        self.value = -self.pot_contributions[0]
                    else:
                        self.value = self.pot_contributions[0]
            elif player_action == BET:
                self.pot += 1
                self.pot_contributions[self.player_on_turn] += 1
                self.player_on_turn = opponent(self.player_on_turn)
                self.call_needed = True
            self.first_action_after_chance = False

    def get_private_information(self, player: int):
        return self.private_cards[player],

    def get_public_information(self):
        return tuple(self.public_sequence), self.player_folded, tuple(self.pot_contributions)

    def get_current_deck(self):
        return [CARD_TO_STRING[card] for card in self.deck]

    def get_private_cards(self):
        return [CARD_TO_STRING[card] for card in self.private_cards]

    def get_state_string(self):
        return "Player: " + str(self.player_on_turn) + " Deck: " + str(self.get_current_deck()) + " Hands: " + str(self.get_private_cards()) + " Pot: " + str(self.pot) + " Pot contribution: " + str(
            self.pot_contributions) + " Public sequence: " + str(self.public_sequence) + (" Value: " + str(self.value) if self.is_terminal() else "")

    def is_terminal(self):
        return self.terminal

    def get_value(self):
        assert self.is_terminal()
        return self.value
