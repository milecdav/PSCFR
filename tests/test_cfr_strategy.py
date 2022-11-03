import unittest
from domains import RepeatedRPS, RPS
from algorithms.cfr import CFR


def get_cfr_strategy(domain):
    cfr = CFR(domain, verbosity=0)
    for i in range(10000):
        cfr.perform_iteration()
    cfr.normalize_cumulative_strategy()
    return cfr.cumulative_strategy


class TestTreeSizes(unittest.TestCase):
    def test_repeated_rps(self):
        strategy = get_cfr_strategy(RepeatedRPS.RepeatedRPS(bias=2))
        for player in range(2):
            for infoset_string in strategy[player]:
                self.assertAlmostEqual(strategy[player][infoset_string][0], 0.25, 1)
                self.assertAlmostEqual(strategy[player][infoset_string][1], 0.25, 1)
                self.assertAlmostEqual(strategy[player][infoset_string][2], 0.5, 1)

    def test_rps(self):
        strategy = get_cfr_strategy(RPS.RPS(bias=2))
        for player in range(2):
            for infoset_string in strategy[player]:
                self.assertAlmostEqual(strategy[player][infoset_string][0], 0.25, 2)
                self.assertAlmostEqual(strategy[player][infoset_string][1], 0.25, 2)
                self.assertAlmostEqual(strategy[player][infoset_string][2], 0.5, 2)


if __name__ == '__main__':
    unittest.main()
