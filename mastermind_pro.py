import pygame
import sys
import random

# Initialisierung von Pygame
pygame.init()

# Fenstergröße und Titel
screen_size = (1200, 800)
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

def draw_dropdown_menu(screen, x, y, options):
    menu_width, menu_height = 60, len(options) * 30
    pygame.draw.rect(screen, BLACK, (x, y, menu_width, menu_height), 2)
    for i, option in enumerate(options):
        color, number = option
        pygame.draw.circle(screen, COLORS[color], (x + 15, y + 15 + i * 30), 10)
        font = pygame.font.Font(None, 24)
        text = font.render(str(number), True, BLACK)
        screen.blit(text, (x + 30, y + 10 + i * 30))

# Hauptspiel-Schleife
def main():
    # Initiale Einstellungen
    secret_code = generate_code()
    attempts = []
    current_guess = [None] * 5
    selected_circle = None
    check_button_active = False
    dropdown_active = False
    dropdown_position = (0, 0)
    
    # Kreise für die Benutzereingabe
    input_circles = [{'x': 100 + i * 100, 'y': 300, 'radius': 30, 'color': WHITE, 'number': None} for i in range(5)]
    dropdown_options = [(color, num) for color in COLORS.keys() for num in range(1, 9)]
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if dropdown_active:
                    # Überprüfung, ob eine Auswahl im Dropdown getroffen wurde
                    dropdown_x, dropdown_y = dropdown_position
                    if dropdown_x <= pos[0] <= dropdown_x + 60 and dropdown_y <= pos[1] <= dropdown_y + len(dropdown_options) * 30:
                        selected_option_index = (pos[1] - dropdown_y) // 30
                        selected_color, selected_number = dropdown_options[selected_option_index]
                        input_circles[selected_circle]['color'] = COLORS[selected_color]
                        input_circles[selected_circle]['number'] = selected_number
                        current_guess[selected_circle] = (selected_color, selected_number)
                        dropdown_active = False
                        if None not in current_guess:
                            check_button_active = True
                            print('All circles filled, check button active')
                else:
                    clicked_circle_index = handle_circle_click(pos, input_circles)
                    if clicked_circle_index is not None:
                        selected_circle = clicked_circle_index
                        dropdown_position = (input_circles[clicked_circle_index]['x'], input_circles[clicked_circle_index]['y'] + 40)
                        dropdown_active = True
                    elif check_button_active and 350 <= pos[0] <= 450 and 500 <= pos[1] <= 550:
                        black_pegs, white_pegs = check_guess(current_guess, secret_code)
                        attempts.append((current_guess.copy(), black_pegs, white_pegs))
                        current_guess = [None] * 5
                        input_circles = [{'x': 100 + i * 100, 'y': 300, 'radius': 30, 'color': WHITE, 'number': None} for i in range(5)]
                        check_button_active = False
                        print(f'Checked guess: {black_pegs} black pegs, {white_pegs} white pegs')
                        if black_pegs == 5:
                            print("Congratulations! You've cracked the code!")
                            running = False
        
        # Bildschirm löschen
        screen.fill(WHITE)
        
        # Eingabekreise zeichnen
        for i, circle in enumerate(input_circles):
            pygame.draw.circle(screen, BLACK, (circle['x'], circle['y']), circle['radius'] + 2)  # Schwarze Umrandung
            pygame.draw.circle(screen, circle['color'], (circle['x'], circle['y']), circle['radius'])
            if circle['number'] is not None:
                font = pygame.font.Font(None, 24)
                text = font.render(str(circle['number']), True, BLACK)
                screen.blit(text, (circle['x'] - 10, circle['y'] + 30))
        
        # Dropdown-Menü zeichnen
        if dropdown_active:
            draw_dropdown_menu(screen, dropdown_position[0], dropdown_position[1], dropdown_options)
        
        # Check-Button zeichnen
        if check_button_active:
            pygame.draw.rect(screen, GREEN, (350, 500, 100, 50))
            font = pygame.font.Font(None, 36)
            text = font.render("Check", True, BLACK)
            screen.blit(text, (370, 510))
        else:
            pygame.draw.rect(screen, (200, 200, 200), (350, 500, 100, 50))
            font = pygame.font.Font(None, 36)
            text = font.render("Check", True, BLACK)
            screen.blit(text, (370, 510))
        
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
