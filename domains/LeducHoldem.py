from FOSG import FOSG, State
import numpy as np
from utils import opponent, CHANCE, NO_ACTION, NO_VALUE

CARDS_DEALT = -3
NO_CARD = -1
ANTE = 1
BET_STRUCTURE = [2, 4]
FOLD = 0
CALL = 1
BET = 2
CARD_TO_STRING = {-1: "", 0: "Jh", 1: "Js", 2: "Qh", 3: "Qs", 4: "Kh", 5: "Ks"}


class LeducHoldem(FOSG):

    @staticmethod
    def get_initial_state():
        return LeducHoldemState()


class LeducHoldemState(State):
    def __init__(self):
        self.private_cards_dealt = False
        self.private_cards = np.asarray([NO_CARD, NO_CARD])
        self.public_card = NO_CARD
        self.public_sequence = []
        self.deck = np.arange(0, 6)
        self.pot = ANTE * 2
        self.round = 0
        self.player_on_turn = CHANCE
        self.call_needed = False
        self.terminal = False
        self.player_folded = -1
        self.bets_this_round = 0
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
                            chance_actions.append(card_one * 6 + card_two)
            return [[NO_ACTION], [NO_ACTION], chance_actions, np.full(len(chance_actions), fill_value=1. / len(chance_actions), dtype=float)]
        else:
            actions = [[], [], [NO_ACTION], [1]]
            if self.call_needed:
                actions[opponent(self.player_on_turn)] = [NO_ACTION]
                if self.bets_this_round == 2:
                    actions[self.player_on_turn] = [FOLD, CALL]
                else:
                    actions[self.player_on_turn] = [FOLD, CALL, BET]
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
        return not (self.get_possible_actions()[player] == [NO_ACTION] or self.get_possible_actions()[player] == [])

    def apply_actions(self, actions):
        assert not self.terminal
        for action, possible_actions in zip(actions, self.get_possible_actions()):
            assert action in possible_actions,  f"Invalid action selected {action}. Possible actions {possible_actions}."
        if self.player_on_turn == CHANCE:
            chance_action = actions[2]
            if self.private_cards_dealt:
                self.public_card = chance_action
                self.deck = np.delete(self.deck, np.where(self.deck == chance_action))
                self.round += 1
                self.first_action_after_chance = True
                self.bets_this_round = 0
                self.public_sequence.append(self.public_card)
            else:
                cards = np.asarray([int(chance_action / 6), chance_action % 6])
                self.private_cards = cards
                self.deck = np.delete(self.deck, np.where(self.deck == cards[0]))
                self.deck = np.delete(self.deck, np.where(self.deck == cards[1]))
                self.private_cards_dealt = True
                self.first_action_after_chance = True
                self.bets_this_round = 0
                self.public_sequence.append(CARDS_DEALT)
            self.player_on_turn = 0
        else:
            player_action = actions[self.player_on_turn]
            self.public_sequence.append(player_action)
            if player_action == FOLD:
                self.terminal = True
                self.player_folded = self.player_on_turn
                self.player_on_turn = -1
                self.value = (-1 * self.pot_contributions[self.player_folded] if self.player_folded == 0 else self.pot_contributions[self.player_folded])
            elif player_action == CALL:
                if self.call_needed:
                    self.pot += BET_STRUCTURE[self.round]
                    self.pot_contributions[self.player_on_turn] += BET_STRUCTURE[self.round]
                    self.call_needed = False
                if self.first_action_after_chance:
                    self.player_on_turn = opponent(self.player_on_turn)
                else:
                    if self.round == 0:
                        self.player_on_turn = CHANCE
                    else:
                        self.player_on_turn = -1
                        self.showdown = True
                        self.terminal = True
                        self.value = self.get_showdown_value()
            elif player_action == BET:
                self.pot += BET_STRUCTURE[self.round]
                self.pot_contributions[self.player_on_turn] += BET_STRUCTURE[self.round]
                if self.call_needed:
                    self.pot += BET_STRUCTURE[self.round]
                    self.pot_contributions[self.player_on_turn] += BET_STRUCTURE[self.round]
                self.bets_this_round += 1
                self.player_on_turn = opponent(self.player_on_turn)
                self.call_needed = True
            self.first_action_after_chance = False

    def get_showdown_value(self):
        card_ranks = [int(self.private_cards[0] / 2), int(self.private_cards[1] / 2)]
        for player in range(2):
            if card_ranks[player] == int(self.public_card / 2):
                return self.pot_contributions[0] if player == 0 else -self.pot_contributions[0]
        if card_ranks[0] < card_ranks[1]:
            return -self.pot_contributions[0]
        if card_ranks[0] > card_ranks[1]:
            return self.pot_contributions[0]
        else:
            return 0

    def get_private_information(self, player: int):
        return self.private_cards[player],

    def get_public_information(self):
        return tuple(self.public_sequence), self.public_card, self.player_folded, tuple(self.pot_contributions)

    def get_current_deck(self):
        return [CARD_TO_STRING[card] for card in self.deck]

    def get_private_cards(self):
        return [CARD_TO_STRING[card] for card in self.private_cards]

    def get_state_string(self):
        return "Player: " + str(self.player_on_turn) + " Deck: " + str(self.get_current_deck()) + " Hands: " + str(self.get_private_cards()) + " Pot: " + str(self.pot) + " Public card: " + CARD_TO_STRING[
            self.public_card] + " Pot contribution: " + str(self.pot_contributions) + " Public sequence: " + str(self.public_sequence) + (" Value: " + str(self.value) if self.is_terminal() else "")

    def is_terminal(self):
        return self.terminal

    def get_value(self):
        assert self.is_terminal()
        return self.value
