import unittest
from domains import KuhnPoker, LeducHoldem, RepeatedRPS, RPS
from algorithms.cfr import CFR


def get_cfr_value(domain):
    cfr = CFR(domain, verbosity=0)
    for i in range(1000):
        cfr.perform_iteration()
    cfr.normalize_cumulative_strategy()
    cfr.strategy = cfr.cumulative_strategy
    cfr.compute_reaches()
    cfr.compute_terminal_values()
    cfr.compute_cfvs()
    return cfr.root_cfvs()[0]


class TestTreeSizes(unittest.TestCase):
    def test_kuhn_poker(self):
        game_value = get_cfr_value(KuhnPoker.KuhnPoker())
        self.assertAlmostEqual(game_value, -1. / 18, 3)

    def test_leduc_holdem(self):
        game_value = get_cfr_value(LeducHoldem.LeducHoldem())
        self.assertAlmostEqual(game_value, -0.085606424, 3)

    def test_repeated_rps(self):
        game_value = get_cfr_value(RepeatedRPS.RepeatedRPS(bias=2))
        self.assertAlmostEqual(game_value, 0, 3)

    def test_rps(self):
        game_value = get_cfr_value(RPS.RPS(bias=2))
        self.assertAlmostEqual(game_value, 0, 3)


if __name__ == '__main__':
    unittest.main()
