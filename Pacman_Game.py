#Shubham Mittal 2018101
import pygame
from pygame.locals import *
from numpy import loadtxt
import time
import sys
from random import *
#Constants for the game
x=35
WIDTH, HEIGHT = (x, x)
WALL_COLOR = pygame.Color(69, 139, 116,0)
DOWN = (0,1)
RIGHT = (1,0)
TOP = (0,-1)
LEFT = (-1,0)
STAY=(0,0)
pacman_image=[["0"],["pacman1.png","pacman11.png"],["pacman2.png","pacman22.png"],["pacman3.png","pacman33.png"],["pacman4.png","pacman44.png"]]#file names for pacman images facing different directions
number_of_coins=0 # to store total nomber of coins in the given layout
pacman_position = (1,1) # initial position for pacman
enemy1=(4,5)#initial coordinates for enemy 1
enemy2=(6,7)#initial coordinates for enemy 2
enemy3=(2,1)#initial coordinates for enemy 3
enemy4=(7,8)#initial coordinates for enemy 4
lives=3# to store number of lives left
score=0#to store current scores of the player
direction=1#to store direction of face of pacman
moves=[(0,1),(1,0),(-1,0),(0,-1)]#moves for enemies
speed=4#for enemies
change=0#positon for enemies
def draw_wall(screen, pos):
	pixels = pixels_from_points(pos)
	pygame.draw.rect(screen, WALL_COLOR, [pixels, (WIDTH, HEIGHT)])
def draw_enemy(screen, pos): 
	pixels = pixels_from_points(pos)
	img=pygame.image.load("enemy.jpg").convert()
	screen.blit(img,pixels)
def draw_pacman(screen, pos,dir): 
	pixels = pixels_from_points(pos)
	img=pygame.image.load(dir).convert()
	screen.blit(img,pixels)
def draw_coin(screen, pos):
	pixels = pixels_from_points(pos)
	img=pygame.image.load("coin.png").convert()
	screen.blit(img,pixels)	
def valid_move(pos,pos2):#to check move by pacman or enemies are valid i.e no wall
        if(layout[pos[1]+pos2[1],pos[0]+pos2[0]]!='w'):
                return True
        else:
                return False      
def add_to_pos(pos, pos2):
	return (pos[0]+pos2[0], pos[1]+pos2[1])
def pixels_from_points(pos):
	return (pos[0]*WIDTH, pos[1]*HEIGHT)

layout = loadtxt('layout1.txt', dtype=str)
rows, cols = layout.shape
k=0
#to count the number of coins in the given layout of pacman game and give initial position to enemy 2 and 3
for i in layout:
        k+=1
        for j in range(len(i)):
                if(number_of_coins==25):
                        enemy2=(j,k)
                if(number_of_coins==10):
                        enemy3=(j,k)
                if(number_of_coins==30):
                        enemy4=(j,k)
                if(i[j]=='c'):
                        number_of_coins+=1
pygame.init()
screen = pygame.display.set_mode((x*cols,x*rows), 0, 32)
background = pygame.surface.Surface((x*cols,x*rows)).convert()

font_large=pygame.font.SysFont('inkfree',50,True)
welcome=font_large.render("WELCOME TO PACMAN",1,(139,10,80),True) # to print welcome message
screen.blit(welcome,((x-25)*cols//2,x*rows//2))
pygame.display.update()
pygame.time.delay(1000)
clock=pygame.time.Clock()
font=pygame.font.SysFont('inkfree',30,True)
text=font.render("SCORE: %d"%score,1,(139,10,80),True)#display initial score=0
flag=0
while True:  
        keys=pygame.key.get_pressed()#to store the keyboard input
        seconds=150-pygame.time.get_ticks()//1000#to store time elapsed in seconds
        for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[K_q]:
                        pygame.quit()
                        sys.exit()

        screen.blit(background,(0,0))
        
        x=moves[randint(0,3)]
        if(change%speed==0 and valid_move(enemy1,x)):
                enemy1=add_to_pos(enemy1,x)
        x=moves[randint(0,3)]
        if(change%speed==0 and valid_move(enemy2,x )):
                enemy2=add_to_pos(enemy2,x)
        x=moves[randint(0,3)]
        if(change%speed==0 and valid_move(enemy3,x )):
                enemy3=add_to_pos(enemy3,x)
        if(change%speed==0 and valid_move(enemy4,x )):
                enemy4=add_to_pos(enemy4,x)
        change+=1
        
        move_direction = STAY#default movement for pacman

        #draw the layout for game
        for col in range(cols):
                for row in range(rows):
                        value = layout[row][col]
                        pos = (col, row)
                        if value == 'w':
                                draw_wall(screen, pos)
                        elif value == 'c':
                                draw_coin(screen, pos)
        
        draw_enemy(screen,enemy1)
        draw_enemy(screen,enemy2)
        draw_enemy(screen,enemy3)
        draw_enemy(screen,enemy4)
        draw_pacman(screen,pacman_position,pacman_image[direction][randint(0,1)])

        #check for collission or time up
        if(pacman_position==enemy1 or pacman_position==enemy2 or pacman_position==enemy3 or pacman_position==enemy4 or seconds<=0):
                #giving another life
                pygame.mixer.music.load('die.wav')
                pygame.mixer.music.play(0)
                if(lives!=0 and seconds>0):
                        lives-=1
                        another_life=font_large.render("REVIVING",1,(255,25,0,222),True)
                        screen.blit(another_life,(cols*(cols)/2,rows*(rows+rows/2)/2))
                        direction=1
                        if(score!=0):#decreasing score by 1 for reviving
                                score-=1
                                number_of_coins-=1
                                
                        pygame.display.update()
                        pygame.time.delay(2000)
                        pacman_position=(1,1)
                        continue
                #lost due to time up

                screen.blit(background,(0,0))
                if(seconds<=0):
                        time_up=font_large.render("TIME UP!",1,(139,10,80),True)
                        screen.blit(time_up,(cols*cols/2,0*rows))
                game_over=font_large.render("GAME OVER",1,(139,10,80),True)
                final_scores=font_large.render("SCORE= %d"%score,5,(139,10,80))
                screen.blit(game_over,(cols*cols/2,10*cols))
                screen.blit(final_scores,(cols*cols/2,14*cols))
                break
        
        #all coins eaten up
        if(score==number_of_coins):
                
                screen.blit(background,(0,0))
                font=pygame.font.SysFont('inkfree',50,True)
                pygame.mixer.music.load('won.mp3')
                pygame.mixer.music.play(0)
                text=font_large.render("YOU WON",1,(139,10,80),True)
                final_scores=font_large.render("SCORE= %d"%score,1,(139,10,80))
                screen.blit(text,(cols*cols/2,10*cols))
                screen.blit(final_scores,(cols*cols/2,14*cols))
                break

        #taking keyboard input
        if(keys[pygame.K_LEFT] or keys[pygame.K_a]):
             move_direction=LEFT
             direction=3
        elif(keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            move_direction=RIGHT
            direction=1
        elif(keys[pygame.K_UP] or keys[pygame.K_w]):
            move_direction=TOP
            direction=4
        elif(keys[pygame.K_DOWN] or keys[pygame.K_s]):
            direction=2
            move_direction=DOWN

        #check for valid move by pacman according to keyboard input
        if(valid_move(pacman_position, move_direction)):
                pacman_position = add_to_pos(pacman_position, move_direction)
                
                if(layout[pacman_position[1]][pacman_position[0]]=='c'):#coin is eaten so increasing score and removing coin
                        score+=1
                        pygame.mixer.music.load('eat.mp3')
                        pygame.mixer.music.set_volume(0.2)
                        pygame.mixer.music.play(0)
                        layout[pacman_position[1]][pacman_position[0]]='.'

        time=font.render("Time: %d"%seconds,1,(255,25,0,222),True)
        text=font.render("SCORE: %d"%score,1,(255,25,0,222),True)
        live=font.render("Lives: %d"%lives,1,(255,25,0,222),True)
        screen.blit(time,(0,0))
        screen.blit(text,((cols+7)*rows//2,0))
        screen.blit(live,((cols+7)*rows,0))
        pygame.display.update()
        pygame.time.delay(70)


designer=font_large.render("MADE BY SHUBHAM",1,(139,10,80))
screen.blit(designer,(cols*cols/4,(cols-2)*rows))
pygame.display.update()
pygame.time.delay(3500)
pygame.quit()
sys.exit()
