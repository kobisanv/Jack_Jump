# Name       : Deck Creation and Scoring for Simulated Poker Game
# Programmer : Paul Kabbya
# Date       : April 12, 2022
# Description: Contains Card(), Deck(), Dealing(), and Scoring() classes

import random

class Card():
    overall = []

    def __init__(self, rank, suit, value):
        self.rank = rank
        self.suit = suit
        self.card_name = rank + ' of ' + suit #Build and store name
        self.value = value
        self.overall = [value, rank, suit, self.card_name]
        Card.overall.append(self.overall)

    def get_name(self):
        return Card.overall

    def get_value(self):
        return self.value

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

class Deck():
    SUIT_TUPLE = ("Diamonds", "Clubs", "Hearts", "Spades")
    # Dictionary maps each card rank to a value for a standard deck
    STANDARD_DICT = {"Ace":1, "2":2, "3":3, "4":4, "5":5,
                                  "6":6, "7":7, "8": 8, "9":9, "10":10,
                                  "Jack":11, "Queen":12, "King":13}

    def __init__(self):
        self.starting_deck_list = []
        self.playing_deck_list = []
        for suit in Deck.SUIT_TUPLE:
            for rank, value in Deck.STANDARD_DICT.items():
                new_card = Card(rank, suit, value)
                self.starting_deck_list.append(new_card.get_name())

    def shuffle(self):
        # Copy the starting deck and save it in the playing deck list
        self.playing_deck_list = self.starting_deck_list
        random.shuffle(self.playing_deck_list)

    def get_cards(self):
        if (len(self.playing_deck_list) == 0):
            print ("No more cards")
        # Pop one card off the deck and return it
        card_ref = self.playing_deck_list.pop()  
        return card_ref

#    def return_card(self, new_card):
    def return_card(self, card_ref):
        # Put a card back into the deck
#        self.playing_deck_list.insert(0, new_card)
        self.playing_deck_list.insert(0, card_ref)        

class Dealing():

    def __init__(self, shuffled):
        #This contains a shuffled deck
        self.deck = shuffled

    def single_deal(self):
        #Adds one card at a time
        dealt_card = self.deck.pop()
        if dealt_card in self.deck:
            self.deck.remove(dealt_card)
        return dealt_card

class Scoring():
    VALUE_DICT = {"Ace":1, "2":2, "3":3, "4":4, "5":5,
                                  "6":6, "7":7, "8": 8, "9":9, "10":10,
                                  "Jack":11, "Queen":12, "King":13}
    #The following dictionary is for comparing hands later on
    SCORE_COMPARING = {"High Card": 1,  "Pair": 2, "Two Pairs": 3, "Three of a Kind": 4,
                                           "Straight": 5, "Flush": 6, "Full House": 7, "Four of a Kind": 8, "Straight Flush": 9}

    #These class variables are to get some information for both player's hands to use to determine their hand types
    player_one_sorted = []
    player_one_suits = {"Diamonds": 0, "Clubs": 0, "Hearts": 0, "Spades": 0}
    player_one_high_value = 0
    player_one_hand_type = ""
    
    player_two_sorted = []
    player_two_suits = {"Diamonds": 0, "Clubs": 0, "Hearts": 0, "Spades": 0}
    player_two_high_value = 0
    player_two_hand_type = ""
    
    def __init__(self, player_one_hand, player_two_hand):
        self.player_one_hand = player_one_hand
        self.player_two_hand = player_two_hand
            
    def hand_number_organization(self):
        #The sorted() function here will organize the cards based on the first element in each of the lists representing the cards, which happens to be their corresponding numerical value
        Scoring.player_one_sorted = sorted(self.player_one_hand)
        Scoring.player_two_sorted = sorted(self.player_two_hand)
        player_one_high_value = Scoring.player_one_sorted[4]
        player_two_high_value = Scoring.player_two_sorted[4]

        #This relays the information to the user
        print()
        print("Player One's sorted hand:")
        print(sorted(Scoring.player_one_sorted))
        print()
        print("Player Two's sorted hand:")
        print(sorted(Scoring.player_two_sorted))

    def hand_suit_organization(self):
        #The user does not really need this information, so it is not given to them
        
        #These variables need to be reset each time, because otherwise it doesn't clear the values
        Scoring.player_one_suits = {"Diamonds": 0, "Clubs": 0, "Hearts": 0, "Spades": 0}
        Scoring.player_two_suits = {"Diamonds": 0, "Clubs": 0, "Hearts": 0, "Spades": 0}

        #This makes sure the suits are kept track of, to determine if any flush situations are possible
        for i in range(len(self.player_one_hand)):
            Scoring.player_one_suits[self.player_one_hand[i][2]] = Scoring.player_one_suits[self.player_one_hand[i][2]] + 1
        for j in range(len(self.player_two_hand)):
            Scoring.player_two_suits[self.player_two_hand[j][2]] = Scoring.player_two_suits[self.player_two_hand[j][2]] + 1

    def hand_organization(self):
        #Does both forms of organization
        self.hand_suit_organization()
        self.hand_number_organization()

    def flush_or_not(self):
        #Using the suit tracking dictionaries, this determines if any flush situations are possible        
        if (Scoring.player_one_suits["Diamonds"] == 5) or (Scoring.player_one_suits["Clubs"] == 5) or (Scoring.player_one_suits["Hearts"] == 5) or (Scoring.player_one_suits["Spades"] == 5):
            Scoring.player_one_hand_type = Scoring.player_one_hand_type + "Flush"
        
        if (Scoring.player_two_suits["Diamonds"] == 5) or (Scoring.player_two_suits["Clubs"] == 5) or (Scoring.player_two_suits["Hearts"] == 5) or (Scoring.player_two_suits["Spades"] == 5):
            Scoring.player_one_hand_type = Scoring.player_two_hand_type + "Flush"

    def number_based_hand_definition(self):
        #Just easier to write the shorter variable names
        one_a = int(Scoring.player_one_sorted[0][0])
        one_b = int(Scoring.player_one_sorted[1][0])
        one_c = int(Scoring.player_one_sorted[2][0])
        one_d = int(Scoring.player_one_sorted[3][0])
        one_e = int(Scoring.player_one_sorted[4][0])
        two_a = int(Scoring.player_two_sorted[0][0])
        two_b = int(Scoring.player_two_sorted[1][0])
        two_c = int(Scoring.player_two_sorted[2][0])
        two_d = int(Scoring.player_two_sorted[3][0])
        two_e = int(Scoring.player_two_sorted[4][0])

        #The 'straight' determination
        if (one_a + 1 == one_b) and (one_b + 1 == one_c) and (one_c + 1 == one_d) and (one_d + 1 == one_e):
            Scoring.player_one_hand_type = "Straight"

        #Four of a kind, since there are one 4 of each number the last number does not need to be checked for
        elif ((one_a == one_b) and (one_b == one_c) and (one_c == one_d)) or ((one_b == one_c) and (one_c == one_d) and (one_d == one_e)):
            Scoring.player_one_hand_type = "Four of a Kind"

        #Three of a kind and two of another kind for a full house
        elif ((one_a == one_b) and (one_b == one_c) and (one_d == one_e)) or ((one_a == one_b) and (one_c == one_d) and (one_d == one_e)):
            Scoring.player_one_hand_type = "Full House"

        #Three of a kind check
        elif ((one_a == one_b) and (one_b == one_c)) or ((one_b == one_c) and (one_c == one_d)) or ((one_c == one_d) and (one_d == one_e)):
            Scoring.player_one_hand_type = "Three of a Kind"

        #Double double check
        elif ((one_a == one_b) and (one_c == one_d)) or ((one_a == one_b) and (one_d == one_e)) or ((one_c == one_d) and (one_d == one_e)):
            Scoring.player_one_hand_type = "Two Pairs"

        #Single pair check
        elif (one_a == one_b) or (one_b == one_c) or (one_c == one_d) or (one_d == one_e):
            Scoring.player_one_hand_type = "Pair"

        #If there aren't any doubles
        else:
            Scoring.player_one_hand_type = "High Card"

        #Repeat of player one's hand's number based definitions
        if (two_a + 1 == two_b) and (two_b + 1 == two_c) and (two_c + 1 == two_d) and (two_d + 1 == two_e):
            Scoring.player_two_hand_type = "Straight"
            
        elif ((two_a == two_b) and (two_b == two_c) and (two_c == two_d)) or ((two_b == two_c) and (two_c == two_d) and (two_d == two_e)):
            Scoring.player_two_hand_type = "Four of a Kind"
            
        elif ((two_a == two_b) and (two_b == two_c) and (two_d == two_e)) or ((two_a == two_b) and (two_c == two_d) and (two_d == two_e)):
            Scoring.player_two_hand_type = "Full House"
            
        elif ((two_a == two_b) and (two_b == two_c)) or ((two_b == two_c) and (two_c == two_d)) or ((two_c == two_d) and (two_d == two_e)):
            Scoring.player_two_hand_type = "Three of a Kind"
            
        elif ((two_a == two_b) and (two_c == two_d)) or ((two_a == two_b) and (two_d == two_e)) or ((two_c == two_d) and (two_d == two_e)):
            Scoring.player_two_hand_type = "Two Pairs"
            
        elif (two_a == two_b) or (two_b == two_c) or (two_c == two_d) or (two_d == two_e):
            Scoring.player_two_hand_type = "Pair"
        else:
            Scoring.player_two_hand_type = "High Card"

    def full_hand_definition(self):
        #These variables need to be reset each time, because otherwise it doesn't clear the values
        Scoring.player_one_hand_type = ""
        Scoring.player_two_hand_type = ""

        #Calls the other hand definition functions for more streamlined main function
        self.number_based_hand_definition()
        self.flush_or_not()

        #Shows what kind of hand both players have
        print()
        print()
        print("Player one's hand is a " + Scoring.player_one_hand_type)
        print()
        print("Player two's hand is a " + Scoring.player_two_hand_type)

    def hand_comparison(self):
        #This method determines who wins, or ties in some cases
        if (Scoring.player_one_hand_type == "High Card") and (Scoring.player_two_hand_type == "High Card"):
            if (Scoring.player_one_sorted[4][0] > Scoring.player_two_sorted[4][0]):
                return ("Player One is the winner because their high card, the " +  Scoring.player_one_sorted[4][3] + "was higher than Player Two's high card, the " + Scoring.player_two_sorted[4][3] + ".")
            elif (Scoring.player_one_sorted[4][0] < Scoring.player_two_sorted[4][0]):
                return ("Player Two is the winner because their high card, the " +  Scoring.player_two_sorted[4][3] + "was higher than Player One's high card, the " + Scoring.player_one_sorted[4][3] + ".")
            else:
                return "Both players had equal high cards, so this round is a tie."
        else:
            if (Scoring.SCORE_COMPARING[Scoring.player_one_hand_type] > Scoring.SCORE_COMPARING[Scoring.player_two_hand_type]):
                return ("Player One won because their " + Scoring.player_one_hand_type + " beat Player Two's " + Scoring.player_two_hand_type + ".")
            elif (Scoring.SCORE_COMPARING[Scoring.player_one_hand_type] < Scoring.SCORE_COMPARING[Scoring.player_two_hand_type]):
                return ("Player Two won because their " + Scoring.player_two_hand_type + " beat Player One's " + Scoring.player_one_hand_type + ".")
            else:
                return "Both players tied because they had the same kind of hand"


