import random

#Will simulate the experience of playing blackjack in the casino right in the terminal of the computer

#Class for the cards in the game
class Card():
    card_values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11}
    card_suits = ["♣", "♠", "♦", "♥"]
    def __init__(self, title, suit):
        self.title = title
        self.suit = suit
        self.value = Card.card_values[self.title]

    #String representation of Card
    def __str__(self):
        return self.title + self.suit
    
#Class for the players of the game
class Player(): 
    def __init__(self):
        self.name = "Name"
        self.hand = []
        self.hand_value = 0
        self.chips = 0
        self.bet = 0
        self.earnings = 0

#Class that will actually be used to play the game of blackjack
class Game():

    def __init__(self, num_decks=1):
        self.num_players = 0
        self.num_decks = num_decks
        self.round_num = 0
        self.players = []
        self.eliminated_players = []
        #Sets up ordered deck for easy shuffling
        self.ordered_deck = []
        for n in range(self.num_decks):
            for card_title in Card.card_values.keys():
                for card_suit in Card.card_suits:
                    self.ordered_deck.append(Card(card_title, card_suit))
        #Shuffles deck one card at a time to create playing deck
        self.playing_deck = self.shuffle_deck()
        self.num_decks = num_decks

    #Function to shuffle playing deck(s)
    def shuffle_deck(self):
        new_shuffle = []
        cards_to_shuffle = self.ordered_deck.copy()
        while len(cards_to_shuffle) > 0:
            new_shuffle.append(cards_to_shuffle.pop(random.randint(0, len(cards_to_shuffle) - 1)))
        return new_shuffle

    def play(self):

        #Series of helper methods to call throughout the game

        #Asks for and sets number of players in the game; must be between 1 and 8
        def set_num_players():
            while True:
                try:
                    num_players = round(int(input("Welcome to the Grand Python Casino! The game today is Blackjack. How many players will be playing? Please enter a number between 1 and 8.\n")))
                except ValueError:
                    print("I'm sorry, I don't recognize this as a whole number. Please try again.\n")
                if num_players >= 1 and num_players <= 8:
                    break
                else:
                    print("I'm sorry, there is a minimum of 1 player and a maximum of 8 at this table. Please try again.\n")
            return num_players

        #Creates player list
        def set_players(num_players):
            players = []
            for i in range(1, num_players + 1):
                players.append(Player())
            #Adds dealer
            players.append(Player())
            players[-1].name = "Dealer"

            return players

        def get_names(players):
            #Sets name for each player in the game (except for the dealer)
            player_names = ["dealer"]
            #Counter for player number
            i = 1
            for player in players[:-1]:
                while True:
                    new_name = input(f"\nPlayer {i}, what is your name? If you would like me to just call you player {i}, just press enter without typing anything.\n")
                    if new_name != "" and (new_name.lower() not in player_names):
                        player.name = new_name
                        i += 1
                        break
                    elif new_name == "":
                        player.name = f"Player {i}"
                        i += 1
                        break
                    else:
                        print(f"I'm sorry, that name has already been taken. Please try again.\n")
                print(f"Okay, {player.name}, glad to have you.\n")
                player_names.append(new_name.lower())

        #Collects chip buy-in from each player (except for the dealer)
        def collect_buyin(players):
            for player in players[:-1]:
                while True:
                    try:
                        num_chips = round(int(input(f"{player.name}, what's your buy-in?\n")))
                        if num_chips <= 0:
                            print("I'm sorry, your buy-in must be a whole number greater than 0. Please try again.\n")
                        else:
                            player.chips = num_chips
                            break
                    except ValueError:
                        print("I'm sorry, your buy-in must be a whole number greater than 0. Please try again.\n")
                print(f"\n{player.chips} chips it is for you, {player.name}!\n")
        
        #Collects bets from each player (except for the dealer): must be a whole number greater than 0 and less than or equal to the number of chips the player has remaining
        def collect_bets(players):
            for player in players[:-1]:
                while True:
                    try:
                        round_bet = round(int(input(f"{player.name}, What is your bet? (Current Balance = {player.chips} chips)\n")))
                        if round_bet > player.chips:
                            print(f"I'm sorry, you can't bet more chips than you have. Please try again.\n")
                        #If input is valid, adds chips to bet and removes them from chip balance
                        else:
                            player.bet = round_bet
                            player.chips -= player.bet
                            break
                    except ValueError:
                        print("I'm sorry, your bet must be a whole number greater than 0. Please try again.\n")
                print(f"\n{player.bet} chips on the table for you, {player.name}. Good luck!\n")
        
        #Deals cards to all players in the game, including the dealer, removing them from the top of the shuffled deck
        def deal_cards(players):
            #Each player starts with two cards
            for i in range(2):
                for player in players:
                    new_card = self.playing_deck.pop(0)
                    player.hand.append(new_card)
                    player.hand_value += new_card.value
            
            #Reshuffles deck at a minimum point, depending on the number players and number of decks
            if len(self.playing_deck) < (len(players)) * 6 * self.num_decks:
                print("Low on cards. Reshuffling the deck...")
                self.playing_deck = self.shuffle_deck()
                print("Done.\n")



        #Game flow
        #Sets number of players
        self.num_players = set_num_players()
        print(f"\nSo that's {self.num_players} players. Count the dealer and we'll have {self.num_players + 1} in total.")

        #Initializes player list
        self.players = set_players(self.num_players)
        
        #Collects player names
        get_names(self.players)

        #Collects chip buy-ins
        print("\n\nNow that we have your names, it's time to collect your buy-ins. We'll go around the table, player by player. You can start with as many chips as you want, as long as it's a whole number and it's more than zero.\n")
        
        collect_buyin(self.players)

        print("\n\nNow that all of that's out of the way, let's finally play the game!")

        #Game continues until there are no players left
        while len(self.players) > 0:
            self.round_num += 1
            print(f"\nBeginning Round {self.round_num}...\n")
            
            #Collects bets
            print("\n\n\nTime to collect the bets for the round.\n")
            collect_bets(self.players)

            #Each player is dealt their cards, including the dealer. the dealer's second card is hidden from all of the players
            print("\nTime to deal the cards.\n")
            deal_cards(self.players)
            #Displays hands and bets

            for player in self.players:
                if(player.name != "Dealer"):
                    print(f"{player.name} (Bet = {player.bet}):    {player.hand[0]}  {player.hand[1]}    Current Score = {player.hand_value}")
                else:
                    print(f"{player.name}:    {player.hand[0]}  ??     Current Score = {player.hand_value - player.hand[1].value}")

            #Each player gets their opportunity to decide what to do: hit or stay. If they go over 21, they bust and their turn is immediately over; otherwise, they continue until they decide to stay

            #Dealer plays out their hand according to rules: must hit if value is under 17; otherwise, must stay

            #Chip balances are adjusted for each player according to whether or not they beat the dealer in that round. In the event of a tie score (as long as the player has NOT busted), the player simply gets back the chips that they bet

            #Each player is asked whether they would like to continue. Players who have been reduced to 0 chips have the option to buy back in with new chips, but their overall balance is still tracked. Players who elect to leave the game are removed after being told their total earnings/losses, and the next round is played with the remaining players

            #The game continues until the last remaining player(s) elect to leave

test_game = Game()
test_game.play()
