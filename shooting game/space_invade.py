# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 12:30:39 2021

@author: User
"""

import pygame;
from pygame import mixer;
from pygame.locals import *;
import random;
pygame.init();
pygame.mixer.pre_init(22050,-16,2,4096);
mixer.init();

screen_width = 800;
screen_height = 1000;
screen = pygame.display.set_mode((screen_width,screen_height));
pygame.display.set_caption('Space shooters');

#variables
run = True;
bg = pygame.image.load('img_game/bg1.png');
red = (255,0,0);
green = (0,255,0);
rows = 6;
cols = 6;
alien_last_hit = pygame.time.get_ticks();
alien_last_hit_boss = pygame.time.get_ticks();
alien_cooldown = 1000; # in ms
alien_boss_cooldown = 900; # in ms
font1 = pygame.font.SysFont('Constantia',30);
font2 = pygame.font.SysFont('Constantia',40);
white=(255,255,255);
countdown = 5;
last_count = pygame.time.get_ticks();
game_over = 0;
#sound
explosion_fx = pygame.mixer.Sound('img_game/explosion.wav');
explosion_fx.set_volume(0.10);

explosion2_fx = pygame.mixer.Sound('img_game/explosion2.wav');
explosion2_fx.set_volume(0.10);

laser_fx = pygame.mixer.Sound('img_game/laser.wav');
laser_fx.set_volume(0.10);

intro = pygame.mixer.Sound('img_game/space.mp3');
intro.set_volume(0.30);
intro.play(-1);
def show_bg():
    screen.blit(bg,(0,0));

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x , y , health):
        pygame.sprite.Sprite.__init__(self);
        self.image = pygame.image.load('img_game/spaceship.png');
        self.rect = self.image.get_rect();
        self.rect.center =[x,y];
        self.health_start = health;
        self.health_remaining = health;
        self.last_hit = pygame.time.get_ticks();
    
    def move(self):
        speed = 8;
        cooldown = 600;
        game_over = 0;
        key = pygame.key.get_pressed();
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-1*speed, 0);
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.move_ip(speed, 0);
        if key[pygame.K_UP] and self.rect.top > screen_height // 2:
            self.rect.move_ip(0, -1 * speed // 2);
        if key[pygame.K_DOWN] and self.rect.top < screen_height - 110:
            self.rect.move_ip(0,speed // 2);
        
        time_now = pygame.time.get_ticks();
        if key[pygame.K_SPACE] and time_now - self.last_hit > cooldown:
            bullet = Bullets(self.rect.centerx,self.rect.top);
            bullet_grp.add(bullet);
            self.last_hit = time_now;
            laser_fx.play();
        
        #update mask for pixel perfect collision
        self.mask = pygame.mask.from_surface(self.image);
            
        pygame.draw.rect(screen,red,(self.rect.x,self.rect.bottom + 10,self.rect.width,15));
        if self.health_remaining > 0:
            pygame.draw.rect(screen,green,(self.rect.x,(self.rect.bottom + 10),int(self.rect.width * (self.health_remaining / self.health_start)),15));
        elif self.health_remaining <= 0:
            exp = Explosion(self.rect.x,self.rect.y,3);
            explosion_grp.add(exp);
            self.kill();
            game_over = -1;
        return game_over;
#bullet class
class Bullets(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self);
        self.image = pygame.image.load('img_game/bullet.png');
        self.rect = self.image.get_rect();
        self.rect.center =[x,y];
    def update(self):
        self.rect.y -= 5;
        if self.rect.bottom < 0:
            self.kill();
        if pygame.sprite.spritecollide(self,alien_grp,True):
            self.kill();
            explosion_fx.play();
            exp = Explosion(self.rect.x,self.rect.y,2);
            explosion_grp.add(exp);
        if pygame.sprite.spritecollide(self,alien_boss_group,False,pygame.sprite.collide_mask):
            self.kill();
            alien_boss.health_remain_boss -= 1;
            explosion2_fx.play();
            exp = Explosion(self.rect.x,self.rect.y,1);
            explosion_grp.add(exp);
            

class Aliens(pygame.sprite.Sprite):
    def __init__(self , x ,y):
        pygame.sprite.Sprite.__init__(self);
        self.image = pygame.image.load("img_game/alien" + str(random.randint(1,5)) +".png");
        self.rect = self.image.get_rect();
        self.rect.center=[x,y];
        self.move_counter = 0;
        self.move_direction = 1;
    def update(self):
        self.rect.x += self.move_direction;
        self.move_counter += 1;
        if abs(self.move_counter) > 75:
            self.move_direction *= -1;
            self.move_counter *= self.move_direction;
        
        
class AlienBoss(pygame.sprite.Sprite):
    def __init__(self , x ,y,health):
        pygame.sprite.Sprite.__init__(self);
        self.image = pygame.image.load('img_game/alien13.png');
        self.rect = self.image.get_rect();
        self.rect.center=[x,y];
        self.move_counter = 0;
        self.move_direction = 1;
        self.health_start = health;
        self.health_remain_boss = health;
        self.move_direction_y = 2;
        self.move_direction_x = 1;
        self.move_counter = 0;
        
    def update(self):
       
        pygame.draw.rect(screen,green,(self.rect.x,self.rect.top - 10,self.rect.width,15));
       
        #update mask for pixel perfect collision
        self.mask = pygame.mask.from_surface(self.image);
        
        if self.health_remain_boss > 0:
            pygame.draw.rect(screen,red,(self.rect.x,(self.rect.top  -  10),int(self.rect.width * (self.health_remain_boss / self.health_start)),15));
        elif self.health_remain_boss <= 0:
            exp = Explosion(self.rect.x,self.rect.y,3);
            explosion_grp.add(exp);
            self.kill();
            game_over = 1;
        if self.rect.y <= 100:
            self.rect.y += self.move_direction_y;
        if self.rect.y > 100:
            print(self.rect.x);
            if self.move_direction_x > 0:
                self.rect.x += 3;
            elif self.move_direction_x < 0:
                self.rect.x -= 3;
                
            self.move_counter += 1;
            if abs(self.move_counter) > 120:
                self.move_direction_x *= -1;
                self.move_counter *= self.move_direction_x;
        

#alien_boss_bullet
class AlienBossBullets(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self);
        self.image = pygame.image.load('img_game/bulletboss.png');
        self.rect = self.image.get_rect();
        self.rect.center =[x,y];
        self.count = 0;
    def update(self):
        
        self.rect.y +=3;
       
                
        if self.rect.top > screen_height:
            self.kill();
        if pygame.sprite.spritecollide(self,ship_grp,False,pygame.sprite.collide_mask):
            self.kill();
            ship.health_remaining -= 1;
            explosion2_fx.play();
            exp = Explosion(self.rect.x,self.rect.y,2);
            explosion_grp.add(exp);
        
#alien bullet class
class AlienBullets(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self);
        self.image = pygame.image.load('img_game/alien_bullet.png');
        self.rect = self.image.get_rect();
        self.rect.center =[x,y];
    def update(self):
        self.rect.y += 2;
        if self.rect.top > screen_height:
            self.kill();
        if pygame.sprite.spritecollide(self,ship_grp,False,pygame.sprite.collide_mask):
            self.kill();
            ship.health_remaining -= 1;
            explosion2_fx.play();
            exp = Explosion(self.rect.x,self.rect.y,1);
            explosion_grp.add(exp);

#explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self , x , y,size):
        pygame.sprite.Sprite.__init__(self);
        self.images = [];
        for num in range(1,6):
            image = pygame.image.load(f'img/exp{num}.png');
            if size == 1:
                image = pygame.transform.scale(image,(20,20));
            if size == 2:
                image = pygame.transform.scale(image,(40,40));
            if size == 3:
                image = pygame.transform.scale(image,(120,120));
            
            self.images.append(image);
        self.index = 0;
        self.image = self.images[self.index];
        self.rect = self.image.get_rect();
        self.rect.center=[x,y];
        self.counter = 0;
    def update(self):
        explosion_speed = 6;
        self.counter += 1;
        
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0;
            self.index += 1;
            self.image = self.images[self.index];
        #if animation is completed
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill() #to kill an instance
        
            
ship = Spaceship(screen_width//2,screen_height - 100,4);
alien_boss = AlienBoss(screen_width // 2, - 100 ,25);
ship_grp = pygame.sprite.Group();
bullet_grp = pygame.sprite.Group();
alien_grp = pygame.sprite.Group();
alien_bullet_grp = pygame.sprite.Group();
explosion_grp = pygame.sprite.Group(); 
alien_boss_group = pygame.sprite.Group();
alien_boss_bullets_grp = pygame.sprite.Group();
 
def create_alien():
    for row in range(rows):
        for col in range(cols):
            alien = Aliens(150 + col * 100 , 200 + row * 70);
            alien_grp.add(alien);
create_alien();   
ship_grp.add(ship);
def create_alien_boss():
            alien_boss_group.add(alien_boss);
            
create_alien_boss(); 
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))  
while run:
    show_bg();
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False;
    ship_grp.draw(screen);
    bullet_grp.draw(screen);
    alien_grp.draw(screen);
    alien_bullet_grp.draw(screen);
    alien_boss_bullets_grp.draw(screen);
    explosion_grp.draw(screen);
    alien_boss_group.draw(screen);
    if countdown > 0:
        draw_text('GET READY!',font2,white,int(screen_width/2 - 100),int(screen_height/2 + 100));
        draw_text(str(countdown),font2,white,int(screen_width/2),int(screen_height/2 + 150));
        time_now = pygame.time.get_ticks();
        if time_now - last_count >= 1000:
            countdown-=1;
            last_count = time_now;
    explosion_grp.update();
    if countdown == 0:
        if game_over == 0:
            game_over = ship.move();    
            bullet_grp.update();
            alien_grp.update();
            alien_bullet_grp.update();
            alien_boss_bullets_grp.update();
            if len(alien_grp) <= 0:
               alien_boss_group.update();
        else:
            if game_over == -1:
                 draw_text('GAME OVER!',font2,white,int(screen_width/2 - 100),int(screen_height/2 + 100));
            if game_over == 1:
                 draw_text('YOU WIN!',font2,white,int(screen_width/2 - 100),int(screen_height/2 + 100));
                 intro.stop();
        
        #create aline bullets
        time_now = pygame.time.get_ticks();
        if time_now - alien_last_hit > alien_cooldown and len(alien_bullet_grp) < 6 and len(alien_grp) > 0:
            attacking_alien = random.choice(alien_grp.sprites());
            alien_bullet = AlienBullets(attacking_alien.rect.centerx,attacking_alien.rect.top);
            alien_bullet_grp.add(alien_bullet);
            alien_last_hit = time_now;
            
        if len(alien_grp) <= 0:
            #create alien boss bullets
            time_now = pygame.time.get_ticks();
            if time_now - alien_last_hit > alien_boss_cooldown and len(alien_boss_bullets_grp) < 50:
                if len(alien_boss_group) <= 0:  
                    game_over = 1;
                else:
                    attacking_alien = random.choice(alien_boss_group.sprites());
                    alien_boss_bullet = AlienBossBullets(attacking_alien.rect.centerx-4,attacking_alien.rect.centery+2);               
                    alien_boss_bullets_grp.add(alien_boss_bullet);
                    alien_last_hit = time_now;
            
        
    pygame.display.update();
pygame.quit();