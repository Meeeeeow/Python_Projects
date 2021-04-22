# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 01:18:28 2021

@author: User
"""
import pygame;
from pygame.locals import *;

pygame.init();

screen_width = 700;
screen_height = 700;
screen = pygame.display.set_mode((screen_width,screen_height));
pygame.display.set_caption('Explosion');


#variables
run = True;
fpsClock = pygame.time.Clock();
fps = 60;
bg =(50,50,50);

def show_bg():
    screen.fill(bg);

#create explosion class
class explosion(pygame.sprite.Sprite):
    def __init__(self ,  x ,y):
        pygame.sprite.Sprite.__init__(self);
        self.images=[];
        for num in range(1,6):
            img =pygame.image.load(f'img/exp{num}.png');
            img = pygame.transform.scale(img, (100,100));
            self.images.append(img);
        self.index =0;
        #needs to be there when working with sprites
        self.image = self.images[self.index];
        self.rect = self.image.get_rect();
        self.rect.center =[x,y];
        self.counter =0;
    def update(self):
        explosion_speed = 6;
        self.counter += 1;
        
        #change img
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0;
            self.index += 1;
            self.image = self.images[self.index]; #update ihe img
        
        #if animation is completed
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill() #to kill an instance

explosion_grp = pygame.sprite.Group();  #need to check 
            
while run:
    fpsClock.tick(fps);
    show_bg();
    
    #for explosion
    explosion_grp.draw(screen); #as  sprites are being used
    explosion_grp.update();
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False;
        #for creating explosion
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos();
            exp = explosion(pos[0], pos[1]);
            explosion_grp.add(exp);
            
    pygame.display.update();
pygame.quit();
