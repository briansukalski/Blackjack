import random

#Will simulate the experience of playing blackjack in the casino right in the terminal of the computer

class Deck():
    card_values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11}

    def __init__(self):
        #Initializes ordered deck
        blank_deck = []
        index = 0
        for card in Deck.card_values.keys():
            for i in range(4):
                blank_deck.append(card)
            index += 4
        ordered_deck = blank_deck
        #Shuffles deck one card at a time
        self.shuffled_deck = []
        while len(ordered_deck) > 0:
            self.shuffled_deck.append(ordered_deck.pop(random.randint(0, len(ordered_deck) - 1)))
        
        self.discarded_cards = []
        
test_deck = Deck()

print(test_deck.shuffled_deck)
