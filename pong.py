# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 13:47:46 2021

@author: User
"""

import pygame;
from pygame.locals import  *;

pygame.init();

#screen 
screen_width = 600;
screen_height = 500;

screen = pygame.display.set_mode((screen_width,screen_height));

pygame.display.set_caption('pong');


#frame rate
fpsClock = pygame.time.Clock();
fps = 60;
#variables
run  = True;
bg = (50,25,50);
bg1 = (60,91,89);
bg2 = (155,175,142);
margin = 60;
white = (255,255,255);
font = pygame.font.SysFont('Constantia', 30);
cpu_score = 0;
player_score = 0;
winner = 0;
reset_ball = False;
speed_increase = 0;
#create paddle

class paddle():
    def __init__(self,x,y):
        self.x = x;
        self.y = y;
        self.rect = Rect(self.x,self.y,20,100);
        self.speed = 5;

    def draw(self):
        pygame.draw.rect(screen,white,self.rect);
    def move_paddle(self):
        key = pygame.key.get_pressed();
        if key[pygame.K_UP] and self.rect.top > margin:
            self.rect.move_ip(0, -1 * self.speed);
        if key[pygame.K_DOWN] and self.rect.bottom < screen_height:
            self.rect.move_ip(0, self.speed);
    def ai_move(self):
        #if ball is down below center of paddle
        if self.rect.centery < pong_ball.rect.top and self.rect.bottom < screen_height:
            self.rect.move_ip(0, self.speed);
        #if ball is up above center of paddle
        if self.rect.centery  > pong_ball.rect.bottom and self.rect.top > margin:
            self.rect.move_ip(0, -1 * self.speed);

class ball():
    def __init__(self,x,y):
        self.reset(x,y);
    
    def draw(self):
        pygame.draw.circle(screen,white,(self.rect.x + self.ball_rad , self.rect.y + self.ball_rad),self.ball_rad); 

    def move(self):
        
        #update ball position
        self.rect.x += self.xspeed;  
        self.rect.y += self.yspeed;
        
        #top and bottom bound
        if self.rect.top < margin:
            self.yspeed *= -1;
           # print(f'i am {self.yspeed}');
        if self.rect.bottom > screen_height:
            self.yspeed *= -1;
            #print(f'you are {self.yspeed}');
        #check collision with paddles
        if self.rect.colliderect(player_paddle) or self.rect.colliderect(cpu_paddle):
            self.xspeed *= -1;    
        #left and right bound
        if self.rect.left < 0:
            self.winner = 1;
        if self.rect.right > screen_width:
            self.winner = -1;
        
       
        
        
        return self.winner;    
   
    def reset(self,x,y):
        self.x = x;
        self.y = y;
        self.ball_rad = 10;
        self.rect = Rect(self.x,self.y,self.ball_rad * 2,self.ball_rad * 2);
        self.xspeed = -5;
        self.yspeed = 5;
        self.winner = 0; #1 -> player -1 -> cpu
                 
            
        
player_paddle = paddle(screen_width - 40 ,screen_height // 2);
cpu_paddle = paddle(20,screen_height // 2);
pong_ball = ball(screen_width - 60,screen_height // 2 + 60);        
def draw_screen():
    screen.fill(bg);
    pygame.draw.line(screen,white,(0,margin),(screen_width , margin));
    if cpu_score > 3 or player_score > 3:
        screen.fill(bg1);
    if cpu_score > 13 or player_score > 13:
        screen.fill(bg1);    
def show_text(text,text_col,x,y):
    txt_img = font.render(text, True , text_col);
    screen.blit(txt_img , (x , y));     
while run:
    fpsClock.tick(fps);
    draw_screen();
    show_text(f'CPU: {cpu_score}', white , 20 , 15);
    show_text(f'P1: {player_score}', white , screen_width - 100 , 15);
    show_text(f'BALL SPEED: {abs(pong_ball.xspeed)}', white , screen_width // 2 - 100 , 15);
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                run = False;
        if event.type == pygame.MOUSEBUTTONDOWN and reset_ball == False:
            reset_ball = True;
            pong_ball.reset(screen_width - 60,screen_height // 2 + 60);
            
    #draw paddle
    player_paddle.draw();
    cpu_paddle.draw();  
    
   
    if reset_ball:
        speed_increase += 1;
        winner = pong_ball.move();
        print(winner);
        
        if winner == 0:
             player_paddle.move_paddle();
             cpu_paddle.ai_move();
             #draw ball
             pong_ball.draw();
        else:
            reset_ball = False;
            if winner == 1:
                player_score += 1;
            elif winner == -1:
                cpu_score += 1;
    
    if reset_ball == False:
        if winner == 0:
            show_text('CLICK ANYWHERE TO START', white , 100 , screen_height // 2 - 90);
        if winner == 1:
            show_text('YOU SCORED!', white , 220 , screen_height // 2 - 90);
            show_text('CLICK ANYWHERE TO START', white , 100 , screen_height // 2 - 40);
        if winner == -1:
            show_text('CPU SCORED!', white , 220 , screen_height // 2 - 90);
            show_text('CLICK ANYWHERE TO START', white , 100 , screen_height // 2 - 40);    
            
    if speed_increase > 500:
        speed_increase = 0;
        if pong_ball.xspeed < 0:
            pong_ball.xspeed -= 1;
        if pong_ball.xspeed > 0:
            pong_ball.xspeed += 1;
        if pong_ball.yspeed < 0:
            pong_ball.yspeed -= 1;
        if pong_ball.yspeed > 0:
            pong_ball.yspeed += 1;    
            
    pygame.display.update();            
pygame.quit();                