import unittest
from poker_deck import PokerDeck
from poker_round import PokerRound
from combination_value import CombinationChecker
from poker_deck import PokerCard
from poker_deck import CardNumber
from poker_deck import CardColor
import os
import json


class TestPokerDeck(unittest.TestCase):
    def test_deck_length(self):
        test_deck = PokerDeck()
        test_deck.generate_deck()
        self.assertEqual(test_deck.get_current_stack_size(), 52)

    def test_deck_shuffle(self):
        test_deck = PokerDeck()
        test_deck.generate_deck()
        test_deck_string_before_shuffle = test_deck.get_deck_string()
        test_deck.shuffle_deck()
        test_deck_string_after_shuffle = test_deck.get_deck_string()
        self.assertNotEqual(test_deck_string_before_shuffle, test_deck_string_after_shuffle)

    def test_player_size(self):
        test_round = PokerRound(5, 2)
        test_round.prepare_round()
        test_round.initiate_round()
        self.assertEqual(test_round.number_of_players, test_round.get_player_count())

    def test_deck_length_after_deal(self):
        test_round = PokerRound(5, 2)
        test_round.prepare_round()
        test_round.initiate_round()
        test_round.deal_board()
        stack_size_after_deal = test_round.deck.get_current_stack_size()
        self.assertEqual(34, stack_size_after_deal)

    def test_deserialize_poker_card(self):
        json_card = '{"number": {"name": "TWO"}, "color": "SPADES", "description": "Two of SPADES"}'
        test_poker_card = PokerCard()
        test_poker_card.define_card_from_json(json_card)
        self.assertEqual(test_poker_card.get_number().name, "TWO")
        self.assertEqual(test_poker_card.get_color().name, "SPADES")
        self.assertEqual(test_poker_card.get_description(), "Two of SPADES")

    def test_serialize_and_deserialize_poker_card(self):
        test_poker_card01 = PokerCard()
        test_poker_card01.define_card(CardColor.SPADES, CardNumber.TWO)
        json_card01 = test_poker_card01.to_json()
        test_poker_card02 = PokerCard()
        test_poker_card02.define_card_from_json(json_card01)
        json_card02 = test_poker_card02.to_json()
        self.assertEqual(json_card01, json_card02)

    def test_serialize_poker_card(self):
        test_poker_card = PokerCard()
        test_poker_card.define_card(CardColor.SPADES, CardNumber.TWO)
        self.assertEqual(test_poker_card.to_json(),
                         '{"number": {"name": "TWO"}, "color": "SPADES", "description": "Two of SPADES"}')

    def test_card_value_get_number(self):
        test_poker_card = PokerCard()
        test_poker_card.define_card(CardColor.SPADES, CardNumber.TWO)
        self.assertEqual(test_poker_card.get_number().name, "TWO")

    def test_card_value_get_color(self):
        test_poker_card = PokerCard()
        test_poker_card.define_card(CardColor.SPADES, CardNumber.TWO)
        self.assertEqual(test_poker_card.get_color().name, "SPADES")

    def test_card_value_get_number_value(self):
        test_poker_card = PokerCard()
        test_poker_card.define_card(CardColor.SPADES, CardNumber.TWO)
        self.assertEqual(test_poker_card.get_number().value.get_value(), [2])

    def test_card_value_get_number_name(self):
        test_poker_card = PokerCard()
        test_poker_card.define_card(CardColor.SPADES, CardNumber.TWO)
        self.assertEqual(test_poker_card.get_number().value.get_name(), "Two")

    def test_card_value_get_color_value(self):
        test_poker_card = PokerCard()
        test_poker_card.define_card(CardColor.SPADES, CardNumber.TWO)
        self.assertEqual(test_poker_card.get_color().value.get_value(), 0)

    def test_card_value_get_color_name(self):
        test_poker_card = PokerCard()
        test_poker_card.define_card(CardColor.SPADES, CardNumber.TWO)
        self.assertEqual(test_poker_card.get_color().value.get_name(), "Spades")

    def test_card_ace_get_max_val(self):
        test_poker_card = PokerCard()
        test_poker_card.define_card(CardColor.SPADES, CardNumber.ACE)
        self.assertEqual(test_poker_card.get_number().value.get_highest_value(), 14)

    def test_draw_top_card(self):
        test_poker_deck = PokerDeck()
        test_poker_deck.generate_deck()
        top_card = test_poker_deck.get_deck()[0]
        drawn_top_card = test_poker_deck.draw_top_card()
        self.assertEqual(top_card.get_number().value.get_value(), drawn_top_card.get_number().value.get_value())
        self.assertEqual(top_card.get_color().value.get_value(), drawn_top_card.get_color().value.get_value())

    def test_build_deck_dict(self):
        test_poker_deck = PokerDeck()
        test_poker_deck.generate_deck()
        print(json.dumps(test_poker_deck.get_dict()))

    def test_deserialize_deck(self):
        with open('test_cases/test_deserialize_deck.json') as json_file:
            data = json.load(json_file)
        test_poker_deck = PokerDeck()
        test_poker_deck.generate_deck_from_dict(data)
        self.assertEqual(test_poker_deck.get_deck()[0].get_number().value.get_name(), "Two")
        self.assertEqual(test_poker_deck.get_deck()[1].get_number().value.get_name(), "Three")
        self.assertEqual(test_poker_deck.get_deck()[2].get_number().value.get_name(), "Four")
        self.assertEqual(test_poker_deck.get_deck()[3].get_number().value.get_name(), "Five")
        self.assertEqual(test_poker_deck.get_deck()[4].get_number().value.get_name(), "Six")

    def test_deserialize_deck_goes_wrong(self):
        with open('test_cases/test_deserialize_deck.json') as json_file:
            data = json.load(json_file)
        test_poker_deck = PokerDeck()
        test_poker_deck.generate_deck_from_dict(data)
        self.assertNotEqual(test_poker_deck.get_deck()[0].get_number().value.get_name(), "Jack")
        self.assertNotEqual(test_poker_deck.get_deck()[1].get_number().value.get_name(), "King")
        self.assertNotEqual(test_poker_deck.get_deck()[2].get_number().value.get_name(), "Queen")
        self.assertNotEqual(test_poker_deck.get_deck()[3].get_number().value.get_name(), "Nine")
        self.assertNotEqual(test_poker_deck.get_deck()[4].get_number().value.get_name(), "Two")

    def test_poker_royal_flush_on_board(self):
        with open('test_cases/royal_flush.json') as json_file:
            data = json.load(json_file)
        test_poker_round = PokerRound(5, 2)
        test_poker_round.prepare_round_with_prepared_deck(data)
        test_poker_round.initiate_round()
        test_poker_round.deal_board()
        self.assertEqual(test_poker_round.get_board()[0].get_number().value.get_name(), "Ace")
        self.assertEqual(test_poker_round.get_board()[1].get_number().value.get_name(), "King")
        self.assertEqual(test_poker_round.get_board()[2].get_number().value.get_name(), "Queen")
        self.assertEqual(test_poker_round.get_board()[3].get_number().value.get_name(), "Jack")
        self.assertEqual(test_poker_round.get_board()[4].get_number().value.get_name(), "Ten")
        self.assertEqual(test_poker_round.get_board()[0].get_color().value.get_name(), "Spades")
        self.assertEqual(test_poker_round.get_board()[1].get_color().value.get_name(), "Spades")
        self.assertEqual(test_poker_round.get_board()[2].get_color().value.get_name(), "Spades")
        self.assertEqual(test_poker_round.get_board()[3].get_color().value.get_name(), "Spades")
        self.assertEqual(test_poker_round.get_board()[4].get_color().value.get_name(), "Spades")

    def test_poker_street_combination(self):
        with open('test_cases/ace_high_street.json') as json_file:
            data = json.load(json_file)
        test_poker_round = PokerRound(5, 2)
        test_poker_round.prepare_round_with_prepared_deck(data)
        test_poker_round.initiate_round()
        test_poker_round.deal_board()
        test_combo_checker = CombinationChecker(test_poker_round.get_board(), test_poker_round.players[0].get_hand())
        test_combo_checker.get_all_straights(3)
        rank = test_combo_checker.get_combination()[0].get_rank().value.get_value()
        highest_card = test_combo_checker.get_combination()[0].get_value()
        self.assertEqual(rank, 5)
        self.assertEqual(highest_card, [1, 14])

    def test_poker_flush_combination(self):
        with open('test_cases/ace_high_street.json') as json_file:
            data = json.load(json_file)
        test_poker_round = PokerRound(5, 2)
        test_poker_round.prepare_round_with_prepared_deck(data)
        test_poker_round.initiate_round()
        test_poker_round.deal_board()
        test_combo_checker = CombinationChecker(test_poker_round.get_board(), test_poker_round.players[0].get_hand())
        test_combo_checker.check_for_flush()
        self.assertEqual(test_combo_checker.combinations[0].get_rank().value.get_value(), 6)
        self.assertEqual(test_combo_checker.combinations[0].get_value(), [1, 14])

    def test_poker_number_of_equivalents(self):
        with open('test_cases/pocket_nine.json') as json_file:
            data = json.load(json_file)
        test_poker_round = PokerRound(5, 2)
        test_poker_round.prepare_round_with_prepared_deck(data)
        test_poker_round.initiate_round()
        test_poker_round.deal_board()
        test_combo_checker = CombinationChecker(test_poker_round.get_board(), test_poker_round.players[0].get_hand())
        test_combo_checker.set_equivalents()
        print(test_combo_checker.combinations[0].get_rank().value.get_value())
        print(test_combo_checker.combinations[0].get_value())
        print(test_combo_checker.combinations[1].get_rank().value.get_value())
        print(test_combo_checker.combinations[1].get_value())
        print(test_poker_round.players[0].describe_hand())
        print(test_poker_round.describe_board())

    def test_poker_round_combination_recognition(self):
        test_poker_round = PokerRound(5, 2)
        test_poker_round.prepare_round()
        test_poker_round.initiate_round()
        test_poker_round.deal_board()
        test_combo_checker = CombinationChecker(test_poker_round.get_board(), test_poker_round.players[0].get_hand())
        test_combo_checker.set_equivalents()
        test_combo_checker.check_for_flush()
        test_combo_checker.get_all_straights(3)
        for equivalent_combo in test_combo_checker.combinations:
            print(equivalent_combo.get_rank(), equivalent_combo.get_value())
        print(test_poker_round.players[0].describe_hand())
        print(test_poker_round.describe_board())
