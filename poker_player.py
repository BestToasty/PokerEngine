class PokerPlayer:
    name = None
    id = None
    hand = []

    def __init__(self, name):
        self.hand = []
        self.name = "Player " + str(name)
        self.id = name

    def draw_card(self, deck):
        card = deck.draw_top_card()
        self.hand.append(card)

    def describe_hand(self):
        hand_string = ""
        for card in self.hand:
            hand_string += card.description + ", "
        return hand_string

    def get_hand(self):
        return self.hand
