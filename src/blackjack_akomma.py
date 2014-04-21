#!/usr/bin/python

# The MIT License (MIT)
# Copyright (c) <2013> <Abi Komma>
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction,including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#  The software is provided "as is", without warranty of any kind,
#  express or implied, i ncluding but not limited to the warranties
#  of merchantability, fitness for a particular purpose and noninfringement.
#  In no event shall the authors or copyright holders be liable for any claim,
#  damages or other liability, whether in an action of contract, tort or
#  otherwise, arising from, out of or in connection with the software or
#  the use or other dealings in the software.
#
#-------------------------------------------------------------------------------
# Let's play Blackjack on a text-console
# Author:      Abi Komma
# Created:     15/04/2014
# Version:     Python 2.7.3
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Assumptions:
# -------------
# 1. One dealer (computer), One player (user input)
# 2. Infinite decks in play
# 3. Dealer logic: Stands if current total >=17
# 4. Dealer wins in a tie
# 5. Player buys-in with 100 Chips and bets atleast 1 chip every game
#-------------------------------------------------------------------------------

import sys
from random import choice

# Defining a deck. Pool of Cards
# Allocating values to the cards
cards = {'A':11, '2':2, '3':3, '4':4, '5':5,
         '6':6, '7':7, '8':8, '9':9, '10':10,
         'J':10, 'Q':10, 'K':10}

# Welcome message
welcome_msg = ['Start a New game??',
                'Try your luck again! New game??',
                'It is now or never! New game??',
                'The odds are in your favor! New game??']

# Define the player and dealer lists
player = []
dealer = []

# Define vars to keep track of the chips and bet each game
chips = 100
bet = 0

print('==============================================================')
print('Welcome! Huan Ying! Yokoso! Bienvenido! Swagat! Welkom!')
print('You are @ oostopitre Casino')
print('Let\'s play some Blackjack')
print('==============================================================')
print

def main():
    initiate()  #Initiate the game
    read_bet()  #Read the bet amount for the current game
    play()  #Begin the game

def play():
    while(True):
        choice = read_choice()
        if(choice=='h'):
            hit()
        elif(choice=='s'):
            stand()

# Initiate the game. Two cards dealt to each player and dealer
def initiate():
    draw(player), draw(dealer)
    draw(player), draw(dealer)
    print("Player has {0} with a sum of {1}"
    .format(player, sum_hand(player)))
    print("Dealer has {0} with a sum of {1}"
    .format(dealer, sum_hand(dealer)))

# Pick one item from the 'cards' deck
def draw(member):
    pick = random.choice(cards.keys())
    member.append(pick)

# Ask the player to Hit or Stand
def read_choice():
    choice = raw_input('Hit(h) or Stand(s)?').lower()
    while(choice not in ('h','s')):
        print('Invalid Choice. Hit(h) or Stand(s)?')
        choice = raw_input('Hit(h) or Stand(s)?').lower()
    return choice

# Defining the events when a player says 'hit'
def hit():
    global pool
    global chips

    draw(player)

    #print 'Player:', player,'=',sum_hand(player)
    print('Player has {0} with a sum total of {1}'
    .format(player, sum_hand(player)))

    # Check if Blackajack
    if(sum_hand(player)==21):
        print('You have a ***Blackjack***')
        stand() #Player wins unless the dealer has a Blackjack too

    # Check if player bust, Dealer wins
    if(check_bust(player)):
        print('You got *Busted*. <DEALER> wins!\'Get lucky\' next game')
        chips-=bet
        print('Your chips remaining: {0}'.format(chips))
        start_new_game()

# Defining the events when a player says 'stand'
def stand():

    global chips
    global pool

    # Dealer draws only if dealer total<17 and player>dealer
    while (sum_hand(dealer)<17 and (sum_hand(player)>sum_hand(dealer))):
        draw(dealer)
        print("Dealer has {0} with a sum of {1}"
        .format(dealer, sum_hand(dealer)))

        # Check Dealer bust, Player wins
        if(check_bust(dealer)):
            print('Dealer Buster. <PLAYER> wins! :) Winners never quit!')
            chips+=bet
            print('Your chips remaining: {0}'.format(chips))
            start_new_game()

    # If dealer < 17 & Player < Dealer
    if (sum_hand(dealer)<17 and (sum_hand(player)<=sum_hand(dealer))):
        if(check_win()):
            start_new_game()

    # Dealer ends the current game if the total>=17
    if (sum_hand(dealer)>=17):
        if(check_win()):
            start_new_game()

# Reading in the amount to bet on each hand
def read_bet():
    while(True):

        global chips
        global bet

        try:
            bet = int(raw_input("Amount to bet (1 Chip minimum): "))

            if(bet>=1 and bet<=chips):
                print('Bet amount is: {0}'.format(bet))
                break
            elif(bet>chips):
                print('Amount exceeds your total chips. Try a smaller bet')
            else:
                print('Enter a valid bet amount')
        except(ValueError):
            print('Invalid Entry. Try again. Enter a valid bet amount')

# If neither are busted, evaluating the winner
def check_win():

    global chips
    global bet

    print '--------------------------------------------------------------'
    print('Player has {0} with a sum total of {1}'
    .format(player, sum_hand(player)))
    print('Player has {0} with a sum total of {1}'
    .format(dealer, sum_hand(dealer)))
    print '--------------------------------------------------------------'
    if(sum_hand(dealer)>=sum_hand(player)):
        print('<DEALER> wins! Do you know that Quitters never win? ')
        chips-=bet
        print('Total chips remaining is {0}:'.format(chips))
    else:
        print('<PLAYER> wins! :) Winner winner chicken dinner!')
        chips+=bet
        print('Total chips remaining is {0}:'.format(chips))
    return True

# Calculate the sum total value of the current hand
def sum_hand(member):
    total = 0
    num_aces = member.count('A')

    for each in member:
        total+=cards[each]
    if(total>21 and num_aces>=1):
        while(total>21 and num_aces>=1):
            total-=10
            num_aces-=1
    return total

# Checking if a member has a busted hand
def check_bust(member):
    if(sum_hand(member)>21):
        #print('xxx Busted xxx')
        return True

# Start a new game
def start_new_game():
    global pool
    global bet

    #print
    print('==============================================================')
    msg = random.choice(welcome_msg)
    print msg
    new_game = raw_input(('Press \'q\' to QUIT (or)\
    Any other key to continue')).lower()

    if(new_game=='q'):
        print('==============================================================')
        print('Aww. Thank you for playing @ oostopitre Casino!')
        sys.exit()
    else:
        print('--> Yay! New Deal:')
        print('--------------------------------------------------------------')
        # Clear the player and dealer lists
        player[:]=[]
        dealer[:]=[]
        pool = 0
        bet = 0
        main()


if __name__ == "__main__":
    try:
      main()
    except KeyboardInterrupt:
      pass
