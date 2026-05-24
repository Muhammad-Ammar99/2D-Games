import pygame
import random
from colors import PURPLE

pygame.mixer.init()
pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 255)

# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Bg img
img = pygame.image.load("glass.jpg")
img = pygame.transform.scale(img, (screen_width, screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption("Snake Master")
pygame.display.update()
font = pygame.font.SysFont("calibri", 30)
clock = pygame.time.Clock()

def screen_score(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((255, 255, 0))
        screen_score("Welcome to Snake Master", black, 250, 250)
        screen_score("Press Space Bar to Play", black, 265, 280)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load("back.mp3")
                    pygame.mixer.music.play()
                    game_loop()
        pygame.display.update()
        clock.tick(60)

# Game Loop
def game_loop():
    # Game specific variables
    exit_game = False
    game_over = False

    snake_x = 45
    snake_y = 55

    velocity_x = 8
    velocity_y = 0

    snake_size = 15

    food_x = random.randint(20, screen_width - 20)
    food_y = random.randint(20, screen_height - 20)

    try:
        with open("high_score.txt", "r") as f:
            high_score = int(f.read())
    except FileNotFoundError:
        high_score = 0

    snk_list = []
    snk_length = 1

    score = 0
    fps = 30

    while not exit_game:

        if game_over:
            with open("high_score.txt", "w") as f:
                f.write(str(high_score))

            gameWindow.fill(white)
            screen_score("Game Over! Press Enter to Continue", red, 250, 250)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.load("back.mp3")
                        pygame.mixer.music.play()
                        game_loop()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_RIGHT, pygame.K_d]:
                        velocity_x = 8
                        velocity_y = 0
                    elif event.key in [pygame.K_LEFT, pygame.K_a]:
                        velocity_x = -8
                        velocity_y = 0
                    elif event.key in [pygame.K_UP, pygame.K_w]:
                        velocity_y = -8
                        velocity_x = 0
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        velocity_y = 8
                        velocity_x = 0
                    elif event.key in [pygame.K_SPACE]:
                        score+=10

            snake_x += velocity_x
            snake_y += velocity_y

            # Update the collision detection for food
            if (snake_x < food_x + snake_size and
                snake_x + snake_size > food_x and
                snake_y < food_y + snake_size and
                snake_y + snake_size > food_y):
                score += 10
                food_x = random.randint(30, screen_width - 30)
                food_y = random.randint(40, screen_height - 40)
                snk_length += 5  # Increase snake length when food is eaten

            if score > high_score:
                high_score = score

            gameWindow.fill(white)
            gameWindow.blit(img, (0, 0))
            screen_score("Score: " + str(score) + "  High Score: " + str(high_score), PURPLE, 5, 5)

            head = [snake_x, snake_y]
            snk_list.append(head)

            # Check for self-collision
            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load("end.mp3")
                pygame.mixer.music.play()

            # Boundary check to end game if snake goes out of bounds
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load("end.mp3")
                pygame.mixer.music.play()

            # Ensure the snake grows as expected
            if len(snk_list) > snk_length:
                del snk_list[0]

            plot_snake(gameWindow, black, snk_list, snake_size)

            pygame.draw.circle(gameWindow, red, (food_x, food_y), 5)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()
