# Poker Game with simple GUI

# 2023-09-13
# Start with just the game the betting will come later and then the CPU and then the graphics?
# The basics of the pocker code are complete. We can have two players that play each other no betting and see who had the better hand.
# Still need some brush ups. Think about functionality.
# Next Step Betting?

import random
import itertools

# Constants
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
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

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        
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
        
    
class Deck:
    def __init__(self):
        self.cards = [Card(rank,suit) for suit in suits for rank in ranks]
        random.shuffle(self.cards)
        
    def drawCard(self) -> Card:
        return self.cards.pop()
    
    
class Player:
    def __init__(self, name: str, chips: int = 1000):
        self.name = name
        self.hand = []
        self.chips = chips
        self.bet = 0
        self.folded = False
        
    def printCards(self):
        s = self.name + ": " + self.hand[0].rank + " of " + self.hand[0].suit + ", " + self.hand[1].rank + " of " + self.hand[1].suit
        print(s)
            
    
    def raiseBet(self, amount: int):
        if self.chips < amount:
            amount = self.chips
        self.chips -= amount
        self.bet += amount
    
    def callBet(self, valueToMatch):
        if valueToMatch > self.chips:
            self.bet += self.chips
            self.chips = 0
        else:
            self.chips = self.chips - (valueToMatch - self.bet)
            self.bet = valueToMatch
    
    def fold(self):
        pass
        
# Community Cards
class CommunityCards:
    def __init__(self):
        self.cards = []
    
    def printCards(self):
        print("The Community Cards:")
        s = ""
        for card in self.cards:
            if s != "":
                s += ", "
            s += card.rank + " of " + card.suit
        print(s)  

class Game:
    def __init__(self):
        self.players = []
        self.deck = Deck()
        self.communityCards = CommunityCards()
        
    def addPlayers(self):
        """
        Add at least two players.

        Args:
            name (str): _description_
        """
        print("Welcome to poker. Please add players to the game (min=2, max=6).")
        count = 1
        name = input(f"Enter name of player{count}: ")
        ply = Player(name)
        self.players.append(ply)
        count += 1
        name = input(f"Enter name of player{count}: ")
        ply = Player(name)
        self.players.append(ply)
        addMore = True
        while addMore and count < 7:
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
            elif handInfo1[0] == "one_pair" or handInfo1[0] == "two_pairs" or handInfo1[0] == "three_of_a_kind" or handInfo1[0] == "four_of_a_kind":
                if handInfo1[1] > handInfo2[1]:
                    return 1
                elif handInfo1[1] < handInfo2[1]:
                    return 2
                else:
                    return 3
            else:
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
    
    def printBoard(self):
        self.communityCards.printCards()
        for player in self.players:
            player.printCards()
            
    def printWinners(self, winners, bestHand):
        winningHand = bestHand[0][0].replace('_',' ')
        print("The winners are:")
        for player in winners:
            print(player.name)
        print("With the winning hand of " + winningHand)
    
    def playRound(self) -> list[Player]:
        self.dealCards()
        # Betting
        self.dealFlop()
        self.dealTurn()
        self.dealRiver()
        # Evaluating the winner
        winners = []
        bestHand = []
        for player in self.players:
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
        
        self.printBoard()
        self.printWinners(winners, bestHand)
        
        
        
def main():
    game = Game()
    game.addPlayers()
    game.playRound()
    
main()
