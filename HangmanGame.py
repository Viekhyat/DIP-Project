import pygame
import random
import os

class HangmanGame:
    def __init__(self):
        pygame.init()

        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("Hangman")

        self.clock = pygame.time.Clock()

        self.words = ["python", "panda3d", "game", "programming", "developer", "algorithm", "variable", "function", "loop", "class"]
        self.secret_word = ""
        self.letters_guessed = set()
        self.attempts_left = 6
        self.game_over = False
        self.won = False  # Flag to track if the player won

        self.font = pygame.font.Font(None, 36)
        self.message_font = pygame.font.Font(None, 48)

        self.image_folder = "images"
        self.gallows_image = self.load_image("gallows.png")  # Or "gallows.jpg"
        self.hangman_images = []
        for i in range(7):
            image = self.load_image(f"hangman_{i}.png")  # Or "hangman_{i}.jpg"
            self.hangman_images.append(image)

        self.start_new_game()

    def load_image(self, filename):
        filepath = os.path.join(self.image_folder, filename)
        try:
            image = pygame.image.load(filepath).convert_alpha()
            return image
        except pygame.error as e:
            print(f"Error loading image {filename}: {e}")
            return None

    def start_new_game(self):
        self.secret_word = random.choice(self.words).lower()
        self.letters_guessed = set()
        self.attempts_left = 6
        self.game_over = False
        self.won = False

    def guess_letter(self, letter):
        if self.game_over:
            return

        if letter in self.letters_guessed:
            return

        self.letters_guessed.add(letter)

        if letter not in self.secret_word:
            self.attempts_left -= 1
            if self.attempts_left == 0:
                self.game_over = True

    def draw(self):
        self.screen.fill((50, 50, 50))

        # Image Positions (Fixed on the right side)
        gallows_x = self.width - 300
        gallows_y = 50
        hangman_x = self.width - 250
        hangman_y = 100

        if self.gallows_image:
            self.screen.blit(self.gallows_image, (gallows_x, gallows_y))

        if self.hangman_images:
            hangman_stage = 6 - self.attempts_left
            if 0 <= hangman_stage < len(self.hangman_images) and self.hangman_images[hangman_stage] is not None:
                self.screen.blit(self.hangman_images[hangman_stage], (hangman_x, hangman_y))
            else:
                print("Hangman stage out of range or image is None:", hangman_stage)

        # Dynamic Text Positioning and Sizing
        word_text_y = 100
        guessed_text_y = 200
        attempts_text_y = 200
        message_text_y = 300

        word_font_scale = self.width / 800
        self.font = pygame.font.Font(None, int(36 * word_font_scale))
        self.message_font = pygame.font.Font(None, int(48 * word_font_scale))

        displayed_word = ""
        for letter in self.secret_word:
            displayed_word += letter + " " if letter in self.letters_guessed else "_ "
        word_text = self.font.render(displayed_word, True, (0, 0, 0))
        self.screen.blit(word_text, (self.width // 2 - word_text.get_width() // 2, word_text_y))

        guessed_text = self.font.render("Guessed: " + ", ".join(sorted(self.letters_guessed)), True, (0, 0, 0))
        self.screen.blit(guessed_text, (50, guessed_text_y))

        attempts_text = self.font.render("Attempts: " + str(self.attempts_left), True, (0, 0, 0))
        self.screen.blit(attempts_text, (self.width - 50 - attempts_text.get_width(), attempts_text_y))

        if self.attempts_left == 0:
            message = "Game Over! The word was: " + self.secret_word
            self.game_over = True
        elif all(letter in self.letters_guessed for letter in self.secret_word):
            message = "You Win!"
            self.game_over = True
            self.won = True
        else:
            message = ""

        message_text = self.message_font.render(message, True, (255, 0, 0) if self.attempts_left == 0 else (0, 255, 0))
        self.screen.blit(message_text, (self.width // 2 - message_text.get_width() // 2, message_text_y))

        if self.game_over:  # Show retry option
            retry_font = pygame.font.Font(None, int(36 * word_font_scale))
            retry_text = retry_font.render("Press 'r' to retry", True, (0, 0, 0))
            self.screen.blit(retry_text, (self.width // 2 - retry_text.get_width() // 2, message_text_y + 50))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key >= pygame.K_a and event.key <= pygame.K_z:
                        letter = chr(event.key)
                        self.guess_letter(letter)
                    if event.key == pygame.K_r and self.game_over:  # Retry
                        self.start_new_game()
                if event.type == pygame.VIDEORESIZE:
                    self.width = event.w
                    self.height = event.h
                    self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

            self.draw()
            self.clock.tick(60)

        pygame.quit()


game = HangmanGame()
game.run()