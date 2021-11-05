from poker_round import PokerRound
from combination_value import CombinationChecker


def main():
    poker_round = PokerRound(5, 2)
    poker_round.prepare_round()
    poker_round.initiate_round()
    print(poker_round.describe_player_hands())
    poker_round.deal_board()
    print(poker_round.describe_board())


if __name__ == "__main__":
    main()
