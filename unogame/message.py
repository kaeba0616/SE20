import pygame, sys

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Load the font
font = pygame.font.SysFont(None, 24)

# Define the keyboard list
keys = [
    ("LEFT", pygame.K_LEFT),
    ("RIGHT", pygame.K_RIGHT),
    ("UP", pygame.K_UP),
    ("DOWN", pygame.K_DOWN),
    ("RETURN", pygame.K_RETURN),
    ("ESCAPE", pygame.K_ESCAPE),
]

# Define the opacity percentage and visibility flag
opacity_percent = 100
visible = True


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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                visible = not visible
            elif event.key == pygame.K_UP:
                opacity_percent = min(opacity_percent + 10, 100)
            elif event.key == pygame.K_DOWN:
                opacity_percent = max(opacity_percent - 10, 0)
            else:
                keys_text = ", ".join([name for name, key in keys])
                message_box.show(f"Available keys: {keys_text}", 2000)

    # Draw the screen
    screen.fill((0, 0, 0))
    if visible:
        for i, (name, key) in enumerate(keys):
            text = font.render(
                f"{name}: {pygame.key.name(key)}",
                True,
                (255, 255, 255, opacity_percent * 255 // 100),
            )
            screen.blit(text, (50, 50 + i * 30))
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
