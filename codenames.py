# This file's code (only this file) was made by Chat GPT and modified by me to fit my game.
import pygame
from game import Game

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Code Names")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (168, 50, 50)
GREEN = (0, 255, 0)
BLUE = (50, 129, 168)
NEUTRAL = (171, 163, 125)
BEIGE = (220, 210, 160)
GREY = (73, 73, 73)

# Set up fonts
font = pygame.font.Font("/Users/navyan21/Desktop/School 2023-2024/ATCS/CodeNames/JAi_____.TTF", 20)
font_start = pygame.font.Font("/Users/navyan21/Desktop/School 2023-2024/ATCS/CodeNames/JAi_____.TTF", 50)
font_game_over = pygame.font.Font("/Users/navyan21/Desktop/School 2023-2024/ATCS/CodeNames/JAi_____.TTF", 80)

# Define Game class
class PygameGame:
    def __init__(self, filename):
        # Initialize the game backend
        self.game = Game(filename)
        self.game.setup()
        self.game.run_turn()
        self.cards = []

        # Create Card objects based on backend Game
        positions = [(x * 180 + 75, y * 105 + 75) for y in range(5) for x in range(5)]
        for idx, card in enumerate(self.game.cards):
            self.cards.append((card.word, card.type, positions[idx], False))

    def handle_click(self, mouse_pos):
        # Handle click events on cards
        if self.game.game_over != True:
            for idx, card in enumerate(self.cards):
                card_rect = pygame.Rect(card[2][0], card[2][1], 150, 75)
                if card_rect.collidepoint(mouse_pos):
                    # Update game backend with the selected guess
                    self.game.make_guess(self.cards[idx][0])
                    # Change card color based on type
                    if card[1] == 1:
                        self.cards[idx] = (card[0], card[1], card[2], BLUE)
                    elif card[1] == 2:
                        self.cards[idx] = (card[0], card[1], card[2], RED)
                    elif card[1] == 3:
                        self.cards[idx] = (card[0], card[1], card[2], NEUTRAL)
                    elif card[1] == 4:
                        self.cards[idx] = (card[0], card[1], card[2], GREY)

    def display_board(self):
        # Display title
        text_surface = font_start.render("CODE NAMES", True, BLACK)
        text_rect = text_surface.get_rect(center=(500, 40))
        screen.blit(text_surface, text_rect)
        
        # Display cards
        for card in self.cards:
            card_rect = pygame.Rect(card[2][0], card[2][1], 150, 75)
            if isinstance(card[3], bool):
                pygame.draw.rect(screen, (BEIGE), card_rect)
            else:
                pygame.draw.rect(screen, card[3], card_rect)
            
            # Draw the text on the card
            text_surface = font.render(card[0], True, BLACK)
            text_rect = text_surface.get_rect(center=card_rect.center)
            screen.blit(text_surface, text_rect)

        # Display "GAME OVER" if the game is over
        if self.game.game_over == True:
            text_surface = font_game_over.render("GAME OVER", True, BLACK)
            text_rect = text_surface.get_rect(center=(500, 300))
            screen.blit(text_surface, text_rect)


if __name__ == "__main__":
    # Initialize the Pygame game
    pygame_game = PygameGame("/Users/navyan21/Desktop/School 2023-2024/ATCS/Labs/Unit07/IntroToNLP/data/words.txt")
    running = True
    while running:
        # Clear the screen
        screen.fill(WHITE)
        for event in pygame.event.get():
            # Handle events
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                pygame_game.handle_click(mouse_pos)

        # Draw the game board
        pygame_game.display_board()

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
