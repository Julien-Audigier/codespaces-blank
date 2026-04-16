
import math
import random
from colorama import Fore, Style
import time

#Common functions

def askList(array: list, question: str):
    print(question)
    for i in range (0, len(array)):
        print(str(i+1) + ". " + str(array[i]))
    answer = input("")
    try:
        if int(answer) >= 0 & int(answer) <= len(array):
            return round(int(answer))
    except TypeError and ValueError:
        print("")
    askList(array, question)

def repeatPrt(string: str, NUM: int): #Prints something multiple times
    for i in range(1,NUM): #Repeats NUM times
        print(string) #Prints the string

#Common game functions

def deckToNum(deck: list):
    for i in range(0, len(deck)):
        try:
            deck[i] = int(deck[i][1].split(" ")[1]) #Changes card to number
        except (TypeError, ValueError):
                try:
                    if deck[i][1].split(" ")[1] == "Ace":
                        deck[i] = 11
                    else:
                        deck[i] = 10
                except TypeError:
                    deck[i] = deck[i]
    return(deck)

def newGameDeck(numDecks:int, suitCards:list):
    cardsOfEachSuit = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
    gameDeck = []
    for i in range(0, len(suitCards)): #Repeats for every suit, "i" is suit
        for d in range(0,numDecks):
            for c in range(0,len(cardsOfEachSuit)): 
                gameDeck.append([suitsCards[i][2], " ".join([suitsCards[i][1], cardsOfEachSuit[c]])]) #Adds the card, an array, to the game deck
    return(gameDeck)
        
def showCard(card:list, index:int, amount:int):
    if (index >= amount):
        print(card[0] + card[1], end = "") #Color + Value
        print(Style.RESET_ALL)
    else:
        print(card[0] + card[1], end=", ") #Color + Value

def showDeck(deck:list, name:str):
    print(str(name) + "'s cards showing:")
    for i in range(1, len(deck)):
        showCard(deck[i], i, len(deck)-1)

def cacProb(decks:list, pdeck:list, suitsCards: list, gameDeck:list):
    cardsShowing = []
    cardsLeft = [len(suitsCards),len(suitsCards),len(suitsCards),len(suitsCards),len(suitsCards),len(suitsCards),len(suitsCards),len(suitsCards),len(suitsCards),len(suitsCards)*4]
    for i in range(0, 2):
        for o in range(0, len(decks[i])):
            for q in range(1,len(decks[i][o])):
                cardsShowing.append(decks[i][o][q])
    for i in range(1, len(decks[2])):
        cardsShowing.append(decks[2][i])
    cardsShowing = deckToNum(cardsShowing)
    for i in range(0, len(pdeck)):
        cardsShowing.append(pdeck[i])
    for i in range(0, len(cardsShowing)):
        if cardsShowing[i] == 11:
            cardsLeft[0] -= 1
        else:
            cardsLeft[cardsShowing[i]-1] -= 1
    sum = 0
    for i in range(0, len(pdeck)):
        sum += pdeck[i]
    if sum >= 21:
        return(0)
    elif sum <= 11:
        return(100)
    temp = pdeck.count(11)
    while temp < 0:
        sum -= 10
        if sum == 21:
            return(0)
        elif sum >= 11:
            return(100)
    sum = 21 - sum
    prob = 0
    for i in range(0, sum+1):
        prob += cardsLeft[i]
    prob = prob/(len(gameDeck)+len(cardsShowing))
    return(prob*100)

def aiPlay(decks:list, aiNum:int, suitsCards:list, gameDeck:list):
    pDeck = []
    for i in range(0,len(decks[0][aiNum])):
        pDeck.append(decks[0][aiNum][i])
    pDeck = deckToNum(pDeck)
    sum = 0
    for i in range(0, len(pDeck)):
        sum += pDeck[i]
    if random.randint(1,100) <= (cacProb(decks, pDeck, suitsCards, gameDeck)-5) and sum < 21: #Hit
        print("AI " + str(aiNum) + " chose to hit,")
        time.sleep(0.5)
        decks[0][aiNum].append(gameDeck.pop(0))
        print("AI " + str(aiNum) + " drew the card:", end=" ")
        showCard(decks[0][aiNum][len(decks[0][aiNum])-1], 1, 1)
        time.sleep(2)
        tempList = aiPlay(decks, aiNum, suitsCards, gameDeck)
        time.sleep(2)
        decks = tempList[1]
        gameDeck = tempList[0]
    else:
        time.sleep(2)
        print("AI " + str(aiNum) + " chose to stay")
        time.sleep(3.5)
    repeatPrt("", 70)
    return([gameDeck, decks])

def dealerPlay(decks:list, suitsCards:list, gameDeck:list):
    pDeck = []
    for i in range(0,len(decks[2])):
        pDeck.append(decks[2][i])
    pDeck = deckToNum(pDeck)
    sum = 0
    for i in range(0, len(pDeck)):
        sum += pDeck[i]
    if random.randint(1,100) <= (cacProb(decks, pDeck, suitsCards, gameDeck)-5) and sum < 21: #Hit
        print("The dealer chose to hit,")
        time.sleep(0.5)
        decks[2].append(gameDeck.pop(0))
        print("The dealer drew the card:", end=" ")
        showCard(decks[2][len(decks[2])-1], 1, 1)
        time.sleep(2)
        tempList = dealerPlay(decks, suitsCards, gameDeck)
        time.sleep(2)
        decks = tempList[1]
        gameDeck = tempList[0]
        time.sleep(2)
    else:
        print("The dealer chose to stay")
        time.sleep(3.5)
        repeatPrt("", 70)
    return([gameDeck, decks])

#Game fuctions

def startGameLoop(gameDeck:list, numPlayers:int, numAi:int, suitsCards:list):
    aiDecks = []
    playerDecks = []
    for i in range(0, numAi):
        aiDecks.append([gameDeck.pop(0)])#add card + makes list
    for i in range(0, numPlayers):
        playerDecks.append([gameDeck.pop(0)])#add card + makes list
    dealerDeck = [gameDeck.pop(0)]#add card + makes list
    for i in range(0, numAi):
        aiDecks[i].append(gameDeck.pop(0))#adds card
    for i in range(0, numPlayers):
        playerDecks[i].append(gameDeck.pop(0))#adds card
    dealerDeck.append(gameDeck.pop(0))#adds card
    for i in range(0, len(aiDecks)):
        repeatPrt("", 70)
        tempList = aiPlay([aiDecks, playerDecks, dealerDeck], i, suitsCards, gameDeck)
        gameDeck = tempList[0]
        aiDecks = tempList[1][0]
    tempList = dealerPlay([aiDecks, playerDecks, dealerDeck], suitsCards, gameDeck)
    gameDeck = tempList[0]
    dealerDeck = tempList[1][2]
    for i in range(0, len(playerDecks)):
        repeatPrt("", 70)
        print("Player " + str(i+1) +"'s turn")
        repeatPrt("", 70)
        time.sleep(2.5)
        while (True):
            tempDeck = []
            for o in range(0,len(playerDecks[i])):
                tempDeck.append(playerDecks[i][o])
            tempDeck = deckToNum(tempDeck)
            sum = 0
            for o in range(0, len(tempDeck)):
                sum += tempDeck[o]
            if sum > 21:
                temp = tempDeck.count(11)
                while temp > 0:
                    sum -= 10
                    temp -= 1
                    if sum <= 21:
                        print("You got blackjack!")
                        time.sleep(3.5)
                        break
                    else:
                        print("You busted with a total of " + str(sum) + "!")
                        time.sleep(3.5)
                        break
                print("You busted with a total of " + str(sum) + "!")
                time.sleep(3.5)
                break
            elif sum == 21:
                print("You got blackjack!")
                time.sleep(3.5)
                break
            answer = askList(["See Cards", "Hit", "Stay"], "What do you want to do:")
            match answer:
                case 1: #See Cards
                    repeatPrt("", 70)
                    playerDecks[i].insert(0,"~")
                    showDeck(playerDecks[i], "Your")
                    for o in range(0, len(playerDecks)):
                        if (o != i):
                            showDeck(playerDecks[o], "Player " + str(o))
                    playerDecks[i].pop(0)
                    showDeck(dealerDeck, "Dealer")
                    for o in range(0, len(aiDecks)):
                        showDeck(aiDecks[o], "AI " + str(o+1))
                    repeatPrt("", 2)
                case 2: #Hit
                    repeatPrt("", 70)
                    playerDecks[i].append(gameDeck.pop(0))
                    print("You drew the card:", end=" ")
                    showCard(playerDecks[i][len(playerDecks[i])-1], 1, 1)
                    time.sleep(3.5)
                    repeatPrt("", 70)
                case 3: #Stay
                    repeatPrt("", 70)
                    print("You chose to stay")
                    time.sleep(3.5)
                    repeatPrt("", 70)
                    break
    sums = [[],[],[]]
    for o in range(0, len(playerDecks)):
        showDeck(playerDecks[o], "Player " + str(o))
        playerDecks[o] = deckToNum(playerDecks)
        sum = 0
        for i in range(0,len(playerDecks[o])):
            sum += playerDecks[o][i]
        print("sum = " + str(sum))
        sums[0].append(sum)
    showDeck(dealerDeck, "Dealer")
    sum = 0
    for i in range(0,len(dealerDeck)):
        sum +=dealerDeck[i]
    print("sum = " + str(sum))
    sums[1].append(sum)
    for o in range(0, len(aiDecks)):
        showDeck(aiDecks[o], "AI " + str(o+1))
        sum = 0
        for i in range(0,len(aiDecks[o])):
            sum += aiDecks[o][i]
        print("sum = " + str(sum))
        sums[2].append(sum)
    
        

def setupBlackjack(suitCards):
    try:
        repeatPrt("", 70)
        print("How many players: ")
        inputR = math.ceil(int(input(""))) #Find num. of players
        if inputR >= 1: #Check to make sure inputR is an int and >= 0
                numPlayers = inputR #Rephases inputR to numPlayers for better understanding
                while True: #Repeats forever until rules are met, use "break"
                    repeatPrt("", 70)
                    print("Number of AI players: ")
                    inputR = math.ceil(int(input(""))) #Find num. of AI players
                    if inputR >= 0: #Check to make sure inputR is an int and >= 0
                        numAi = inputR
                        break
                while True: #Repeats forever until rules are met, use "break"
                    repeatPrt("", 70)
                    print("How many decks: ")
                    inputR = math.ceil(int(input(""))) #Find num. of card decks
                    if inputR >= 1: #Check to make sure inputR is an int and >= 1
                        break
                numDecks = inputR #Rephases inputR to numDecks for better understanding
                gameDeck = newGameDeck(numDecks, suitCards) #Create decks
                random.shuffle(gameDeck)
                repeatPrt("", 70)
                startGameLoop(gameDeck, numPlayers, numAi,suitCards)
        else:
            setupBlackjack(suitsCards)
    except ValueError: #Rety if inputR doesn't meet rules
        setupBlackjack(suitCards)

#Start game

repeatPrt("", 40) #Clears screen
print(Fore.LIGHTBLUE_EX + "Link to colors: " + "https://www.geeksforgeeks.org/print-colors-python-terminal/")
print(Style.RESET_ALL)
repeatPrt("", 3)
time.sleep(3)

suitsCards = [["clubs", "♣", Fore.BLACK], ["diamonds", "♦", Fore.RED], ["hearts", "♥", Fore.RED], ["spades", "♠", Fore.BLACK]]
setupBlackjack(suitsCards)

#gameDeck = newGameDeck(1, suitsCards)
#random.shuffle(gameDeck)
#for i in range(0, len(gameDeck)):
    #print(gameDeck[i])
