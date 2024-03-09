import asyncio
import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH,HEIGHT=900,500
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('First game!')
    
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)
GREEN=(0,255,0)

FPS=60

direction=False

HEALTH_FONT=pygame.font.SysFont('sans',40)
WINNER_FONT=pygame.font.SysFont('sans',100)

BULLET_HIT_SOUND=pygame.mixer.Sound(os.path.join('Assets','Grenade-1.ogg'))
BULLET_FIRE_SOUND=pygame.mixer.Sound(os.path.join('Assets','Gun-Silencer.ogg'))

SPACESHIP_WIDTH,SPACESHIP_HEIGHT=55,40

YELLOW_HIT=pygame.USEREVENT+1
RED_HIT=pygame.USEREVENT+2
GREEN_HIT_YELLOW=pygame.USEREVENT+3
GREEN_HIT_RED=pygame.USEREVENT+4

VEL=5
BULLET_VEL=15
MAX_BULLETS=3

BORDER=pygame.Rect(WIDTH//2-5,0,10,HEIGHT)
BORDER1=pygame.Rect(WIDTH//4-5,0,10,HEIGHT)
BORDER2=pygame.Rect(3*WIDTH//4-5,0,10,HEIGHT)

YELLOW_SPACESHIP_IMAGE=pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
YELLOW_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)
RED_SPACESHIP_IMAGE=pygame.image.load(os.path.join('Assets','spaceship_red.png'))
RED_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)
 
SPACE=pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')),(WIDTH,HEIGHT))

def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health,green_square):
    WIN.blit(SPACE,(0,0))
    pygame.draw.rect(WIN,BLACK,BORDER)
    pygame.draw.rect(WIN,GREEN,green_square)
    pygame.draw.rect(WIN,BLACK,BORDER1)
    pygame.draw.rect(WIN,BLACK,BORDER2)


    red_health_text=HEALTH_FONT.render('RED HEALTH: '+str(red_health),1,WHITE)
    yellow_health_text=HEALTH_FONT.render('YELLOW HEALTH: '+str(yellow_health),1,WHITE)

    WIN.blit(red_health_text,(WIDTH-red_health_text.get_width()-70,10))
    WIN.blit(yellow_health_text,(10,10))


    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x,red.y)) 

    for bullet in red_bullets: 
        pygame.draw.rect(WIN,RED,bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)
    pygame.display.update()

def yellow_handle_movement(keys_pressed,yellow):
        if keys_pressed[pygame.K_a] and yellow.x-VEL>0:#LEFT
            yellow.x-=VEL
        if keys_pressed[pygame.K_d] and yellow.x+VEL+yellow.width<BORDER1.x:#RIGHT
            yellow.x+=VEL
        if keys_pressed[pygame.K_w] and yellow.y-VEL>0:#UP
            yellow.y-=VEL
        if keys_pressed[pygame.K_s] and yellow.y+VEL+yellow.height<HEIGHT-15:#DOWN
            yellow.y+=VEL

def red_handle_movement(keys_pressed,red):
        if keys_pressed[pygame.K_j] and red.x-VEL>BORDER2.x+BORDER2.width:#LEFT
            red.x-=VEL
        if keys_pressed[pygame.K_l] and red.x+VEL+red.width<WIDTH:#RIGHT
            red.x+=VEL
        if keys_pressed[pygame.K_i] and red.y-VEL>0:#UP
            red.y-=VEL
        if keys_pressed[pygame.K_k] and red.y+VEL+red.height<HEIGHT-15:#DOWN
            red.y+=VEL

def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x+=BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
            BULLET_HIT_SOUND.play()
        elif bullet.x>WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x-=BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
            BULLET_HIT_SOUND.play()

        elif bullet.x<0:
            red_bullets.remove(bullet)

def green_handle(green_square):
    global direction
    if green_square.y+green_square.height+VEL*2==HEIGHT:
        direction=False
    if  green_square.y-VEL*2==0:
        direction=True
    if direction==False:
        green_square.y-=VEL*2
    elif direction:
        green_square.y+=VEL*2

def green_collison(green_square,red_health,yellow_health,red_bullets,yellow_bullets):
    for bullet in yellow_bullets:
        if green_square.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GREEN_HIT_YELLOW))
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        if green_square.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GREEN_HIT_RED))
            red_bullets.remove(bullet)

def draw_winner(winner_text): 
    winner=WINNER_FONT.render(winner_text,1,WHITE)
    WIN.blit(winner,(WIDTH//2-winner.get_width()//2,HEIGHT//2-winner.get_height()//2))
    pygame.display.update()
    pygame.time.delay(100)

async def main():
    red=pygame.Rect(700,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow=pygame.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    green_square=pygame.Rect(WIDTH//2-20,HEIGHT//2-20,40,40)

    red_bullets=[]
    yellow_bullets=[]

    red_health=10
    yellow_health=10

    clock=pygame.time.Clock()
    run=True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                pygame.quit()

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_TAB  and len(yellow_bullets)<MAX_BULLETS:
                    bullet=pygame.Rect(yellow.x+yellow.width,yellow.y+yellow.height//2-2,10,5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key==pygame.K_SPACE and len(red_bullets)<MAX_BULLETS:
                    bullet=pygame.Rect(red.x,red.y+red.height//2-2,10,5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            
            if event.type==RED_HIT:
                red_health-=1
                
            if event.type==YELLOW_HIT:
                yellow_health-=1
            
            if (event.type==GREEN_HIT_YELLOW and yellow_health!=1):
                yellow_health-=2

            if (event.type==GREEN_HIT_YELLOW and yellow_health==1):
                yellow_health-=1

            if (event.type==GREEN_HIT_RED and red_health!=1):
                red_health-=2

            if (event.type==GREEN_HIT_RED and red_health==1):
                red_health-=1

        winner_text=''
        if red_health<=0:
            winner_text='YELLOW WINS!'
            draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health,green_square) 

        if yellow_health<=0:
            winner_text='RED WINS!'
            draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health,green_square) 
            
        if winner_text:
            draw_winner(winner_text)
            break

        keys_pressed=pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed,red)
        handle_bullets(yellow_bullets,red_bullets,yellow,red)
        green_handle(green_square)
        green_collison(green_square,red_health,yellow_health,red_bullets,yellow_bullets)
        draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health,green_square) 
        if(red_health>0 and yellow_health>0):
            await asyncio.sleep(0)
    pygame.quit()

# if __name__=="__main__":
#     main()

asyncio.run(main())