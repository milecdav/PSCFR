from algorithms.infoset_tree import InfosetTree, InfosetTreeNode, OBSERVATION_NODE, DECISION_NODE, HELPER_NODE, TERMINAL_NODE
from FOSG import FOSG, State
from utils import opponent, CHANCE
import numpy as np

MIDDLE = 0
TERMINAL = 1


class PublicNode:
    def __init__(self, node_type: int, public_sequence):
        self.node_type = node_type
        self.infoset_nodes = [[], []]
        self.children = []
        self.parent = None
        self.public_sequence = public_sequence
        self.terminal_matrices = {}

    def set_parent(self, node):
        self.parent = node

    def add_child(self, node):
        self.children.append(node)

    def is_terminal(self):
        return self.node_type == TERMINAL

    def __str__(self):
        return str(self.public_sequence)

    def __repr__(self):
        return str(self.public_sequence)


class PublicTree:
    def __init__(self, game: FOSG):
        self.num_nodes = 1
        self.infoset_trees = [InfosetTree(0), InfosetTree(1)]
        self.public_states = {}
        self.terminal_states = []
        self.helper_count = [0, 0]
        self.root = PublicNode(MIDDLE, (-1,))
        self.public_states[-1] = self.root
        self.infoset_trees[0].root = InfosetTreeNode(OBSERVATION_NODE, (-1,))
        self.infoset_trees[0].add_node(self.infoset_trees[0].root.infoset, self.infoset_trees[0].root)
        self.infoset_trees[1].root = InfosetTreeNode(OBSERVATION_NODE, (-1,))
        self.infoset_trees[1].add_node(self.infoset_trees[1].root.infoset, self.infoset_trees[1].root)
        self.root.infoset_nodes = [[self.infoset_trees[0].root], [self.infoset_trees[1].root]]
        initial_state = game.get_initial_state()
        self.build_tree_steps(self.root, [self.infoset_trees[0].root, self.infoset_trees[1].root], initial_state, 1.)
        self.build_terminal_matrices()

    def build_tree_steps(self, public_parent: PublicNode, infoset_parents, state: State, chance_reach: float):
        public_information = state.get_public_information()
        if public_information not in self.public_states:
            self.num_nodes += 1
            if state.is_terminal():
                new_public_node = PublicNode(TERMINAL, public_information)
                self.terminal_states.append(new_public_node)
            else:
                new_public_node = PublicNode(MIDDLE, public_information)
            self.public_states[public_information] = new_public_node
            new_public_node.set_parent(public_parent)
            public_parent.add_child(new_public_node)
        else:
            new_public_node = self.public_states[public_information]
        new_parents = [[], []]
        switch_for_dummy = False
        for player in range(2):
            information_state = state.get_player_information(player)
            if self.infoset_trees[player].get_node(information_state) is None:
                if state.is_terminal():
                    new_node = InfosetTreeNode(TERMINAL_NODE, information_state)
                elif state.can_play(player):
                    new_node = InfosetTreeNode(DECISION_NODE, information_state)
                else:
                    new_node = InfosetTreeNode(OBSERVATION_NODE, information_state)
                self.infoset_trees[player].add_node(information_state, new_node)
                new_node.set_parent(infoset_parents[player])
                new_public_node.infoset_nodes[player].append(new_node)
                infoset_parents[player].add_child(new_node)
                if state.can_play(player):
                    if len(state.get_possible_actions()[opponent(player)]) * len(state.get_possible_actions()[CHANCE]) > 1:
                        switch_for_dummy = True
                        dummy_public_information = public_information + ("dummy",)
                        if dummy_public_information not in self.public_states:
                            dummy_public_node = PublicNode(MIDDLE, dummy_public_information)
                            self.public_states[dummy_public_information] = dummy_public_node
                            dummy_public_node.set_parent(new_public_node)
                            new_public_node.add_child(dummy_public_node)
                        else:
                            dummy_public_node = self.public_states[dummy_public_information]
                        for _ in state.get_possible_actions()[player]:
                            new_helper_node = InfosetTreeNode(HELPER_NODE, "dummy node " + str(self.helper_count[player]))
                            self.helper_count[player] += 1
                            new_helper_node.set_parent(new_node)
                            new_node.add_child(new_helper_node)
                            new_parents[player].append(new_helper_node)
                            dummy_public_node.infoset_nodes[player].append(new_helper_node)
                    else:
                        new_parents[player] = [new_node] * len(state.get_possible_actions()[player])
                else:
                    new_parents[player].append(new_node)
            else:
                if state.can_play(player):
                    new_parents[player] = self.infoset_trees[player].get_node(information_state).children
                else:
                    new_parents[player] = [self.infoset_trees[player].get_node(information_state)]
        if state.is_terminal():
            information_states = (state.get_player_information(0), state.get_player_information(1))
            new_public_node.terminal_matrices[information_states] = state.get_value() * chance_reach
        if switch_for_dummy:
            new_public_node = dummy_public_node
        for i, action_one in enumerate(state.get_possible_actions()[0]):
            for j, action_two in enumerate(state.get_possible_actions()[1]):
                for chance_action, probability in state.get_possible_actions()[2]:
                    self.build_tree_steps(new_public_node, [new_parents[0][i], new_parents[1][j]], state.get_child([action_one, action_two, (chance_action, probability)]), chance_reach * probability)

    def build_terminal_matrices(self):
        for public_state in self.terminal_states:
            terminal_matrix = np.zeros((len(public_state.infoset_nodes[0]), len(public_state.infoset_nodes[0])))
            for i, player_one_node in enumerate(public_state.infoset_nodes[0]):
                infoset_string_one = player_one_node.get_infoset()
                for j, player_two_node in enumerate(public_state.infoset_nodes[1]):
                    infoset_string_two = player_two_node.get_infoset()
                    terminal_matrix[i, j] = public_state.terminal_matrices.get((infoset_string_one, infoset_string_two), 0)
            public_state.terminal_matrices = terminal_matrix, -np.transpose(terminal_matrix)

    def print_tree(self):
        def print_tree_step(node, level):
            print("".join(["-"] * level), end="")
            print(node, "Children:", node.children, "Infoset nodes", node.infoset_nodes)
            for child in node.children:
                print_tree_step(child, level + 1)

        print_tree_step(self.root, 0)
