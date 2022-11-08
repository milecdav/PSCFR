import unittest
from algorithms.public_tree import PublicTree
from domains import KuhnPoker, LeducHoldem, RepeatedRPS, RPS, TickTacToe, SmallDrawPoker
from algorithms.infoset_tree import DECISION_NODE, TERMINAL_NODE, HELPER_NODE, OBSERVATION_NODE


def infoset_count(domain):
    decision_nodes = 0
    helper_nodes = 0
    terminal_nodes = 0
    observation_nodes = 0

    def crawl(node):
        if node.node_type == DECISION_NODE:
            nonlocal decision_nodes
            decision_nodes += 1
        elif node.node_type == OBSERVATION_NODE:
            nonlocal observation_nodes
            observation_nodes += 1
        elif node.node_type == HELPER_NODE:
            nonlocal helper_nodes
            helper_nodes += 1
        elif node.node_type == TERMINAL_NODE:
            nonlocal terminal_nodes
            terminal_nodes += 1
        else:
            assert False, f"Invalid node type {node.node_type}"
        for child in node.children:
            crawl(child)

    tree = PublicTree(domain)
    crawl(tree.infoset_trees[0].root)
    return decision_nodes, observation_nodes, helper_nodes, terminal_nodes


class TestTreeSizes(unittest.TestCase):
    def test_kuhn_poker(self):
        decision_nodes, observation_nodes, helper_nodes, terminal_nodes = infoset_count(KuhnPoker.KuhnPoker())
        self.assertEqual(decision_nodes, 6)
        self.assertEqual(observation_nodes, 8)
        self.assertEqual(helper_nodes, 0)
        self.assertEqual(terminal_nodes, 15)

    def test_leduc_holdem(self):
        decision_nodes, observation_nodes, helper_nodes, terminal_nodes = infoset_count(LeducHoldem.LeducHoldem())
        self.assertEqual(decision_nodes, 468)
        self.assertEqual(observation_nodes, 500)
        self.assertEqual(helper_nodes, 0)
        self.assertEqual(terminal_nodes, 1374)

    def test_repeated_rps(self):
        decision_nodes, observation_nodes, helper_nodes, terminal_nodes = infoset_count(RepeatedRPS.RepeatedRPS())
        self.assertEqual(decision_nodes, 10)
        self.assertEqual(observation_nodes, 1)
        self.assertEqual(helper_nodes, 30)
        self.assertEqual(terminal_nodes, 27)

    def test_rps(self):
        decision_nodes, observation_nodes, helper_nodes, terminal_nodes = infoset_count(RPS.RPS())
        self.assertEqual(decision_nodes, 1)
        self.assertEqual(observation_nodes, 1)
        self.assertEqual(helper_nodes, 3)
        self.assertEqual(terminal_nodes, 3)

    def test_small_draw_poker(self):
        decision_nodes, observation_nodes, helper_nodes, terminal_nodes = infoset_count(SmallDrawPoker.SmallDrawPoker())
        self.assertEqual(decision_nodes, 1128)
        self.assertEqual(observation_nodes, 1490)
        self.assertEqual(helper_nodes, 0)
        self.assertEqual(terminal_nodes, 3264)

    def test_tick_tac_toe(self):
        decision_nodes, observation_nodes, helper_nodes, terminal_nodes = infoset_count(TickTacToe.TickTacToe(2))
        self.assertEqual(decision_nodes, 13)
        self.assertEqual(observation_nodes, 5)
        self.assertEqual(helper_nodes, 0)
        self.assertEqual(terminal_nodes, 24)


if __name__ == '__main__':
    unittest.main()
