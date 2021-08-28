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
    def __repr__(self):
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
                    if num_players >= 1 and num_players <= 8:
                        break
                    else:
                        print("I'm sorry, there is a minimum of 1 player and a maximum of 8 at this table. Please try again.\n")
                except ValueError:
                    print("I'm sorry, I don't recognize this as a whole number. Please try again.\n")
            return num_players

        #Creates player list; dealer is always last player in list
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
                print(f"\nOkay, {player.name}, glad to have you.\n")
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
                        print("\nI'm sorry, your buy-in must be a whole number greater than 0. Please try again.\n")
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

        def print_hands(players, initial_deal=True):
            msg = "\n"
            for player in players:
                #Displays player name
                msg += f"{player.name} "

                #Displays bet
                if(player.name != "Dealer"):
                    msg += f"(Bet = {player.bet})"
                
                msg += ":  "
                #Displays cards (hides dealer's second card if not at end of round)
                for card in player.hand:
                    if card == player.hand[-1] and player.name == "Dealer" and initial_deal == True:
                        msg += "??  "
                    else:
                        msg += repr(card) + "  "

                #Displays current hand value
                if card == player.hand[-1] and player.name == "Dealer" and initial_deal == True:
                    msg += f"  Current Score = {player.hand_value - player.hand[-1].value}"
                else:
                    msg += f"  Current Score = {player.hand_value}"

                #Adds a couple of line breaks at the end
                msg += "\n"

            print(msg)

        #Player gets their opportunity to decide what to do: hit or stay. If they go over 21, they bust and their turn is immediately over; if they reach 21 exactly, they have a blackjack. Otherwise, they continue on until they decide to stay.
        def hit_or_stay(player):
            while True and player.hand_value < 21:
                response = input(f"{player.name}, Would you like to hit or stay? (hit/stay)\n")
                if response.lower() == "stay":
                    print(f"\n{player.name}, your score is {player.hand_value}.")
                    print_hands(self.players)
                    break
                elif response.lower() == "hit":
                    card_to_deal = self.playing_deck.pop(0)
                    player.hand.append(card_to_deal)
                    player.hand_value += card_to_deal.value
                    print(f"\n{player.name}, Your new card is {card_to_deal}, bringing your score to {player.hand_value}.")
                    print_hands(self.players)
                else:
                    print("\nCommand not recognized. Please try again.\n")

                if player.hand_value == 21:
                    print("\nBlackjack!\n")
                elif player.hand_value > 21:
                    print("\nBust!\n")

        #Dealer plays out their hand according to rules: must hit if value is under 17; otherwise, must stay
        def resolve_dealer(dealer):
            print(f"\nTime to reveal the dealer's card... it's {dealer.hand[-1]}!")
            print_hands(self.players, False)
            while dealer.hand_value < 17:
                card_to_deal = self.playing_deck.pop(0)
                dealer.hand.append(card_to_deal)
                dealer.hand_value += card_to_deal.value
                print(f"\nThe dealer flips over a new card... {card_to_deal}. The dealer's score is now {dealer.hand_value}.")
                print_hands(self.players, False)

            if dealer.hand_value == 21:
                print("Dealer Blackjack!\n")
            elif dealer.hand_value > 21:
                print("Dealer busts!\n")
            else:
                print(f"The dealer stays at a score of {dealer.hand_value}.")

        #Chip balances are adjusted for each player according to whether or not they beat the dealer in that round. In the event of a tie score (as long as the player has NOT busted), the player simply gets back the chips that they bet
        def resolve_round(players):
            winning_players = []
            losing_players = []
            push_players = []
            dealer = players[-1]
            for player in players[:-1]:
                if player.hand_value <= 21 and (player.hand_value > dealer.hand_value or dealer.hand_value > 21):
                    winning_players.append(player)
                elif player.hand_value < dealer.hand_value or player.hand_value > 21:
                    losing_players.append(player)
                else:
                    push_players.append(player)
                
            if len(winning_players) > 0:
                winning_msg = "\nWinning players:    "
                for player in winning_players:
                    winning_msg += player.name + f" (+{player.bet} chips)    "
                    #Winning players get their money back plus their profit in chips
                    player.chips += player.bet * 2
                    #Keeps track of players' overall earnings
                    player.earnings += player.bet
                winning_msg += "\n"
            else:
                winning_msg = "\nWinners: None :(\n"

            if len(losing_players) > 0:
                losing_msg = "\nLosing players:    "
                for player in losing_players:
                    losing_msg += player.name + f" (-{player.bet} chips)    "
                    #Losing player doesn't get their bet back, and overall earnings are adjusted downward
                    player.earnings -= player.bet
                losing_msg += "\n"
            else:
                losing_msg = "\nLosers: None :)\n"

            if len(push_players) > 0:
                push_msg = "\nPush players:    "
                for player in push_players:
                    push_msg += player.name + f" ({player.bet} chip bet returned)    "
                    #Push player gets their bet back
                    player.chips += player.bet
                push_msg += "\n"
            else:
                push_msg = "\nPush: None :/\n"
            
            print(winning_msg, losing_msg, push_msg)

        #Each player is asked whether they would like to continue. Players who have been reduced to 0 chips have the option to buy back in with new chips, but their overall balance is still tracked. Players who elect to leave the game are removed after being told their total earnings/losses, and the next round is played with the remaining players
        def continue_players(players):
            idx = 0
            for player in players:
                #Actions for players with chips remaining
                if player.chips > 0:
                    while True:
                        contin = input(f"\n{player.name}, your current balance is {player.chips}. Would you like to play another round? (yes/no)\n")
                        if contin.lower() == "yes":
                            idx += 1
                            #Resets player hands
                            player.hand = []
                            player.hand_value = 0
                            player.bet = 0
                            break
                        elif contin.lower() == "no":
                            #Removes player from active player list and adds them to eliminated player list
                            print(f"\nThanks for playing, {player.name}. Your total earnings in this game were {player.earnings} chips.\n")
                            self.eliminated_players.append(self.players.pop(idx))
                            idx += 1
                            break
                        else:
                            print("\nCommand not recognized. Please try again.\n")
                #Actions for players out of chips
                else:
                    while True:
                        contin = input(f"\n{player.name}, you are out of chips! Would you like to buy back in? (yes/no)\n")
                        if contin.lower() == "yes":
                            while True:
                                try:
                                    player.chips = int(input(f"\n{player.name}, How many chips would you like to buy back in with?\n"))
                                    if player.chips <= 0:
                                        print("\nI'm sorry, you must specify a postive whole number of chips. Please try again.\n")
                                    else:
                                        print(f"\nOkay {player.name}, you're back in with {player.chips} more chips!\n")
                                        idx += 1
                                        player.hand = []
                                        player.hand_value = 0
                                        player.bet = 0
                                        break
                                except ValueError:
                                    print("\nI'm sorry, you must specify a positive whole number of chips. Please try again.\n")
                            break
                        elif contin.lower() == "no":
                            #Removes player from active player list and adds them to eliminated player list
                            print(f"\nThanks for playing, {player.name}. Your total earnings in this game were {player.earnings} chips.\n")
                            self.eliminated_players.append(self.players.pop(idx))
                            idx += 1
                            break
                        else:
                            print("\nCommand not recognized. Please try again.\n")

        #Rotates player order for the next round, moving first player to the last position before the dealer, and everybody else forward one
        def rotate_players(players):
            if len(players) > 2:
                new_players_order = players[1:-1] + [players[0]]+ [players[-1]]
            else:
                new_players_order = players
            return new_players_order
            


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

        #Game continues until there are no players left (not counting the dealer)
        while len(self.players) > 1:
            self.round_num += 1
            #Reshuffles deck at a minimum point, depending on the number players and number of decks
            if len(self.playing_deck) < (len(self.players)) * 6 * self.num_decks:
                print("\nLow on cards. Reshuffling the deck...\n")
                self.playing_deck = self.shuffle_deck()
                print("Done.\n")

            print(f"\nBeginning Round {self.round_num}...\n")
            
            #Collects bets
            print("\nTime to collect the bets for the round.\n")
            collect_bets(self.players)

            #Each player is dealt their cards
            print("\nTime to deal the cards.\n")
            deal_cards(self.players)
            #Displays hands and bets

            print_hands(self.players)

            #Each player plays out their hand
            for player in self.players[:-1]:
                hit_or_stay(player)

            #Dealer resolves their hand
            resolve_dealer(self.players[-1])

            #Distributes winnings or takes bets at end of round
            print("\nResolving the bets...\n")
            resolve_round(self.players)
            
            #Asks each player whether they wish to play another round
            continue_players(self.players[:-1])

            #The game continues until the last remaining player(s) elect to leave
            if len(self.players) > 1:
                print("\nRotating deal order for the next round...\n")
                self.players = rotate_players(self.players)
                #resets dealer hand and score
                self.players[-1].hand = []
                self.players[-1].hand_value = 0
                print("\nDone.\n")
                print("\nOnto the next round!\n")

        #Once game is over, prints out summary of how each player performed

test_game = Game()
test_game.play()
