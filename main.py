from domains import KuhnPoker
from algorithms.cfr import CFR


def example_pscfr_run():
    domain = KuhnPoker.KuhnPoker()
    cfr = CFR(domain, verbosity=0)
    for i in range(1000):
        print("Iteration:", i)
        cfr.perform_iteration()
    cfr.normalize_cumulative_strategy()
    cfr.strategy = cfr.cumulative_strategy
    cfr.compute_reaches()
    cfr.compute_terminal_values()
    cfr.compute_cfvs()
    print(cfr.strategy)
    print(cfr.root_cfvs())


if __name__ == '__main__':
    example_pscfr_run()
