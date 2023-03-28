import pygame
import sys

# Initialize Pygame
pygame.init()

# Define screen dimensions
screen_width = 640
screen_height = 480

# Set up the game window
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the caption for the game window
pygame.display.set_caption("Configure Keys Example")

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the font for displaying text
font = pygame.font.Font(None, 36)

# Define the default keys used in the game
key_up = pygame.K_UP
key_down = pygame.K_DOWN
key_left = pygame.K_LEFT
key_right = pygame.K_RIGHT

# Define a dictionary to store the key mappings
key_map = {
    "up": key_up,
    "down": key_down,
    "left": key_left,
    "right": key_right
}

# Game loop
done = False
while not done:
    # Clear the screen
    screen.fill(WHITE)

    # Draw the current key mappings
    text = font.render(f"Up: {pygame.key.name(key_map['up']).capitalize()}", True, BLACK)
    screen.blit(text, (screen_width/2 - text.get_width()/2, screen_height/2 - text.get_height()/2 + 50))
    text = font.render(f"Down: {pygame.key.name(key_map['down']).capitalize()}", True, BLACK)
    screen.blit(text, (screen_width/2 - text.get_width()/2, screen_height/2 - text.get_height()/2 + 100))
    text = font.render(f"Left: {pygame.key.name(key_map['left']).capitalize()}", True, BLACK)
    screen.blit(text, (screen_width/2 - text.get_width()/2, screen_height/2 - text.get_height()/2 + 150))
    text = font.render(f"Right: {pygame.key.name(key_map['right']).capitalize()}", True, BLACK)
    screen.blit(text, (screen_width/2 - text.get_width()/2, screen_height/2 - text.get_height()/2 + 200))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == 27:
                pygame.quit()
                sys.exit()
            # Check for key presses
            for key, value in key_map.items():
                if event.key == value:
                    print(f"{key.capitalize()} key pressed!")
    
    
    
    # Draw some text on the screen
    text = font.render("Press keys to configure", True, BLACK)
    screen.blit(text, (screen_width/2 - text.get_width()/2, screen_height/2 - text.get_height()/2))
    
    # Update the screen
    pygame.display.flip()

    # Wait for key presses to configure game keys
    for key in key_map:
        while True:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                key_map[key] = event.key
                print(f"{key.capitalize()} key set to {pygame.key.name(event.key).capitalize()}")
                break
    
# Quit Pygame
pygame.quit()
sys.exit()
