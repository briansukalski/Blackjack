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
    def shuffle_deck(self):
        new_shuffle = []
        cards_to_shuffle = self.ordered_deck.copy()
        while len(cards_to_shuffle) > 0:
            new_shuffle.append(cards_to_shuffle.pop(random.randint(0, len(cards_to_shuffle) - 1)))
        return new_shuffle

    #Deals cards to all players in the game, including the dealer, removing them from the top of the shuffled deck
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
            self.shuffled_deck = self.shuffle_deck()
        
        return player_hands

test_deck = Deck()

#Class that will actually be used to play the game of blackjack
class Game():

    def __init__(self, num_players=1, num_decks=1):
        self.num_players = num_players
        self.playing_deck = Deck(num_decks)
        
    def play(self):
        #Collects chip buy-in from each player and allows them to name themselves if they wish

        #At the beginning of each round, asks each player to make their bet; must be an integer, at least 1, and not more than the number of chips they have remaining

        #Each player is dealt their cards, including the dealer. the dealer's second card is hidden from all of the players

        #Each player gets their opportunity to decide what to do: hit or stay. If they go over 21, they bust and their turn is immediately over; otherwise, they continue until they decide to stay

        #Dealer plays out their hand according to rules: must hit if value is under 17; otherwise, must stay

        #Chip balances are adjusted for each player according to whether or not they beat the dealer in that round. In the event of a tie score (as long as the player has NOT busted), the player simply gets back the chips that they bet

        #Each player is asked whether they would like to continue. Players who have been reduced to 0 chips have the option to buy back in with new chips, but their overall balance is still tracked. Players who elect to leave the game are removed after being told their total earnings/losses, and the next round is played with the remaining players

        #The game continues until the last remaining player(s) elect to leave
print(test_deck.shuffled_deck)

print(test_deck.deal_cards(3))

print(test_deck.shuffled_deck)
