# Create an uno game
# Outline:
# 1 - Create a circular queue for player order. - V
# 2 - Card class, a player deck is a list with card objects. - V
# 4 - create discarded deck (list, ADT not needed). - V
# 3 - List of all cards, popped card whenever card is drawn. When All cards list has no cards, shuffle discarded deck (use random to randomly select new cards). - V
# 4 - move validation (only if previous card is same colour or number, unless wildcard). - V
# 5 - create a win condition. - V
# 6 - Implement stacking +2 and +4 - X
# 7 - Implement putting down 2 or more identical at once - X
#So far:
#Created a game where cards can be played, then they are removed from player deck
##############Modules###############

from deck import DECK
import random as rnd

##############Constants#############

ALLCARDS = DECK
# DISCARDED means card is in play, so undrawable
DISCARDED = [[], [], [], [], []]


def deckEmpty():
    for i in range(len(ALLCARDS)):
        if len(ALLCARDS[i]) != 0:
            return False
    return True


##############Classes###############


class PlayerQueue:

    def __init__(self, playerN):
        self.frontpointer = 0
        self.length = playerN
        self.direction = 1
        self.data = []
        # Creates a list of players, from 1 to playerN
        for i in range(self.length):
            self.data.append(i + 1)

    # Returns next player number (index of player + 1)
    def nextPlayer(self):
        self.frontpointer += 1 * self.direction
        if self.direction == -1:
            if self.frontpointer == -1:
                self.frontpointer = self.length - 1
        else:
            self.frontpointer %= self.length
        self.data[self.frontpointer]
        return self.data[self.frontpointer]

    # Returns current player number (index of player + 1)
    @property
    def getCurrentPlayer(self):
        return self.data[self.frontpointer]

    def setDirection(self, d):
        self.direction = d


class Card:

    def __init__(self):
        self.colour = None
        self.number = None

    @property
    def drawCard(self):
        if not deckEmpty():
            drawing = True
        while drawing:
            colour = rnd.randint(0, len(ALLCARDS) - 1)  # colour list of cards
            if len(ALLCARDS[colour]) - 1 >= 0:
                number = rnd.randint(0,
                                     len(ALLCARDS[colour]) -
                                     1)  # number/element in list of cards
                self.colour = colour  # self.colour = number index of colour (0 = red, 1 = yellow, 2= blue, 3 = green, 4=wildcard/black)
                self.number = ALLCARDS[colour][number]
                DISCARDED[colour].append(
                    ALLCARDS[colour]
                    [number])  # Adds drawn card to discarded lsit
                ALLCARDS[colour].pop(number)  # removes card from allcards list
                drawing = False

    @property
    def getNumber(self):
        return self.number

    @property
    def getColour(self):
        return self.colour

    def __repr__(self):
        return f'C = {self.colour}, N = {self.number}'


class Uno:

    # playerDecks = list of N players, each player starts with 7 cards in deck
    def __init__(self, Nplayers):
        self.turn = 0
        self.playerQueue = PlayerQueue(Nplayers)
        self.playerDecks = []
        self.currentCard = Card()
        self.currentCard.drawCard
        self.punish = None

    def __createDeck(self):
        for i in range(self.playerQueue.length):
            self.playerDecks.append([])
            for j in range(7):
                self.playerDecks[i].append(Card())
                self.playerDecks[i][j].drawCard

    def __validateCardChoice(self, card):
        try:
            if self.currentCard.getColour == self.playerDecks[
                    self.playerQueue.getCurrentPlayer -
                    1][card -
                       1].getColour or str(self.currentCard.getNumber) == str(
                           self.playerDecks[self.playerQueue.getCurrentPlayer -
                                            1][card - 1].getNumber
                       ) or str(
                           self.playerDecks[self.playerQueue.getCurrentPlayer -
                                            1][card - 1].getColour) == '4':
                return True
        except:
            return False

    def __drawNewCard(self, n, punish):
        for i in range(n):
            c = Card()
            c.drawCard
            self.playerDecks[self.playerQueue.getCurrentPlayer - 1].append(c)
            if not punish:
                print('\033[1;37;40mCard drawn: ')
                self.__displayCard(c)

    def __enactCardAction(self, card):
        actions = ['X', '♺', '+2', '+4', '⊕']
        colours = ['r', 'y', 'g', 'b']
        colourDict = {'r': 0, 'g': 1, 'y': 2, 'b': 3}
        cardEnacted = self.playerDecks[self.playerQueue.getCurrentPlayer -
                                       1][card - 1]
        if cardEnacted.getNumber in actions:
            self.punish = cardEnacted.getNumber
            if cardEnacted.getColour == 4:
                picking = True
                while picking:
                    answer = input(
                        'What colour do you want to change the current card to? (r, y, b, g)'
                    ).lower()
                    if answer in colours:
                        self.currentCard.colour = colourDict[answer]
                        picking = False
                    else:
                        print('That is not a valid colour, try again.')

    def __displayCard(self, card):
        #\033[1;37;40m
        if card.getColour < 4:
            col = card.getColour + 31
        else:
            col = 37
        num = card.getNumber
        print(f'\033[1;{col};40m ' + f'\033[1;{col};40m_' *
              (2 + len(str(num))))
        print(f'\033[1;{col};40m|' + f'\033[1;{col};40m ' *
              (2 + len(str(num))) + '|')
        print(f'\033[1;{col};40m| ' + str(num) + f'\033[1;{col};40m |')
        print(f'\033[1;{col};40m|' + f'\033[1;{col};40m_' *
              (2 + len(str(num))) + f'\033[1;{col};40m|')

    @property
    #Create dict for the action cards so players understand which card does what
    def __displayDeck(self):
        index = self.playerQueue.getCurrentPlayer - 1
        for i in range(len(self.playerDecks[index])):
            print('\033[1;37;40mCard', i + 1)
            self.__displayCard(self.playerDecks[index][i])

    def __playTurn(self):
        picking = True
        print(f'\033[1;37;40mTurn {self.turn}')
        print('\033[1;37;40m=' *
              (14 + len(str(self.playerQueue.getCurrentPlayer))))
        print(
            f"\033[1;37;40mPlayer {self.playerQueue.getCurrentPlayer}'s turn")
        print('\033[1;37;40m=' *
              (14 + len(str(self.playerQueue.getCurrentPlayer))))
        print("\033[1;37;40mCurrent card: ")
        self.__displayCard(self.currentCard)
        print(
            f"\033[1;37;40mPlayer {self.playerQueue.getCurrentPlayer}'s deck: "
        )
        self.__displayDeck
        while picking:
            print(
                "\033[1;37;40mSelect card to play (i.e., 1, 2, 3, ...) or draw new card (any other input)"
            )
            answer = input()
            try:
                cardToPlay = int(answer)
            except ValueError:
                cardToPlay = answer
            if self.__validateCardChoice(cardToPlay):
                self.currentCard = self.playerDecks[
                    self.playerQueue.getCurrentPlayer - 1][cardToPlay - 1]
                self.__enactCardAction(cardToPlay)
                self.playerDecks[self.playerQueue.getCurrentPlayer -
                                 1].pop(cardToPlay - 1)
                picking = False
            else:
                print(
                    '\033[1;37;40mYou picked a card that does not exist, want to pick again? If not a new card will be drawn. (y/n),'
                )
                ans = input()
                if ans.lower() == 'n':
                    picking = False
                    self.__drawNewCard(1, False)

    def __reverse(self):
        self.playerQueue.direction = -1
        self.playerDecks.reverse()

    def __enactPunish(self):
        if self.punish == 'X':
            self.playerQueue.nextPlayer()
        elif self.punish == '♺':
            self.__reverse()
            self.playerQueue.nextPlayer()
        elif self.punish == '+2':
            self.__drawNewCard(2, True)
        elif self.punish == '+4':
            self.__drawNewCard(4, True)

    def __checkWin(self):
        if len(self.playerDecks[self.playerQueue.getCurrentPlayer - 1]) == 0:
            return True

    def startGame(self):
        playing = True
        self.__createDeck()
        while playing:
            if self.punish != None:
                self.__enactPunish()
                self.punish = None
            self.turn += 1
            self.__playTurn()
            if self.__checkWin():
                playing = False
            else:
                self.playerQueue.nextPlayer()
        print(
            f'\033[1;37;40mPlayer {self.playerQueue.getCurrentPlayer} has won!!!'
        )
