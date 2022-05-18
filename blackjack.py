import random
import time
import sys
from dictionary_adder import add_dictionaries

card_values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11}
card_suits = ["♣", "♠", "♦", "♥"]

#Will simulate the experience of playing blackjack in the casino right in the terminal of the computer
def scroll_print(msg):
    time.sleep(0.25)
    for i in msg:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.01)
    time.sleep(0.25)

def scroll_input(msg):
    scroll_print(msg)
    return input("")

#Class for the cards in the game
class Card():
    def __init__(self, title, suit):
        self.title = title
        self.suit = suit
        self.value = card_values[self.title]

    #String representation of Card
    def __repr__(self):
        return self.title + self.suit

#Class for card deck
class Deck():
    def __init__(self, num_decks=1):
        self.num_decks = num_decks
        self.active_cards = []
        self.discarded_cards = []
        for i in range(num_decks):
            for value in card_values.keys():
                for suit in card_suits:
                    self.active_cards.append(Card(value, suit))

#Class for the players of the game
class Player(): 
    def __init__(self):
        self.name = "Name"
        self.hand = []
        self.hand_value = 0
        self.chips = 0
        self.bet = 0
        self.earnings = 0
        self.num_aces = 0
        self.rounds_played = 0
        self.buy_in = 0

#Class for calculating game probabilities
class Probability_Calculator():
    def __init__(self, num_decks):
        self.num_decks = num_decks
        self.value_counts = {2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0}
        self.total_unrevealed_cards = 0
        for i in range(num_decks):
            #Fills in total number of cards of each value in the playing deck
            for value in card_values.values():
                for suit in card_suits:
                    self.value_counts[value] += 1
                    self.total_unrevealed_cards += 1
                    
    def pop_card(self, value):
        #Simulates revealing a new card from the deck, meaning that card is no longer part of future probability calculations
        self.value_counts[value] -= 1
        self.total_unrevealed_cards -= 1

    def calculate_bust_probability(self, current_score, num_aces):
        bust_probability = 0
        #Can't bust if you're holding an unused ace, since aces are soft
        if num_aces > 0:
            return bust_probability
        #Tallies up the number of cards that will result in a bust
        else:
            for value in self.value_counts.keys():
                #Excludes aces from calculation, since aces are soft (you can't bust on a dealt ace)
                if value + current_score > 21 and value != 11:
                    bust_probability += self.value_counts[value] / self.total_unrevealed_cards

        return bust_probability

    def calculate_dealer_score_probabilities(self, current_score, num_aces, value_counts, total_unrevealed_cards):
        #Probabilities for all the possible next scores are stored in a dictionary
        new_score_probabilities = {4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0}

        #Loops through each possible card that could be drawn and processes depending on whether or not it will result in a bust
        for value in value_counts:
            #Checks for ace
            if value == 11:
                num_aces += 1
            #Applies new value
            new_score = current_score + value
            #Applies soft ace to prevent bust if available
            if new_score > 21:
                if num_aces > 0:
                    new_score -= 10
                    num_aces -= 1
            #If value goes over 21, results in a bust and probability
            if new_score > 21:
                #Adds probability of drawing particular value to bust probability (since current value will result in a bust)
                new_score_probabilities[22] += value_counts[value] / total_unrevealed_cards
            #Values between 17 and 21 will result in the dealer staying and won't affect bust probability
            #If value is between 17 and 21, results in the dealer holding and probability is added
            elif 17 <= new_score <= 21:
                new_score_probabilities[new_score] += value_counts[value] / total_unrevealed_cards
            #If value is under 17, recursively calls function to simulate continuing to have the dealer play until they reach at least 17 as a score
            else:
                #Sets up recursive variables so that function can be called recursively without interfering with function's variables
                recursive_value_counts = value_counts.copy()
                recursive_value_counts[value] -= 1
                recursive_total_unrevealed_cards = total_unrevealed_cards
                recursive_total_unrevealed_cards -= 1
                recursive_probability_factor = value_counts[value] / total_unrevealed_cards
                add_dictionaries(new_score_probabilities, self.calculate_dealer_score_probabilities(new_score, num_aces, recursive_value_counts, recursive_total_unrevealed_cards), recursive_probability_factor)
        
        return new_score_probabilities

#Class that will actually be used to play the game of blackjack
class Game():

    def __init__(self, num_decks=1):
        self.num_players = 0
        self.num_decks = num_decks
        self.round_num = 0
        self.players = []
        self.all_players = []
        #Sets up ordered deck for easy shuffling
        self.ordered_deck = []
        for n in range(self.num_decks):
            for card_title in card_values.keys():
                for card_suit in card_suits:
                    self.ordered_deck.append(Card(card_title, card_suit))
        #Shuffles deck one card at a time to create playing deck
        self.playing_deck = self.shuffle_deck()
        self.num_decks = num_decks
        #Sets up probability calculator to provide dynamic probability calculations throughout the game
        self.probabilties = Probability_Calculator(self.num_decks)

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
                    num_players = round(int(scroll_input("Welcome to the Grand Python Casino! The game today is Blackjack. How many players will be playing? Please enter a number between 1 and 8.\n")))
                    if num_players >= 1 and num_players <= 8:
                        break
                    else:
                        scroll_print("I'm sorry, there is a minimum of 1 player and a maximum of 8 at this table. Please try again.\n")
                except ValueError:
                    scroll_print("I'm sorry, I don't recognize this as a whole number. Please try again.\n")
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
                    new_name = scroll_input(f"\nPlayer {i}, what is your name? If you would like me to just call you player {i}, just press enter without typing anything.\n")
                    if new_name != "" and (new_name.lower() not in player_names):
                        player.name = new_name
                        i += 1
                        break
                    elif new_name == "":
                        player.name = f"Player {i}"
                        i += 1
                        break
                    else:
                        scroll_print(f"I'm sorry, that name has already been taken. Please try again.\n")
                scroll_print(f"\nOkay, {player.name}, glad to have you.\n")
                player_names.append(new_name.lower())

        #Collects chip buy-in from each player (except for the dealer)
        def collect_buyin(players):
            for player in players[:-1]:
                while True:
                    try:
                        num_chips = round(int(scroll_input(f"\n{player.name}, what's your buy-in?\n")))
                        if num_chips <= 0:
                            scroll_print("I'm sorry, your buy-in must be a whole number greater than 0. Please try again.\n")
                        else:
                            player.buy_in += num_chips
                            player.chips = num_chips
                            break
                    except ValueError:
                        scroll_print("\nI'm sorry, your buy-in must be a whole number greater than 0. Please try again.\n")
                scroll_print(f"\n{player.chips} chips it is for you, {player.name}!\n")
        
        #Collects bets from each player (except for the dealer): must be a whole number greater than 0 and less than or equal to the number of chips the player has remaining
        def collect_bets(players):
            for player in players[:-1]:
                while True:
                    try:
                        round_bet = round(int(scroll_input(f"\n{player.name}, What is your bet? (Current Balance = {player.chips} chips)\n")))
                        if round_bet > player.chips:
                            scroll_print(f"I'm sorry, you can't bet more chips than you have. Please try again.\n")
                        #If scroll_input is valid, adds chips to bet and removes them from chip balance
                        else:
                            player.bet = round_bet
                            player.chips -= player.bet
                            break
                    except ValueError:
                        scroll_print("I'm sorry, your bet must be a whole number greater than 0. Please try again.\n")
                scroll_print(f"\n{player.bet} chips on the table for you, {player.name}. Good luck!\n")
        
        #Deals cards to all players in the game, including the dealer, removing them from the top of the shuffled deck
        def deal_card(player):
            #Player is dealt a single card from the top of the deck
                new_card = self.playing_deck.pop(0)
                if new_card.title == "A":
                    player.num_aces += 1
                player.hand.append(new_card)
                player.hand_value += new_card.value
                #Adjusts probability calculator, removing newly-dealt card, unless the card is the dealer's second card, which is not initially revealed
                if not(player.name == "Dealer" and len(player.hand) == 2):
                    self.probabilities.pop_card(new_card.value)
                #Aces are soft; their value switches from 11 to 1 if the player busts
                if player.hand_value > 21 and player.num_aces > 0:
                    player.hand_value -= 10
                    player.num_aces -= 1


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

                #Adds a line break at the end for each player
                msg += "\n"
            
            #Adds a couple of line breaks at the end of the printout
            msg += "\n\n"

            scroll_print(msg)

        #Player gets their opportunity to decide what to do: hit or stay. If they go over 21, they bust and their turn is immediately over; if they reach 21 exactly, they have a blackjack. Otherwise, they continue on until they decide to stay.
        def hit_or_stay(player):
            while True and player.hand_value < 21:
                response = scroll_input(f"{player.name}, Would you like to hit or stay? (hit/stay)\n")
                if response.lower() == "stay":
                    scroll_print(f"\n{player.name}, your score is {player.hand_value}.")
                    print_hands(self.players)
                    break
                elif response.lower() == "hit":
                    deal_card(player)
                    scroll_print(f"\n{player.name}, Your new card is {player.hand[-1]}, bringing your score to {player.hand_value}.")
                    print_hands(self.players)
                else:
                    scroll_print("\nCommand not recognized. Please try again.\n")

                if player.hand_value == 21:
                    scroll_print("\nBlackjack!\n")
                elif player.hand_value > 21:
                    scroll_print("\nBust!\n")

        #Dealer plays out their hand according to rules: must hit if value is under 17; otherwise, must stay
        def resolve_dealer(dealer):
            scroll_print(f"\nTime to reveal the dealer's card... it's {dealer.hand[-1]}!")
            #Removes newly-revealed card from probability calculator
            self.probabilities.pop_card(dealer.hand[-1].value)

            print_hands(self.players, False)
            while dealer.hand_value < 17:
                deal_card(dealer)
                scroll_print(f"\nThe dealer flips over a new card... {dealer.hand[-1]}. The dealer's score is now {dealer.hand_value}.")
                print_hands(self.players, False)

            if dealer.hand_value == 21:
                scroll_print("Dealer Blackjack!\n")
            elif dealer.hand_value > 21:
                scroll_print("Dealer busts!\n")
            else:
                scroll_print(f"The dealer stays at a score of {dealer.hand_value}.")

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
                player.rounds_played += 1

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

            final_msg = winning_msg + losing_msg + push_msg
            
            scroll_print(final_msg)

        #Each player is asked whether they would like to continue. Players who have been reduced to 0 chips have the option to buy back in with new chips, but their overall balance is still tracked. Players who elect to leave the game are removed after being told their total earnings/losses, and the next round is played with the remaining players
        def continue_players(players):
            idx = 0
            for player in players:
                #Actions for players with chips remaining
                if player.chips > 0:
                    while True:
                        contin = scroll_input(f"\n{player.name}, your current balance is {player.chips}. Would you like to play another round? (yes/no)\n")
                        if contin.lower() == "yes":
                            idx += 1
                            #Resets player hands
                            player.hand = []
                            player.hand_value = 0
                            player.bet = 0
                            break
                        elif contin.lower() == "no":
                            #Removes player from active player list; they will remain in the all players list
                            scroll_print(f"\nThanks for playing, {player.name}. Your total earnings in this game were {player.earnings} chips.\n")
                            self.players.pop(idx)
                            idx += 1
                            break
                        else:
                            scroll_print("\nCommand not recognized. Please try again.\n")
                #Actions for players out of chips
                else:
                    while True:
                        contin = scroll_input(f"\n{player.name}, you are out of chips! Would you like to buy back in? (yes/no)\n")
                        if contin.lower() == "yes":
                            while True:
                                try:
                                    player.chips = int(scroll_input(f"\n{player.name}, How many chips would you like to buy back in with?\n"))
                                    if player.chips <= 0:
                                        scroll_print("\nI'm sorry, you must specify a postive whole number of chips. Please try again.\n")
                                    else:
                                        scroll_print(f"\nOkay {player.name}, you're back in with {player.chips} more chips!\n")
                                        idx += 1
                                        player.hand = []
                                        player.hand_value = 0
                                        player.bet = 0
                                        break
                                except ValueError:
                                    scroll_print("\nI'm sorry, you must specify a positive whole number of chips. Please try again.\n")
                            break
                        elif contin.lower() == "no":
                            #Removes player from active player list; they will remain in the all players list
                            scroll_print(f"\nThanks for playing, {player.name}. Your total earnings in this game were {player.earnings} chips.\n")
                            self.players.pop(idx)
                            idx += 1
                            break
                        else:
                            scroll_print("\nCommand not recognized. Please try again.\n")

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
        scroll_print(f"\nSo that's {self.num_players} players. Count the dealer and we'll have {self.num_players + 1} in total.\n")

        #Initializes player list
        self.players = set_players(self.num_players)
        self.all_players = self.players[:-1]
        
        #Collects player names
        get_names(self.players)

        #Collects chip buy-ins
        scroll_print("\n\nNow that we have your names, it's time to collect your buy-ins. We'll go around the table, player by player. You can start with as many chips as you want, as long as it's a whole number and it's more than zero.\n")
        
        collect_buyin(self.players)

        scroll_print("\n\nNow that all of that's out of the way, let's finally play the game!")

        #Game continues until there are no players left (not counting the dealer)
        while len(self.players) > 1:
            self.round_num += 1
            #Reshuffles deck at a minimum point, depending on the number players and number of decks
            if len(self.playing_deck) < (len(self.players)) * 6 * self.num_decks:
                scroll_print("\nLow on cards. Reshuffling the deck...\n")
                self.playing_deck = self.shuffle_deck()
                #Also resets probability calculator
                self.probabilities = Probability_Calculator(self.num_decks)
                scroll_print("Done.\n")

            scroll_print(f"\nBeginning Round {self.round_num}...\n")
            
            #Collects bets
            scroll_print("\nTime to collect the bets for the round.\n")
            collect_bets(self.players)

            #Each player is dealt their cards
            scroll_print("\nTime to deal the cards.\n")
            for i in range(2):
                for player in self.players:
                    deal_card(player)

            #Displays hands and bets

            print_hands(self.players)

            #Each player plays out their hand
            for player in self.players[:-1]:
                hit_or_stay(player)

            #Dealer resolves their hand
            resolve_dealer(self.players[-1])

            #Distributes winnings or takes bets at end of round
            scroll_print("\nResolving the bets...\n")
            resolve_round(self.players)
            
            #Asks each player whether they wish to play another round
            continue_players(self.players[:-1])

            #The game continues until the last remaining player(s) elect to leave
            if len(self.players) > 1:
                scroll_print("\nRotating deal order for the next round...\n")
                self.players = rotate_players(self.players)
                #resets dealer hand and score
                self.players[-1].hand = []
                self.players[-1].hand_value = 0
                scroll_print("\nDone.\n")
                scroll_print("\nOnto the next round!\n")

        #Once game is over, prints out summary of how each player performed
        scroll_print("\nThat was fun! Let's see how everyone did today...\n")
        for player in self.all_players:
            if player.earnings >= 0:
                winnings = f"won {player.earnings}"
            else:
                winnings = f"lost {-player.earnings}"

            if player.earnings / player.buy_in <= -0.5:
                comment = "Hope that wasn't your life savings!"
            elif player.earnings / player.buy_in <= -0.2:
                comment = "Better luck next time."
            elif player.earnings / player.buy_in < 0:
                comment = "Not your best day, but it could have been a lot worse."
            elif player.earnings / player.buy_in == 0:
                comment = "You know gambling usually involves taking risks, right?"
            elif player.earnings / player.buy_in < 0.2:
                comment = "Got yourself a little extra spending money!"
            elif player.earnings / player.buy_in < 1:
                comment = "Congratulations!"
            elif player.earnings / player.buy_in < 3:
                comment = "Wow, looks like drinks are on you!"
            else:
                comment = "I'm sorry, but you will no longer be welcome at this table."

            scroll_print(f"\n{player.name}, you played {player.rounds_played} rounds of blackjack today, and overall you {winnings} chips against a total buy-in of {player.buy_in}. {comment}\n")

# test_game = Game()
# test_game.play()
# test_deck = Deck(1)
test_p_c = Probability_Calculator(1)
print(test_p_c.value_counts, test_p_c.total_unrevealed_cards)
test_p_c.value_counts[2] -= 1
test_p_c.total_unrevealed_cards -= 1
print(2, test_p_c.calculate_dealer_score_probabilities(2, 0, test_p_c.value_counts, test_p_c.total_unrevealed_cards))
test_p_c.value_counts[2] += 1
test_p_c.value_counts[3] -= 1
print(3, test_p_c.calculate_dealer_score_probabilities(3, 0, test_p_c.value_counts, test_p_c.total_unrevealed_cards))
test_p_c.value_counts[3] += 1
test_p_c.value_counts[4] -= 1
print(4, test_p_c.calculate_dealer_score_probabilities(4, 0, test_p_c.value_counts, test_p_c.total_unrevealed_cards))
test_p_c.value_counts[4] += 1
test_p_c.value_counts[5] -= 1
print(5, test_p_c.calculate_dealer_score_probabilities(5, 0, test_p_c.value_counts, test_p_c.total_unrevealed_cards))
test_p_c.value_counts[5] += 1
test_p_c.value_counts[6] -= 1
print(6, test_p_c.calculate_dealer_score_probabilities(6, 0, test_p_c.value_counts, test_p_c.total_unrevealed_cards))
test_p_c.value_counts[6] += 1
test_p_c.value_counts[7] -= 1
print(7, test_p_c.calculate_dealer_score_probabilities(7, 0, test_p_c.value_counts, test_p_c.total_unrevealed_cards))
test_p_c.value_counts[7] += 1
test_p_c.value_counts[8] -= 1
print(8, test_p_c.calculate_dealer_score_probabilities(8, 0, test_p_c.value_counts, test_p_c.total_unrevealed_cards))
test_p_c.value_counts[8] += 1
test_p_c.value_counts[9] -= 1
print(9, test_p_c.calculate_dealer_score_probabilities(9, 0, test_p_c.value_counts, test_p_c.total_unrevealed_cards))
test_p_c.value_counts[9] += 1
test_p_c.value_counts[10] -= 1
print(10, test_p_c.calculate_dealer_score_probabilities(10, 0, test_p_c.value_counts, test_p_c.total_unrevealed_cards))
test_p_c.value_counts[10] += 1
test_p_c.value_counts[11] -= 1
print(11, test_p_c.calculate_dealer_score_probabilities(11, 1, test_p_c.value_counts, test_p_c.total_unrevealed_cards))
test_p_c.value_counts[11] += 1