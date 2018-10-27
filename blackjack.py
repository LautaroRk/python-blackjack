import random

suits = ('♥','♦','♠','♣')
ranks = ('2','3','4','5','6','7','8','9','10','J','Q','K','A')
values = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10,'A':11}

class Card:
    
    def __init__(self,rank,suit):
        self.rank = rank
        self.suit = suit
        self.value = values[rank]
        
    def __str__(self):
        return f'[{self.rank}{self.suit}]'

class Deck:
    
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(rank,suit))
                self.deck.append(Card(rank,suit))
                self.deck.append(Card(rank,suit))
    
    def __str__(self):
        my_deck = ''
        for card in self.deck:
            my_deck += card.__str__()
        return my_deck
    
    def shuffle(self):
        random.shuffle(self.deck)
    
    def deal(self):
        single_card = self.deck.pop()
        return single_card   

class Player:
    
    def __init__(self):
        self.name = ''
        self.hand = []
        self.split = []
        self.value = 0
        self.chips = 0
        self.aces = 0
        self.bet = 0
        self.playing = True
        self.playing_hand = True
        
    def __str__(self):
        myhand = ''
        for card in self.hand:
            myhand += card.__str__()
        return f'Name: {self.name}\nHand: {myhand}\nValue: {self.value}\nChips: {self.chips}\nBet: {self.bet}'
        
    def new_player(self):
        self.name = input('Name: ')
        self.chips = 100
        self.hand = []
        
    def first_deal(self,deck):
        self.hand.append(deck.deal())
        self.hand.append(deck.deal())
        if self.hand[0].rank == 'A':
            self.aces += 1
        if self.hand[1].rank == 'A':
            self.aces += 1
        self.value = self.hand[0].value + self.hand[1].value
        self.adjust_for_aces()
            
    def add_card(self,deck):
        card = deck.deal()
        self.hand.append(card)
        self.value += card.value
        if card.rank == 'A':
                self.aces += 1
        
    def adjust_for_aces(self):
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1
            
    def win_bet(self):
        self.chips += self.bet
        
    def lose_bet(self):
        self.chips -= self.bet

#FUNCIONES

def take_bet(player):
    
    while True:
        try:
            player.bet = int(input(f'{player.name}, you have {player.chips} chips. Place your bet: '))
        except:
            continue
        else:
            if player.bet > player.chips or player.bet < 1:
                print("You don't have enough chips.")
                continue
            else:
                break

def hit(deck,player):
    
    player.add_card(deck)
    player.adjust_for_aces()
    show_all(player)

def hit_or_stand(deck,player):
    
    while player.value < 21 and player.playing and player.playing_hand:
        
        if len(player.hand) == 2 and player.chips >= (player.bet * 2):
            show_all(player)
            x = input(f"\n{player.name}'s turn\n'h' for hit, 's' for stand, 'd' for double: ").lower()
            if x == 'h':
                hit(deck,player)
            elif x == 's':
                player.playing = False
            elif x == 'd':
                player.bet += player.bet
                hit(deck,player)
                player.playing = False
            else:
                continue
                
        else:
            show_all(player)
            x = input(f"\n{player.name}'s turn\n'h' for hit, 's' for stand: ").lower()
            if x == 'h':
                hit(deck,player)
            elif x == 's':
                player.playing = False
            else:
                continue

def show_some(player):
    print('\n\n\n\n______________________________________________________________________\n\nDealer\n[hidden] ' + player.hand[1].__str__() + '\n')
    
def show_all(player):
    print(f'\n{player.name}\nChips: {player.chips}\nBet: {player.bet}\nHand:', *player.hand, sep = ' ')
    
def show_all_dealer(player):
    print('\nDealer\n', *player.hand, sep = ' ')



#GAMEPLAY

while True:
    
    #SET DECK, DEALER AND POSSIBLE PLAYERS
    
    mydeck = Deck()
    mydeck.shuffle()

    dealer = Player()
    dealer.name = 'Dealer'
    dealer.chips = float('inf')

    player1 = Player()
    player2 = Player()
    player3 = Player()
    
    hand_on = True
    game_on = True
    
    
    #TITULO
    
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n                                                                                             _________\n                                                                                             BLACKJACK')
    
    
    #CANTIDAD DE JUGADORES
    
    number_of_players = 1
    players_list = [player1]
    
    while True:
        try:
            number_of_players = int(input('Number of players: (3 max): '))
            if number_of_players > 3 or number_of_players < 1:
                continue
            break
        except:
            continue
            
    #CARGAR NOMBRES DE JUGADORES
    
    if number_of_players == 1:
        players_list = [player1]
        
    if number_of_players == 2:
        players_list = [player1,player2]
        
    if number_of_players == 3:
        players_list = [player1,player2,player3]
        
    for player in players_list:
        player.new_player()

    

    while game_on:
        
        #PRIMER REPARTIJA
        
        mydeck = Deck()
        mydeck.shuffle()

        for player in players_list:
            if player.playing:
                take_bet(player)

        for player in players_list:
            if player.playing:
                player.first_deal(mydeck)

        dealer.first_deal(mydeck)
        
        
        #DISPLAY BOARD
        
        show_some(dealer)
        
        for player in players_list:
            if player.playing:
                show_all(player)
        
        print('\n')
        
        #???while hand_on:
        for player in players_list:
            
            if player.playing: 
                
                if player.value == 21:
                    player.bet *= 1.5 
                    player.chips += player.bet
                    player.playing_hand = False
                    print(f'\n{player.name} got BLACKJACK! {player.bet} chips earned...')
                
                show_some(dealer)    
                hit_or_stand(mydeck,player)
                
                if player.value > 21:
                    player.lose_bet()
                    player.playing_hand = False
                    print(f'\n{player.name} BUSTS! {player.bet} chips lost...')
                    if player.chips == 0:
                        print(f'{player.name} run out of chips :(')
                        player.playing = False
                    
        show_all_dealer(dealer)
        
        while dealer.value < 17:
            dealer.add_card(mydeck)
            show_all_dealer(dealer)
            dealer.adjust_for_aces()
        
        if dealer.value > 21:
            print('\nDealer BUSTS!')
            for player in players_list:
                if player.playing_hand:    
                    player.win_bet()
                    print(f'\n{player.name} earns {player.bet} chips!')
        else:
            for player in players_list:
                if player.playing_hand:  
                    if player.value > dealer.value:
                        player.win_bet()
                        print(f'\n{player.name} WINS! {player.bet} chips earned...')
                    elif player.value < dealer.value:
                        player.lose_bet()
                        print(f'\n{player.name} lost {player.bet} chips...')
                    else:
                        print(f"\n{player.name}: It's a PUSH!")
                        
                
        count = 0
        for player in players_list:
            if player.chips <= 0:
                print(f'{player.name} run out of chips :(')
                players_list.pop(count)
            else:
                player.bet = 0
                player.hand = []
                player.playing = True
                player.playing_hand = True 
                player.aces = 0       
            count += 1
            
        if len(players_list) == 0:
            game_on = False
        else:
            dealer.hand = []
            continue
        
    #JUGAR DE NUEVO?
    answer = input('\n\n\nWant to play again? (y/n): ').lower()
    if answer == 'y':
        continue
    else:
        break

