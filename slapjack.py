from poker_classes import *
import time
import random

class SlapJack: #This simulates a single round game of Slapjack wherein if the player wins, they get an extra life in the overall game
    
    def __init__(self):#These variables will maintain the game
        
        self.deck_ref = Deck() # make deck 
        self.player_onehand = [] # player one hand 
        self.player_twohand = [] # player two hand
        self.p1_jack_one = False 
        self.p1_jack_two = False
        self.p2_jack_one = False
        self.p2_jack_two = False
        self.slap_player = False
        self.slap_comp = False
             
    def show(self): #This method is for the final game
        print("Welcome to Slap Jack! This is your chance to climb the beanstalk again!")
        print("Are you willing to take another chance?")
    
    def deal_cards(self): #Using the Deck class in the poker_classes file, the deck is shuffled and dealt to two players

        #These are for the user to understand what's happening
        print("Shuffling...")
        time.sleep(2)
        print("Shuffling...")
        time.sleep(1)
        self.deck_ref.shuffle()
        self.deck_ref.shuffle()
        print("Cards Shuffled")
        print("")

        #To take as much user input as possible
        input_ = input("Press Enter to start dealing cards: ")
        print("")

        #The deck is dealth to completion for 2 players (user and computer) so only 26 runs of the loop is needed
        for i in range(26): 
            if input_ == "":
                card = self.deck_ref.get_cards()
                self.player_onehand.append(card.pop())
                random.shuffle(self.player_onehand)
                
                card = self.deck_ref.get_cards()
                self.player_twohand.append(card.pop())
                random.shuffle(self.player_twohand)

        #Also for the user to keep up
        print("Cards Dealt")
        print("")

    def game(self): #This actually simulates the SlapJack game

        #This counter is to allow for the first round to be different than the next rounds, as the first round offers a different input statement
        x = 0
        
        while ((self.p1_jack_one == False) and (self.p1_jack_two == False) and (self.p2_jack_one == False) and (self.p2_jack_two == False)): #Since the game can go on indefinitely, a while loop is needed

            #To allow for a unique statement in the first interation of the loop
            if x == 0:
                input_ = input("Press Enter to pull out a card: ")
                print("")

            #For the user to catch up (all the time.sleep statements are for the same reason)
            time.sleep(1)

            #Here is where the actual game starts, checking each flipped card for the "Jack" cards and prompting the user to slap or pass
            random.shuffle(self.player_onehand)

            dealt_card = self.player_onehand.pop()

            #Different statements are used to simulate a real game wherein flipping a Jack causes more hype than a regular flip
            if ("Jack" not in dealt_card):
                print("The flipped card for Player 1 is " + dealt_card[3])
            else:
                if ("Jack" in dealt_card):
                    print("LOOK, PLAYER 1 HAS PUT DOWN A JACK! SLAP IT!")

            self.slap_comp = self.slapping(dealt_card) #This method checks if the computer slaps the pile or not
            
            player_slap = input("Will you slap? Y/N? ") #Actual prompt to slap or pass
            print("")

            time.sleep(1)

            #This conditional set checks to see the winner of the round, if anything round determining happened
            if (player_slap == "Y") and ("Jack" in dealt_card) and (self.slap_comp == False):
                return "Player wins by slapping Jack first", 1 #If the player slaps correctly, they win
            
            elif ((player_slap == "Y") and ("Jack" in dealt_card) and (self.slap_comp == True)) or ((player_slap == "N") and ("Jack" in dealt_card)):
                return "Computer wins by slapping Jack first", 0 #If the computer slaps, it will slap first, and if the player doesn't slap, the computer slaps first, meaning the computer wins either way
            
            elif (player_slap == "Y") and ("Jack" not in dealt_card) and (self.slap_comp == False):
                return "Computer wins (player slapped the wrong card)", 0 #The player slapped the wrong card which is a mistake
            
            elif (player_slap == "N") and ("Jack" not in dealt_card) and (self.slap_comp == True):
                return "Player wins (opponent slapped the wrong card)", 1 #If the computer slaps the wrong card

            #This next set of code redoes the previous conditionals and prompting but with the cards of the second pile, given to the computer

            #Taking from the pile of the second player (computer)
            random.shuffle(self.player_twohand)
            dealt_card_two = self.player_twohand.pop()

            #Different statements are used to simulate a real game wherein flipping a Jack causes more hype than a regular flip
            if ("Jack" not in dealt_card_two):
                print("The flipped card for Player 2 is " + dealt_card_two[3])
            else:
                if ("Jack" in dealt_card_two):
                    print("LOOK, PLAYER 2 HAS PUT DOWN A JACK! SLAP IT!")

            self.slap_comp = self.slapping(dealt_card_two) #This method checks if the computer slaps the pile or not

            player_slap = input("Will you slap? Y/N? ")#Actual prompt to slap or pass
            print("")
            
            time.sleep(1)

            #This conditional set checks to see the winner of the round, if anything round determining happened
            if (player_slap == "Y") and ("Jack" in dealt_card_two) and (self.slap_comp == False):
                return "Player wins by slapping Jack first", 1 #If the player slaps correctly, they win
            
            elif ((player_slap == "Y") and ("Jack" in dealt_card_two) and (self.slap_comp == True)) or ((player_slap == "N") and ("Jack" in dealt_card_two)):
                return "Computer wins by slapping Jack first", 0 #If the computer slaps, it will slap first, and if the player doesn't slap, the computer slaps first, meaning the computer wins either way
            
            elif (player_slap == "Y") and ("Jack" not in dealt_card_two) and (self.slap_comp == False):
                return "Computer wins (player slapped the wrong card)", 0 #The player slapped the wrong card which is a mistake
            
            elif (player_slap == "N") and ("Jack" not in dealt_card_two) and (self.slap_comp == True):
                return "Player wins (opponent slapped the wrong card)", 1 #If the computer slaps the wrong card

            x = x + 1 #Makes it so that the first loop is unique in starting the game

                        
    def slapping(self, dealt_card): #Uses random chance to see if the computer will slap the card or not
        slap_prob = random.randrange(100)

        if (slap_prob <= 38) and (dealt_card[:4] == "Jack"):
            return True #If the card drawn is a Jack, and the probability of the slap comes below the chance of the computer slapping right, the computer will slap and win

        elif (slap_prob >= 94) and (dealt_card[:4] != "Jack"):
            return True #If the card drawn is not a Jack, and the probability of the slap comes above the chance of the computer slapping wrong, the computer will slap and lose (in 1 of 2 cases)

        else:
            return False #Computer does not slap
        
