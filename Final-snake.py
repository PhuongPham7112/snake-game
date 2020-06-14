import pygame
import time
import random

pygame.init()

# variables
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (25, 150, 25)
dark_green = (0, 75, 0)

font_size = 40
display_width = 600
display_height = 600
block_size = 10
apple_thickness = 20
font = pygame.font.SysFont(None, font_size)  # create font object
fps = 45

icon = pygame.image.load('C:/Users/Minh Phuong/PycharmProjects/working38/Pictures_for_snake/heart pixel art.png')
img = pygame.image.load('C:/Users/Minh Phuong/PycharmProjects/working38/Pictures_for_snake/output-onlinepngtools.png')
apple_img = pygame.image.load('C:/Users/Minh Phuong/PycharmProjects/working38/Pictures_for_snake/output-onlinepngtools (1).png')

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Slither')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()  # set this before the game logic
direction = 'right'


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_c:
                    paused = False
        gameDisplay.fill(white)
        screen_message('Paused game', black)
        screen_message('Press Q to quit, C to continue', red, 50)
        pygame.display.update()


def location_generator():
    apple_x = round(random.randrange(0, display_width - apple_thickness, 10))
    apple_y = round(random.randrange(0, display_height - apple_thickness, 10))
    return apple_x, apple_y


def game_menu():
    intro = True
    while intro:
        gameDisplay.fill(white)
        screen_message('Welcome to Slitherio', blue)
        screen_message('Press S to start, Q to quit, P to pause', blue, 50)
        pygame.display.update()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()


def snake_draw(snake_list):
    head = img
    if direction == 'right':
        head = pygame.transform.rotate(img, 270)
    elif direction == 'left':
        head = pygame.transform.rotate(img, 90)
    elif direction == 'up':
        head = img
    elif direction == 'down':
        head = pygame.transform.rotate(img, 180)

    gameDisplay.blit(head, (snake_list[-1][0], snake_list[-1][1]))
    #  head is the last item in the list because new blocks are constantly added => old ones stay at the bottom
    for x_y in snake_list[:-1]:
        pygame.draw.rect(gameDisplay, green, [x_y[0], x_y[1], block_size, block_size])


def screen_message(text, color, y_displace=0):
    screen_text = font.render(text, True, color)  # creating the idea of the font
    text_rect = screen_text.get_rect()
    text_rect.center = [display_width/2, display_height/2 + y_displace]
    gameDisplay.blit(screen_text, text_rect)


def player_score(score):
    score += 1
    print_score = font.render(str(score), True, black)
    text_rect = print_score.get_rect()
    text_rect.center = [20, 20]
    gameDisplay.blit(print_score, text_rect)


def apple(x, y):
    gameDisplay.blit(apple_img, (x, y))


def game_loop():

    global direction

    snake_list = []
    snake_length = 1

    gameExit = False
    gameOver = False

    head_x = display_width / 2
    head_y = display_height / 2

    head_x_change = 0
    head_y_change = 0

    apple_x, apple_y = location_generator()
    score = 0

    while not gameExit:

        while gameOver == True:  # menu screen when lose
            gameDisplay.fill(white)
            screen_message('Game Over', red)
            screen_message('Press C to continue, Q to quit', black, 50)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False  # to stop the gameOver loop in order to successfully re-assign gameExit
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():  # movements of the snake
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    head_x_change = -block_size
                    head_y_change = 0
                    direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    head_x_change = block_size
                    head_y_change = 0
                    direction = 'right'
                elif event.key == pygame.K_UP:
                    head_y_change = -block_size
                    head_x_change = 0
                    direction = 'up'
                elif event.key == pygame.K_DOWN:
                    head_y_change = block_size
                    head_x_change = 0
                    direction = 'down'
                elif event.key == pygame.K_p:
                    pause()
        head_x += head_x_change  # make the snake continuously move
        head_y += head_y_change

        if head_x >= display_width or head_x < 0 or head_y >= display_height or head_y < 0:  # boundaries
            head_x = display_width / 2
            head_y = display_height / 2
            gameOver = True

        snake_head = [head_x, head_y]
        snake_list.append(snake_head)  # update snake length

        for block in snake_list[:-1]:  # no going backward
            if snake_head == block and snake_length > 1:
                gameOver = True

        gameDisplay.fill(white)  # start, a clean slate
        apple(apple_x, apple_y)  # draw an apple
        snake_draw(snake_list)  # draw snake

        if head_x == apple_x and head_y == apple_y:  # collision check
            apple_x, apple_y = location_generator()
            score += 1
            snake_length += 1

        if (apple_x < head_x < apple_x + apple_thickness) and (apple_y < head_y < apple_y + apple_thickness):
            apple_x, apple_y = location_generator()
            score += 1
            snake_length += 1

        if (apple_y < head_y + block_size < apple_y + apple_thickness) and (apple_x < head_x + block_size <
                                                                              apple_x + apple_thickness):
            apple_x, apple_y = location_generator()
            score += 1
            snake_length += 1
        player_score(score - 1)
        if len(snake_list) > snake_length:
            del snake_list[0]  # making sure the length is suitable

        pygame.display.update()  # end, go back to start of loop
        clock.tick(fps)

    gameDisplay.fill(white)
    screen_message('Quit so soon?', red)
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    quit()


game_menu()
game_loop()
