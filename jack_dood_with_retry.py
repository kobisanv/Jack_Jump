# import modules
import random
import pygame
from pygame import mixer
import math
import os
from slapjack import SlapJack

# initialize pygame
pygame.init() 

#welcome message
print("Welcome to Jack Jump.")
print("Jump from platform to platform in order to survive!")
print("Use the key A to move left | Use the key D to move right")
print("Hope you enjoy the game!")

# create window dimensions
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600 

# create window 
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Jack Jump")

# set frame rate
clock = pygame.time.Clock()
FPS = 60

# game variables
SCROLL_THRESH = 200 # threshold for player to pass so background can scroll
GRAVITY = 1 
MAX_PLATFORMS = 20 # max platforms before platforms start deleting 
SCROLL = 0 
bg_scroll = 0
game_over = False
score = 0
cont_choice = ""
retried = False

if os.path.exists('score.txt'): 
    with open('score.txt', 'r') as file:
        high_score = int(file.read()) # read the high score from file 
else:
    high_score = 0 # set high score to 0 when first playing

# importing audio
mixer.init()
mixer.music.load('amazonrainforest.mp3')
mixer.music.set_volume(0.2)
mixer.music.play()

# define color
WHITE = (255, 255, 255)
BLACK = (0,0,0)
PANEL = (254, 117, 234)

# define fonts
font_small = pygame.font.SysFont('Consolas', 20)
font_big = pygame.font.SysFont('Consolas', 24)

# import images
jumpy_image = pygame.image.load('1Jack_Character.png').convert_alpha()
jumpy_dim = (64, 64)
jumpy_image = pygame.transform.scale(jumpy_image, jumpy_dim)

#Parameters for infinite bg
bg_image = pygame.image.load('bg.png').convert_alpha()
bg_height = bg_image.get_height()
bg_dim = (400, bg_height)

tiles = math.ceil (WINDOW_HEIGHT / bg_height) # ensures the background goes through an infinite scroll as user plays
bg_image = pygame.transform.smoothscale(bg_image, bg_dim)

platform_image = pygame.image.load('vine.png').convert_alpha()
platform_dim = (1654, 66)
platform_image = pygame.transform.smoothscale(platform_image, platform_dim)

# function for outputting text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# function for drawing the background
def draw_bg(bg_scroll):
    screen.blit(bg_image, (0, 0 + bg_scroll))
    screen.blit(bg_image, (0, -600 + bg_scroll))

# function for drawing info panel
def draw_panel():
    pygame.draw.rect(screen, PANEL, (0, 0, WINDOW_WIDTH, 22))
    draw_text('SCORE: ' + str(score), font_small, BLACK, 0, 0)

# player class
class Player():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(jumpy_image, (45,45))
        self.width = 30
        self.height = 40
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False

    def move(self):
        dx = 0
        dy = 0
        SCROLL = 0
        
        key = pygame.key.get_pressed()
        if key[pygame.K_a]: # left
            dx = -11 # sensitivity
            self.flip = True
        if key[pygame.K_d]: # right
            dx = 11 # sensitivity
            self.flip = False

        # gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # ensure player doesn't go off the edge of the screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > WINDOW_WIDTH:
            dx = WINDOW_WIDTH - self.rect.right

        # check collision with platforms
        for platform in platform_group:
            # check for collision in y axis 
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if above the platform 
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20

        # check if the player has bounced to the top of the screen
        if self.rect.top <= SCROLL_THRESH:
            # if player is jumping, scroll up, if not, keep background static
            if self.vel_y < 0:
                SCROLL = -dy

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy + SCROLL # scroll is a vertical variable so it has to be added to delta y 

        return SCROLL


    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5))

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width + 20, 15))
        self.moving = moving
        self.move_counter = random.randint(0, 50)
        self.direction = random.choice([-1, 1]) 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def update(self, scroll):
        # moving platform from side to side (if platform is flagged as moving)
        if self.moving == True:
            self.move_counter += 1
            self.rect.x += self.direction
        else:
            pass
        # changing platform direction if it collided with wall
        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > WINDOW_WIDTH:
            self.direction *= -1
            self.move_counter = 0
        # update platform's vertical position
        self.rect.y += scroll
        # check if platform has gone off screen
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

# instantiate object 
jumpy = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 150)
# create sprite groups
platform_group = pygame.sprite.Group()
# create starting platform
platform = Platform(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT - 50, 100, False)
platform_group.add(platform)
        
# game loop
running = True 
while running:
    clock.tick(FPS) # set fps
    if game_over == False:
            
        SCROLL = jumpy.move() # move player

        for i in range (0, tiles):  # infinite scrolling for bg as player moves; keeps images clean
            screen.blit(bg_image, (0, i * bg_height + SCROLL))

        # generate platforms
        if len(platform_group) < MAX_PLATFORMS:
            p_w = random.randint(40, 60) # used to randomize the coordinates of platforms
            p_x = random.randint(0, WINDOW_WIDTH - p_w)
            p_y = platform.rect.y - random.randint(80, 120)
            # p_y can't be fully random as if platform is too spread out player cannot jump to next platform
            p_type = random.randint(1, 2)
            if p_type == 1:
                p_moving = True
            else:
                p_moving = False
            platform = Platform(p_x, p_y, p_w, p_moving)
            platform_group.add(platform) 
            
        # update platforms
        platform_group.update(SCROLL) # update the group of platforms being made and display

        # update score
        if SCROLL > 0:
            score += int(SCROLL)

        # score multipliers
        if score >= 3000:
            score += int(round(SCROLL * (1.1)))
        if score >= 5000:
            score += int(round(SCROLL * (1.2)))
        if score >= 7000:
            score += int(round(SCROLL * (1.3)))
        if score >= 10000:
            score += int(round(SCROLL * (1.4)))

        # draw line at high score
        pygame.draw.line(screen, BLACK, (0, score - high_score + SCROLL_THRESH), (WINDOW_WIDTH, score - high_score + SCROLL_THRESH), 3)
        draw_text('HIGH SCORE: ', font_small, BLACK, WINDOW_WIDTH - 130, score - high_score + SCROLL_THRESH) # draw high score 
            
        # draw sprites
        platform_group.draw(screen) # draw platform group on screen
        jumpy.draw() # draw player

        # draw panel
        draw_panel()

        # check game over
        if jumpy.rect.top > WINDOW_HEIGHT:

            if(retried == False):
                retried = True

                print()
                print("If you want to continue from where you fell, you must win a game of Slapjack.")
                cont_choice = input("Would you like another life? Y/N: ")

                if (cont_choice == "Y"):
                    retry = SlapJack()
                    retry.deal_cards()

                    retry_check = retry.game()
                    print(retry_check)

                    if (1 in retry_check):
                        game_over == False

                        jumpy.rect = pygame.Rect(platform.rect.x, 0, 30, 40)
                        jumpy.move()
                        print("")
                        print("Click the game window to keep playing.")

                    else:
                        draw_text('GAME OVER!', font_big, BLACK, 130, 200)
                        draw_text('SCORE: ' + str(score), font_big, BLACK, 130, 250)

                        # update high score 
                        if score > high_score:
                            high_score = score # high score is score if score is higher than high score
                            with open('score.txt', 'w') as file: # call in file
                                file.write(str(high_score)) # writes the high score onto text file automatically
       
                        game_over = True

                elif (cont_choice == "N"):
                    draw_text('GAME OVER!', font_big, BLACK, 130, 200)
                    draw_text('SCORE: ' + str(score), font_big, BLACK, 130, 250)

                    # update high score 
                    if score > high_score:
                        high_score = score # high score is score if score is higher than high score
                        with open('score.txt', 'w') as file: # call in file
                            file.write(str(high_score)) # writes the high score onto text file automatically
                    
            else:
                game_over = True
                pygame.quit()

    else:
        draw_text('GAME OVER!', font_big, BLACK, 130, 200)
        draw_text('SCORE: ' + str(score), font_big, BLACK, 130, 250)

        # update high score 
        if score > high_score:
            high_score = score # high score is score if score is higher than high score
            with open('score.txt', 'w') as file: # call in file
                file.write(str(high_score)) # writes the high score onto text file automatically

    if game_over == False:  
        # event handler 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # update high score 
                if score > high_score:
                    high_score = score
                    with open('score.txt', 'w') as file:
                        file.write(str(high_score))
                running = False
                
        pygame.display.update()

pygame.quit()
