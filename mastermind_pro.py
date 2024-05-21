import pygame
import sys
import random

# Initialisierung von Pygame
pygame.init()

# Fenstergröße und Titel
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Mastermind Pro')

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (144, 238, 144)
ORANGE = (255, 165, 0)
LIGHT_ORANGE = (255, 200, 0)
COLORS = {
    'R': (255, 0, 0),
    'G': (0, 255, 0),
    'B': (0, 0, 255),
    'Y': (255, 255, 0),
    'O': (255, 165, 0),
    'P': (128, 0, 128),
    'C': (0, 255, 255),
    'M': (255, 0, 255)
}

# Funktionen zur Eingabeverarbeitung
def handle_circle_click(pos, circles):
    for i, circle in enumerate(circles):
        if (pos[0] - circle['x'])**2 + (pos[1] - circle['y'])**2 <= circle['radius']**2:
            return i
    return None

def feedback_color(black_pegs, white_pegs, index):
    if index < black_pegs:
        return GREEN
    elif index < black_pegs + white_pegs:
        return LIGHT_GREEN
    else:
        return WHITE

# Hauptspiel-Schleife
def main():
    # Initiale Einstellungen
    secret_code = generate_code()
    attempts = []
    current_guess = [None] * 5
    selected_circle = None
    check_button_active = False
    
    # Kreise für die Benutzereingabe
    input_circles = [{'x': 100 + i * 60, 'y': 300, 'radius': 20, 'color': WHITE, 'number': None} for i in range(5)]
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked_circle_index = handle_circle_click(pos, input_circles)
                if clicked_circle_index is not None:
                    selected_circle = clicked_circle_index
                    # Simulate dropdown selection for simplicity
                    selected_color = random.choice(list(COLORS.keys()))  # Replace with actual dropdown logic
                    selected_number = random.randint(1, 8)  # Replace with actual dropdown logic
                    input_circles[clicked_circle_index]['color'] = COLORS[selected_color]
                    input_circles[clicked_circle_index]['number'] = selected_number
                    current_guess[clicked_circle_index] = (selected_color, selected_number)
                    if None not in current_guess:
                        check_button_active = True
            elif event.type == pygame.MOUSEBUTTONDOWN and check_button_active:
                pos = pygame.mouse.get_pos()
                if 350 <= pos[0] <= 450 and 400 <= pos[1] <= 450:
                    black_pegs, white_pegs = check_guess(current_guess, secret_code)
                    attempts.append((current_guess.copy(), black_pegs, white_pegs))
                    current_guess = [None] * 5
                    input_circles = [{'x': 100 + i * 60, 'y': 300, 'radius': 20, 'color': WHITE, 'number': None} for i in range(5)]
                    check_button_active = False
                    if black_pegs == 5:
                        print("Congratulations! You've cracked the code!")
                        running = False
        
        # Bildschirm löschen
        screen.fill(WHITE)
        
        # Eingabekreise zeichnen
        for circle in input_circles:
            pygame.draw.circle(screen, circle['color'], (circle['x'], circle['y']), circle['radius'])
            if circle['number'] is not None:
                font = pygame.font.Font(None, 24)
                text = font.render(str(circle['number']), True, BLACK)
                screen.blit(text, (circle['x'] - 10, circle['y'] + 30))
        
        # Check-Button zeichnen
        if check_button_active:
            pygame.draw.rect(screen, GREEN, (350, 400, 100, 50))
            font = pygame.font.Font(None, 36)
            text = font.render("Check", True, BLACK)
            screen.blit(text, (370, 410))
        else:
            pygame.draw.rect(screen, (200, 200, 200), (350, 400, 100, 50))
            font = pygame.font.Font(None, 36)
            text = font.render("Check", True, BLACK)
            screen.blit(text, (370, 410))
        
        # Versuche anzeigen
        y_offset = 50
        for attempt in attempts:
            guess, black_pegs, white_pegs = attempt
            x_offset = 100
            for i, (color, number) in enumerate(guess):
                pygame.draw.circle(screen, COLORS[color], (x_offset, y_offset), 20)
                font = pygame.font.Font(None, 24)
                text = font.render(str(number), True, BLACK)
                screen.blit(text, (x_offset - 10, y_offset + 30))
                feedback = feedback_color(black_pegs, white_pegs, i)
                pygame.draw.circle(screen, feedback, (x_offset + 30, y_offset), 10)
                x_offset += 60
            y_offset += 60
        
        # Bildschirm aktualisieren
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

def generate_code(length=5, colors=list(COLORS.keys()), numbers=range(1, 9)):
    return [(random.choice(colors), random.choice(numbers)) for _ in range(length)]

def check_guess(guess, code):
    black_pegs = sum(g == c for g, c in zip(guess, code))
    color_matches = sum(min(guess.count(color), code.count(color)) for color, _ in set(code))
    number_matches = sum(min(guess.count(number), code.count(number)) for _, number in set(code))
    white_pegs = color_matches + number_matches - 2 * black_pegs
    return black_pegs, white_pegs

if __name__ == "__main__":
    main()
