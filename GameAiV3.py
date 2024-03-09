import pygame
from random import randint
import os
from time import sleep
import time

#Розширення програми
WIDTH = 700
HEIGHT = 700
FPS = 60

# Ініціалізуємо Pygame та створюємо вікно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gaem")
clock = pygame.time.Clock()

class Area():
    def __init__(self,x,y,width,height,color=(255,0,0),way=None):
        self.rect=pygame.Rect(x,y,width,height)
        self.fill_color=color
        self.hit=0
        self.width=width
        self.height=height
        
        self.way=way
    
    def color(self,new_color):
        self.fill_color=new_color

    def outline(self,frame_color,thickness):
        pygame.draw.rect(screen,frame_color,self.rect,thickness)
    
    def fill(self):
        pygame.draw.rect(screen,self.fill_color,self.rect)

    def collidepoint(self,x,y):
        return self.rect.collidepoint(x,y)
    
    def colliderect(self,rect):
        return self.rect.colliderect(rect)
    
    def collidelist(self,rect_list):
        return self.rect.collidelist(rect_list)

    def rotate(self,rote):
        pass

    def draw(self):
        pygame.draw.rect(screen, self.fill_color,self.rect)
class Enemy(Area):
    def __init__(self,x,y,width,height,color=(255,0,0)):
        self.rect=pygame.Rect(x,y,width,height)
        self.fill_color=color
        
        self.vision_rectHx=Area(x+25,y+5,width,height-10,(255,255,255),"right")
        self.vision_rectH=Area(x-25,y+5,width,height-10,(255,255,255),"left")
        
        self.vision_rectV=Area(x+5,y-25,width-10,height,(255,255,255),"up")
        self.vision_rectVy=Area(x+5,y+25,width-10,height,(255,255,255),"down")
        
        self.ghost_box=Area(x,y,width,height,(125,125,255))
        
        self.run=0
        self.player_oldx=0
        self.player_oldy=0
        self.unstuck=0


        self.moving=True

        self.boxes=[self.vision_rectH,self.vision_rectHx,self.vision_rectV,self.vision_rectVy]
        self.collided=0


        self.timer=-1

        self.randi=0

        self.way_move="right"
    
    def find_collided(self):
        not_collided_boxes=[]
        for i in self.boxes:
            if i.hit == 0:
                not_collided_boxes.append(i)
        return not_collided_boxes

    def draw_hiden(self):
        for i in self.boxes:
            i.draw()
        self.ghost_box.draw()
    
    def hiden_move(self):
        for i in self.boxes:
            if i.way=="up":
                i.rect.x=self.rect.x+5
                i.rect.y=self.rect.y-25
            if i.way=="down":
                i.rect.x=self.rect.x+5
                i.rect.y=self.rect.y+25
            if i.way=="left":
                i.rect.x=self.rect.x-25
                i.rect.y=self.rect.y+5
            if i.way=="right":
                i.rect.x=self.rect.x+25
                i.rect.y=self.rect.y+5


    def find_player(self,player):
        if self.run==0:
            self.ghost_box.hit=0
            self.run=1
            self.ghost_box.rect.x=self.rect.x
            self.ghost_box.rect.y=self.rect.y
        
        direction = pygame.Vector2(player.rect.x - self.ghost_box.rect.x, player.rect.y - self.ghost_box.rect.y)
        direction = direction.normalize()

        speed = 20

        self.ghost_box.rect.x += direction.x * speed
        self.ghost_box.rect.y += direction.y * speed

        if self.ghost_box.collidelist(zones)>=0:
            self.ghost_box.hit=1
        if self.ghost_box.colliderect(player.rect):
            if self.ghost_box.hit==0:
                self.player_oldx=player.rect.x
                self.player_oldy=player.rect.y
            
            self.ghost_box.rect.x=self.rect.x
            self.ghost_box.rect.y=self.rect.y
            self.run=0
            return self.ghost_box.hit


    def go_to(self,x,y):
        
        direction = pygame.Vector2(x - self.rect.x , y - self.rect.y)
        direction = direction.normalize()
        speed = 3  

        self.rect.x += direction.x * speed
        self.rect.y += direction.y * speed
        if self.rect.collidelist(zones)>=0:
            self.rect.x -= direction.x * speed
            self.rect.y -= direction.y * speed
            return 1


        if self.rect.y >= y-10 and self.rect.y <= y+10 and self.rect.x >= x-10 and self.rect.x <= x+10:
            return 1
        else:
            return 0


    def move(self):
        self.hiden_move()

        inner_time=time.time()
        
        if self.timer>int(inner_time)-int(start_time):
            pass
        else:
            self.timer=int(inner_time)-int(start_time)+5
            s=randint(0,5)
            if s == 5:
                self.way_move="still"
            else:
                try:
                    go_to=self.find_collided()
                    self.way_move=go_to[randint(0,len(go_to)-1)].way
                    print("chaged way to: "+self.way_move)
                except:
                    self.way_move="right"
                    print("error1")


        found=self.find_player(block1)
        if self.player_oldx != 0 and self.player_oldy != 0:
            r = self.go_to(self.player_oldx,self.player_oldy)
            if r == 1:
                self.player_oldx=0
                self.player_oldy=0
                self.way_move="still"
                print("served")
        elif self.way_move !="still":
            if self.moving==False:
                colli = self.find_collided()
                try:
                    self.way_move=colli[randint(0,len(colli)-1)].way
                except:
                    self.way_move="right"
                    print("error")

            if self.way_move=="right":
                self.rect.x+=2
                self.moving=True
                
                if self.rect.collidelist(zones)>=0:
                    self.rect.x-=2
                    self.moving=False
            
            if self.way_move=="left":
                self.rect.x-=2
                self.moving=True
                
                if self.rect.collidelist(zones)>=0:
                    self.rect.x+=2
                    self.moving=False
            
            if self.way_move=="up":
                self.rect.y-=2
                self.moving=True
                
                if self.rect.collidelist(zones)>=0:
                    self.rect.y+=2
                    self.moving=False
            
            if self.way_move=="down":
                self.rect.y+=2
                self.moving=True
                
                if self.rect.collidelist(zones)>=0:
                    self.rect.y-=2
                    self.moving=False


        for i in self.boxes:
            if i.rect.collidelist(zones)>=0:
                i.hit=1
            else:
                i.hit=0




block1=Area(325,250,25,25,(255,255,255))
block2=Area(400,200,50,50)
block3=Area(200,300,50,50)

enemy=Enemy(350,75,25,25,(255,0,0))
enemy1=Enemy(350,75,25,25,(255,0,0))
enemy2=Enemy(350,75,25,25,(255,0,0))
enemy3=Enemy(350,75,25,25,(255,0,0))
enemy4=Enemy(350,75,25,25,(255,0,0))
enemy5=Enemy(350,75,25,25,(255,0,0))


blocks=[block2,block3]

map=[1,1,1,1,1,1,1,1,1,1,1,1,2,1,
     2,0,0,0,0,0,0,0,0,0,0,0,0,1,
     1,1,1,0,1,1,1,1,1,1,1,0,0,1,
     1,0,0,0,0,0,0,0,0,0,0,0,0,1,
     1,0,0,1,1,1,1,0,1,1,1,1,0,1,
     1,0,0,0,0,0,0,0,0,0,0,0,0,1,
     1,1,1,1,0,1,1,1,1,1,1,0,0,1,
     1,0,0,0,0,0,0,0,0,0,0,0,0,1,
     1,0,0,1,0,1,1,0,1,1,0,1,0,1,
     1,0,1,0,0,0,0,0,1,0,0,1,0,1,
     1,0,1,0,1,0,1,0,0,0,0,0,0,1,
     1,0,0,0,0,0,0,1,0,1,1,1,0,1,
     1,0,1,0,1,1,0,0,0,0,0,0,0,1,
     1,1,1,1,1,1,1,1,1,1,1,1,1,1]
xm=0
ym=0
zones=[]
escape=[]
#main movement
up=False
down=False
right=False
left=False


# Головний цикл
end = False

start_time=time.time()

while not end:
    #Малювання об'єктів
    screen.fill((0,0,0))
    block1.draw()

    enemy1.draw()
    enemy1.move()

    enemy.draw()
    enemy.move()

    enemy2.draw()
    enemy2.move()

    enemy3.draw()
    enemy3.move()

    enemy4.draw()
    enemy4.move()

    enemy5.draw()
    enemy5.move()

    if enemy.rect.colliderect(block1.rect) or enemy1.rect.colliderect(block1.rect):
        print("game over")
        break
    if block1.collidelist(escape) >=0:
        print("you won!")
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True
        if event.type== pygame.KEYDOWN:
            if event.key ==pygame.K_a:
                left=True
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_a:
                left=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_d:
                right=True
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_d:
                right=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_s:
                down=True
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_s:
                down=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_w:
                up=True
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_w:
                up=False
    if len(zones) != len(map):
        for block in map:
            if block==1:
                zones.append(Area(xm,ym,50,50,(0,100,0)))
                xm+=50
                if xm==700:
                    ym+=50
                    xm=0
            if block==2:
                zones.append(Area(xm,ym,50,50,(255,255,255)))
                escape.append(Area(xm,ym,60,60,(255,255,255)))
                xm+=50
                if xm==700:
                    ym+=50
                    xm=0
            if block==0:
                zones.append(Area(1000,1000,50,50,(0,0,0)))
                xm+=50
                if xm==700:
                    ym+=50
                    xm=0
        print(len(zones))
    for s in zones:
        s.draw()
    

    if left==True:
        block1.rect.x -= 2
        if block1.collidelist(zones)>=0:
            block1.rect.x += 2
    if right==True:
        block1.rect.x += 2
        if block1.collidelist(zones)>=0:
            block1.rect.x -= 2
    if up==True:
        block1.rect.y -= 2
        if block1.collidelist(zones)>=0:
            block1.rect.y += 2
    if down==True:
        block1.rect.y += 2
        if block1.collidelist(zones)>=0:
            block1.rect.y -= 2
    

    # Оновлення
    clock.tick(FPS)
    # Після малювання всього, перевертаємо екран
    pygame.display.update()

pygame.quit()
