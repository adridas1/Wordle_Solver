import pygame
import sys
import random
import engine

def initialize_game():
    """Set up the game environment."""
    pygame.init()
    pygame.display.set_caption("Wordle Clone")
    return pygame.display.set_mode((800, 800))

def load_word_list(filename):
    """Load the word list from a file."""
    try:
        with open(filename, "r") as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print("Dictionary file not found.")
        sys.exit()

def pick_random_word(wordlist):
    """Pick a random word from the list."""
    return random.choice(wordlist)

def draw_grid(screen, rows, cols, base_x, base_y, rect_size, padding):
    """Draw the grid for the Wordle game."""
    rects = []
    for row in range(rows):
        row_rects = []
        for col in range(cols):
            x = base_x + col * (rect_size + padding)
            y = base_y + row * (rect_size + padding)
            rect = pygame.Rect(x, y, rect_size, rect_size)
            pygame.draw.rect(screen, (100, 100, 100), rect, 2)
            row_rects.append(rect)
        rects.append(row_rects)
    return rects

def display_message(screen, text, position, color=(255, 108, 108), font_size=40, center=False):
    """Display a message on the screen."""
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    if center:
        position = (screen.get_width() // 2 - text_surface.get_width() // 2, position[1])
    screen.blit(text_surface, position)

def draw_title(screen, base_x, base_y):
    """Draw the Wordle title at the top of the screen."""
    font = pygame.font.Font(None, 80)
    title_surface = font.render("WORDLE", True, (255, 255, 255))
    underline_start = (base_x, base_y - 20)
    underline_end = (base_x + 5 * (50 + 10) - 10, base_y - 20)
    screen.blit(title_surface, (screen.get_width() // 2 - title_surface.get_width() // 2, base_y - 100))
    pygame.draw.line(screen, (255, 255, 255), underline_start, underline_end, width=2)

def handle_input(event, current_word, max_length):
    """Improved input handling that filters out non-alphabetic keys."""
    if event.key == pygame.K_BACKSPACE:
        return current_word[:-1]
    elif event.unicode.isalpha() and len(current_word) < max_length:
        return current_word + event.unicode.upper()
    return current_word

def calculate_base_offsets(screen_width, screen_height, cols, rows, rect_size, padding):
    """Calculate base offsets for grid placement."""
    base_x = (screen_width - (cols * rect_size + (cols - 1) * padding)) // 2
    base_y = (screen_height - (rows * rect_size + (rows - 1) * padding)) // 2
    return base_x, base_y

def evaluate_guess(guess, secret_word):
    """Provide feedback for a user's guess with better handling for repeated letters."""
    feedback = ['X'] * len(guess)
    secret_counts = {}

    # First pass to mark correct positions
    for i in range(len(guess)):
        if guess[i] == secret_word[i]:
            feedback[i] = '✓'
        else:
            if secret_word[i] in secret_counts:
                secret_counts[secret_word[i]] += 1
            else:
                secret_counts[secret_word[i]] = 1

    # Second pass to mark misplaced letters
    for i in range(len(guess)):
        if feedback[i] == 'X' and guess[i] in secret_counts and secret_counts[guess[i]] > 0:
            feedback[i] = '~'
            secret_counts[guess[i]] -= 1

    return feedback

def main():
    def restart_game():
        main()

    # Initialize game settings
    screen = initialize_game()
    clock = pygame.time.Clock()
    word_list = load_word_list("dictionary_wordle.txt")
    secret_word = pick_random_word(word_list).upper()
    game_engine = engine.Engine(word_list)

    # Constants
    ROWS, COLS = 6, 5
    RECT_SIZE = 50
    PADDING = 10
    BASE_X, BASE_Y = calculate_base_offsets(800, 800, COLS, ROWS, RECT_SIZE, PADDING)

    current_word = ""
    attempts = []
    feedbacks = []
    game_over = False
    invalid_message = None
    end_message = None
    guess_updated = False

    # Get the first suggestion at the start of the game
    suggested_guess = game_engine.find_best_guess([], [])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    restart_game()
                elif not game_over:
                    if event.key == pygame.K_RETURN and len(current_word) == COLS:
                        if current_word.lower() not in word_list:
                            invalid_message = "Invalid word"
                        else:
                            invalid_message = None
                            feedback = evaluate_guess(current_word, secret_word)
                            attempts.append(current_word.lower())
                            feedbacks.append(feedback)
                            guess_updated = True
                            if all(f == "✓" for f in feedback):
                                game_over = True
                                end_message = "You Win! Press 'R' to restart."
                            elif len(attempts) == ROWS:
                                game_over = True
                                end_message = f"Game Over! The word was: {secret_word}. Press 'R' to restart."
                            current_word = ""
                    elif event.key != pygame.K_RETURN:
                        current_word = handle_input(event, current_word, COLS)

        screen.fill((20, 20, 20))

        # Draw title
        draw_title(screen, BASE_X, BASE_Y)

        # Draw grid
        rects = draw_grid(screen, ROWS, COLS, BASE_X, BASE_Y, RECT_SIZE, PADDING)

        # Render previous guesses and feedback
        font = pygame.font.Font(None, 65)
        for row, (word, feedback) in enumerate(zip(attempts, feedbacks)):
            word = word.upper()
            for col, (letter, fb) in enumerate(zip(word, feedback)):
                x, y = BASE_X + col * (RECT_SIZE + PADDING), BASE_Y + row * (RECT_SIZE + PADDING)
                color = (0, 185, 6) if fb == "✓" else (255, 193, 53) if fb == "~" else (50, 50, 50)
                pygame.draw.rect(screen, color, rects[row][col])
                letter_surface = font.render(letter, True, (255, 255, 255))
                letter_rect = letter_surface.get_rect(center=(x + RECT_SIZE // 2, y + RECT_SIZE // 2))
                screen.blit(letter_surface, letter_rect.topleft)

        # Render current word
        for col, letter in enumerate(current_word):
            letter_surface = font.render(letter, True, (255, 255, 255))
            x, y = BASE_X + col * (RECT_SIZE + PADDING), BASE_Y + len(attempts) * (RECT_SIZE + PADDING)
            letter_rect = letter_surface.get_rect(center=(x + RECT_SIZE // 2, y + RECT_SIZE // 2))
            screen.blit(letter_surface, letter_rect.topleft)

        # Suggest a guess
        if not game_over:
            if guess_updated:
                suggested_guess = game_engine.find_best_guess(attempts, feedbacks)
                guess_updated = False
            display_message(screen, f"Suggestion: {suggested_guess.upper()}", (BASE_X - 225, BASE_Y + 15 + len(attempts) * (RECT_SIZE + PADDING)), color=(255, 255, 255), font_size=30)

        # Display invalid word message if needed
        if invalid_message:
            display_message(screen, invalid_message, (0, BASE_Y + ROWS * (RECT_SIZE + PADDING) + 20), font_size=30, center=True)

        # Display end message if game is over
        if end_message:
            display_message(screen, end_message, (0, BASE_Y + ROWS * (RECT_SIZE + PADDING) + 50), color=(255, 255, 255), font_size=30, center=True)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
