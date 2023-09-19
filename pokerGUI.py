# Poker Game with simple GUI

# 2023-09-16
# Basics of the game is done
# Comment on the Functions
# Work on the GUI (Can Wait)
# Organize code. Separate files?
# Work on getting the CPU making more logical decisions? (For Fun)
# Win Rate Calculator? (Optional)

import random
import itertools
import time
import pygame
import os

# Constants for card ranks and suits
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['hearts', 'diamonds', 'clubs', 'spades']

# Hand rankings used for poker evaluation
HAND_RANKINGS = {
            "high_card": 0,
            "one_pair": 1,
            "two_pairs": 2,
            "three_of_a_kind": 3,
            "straight": 4,
            "flush": 5,
            "full_house": 6,
            "four_of_a_kind": 7,
            "straight_flush": 8,
        }

# Define a Card class to represent playing cards
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        
        # Mapping of card ranks to integer values for poker hand evaluation
        rankToVal = {
            '2':2,
            '3':3,
            '4':4,
            '5':5,
            '6':6,
            '7':7,
            '8':8,
            '9':9,
            '10':10,
            'J':11,
            'Q':12,
            'K':13,
            'A':1
        }
        self.value = rankToVal[self.rank]
          
# Define a Deck class to represent a deck of playing cards
class Deck:
    def __init__(self):
        # Create a list of Card objects for a standard deck of 52 cards and shuffle it
        self.cards = [Card(rank,suit) for suit in suits for rank in ranks]
        random.shuffle(self.cards)
        
    def drawCard(self) -> Card:
        # Draw (pop) a card from the deck and return it
        return self.cards.pop()

# Define a Player class to represent a player in the poker game
class Player:
    def __init__(self, name: str, chips: int = 1000):
        self.name = name
        self.hand = []
        self.totalChips = chips
        self.currentBet = 0
        self.folded = False
        
    def fold(self):
        # Reset the current bet to 0 and mark the player as folded
        self.currentBet = 0
        self.folded = True
        
    def call(self, toMatch):
        # Calculate and perform a call action by the player
        diff = toMatch - self.currentBet
        if diff >= self.totalChips:
            # If the required bet is greater than or equal to the player's total chips, they go all-in
            self.currentBet += self.totalChips
            amount = self.totalChips
            self.totalChips = 0
            return amount
        else:
            # If the required bet is less than the player's total chips, they call that amount
            self.currentBet += diff
            self.totalChips -= diff
            return diff
    
    def raiseBet(self, toMatch) -> int:
        # Calculate and perform a raise action by the player
        diff = toMatch - self.currentBet
        raiseAmount = 0
        while True:
            raiseAmountStr = input("How many more chips would you like raise by?: ")
            if raiseAmountStr.isdigit():
                raiseAmount = int(raiseAmountStr)
                if raiseAmount > self.totalChips:
                    print("You do not have enough chips.")
                elif raiseAmount < diff:
                    print("You must raise by a larger amount. (To Match: " + str(diff) + ")")
                    raiseAmount = 0
                else:
                    break
            else:
                print("Input interger value.")
        # Update the player's total chips and current bet after the raise
        self.totalChips -= raiseAmount
        self.currentBet += raiseAmount
        
        return raiseAmount, self.currentBet
        
    def printStatus(self):
        # Print the player's total chips, current bet, and folded status
        totalChips = str(self.totalChips)
        currentBet = str(self.currentBet)
        s = "Total Chips: " + totalChips
        if self.folded == True:
            s = s + " | Folded"
        else:
            s = s + " | Current Bet: " + currentBet
        print(s)
        
    def printCards(self):
        # Print the player's name and their two hole cards
        s = self.name + ": " + self.hand[0].rank + " of " + self.hand[0].suit + ", " + self.hand[1].rank + " of " + self.hand[1].suit
        print(s)
    
        
# Define a CommunityCards class to represent the community cards on the table
class CommunityCards:
    def __init__(self):
        self.cards = []
    
    def printCards(self):
        # Print the community cards on the table
        print("The Community Cards:")
        s = ""
        for card in self.cards:
            if s != "":
                s += ", "
            s += card.rank + " of " + card.suit
        print(s)  

class Game:
    def __init__(self):
        # Initialize the game state
        self.players = []            # List to store player objects
        self.deck = Deck()           # Create a deck of cards
        self.communityCards = CommunityCards()  # Create an empty set of community cards
        self.smallAndBig = [0, 1]    # Index of small blind and big blind players
        self.toMatch = 0             # Current amount to match for betting
        self.pot = 0                # Total chips in the pot
        
    def addPlayers(self):
        """
        Add at least two players.

        Args:
            name (str): _description_
        """
        # Prompt players to enter their names and add them to the game
        print("Welcome to poker. Please add players to the game (min=2, max=6).")
        count = 1
        name = input(f"Enter your name (Player 1): ")
        ply = Player(name)
        self.players.append(ply)
        count += 1
        name = input(f"Enter name of player{count}: ")
        ply = Player(name)
        self.players.append(ply)
        addMore = True
        while addMore and count < 6:
            response = input("Would you like to add another player (y/n)?: ")
            if response == 'y':
                count += 1
                name = input(f"Enter name of player{count}: ")
                ply = Player(name)
                self.players.append(ply)
            elif response == 'n':
                addMore = False
            else:
                print("Please respond with (y/n)")
        
    def dealCards(self):
        for player in self.players:
            card = self.deck.drawCard()
            player.hand.append(card)
        for player in self.players:
            card = self.deck.drawCard()
            player.hand.append(card)
    
    def dealFlop(self):
        for i in range(3):
            card = self.deck.drawCard()
            self.communityCards.cards.append(card)
    
    def dealTurn(self):
        card = self.deck.drawCard()
        self.communityCards.cards.append(card)

    def dealRiver(self):
        card = self.deck.drawCard()
        self.communityCards.cards.append(card)
    
    def compareHands(self, handInfo1: list, handInfo2: list):
        """
        Compare two poker hands to determine the winner or a tie.

        Args:
            handInfo1 (list): Information about the first hand, including its type and relevant values.
            handInfo2 (list): Information about the second hand, including its type and relevant values.

        Returns:
            int: 1 if the first hand wins, 2 if the second hand wins, or 3 in case of a tie.
        """
        if HAND_RANKINGS[handInfo1[0]] > HAND_RANKINGS[handInfo2[0]]:
            return 1
        elif HAND_RANKINGS[handInfo1[0]] < HAND_RANKINGS[handInfo2[0]]:
            return 2
        else:
            if "straight_flush" == handInfo1[0] or "straight" == handInfo1[0]:
                if handInfo1[1] > handInfo2[1]:
                    return 1
                elif handInfo1[1] < handInfo2[1]:
                    return 2
                else:
                    return 3
            elif "full_house" == handInfo1[0]:
                # Change Ace value from 1 to 14
                if handInfo1[1] == 1:
                    handInfo1[1] += 13
                if handInfo1[2] == 1:
                    handInfo1[2] += 13
                if handInfo2[1] == 1:
                    handInfo2[1] += 13
                if handInfo2[2] == 1:
                    handInfo2[2] += 13
                # Compare card strengths
                if handInfo1[1] > handInfo2[1]:
                    return 1
                elif handInfo1[1] < handInfo2[1]:
                    return 2
                elif handInfo1[2] > handInfo2[2]:
                    return 1
                elif handInfo1[2] < handInfo2[2]:
                    return 2
                else:
                    return 3
            elif handInfo1[0] == "one_pair" or handInfo1[0] == "three_of_a_kind" or handInfo1[0] == "four_of_a_kind":
                # Change Ace value from 1 to 14
                if handInfo1[1] == 1:
                    handInfo1[1] += 13
                if handInfo2[1] == 1:
                    handInfo2[1] += 13
                # Compare card strengths
                if handInfo1[1] > handInfo2[1]:
                    return 1
                elif handInfo1[1] < handInfo2[1]:
                    return 2
                else:
                    return 3
            elif handInfo1[0] == "two_pairs":
                # Change Ace value from 1 to 14
                if handInfo1[1] == 1:
                    handInfo1[1] += 13
                if handInfo1[2] == 1:
                    handInfo1[2] += 13
                if handInfo2[1] == 1:
                    handInfo2[1] += 13
                if handInfo2[2] == 1:
                    handInfo2[2] += 13
                # Compare card strengths
                if handInfo1[1] > handInfo2[1]:
                    return 1
                elif handInfo1[1] < handInfo2[1]:
                    return 2
                elif handInfo1[2] > handInfo2[2]:
                    return 1
                elif handInfo1[2] < handInfo2[2]:
                    return 2
                else:
                    return 3
            else:
                # Change Ace value from 1 to 14
                if handInfo1[1] == 1:
                    handInfo1[1] += 13
                if handInfo2[1] == 1:
                    handInfo2[1] += 13
                # Compare card strengths
                for i in range(5):
                    if handInfo1[1+i] != handInfo2[1+i]:
                        if handInfo1[1+i] > handInfo2[1+i]:
                            return 1
                        elif handInfo1[1+i] < handInfo2[1+i]:
                            return 2
                return 3
                          
    def countCardsInHand(self, hand):
        """
        Count the occurrences of each card value in a given hand.

        Args:
            hand (list of Card): The hand for which card occurrences are counted.

        Returns:
            dict: A dictionary where keys represent card values (1-13) and values represent the number of occurrences
                of each card value in the hand.
        """
        cardCount = {
                2:0,
                3:0,
                4:0,
                5:0,
                6:0,
                7:0,
                8:0,
                9:0,
                10:0,
                11:0,
                12:0,
                13:0,
                1:0
            }
        for card in hand:
            cardCount[card.value] += 1
        return cardCount
        
    def findBestHand(self, player: Player) -> list:
        """
        Finds the best hand among the given player's cards and the community cards.

        Args:
            player: The player whose hand is being evaluated.

        Returns:
            A list representing the best hand, including the hand's name as a string and additional values if needed.
            For example, ["straight_flush", 10] or ["one_pair", 8, 6, 5].
        """
        sevenCards = []
        for card in player.hand:
            sevenCards.append(card)
        for card in self.communityCards.cards:
            sevenCards.append(card)
        combinations = itertools.combinations(sevenCards, 5)
        
        
        bestHand = []
        for hand in combinations:
            isFlush = True
            # Check for flush
            first = hand[0].suit
            for card in hand:
                if first != card.suit:
                    isFlush = False
            # Check for straight
            isStraight = False
            straightStart = 0
            valuesOfHand = []
            for card in hand:
                valuesOfHand.append(card.value)
            valuesOfHand.sort()
            if valuesOfHand == [1,10,11,12,13]:
                isStraight = True
                straightStart = 10
            for i in range(9):
                if valuesOfHand == [i+1,i+2,i+3,i+4,i+5]:
                    isStraight = True
                    straightStart = i+1
            # Count the Cards
            cardCount = self.countCardsInHand(hand)
            # Setting variables
            fourOfKind = False
            fourOfKindValue = 0
            
            threeOfKind = False
            threeOfKindValue = 0
            
            hasPair = False
            pairValue = 0
            pairValue2 = 0
            
            for key in cardCount:
                if cardCount[key] == 2 and hasPair == False:
                    hasPair = True
                    pairValue = key
                elif cardCount[key] == 2 and hasPair == True:
                    pairValue2 = key
                if cardCount[key] == 3:
                    threeOfKind = True
                    threeOfKindValue = key
                if cardCount[key] == 4:
                    fourOfKind = True
                    fourOfKindValue = key
            if fourOfKind == False and threeOfKind == False and hasPair == False and isStraight == False:
                highCard = 0
                secondHighCard = 0
                thirdHighCard = 0
                fourthHighCard = 0
                fifthHighCard = 0
                for key in cardCount:
                    if cardCount[key] != 0:
                        fifthHighCard = fourthHighCard
                        fourthHighCard = thirdHighCard
                        thirdHighCard = secondHighCard
                        secondHighCard = highCard
                        highCard = key
                        
            # Assign Proper name to the hand and save card values for comparing ties
            handInfo = []
            if isStraight == True and isFlush == True:
                handInfo.append("straight_flush")
                handInfo.append(straightStart)
            elif isStraight == True and isFlush == False:
                handInfo.append("straight")
                handInfo.append(straightStart)
            elif isStraight == False and isFlush == True:
                handInfo.append("flush")
                handInfo.append(highCard)
                handInfo.append(secondHighCard)
                handInfo.append(thirdHighCard)
                handInfo.append(fourthHighCard)
                handInfo.append(fifthHighCard)
            elif fourOfKind == True:
                handInfo.append("four_of_a_kind")
                handInfo.append(fourOfKindValue)
            elif threeOfKind == True and hasPair == True:
                handInfo.append("full_house")
                handInfo.append(threeOfKindValue)
                handInfo.append(pairValue)
            elif threeOfKind == True and hasPair == False:
                handInfo.append("three_of_a_kind")
                handInfo.append(threeOfKindValue)
            elif hasPair == True and pairValue2 != 0:
                handInfo.append("two_pairs")
                handInfo.append(pairValue2)
                handInfo.append(pairValue)
            elif hasPair == True and pairValue2 == 0:
                handInfo.append("one_pair")
                handInfo.append(pairValue)
            else:
                handInfo.append("high_card")
                handInfo.append(highCard)
                handInfo.append(secondHighCard)
                handInfo.append(thirdHighCard)
                handInfo.append(fourthHighCard)
                handInfo.append(fifthHighCard)
            if bestHand == []:
                bestHand = handInfo
            else:
                result = self.compareHands(bestHand, handInfo)
                if result == 2:
                    bestHand = handInfo
        return bestHand
    
    def printBoard(self, gameEnd):
        """
            Print the Cards on the Board and the individual chip situation

        Args:
            gameEnd (bool): If the round is at the end, show everyone's hand. If not only player 1
        """
        print("______________________________________________________________________")
        self.communityCards.printCards()
        print("Pot: " + str(self.pot))
        print("______________________________________________________________________")
        if gameEnd:
            for player in self.players:
                player.printCards()
                player.printStatus()
                print("______________________________________________________________________")
        else:
            for player in self.players:
                if player == self.players[0]:
                    player.printCards()
                    player.printStatus()
                else:
                    print(player.name + ": ")
                    player.printStatus()
                print("______________________________________________________________________")
        time.sleep(2)
            
    def printWinners(self, winners, bestHand):
        """
            Print the Winners of the game and what hand they won by

        Args:
            winners (list[Player]): A List of all the players that won
            bestHand (list[]): A list of all the winning hand and the card strength
        """
        winningHand = bestHand[0][0].replace('_',' ')
        print("The winners are:")
        for player in winners:
            print(player.name)
        print("With the winning hand of " + winningHand)
    
    def smallAndBigBets(self):
        """
            Start the game by getting the big and small blind bets
        """
        bigBlind = self.players[self.smallAndBig[1]]
        smallBlind = self.players[self.smallAndBig[0]]
        self.toMatch = 20
        if bigBlind.totalChips >= 20:
            bigBlind.totalChips -= 20
            bigBlind.currentBet += 20
        else:
            bigBlind.currentBet = bigBlind.totalChips
            bigBlind.totalChips = 0
        self.pot += bigBlind.currentBet
        if smallBlind.totalChips >= 10:
            smallBlind.totalChips -= 10
            smallBlind.currentBet += 10
        else:
            smallBlind.currentBet = smallBlind.totalChips
            smallBlind.totalChips = 0
        self.pot += smallBlind.currentBet
              
    def betting(self):
        """
            Play the round of betting
        """
        l = len(self.players)
        if len(self.communityCards.cards) == 0:
            start = (self.smallAndBig[1] + 1) % l
            cur = start
        else:
            start = (self.smallAndBig[0]) % l
            cur = start
        print("\nBetting Start\n")
        while True:
            player = self.players[cur]
            validMove = False
            while validMove == False and player.folded != True:
                if cur == 0 and player.totalChips != 0:
                    print(player.name + ": choose action from following (Enter: 1,2, or 3):")
                    move = input("1. Call/Check \n2. Raise \n3. Fold \nInput: ")
                else:
                    
                    move = "1"
                if move == "1":
                    # Call
                    print(player.name + " Call/Checks " + str(self.toMatch))
                    print("______________________________________________________________________\n")
                    validMove = True
                    self.pot += player.call(self.toMatch)
                elif move == "2":
                    # Raise
                    start = cur
                    raiseAmount, self.toMatch = player.raiseBet(self.toMatch)
                    self.pot += raiseAmount
                    print(self.toMatch)
                    print(player.name + " Raises by " + str(raiseAmount))
                    print("______________________________________________________________________\n")
                    validMove = True
                    pass
                elif move == "3":
                    # Fold
                    validMove = True
                    print(player.name + " Folds")
                    print("______________________________________________________________________\n")
                    player.fold()
                else:
                    print("Invalid Input. Please re-enter your choice.")
            
            cur = (cur + 1) % l
            time.sleep(1)
            if cur == start:
                break
        print("Betting Closed")
    
    def evalWinners(self):
        """
            Evaluate the winners based on the hands of the players
            
            Returns:
                winners: A list of all of the players that won
                bestHand: A list of the hand information of all the players that won in the same order
        """
        winners = []
        bestHand = []
        for player in self.players:
            if player.folded != True:
                if winners == []:
                    winners.append(player)
                    bestHand.append(self.findBestHand(player))
                else:
                    curBest = bestHand[0]
                    compHand = self.findBestHand(player)
                    result = self.compareHands(curBest, compHand)
                    if result == 2:
                        winners = []
                        bestHand = []
                        winners.append(player)
                        bestHand.append(compHand)
                    elif result == 3:
                        winners.append(player)
                        bestHand.append(compHand)
                    else:
                        pass
        return winners, bestHand
    
    def distributeWinnings(self, winners):
        """
            Distribute the pot to all of the winners

        Args:
            winners (List[Player]): A list of all of the winners in a round
        """
        pot = self.pot
        l = len(winners)
        winnings = pot // l
        for winner in winners:
            winner.totalChips += winnings
        for player in self.players:
            player.currentBet = 0
               
    def prepNewRound(self) -> bool:
        """
        Prepare for a new round of the game.

        Returns:
            bool: True if the main player has no chips left or is the last player remaining, else False.
        """
        # Reset the deck, community cards, and pot
        self.deck = Deck()
        self.communityCards = CommunityCards()
        self.pot = 0
        # If the main player has busted, they are out of the game
        if self.players[0].totalChips == 0:
            print("You have no chips left!")
            return True
        for player in self.players:
            player.folded = False
            player.hand = []
            if player.totalChips == 0:
                self.players.remove(player)
        # Rotate SBBB
        l = len(self.players)
        if l == 1:
            print("You are the last player remaining. You win!")
            return True
        self.smallAndBig[0] = (self.smallAndBig[0] + 1) % l
        self.smallAndBig[1] = (self.smallAndBig[1] + 1) % l
        return False
              
    def playRound(self) -> bool:
        # Take Small and Big Blind
        self.smallAndBigBets()
        self.dealCards()
        self.printBoard(False)
        self.betting()
        # Betting
        self.dealFlop()
        self.printBoard(False)
        self.betting()
        # Betting
        self.dealTurn()
        self.printBoard(False)
        self.betting()
        # Betting
        self.dealRiver()
        self.printBoard(False)
        self.betting()
        # Betting
        
        winners, bestHand = self.evalWinners()
        self.distributeWinnings(winners)
            
        self.printWinners(winners, bestHand)
        self.printBoard(True)
        return self.prepNewRound()
        
class PokerGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Poker Game")

        # Load card images
        self.card_images = self.load_card_images("images/PNG-cards-1.3/")
        
    def load_card_images(self, image_dir):
        card_images = {}
        for filename in os.listdir(image_dir):
            if filename.endswith(".png"):
                card_name = os.path.splitext(filename)[0]
                card_image = pygame.image.load(os.path.join(image_dir, filename))
                card_images[card_name] = card_image
        return card_images
    
    def draw_game(self):
        # Draw player hands, community cards, buttons, and other game elements
        pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # Handle other events like mouse clicks or button presses

    def run(self):
        while True:
            self.handle_events()
            self.draw_game()
            pygame.display.flip()
            
def main():
    game = Game()
    pokerGUI = PokerGUI()
    game.addPlayers()
    while True:
        print("______________________________________________________________________\n")
        print("Game Start")
        gameEnd = game.playRound()
        if gameEnd != True:
            cont = input("Would you like to continue? (y/n): ")
            if cont == 'n':
                break
        else:
            break
    print("Thank you for playing.")
    
main()
