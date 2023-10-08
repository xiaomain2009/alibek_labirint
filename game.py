from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)

        self.x_speed = player_x_speed
        self.y_speed = player_y_speed


    def update(self):
        # сначала движение по горизонт али
        if packman.rect.x <= win_wight - 80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right,p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left,
                                    p.rect.right)  # если коснулись нескольких стен, то левый край - максимальный
        if packman.rect.y <= win_height - 80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:  # идем вниз
            for p in platforms_touched:
                self.y_speed = 0
                # Проверяем, какая из платформ снизу самая высокая, выравниваемся по ней, запоминаем её как свою опору:
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0:  # идем вверх
            for p in platforms_touched:
                self.y_speed = 0  # при столкновении со стеной вертикальная скорость гасится
                self.rect.top = max(self.rect.top,
                                    p.rect.bottom)  # выравниваем верхний край по нижним краям стенок, на которые наехали

    
    


    def fire(self):
        bullet = Bullet('Bullet.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)


class Enemy(GameSprite):
    size = 'left'

    def __init__(self,player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed


    def update(self):
        if self.rect.x <= 420:
            self.side = 'right'
        if self.rect.x >= win_wight - 85:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed 
        else:
            self.rect.x += self.speed


class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_wight + 10:
            self.kill()

win_wight = 700
win_height = 500

display.set_caption('Лaбиринт')
window = display.set_mode((win_wight, win_height))
back = (119,210,223)

barriers = sprite.Group()

bullets = sprite.Group()

monsters = sprite.Group()

v1 = GameSprite('Platform.png', win_wight / 2 - win_wight / 3, win_height / 2, 300, 50)
v2 = GameSprite('Platform.png', 370, 100, 50, 400)

barriers.add(v1)
barriers.add(v2)

packman = Player('superhero.png', 5,win_height - 80, 80, 80, 0, 0)
final_sprite = GameSprite('fast-food (1).png', win_wight - 85, win_height - 100, 80, 80)

monster1 = Enemy('monster.png', win_wight - 80, 150, 80, 80, 5)
monster2 = Enemy('monster.png', win_wight - 80, 230, 80, 80, 5)

monsters.add(monster1)
monsters.add(monster2)

finish = False
run = True

while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
            elif e.key == K_SPACE:
                packman.fire()

    if not finish:

        window.fill(back)

        packman.update()
        bullets.update()

        packman.reset()

        bullets.draw(window)
        barriers.draw(window)
        final_sprite.reset()

        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)


        if sprite.spritecollide(packman, monsters, False):
            finish = True
            img = image.load('game-over -1.webp')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)),(90, 0))

        if sprite.collide_rect(packman, final_sprite):
            finish = True
            img = image.load('win.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_wight, win_height)), (0, 0))

    display.update()







