DECISION_NODE = 0
OBSERVATION_NODE = 1
HELPER_NODE = 2
TERMINAL_NODE = 3


class InfosetTreeNode:
    def __init__(self, node_type: int, infoset):
        self.parent = None
        self.infoset = infoset
        self.node_type = node_type
        self.children = []

    def set_parent(self, parent):
        self.parent = parent

    def add_child(self, node):
        self.children.append(node)

    def num_children(self):
        return len(self.children)

    def get_infoset(self):
        return self.infoset

    def is_terminal(self):
        return self.node_type == TERMINAL_NODE

    def __str__(self):
        return str(self.infoset)

    def __repr__(self):
        return str(self.infoset)


class InfosetTree:
    def __init__(self, player):
        self.root = None
        self.player = player
        self.nodes = {}

    def get_node(self, information_state):
        return self.nodes.get(information_state)

    def add_node(self, information_state, node):
        self.nodes[information_state] = node

    def print_tree(self):
        def print_tree_step(node, level):
            print("".join(["-"] * level), end="")
            print(node, "Children:", node.children, node.node_type)
            for child in node.children:
                print_tree_step(child, level + 1)

        print_tree_step(self.root, 0)
