import pygame;
import math;
import random;

#setup windowed display
pygame.init();
WIDTH,HEIGHT=800,600;
window = pygame.display.set_mode((WIDTH,HEIGHT));
pygame.display.set_caption('Hangman Clone');

#button variables and set positions
RADIUS=20;
GAP=15;
startx=round((WIDTH-(GAP+(RADIUS*2))*13)/2);#shurur gap

starty=450;
A=65;
letters=[];

for i in range(26):
  x=startx+GAP*2+((GAP+(RADIUS*2))*(i%13));#distance of x or every new button 82.5 meters 1st button then 55 plus to 2nd and so on
  
  y=starty+((i//13)*(GAP+(RADIUS*2)));# position of the 2 rows as 0-12 will give (0~12//13=0 so 1st row and 14~25 2nd row);
  letters.append([x,y,chr(i+A),True]); 
 

#game variables
hangman_status=0;
words=['PYTHON','SUICIDE','APOCALYPSE','LANGUAGE','HANGMAN','ALICE IN WONDERLAND','MATRIX','ZOOLOGY','ASTRONOMY','EGYPT',
       'GAME OF THRONES'];
word = random.choice(words);
guessed=[];
count=0;
pygame.mixer.music.load('Hangmansound.mp3');
pygame.mixer.music.play(-1);

#color
WHITE=(255,255,255);
BLACK=(0,0,0);

#fonts
FONT_STYLE=pygame.font.SysFont('comicsans',40);
WORD_FONT_STYLE = pygame.font.SysFont('comicsans',50);
TITLE_FONT= pygame.font.SysFont('comicsans',75);
#load images
images=[];
for i in range(7):
  images.append(pygame.image.load(f'images/hangman{str(i)}.png'));

def display_msg(msg):
    pygame.time.delay(2000);
    pygame.mixer.music.stop();
    window.fill(WHITE);
    text=WORD_FONT_STYLE.render(msg,1,BLACK);
    window.blit(text,(WIDTH/2-text.get_width()/2,HEIGHT/2-text.get_height()/2));
    if msg == 'You Lose!':
        text=WORD_FONT_STYLE.render(f'Word was {word}',1,BLACK);
        window.blit(text,(WIDTH/2-text.get_width()/2,(HEIGHT/2-text.get_height()/2)+50));
    pygame.display.update();
    pygame.time.delay(4000);


def draw():
  window.fill(WHITE); #fill the window with color
  
  #draw TITLE

  text=TITLE_FONT.render('HANGMAN CLONE',1,BLACK);
  window.blit(text,(WIDTH/2-text.get_width()/2,20))
  # draw words
  
  display_words="";
  for letter in word:
    if letter in guessed:
      display_words+=f'{letter} ';
    elif letter == ' ':
      display_words += letter;
    else:
      display_words += '_ ';
  text=WORD_FONT_STYLE.render(display_words,1,BLACK);    
  window.blit(text,(250,350));  

  for letter in letters:
    x,y,z,visible=letter;
    if visible:
      pygame.draw.circle(window,BLACK,(x,y),RADIUS,3);#draw circle
      character=FONT_STYLE.render(z,1,BLACK);
      window.blit(character,(x-(character.get_width()/2),y-character.get_height()/2));

  #hangman status

  window.blit(images[hangman_status],(100,100)); #fill entire screen with color or images  that is drawn
  pygame.display.update();
  

def main():
    pygame.mixer.music.load('Hangmansound.mp3');
    pygame.mixer.music.play(-1);
    global hangman_status;
    FPS=60;
    clock=pygame.time.Clock();
    global run;
    run = True;
    while run:
     
      clock.tick(FPS);
    #Events
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run=False;
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.K_ESCAPE:
                run = False;
        if event.type == pygame.MOUSEBUTTONDOWN:
          mouse_x,mouse_y=pygame.mouse.get_pos();
          for letter in letters:
            x,y,character,visible=letter;
            if visible:
              distance = math.sqrt((x - mouse_x)**2 + ((y - mouse_y) ** 2));
              if distance < RADIUS:
                letter[3] = False;
                guessed.append(character);
                if character not in word:
                    hangman_status += 1;

      draw();
      
      won=True;
      for letter in word:
        if letter not in guessed:
          won=False;
          break;
      if won:
        print('hello');
        display_msg('You Won!');
        break;
      if hangman_status==6:
        display_msg('You Lose!');
        break;        
while True:   
   if count == 0:
       main();
       count+=1;
   else:
       window.fill(WHITE);
       text = WORD_FONT_STYLE.render('Press any key to continue',1,BLACK);
       window.blit(text,(WIDTH/2-text.get_width()/2,HEIGHT/2-text.get_height()/2));
       pygame.display.update();
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit();
           if event.type == pygame.MOUSEBUTTONDOWN:
                hangman_status =0;
                guessed.clear();
                print(guessed);
                word = random.choice(words);
                print(word);
                for i in range(len(letters)):
                    letters[i][3]=True;
                    
                main();
                  
pygame.quit();      