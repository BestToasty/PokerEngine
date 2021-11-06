from poker_deck import PokerDeck
from poker_player import PokerPlayer
from combination_value import CombinationChecker
import json


class PokerRound:
    number_of_players = None
    number_of_cards = None
    players = []
    board = []
    deck = []
    combo_checker = None

    def __init__(self, player_count, card_count):
        self.number_of_players = player_count
        self.number_of_cards = card_count
        self.players = []
        self.board = []
        self.combo_checker = None

    def prepare_round_with_prepared_deck(self, json_deck_string):
        self.create_players()
        self.deck = PokerDeck()
        self.deck.generate_deck_from_dict(json_deck_string)

    def prepare_round(self):
        self.create_players()
        self.deck = PokerDeck()
        self.deck.generate_deck()
        self.deck.shuffle_deck()

    def initiate_round(self):
        self.deal_cards()

    def test_initiate_round(self):
        self.deal_cards()
        self.deal_board()
        self.combo_checker = CombinationChecker(self.get_players()[0].get_hand(), self.get_board())

    def create_players(self):
        for player in range(self.number_of_players):
            self.players.append(PokerPlayer(player))

    def describe_player_hands(self):
        hands_string = ""
        for player in self.players:
            hands_string += player.name + ": " + player.describe_hand() + "\n"
        return hands_string

    def describe_board(self):
        board_string = "Board: "
        for card in self.board:
            board_string += card.description + ", "
        return board_string

    def deal_cards(self):
        for card in range(self.number_of_cards):
            for player in self.players:
                player.draw_card(self.deck)

    def get_player_count(self):
        return len(self.players)

    def deal_flop(self):
        self.deck.draw_top_card()
        for i in range(3):
            card = self.deck.draw_top_card()
            self.board.append(card)

    def deal_turn(self):
        self.deck.draw_top_card()
        card = self.deck.draw_top_card()
        self.board.append(card)

    def deal_river(self):
        self.deck.draw_top_card()
        card = self.deck.draw_top_card()
        self.board.append(card)

    def deal_board(self):
        self.deal_flop()
        self.deal_turn()
        self.deal_river()

    def get_board(self):
        return self.board

    def get_deck(self):
        return self.deck

    def get_players(self):
        return self.players
