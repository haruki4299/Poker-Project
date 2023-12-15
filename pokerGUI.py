class PokerGUI:
    def __init__(self):
        # gameState represents the following. The number represents the index of the current state.
        # [Start of Game, Dealing cards and preflop betting, dealing the flop and betting, dealing the turn and betting, dealing the river and betting, Show down, Round end]
        self.gameState = 0
        
        pygame.init()
        self.screenHeight = 750
        self.screenWidth = 1000
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption("Poker Game")
        
        self.POKER_GREEN = (51, 101, 77)
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.font = pygame.font.Font(None, 36)
        self.cardImages = self.loadCardImages("images/PNG-cards-1.3/")
        self.running = True

    def loadCardImages(self, imageDir):
        cardImages = {}
        for filename in os.listdir(imageDir):
            if filename.endswith(".png"):
                cardName = os.path.splitext(filename)[0]
                cardImagePath = imageDir + filename
                cardImages[cardName] = cardImagePath
        return cardImages
    
    def draw_game(self, game):
        # Clear the screen
        self.screen.fill(self.POKER_GREEN)
        
        # Draw card slots
        pygame.draw.rect(self.screen, self.BLACK, (self.screenWidth / 2 - 75, self.screenHeight - 200, 100, 150), width=2)  # Player's card slot 1
        pygame.draw.rect(self.screen, self.BLACK, (self.screenWidth / 2 + 75, self.screenHeight - 200, 100, 150), width=2)  # Player's card slot 2
        for i in range(5):
            x = self.screenWidth / 2 - 240 + i * 120 #50 + i * 120
            pygame.draw.rect(self.screen, self.BLACK, (x, 300, 100, 150), width=2)  # Community card slots

        # Draw player information
        player_info = "Player1; Total Chips: 1000, currentBet: 0"
        text = self.font.render(player_info, True, (255, 255, 255))
        self.screen.blit(text, (self.screen.get_width() - text.get_width() - 20, self.screen.get_height() - text.get_height() - 20))

        # Test for displaying card images
        cardImage = pygame.image.load(self.cardImages["2_of_spades"])
        cardImage = pygame.transform.scale(cardImage, (100, 150))
        self.screen.blit(cardImage, (self.screenWidth / 2 - 75, self.screenHeight - 200))
        
        # Update the display
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # Handle other events like mouse clicks or button presses
        if self.gameState == 0:
            pass
        elif self.gameState == 1:
            pass
        elif self.gameState == 2:
            pass
        elif self.gameState == 3:
            pass
        elif self.gameState == 4:
            pass
        elif self.gameState == 5:
            pass
        elif self.gameState == 6:
            pass
        
        
    def run(self, game):
        while self.running:
            self.handle_events()
            self.draw_game(game)
            pygame.display.update()
            
        pygame.quit()