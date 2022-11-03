from domains.LeducHoldem import LeducHoldem, NO_ACTION, FOLD, CALL, BET
from domains import RPS, RepeatedRPS, TickTacToe, KuhnPoker
from algorithms.infoset_tree import InfosetTree
from algorithms.public_tree import PublicTree
from algorithms.cfr import CFR
import time
import numpy as np

np.set_printoptions(linewidth=1600)


def time_test_leduc():
    start = time.time()
    for i in range(200000):
        initial_state = LeducHoldem.get_initial_state()
        # print(initial_state.get_state_string())
        # print(initial_state.get_public_information())

        initial_state.apply_actions([NO_ACTION, NO_ACTION, 2])
        # print(initial_state.get_state_string())
        # print(initial_state.get_public_information())

        initial_state.apply_actions([BET, NO_ACTION, NO_ACTION])
        # print(initial_state.get_state_string())
        # print(initial_state.get_public_information())

        initial_state.apply_actions([NO_ACTION, BET, NO_ACTION])
        # print(initial_state.get_state_string())
        # print(initial_state.get_public_information())

        initial_state.apply_actions([CALL, NO_ACTION, NO_ACTION])
        # print(initial_state.get_state_string())
        # print(initial_state.get_public_information())

        initial_state.apply_actions([NO_ACTION, NO_ACTION, 1])
        # print(initial_state.get_state_string())
        # print(initial_state.get_public_information())
    end = time.time()
    print(end - start)


dec_nodes = 0
helper_nodes = 0


def infoset_tree_test():
    tree = PublicTree(LeducHoldem())
    crawl(tree.root)
    print(dec_nodes, helper_nodes)


def crawl(node):
    print(node, node.children)
    print(node.infoset_nodes)
    global dec_nodes
    global helper_nodes
    if node.node_type == 0:
        dec_nodes += 1
    else:
        helper_nodes += 1
    for child in node.children:
        crawl(child)


def cfr_leduc_test():
    cfr = CFR(LeducHoldem(), verbosity=0)
    for i in range(10):
        print("Iteration:", i)
        cfr.perform_iteration()
    cfr.normalize_cumulative_strategy()
    cfr.strategy = cfr.cumulative_strategy
    cfr.compute_reaches()
    cfr.compute_terminal_values()
    cfr.compute_cfvs()
    print(cfr.root_cfvs())


def cfr_kuhn_test():
    cfr = CFR(KuhnPoker.KuhnPoker(), verbosity=0)
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


def cfr_rps_test():
    cfr = CFR(RPS.RPS(bias=2))
    cfr.public_tree.print_tree()
    for i in range(10000):
        print("Iteration:", i)
        cfr.perform_iteration()
    cfr.normalize_cumulative_strategy()
    cfr.strategy = cfr.cumulative_strategy
    cfr.compute_reaches()
    cfr.compute_terminal_values()
    cfr.compute_cfvs()
    print(cfr.root_cfvs())
    print(cfr.cfvs)
    print(cfr.strategy)


def cfr_repeated_rps_test():
    cfr = CFR(RepeatedRPS.RepeatedRPS(rounds=2), RepeatedRPS.RepeatedRPSTerminalEvaluation(bias=2), verbosity=0)
    cfr.public_tree.print_tree()
    for i in range(1000):
        print("Iteration:", i)
        cfr.perform_iteration()
    cfr.normalize_cumulative_strategy()
    cfr.strategy = cfr.cumulative_strategy
    cfr.compute_reaches()
    cfr.compute_terminal_values()
    cfr.compute_cfvs()
    print(cfr.root_cfvs())
    print(cfr.cfvs)
    print(cfr.strategy)


def cfr_tick_tac_toe_test():
    cfr = CFR(TickTacToe.TickTacToe(2), TickTacToe.TickTacToeEvaluation(), verbosity=0)
    print(len(cfr.public_tree.infoset_trees[0].nodes))
    for i in range(1000):
        print("Iteration:", i)
        cfr.perform_iteration()
    cfr.normalize_cumulative_strategy()
    cfr.strategy = cfr.cumulative_strategy
    cfr.compute_reaches()
    cfr.compute_terminal_values()
    cfr.compute_cfvs()
    print(cfr.root_cfvs())
    print(cfr.cfvs)
    print(cfr.strategy)


def cfr_repeated_mp_pi_test():
    cfr = CFR(RepeatedMPPI.RepeatedMPPI(2), RepeatedMPPI.RepeatedMPPIerminalEvaluation(), verbosity=0)
    print(len(cfr.public_tree.infoset_trees[0].nodes))
    for i in range(1000):
        print("Iteration:", i)
        cfr.perform_iteration()
    cfr.normalize_cumulative_strategy()
    cfr.strategy = cfr.cumulative_strategy
    cfr.compute_reaches()
    cfr.compute_terminal_values()
    cfr.compute_cfvs()
    print(cfr.root_cfvs())
    print(cfr.cfvs)
    print(cfr.strategy)


def cfr_repeated_mp_test():
    cfr = CFR(RepeatedMP.RepeatedMP(2), RepeatedMP.RepeatedMPTerminalEvaluation(bias=1), verbosity=0)
    cfr.public_tree.print_tree()
    print(len(cfr.public_tree.infoset_trees[0].nodes))
    for i in range(10000):
        print("Iteration:", i)
        cfr.perform_iteration()
    cfr.normalize_cumulative_strategy()
    cfr.strategy = cfr.cumulative_strategy
    cfr.compute_reaches()
    cfr.compute_terminal_values()
    cfr.compute_cfvs()
    print(cfr.root_cfvs())
    print(cfr.cfvs)
    print(cfr.strategy)


def repeated_rps_test():
    repeated_rps = RepeatedRPS.RepeatedRPS(2)
    state = repeated_rps.get_initial_state()

    print(state)
    print(state.get_public_information())
    print(state.get_private_information(0))

    state.apply_actions([0, 1, -2])

    print(state)
    print(state.get_public_information())
    print(state.get_private_information(0))

    state.apply_actions([2, 0, -2])

    print(state)
    print(state.get_public_information())
    print(state.get_private_information(0))


def tick_tac_toe_test():
    tick_tac_toe = TickTacToe.TickTacToe()
    state = tick_tac_toe.get_initial_state()

    print(state)
    print(state.get_public_information())
    print(state.get_private_information(0))
    print(state.get_possible_actions())

    state.apply_actions([4, -2, -2])

    print(state)
    print(state.get_public_information())
    print(state.get_private_information(0))

    state.apply_actions([-2, 0, -2])

    print(state)
    print(state.get_public_information())
    print(state.get_private_information(0))

    state.apply_actions([2, -2, -2])

    print(state)
    print(state.get_public_information())
    print(state.get_private_information(0))

    state.apply_actions([-2, 1, -2])

    print(state)
    print(state.get_public_information())
    print(state.get_private_information(0))

    state.apply_actions([6, -2, -2])

    print(state)
    print(state.get_public_information())
    print(state.get_private_information(0))


def mp_pi_test():
    mp_pi = RepeatedMPPI.RepeatedMPPI(2)
    state = mp_pi.get_initial_state()

    print(state)
    print(state.get_public_information())
    print(state.get_private_information(0))
    print(state.get_possible_actions())

    state.apply_actions([0, -2, -2])

    print(state)
    print(state.get_public_information())
    print(state.get_private_information(0))

    state.apply_actions([-2, 0, -2])

    print(state)
    print(state.get_public_information())
    print(state.get_private_information(0))

    state.apply_actions([0, -2, -2])

    print(state)
    print(state.get_public_information())
    print(state.get_private_information(0))

    state.apply_actions([-2, 1, -2])

    print(state)
    print(state.get_public_information())
    print(state.get_private_information(0))


if __name__ == '__main__':
    # start = time.time()
    # cfr_rps_test()
    # end = time.time()
    # print("Time elapsed:", end - start)
    # infoset_tree_test()
    # repeated_rps_test()
    # cfr_repeated_rps_test()
    # tick_tac_toe_test()
    # cfr_tick_tac_toe_test()
    # mp_pi_test()
    # cfr_repeated_mp_pi_test()
    # cfr_leduc_test()
    # cfr_repeated_mp_test()
    cfr_kuhn_test()
