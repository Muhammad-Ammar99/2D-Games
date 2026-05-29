from turtle import Screen
import pygame
import random

from colors import WHITE, PURPLE

pygame.init()


screen_width= 600
screen_height= 600

pygame.display.set_caption("Galaxy Stars")

bg_img = pygame.image.load("bg.jpg").convert()
User_img = pygame.image.load("user.png").convert_alpha()
Coin_img = pygame.image.load("coin.png").convert_alpha()
Bomb_img = pygame.image.load("tnt.png").convert_alpha()

# Game Variables

font =pygame.font.SysFont(None, 30)

def welcome():
    run = True
    while run:
        Screen.fill((255,255, 0))
        font = pygame.font.SysFont(None, 30)
        score_text=font.render("Welcome to Galaxy Stars", True, PURPLE)
        Screen.blit(score_text,(180,230))
        score_text=font.render("Press Spacebar to Continue", True, PURPLE)
        Screen.blit(score_text, (180, 260))

        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                run=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    pygame.mixer.music.load("interstellar.mp3")
                    pygame.mixer.music.play(-1)
                    gameloop()
        pygame.display.update()


def gameloop():
   
    speed_ac =0.3
    speed=0.2
    ac_x_cord= 240
    ac_y_cord=525
    bombx =random.randint(20, 570)
    bomby=-10
    coinx=random.randint(20, 570)
    coiny=-10
    coinx2=-50
    coiny2=-100
    bombx2=-50
    bomby2=-100
    bombx3,bomby3=-70,-100
    bombx4,bomby4=-100,-100
    score = 0
    font = pygame.font.SysFont(None, 30)
    exitgame = False
    gameover = False

    with open("Highscore2.txt", "r") as f:
        highscore=f.read().strip()

    if not highscore.isdigit():
        highscore="0"
    highscore=int(highscore)  

    shift_pressed = False
    
    while not exitgame:
        if gameover:
            with open("Highscore2.txt", "w") as f:
                f.write(str(highscore)) 

            Screen.fill(WHITE)
            font=pygame.font.SysFont(None,30)
            screen_text=font.render("Game Over! Press Enter to Continue",True,PURPLE)
            Screen.blit(screen_text, [180, 230])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitgame = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.load("interstellar.mp3")
                        pygame.mixer.music.play(-1)
                        gameloop()
            pygame.display.update()

        else:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exitgame=True

            
            bomby+=speed
            bomby2+=speed
            bomby3+=speed
            bomby4+=speed
            coiny+=speed
            coiny2+=speed

            
            if bomby>screen_height:
                bombx=random.randint(20, 570)
                bomby=-10

            if bomby2>screen_height:
                bombx2=random.randint(20, 570)
                bomby2=-10
            
            if bomby3>screen_height:
                bombx3=random.randint(20, 570)
                bomby3=-10
                
            if bomby4>screen_height:
                bombx4=random.randint(20, 570)
                bomby4=-10

            if coiny>screen_height:
                coinx=random.randint(20, 570)
                coiny=-10

            if coiny2>screen_height:
                coinx2=random.randint(20, 570)
                coiny2=-10

            # Controlling AirCraft
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                ac_x_cord -= speed_ac
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                ac_x_cord += speed_ac
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                ac_y_cord -= speed_ac
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                ac_y_cord += speed_ac

            # Cheat Code
            if keys[pygame.K_RSHIFT or pygame.K_LSHIFT] and not shift_pressed:
                score += 10
                shift_pressed = True  

            if not keys[pygame.K_RSHIFT or pygame.K_LSHIFT]:
                shift_pressed = False

            # Collision Detection
            if ((ac_x_cord -bombx) **2+(ac_y_cord-bomby)**2)**0.5<40:
                gameover = True
                pygame.mixer.music.load("Glass and Metal Collision.mp3")
                pygame.mixer.music.play()

            if ((ac_x_cord-bombx2)**2+(ac_y_cord-bomby2)**2)** 0.5<40:
                gameover = True
                pygame.mixer.music.load("Glass and Metal Collision.mp3")
                pygame.mixer.music.play()

            if ((ac_x_cord-bombx3)**2+(ac_y_cord-bomby3)**2)**0.5<40:
                gameover = True
                pygame.mixer.music.load("Glass and Metal Collision.mp3")
                pygame.mixer.music.play()
                
            if ((ac_x_cord - bombx4) ** 2 + (ac_y_cord - bomby4) ** 2) ** 0.5 < 40:
                gameover = True
                pygame.mixer.music.load("Glass and Metal Collision.mp3")
                pygame.mixer.music.play()

            if ((ac_x_cord - coinx) ** 2 + (ac_y_cord - coiny) ** 2) ** 0.5 < 50:
                score += 1
                coinx = random.randint(20, 570)
                coiny = -10

            if ((ac_x_cord - coinx2) ** 2 + (ac_y_cord - coiny2) ** 2) ** 0.5 < 40:
                score += 1
                coinx2 = random.randint(20, 570)
                coiny2 = -10

            #setting the img positions
            scaled_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
            Screen.blit(scaled_img, (0, 0))

            scaled_User_img = pygame.transform.scale(User_img, (screen_width // 8, screen_height // 8))
            Screen.blit(scaled_User_img, (ac_x_cord, ac_y_cord))

            scaled_tnt_img = pygame.transform.scale(Bomb_img, (screen_width // 15, screen_height // 15))
            Screen.blit(scaled_tnt_img, (bombx, bomby))

            scaled_coin_img = pygame.transform.scale(Coin_img, (screen_width // 20, screen_height // 20))
            Screen.blit(scaled_coin_img, (coinx, coiny))

            # Coin2 img Random pos 
            if score >= 5:
                scaled_coin_img2 = pygame.transform.scale(Coin_img, (screen_width // 20, screen_height // 20))
                Screen.blit(scaled_coin_img2, (coinx2, coiny2))

            # Tnt2 img Random pos 2-4
            if score >= 10:
                scaled_tnt_img2 = pygame.transform.scale(Bomb_img, (screen_width // 15, screen_height // 15))
                Screen.blit(scaled_tnt_img2, (bombx2, bomby2))
                
            if score >= 25:
                scaled_tnt_img3 = pygame.transform.scale(Bomb_img, (screen_width // 15, screen_height // 15))
                Screen.blit(scaled_tnt_img3, (bombx3, bomby3))

            if score >= 50:
                scaled_tnt_img4 = pygame.transform.scale(Bomb_img, (screen_width // 15, screen_height // 15))
                Screen.blit(scaled_tnt_img4, (bombx4, bomby4))
            
            # Checking if player goes out of screen boundaries
            if ac_x_cord < 0:
                ac_x_cord = 0
            elif ac_x_cord > screen_width - scaled_User_img.get_width():
                ac_x_cord = screen_width - scaled_User_img.get_width()
            if ac_y_cord < 0:
                ac_y_cord = 0
            elif ac_y_cord > screen_height - scaled_User_img.get_height():
                ac_y_cord = screen_height - scaled_User_img.get_height()

            # Checking: if current score is greater than highscore
            if score>highscore:
                highscore=score

            font = pygame.font.SysFont(None,30)
            scoreSS_text = font.render("Score: "+str(score), True, WHITE)
            Screen.blit(score_text, (10, 10))

            highscore_text = font.render("Highscore: "+str(highscore), True, WHITE)
            Screen.blit(highscore_text, (450, 10))

            pygame.display.update()
            
    pygame.quit()
    quit()

welcome()
