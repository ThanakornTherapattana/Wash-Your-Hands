import pygame
from pygame.locals import *
from pygame import mixer
import os
import random
pygame.init()

clock = pygame.time.Clock()
fps = 60

WIN_WIDTH, WIN_HEIGHT = 900, 800

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("WASH YOUR HANDS")

#font
font = pygame.font.SysFont('Impact', 50)
white = (255,255,255)


#game variables
bush_scroll = 0
scroll_vel = 5
gravity = False
game_over = False
virus_frequency = 400 #millisec
last_virus = pygame.time.get_ticks()
score = 0
score_counter = 0

player_hp = 100
hit_count = 0

donut_counter = 0

#sound variables
sound = True
hit_sound = mixer.Sound(os.path.join('Assets', 'mixkit-man-coughing-2224.wav'))
falling_sound = mixer.Sound(os.path.join('Assets', 'mixkit-short-whistle-fall-406.wav'))
jumping_sound = mixer.Sound(os.path.join('Assets', 'mixkit-player-jumping-in-a-video-game-2043.wav'))
collect_sound = mixer.Sound(os.path.join('Assets', 'mixkit-game-treasure-coin-2038.wav'))

#load image
bg = pygame.image.load(
    os.path.join('Assets', 'city background.png'))
bg = pygame.transform.scale(bg, (WIN_WIDTH, WIN_HEIGHT))

bush = pygame.image.load(
    os.path.join('Assets', 'bush2.png'))
bush = pygame.transform.scale(bush, (500*2.5, WIN_HEIGHT))

button_img = pygame.image.load(os.path.join('Assets', 'reset button.png'))
button_img = pygame.transform.scale(button_img, (180, 66))



def draw_text(text, font, text_col, x, y) :
    img = font.render(text, True, text_col)
    WIN.blit(img, (x, y))
    
def reset_game():
    
    global player_hp
    virus.empty()
    donut_group.empty()
    player_pos.rect.x = 100
    player_pos.rect.y = int(WIN_HEIGHT/2)
    score = 0
    player_hp = 100
    return score
    
    
    


class Player(pygame.sprite.Sprite) :
    #player function
    def __init__(self, x, y):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            os.path.join('Assets', 'fallingplayer.png'))
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
    
    def update(self):
        
        if gravity == True :
            #garvity
            self.vel += 1
            if self.vel > 15 :
                self.vel = 15
            if self.rect.bottom < 800 :
                self.rect.y += int(self.vel)
        
        if game_over == False and sound == True:
            #jump and animation?
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -13
                
                self.image = pygame.image.load(
                    os.path.join('Assets', 'jumpingplayer.png'))
                self.image = pygame.transform.scale(self.image, (50, 50))
                jumping_sound.play()
                
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            
                self.image = pygame.image.load(
                    os.path.join('Assets', 'fallingplayer.png'))
                self.image = pygame.transform.scale(self.image, (50, 50))
            

class Virus(pygame.sprite.Sprite) :
    
    def __init__(self, x, y) :
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        #add images to the list
        for num in range(1,3) :
            img = pygame.image.load(os.path.join('Assets', f'virus{num}.png'))
            self.images.append(img)
        #use image in the list
        self.image = self.images[self.index]
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
    
    def update(self) :
        #animation cooldown
        self.counter += 1
        cooldown = 5
        
        if self.counter > cooldown :
            self.counter = 0
            self.index += 1
            if self.index == len(self.images):
                self.index = 0
        #draw virus
        self.image = self.images[self.index]
        self.image = pygame.transform.scale(self.image, (60, 60))
        
        #start moving
        if gravity == True :
            self.rect.x -= scroll_vel
            
        if self.rect.right < 0 :
            self.kill()

class Donut(pygame.sprite.Sprite) :
    def __init__(self, x, y): 
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            os.path.join('Assets', 'donut.png'))
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]   
        
    def update(self) :
        if gravity == True :
            self.rect.x -= scroll_vel
        if self.rect.right < 0 :
            self.kill()
        #get donut
        if pygame.sprite.groupcollide(player, donut_group, False, False) and game_over == False: 
            global player_hp
            self.kill()
            player_hp += 10
            collect_sound.play()
            if player_hp > 100 :
                player_hp = 100
 
class Button():
    
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
    def draw(self):
        
        action = False
        
        #get mouse position
        pos = pygame.mouse.get_pos()
        
        #check if mouse is over the button
        if self.rect.collidepoint(pos) :
            if pygame.mouse.get_pressed()[0] == 1 :
                action = True
                
        WIN.blit(self.image, (self.rect.x, self.rect.y))
        
        return action
        


player = pygame.sprite.Group()
player_pos = Player(100, int(WIN_HEIGHT/2))
player.add(player_pos)

virus = pygame.sprite.Group()

donut_group = pygame.sprite.Group()

#create restart button
button = Button(WIN_WIDTH / 2 - 90, WIN_HEIGHT /2 - 33, button_img)

#main loop  
run = True
while run :
    clock.tick(fps)
    
            
    
    #draw background
    WIN.blit(bg, (0,0))
    WIN.blit(bush,(bush_scroll,0))
    WIN.blit(bush,(bush_scroll + 1250, 0))
    
    #player draw   
    player.draw(WIN)
    player.update()
    #virus
    virus.draw(WIN)
    
    #donut
    donut_group.draw(WIN)
    
    
    
    #check the score
    if gravity == True and game_over == False :
        score_counter += 1
        score_frequency = 50
        if score_counter > score_frequency :
            score += 1
            score_counter = 0

            
    draw_text('Score : ' + (str(score)), font, white, 350, 730)
    draw_text('Hp : ' + (str(player_hp)), font, white, 700, 730)
    
    #hit virus
    hit_cooldown = 30
    hit_count += 1
    if pygame.sprite.groupcollide(player, virus, False, False) and game_over == False:
        if hit_count > hit_cooldown :
            player_hp -= 15  
            hit_sound.play()
            hit_count = 0
                
        if player_hp <= 0 :
            player_hp = 0
            game_over = True
            if sound == True :
                falling_sound.play()
                sound = False   
            
    #hit the top
    if player_pos.rect.top < 0 :
            game_over = True

            if sound == True :
                falling_sound.play()
                sound = False
        
        
        
    #check if player hit the ground
    if player_pos.rect.bottom > 800 :
        game_over = True
        gravity = False
    
    if game_over == False :
        
        if gravity == True :
            #generate virus
            time_now = pygame.time.get_ticks()
            if time_now - last_virus > virus_frequency :
                virus_y = random.randint(1,740)
                virus_pos = Virus(WIN_WIDTH, virus_y)
                virus.add(virus_pos)
                last_virus = time_now
                
            #spawn donut      
            donut_counter += 1 
            if donut_counter > 100 :
                donut_y = random.randint(1, 740)
                donut_pos = Donut(WIN_WIDTH, donut_y)
                donut_group.add(donut_pos)
                donut_counter = 0


        #bush scroll
        if bush_scroll == -1250 :
            bush_scroll = 0
        bush_scroll -= scroll_vel
    

        virus.update()
        donut_group.update()

    #check for game over and reset
    if game_over == True and gravity == False:
        button.draw()
        if button.draw() == True :
            game_over = False
            score = reset_game()
            sound = True
            
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and gravity == False and game_over == False:
            gravity = True
 
    
    pygame.display.update()     
                            
pygame.quit()