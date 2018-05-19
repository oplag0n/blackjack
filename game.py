import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

#CARD CLASS 
class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        
    
    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)

#CARD DECK
class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    
    def __str__(self): 
        deck_comp = ''  # start with an empty string
        for card in self.deck:
            deck_comp += '\n '+card.__str__() # add each Card object's print string
        return 'The deck has:' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        single_card = self.deck.pop()
        return single_card

#PLAYER HAND/ BANK HAND
class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1  # add to self.aces
    
    def adjust_for_ace(self):
        if self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet*2
    
    def lose_bet(self):
        self.total -= self.bet


########FUNCTIONS#########

def take_bet(chips):

    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except ValueError:
            print('Sorry, a bet must be an integer!')
        else:
            if chips.bet > chips.total:
                print("Sorry, your bet can't exceed",chips.total)
            else:
                break

def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing
    
    while True:
        x = input("Would you like to Hit or Stand? Enter 'h' or 's' ")
        
        if x[0].lower() == 'h':
            hit(deck,hand)  # hit() function defined above

        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False

        else:
            print("Sorry, please try again.")
            continue
        break

def show_some(player,dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])  
    print("\nPlayer's Hand:", player.cards)
    
def show_all(player,dealer):
    print("\nDealer's Hand:", dealer.cards)
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", player.cards)
    print("Player's Hand =",player.value)

#Game ending cases 

def player_busts(player, chips):
    print("You busted! Your value is: {}".format(player.value))
    chips.lose_bet()

def player_wins(player, dealer):
    print("You win! Your value is: {} The dealer has: {}".format(player.value, dealer.value))
    chips.win_bet()

def dealer_busts(chips):
    print("Dealer Busts! You are in Luck!")
    chips.win_bet()
    
def dealer_wins(player, dealer, chips):
    print("The Dealer wins! Your value is: {} The dealer has: {}".format(player.value, dealer.value))
    chips.lose_bet()
    
def push(player):
    print("Its a draw! You both have {}. You get your money back.".format(player.value))

#GAME LOGIC

while True:
    # Print an opening statement
    print("Welcome to Blackjack!")

    
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    player = Hand()
    player.add_card(deck.deal())
    player.add_card(deck.deal())
    dealer = Hand()
    dealer.add_card(deck.deal())
    dealer.add_card(deck.deal())
 
    # Set up the Player's chips
    chips = Chips()
    
    
    # Prompt the Player for their bet
    print("Place your bets!")
    take_bet(chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player, dealer)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        print("Hit or Stand?")
        hit_or_stand(deck,player)
        
        # Show cards (but keep one dealer card hidden)
        show_some(player, dealer)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player.value > 21:
            player_busts(player, chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player.value <= 21:
        
        while dealer.value < 17:
            hit(deck,dealer)
            
        # Show all cards
        show_all(player,dealer)
        
        # Test different winning scenarios
        if dealer.value > 21:
            dealer(player,dealer,chips)

        elif dealer.value > player.value:
            dealer_wins(player,dealer,chips)

        elif dealer.value < player.value:
            player_wins(player,dealer,chips)

        else:
            push(player,dealer) 
    
    # Inform Player of their chips total 
    print("\nPlayer's winnings stand at",player_chips.total)
    
    # Ask to play again
    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")
    if new_game[0].lower()=='y':
        playing=True
        continue
    else:
        print("Thanks for playing!")
        break
    # Ask to play again

    break