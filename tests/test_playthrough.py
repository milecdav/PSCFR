import unittest
from domains import RepeatedRPS, RPS, SmallDrawPoker, KuhnPoker, LeducHoldem, TickTacToe, Battleships
from FOSG import FOSG
from utils import NO_ACTION


class TestPlaythrough(unittest.TestCase):
    def check_playthrough(self, domain: FOSG, actions, state_strings):
        state = domain.get_initial_state()
        self.assertEqual(state.get_state_string(), state_strings[0])
        for action, state_string in zip(actions, state_strings[1:]):
            state.apply_actions(action)
            self.assertEqual(state.get_state_string(), state_string)

    def test_kuhn_poker(self):
        action_arrays = [
            [
                [NO_ACTION, NO_ACTION, 1],
                [SmallDrawPoker.CALL, NO_ACTION, NO_ACTION],
                [NO_ACTION, SmallDrawPoker.BET, NO_ACTION],
                [SmallDrawPoker.CALL, NO_ACTION, NO_ACTION],
            ],
            [
                [NO_ACTION, NO_ACTION, 2],
                [SmallDrawPoker.CALL, NO_ACTION, NO_ACTION],
                [NO_ACTION, SmallDrawPoker.BET, NO_ACTION],
                [SmallDrawPoker.FOLD, NO_ACTION, NO_ACTION],
            ],
            [
                [NO_ACTION, NO_ACTION, 3],
                [SmallDrawPoker.CALL, NO_ACTION, NO_ACTION],
                [NO_ACTION, SmallDrawPoker.CALL, NO_ACTION],
            ],
            [
                [NO_ACTION, NO_ACTION, 5],
                [SmallDrawPoker.BET, NO_ACTION, NO_ACTION],
                [NO_ACTION, SmallDrawPoker.CALL, NO_ACTION],
            ],
            [
                [NO_ACTION, NO_ACTION, 6],
                [SmallDrawPoker.BET, NO_ACTION, NO_ACTION],
                [NO_ACTION, SmallDrawPoker.FOLD, NO_ACTION],
            ]
        ]

        state_string_arrays = [
            [
                "Player: 2 Deck: ['J', 'Q', 'K'] Hands: ['', ''] Pot: 2 Pot contribution: [1, 1] Public sequence: []",
                "Player: 0 Deck: ['K'] Hands: ['J', 'Q'] Pot: 2 Pot contribution: [1, 1] Public sequence: [-3]",
                "Player: 1 Deck: ['K'] Hands: ['J', 'Q'] Pot: 2 Pot contribution: [1, 1] Public sequence: [-3, 1]",
                "Player: 0 Deck: ['K'] Hands: ['J', 'Q'] Pot: 3 Pot contribution: [1, 2] Public sequence: [-3, 1, 2]",
                "Player: -1 Deck: ['K'] Hands: ['J', 'Q'] Pot: 4 Pot contribution: [2, 2] Public sequence: [-3, 1, 2, 1] Value: -2"
            ],
            [
                "Player: 2 Deck: ['J', 'Q', 'K'] Hands: ['', ''] Pot: 2 Pot contribution: [1, 1] Public sequence: []",
                "Player: 0 Deck: ['Q'] Hands: ['J', 'K'] Pot: 2 Pot contribution: [1, 1] Public sequence: [-3]",
                "Player: 1 Deck: ['Q'] Hands: ['J', 'K'] Pot: 2 Pot contribution: [1, 1] Public sequence: [-3, 1]",
                "Player: 0 Deck: ['Q'] Hands: ['J', 'K'] Pot: 3 Pot contribution: [1, 2] Public sequence: [-3, 1, 2]",
                "Player: -1 Deck: ['Q'] Hands: ['J', 'K'] Pot: 3 Pot contribution: [1, 2] Public sequence: [-3, 1, 2, 0] Value: -1"
            ],
            [
                "Player: 2 Deck: ['J', 'Q', 'K'] Hands: ['', ''] Pot: 2 Pot contribution: [1, 1] Public sequence: []",
                "Player: 0 Deck: ['K'] Hands: ['Q', 'J'] Pot: 2 Pot contribution: [1, 1] Public sequence: [-3]",
                "Player: 1 Deck: ['K'] Hands: ['Q', 'J'] Pot: 2 Pot contribution: [1, 1] Public sequence: [-3, 1]",
                "Player: -1 Deck: ['K'] Hands: ['Q', 'J'] Pot: 2 Pot contribution: [1, 1] Public sequence: [-3, 1, 1] Value: 1"
            ],
            [
                "Player: 2 Deck: ['J', 'Q', 'K'] Hands: ['', ''] Pot: 2 Pot contribution: [1, 1] Public sequence: []",
                "Player: 0 Deck: ['J'] Hands: ['Q', 'K'] Pot: 2 Pot contribution: [1, 1] Public sequence: [-3]",
                "Player: 1 Deck: ['J'] Hands: ['Q', 'K'] Pot: 3 Pot contribution: [2, 1] Public sequence: [-3, 2]",
                "Player: -1 Deck: ['J'] Hands: ['Q', 'K'] Pot: 4 Pot contribution: [2, 2] Public sequence: [-3, 2, 1] Value: -2"
            ],
            [
                "Player: 2 Deck: ['J', 'Q', 'K'] Hands: ['', ''] Pot: 2 Pot contribution: [1, 1] Public sequence: []",
                "Player: 0 Deck: ['Q'] Hands: ['K', 'J'] Pot: 2 Pot contribution: [1, 1] Public sequence: [-3]",
                "Player: 1 Deck: ['Q'] Hands: ['K', 'J'] Pot: 3 Pot contribution: [2, 1] Public sequence: [-3, 2]",
                "Player: -1 Deck: ['Q'] Hands: ['K', 'J'] Pot: 3 Pot contribution: [2, 1] Public sequence: [-3, 2, 0] Value: 1"
            ]
        ]

        for actions, state_strings in zip(action_arrays, state_string_arrays):
            self.check_playthrough(KuhnPoker.KuhnPoker(), actions, state_strings)

    def test_leduc_holdem(self):
        action_arrays = [
            [
                [NO_ACTION, NO_ACTION, 5],
                [SmallDrawPoker.CALL, NO_ACTION, NO_ACTION],
                [NO_ACTION, SmallDrawPoker.BET, NO_ACTION],
                [SmallDrawPoker.BET, NO_ACTION, NO_ACTION],
                [NO_ACTION, SmallDrawPoker.CALL, NO_ACTION],
                [NO_ACTION, NO_ACTION, 1],
                [SmallDrawPoker.CALL, NO_ACTION, NO_ACTION],
                [NO_ACTION, SmallDrawPoker.BET, NO_ACTION],
                [SmallDrawPoker.BET, NO_ACTION, NO_ACTION],
                [NO_ACTION, SmallDrawPoker.CALL, NO_ACTION],
            ],
            [
                [NO_ACTION, NO_ACTION, 10],
                [SmallDrawPoker.CALL, NO_ACTION, NO_ACTION],
                [NO_ACTION, SmallDrawPoker.CALL, NO_ACTION],
                [NO_ACTION, NO_ACTION, 2],
                [SmallDrawPoker.CALL, NO_ACTION, NO_ACTION],
                [NO_ACTION, SmallDrawPoker.CALL, NO_ACTION],
            ],
            [
                [NO_ACTION, NO_ACTION, 15],
                [SmallDrawPoker.BET, NO_ACTION, NO_ACTION],
                [NO_ACTION, SmallDrawPoker.CALL, NO_ACTION],
                [NO_ACTION, NO_ACTION, 4],
                [SmallDrawPoker.CALL, NO_ACTION, NO_ACTION],
                [NO_ACTION, SmallDrawPoker.BET, NO_ACTION],
                [SmallDrawPoker.FOLD, NO_ACTION, NO_ACTION],
            ]
        ]

        state_string_arrays = [
            [
                "Player: 2 Deck: ['Jh', 'Js', 'Qh', 'Qs', 'Kh', 'Ks'] Hands: ['', ''] Pot: 2 Public card:  Pot contribution: [1, 1] Public sequence: []",
                "Player: 0 Deck: ['Js', 'Qh', 'Qs', 'Kh'] Hands: ['Jh', 'Ks'] Pot: 2 Public card:  Pot contribution: [1, 1] Public sequence: [-3]",
                "Player: 1 Deck: ['Js', 'Qh', 'Qs', 'Kh'] Hands: ['Jh', 'Ks'] Pot: 2 Public card:  Pot contribution: [1, 1] Public sequence: [-3, 1]",
                "Player: 0 Deck: ['Js', 'Qh', 'Qs', 'Kh'] Hands: ['Jh', 'Ks'] Pot: 4 Public card:  Pot contribution: [1, 3] Public sequence: [-3, 1, 2]",
                "Player: 1 Deck: ['Js', 'Qh', 'Qs', 'Kh'] Hands: ['Jh', 'Ks'] Pot: 8 Public card:  Pot contribution: [5, 3] Public sequence: [-3, 1, 2, 2]",
                "Player: 2 Deck: ['Js', 'Qh', 'Qs', 'Kh'] Hands: ['Jh', 'Ks'] Pot: 10 Public card:  Pot contribution: [5, 5] Public sequence: [-3, 1, 2, 2, 1]",
                "Player: 0 Deck: ['Qh', 'Qs', 'Kh'] Hands: ['Jh', 'Ks'] Pot: 10 Public card: Js Pot contribution: [5, 5] Public sequence: [-3, 1, 2, 2, 1, 1]",
                "Player: 1 Deck: ['Qh', 'Qs', 'Kh'] Hands: ['Jh', 'Ks'] Pot: 10 Public card: Js Pot contribution: [5, 5] Public sequence: [-3, 1, 2, 2, 1, 1, 1]",
                "Player: 0 Deck: ['Qh', 'Qs', 'Kh'] Hands: ['Jh', 'Ks'] Pot: 14 Public card: Js Pot contribution: [5, 9] Public sequence: [-3, 1, 2, 2, 1, 1, 1, 2]",
                "Player: 1 Deck: ['Qh', 'Qs', 'Kh'] Hands: ['Jh', 'Ks'] Pot: 22 Public card: Js Pot contribution: [13, 9] Public sequence: [-3, 1, 2, 2, 1, 1, 1, 2, 2]",
                "Player: -1 Deck: ['Qh', 'Qs', 'Kh'] Hands: ['Jh', 'Ks'] Pot: 26 Public card: Js Pot contribution: [13, 13] Public sequence: [-3, 1, 2, 2, 1, 1, 1, 2, 2, 1] Value: 13"
            ],
            [
                "Player: 2 Deck: ['Jh', 'Js', 'Qh', 'Qs', 'Kh', 'Ks'] Hands: ['', ''] Pot: 2 Public card:  Pot contribution: [1, 1] Public sequence: []",
                "Player: 0 Deck: ['Jh', 'Qh', 'Qs', 'Ks'] Hands: ['Js', 'Kh'] Pot: 2 Public card:  Pot contribution: [1, 1] Public sequence: [-3]",
                "Player: 1 Deck: ['Jh', 'Qh', 'Qs', 'Ks'] Hands: ['Js', 'Kh'] Pot: 2 Public card:  Pot contribution: [1, 1] Public sequence: [-3, 1]",
                "Player: 2 Deck: ['Jh', 'Qh', 'Qs', 'Ks'] Hands: ['Js', 'Kh'] Pot: 2 Public card:  Pot contribution: [1, 1] Public sequence: [-3, 1, 1]",
                "Player: 0 Deck: ['Jh', 'Qs', 'Ks'] Hands: ['Js', 'Kh'] Pot: 2 Public card: Qh Pot contribution: [1, 1] Public sequence: [-3, 1, 1, 2]",
                "Player: 1 Deck: ['Jh', 'Qs', 'Ks'] Hands: ['Js', 'Kh'] Pot: 2 Public card: Qh Pot contribution: [1, 1] Public sequence: [-3, 1, 1, 2, 1]",
                "Player: -1 Deck: ['Jh', 'Qs', 'Ks'] Hands: ['Js', 'Kh'] Pot: 2 Public card: Qh Pot contribution: [1, 1] Public sequence: [-3, 1, 1, 2, 1, 1] Value: -1"
            ],
            [
                "Player: 2 Deck: ['Jh', 'Js', 'Qh', 'Qs', 'Kh', 'Ks'] Hands: ['', ''] Pot: 2 Public card:  Pot contribution: [1, 1] Public sequence: []",
                "Player: 0 Deck: ['Jh', 'Js', 'Kh', 'Ks'] Hands: ['Qh', 'Qs'] Pot: 2 Public card:  Pot contribution: [1, 1] Public sequence: [-3]",
                "Player: 1 Deck: ['Jh', 'Js', 'Kh', 'Ks'] Hands: ['Qh', 'Qs'] Pot: 4 Public card:  Pot contribution: [3, 1] Public sequence: [-3, 2]",
                "Player: 2 Deck: ['Jh', 'Js', 'Kh', 'Ks'] Hands: ['Qh', 'Qs'] Pot: 6 Public card:  Pot contribution: [3, 3] Public sequence: [-3, 2, 1]",
                "Player: 0 Deck: ['Jh', 'Js', 'Ks'] Hands: ['Qh', 'Qs'] Pot: 6 Public card: Kh Pot contribution: [3, 3] Public sequence: [-3, 2, 1, 4]",
                "Player: 1 Deck: ['Jh', 'Js', 'Ks'] Hands: ['Qh', 'Qs'] Pot: 6 Public card: Kh Pot contribution: [3, 3] Public sequence: [-3, 2, 1, 4, 1]",
                "Player: 0 Deck: ['Jh', 'Js', 'Ks'] Hands: ['Qh', 'Qs'] Pot: 10 Public card: Kh Pot contribution: [3, 7] Public sequence: [-3, 2, 1, 4, 1, 2]",
                "Player: -1 Deck: ['Jh', 'Js', 'Ks'] Hands: ['Qh', 'Qs'] Pot: 10 Public card: Kh Pot contribution: [3, 7] Public sequence: [-3, 2, 1, 4, 1, 2, 0] Value: -3"
            ]
        ]

        for actions, state_strings in zip(action_arrays, state_string_arrays):
            self.check_playthrough(LeducHoldem.LeducHoldem(), actions, state_strings)

    def test_repeated_rps(self):
        action_arrays = [
            [
                [RepeatedRPS.ROCK, RepeatedRPS.PAPER, NO_ACTION],
                [RepeatedRPS.ROCK, RepeatedRPS.PAPER, NO_ACTION],
            ],
            [
                [RepeatedRPS.ROCK, RepeatedRPS.ROCK, NO_ACTION],
                [RepeatedRPS.ROCK, RepeatedRPS.SCISSORS, NO_ACTION],
            ],
            [
                [RepeatedRPS.PAPER, RepeatedRPS.PAPER, NO_ACTION],
                [RepeatedRPS.SCISSORS, RepeatedRPS.SCISSORS, NO_ACTION],
            ],
            [
                [RepeatedRPS.PAPER, RepeatedRPS.SCISSORS, NO_ACTION],
                [RepeatedRPS.SCISSORS, RepeatedRPS.ROCK, NO_ACTION],
            ]
        ]

        state_string_arrays = [
            [
                "Repeated RPS state - Round: 0 Actions played: ['[-2 -2]', '[-2 -2]']",
                "Repeated RPS state - Round: 1 Actions played: ['[0 1]', '[-2 -2]']",
                "Repeated RPS state - Round: 2 Actions played: ['[0 1]', '[0 1]'] Value: -4"
            ],
            [
                "Repeated RPS state - Round: 0 Actions played: ['[-2 -2]', '[-2 -2]']",
                "Repeated RPS state - Round: 1 Actions played: ['[0 0]', '[-2 -2]']",
                "Repeated RPS state - Round: 2 Actions played: ['[0 0]', '[0 2]'] Value: 1"
            ],
            [
                "Repeated RPS state - Round: 0 Actions played: ['[-2 -2]', '[-2 -2]']",
                "Repeated RPS state - Round: 1 Actions played: ['[1 1]', '[-2 -2]']",
                "Repeated RPS state - Round: 2 Actions played: ['[1 1]', '[2 2]'] Value: 0"
            ],
            [
                "Repeated RPS state - Round: 0 Actions played: ['[-2 -2]', '[-2 -2]']",
                "Repeated RPS state - Round: 1 Actions played: ['[1 2]', '[-2 -2]']",
                "Repeated RPS state - Round: 2 Actions played: ['[1 2]', '[2 0]'] Value: -2"
            ]
        ]

        for actions, state_strings in zip(action_arrays, state_string_arrays):
            self.check_playthrough(RepeatedRPS.RepeatedRPS(bias=2), actions, state_strings)

    def test_rps(self):
        action_arrays = [
            [
                [RPS.PAPER, RPS.SCISSORS, NO_ACTION],
            ],
            [
                [RPS.ROCK, RPS.ROCK, NO_ACTION],
            ],
            [
                [RPS.ROCK, RPS.PAPER, NO_ACTION],
            ]
        ]

        state_string_arrays = [
            [
                "Root",
                "Terminal - Actions: [1, 2] Value: -1"
            ],
            [
                "Root",
                "Terminal - Actions: [0, 0] Value: 0"
            ],
            [
                "Root",
                "Terminal - Actions: [0, 1] Value: -5"
            ]
        ]

        for actions, state_strings in zip(action_arrays, state_string_arrays):
            self.check_playthrough(RPS.RPS(bias=5), actions, state_strings)

    def test_small_draw_poker(self):
        action_arrays = [
            [
                [NO_ACTION, NO_ACTION, 12],
                [SmallDrawPoker.CALL, NO_ACTION, NO_ACTION],
                [NO_ACTION, SmallDrawPoker.BET, NO_ACTION],
                [SmallDrawPoker.BET, NO_ACTION, NO_ACTION],
                [NO_ACTION, SmallDrawPoker.CALL, NO_ACTION],
                [SmallDrawPoker.EXCHANGE, NO_ACTION, NO_ACTION],
                [NO_ACTION, NO_ACTION, 5],
                [NO_ACTION, SmallDrawPoker.KEEP, NO_ACTION],
                [SmallDrawPoker.CALL, NO_ACTION, NO_ACTION],
                [NO_ACTION, SmallDrawPoker.CALL, NO_ACTION],
            ],
            [
                [NO_ACTION, NO_ACTION, 24],
                [SmallDrawPoker.BET, NO_ACTION, NO_ACTION],
                [NO_ACTION, SmallDrawPoker.CALL, NO_ACTION],
                [SmallDrawPoker.KEEP, NO_ACTION, NO_ACTION],
                [NO_ACTION, SmallDrawPoker.EXCHANGE, NO_ACTION],
                [NO_ACTION, NO_ACTION, 5],
                [SmallDrawPoker.BET, NO_ACTION, NO_ACTION],
                [NO_ACTION, SmallDrawPoker.BET, NO_ACTION],
                [SmallDrawPoker.CALL, NO_ACTION, NO_ACTION],
            ],
            [
                [NO_ACTION, NO_ACTION, 3],
                [SmallDrawPoker.CALL, NO_ACTION, NO_ACTION],
                [NO_ACTION, SmallDrawPoker.BET, NO_ACTION],
                [SmallDrawPoker.CALL, NO_ACTION, NO_ACTION],
                [SmallDrawPoker.EXCHANGE, NO_ACTION, NO_ACTION],
                [NO_ACTION, NO_ACTION, 2],
                [NO_ACTION, SmallDrawPoker.EXCHANGE, NO_ACTION],
                [NO_ACTION, NO_ACTION, 1],
                [SmallDrawPoker.BET, NO_ACTION, NO_ACTION],
                [NO_ACTION, SmallDrawPoker.BET, NO_ACTION],
                [SmallDrawPoker.FOLD, NO_ACTION, NO_ACTION],
            ],
            [
                [NO_ACTION, NO_ACTION, 30],
                [SmallDrawPoker.CALL, NO_ACTION, NO_ACTION],
                [NO_ACTION, SmallDrawPoker.CALL, NO_ACTION],
                [SmallDrawPoker.KEEP, NO_ACTION, NO_ACTION],
                [NO_ACTION, SmallDrawPoker.KEEP, NO_ACTION],
                [SmallDrawPoker.BET, NO_ACTION, NO_ACTION],
                [NO_ACTION, SmallDrawPoker.FOLD, NO_ACTION],
            ]
        ]

        state_string_arrays = [
            [
                "Player: 2 Deck: ['Jh', 'Js', 'Qh', 'Qs', 'Kh', 'Ks'] Hands: ['', ''] Pot: 2 Pot contribution: [1, 1] Public sequence: []",
                "Player: 0 Deck: ['Js', 'Qs', 'Kh', 'Ks'] Hands: ['Qh', 'Jh'] Pot: 2 Pot contribution: [1, 1] Public sequence: [-3]",
                "Player: 1 Deck: ['Js', 'Qs', 'Kh', 'Ks'] Hands: ['Qh', 'Jh'] Pot: 2 Pot contribution: [1, 1] Public sequence: [-3, 1]",
                "Player: 0 Deck: ['Js', 'Qs', 'Kh', 'Ks'] Hands: ['Qh', 'Jh'] Pot: 4 Pot contribution: [1, 3] Public sequence: [-3, 1, 2]",
                "Player: 1 Deck: ['Js', 'Qs', 'Kh', 'Ks'] Hands: ['Qh', 'Jh'] Pot: 8 Pot contribution: [5, 3] Public sequence: [-3, 1, 2, 2]",
                "Player: 0 Deck: ['Js', 'Qs', 'Kh', 'Ks'] Hands: ['Qh', 'Jh'] Pot: 10 Pot contribution: [5, 5] Public sequence: [-3, 1, 2, 2, 1]",
                "Player: 2 Deck: ['Js', 'Qs', 'Kh', 'Ks'] Hands: ['Qh', 'Jh'] Pot: 10 Pot contribution: [5, 5] Public sequence: [-3, 1, 2, 2, 1, 3]",
                "Player: 1 Deck: ['Js', 'Qs', 'Kh'] Hands: ['Ks', 'Jh'] Pot: 10 Pot contribution: [5, 5] Public sequence: [-3, 1, 2, 2, 1, 3, -4]",
                "Player: 0 Deck: ['Js', 'Qs', 'Kh'] Hands: ['Ks', 'Jh'] Pot: 10 Pot contribution: [5, 5] Public sequence: [-3, 1, 2, 2, 1, 3, -4, 4]",
                "Player: 1 Deck: ['Js', 'Qs', 'Kh'] Hands: ['Ks', 'Jh'] Pot: 10 Pot contribution: [5, 5] Public sequence: [-3, 1, 2, 2, 1, 3, -4, 4, 1]",
                "Player: -1 Deck: ['Js', 'Qs', 'Kh'] Hands: ['Ks', 'Jh'] Pot: 10 Pot contribution: [5, 5] Public sequence: [-3, 1, 2, 2, 1, 3, -4, 4, 1, 1] Value: 5"
            ],
            [
                "Player: 2 Deck: ['Jh', 'Js', 'Qh', 'Qs', 'Kh', 'Ks'] Hands: ['', ''] Pot: 2 Pot contribution: [1, 1] Public sequence: []",
                "Player: 0 Deck: ['Js', 'Qh', 'Qs', 'Ks'] Hands: ['Kh', 'Jh'] Pot: 2 Pot contribution: [1, 1] Public sequence: [-3]",
                "Player: 1 Deck: ['Js', 'Qh', 'Qs', 'Ks'] Hands: ['Kh', 'Jh'] Pot: 4 Pot contribution: [3, 1] Public sequence: [-3, 2]",
                "Player: 0 Deck: ['Js', 'Qh', 'Qs', 'Ks'] Hands: ['Kh', 'Jh'] Pot: 6 Pot contribution: [3, 3] Public sequence: [-3, 2, 1]",
                "Player: 1 Deck: ['Js', 'Qh', 'Qs', 'Ks'] Hands: ['Kh', 'Jh'] Pot: 6 Pot contribution: [3, 3] Public sequence: [-3, 2, 1, 4]",
                "Player: 2 Deck: ['Js', 'Qh', 'Qs', 'Ks'] Hands: ['Kh', 'Jh'] Pot: 6 Pot contribution: [3, 3] Public sequence: [-3, 2, 1, 4, 3]",
                "Player: 0 Deck: ['Js', 'Qh', 'Qs'] Hands: ['Kh', 'Ks'] Pot: 6 Pot contribution: [3, 3] Public sequence: [-3, 2, 1, 4, 3, -4]",
                "Player: 1 Deck: ['Js', 'Qh', 'Qs'] Hands: ['Kh', 'Ks'] Pot: 10 Pot contribution: [7, 3] Public sequence: [-3, 2, 1, 4, 3, -4, 2]",
                "Player: 0 Deck: ['Js', 'Qh', 'Qs'] Hands: ['Kh', 'Ks'] Pot: 18 Pot contribution: [7, 11] Public sequence: [-3, 2, 1, 4, 3, -4, 2, 2]",
                "Player: -1 Deck: ['Js', 'Qh', 'Qs'] Hands: ['Kh', 'Ks'] Pot: 22 Pot contribution: [11, 11] Public sequence: [-3, 2, 1, 4, 3, -4, 2, 2, 1] Value: 0"
            ],
            [
                "Player: 2 Deck: ['Jh', 'Js', 'Qh', 'Qs', 'Kh', 'Ks'] Hands: ['', ''] Pot: 2 Pot contribution: [1, 1] Public sequence: []",
                "Player: 0 Deck: ['Js', 'Qh', 'Kh', 'Ks'] Hands: ['Jh', 'Qs'] Pot: 2 Pot contribution: [1, 1] Public sequence: [-3]",
                "Player: 1 Deck: ['Js', 'Qh', 'Kh', 'Ks'] Hands: ['Jh', 'Qs'] Pot: 2 Pot contribution: [1, 1] Public sequence: [-3, 1]",
                "Player: 0 Deck: ['Js', 'Qh', 'Kh', 'Ks'] Hands: ['Jh', 'Qs'] Pot: 4 Pot contribution: [1, 3] Public sequence: [-3, 1, 2]",
                "Player: 0 Deck: ['Js', 'Qh', 'Kh', 'Ks'] Hands: ['Jh', 'Qs'] Pot: 6 Pot contribution: [3, 3] Public sequence: [-3, 1, 2, 1]",
                "Player: 2 Deck: ['Js', 'Qh', 'Kh', 'Ks'] Hands: ['Jh', 'Qs'] Pot: 6 Pot contribution: [3, 3] Public sequence: [-3, 1, 2, 1, 3]",
                "Player: 1 Deck: ['Js', 'Kh', 'Ks'] Hands: ['Qh', 'Qs'] Pot: 6 Pot contribution: [3, 3] Public sequence: [-3, 1, 2, 1, 3, -4]",
                "Player: 2 Deck: ['Js', 'Kh', 'Ks'] Hands: ['Qh', 'Qs'] Pot: 6 Pot contribution: [3, 3] Public sequence: [-3, 1, 2, 1, 3, -4, 3]",
                "Player: 0 Deck: ['Kh', 'Ks'] Hands: ['Qh', 'Js'] Pot: 6 Pot contribution: [3, 3] Public sequence: [-3, 1, 2, 1, 3, -4, 3, -4]",
                "Player: 1 Deck: ['Kh', 'Ks'] Hands: ['Qh', 'Js'] Pot: 10 Pot contribution: [7, 3] Public sequence: [-3, 1, 2, 1, 3, -4, 3, -4, 2]",
                "Player: 0 Deck: ['Kh', 'Ks'] Hands: ['Qh', 'Js'] Pot: 18 Pot contribution: [7, 11] Public sequence: [-3, 1, 2, 1, 3, -4, 3, -4, 2, 2]",
                "Player: -1 Deck: ['Kh', 'Ks'] Hands: ['Qh', 'Js'] Pot: 18 Pot contribution: [7, 11] Public sequence: [-3, 1, 2, 1, 3, -4, 3, -4, 2, 2, 0] Value: -7"
            ],
            [
                "Player: 2 Deck: ['Jh', 'Js', 'Qh', 'Qs', 'Kh', 'Ks'] Hands: ['', ''] Pot: 2 Pot contribution: [1, 1] Public sequence: []",
                "Player: 0 Deck: ['Js', 'Qh', 'Qs', 'Kh'] Hands: ['Ks', 'Jh'] Pot: 2 Pot contribution: [1, 1] Public sequence: [-3]",
                "Player: 1 Deck: ['Js', 'Qh', 'Qs', 'Kh'] Hands: ['Ks', 'Jh'] Pot: 2 Pot contribution: [1, 1] Public sequence: [-3, 1]",
                "Player: 0 Deck: ['Js', 'Qh', 'Qs', 'Kh'] Hands: ['Ks', 'Jh'] Pot: 2 Pot contribution: [1, 1] Public sequence: [-3, 1, 1]",
                "Player: 1 Deck: ['Js', 'Qh', 'Qs', 'Kh'] Hands: ['Ks', 'Jh'] Pot: 2 Pot contribution: [1, 1] Public sequence: [-3, 1, 1, 4]",
                "Player: 0 Deck: ['Js', 'Qh', 'Qs', 'Kh'] Hands: ['Ks', 'Jh'] Pot: 2 Pot contribution: [1, 1] Public sequence: [-3, 1, 1, 4, 4]",
                "Player: 1 Deck: ['Js', 'Qh', 'Qs', 'Kh'] Hands: ['Ks', 'Jh'] Pot: 6 Pot contribution: [5, 1] Public sequence: [-3, 1, 1, 4, 4, 2]",
                "Player: -1 Deck: ['Js', 'Qh', 'Qs', 'Kh'] Hands: ['Ks', 'Jh'] Pot: 6 Pot contribution: [5, 1] Public sequence: [-3, 1, 1, 4, 4, 2, 0] Value: 1"
            ]
        ]
        for actions, state_strings in zip(action_arrays, state_string_arrays):
            self.check_playthrough(SmallDrawPoker.SmallDrawPoker(), actions, state_strings)

    def test_tick_tac_toe(self):
        action_arrays = [
            [
                [4, NO_ACTION, NO_ACTION],
                [NO_ACTION, 0, NO_ACTION],
                [8, NO_ACTION, NO_ACTION],
                [NO_ACTION, 1, NO_ACTION],
                [2, NO_ACTION, NO_ACTION],
                [NO_ACTION, 6, NO_ACTION],
                [5, NO_ACTION, NO_ACTION]
            ],
            [
                [4, NO_ACTION, NO_ACTION],
                [NO_ACTION, 0, NO_ACTION],
                [2, NO_ACTION, NO_ACTION],
                [NO_ACTION, 6, NO_ACTION],
                [3, NO_ACTION, NO_ACTION],
                [NO_ACTION, 5, NO_ACTION],
                [7, NO_ACTION, NO_ACTION],
                [NO_ACTION, 1, NO_ACTION],
                [8, NO_ACTION, NO_ACTION]
            ],
            [
                [0, NO_ACTION, NO_ACTION],
                [NO_ACTION, 1, NO_ACTION],
                [2, NO_ACTION, NO_ACTION],
                [NO_ACTION, 4, NO_ACTION],
                [6, NO_ACTION, NO_ACTION],
                [NO_ACTION, 7, NO_ACTION],
            ]
        ]

        state_string_arrays = [
            [
                "Tick Tack Toe state - Board: ['[0. 0. 0.]', '[0. 0. 0.]', '[0. 0. 0.]'] Active player: 0",
                "Tick Tack Toe state - Board: ['[0. 0. 0.]', '[0. 1. 0.]', '[0. 0. 0.]'] Active player: 1",
                "Tick Tack Toe state - Board: ['[-1.  0.  0.]', '[0. 1. 0.]', '[0. 0. 0.]'] Active player: 0",
                "Tick Tack Toe state - Board: ['[-1.  0.  0.]', '[0. 1. 0.]', '[0. 0. 1.]'] Active player: 1",
                "Tick Tack Toe state - Board: ['[-1. -1.  0.]', '[0. 1. 0.]', '[0. 0. 1.]'] Active player: 0",
                "Tick Tack Toe state - Board: ['[-1. -1.  1.]', '[0. 1. 0.]', '[0. 0. 1.]'] Active player: 1",
                "Tick Tack Toe state - Board: ['[-1. -1.  1.]', '[0. 1. 0.]', '[-1.  0.  1.]'] Active player: 0",
                "Tick Tack Toe state - Board: ['[-1. -1.  1.]', '[0. 1. 1.]', '[-1.  0.  1.]'] Value: 1"
            ],
            [
                "Tick Tack Toe state - Board: ['[0. 0. 0.]', '[0. 0. 0.]', '[0. 0. 0.]'] Active player: 0",
                "Tick Tack Toe state - Board: ['[0. 0. 0.]', '[0. 1. 0.]', '[0. 0. 0.]'] Active player: 1",
                "Tick Tack Toe state - Board: ['[-1.  0.  0.]', '[0. 1. 0.]', '[0. 0. 0.]'] Active player: 0",
                "Tick Tack Toe state - Board: ['[-1.  0.  1.]', '[0. 1. 0.]', '[0. 0. 0.]'] Active player: 1",
                "Tick Tack Toe state - Board: ['[-1.  0.  1.]', '[0. 1. 0.]', '[-1.  0.  0.]'] Active player: 0",
                "Tick Tack Toe state - Board: ['[-1.  0.  1.]', '[1. 1. 0.]', '[-1.  0.  0.]'] Active player: 1",
                "Tick Tack Toe state - Board: ['[-1.  0.  1.]', '[ 1.  1. -1.]', '[-1.  0.  0.]'] Active player: 0",
                "Tick Tack Toe state - Board: ['[-1.  0.  1.]', '[ 1.  1. -1.]', '[-1.  1.  0.]'] Active player: 1",
                "Tick Tack Toe state - Board: ['[-1. -1.  1.]', '[ 1.  1. -1.]', '[-1.  1.  0.]'] Active player: 0",
                "Tick Tack Toe state - Board: ['[-1. -1.  1.]', '[ 1.  1. -1.]', '[-1.  1.  1.]'] Value: 0"
            ],
            [
                "Tick Tack Toe state - Board: ['[0. 0. 0.]', '[0. 0. 0.]', '[0. 0. 0.]'] Active player: 0",
                "Tick Tack Toe state - Board: ['[1. 0. 0.]', '[0. 0. 0.]', '[0. 0. 0.]'] Active player: 1",
                "Tick Tack Toe state - Board: ['[ 1. -1.  0.]', '[0. 0. 0.]', '[0. 0. 0.]'] Active player: 0",
                "Tick Tack Toe state - Board: ['[ 1. -1.  1.]', '[0. 0. 0.]', '[0. 0. 0.]'] Active player: 1",
                "Tick Tack Toe state - Board: ['[ 1. -1.  1.]', '[ 0. -1.  0.]', '[0. 0. 0.]'] Active player: 0",
                "Tick Tack Toe state - Board: ['[ 1. -1.  1.]', '[ 0. -1.  0.]', '[1. 0. 0.]'] Active player: 1",
                "Tick Tack Toe state - Board: ['[ 1. -1.  1.]', '[ 0. -1.  0.]', '[ 1. -1.  0.]'] Value: -1"
            ]
        ]

        for actions, state_strings in zip(action_arrays, state_string_arrays):
            self.check_playthrough(TickTacToe.TickTacToe(), actions, state_strings)

    def test_battleships_ship_size_one(self):
        action_arrays = [
            [
                [0, NO_ACTION, NO_ACTION],
                [NO_ACTION, 1, NO_ACTION],
                [0, NO_ACTION, NO_ACTION],
                [NO_ACTION, 3, NO_ACTION],
                [3, NO_ACTION, NO_ACTION],
                [NO_ACTION, 2, NO_ACTION],
                [2, NO_ACTION, NO_ACTION],
                [NO_ACTION, 0, NO_ACTION],
            ],
            [
                [3, NO_ACTION, NO_ACTION],
                [NO_ACTION, 3, NO_ACTION],
                [0, NO_ACTION, NO_ACTION],
                [NO_ACTION, 2, NO_ACTION],
                [1, NO_ACTION, NO_ACTION],
                [NO_ACTION, 1, NO_ACTION],
                [2, NO_ACTION, NO_ACTION],
                [NO_ACTION, 0, NO_ACTION],
                [3, NO_ACTION, NO_ACTION]
            ],
            [
                [0, NO_ACTION, NO_ACTION],
                [NO_ACTION, 3, NO_ACTION],
                [3, NO_ACTION, NO_ACTION]
            ]
        ]

        state_string_arrays = [
            [
                "Battleships state - Player: 0 Ships: [[], []] Actions: []",
                "Battleships state - Player: 1 Ships: [[0], []] Actions: []",
                "Battleships state - Player: 0 Ships: [[0], [1]] Actions: []",
                "Battleships state - Player: 1 Ships: [[0], [1]] Actions: [0]",
                "Battleships state - Player: 0 Ships: [[0], [1]] Actions: [0, 3]",
                "Battleships state - Player: 1 Ships: [[0], [1]] Actions: [0, 3, 3]",
                "Battleships state - Player: 0 Ships: [[0], [1]] Actions: [0, 3, 3, 2]",
                "Battleships state - Player: 1 Ships: [[0], [1]] Actions: [0, 3, 3, 2, 2]",
                "Battleships state - Terminal - Actions: [0, 3, 3, 2, 2, 0, -1] Value: -1",
            ],
            [
                "Battleships state - Player: 0 Ships: [[], []] Actions: []",
                "Battleships state - Player: 1 Ships: [[3], []] Actions: []",
                "Battleships state - Player: 0 Ships: [[3], [3]] Actions: []",
                "Battleships state - Player: 1 Ships: [[3], [3]] Actions: [0]",
                "Battleships state - Player: 0 Ships: [[3], [3]] Actions: [0, 2]",
                "Battleships state - Player: 1 Ships: [[3], [3]] Actions: [0, 2, 1]",
                "Battleships state - Player: 0 Ships: [[3], [3]] Actions: [0, 2, 1, 1]",
                "Battleships state - Player: 1 Ships: [[3], [3]] Actions: [0, 2, 1, 1, 2]",
                "Battleships state - Player: 0 Ships: [[3], [3]] Actions: [0, 2, 1, 1, 2, 0]",
                "Battleships state - Terminal - Actions: [0, 2, 1, 1, 2, 0, 3, -1] Value: 1",
            ],
            [
                "Battleships state - Player: 0 Ships: [[], []] Actions: []",
                "Battleships state - Player: 1 Ships: [[0], []] Actions: []",
                "Battleships state - Player: 0 Ships: [[0], [3]] Actions: []",
                "Battleships state - Terminal - Actions: [3, -1] Value: 1",
            ]
        ]

        for actions, state_strings in zip(action_arrays, state_string_arrays):
            self.check_playthrough(Battleships.Battleships(2, 2, 1), actions, state_strings)

    def test_battleships_ship_size_two(self):
        action_arrays = [
            [
                [0, NO_ACTION, NO_ACTION],
                [NO_ACTION, 10, NO_ACTION],
                [0, NO_ACTION, NO_ACTION],
                [NO_ACTION, 3, NO_ACTION],
                [3, NO_ACTION, NO_ACTION],
                [NO_ACTION, 2, NO_ACTION],
                [2, NO_ACTION, NO_ACTION],
                [NO_ACTION, 0, NO_ACTION],
            ],
            [
                [7, NO_ACTION, NO_ACTION],
                [NO_ACTION, 11, NO_ACTION],
                [7, NO_ACTION, NO_ACTION],
                [NO_ACTION, 4, NO_ACTION],
                [2, NO_ACTION, NO_ACTION],
                [NO_ACTION, 3, NO_ACTION],
            ],
            [
                [3, NO_ACTION, NO_ACTION],
                [NO_ACTION, 5, NO_ACTION],
                [4, NO_ACTION, NO_ACTION],
                [NO_ACTION, 7, NO_ACTION],
                [5, NO_ACTION, NO_ACTION],
                [NO_ACTION, 5, NO_ACTION],
                [8, NO_ACTION, NO_ACTION],
            ],
            [
                [0, NO_ACTION, NO_ACTION],
                [NO_ACTION, 1, NO_ACTION],
            ],
            [
                [2, NO_ACTION, NO_ACTION],
                [NO_ACTION, 3, NO_ACTION],
            ],
            [
                [4, NO_ACTION, NO_ACTION],
                [NO_ACTION, 5, NO_ACTION],
            ],
            [
                [6, NO_ACTION, NO_ACTION],
                [NO_ACTION, 7, NO_ACTION],
            ],
            [
                [8, NO_ACTION, NO_ACTION],
                [NO_ACTION, 9, NO_ACTION],
            ],
            [
                [10, NO_ACTION, NO_ACTION],
                [NO_ACTION, 11, NO_ACTION],
            ],

        ]

        state_string_arrays = [
            [
                "Battleships state - Player: 0 Ships: [[], []] Actions: []",
                "Battleships state - Player: 1 Ships: [[0, 3], []] Actions: []",
                "Battleships state - Player: 0 Ships: [[0, 3], [4, 5]] Actions: []",
                "Battleships state - Player: 1 Ships: [[0, 3], [4, 5]] Actions: [0]",
                "Battleships state - Player: 0 Ships: [[0], [4, 5]] Actions: [0, 3, -1]",
                "Battleships state - Player: 1 Ships: [[0], [4, 5]] Actions: [0, 3, -1, 3]",
                "Battleships state - Player: 0 Ships: [[0], [4, 5]] Actions: [0, 3, -1, 3, 2]",
                "Battleships state - Player: 1 Ships: [[0], [4, 5]] Actions: [0, 3, -1, 3, 2, 2]",
                "Battleships state - Terminal - Actions: [0, 3, -1, 3, 2, 2, 0, -1] Value: -1",
            ],
            [
                "Battleships state - Player: 0 Ships: [[], []] Actions: []",
                "Battleships state - Player: 1 Ships: [[3, 4], []] Actions: []",
                "Battleships state - Player: 0 Ships: [[3, 4], [7, 8]] Actions: []",
                "Battleships state - Player: 1 Ships: [[3, 4], [8]] Actions: [7, -1]",
                "Battleships state - Player: 0 Ships: [[3], [8]] Actions: [7, -1, 4, -1]",
                "Battleships state - Player: 1 Ships: [[3], [8]] Actions: [7, -1, 4, -1, 2]",
                "Battleships state - Terminal - Actions: [7, -1, 4, -1, 2, 3, -1] Value: -1",
            ],
            [
                "Battleships state - Player: 0 Ships: [[], []] Actions: []",
                "Battleships state - Player: 1 Ships: [[3, 6], []] Actions: []",
                "Battleships state - Player: 0 Ships: [[3, 6], [5, 8]] Actions: []",
                "Battleships state - Player: 1 Ships: [[3, 6], [5, 8]] Actions: [4]",
                "Battleships state - Player: 0 Ships: [[3, 6], [5, 8]] Actions: [4, 7]",
                "Battleships state - Player: 1 Ships: [[3, 6], [8]] Actions: [4, 7, 5, -1]",
                "Battleships state - Player: 0 Ships: [[3, 6], [8]] Actions: [4, 7, 5, -1, 5]",
                "Battleships state - Terminal - Actions: [4, 7, 5, -1, 5, 8, -1] Value: 1",
            ],
            [
                "Battleships state - Player: 0 Ships: [[], []] Actions: []",
                "Battleships state - Player: 1 Ships: [[0, 3], []] Actions: []",
                "Battleships state - Player: 0 Ships: [[0, 3], [1, 4]] Actions: []",
            ],
            [
                "Battleships state - Player: 0 Ships: [[], []] Actions: []",
                "Battleships state - Player: 1 Ships: [[2, 5], []] Actions: []",
                "Battleships state - Player: 0 Ships: [[2, 5], [3, 6]] Actions: []",
            ],
            [
                "Battleships state - Player: 0 Ships: [[], []] Actions: []",
                "Battleships state - Player: 1 Ships: [[4, 7], []] Actions: []",
                "Battleships state - Player: 0 Ships: [[4, 7], [5, 8]] Actions: []",
            ],
            [
                "Battleships state - Player: 0 Ships: [[], []] Actions: []",
                "Battleships state - Player: 1 Ships: [[0, 1], []] Actions: []",
                "Battleships state - Player: 0 Ships: [[0, 1], [3, 4]] Actions: []",
            ],
            [
                "Battleships state - Player: 0 Ships: [[], []] Actions: []",
                "Battleships state - Player: 1 Ships: [[6, 7], []] Actions: []",
                "Battleships state - Player: 0 Ships: [[6, 7], [1, 2]] Actions: []",
            ],
            [
                "Battleships state - Player: 0 Ships: [[], []] Actions: []",
                "Battleships state - Player: 1 Ships: [[4, 5], []] Actions: []",
                "Battleships state - Player: 0 Ships: [[4, 5], [7, 8]] Actions: []",
            ],
        ]

        for actions, state_strings in zip(action_arrays, state_string_arrays):
            self.check_playthrough(Battleships.Battleships(3, 3, 2), actions, state_strings)


if __name__ == '__main__':
    unittest.main()
