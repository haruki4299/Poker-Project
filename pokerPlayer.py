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
        # Print the player's name and their two cards
        s = self.name + ": " + self.hand[0].rank + " of " + self.hand[0].suit + ", " + self.hand[1].rank + " of " + self.hand[1].suit
        print(s)
    