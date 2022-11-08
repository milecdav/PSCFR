import utils
from FOSG import FOSG, State
import numpy as np


class GambitExporter:
    def __init__(self, game: FOSG):
        self.game = game

        self.chance_index = 0
        self.terminal_index = 0
        self.current_information_sets = [0, 0]
        self.information_set_mapping = [{}, {}]

    def export(self, file_name):
        self.chance_index = 0
        self.terminal_index = 0
        with open(file_name, "w") as file:
            file.write("EFG 2 R \"My tree\" { \"Player 1\" \"Player 2\" }\n")
            self.save_node_to_file(self.game.get_initial_state(), 0, file, 0, [])

    def save_node_to_file(self, node: State, level: int, file, current_player: int, previous_actions):
        if not node.is_terminal() and not node.can_play(current_player):
            new_actions = np.copy(previous_actions).astype(int)
            new_actions = np.append(new_actions, utils.NO_ACTION)
            if current_player == utils.CHANCE:
                self.save_node_to_file(node.get_child(new_actions), level, file, 0, [])
            else:
                self.save_node_to_file(node, level, file, current_player + 1, new_actions)
            return
        for i in range(level):
            file.write(" ")
        if node.is_terminal():
            file.write("t \"\" " + str(self.terminal_index) + " \"\" { " + str(node.get_value()) + " " + str(-node.get_value()) + " }\n")
            self.terminal_index += 1
            return
        if current_player == utils.CHANCE:
            file.write("c \"\" " + str(self.chance_index) + " \"\" { ")
            self.chance_index += 1
            for chance_action, probability in zip(node.get_possible_actions()[2], node.get_possible_actions()[3]):
                file.write("\"" + (str(chance_action)) + "\" " + str(probability) + " ")
            file.write("} 0\n")
            for chance_action in node.get_possible_actions()[2]:
                new_actions = np.copy(previous_actions).astype(int)
                new_actions = np.append(new_actions, chance_action)
                self.save_node_to_file(node.get_child(new_actions), level + 1, file, 0, [])
        else:
            player_information = node.get_player_information(current_player)
            if player_information in self.information_set_mapping[current_player]:
                player_information_set = self.information_set_mapping[current_player][player_information]
            else:
                player_information_set = self.current_information_sets[current_player]
                self.information_set_mapping[current_player][player_information] = player_information_set
                self.current_information_sets[current_player] += 1
            file.write("p \"\" " + str(current_player + 1) + " " + str(player_information_set) + " \"\" {")
            for player_action in node.get_possible_actions()[current_player]:
                file.write(" \"" + str(player_action) + "\"")
            file.write(" } 0\n")
            for player_action in node.get_possible_actions()[current_player]:
                new_actions = np.copy(previous_actions).astype(int)
                new_actions = np.append(new_actions, player_action)
                self.save_node_to_file(node, level + 1, file, current_player + 1, new_actions)
