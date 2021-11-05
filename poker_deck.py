import json
from enum import Enum
import random


class CardColorValue:
    name = None
    value = None

    def __init__(self, name, value):
        self.value = value
        self.name = name

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value


class CardColor(Enum):
    SPADES = CardColorValue("Spades", 0)
    HEARTS = CardColorValue("Hearts", 1)
    CLUBS = CardColorValue("Clubs", 2)
    DIAMONDS = CardColorValue("Diamonds", 3)


class CardNumberValue:
    name = None
    value = None

    def __init__(self, name, value):
        self.value = value
        self.name = name

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def get_highest_value(self):
        value = max(self.value)
        return value

    def is_value(self, value):
        return value in self.value


class CardNumber(Enum):
    TWO = CardNumberValue("Two", [2])
    THREE = CardNumberValue("Three", [3])
    FOUR = CardNumberValue("Four", [4])
    FIVE = CardNumberValue("Five", [5])
    SIX = CardNumberValue("Six", [6])
    SEVEN = CardNumberValue("Seven", [7])
    EIGHT = CardNumberValue("Eight", [8])
    NINE = CardNumberValue("Nine", [9])
    TEN = CardNumberValue("Ten", [10])
    JACK = CardNumberValue("Jack", [11])
    QUEEN = CardNumberValue("Queen", [12])
    KING = CardNumberValue("King", [13])
    ACE = CardNumberValue("Ace", [1, 14])


class PokerDeck:
    deck = []

    def __init__(self):
        self.deck = []

    def generate_deck(self):
        for color in CardColor:
            for number in CardNumber:
                poker_card = PokerCard()
                poker_card.define_card(color, number)
                self.deck.append(poker_card)

    def generate_deck_from_dict(self, json_dict):
        deck_dict = json_dict
        for card in deck_dict:
            card_dict = deck_dict[card]
            poker_card = PokerCard()
            poker_card.define_card_from_json(json.dumps(card_dict))
            self.deck.append(poker_card)

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def get_deck_string(self):
        deck_string = ""
        for card in self.deck:
            deck_string += card.description + "\n"
        return deck_string

    def get_current_stack_size(self):
        return len(self.deck)

    def draw_top_card(self):
        top_card = self.deck[0]
        self.deck.pop(0)
        return top_card

    def get_deck(self):
        return self.deck

    def get_dict(self):
        deck_dict = {}
        for idx, card in enumerate(self.deck):
            deck_dict[idx] = card.get_dict()
        return deck_dict

    def to_json(self):
        return json.dumps(self.get_dict())


class PokerCard:
    json_string = ''
    number = None
    color = None
    description = ""

    def __init__(self):
        self.color = None
        self.number = None
        self.description = None

    def define_card_from_json(self, json_string):
        self.json_string = json_string
        self.color = self.color_from_json(json_string)
        self.number = self.number_from_json(json_string)
        self.description = self.description_from_json(json_string)

    def get_number(self):
        return self.number

    def get_color(self):
        return self.color

    def get_description(self):
        return self.description

    def define_card(self, color, number):
        self.color = color
        self.number = number
        self.description = number.value.get_name() + " of " + color.name

    def get_dict(self):
        return {
            "number": {
                "name": self.number.name
            },
            "color": self.color.name,
            "description": self.description
        }

    def to_json(self):
        return json.dumps(self.get_dict())

    def number_from_json(self, json_string):
        card_dict = json.loads(json_string)
        return CardNumber[card_dict["number"]["name"]]

    def color_from_json(self, json_string):
        card_dict = json.loads(json_string)
        return CardColor[card_dict["color"]]

    def description_from_json(self, json_string):
        card_dict = json.loads(json_string)
        return card_dict["description"]
