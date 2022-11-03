from FOSG import FOSG
from algorithms.public_tree import PublicTree
from algorithms.infoset_tree import InfosetTreeNode, DECISION_NODE
import numpy as np
from utils import opponent


class CFR:
    def __init__(self, game: FOSG, verbosity=0):
        self.game = game
        self.public_tree = PublicTree(self.game)
        self.child_indexes = [{}, {}]
        self.indexes = [{}, {}]
        self.current_index = 1
        self.value_sizes = [0, 0]
        self.strategy = [{}, {}]
        self.regret = [{}, {}]
        self.decision_nodes = [[], []]
        self.cumulative_strategy = [{}, {}]
        self.cumulative_count = 0
        self.iteration = 1
        self.verbosity = verbosity

        self.set_indexes()

        # value vectors
        self.reaches = [np.zeros(self.value_sizes[0]), np.zeros(self.value_sizes[1])]
        self.cfvs = [np.zeros(self.value_sizes[0]), np.zeros(self.value_sizes[1])]

        self.reaches[0][0] = 1
        self.reaches[1][0] = 1

    def set_indexes(self):
        self.current_index = 1
        self.indexes[0][self.public_tree.infoset_trees[0].root.infoset] = 0
        self.tree_walk_for_indexes(self.public_tree.infoset_trees[0].root, 0)
        self.value_sizes[0] = self.current_index
        self.current_index = 1
        self.indexes[1][self.public_tree.infoset_trees[1].root.infoset] = 0
        self.tree_walk_for_indexes(self.public_tree.infoset_trees[1].root, 1)
        self.value_sizes[1] = self.current_index

    def tree_walk_for_indexes(self, node: InfosetTreeNode, player: int):
        if node.is_terminal():
            return
        if node.node_type == DECISION_NODE:
            self.decision_nodes[player].append(node)
            self.strategy[player][node.infoset] = np.full(node.num_children(), fill_value=1. / node.num_children())
            self.cumulative_strategy[player][node.infoset] = np.zeros(node.num_children(), dtype=float)
            self.regret[player][node.infoset] = np.zeros(node.num_children(), dtype=float)
        num_children = node.num_children()
        self.child_indexes[player][node.infoset] = (self.current_index, self.current_index + num_children)
        self.current_index += num_children
        child_indexes = np.arange(self.current_index - num_children, self.current_index)
        for i, child in enumerate(node.children):
            self.indexes[player][child.infoset] = child_indexes[i]
            self.tree_walk_for_indexes(child, player)

    # iteration functions
    def perform_iteration(self):
        self.compute_reaches()
        if self.verbosity > 0:
            print("Reaches:")
            print(self.reaches)
        self.compute_terminal_values()
        if self.verbosity > 0:
            print("Counterfactual values:")
            print(self.cfvs)
        self.compute_cfvs()
        if self.verbosity > 0:
            print("Updated counterfactual values:")
            print(self.cfvs)
        self.compute_regret()
        self.compute_strategy()
        if self.verbosity > 0:
            print("Computed strategy")
            print(self.strategy)
        self.cumulative_count += self.iteration
        self.iteration += 1

    def compute_reaches(self):
        self.compute_reaches_step(self.public_tree.root)

    def compute_reaches_step(self, node):
        if node.is_terminal():
            return
        for player in range(2):
            for infoset_node in node.infoset_nodes[player]:
                if infoset_node.node_type == DECISION_NODE:
                    start_index, end_index = self.child_indexes[player][infoset_node.infoset]
                    self.reaches[player][start_index:end_index] = self.reaches[player][self.indexes[player][infoset_node.infoset]] * self.strategy[player][infoset_node.infoset]
                else:
                    start_index, end_index = self.child_indexes[player][infoset_node.infoset]
                    self.reaches[player][start_index:end_index] = self.reaches[player][self.indexes[player][infoset_node.infoset]]
        for child in node.children:
            self.compute_reaches_step(child)

    def compute_cfvs(self):
        self.compute_cfvs_step(self.public_tree.root)

    def compute_cfvs_step(self, node):
        if node.is_terminal():
            return
        for child in node.children:
            self.compute_cfvs_step(child)
        for player in range(2):
            for infoset_node in node.infoset_nodes[player]:
                start_index, end_index = self.child_indexes[player][infoset_node.infoset]
                if self.verbosity > 1:
                    print("Cfvs computation:")
                    print(self.cfvs[player][start_index:end_index])
                if infoset_node.node_type == DECISION_NODE:
                    if self.verbosity > 1:
                        print(self.strategy[player][infoset_node.infoset])
                    self.cfvs[player][self.indexes[player][infoset_node.infoset]] = np.dot(self.cfvs[player][start_index:end_index], self.strategy[player][infoset_node.infoset])
                else:
                    self.cfvs[player][self.indexes[player][infoset_node.infoset]] = np.sum(self.cfvs[player][start_index:end_index])
                if self.verbosity > 1:
                    print(self.cfvs[player][self.indexes[player][infoset_node.infoset]])

    def compute_regret(self):
        for player in range(2):
            for node in self.decision_nodes[player]:
                start_index, end_index = self.child_indexes[player][node.infoset]
                self.regret[player][node.infoset] += self.cfvs[player][start_index:end_index] - self.cfvs[player][self.indexes[player][node.infoset]]
                self.regret[player][node.infoset] = np.clip(self.regret[player][node.infoset], a_min=0, a_max=None)

    def compute_strategy(self):
        for player in range(2):
            for node in self.decision_nodes[player]:
                regret_sum = np.sum(self.regret[player][node.infoset])
                if regret_sum > 0:
                    self.strategy[player][node.infoset] = self.regret[player][node.infoset] / regret_sum
                else:
                    self.strategy[player][node.infoset] = np.full(node.num_children(), fill_value=1. / node.num_children())
                self.cumulative_strategy[player][node.infoset] += self.iteration * self.strategy[player][node.infoset] * self.reaches[player][self.indexes[player][node.infoset]]

    def compute_terminal_values(self):
        for node in self.public_tree.terminal_states:
            player_indexes = []
            for player in range(2):
                indexes = []
                for infoset_node in node.infoset_nodes[player]:
                    indexes.append(self.indexes[player][infoset_node.infoset])
                player_indexes.append(indexes)
            for player in range(2):
                self.cfvs[player][player_indexes[player]] = np.matmul(node.terminal_matrices[player], self.reaches[opponent(player)][player_indexes[opponent(player)]])
                if self.verbosity > 1:
                    print("Terminal values computation:")
                    print(node)
                    print(indexes)
                    print(player)
                    print(self.reaches[opponent(player)][indexes])
                    print(self.cfvs[player][indexes])

    def normalize_cumulative_strategy(self):
        for player in range(2):
            for node in self.decision_nodes[player]:
                self.cumulative_strategy[player][node.infoset] /= np.sum(self.cumulative_strategy[player][node.infoset])

    def root_cfvs(self):
        values = [0., 0.]
        for player in range(2):
            for node in self.public_tree.root.infoset_nodes[0]:
                values[player] += self.cfvs[player][self.indexes[player][node.infoset]]
        return values

    def print_decision_cfvs(self):
        for player, tree in enumerate(self.public_tree.infoset_trees):
            print(f"Player {player}")
            for infoset_string in tree.nodes:
                node = tree.get_node(infoset_string)
                # if node.is_terminal():
                #     print(infoset_string, self.cfvs[player][self.indexes[player][infoset_string]])
                if node.node_type == DECISION_NODE:
                    start_index, end_index = self.child_indexes[player][infoset_string]
                    print(infoset_string, self.cfvs[player][self.indexes[player][infoset_string]], self.cfvs[player][start_index:end_index])
