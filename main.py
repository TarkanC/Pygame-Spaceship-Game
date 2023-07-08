import pygame
import os

pygame.font.init()
pygame.mixer.init()

# Window dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

# Color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Game elements
BORDER = pygame.Rect(SCREEN_WIDTH // 2 - 5, 0, 10, SCREEN_HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))
WINNER_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Winner.mp3"))

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

FPS = 60
VELOCITY = 10
BULLET_VELOCITY = 15
MAX_BULLETS = 6

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Spaceship dimensions
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# Load and transform spaceship images
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
YELLOW_SPACESHIP = pygame.transform.rotate(YELLOW_SPACESHIP, 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
RED_SPACESHIP = pygame.transform.rotate(RED_SPACESHIP, 270)

SPACE_BACKGROUND = pygame.image.load(os.path.join("Assets", "space.png"))
SPACE_BACKGROUND = pygame.transform.scale(SPACE_BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    """
    Draw the game window with all the game elements.

    Args:
        red (pygame.Rect): Red spaceship's rectangle.
        yellow (pygame.Rect): Yellow spaceship's rectangle.
        red_bullets (list): List of red bullets.
        yellow_bullets (list): List of yellow bullets.
        red_health (int): Red spaceship's health.
        yellow_health (int): Yellow spaceship's health.

    Returns:
        None
    """
    WINDOW.blit(SPACE_BACKGROUND, (0, 0))

    pygame.draw.rect(WINDOW, BLACK, BORDER)

    # Render health text
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)

    # Draw health text on the window
    WINDOW.blit(red_health_text, (SCREEN_WIDTH - red_health_text.get_width() - 10, 10))
    WINDOW.blit(yellow_health_text, (10, 10))

    # Draw spaceships on the window
    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))

    # Draw bullets on the window
    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    """
    Handle the movement of the yellow spaceship based on the keys pressed.

    Args:
        keys_pressed (list): List of boolean values representing the keys being pressed.
        yellow (pygame.Rect): Yellow spaceship's rectangle.

    Returns:
        None
    """
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0:  # LEFT
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0:  # UP
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < SCREEN_HEIGHT - 15:  # DOWN
        yellow.y += VELOCITY


def red_handle_movement(keys_pressed, red):
    """
    Handle the movement of the red spaceship based on the keys pressed.

    Args:
        keys_pressed (list): List of boolean values representing the keys being pressed.
        red (pygame.Rect): Red spaceship's rectangle.

    Returns:
        None
    """
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width:  # LEFT
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY + red.width < SCREEN_WIDTH + 10:  # RIGHT
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0:  # UP
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height < SCREEN_HEIGHT - 15:  # DOWN
        red.y += VELOCITY


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    """
    Handle the movement and collisions of bullets.

    Args:
        yellow_bullets (list): List of yellow bullets.
        red_bullets (list): List of red bullets.
        yellow (pygame.Rect): Yellow spaceship's rectangle.
        red (pygame.Rect): Red spaceship's rectangle.

    Returns:
        None
    """
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > SCREEN_WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    """
    Draw the winner text on the screen.

    Args:
        text (str): Text to display as the winner.

    Returns:
        None
    """
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WINDOW.blit(draw_text, (SCREEN_WIDTH / 2 - draw_text.get_width() / 2,
                            SCREEN_HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    """
    Main game loop.

    Returns:
        None
    """
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 5
    yellow_health = 5

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            WINNER_SOUND.play()
            draw_winner(winner_text)  # someone won
            break

        keys_pressed = pygame.key.get_pressed()

        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()


if __name__ == "__main__":
    main()
