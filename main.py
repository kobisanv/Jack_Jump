import random
import pygame
from pygame import mixer
import math
import os
from slapjack import SlapJack

cont_choice = ""
retried = False

player_choice = input("Do you want to play singleplayer or multiplayer? ")

if player_choice == "singleplayer" or player_choice == "Singleplayer" or player_choice == "Single Player":
    import jack_dood_with_retry
elif player_choice == "multiplayer" or player_choice == "Multiplayer":
    import jack_coop

