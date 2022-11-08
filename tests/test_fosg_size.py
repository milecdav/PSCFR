import unittest
from domains import KuhnPoker, LeducHoldem, RepeatedRPS, RPS, TickTacToe, SmallDrawPoker
from FOSG import FOSG, State


def fosg_size(domain: FOSG):
    inner_nodes = 0
    terminal_nodes = 0

    def crawl(node: State):
        if node.is_terminal():
            nonlocal terminal_nodes
            terminal_nodes += 1
        else:
            nonlocal inner_nodes
            inner_nodes += 1
            for actions in node.get_possible_joint_actions():
                crawl(node.get_child(actions))

    crawl(domain.get_initial_state())
    return inner_nodes, terminal_nodes


class TestFosgSize(unittest.TestCase):
    def test_kuhn_poker(self):
        inner_nodes, terminal_nodes = fosg_size(KuhnPoker.KuhnPoker())
        self.assertEqual(inner_nodes, 25)
        self.assertEqual(terminal_nodes, 30)

    def test_leduc_holdem(self):
        inner_nodes, terminal_nodes = fosg_size(LeducHoldem.LeducHoldem())
        self.assertEqual(inner_nodes, 3931)
        self.assertEqual(terminal_nodes, 5520)

    def test_repeated_rps(self):
        inner_nodes, terminal_nodes = fosg_size(RepeatedRPS.RepeatedRPS())
        self.assertEqual(inner_nodes, 10)
        self.assertEqual(terminal_nodes, 81)

    def test_rps(self):
        inner_nodes, terminal_nodes = fosg_size(RPS.RPS())
        self.assertEqual(inner_nodes, 1)
        self.assertEqual(terminal_nodes, 9)

    def test_small_draw_poker(self):
        inner_nodes, terminal_nodes = fosg_size(SmallDrawPoker.SmallDrawPoker())
        self.assertEqual(inner_nodes, 20881)
        self.assertEqual(terminal_nodes, 28470)

    def test_tick_tac_toe(self):
        inner_nodes, terminal_nodes = fosg_size(TickTacToe.TickTacToe(board_size=2))
        self.assertEqual(inner_nodes, 17)
        self.assertEqual(terminal_nodes, 24)


if __name__ == '__main__':
    unittest.main()
