# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        
        self.str_hand = ""
        for i in self.cards:
            self.str_hand += str(i) + " "
        return "hand contains " + self.str_hand

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        
        cards_value = 0
        aces_high = 0
        
        for i in self.cards:
            cards_value += VALUES.get(i.get_rank())
        
            if i.get_rank() == 'A':
                if cards_value + 10 <= 21:
                    cards_value += 10
                    aces_high += 1
                    
            if cards_value > 21 and aces_high > 0:
                cards_value -= 10
                aces_high -= 1
                    
        return cards_value
              
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for i in self.cards:
            pos[0] += 72
            i.draw(canvas, pos)
       
# define deck class 
class Deck:
    def __init__(self):
        
        self.deck = []
        
        for s in SUITS:
            for r in RANKS:
                self.deck.append(Card(s,r))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        # return a string representing the deck
    
        str_deck = ""
        
        for i in self.deck:
            str_deck += str(i) + " "
        return "Deck contains " + str_deck


#define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand, new_deck, score
    
    if in_play:
        outcome = "Player surrenders!"
        score -= 1
        in_play = False
        
    else:
        outcome = ""
    
        new_deck = Deck()
        new_deck.shuffle()
    
        player_hand = Hand()
        dealer_hand = Hand()
    
        for i in range(2):
            player_hand.add_card(new_deck.deal_card())
            dealer_hand.add_card(new_deck.deal_card())
    
        outcome = "Hit or stand?"
    
        in_play = True

def hit():
    
    global in_play, score, player_hand, new_deck, outcome
    # if the hand is in play, hit the player
    
    if in_play:
        player_hand.add_card(new_deck.deal_card())
   
        # if busted, assign a message to outcome, update in_play and score
    
        if player_hand.get_value() > 21:
            outcome = "Player busts! New deal?"
            score -= 1
            in_play = False
       
def stand():
    
    global in_play, dealer_hand, player_hand, new_deck, score, outcome
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(new_deck.deal_card())

    # assign a message to outcome, update in_play and score
    
        if dealer_hand.get_value() > 21:     
            outcome = "Dealer busts! New deal?"
            score += 1
        elif dealer_hand.get_value() > player_hand.get_value():
            outcome = "Dealer wins! New deal?"
            score -= 1
        elif dealer_hand.get_value() == player_hand.get_value():
            outcome = "Tie! Dealer wins! New deal?"
            score -= 1
        else:
            outcome = "Player wins! New deal?"
            score += 1
        
        in_play = False

# draw handler    
def draw(canvas):
    global player_hand, dealer_hand, outcome, score, in_play
    # test to make sure that card.draw works, replace with your code below
    
    p_pos = [100, 300]
    d_pos = [100, 100]
    
    player_hand.draw(canvas, p_pos)
    dealer_hand.draw(canvas, d_pos)
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [d_pos[0] - 72 + CARD_BACK_CENTER[0], d_pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    
    canvas.draw_text("Blackjack", [172, 60], 60, 'Black', 'sans-serif')
    canvas.draw_text(outcome, [172, 255], 30, 'Yellow', 'sans-serif')
    canvas.draw_text("Dealer", [60, 140], 30, 'Black', 'sans-serif')
    if not in_play:
        canvas.draw_text(str(dealer_hand.get_value()), [92, 180], 30, 'Black', 'sans-serif')
    if in_play:
        canvas.draw_text("?", [95, 180], 30, 'Black', 'sans-serif')
    canvas.draw_text("Player", [60, 340], 30, 'Black', 'sans-serif')
    canvas.draw_text(str(player_hand.get_value()), [92, 380], 30, 'Black', 'sans-serif')
    canvas.draw_text("Score: " + str(score), [172, 465], 30, 'Black', 'sans-serif')

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()