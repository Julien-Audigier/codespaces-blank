import math
import random
from colorama import Fore, Style
import time

#Const
cardsHiding = 1
timeSpeed = 0.75
highScore = 0

#basic functions

def prt_ivd( text = "Invalid Input" , color = Fore.RED):
    """prints <Invalid Input> in color"""
    print(color + Style.NORMAL + "<" + Style.BRIGHT + text + Style.NORMAL + ">" + Fore.RESET)

def rpt_prt(string:str, i:int):
    """Prints "string" "i" times """
    for times in range(0,i):
        print(string)

def input_int(prompt:str, min:int = 0, max:int = None):
    """Enter prompt with rules"""
    noError = True
    while noError:
        try:
            answer = int(input(prompt + Fore.CYAN + Style.BRIGHT))
            print(Style.RESET_ALL)
            if (min != None):
                if (answer < min):
                    prt_ivd()
                    continue #restart loop
            if (max != None):
                if (answer > max):
                    prt_ivd()
                    continue #restart loop
            return(answer)
        except ValueError:
            prt_ivd()
        except TypeError:
            prt_ivd()
    return None

def input_list(prompt:str, questions:list[str]):
    """This function generates a question off of "questions"."""
    print(prompt)
    for i, item in enumerate(questions):
        print(str(i+1)+". "+ item)
    try:
        answer = int(input(Fore.CYAN + Style.BRIGHT))
        print(Style.RESET_ALL)
        answer -= 1
        if (answer < 0 or answer >= len(questions)):
            prt_ivd()
            return input_list(prompt,questions)
        return questions[answer]
    except ValueError:
        print("")
        prt_ivd()
        time.sleep(timeSpeed * 1)
        rpt_prt("", 40)
        return input_list(prompt,questions)

def list_to_str(list:list, color = Fore.WHITE, strBreak = "and",):
    """EX: "item0, item1, item2, and item3","""
    string = []
    for i, item in enumerate(list):
        if ((len(list)) > 2 and i != len(list)-1):
            string.append(f" {color}{item}{Fore.RESET},")
        elif (i == 0):
            string.append(f"{color}{item}{Fore.RESET}")
        else:
            string.append(f" {color}{item}{Fore.RESET}")
        if (i == len(list)-2):
            string.append(" "+ strBreak)
    return "".join(string)

def move_list(list):
    newList = []
    for item in list:
        newList.append(item)
    return newList

#classes

class SUIT:
    """Ex: clubs, ♣, Fore.BLACK"""
    def __init__(self, name: str, symbol: str, color):
        self.name = name
        self.symbol = symbol
        self.color = color

class CARD:
    """Ex: suitList[0], 10 | Ex: Clubs, "King" """
    def __init__(self, suit:SUIT, price: str):
        self.suit = suit
        self.price = price

    def card(self):
        """Returns formating of card"""
        if (self.suit.name == "diamonds" and self.price == "10"):
            return(Fore.MAGENTA + "ඞ Greg" + Fore.RESET + Style.RESET_ALL)
        #if (self.suit.name == "hearts" and self.price == "10"):
        #    return(Fore.GREEN + "ඞ Gerg" + Fore.RESET + Style.RESET_ALL)
        return(self.suit.color + Style.BRIGHT + self.suit.symbol +" "+ self.price + Style.RESET_ALL)
    
    def weight(self):
        try:
            weight = (["Ace","2","3","4","5","6","7","8","9","10"].index(self.price))+1
            return weight
        except ValueError:
            try:
                return int(self.price)
            except:
                return 10

class DECK:
    """enter list of suits"""
    def __init__(self, deck:list[CARD] = [], suits: list[SUIT] = None, numDecks = 1,):
        self.deck = deck
        self.suits = suits
        self.numDecks = numDecks
        if (deck == [] and suits != None):
            for i in range(0,numDecks):
                for suit in suits:
                    for price in ["Ace","2","3","4","5","6","7","8","9","10","Jack","Queen","King"]:
                        self.deck.append(CARD(suit,price))

    def shuffle(self):
        random.shuffle(self.deck)
    
    def show_aslist(self):
        """Each card has one line"""
        for card in self.deck:
            print(card.card())

    def append(self, card:CARD):
        """Appends a Card to the end of the deck"""
        self.deck.append(card)

    def pop(self, index):
        """Removes and returns card at the index"""
        return self.deck.pop(index)

    def cardsTo_str(self):
        """All the cards are on one string"""
        if self.deck != []:
            list = []
            for card in self.deck:
                list.append(card.card())
            return list_to_str(list)
        
    def weight(self, color = Fore.WHITE):
        numACE = 0
        total = 0
        for card in self.deck:
            if card.weight() == 1:
                numACE += 1
            total += card.weight()

        totals = [total]
        for i in range(0,numACE):
            total += 10
            totals.append(total)
        global highScore
        if totals[-1] > highScore:
            highScore = totals[-1]
        weights = move_list(totals)
        for weight in totals:
            if weight > 21: #Busted
                weights.remove(weight)
            if weight == 21:
                return "Blackjack!" 
        if len(weights) == 0:
            if len(totals) == 1:
                return f"Busted! with a total of {color}{totals[0]}{Fore.RESET}"
            return f"Busted! with totals of {list_to_str(totals, color)}"
        if len(weights) == 1:
            return f"a total of {color}{weights[0]}{Fore.RESET}"
        return f"totals of {list_to_str(weights, color,"or")}"

    def cac_prob(self, suits: list[SUIT],cardsShowing:list[CARD] = [],numDecks = 1, fair = True):
        """Calculates probability of not busting if a card is drawn"""
        weight = 0
        for card in self.deck:
            weight += card.weight()
        if weight <= 16 and weight > 11 and fair:
            return .90
        gameDeck = DECK([],suits, numDecks)
        goodCards = []
        for card in gameDeck.deck: #For each card in the deck
            cardPlayed = False
            for cardShow in cardsShowing:
                if cardShow == card:
                    cardPlayed = True
            if (cardPlayed == False):
                total = 0
                for selfCard in self.deck:
                    total += selfCard.weight()
                total += card.weight()
                if total <= 21 and selfCard != card:
                    goodCards.append(card)
        return len(goodCards)/len(gameDeck.deck)

class PLAYER:
    def __init__(self, name:str):
        self.name = name
        self.DECK = DECK([])
        self.deck = self.DECK.deck

    def find_cards_showing(self):
        """returns all cards showing"""
        tempDeck = DECK([])
        for card in self.deck:
            if self.deck.index(card) >= cardsHiding:
                tempDeck.append(card)
        return tempDeck

    def user_play(self, gameDeck:DECK, players:list, ai:list, dealer):
        """See cards, Hit, or Stay"""
        rpt_prt("", 40)
        print(Fore.CYAN + "Player " + self.name + "'s" + Style.RESET_ALL + " turn!")

        options = ["See Cards", "Hit", "Stay"]
        while True:
            result = self.DECK.weight()
            if "Busted" in result or "Blackjack" in result:
                        options = ["See Cards", "Stay"]
            match input_list("Choose options", options):
                case "See Cards": #Print all cards showing
                    rpt_prt("", 40)
                    #Their Cards
                    print(f"Your cards: {self.DECK.cardsTo_str()}.")
                    print(f"You have {self.DECK.weight(Fore.CYAN)}")
                    print("")
                    time.sleep(timeSpeed * 1)

                    #Other player's cards
                    show_showingCards(self, players)

                    #Ai cards
                    show_showingCards(self,ai, Fore.GREEN, "AI")

                    #Dealer
                    print(Fore.MAGENTA + "The dealer" + Style.RESET_ALL + f" is showing {len(dealer.deck)-cardsHiding} out of {len(dealer.deck)} cards: {dealer.find_cards_showing().cardsTo_str()}.")
                    print()

                    #Formating
                    print("")
                    time.sleep(timeSpeed * 3)
                    print("")
                    continue

                case "Hit": #Add top card to deck
                    rpt_prt("", 40)
                    print("You have choosen to hit")
                    self.deck.append(gameDeck.pop(0))
                    print(Fore.CYAN +"You " + self.name + Fore.RESET + " were dealt the card: " + self.deck[-1].card() + "!")
                    print("You have " + self.DECK.weight(Fore.CYAN))
                    
                    print("")
                    time.sleep(timeSpeed * 1.4)

                case "Stay": #Go to next player/AI
                    rpt_prt("", 40)
                    print("You have choosen to stay")
                    time.sleep(timeSpeed * 2)
                    return gameDeck

    def ai_play(self, gameDeck:DECK, players:list, ai:list, dealer, name = "AI", color = Fore.GREEN):
        """AI logic for playing"""
        cardsShowing = []
        for player in players: #Append Cards showing
            for card in player.find_cards_showing().deck: cardsShowing.append(card)
        for AI in ai:
            for card in AI.find_cards_showing().deck: cardsShowing.append(card)
        for card in dealer.find_cards_showing().deck: cardsShowing.append(card)
        
        while True:
            if random.randint(0,10) <= self.DECK.cac_prob(gameDeck.suits,cardsShowing,gameDeck.numDecks) * 10: # hit
                self.DECK.append(gameDeck.pop(0))
                print(f"{color}{name} {self.name}{Fore.RESET} chose to hit, drew card: {self.deck[-1].card()}")
                time.sleep(timeSpeed * 1)
            else: # pass
                print(f"{color}{name} {self.name}{Fore.RESET} chose to pass.")
                time.sleep(timeSpeed * 1)
                return gameDeck
                
#Game functions

def show_showingCards(self:PLAYER, others:list[DECK],color = Fore.CYAN, name = "PLayer"):
    """List of players or ai, it shows all the cards that aren't hiding"""
    for other in others:
        if other != self:
            tempDeck = other.find_cards_showing()
            print(color + f"{name} {other.name} " + Style.RESET_ALL + f"is showing {len(other.deck)-cardsHiding} out of {len(other.deck)} cards: {tempDeck.cardsTo_str()}.")
            print("")
            time.sleep(timeSpeed * 0.5)

#Main Script

suitsCards = [SUIT("clubs", "♣", Fore.BLACK), SUIT("diamonds", "♦", Fore.RED), SUIT("spades", "♠", Fore.BLACK), SUIT("hearts", "♥", Fore.RED)]

rpt_prt("", 40)

#gameDeck = DECK([],suitsCards,input_int("Enter number of decks (1-5): ",1,5))
#gameDeck.show_aslist()
#time.sleep(100)

while (True): #Game Loop
    rpt_prt("", 40)
    
    #Setup vars
    gameDeck = DECK([],suitsCards,input_int("Enter number of decks (1-50): ",1))
    gameDeck.shuffle()

    users = []
    ai = []
    dealer = PLAYER("dealer")
    
    numUsers = input_int("Enter number of players: ", 0, 10)
    numAi = input_int("Enter number of AI: ", 0)
    try:
        if (numUsers + numAi > (len(gameDeck.deck)//2)//2 -1): #Max players based on number of decks
            prt_ivd("Too many players for number of decks")
            time.sleep(timeSpeed * 2)
            continue
    except ZeroDivisionError:
        prt_ivd("Too many players for number of decks")
        time.sleep(timeSpeed * 2)
        continue
    if (numAi + numUsers == 0): #Makesure there is at least one player or AI
        rpt_prt("", 40)
        print("No players or AI")
        prt_ivd("Game Restarting")
        print("")
        time.sleep(timeSpeed * 2)
        continue

    #Make AI and Player decks.
    for i in range(0,numUsers):
        users.append(PLAYER(str(i+1))) #make player
    for i in range(0,numAi):
        ai.append(PLAYER(str(i+1))) #make Ai
    
    #Deal
    
    rpt_prt("", 40)
    print(Fore.MAGENTA + "The dealer" + Fore.RESET + " deals:")
    print("")

    for user in users: #Deal players (without showing cards)
        user.deck.append(gameDeck.pop(0))
        print(Fore.CYAN +"Player " + user.name + Fore.RESET + " was dealt a card!")
        print("")
        time.sleep(timeSpeed * 1)

    for i in ai: #Deal AI (without showing cards)
        i.deck.append(gameDeck.pop(0))
        print(Fore.GREEN + "AI " + i.name + Fore.RESET + " was dealt a card!")
        print("")
        time.sleep(timeSpeed * 1)

    dealer.deck.append(gameDeck.deck.pop(0)) #Deal Dealer (without showing cards)
    print(Fore.MAGENTA + "The dealer" + Fore.RESET + " dealt themself a card!")
    print("")
    time.sleep(timeSpeed * 1)

    for user in users: #Deal players
        user.deck.append(gameDeck.pop(0))
        print(Fore.CYAN +"Player " + user.name + Fore.RESET + " was dealt another card: " + user.deck[-1].card()+ "!")
        print("")
        time.sleep(timeSpeed * 1)

    for i in ai: #Deal AI
        i.deck.append(gameDeck.pop(0))
        print(Fore.GREEN + "AI " + i.name + Fore.RESET + " was dealt another card: " + i.deck[-1].card()+ "!")
        print("")
        time.sleep(timeSpeed * 1)

    dealer.deck.append(gameDeck.deck.pop(0)) #Deal Dealer
    print(Fore.MAGENTA + "The dealer" + Fore.RESET + " dealt themself another card: " + dealer.deck[-1].card()+ "!")
    print("")
    time.sleep(timeSpeed * 3)

    #Turns
    for user in users:
        gameDeck = user.user_play(gameDeck, users, ai, dealer)
    for AI in ai:
        gameDeck += AI.ai_play(gameDeck,users, ai, dealer)
        time.sleep(timeSpeed * 1)
        print("")
    dealer.ai_play(gameDeck, users, ai, dealer,"The", Fore.MAGENTA)
    time.sleep(timeSpeed * 2)
    rpt_prt("", 40)

    #Show winner and cards
    for user in users:
        print(Fore.CYAN + "Player " + user.name + "'s" + Style.RESET_ALL + " results:")
        print(f"Cards: {user.DECK.cardsTo_str()}.")
        print(f"Has {user.DECK.weight(Fore.CYAN)}")
        print("")
        time.sleep(timeSpeed * 1)
    for AI in ai:
        print(Fore.GREEN + "AI " + AI.name + "'s" + Style.RESET_ALL + " results:")
        print(f"Cards: {AI.DECK.cardsTo_str()}.")
        print(f"Has {AI.DECK.weight(Fore.GREEN)}")
        print("")
        time.sleep(timeSpeed * 1)
    print(Fore.MAGENTA + "The dealer's" + Style.RESET_ALL + " results:")
    print(f"Cards: {dealer.DECK.cardsTo_str()}.")
    print(f"Has {dealer.DECK.weight(Fore.MAGENTA)}")
    print("")

    #end script
    print(Fore.YELLOW + Style.BRIGHT + f"Highest weight this session: {highScore}" + Style.RESET_ALL)
    if input_list("Choose...", ["Restart Game", "Exit"]) == "Exit":
        break