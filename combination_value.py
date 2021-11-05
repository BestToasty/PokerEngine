from enum import Enum


class CombinationItem:
    rank = None
    value = []

    def __init__(self, rank, value, color):
        self.rank = rank
        self.value = value
        self.color = color

    def get_rank(self):
        return self.rank

    def get_value(self):
        return self.value


class CombinationChecker:
    combination_cards = []
    combinations = []

    def __init__(self, board, hand):
        self.combination_cards = []
        self.combinations = []
        self.build_combination(board, hand)
        self.sort_combination()

    def build_combination(self, board, hand):
        for card in board:
            self.combination_cards.append(card)
        for card in hand:
            self.combination_cards.append(card)

    def get_all_straights(self, length_of_straight):
        amount_of_straights = len(self.combination_cards) - length_of_straight
        for card in self.combination_cards[:amount_of_straights]:
            if self.check_for_straight_below(card, length_of_straight):
                self.combinations.append(CombinationItem(Combinations.STRAIGHT, card.get_number().value.get_value(),
                                                         card.get_color().value.get_value()))

    def check_for_straight_below(self, card, straight_length):  # PROBLEM: Ace is only used as 14 not as 1
        value = card.number.value.get_highest_value()
        for i in range(straight_length):
            value -= 1
            if any(card.number.value.is_value(value) for card in self.combination_cards):
                pass
            else:
                return False

        return True

    def sort_combination(self):
        self.combination_cards.sort(key=self.sort_by_number, reverse=True)

    def get_combination(self):
        return self.combinations

    def sort_by_number(self, elem):
        return elem.number.value.get_highest_value()

    def count_the_colors(self):
        color_counter = ColorCounter()
        for card in self.combination_cards:
            color_counter.increment_dynamic(card.get_color().value.get_value(), 1)
        return color_counter

    def check_for_flush(self):
        counted_colors = self.count_the_colors()
        for color in range(3):
            if counted_colors.get_color_dynamic(color) >= 5:
                card = self.get_highest_color_card(color)
                self.combinations.append(CombinationItem(Combinations.FLUSH, card.get_number().value.get_value(),
                                                         card.get_color().value.get_value()))

    def get_highest_color_card(self, color):
        for card in self.combination_cards:
            if card.get_color().value.get_value() == color:
                return card

    def set_equivalents(self):
        for card in self.combination_cards:
            rank = Combinations.HIGH_CARD
            number_of_equivalents = self.check_for_equivalents(card)
            if number_of_equivalents == 1:  rank = Combinations.PAIR
            if number_of_equivalents == 2:  rank = Combinations.THREE_OF_A_KIND
            if number_of_equivalents == 3:  rank = Combinations.FOUR_OF_A_KIND
            if number_of_equivalents != 0:
                self.add_equivalents_to_combinations(rank, card.get_number().value.get_highest_value(),
                                                     card.get_color().value.get_value())

    def add_equivalents_to_combinations(self, rank, number, color):
        self.combinations.append(CombinationItem(rank, number, color))

    def check_for_equivalents(self, check_card):
        number_of_equivalents = 0
        clone_combination_cards = self.combination_cards
        clone_combination_cards.remove(check_card)
        for card in clone_combination_cards:
            if card.get_number().value.get_value() == check_card.get_number().value.get_value():
                number_of_equivalents += 1
        return number_of_equivalents

    def check_for_straight_flush(self):
        pass


class ColorCounter:
    spades = 0
    clubs = 0
    hearts = 0
    diamonds = 0

    def __init__(self):
        spades = 0
        clubs = 0
        hearts = 0
        diamonds = 0

    def increment_dynamic(self, color, value):
        if color == 0:
            self.increment_spades(value)
        if color == 1:
            self.increment_hearts(value)
        if color == 2:
            self.increment_clubs(value)
        if color == 3:
            self.increment_diamonds(value)

    def get_color_dynamic(self, color):
        if color == 0:
            return self.get_spades()
        if color == 1:
            return self.get_hearts()
        if color == 2:
            return self.get_clubs()
        if color == 3:
            return self.get_diamonds()

    def increment_spades(self, value):
        self.spades += value

    def increment_clubs(self, value):
        self.clubs += value

    def increment_hearts(self, value):
        self.hearts += value

    def increment_diamonds(self, value):
        self.diamonds += value

    def get_spades(self):
        return self.spades

    def get_clubs(self):
        return self.clubs

    def get_hearts(self):
        return self.hearts

    def get_diamonds(self):
        return self.diamonds


class CombinationValue:
    name = None
    value = None

    def __init__(self, name, value):
        self.value = value
        self.name = name

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value


class Combinations(Enum):
    ROYAL_FLUSH = CombinationValue("Royal Flush", 10)
    STRAIGHT_FLUSH = CombinationValue("Straight Flush", 9)
    FOUR_OF_A_KIND = CombinationValue("Four of a Kind", 8)
    FULL_HOUSE = CombinationValue("Full House", 7)
    FLUSH = CombinationValue("Flush", 6)
    STRAIGHT = CombinationValue("Straight", 5)
    THREE_OF_A_KIND = CombinationValue("Three of a Kind", 4)
    TWO_PAIR = CombinationValue("Two Pair", 3)
    PAIR = CombinationValue("Pair", 2)
    HIGH_CARD = CombinationValue("High Card", 1)
