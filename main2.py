from pygame import *
from random import randint
import os 

font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

font2 = font.Font(None, 36)


mixer.init()
mixer.music.load(r'Assets\space.ogg')
mixer.music.play()
fire_sound = mixer.Sound(r'Assets\fire.ogg')


img_back = r"Assets\galaxy.jpg" 
 
img_bullet = [r"Assets\bullet.png",r'Assets\ShotGun_bullet.png',r"Assets\star_bullet.png"]
boxes = [r"Assets\ShotGun_Bullet_box.png",r"Assets\star_box.png"]
img_hero = r"Assets\rocket.png" 
img_enemy = r"Assets\ufo.png"
score = 0
goal = 500
lost = 0 
max_lost = 10
workdir = os.getcwd() 

class GameSprite(sprite.Sprite):
 
    def __init__(self, image_, width , height , x, y):
       
        sprite.Sprite.__init__(self)

       
        self.image = transform.scale(image.load(os.path.join(image_)), (width,height))

       
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y
 

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    
    def __init__(self, image , width , height , x,y):
        super().__init__(image , width , height, x,y)
        
        self.speed = 10

        self.current_bullet = 0

        self.upgrade_timer = 0



    def update(self):
        keys = key.get_pressed()
        if self.current_bullet != 0:
            
            if self.upgrade_timer <= 3:
                self.upgrade_timer += 0.05

            else:
                self.upgrade_timer = 0

                self.current_bullet = 0

        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
 
    def fire(self):
        bullet = Bullet(img_bullet[self.current_bullet] , 9 , 21 , self)
        bullets.add(bullet)

 
class Enemy(GameSprite):
    def __init__(self, image , width, height, x, y):
        super().__init__(image, width, height, x, y)
        self.speed = randint(1,5)


    def update(self):
        self.rect.y += self.speed
        global lost
        
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
   
class Bullet(GameSprite):
    def __init__(self, image, width, height , player):
        super().__init__(image, width, height , player.rect.x+21 , player.rect.y)
        
        self.bullet = player.current_bullet
        if self.bullet == 0:
            self.speed = 15
        elif self.bullet == 1:
            self.speed = 5
        elif self.bullet == 2:
            self.speed = 50
        
    def update(self):
        self.rect.y -= self.speed
        
        global bullets
        global monsters
        global score

        
        collides = sprite.groupcollide(monsters, bullets, True, True)
        if collides:
            if self.bullet == 1:
               bullet = SBullet(r"Assets\Steel_ball.png" , 25 , 25 , self.rect.x , self.rect.y , 2 , 0 )
               bullets.add(bullet)
               bullet = SBullet(r"Assets\Steel_ball.png" , 25 , 25 , self.rect.x , self.rect.y , -2 , 0 )
               bullets.add(bullet)
            if self.bullet == 2:
                bullet = SBullet(r"Assets\star.png" , 25 , 25 , self.rect.x , self.rect.y , 0 , -2 )
                bullets.add(bullet)
        for c in collides:
            # этот цикл повторится столько раз, сколько монстров подбито
            
            score = score + 1
            monster = Enemy(img_enemy, 50 , 50 , randint(20,600), -20)
            monsters.add(monster)



        if self.rect.y < 0:
            self.kill()

class SBullet(GameSprite):
    def __init__(self, image_, width, height, x, y , dx , dy):
        super().__init__(image_, width, height, x, y)
        self.dx = dx
        self.dy = dy
    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        global ship
        global monsters
        global score

        if ship.current_bullet == 2:
            collides = sprite.groupcollide(monsters, bullets, True, False)
        else:
            collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            
            
            score = score + 1
            monster = Enemy(img_enemy, 50 , 50 , randint(20,600), -20)
            monsters.add(monster)
        
        if self.rect.y < 0 and self.rect.y > 500 and self.rect.x > 700 and self.rect.x < 0:
            self.kill()


class Power_box(GameSprite):
    def __init__(self, image_, width, height, x, y , type):
        super().__init__(image_, width, height, x, y)
        
        self.type = type
        self.speed = 2

    def update(self):
        global ship
        global power_boxes
        
        self.rect.y += self.speed

        collides = sprite.spritecollide(ship , power_boxes , True)

        for c in collides:
            ship.current_bullet = self.type + 1
        if self.rect.y > 500:
            self.kill()

 

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
# создаем спрайты
ship = Player(img_hero, 50 , 50 , 50 , 390)
 
# создание группы спрайтов-врагов
monsters = sprite.Group()
for i in range(0, 6):
    monster = Enemy(img_enemy, 50 , 50 , randint(20,600), -20)
    monsters.add(monster)
print(monsters)

power_boxes = sprite.Group()

bullets = sprite.Group()
 
# переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
# Основной цикл игры:
run = True # флаг сбрасывается кнопкой закрытия окна


timer_1 = 0

while run:
    # событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
        # событие нажатия на пробел - спрайт стреляет
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
 
  # сама игра: действия спрайтов, проверка правил игры, перерисовка
    if not finish:
        
        if timer_1 <= 5:
            timer_1 += 0.05
        else:
            print("END!")
            
            _ = randint(0,1)
            box = Power_box(boxes[_] , 40 , 40 , randint(40,640) , -20 , _)
            power_boxes.add(box)
            
            timer_1 = 0

        

        # обновляем фон
        window.blit(background,(0,0))

        # пишем текст на экране
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        # производим движения спрайтов
        ship.update()
        monsters.update()
        bullets.update()
        power_boxes.update()

        # обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        
        power_boxes.draw(window)

        # проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
        collides = sprite.groupcollide(monsters, bullets, True, True)
       
        for c in collides:
            # этот цикл повторится столько раз, сколько монстров подбито
            score = score + 1
            monster = Enemy(img_enemy, 50 , 50 , randint(20,600), -20)
            monsters.add(monster)




        # возможный проигрыш: пропустили слишком много или герой столкнулся с врагом
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True # проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200))

        # проверка выигрыша: сколько очков набрали?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        display.update()
    # цикл срабатывает каждую 0.05 секунд
    
    time.delay(50)