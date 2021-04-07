# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 21:11:46 2021

@author: User
"""
import pygame;
from pygame.locals import *;

pygame.init();

#screen
screen_width = 300;
screen_height = 300;
screen = pygame.display.set_mode((screen_width,screen_height));

#variables
run = True;
markers=[];
clicked = False;
pos = [];
player = 1;
cross_color = (0,204,204);
circle_color = (153,51,255);
winner = 0;
game_over = False;
game_draw = False;
blue=(0,0,255);
green=(0,255,0);
font = pygame.font.SysFont(None,30);
again_text = 'Play Again?';
again_img = font.render(again_text,True,blue);
again_rect = Rect(screen_width//2 - again_img.get_width()//2-8,screen_height//2 - again_img.get_height()//2+47,136,35);
again_text = 'Play Again?';
again_img = font.render(again_text,True,blue);
again_rect = Rect(screen_width//2 - again_img.get_width()//2-8,screen_height//2 - again_img.get_height()//2+47,136,35);
#title
pygame.display.set_caption('Tic-Tac-Toe');


def create_tile():
    for row in range(3):
        row = [0] * 3;
        markers.append(row);
    print(markers);  
    
def create_grid():
    bg =(0,153,76);
    grid_color =(178,255,101);
    screen.fill(bg);
    for x in range(1,3):
        pygame.draw.line(screen, grid_color, (0 , x * 100) , (screen_width , x * 100),4); #horizontally
        pygame.draw.line(screen, grid_color, (x * 100 , 0) , (x * 100 , screen_height),4); #vertically

def draw_markers():
    x_pos = 0;
    for row in markers:
        y_pos = 0;
        for y in row:
            if y == 1:
                pygame.draw.line(screen, cross_color , (x_pos * 100 + 25,y_pos * 100 +25) , (x_pos * 100 + 75,y_pos * 100 + 75),4);
                pygame.draw.line(screen, cross_color , (x_pos * 100 + 25,y_pos * 100 +75) , (x_pos * 100 + 75,y_pos * 100 + 25),4);
            if y == -1:
                pygame.draw.circle(screen, circle_color,(x_pos * 100 + 50,y_pos * 100 + 50),40,4);
            y_pos += 1;
        x_pos += 1;      

def check_winner():
       global winner;
       global game_over;
       y_pos = 0;
       for row in markers:
           if sum(row) == 3:
               winner = 1;
               game_over = True;
           if sum(row) == -3:
               winner = 2;
               game_over = True;
           
           if markers[0][y_pos] + markers[1][y_pos] + markers[2][y_pos] == 3:
              winner = 1;
              game_over = True;
           if markers[0][y_pos] + markers[1][y_pos] + markers[2][y_pos] == -3:
              winner = 2;
              game_over = True;    
           y_pos += 1;
       if markers[0][0] + markers[1][1] + markers[2][2] == 3 or markers[2][0] + markers[1][1] + markers[0][2] == 3:
          winner = 1;
          game_over = True;
       if markers[0][0] + markers[1][1] + markers[2][2] == -3 or markers[2][0] + markers[1][1] + markers[0][2] == -3:
          winner = 2;
          game_over = True;  
       
       if check_draw():
            game_over = True;    
          
               
def show_winner():
    global game_draw;
    if game_draw == False:
        msg = f'winner is player {winner}';
        win_img = font.render(msg,True,blue);
        pygame.draw.rect(screen,green,(screen_width//2 - win_img.get_width()//2-10,screen_height//2 - win_img.get_height()//2-15,200,50));
        screen.blit(win_img,(screen_width//2 - win_img.get_width()//2,screen_height//2 - win_img.get_height()//2));   
    
    
        
        pygame.draw.rect(screen,green,again_rect);
        screen.blit(again_img,(screen_width//2 - win_img.get_width()//2+30,screen_height//2 - win_img.get_height()//2+56)); 
    if game_draw == True:
        msg = f'Match is Drawn!';
        draw_img = font.render(msg,True,blue);
        pygame.draw.rect(screen,green,(screen_width//2 - draw_img.get_width()//2-10,screen_height//2 -draw_img.get_height()//2-15,200,50));
        screen.blit(draw_img,(screen_width//2 - draw_img.get_width()//2,screen_height//2 - draw_img.get_height()//2));  

        pygame.draw.rect(screen,green,again_rect);
        screen.blit(again_img,(screen_width//2 - draw_img.get_width()//2+30,screen_height//2 - draw_img.get_height()//2+56));    
    
                              
    
def check_draw():
    global game_draw;
    count = 0;
    for row in markers:
           for y in row:
               if y != 0:
                   count+=1;
    if count == 9:
        game_draw = True;
        return game_draw;
#game loop

create_tile();
while run:
    create_grid();
    draw_markers();
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False;
        if game_over == False and game_draw == False:
            if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                clicked = True;
            if pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False;
                pos = pygame.mouse.get_pos();
                cell_x = pos[0];
                cell_y = pos[1];
                if markers[cell_x // 100][cell_y // 100] == 0:
                    markers[cell_x // 100][cell_y // 100] = player;
                    player *= -1;
                    check_winner();
                    
    if game_over == True:
            show_winner(); 
            #play again mouse click
            if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                    clicked = True;
            if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                    clicked = False;
                    pos = pygame.mouse.get_pos();
                    if again_rect.collidepoint(pos):
                        markers=[];
                        pos =[];
                        player = 1;
                        winner = 0;
                        game_over = False;
                        game_draw = False;
                        create_tile();
   
                            
    pygame.display.update();        
pygame.quit();            

 