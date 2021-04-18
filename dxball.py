# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 01:33:01 2021

@author: User
"""

import pygame;
from pygame.locals import *;

pygame.init();

#screen
screen_width =600;
screen_height = 600;
screen = pygame.display.set_mode((screen_width,screen_height));

pygame.display.set_caption('Dxball');


#variables
run = True;
bg = (234,218,184)
block_red = (242,85,96);
block_blue = (69,177,233);
block_green=(86,174,87);
paddle_col = (142,135,123);
paddle_outline= (100,100,100);
cols = 6;
rows = 6;
#frame rate
fpsClock = pygame.time.Clock();
fps = 60;
game_over = 0;
reset_ball =False;
txt_col =(78,81,139);
font = pygame.font.SysFont('Constantia', 30);

class wall: 
    def __init__(self):
        self.width = screen_width // cols;
        self.height = 45;
        self.blocks=[];
        
    def create_wall(self):  
        block_individual = [];
        for row in range(rows):
            block_row = [];
            for col in range(cols):
                block_x = col * self.width;
                block_y = row * self.height;
                block_rect= pygame.Rect(block_x,block_y,self.width,self.height);
                
                if row < 2:
                    strength = 3;
                elif row < 4:
                    strength = 2;
                elif row < 6:
                    strength = 1;
                block_individual = [block_rect , strength];
                
                block_row.append(block_individual);
            self.blocks.append(block_row);
    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                if block[1] == 3:
                    block_color = block_blue;
                elif block[1] == 2:
                    block_color = block_green;
                elif block[1] == 1:
                    block_color = block_red;
                pygame.draw.rect(screen,block_color,block[0]);
                pygame.draw.rect(screen,bg,block[0],3);
      
class paddle:
    def __init__(self,x,y):
       self.reset(x,y);
    def draw_paddle(self):
        pygame.draw.rect(screen,paddle_col,self.rect);
        pygame.draw.rect(screen,paddle_outline,self.rect,2);
    def move_paddle(self):
        key = pygame.key.get_pressed();
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-1 * self.speed, 0);
            self.direction = -1;
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.move_ip(self.speed, 0);
            self.direction = 1;
    def reset(self,x,y):
        self.x = x;
        self.y = y;
        self.rect = pygame.Rect(self.x,self.y,140,20);
        self.speed = 7;
        self.direction = 0;
        
class ball: 
    def __init__(self,x,y):
        self.reset(x,y);
    def draw_ball(self):
        pygame.draw.circle(screen,paddle_col,(self.rect.x + self.ball_rad , self.rect.y + self.ball_rad),self.ball_rad);
        pygame.draw.circle(screen,paddle_outline,(self.rect.x + self.ball_rad , self.rect.y + self.ball_rad),self.ball_rad,2);
    
    def move_ball(self):
        #collsion threshold
        col_thresh = 5;
        
        #collsion with wall
        #start with assumption the the wall has been destroyed
        wall_destroyed = 1;
        for row in w.blocks:
            for item in row:
                if self.rect.colliderect(item[0]):
                    #collision from top of brick
                    if abs(self.rect.bottom - item[0].top ) <= col_thresh and self.yspeed > 0:
                        self.yspeed *= -1;
                    #collision from bottom side of brick
                    if abs(self.rect.top - item[0].bottom ) <= col_thresh and self.yspeed < 0:
                        self.yspeed *= -1;
                    #collision from left side of brick
                    if abs(self.rect.right - item[0].left ) <= col_thresh and self.xspeed > 0:
                        self.xspeed *= -1;
                    #collision from right side of brick
                    if abs(self.rect.left - item[0].right ) <= col_thresh and self.xspeed < 0:
                        self.xspeed *= -1;
                    
                    #check strength of blocks and reduce it
                    if item[1] > 1:
                        item[1] -= 1;
                    else:
                        item[0] = (0,0,0,0);
                #check if block still exists
                if item[0] != (0,0,0,0):
                    wall_destroyed = 0;
        #wall is destroyed
        if wall_destroyed == 1:
            self.game_over = 1;
            
        self.rect.x += self.xspeed;
        self.rect.y += self.yspeed;
        
        #left and right collision check
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.xspeed *= -1;
        #top collision 
        if self.rect.top < 0:
            self.yspeed *= -1;
        #bottom collision
        if self.rect.bottom > screen_height:
            self.game_over = -1;
            print(self.game_over);
        
        #collsion with paddle
        if self.rect.colliderect(p):
           #collision with top of paddle 
           if abs(self.rect.bottom - p.rect.top) <=  col_thresh:
               self.yspeed  *= -1;
               self.xspeed += p.direction;
               if self.xspeed >= self.speed_max:
                   self.xspeed = self.speed_max;
               elif self.xspeed < 0 and self.xspeed <= -self.speed_max:
                   self.xspeed = -self.speed_max;
           else:
              self.xspeed *= -1;
        return self.game_over;
    
    def reset(self,x,y):
        self.x = x;
        self.y = y;
        self.ball_rad =10;
        self.rect = pygame.Rect(self.x,self.y,self.ball_rad * 2,self.ball_rad * 2);
        self.xspeed = 5;
        self.yspeed = -5;
        self.speed_max = 6;
        self.game_over = 0;
            
def screen_bg():
    screen.fill(bg);

def show_text(text,text_col,x,y):
    txt_img = font.render(text, True , text_col);
    screen.blit(txt_img , (x , y));    
    
w = wall();
w.create_wall();

p = paddle(screen_width // 2  - 70, screen_height - 30);
b = ball(screen_width // 2  - 10 , p.y - 20);
while run:
    fpsClock.tick(fps);
    screen_bg();
    w.draw_wall();
    p.draw_paddle();
    b.draw_ball();
    if reset_ball:
        p.move_paddle();
        game_over =  b.move_ball();
        
        if game_over != 0:
            reset_ball = False;
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False;
        if event.type == pygame.MOUSEBUTTONDOWN and reset_ball == False:
            reset_ball = True;
            b.reset(screen_width // 2  - 10 , p.y - 20);
            p.reset(screen_width // 2  - 70, screen_height - 30);
            w.create_wall();
            
    if reset_ball == False:
        if game_over == 0:
           show_text('CLICK ANYWHERE TO START', txt_col , 100 , screen_height // 2 + 60);
        elif game_over == 1:
            show_text('YOU WON!', txt_col ,220, screen_height // 2 + 20);
            show_text('CLICK ANYWHERE TO START', txt_col , 100 , screen_height // 2 + 60);
        elif game_over == -1:
           show_text('YOU LOST!', txt_col ,220 ,screen_height // 2 + 20);
           show_text('CLICK ANYWHERE TO START', txt_col , 100 , screen_height // 2 + 60);
    pygame.display.update();
pygame.quit();            
