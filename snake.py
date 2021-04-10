# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 12:52:40 2021

@author: User
"""

import pygame;
from pygame.locals import *;
import random;

pygame.init();


#screen
screen_width = 800;
screen_height = 800;
screen = pygame.display.set_mode((screen_width,screen_height));

pygame.display.set_caption('Snake Game');

#variable and colors
run = True;
bg = (128,128,128);
cellsize = 10;
snake_pos = [[screen_width//2,screen_height//2]];
snake_pos.append([screen_width//2,screen_height//2 + cellsize]);
snake_pos.append([screen_width//2,screen_height//2 + cellsize * 2]);
snake_pos.append([screen_width//2,screen_height//2 + cellsize * 3]);
print(snake_pos);
body_outer = (51,153,255);
body_inner = (204,229,255);
head_col = (0,102,102);
direction = 1; # 1 - up 2 - down 3 - left 4 - right
update_snake = 0;
count = 4;
food =[0,0];
new_food = True;
new_piece=[0,0];
food_col = (255,255,102);
game_over = False;
clicked = False;
score = 0;
blue = (0,0,255);
green=(0,228,0);
font = pygame.font.SysFont(None,30);

#play again code
again_text = 'Play Again?';
again_img = font.render(again_text,True,blue);
again_rect = Rect(screen_width//2 - again_img.get_width()//2+22,screen_height//2 - again_img.get_height()//2+47,146,35);


def show_gameover():
    msg = f'Score is {score}';
    win_img = font.render(msg,True,blue);
    pygame.draw.rect(screen,green,(screen_width//2 - win_img.get_width()//2-10,screen_height//2 - win_img.get_height()//2-15,200,50));
    screen.blit(win_img,(screen_width//2 - win_img.get_width()//2+30,screen_height//2 - win_img.get_height()//2));   


    
    pygame.draw.rect(screen,green,again_rect);
    screen.blit(again_img,(screen_width//2 - win_img.get_width()//2+30,screen_height//2 - win_img.get_height()//2+56));         
def check_gameover(game_over):
    head_count = 0;
    for seg in snake_pos :
        if snake_pos[0] == seg and head_count > 0:
            game_over = True;
        head_count = 1;
    if snake_pos[0][0] < 0 or snake_pos[0][0] > screen_width or snake_pos[0][1] < 0 or snake_pos[0][1] > screen_height:
        game_over  = True;
    return game_over;    
def create_screen():
    screen.fill(bg);
#show score
def show_score(score):
   msg =f'Score: {score}';
   score_img = font.render(msg,True,blue);
   screen.blit(score_img,(10,10));         
while run:
    create_screen();
    show_score(score);
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False;
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 2:
                direction = 1;
            if event.key == pygame.K_DOWN and direction != 1:
                direction = 2;
            if event.key == pygame.K_LEFT and direction != 4:
                direction = 3;
            if event.key == pygame.K_RIGHT and direction != 3:
                direction = 4;    
    #snake movement
    if game_over == False:
        if update_snake > 99:
            update_snake = 0;
            count = 0;
            snake_pos = snake_pos[-1:] + snake_pos[:-1];
            if direction == 1:
                snake_pos[0][0] = snake_pos[1][0];
                snake_pos[0][1] = snake_pos[1][1] - cellsize;
            if direction == 2:
                snake_pos[0][0] = snake_pos[1][0];
                snake_pos[0][1] = snake_pos[1][1] + cellsize;
            if direction == 3:
                snake_pos[0][0] = snake_pos[1][0] - cellsize;
                snake_pos[0][1] = snake_pos[1][1];         
            if direction == 4:
                snake_pos[0][0] = snake_pos[1][0] + cellsize;
                snake_pos[0][1] = snake_pos[1][1];   
            game_over  = check_gameover(game_over);    
    
    if game_over == True:
        show_gameover();
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                clicked = True;
        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False;
                pos = pygame.mouse.get_pos();
                if again_rect.collidepoint(pos):
                    direction = 1 # 1 - up 2 -down 3 - left 4 - right
                    update_snake = 0;
                    new_food = True;
                    food =[0,0];
                    new_piece = [0,0];
                    score = 0;
                    game_over = False;

                    snake_pos = [[screen_width//2 , screen_height // 2]];
                    snake_pos.append([screen_width // 2 , screen_height // 2 + cellsize]);
                    snake_pos.append([screen_width // 2 , screen_height // 2 + cellsize * 2]);
                    snake_pos.append([screen_width // 2 , screen_height // 2 + cellsize * 3]);
    #new food
    if new_food:
        new_food = False;
        food[0] = cellsize * (random.randint(2,screen_width //cellsize) - 1);
        food[1] = cellsize *  (random.randint(2,screen_height // cellsize ) - 1);
    pygame.draw.rect(screen,food_col,(food[0],food[1],cellsize - 2,cellsize));
    #check if food is eaten
    if snake_pos[0] == food:
        new_food = True;
        print(new_food);
        new_piece = list(snake_pos[-1]);
        print(type(new_piece));
        if direction == 1:
            new_piece[1] += cellsize;
        if direction == 2:
            new_piece[1] -= cellsize;
        if direction == 3:
            new_piece[0] += cellsize;
        if direction == 4:
            new_piece[0] -= cellsize;  
        snake_pos.append(new_piece);    
        print(snake_pos);    
        score += 1;

            
    head = 1;        
    for segments in snake_pos:
        if head == 0:
            pygame.draw.rect(screen,body_outer,(segments[0],segments[1],cellsize,cellsize));
            pygame.draw.rect(screen,body_inner,(segments[0] + 1,segments[1] + 1,cellsize - 2,cellsize - 2));
        elif head == 1:
            pygame.draw.rect(screen,body_outer,(segments[0],segments[1],cellsize,cellsize));
            pygame.draw.rect(screen,head_col,(segments[0] + 1,segments[1] + 1,cellsize - 2,cellsize - 2));  
            head = 0;  
    update_snake += 1 + count;                          
    pygame.display.update();        
pygame.quit();            