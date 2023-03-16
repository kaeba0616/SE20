import pygame, sys

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Load the font
font = pygame.font.SysFont(None, 24)


# Define the menu item class
class MenuItem:
    def __init__(self, text, x, y):
        self.text = text
        self.rect = pygame.Rect(x, y, 200, 50)
        self.hovered = False

    def draw(self, surface):
        color = (255, 255, 255)
        if self.hovered:
            color = (200, 200, 200)
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        text = font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)


# Define the menu items
menu_items = [
    MenuItem("Single Player", 300, 200),
    MenuItem("Settings", 300, 300),
    MenuItem("Exit", 300, 400),
]

# Define the opacity percentage and visibility flag
opacity_percent = 100
visible = True

# Define the key_list
key_list = [
    ("LEFT", "Left"),
    ("RIGHT", "Right"),
    ("UP", "Up"),
    ("DOWN", "Down"),
    ("RETURN", "Enter"),
    ("ESCAPE", "Esc"),
]


# Define the message box class
class MessageBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.visible = False

    def show(self, text, delay=0):
        self.text = text
        self.visible = True
        pygame.time.delay(delay)

    def hide(self):
        self.visible = False

    def draw(self, surface):
        if self.visible:
            pygame.draw.rect(surface, (255, 255, 255), self.rect)
            pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
            message_text = font.render(self.text, True, (0, 0, 0))
            message_rect = message_text.get_rect(center=self.rect.center)
            surface.blit(message_text, message_rect)


# Create the message box object
message_box = MessageBox(50, 50, 200, 100)

# Run the game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            for item in menu_items:
                if item.rect.collidepoint(event.pos):
                    item.hovered = True
                else:
                    item.hovered = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for item in menu_items:
                if item.rect.collidepoint(event.pos):
                    if item.text == "Single Player":
                        message_box.show("Starting single player game...", 2000)
                    elif item.text == "Settings":
                        message_box.show("Opening settings menu...", 2000)
                    elif item.text == "Exit":
                        pygame.quit()
                        sys.exit()

    # Draw the screen
    screen.fill((0, 0, 0))
    for item in menu_items:
        item.draw(screen)
    if visible:
        opacity_text = font.render(
            f"Opacity: {opacity_percent}%", True, (255, 255, 255)
        )
        screen.blit(opacity_text, (50, 500))
    else:
        message_box.hide()

    # Erase part of the screen
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 200, 600))

    # Draw the message box
    message_box.draw(screen)

    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)
