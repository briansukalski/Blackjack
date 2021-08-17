import random

#Will simulate the experience of playing blackjack in the casino right in the terminal of the computer

class Deck():
    card_values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11}
    card_suits = ["♣", "♠", "♦", "♥"]
    def __init__(self, num_decks=1):
        #Sets up ordered deck for easy shuffling
        self.ordered_deck = []
        index = 0
        for n in range(num_decks):
            for card in Deck.card_values.keys():
                for i in range(4):
                    self.ordered_deck.append(card + Deck.card_suits[i])
                index += 4
        #Shuffles deck one card at a time
        self.shuffled_deck = self.shuffle_deck(self.ordered_deck)
        self.num_decks = num_decks

    #Function to shuffle playing deck
    def shuffle_deck(self, starting_deck):
        new_shuffle = []
        cards_to_shuffle = starting_deck.copy()
        while len(cards_to_shuffle) > 0:
            new_shuffle.append(cards_to_shuffle.pop(random.randint(0, len(cards_to_shuffle) - 1)))
        return new_shuffle

    #Deals cards to all players in the game, including the dealer
    def deal_cards(self, num_players=1):

        player_hands = []
        #initializes hand lists
        for n in range(num_players + 1):
            player_hands.append([])
        #Each player starts with two cards
        for i in range(2):
            for n in range(num_players + 1):
                player_hands[n].append(self.shuffled_deck.pop(0))
        
        #Reshuffles deck at a minimum point, depending on the number players and number of decks
        if len(self.shuffled_deck) < (num_players + 1) * 6 * self.num_decks:
            self.shuffled_deck = self.shuffle_deck(self.ordered_deck)
        
        return player_hands

test_deck = Deck()

print(test_deck.shuffled_deck)

print(test_deck.deal_cards(3))

print(test_deck.shuffled_deck)
