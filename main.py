from math import cos, sin, pi



import datetime
import pygame
import time

from libs import emeny
from libs import barman
from libs import invertory
from libs import items

t1 = datetime.datetime.now()

def joyer(n):
    global MainHero
    if n == 'w':
        user.KeyPressed.append(pygame.K_w)
    if n == 'a':
        user.KeyPressed.append(pygame.K_a)
    if n == 's':
        user.KeyPressed.append(pygame.K_s)
    if n == 'd':
        user.KeyPressed.append(pygame.K_d)


def joyClean():
    if pygame.K_w in user.KeyPressed:
        del user.KeyPressed[user.KeyPressed.index(pygame.K_w)]
    if pygame.K_a in user.KeyPressed:
        del user.KeyPressed[user.KeyPressed.index(pygame.K_a)]
    if pygame.K_s in user.KeyPressed:
        del user.KeyPressed[user.KeyPressed.index(pygame.K_s)]
    if pygame.K_d in user.KeyPressed:
        del user.KeyPressed[user.KeyPressed.index(pygame.K_d)]

# смена кадров и счёт fps
def flip():
    global t1
    pygame.draw.rect(user.screen, 'black', (0, 0, 40, 20))
    try:
        user.screen.blit(
            font.render(str(int(1000 / ((datetime.datetime.now() - t1).microseconds / 1000))), True, (255, 255, 0)),
            (0, 0))
    except ZeroDivisionError:
        user.screen.blit(font.render('err', True, (255, 0, 0)), (0, 0))
    pygame.display.flip()
    t1 = datetime.datetime.now()


# отрисовка кода
def hud():
    user.screen.fill((0, 0, 0))
    user.level.draw()
    user.AS.draw(user.screen)
    pygame.draw.rect(user.screen, 'white', (user.size[0] - 64, 0, 32, 96), width=1)
    pygame.draw.rect(user.screen, 'white', (user.size[0] - 96, 32, 96, 32), width=1)


# управляющий класс
class settings:
    def __init__(self, fps=60, size='1280x720', level=None, autosize=False):
        self.fps = fps
        self.KeyPressed = []
        if autosize:
            size = str(pygame.display.Info().current_w) + 'x' + str(pygame.display.Info().current_h)
        self.size = list(map(int, size.split('x')))
        self.level = level
        self.screen = None
        self.AS = pygame.sprite.Group()
        self.S = []
        self.floor = []


    def load_guys(self, path):
        self.AS = pygame.sprite.Group()
        with open(path, 'r') as data:
            data2 = [i.replace('\n', '') for i in data.readlines()]
            MainHero.x = int(data2[0].split()[0])
            MainHero.y = int(data2[0].split()[1])
            self.floor = [int(i) for i in data2[1].split(' ')]
            for i in data2[2:]:
                if i.split()[0] == 'Bar':
                    self.S.append(barman.Bar(int(i.split()[1]), int(i.split()[2]), self.size, self.AS))
                if i.split()[0] == 'Elf':
                    self.S.append(emeny.Elf(int(i.split()[1]), int(i.split()[2]), self.size, self.AS))
                if i.split()[0] == 'Slime':
                    self.S.append(emeny.Slime(int(i.split()[1]), int(i.split()[2]), self.size, self.AS))

    def add(self, sth, todo=0):
        if todo == 0:
            self.S.append(sth)
        elif todo == 1:
            for i in range(len(self.S)):
                if id(self.S[i]) == id(sth):
                    self.AS.remove(self.S[i])
                    del self.S[i]
                    break

    def change_level(self, path: str):
        with open(path + '.map') as data:
            self.level = Map([list(map(int, i.split())) for i in data.readlines()])
        for i in self.S:
            self.AS.remove(i)
        self.S = []
        self.load_guys(path + '.guys')



# класс карты
class Map:
    def __init__(self, map: list):
        self.map = map
        self.wall = pygame.image.load('data/wall.png')
        self.grass = pygame.image.load('data/grass.png')
        self.barrier = pygame.image.load('data/barrier.png')
        self.barrierh = pygame.image.load('data/barrierh.png')
        self.portal = pygame.image.load('data/portal.png')
        self.bar = pygame.image.load('data/bar.png')
        self.stone = pygame.image.load('data/stone.png')
        self.bookcase = pygame.image.load('data/bookcase.png')
        self.table = pygame.image.load('data/table.png')
        self.chair = pygame.image.load('data/chair.png')
        self.door = pygame.image.load('data/Снимок экрана 2021-01-01 в 20.27.53.png')
        self.stone.set_colorkey(-1)

    def draw(self):
        for j in range((MainHero.y - user.size[1] // 2) // 32, (MainHero.y + user.size[1] // 2) // 32 + 1):
            for i in range((MainHero.x - user.size[0] // 2) // 32, (MainHero.x + user.size[0] // 2) // 32 + 1):
                if j < 0 or j >= len(self.map) or i < 0 or i >= len(self.map[0]):
                    continue
                if self.map[j][i] == 0:
                    user.screen.blit(self.grass, (user.size[0] // 2 + i * 32 - MainHero.x,
                                                  user.size[1] // 2 + j * 32 - MainHero.y))
                elif self.map[j][i] == 1:
                    user.screen.blit(self.wall, (user.size[0] // 2 + i * 32 - MainHero.x,
                                                 user.size[1] // 2 + j * 32 - MainHero.y))
                elif self.map[j][i] == 2:
                    user.screen.blit(self.stone, (user.size[0] // 2 + i * 32 - MainHero.x,
                                                  user.size[1] // 2 + j * 32 - MainHero.y))
                elif self.map[j][i] == 3:
                    user.screen.blit(self.barrier, (user.size[0] // 2 + i * 32 - MainHero.x,
                                                    user.size[1] // 2 + j * 32 - MainHero.y))
                elif self.map[j][i] == 4:
                    user.screen.blit(self.barrierh, (user.size[0] // 2 + i * 32 - MainHero.x,
                                                     user.size[1] // 2 + j * 32 - MainHero.y))
                elif self.map[j][i] == 5:
                    user.screen.blit(self.bar, (user.size[0] // 2 + i * 32 - MainHero.x,
                                                user.size[1] // 2 + j * 32 - MainHero.y))

                elif self.map[j][i] == 6:
                    user.screen.blit(self.portal, (user.size[0] // 2 + i * 32 - MainHero.x,
                                                   user.size[1] // 2 + j * 32 - MainHero.y))
                elif self.map[j][i] == 7:
                    user.screen.blit(self.bookcase, (user.size[0] // 2 + i * 32 - MainHero.x,
                                                   user.size[1] // 2 + j * 32 - MainHero.y))
                elif self.map[j][i] == 8:
                    user.screen.blit(self.chair, (user.size[0] // 2 + i * 32 - MainHero.x,
                                                   user.size[1] // 2 + j * 32 - MainHero.y))
                elif self.map[j][i] == 9:
                    user.screen.blit(self.table, (user.size[0] // 2 + i * 32 - MainHero.x,
                                                   user.size[1] // 2 + j * 32 - MainHero.y))
                elif self.map[j][i] == 10:
                    user.screen.blit(self.door, (user.size[0] // 2 + i * 32 - MainHero.x,
                                                  user.size[1] // 2 + j * 32 - MainHero.y))

    # функция проверки не вошёл ли объект (x, y (32x32px)) в текстуру
    def check(self, x, y: int, size=16):
        try:
            if self.map[(y - size) // 32][(x - size) // 32] in user.floor and\
                    self.map[(y - size) // 32][(x + size - 1) // 32] in user.floor and\
                    self.map[(y + size - 1) // 32][(x - size) // 32] in user.floor and\
                    self.map[(y + size - 1) // 32][(x + size - 1) // 32] in user.floor:
                return True
            return False
        except IndexError:
            return False


# класс главного героя
class Hero:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.image = pygame.image.load('data/main.png')
        self.image.set_colorkey((0, 0, 0))
        self.pow = 0
        self.flipped = False
        self.stamina = 1000
        self.manna = 1000
        self.health = 1000
        self.back = invertory.inv()
        self.equip = [None for i in range(5)]

    # функция отрисовки героя и его параметров(health, stamina, manna)
    def draw(self):
        user.screen.blit(self.image, (user.size[0] // 2 - 16, user.size[1] // 2 - 16))
        if self.stamina < 300:
            pygame.draw.line(user.screen, 'red', (user.size[0] // 2 + 18, user.size[1] // 2 + 16),
                             (user.size[0] // 2 + 18, user.size[1] // 2 + 16 - (self.stamina // 31)), width=3)
        elif self.stamina < 500:
            pygame.draw.line(user.screen, 'yellow', (user.size[0] // 2 + 18, user.size[1] // 2 + 16),
                             (user.size[0] // 2 + 18, user.size[1] // 2 + 16 - (self.stamina // 31)), width=3)
        elif self.stamina != 1000:
            pygame.draw.line(user.screen, 'white', (user.size[0] // 2 + 18, user.size[1] // 2 + 16),
                             (user.size[0] // 2 + 18, user.size[1] // 2 + 16 - (self.stamina // 31)), width=3)
        if self.manna != 1000:
            pygame.draw.line(user.screen, 'blue', (user.size[0] // 2 - 18, user.size[1] // 2 + 16),
                             (user.size[0] // 2 - 18, user.size[1] // 2 + 16 - (self.manna // 31)), width=3)
        if self.health < 250:
            pygame.draw.line(user.screen, 'red', (user.size[0] // 2 - 16, user.size[1] // 2 - 18),
                             (user.size[0] // 2 - 16 + (self.health // 31), user.size[1] // 2 - 18), width=3)
        elif self.health < 500:
            pygame.draw.line(user.screen, 'yellow', (user.size[0] // 2 - 16, user.size[1] // 2 - 18),
                             (user.size[0] // 2 - 16 + (self.health // 31), user.size[1] // 2 - 18), width=3)
        elif self.health != 1000:
            pygame.draw.line(user.screen, 'green', (user.size[0] // 2 - 16, user.size[1] // 2 - 18),
                             (user.size[0] // 2 - 16 + (self.health // 31), user.size[1] // 2 - 18), width=3)

        for i in range(len(self.equip)):
            if self.equip[i]:
                self.equip[i].DrawEquip(user.screen, user.size)

    # функция отрисовки удара и просчёт нанесения урона по Emeny
    def punch(self, pov):
        # отрисовка удара
        R = 32
        x1 = user.size[0] // 2 + int(R * cos(pov * pi / 180))
        y1 = user.size[1] // 2 + int(R * sin(pov * pi / 180))
        x2 = x1
        y2 = y1
        for i in range(0, 100):
            rad = (i + pov) * pi / 180
            pygame.draw.line(user.screen, (i, i, i),
                             (user.size[0] // 2, user.size[1] // 2), (x2, y2), width=1)
            pygame.draw.line(user.screen, 'white', (x1, y1), (x2, y2), width=1)
            x2 = x1
            y2 = y1
            x1 = int(R * cos(rad)) + user.size[0] // 2
            y1 = int(R * sin(rad)) + user.size[1] // 2
            if i % 10 == 0:
                self.draw()
                flip()
                time.sleep(0.01)
        # просчет удара по Emeny
        pov = (pov + 50) // 90
        k = 0
        for i in range(len(user.S)):
            if pov == 0 and MainHero.y - 32 <= user.S[i - k].y <= MainHero.y and MainHero.x - 16 <= \
                    user.S[i - k].x < MainHero.x + 16:
                user.S[i - k].health -= (self.equip[0].damage if self.equip[0] else 1)
                if user.S[i - k].health < 1:
                    user.AS.remove(user.S[i - k])
                    del user.S[i - k]
                    k += 1
            if pov == 1 and MainHero.y - 16 <= user.S[i - k].y <= MainHero.y + 16 and MainHero.x - 32 <= \
                    user.S[i - k].x < MainHero.x:
                user.S[i - k].health -= (self.equip[0].damage if self.equip[0] else 1)
                if user.S[i - k].health < 1:
                    user.AS.remove(user.S[i - k])
                    del user.S[i - k]
                    k += 1
            if pov == 2 and MainHero.y - 32 <= user.S[i - k].y <= MainHero.y and MainHero.x - 48 <= \
                    user.S[i - k].x < MainHero.x - 16:
                user.S[i - k].health -= (self.equip[0].damage if self.equip[0] else 1)
                if user.S[i - k].health < 1:
                    user.AS.remove(user.S[i - k])
                    del user.S[i - k]
                    k += 1
            if pov == 3 and MainHero.y - 48 <= user.S[i - k].y <= MainHero.y - 16 and MainHero.x - 32 <= \
                    user.S[i - k].x < MainHero.x:
                user.S[i - k].health -= (self.equip[0].damage if self.equip[0] else 1)
                if user.S[i - k].health < 1:
                    user.AS.remove(user.S[i - k])
                    del user.S[i - k]
                    k += 1


if __name__ == '__main__':

    pygame.init()
    pygame.joystick.init()
    joy = pygame.joystick.Joystick(0)
    MainHero = Hero()
    user = settings(autosize=True)
    user.change_level('maps/lobby')
    # подгрузочка всякой всячены
    cursor = []
    cursori = pygame.image.load('data/cursor.png')

    pygame.display.set_caption('PyG')

    pygame.mouse.set_visible(False)
    run_image = pygame.image.load('data/main_run.png')
    user.screen = pygame.display.set_mode(user.size, pygame.FULLSCREEN)
    font = pygame.font.Font(None, 30)
    MainLoop = True
    clock = pygame.time.Clock()

    MainHero.image.convert_alpha()
    MainHero.back.append(items.Weapon(2, 0.5))
    MainHero.back.append(items.Armor(20, 0.1))

    # создание Emeny

    while MainLoop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                MainLoop = False
            if event.type == pygame.JOYAXISMOTION:
                joyClean()
                if joy.get_axis(0) > 0.4:
                    joyer('d')
                if joy.get_axis(0) < -0.4:
                    joyer('a')
                if joy.get_axis(1) > 0.4:
                    joyer('s')
                if joy.get_axis(1) < -0.4:
                    joyer('w')
                if joy.get_axis(5) > 0.99:
                    MainHero.punch(MainHero.pow * 90 - 50)
                if joy.get_axis(2) > 0.99:
                    if pygame.K_SPACE not in user.KeyPressed:
                        user.KeyPressed.append(pygame.K_SPACE)

            if event.type == pygame.MOUSEMOTION:
                cursor = event.pos
            if event.type == pygame.KEYDOWN:
                user.KeyPressed.append(event.key)
            if event.type == pygame.KEYUP:
                try:
                    del user.KeyPressed[user.KeyPressed.index(event.key)]
                except:
                    pass
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if user.size[0] // 2 - 20 < event.pos[0] < user.size[0] // 2 + 20 and \
                        user.size[1] // 2 - 20 < event.pos[1] < user.size[1] // 2 + 20:
                    MainHero.health -= 300
                else:
                    if user.size[1] // 2 - cursor[1] > abs(cursor[0] - user.size[0] // 2):
                        MainHero.pow = 3
                        MainHero.punch(MainHero.pow * 90 - 50)
                    elif user.size[1] // 2 - cursor[1] < -abs(cursor[0] - user.size[0] // 2):
                        MainHero.pow = 1
                        MainHero.punch(MainHero.pow * 90 - 50)
                    elif cursor[0] < user.size[0] // 2:
                        MainHero.pow = 2
                        MainHero.punch(MainHero.pow * 90 - 50)
                    else:
                        MainHero.pow = 0
                        MainHero.punch(MainHero.pow * 90 - 50)

        # обработка нажатий
        if user.KeyPressed:
            if pygame.K_ESCAPE in user.KeyPressed:
                pygame.quit()
                exit('Exit -> 02')
            if pygame.K_w in user.KeyPressed:
                MainHero.pow = 3
                if user.level.check(MainHero.x, MainHero.y - 2):
                    MainHero.y -= 2
            if pygame.K_s in user.KeyPressed:
                MainHero.pow = 1
                if user.level.check(MainHero.x, MainHero.y + 2):
                    MainHero.y += 2

            if pygame.K_a in user.KeyPressed:
                MainHero.pow = 2
                if user.level.check(MainHero.x - 2, MainHero.y):
                    MainHero.x -= 2
                if not MainHero.flipped:
                    MainHero.image = pygame.transform.flip(MainHero.image, True, False)
                    run_image = pygame.transform.flip(run_image, True, False)
                    MainHero.flipped = True
            if pygame.K_d in user.KeyPressed:
                MainHero.pow = 0
                if user.level.check(MainHero.x + 2, MainHero.y):
                    MainHero.x += 2
                if MainHero.flipped:
                    MainHero.image = pygame.transform.flip(MainHero.image, True, False)
                    run_image = pygame.transform.flip(run_image, True, False)
                    MainHero.flipped = False

            if pygame.K_SPACE in user.KeyPressed:
                hud()
                CanJump = True
                if MainHero.pow == 0 and MainHero.x < len(user.level.map[0]) * 32 - 144 and \
                        user.level.check(MainHero.x + 128, MainHero.y) and MainHero.stamina > 300:
                    MainHero.stamina -= 300
                    MainHero.x += 128
                elif MainHero.pow == 1 and MainHero.y < len(user.level.map) * 32 - 144 and \
                        user.level.check(MainHero.x, MainHero.y + 128) and MainHero.stamina > 300:
                    MainHero.stamina -= 300
                    MainHero.y += 128
                elif MainHero.pow == 2 and MainHero.x > 144 and \
                        user.level.check(MainHero.x - 128, MainHero.y) and MainHero.stamina > 300:
                    MainHero.stamina -= 300
                    MainHero.x -= 128
                elif MainHero.pow == 3 and MainHero.y > 144 and \
                        user.level.check(MainHero.x, MainHero.y - 128) and MainHero.stamina > 300:
                    MainHero.stamina -= 300
                    MainHero.y -= 128
                else:
                    CanJump = False
                if CanJump:
                    tempx = user.size[0] // 2
                    tempy = user.size[1] // 2
                    for i in range(1, 15):
                        if MainHero.pow == 0:
                            tempx -= i
                        if MainHero.pow == 1:
                            tempy -= i
                        if MainHero.pow == 2:
                            tempx += i
                        if MainHero.pow == 3:
                            tempy += i
                        user.screen.blit(run_image, (tempx - 16, tempy - 16))
                        flip()
                        MainHero.draw()
                        time.sleep(0.01)
                    hud()
                    del user.KeyPressed[user.KeyPressed.index(pygame.K_SPACE)]

            if pygame.K_e in user.KeyPressed:
                user.KeyPressed = []
                hud()
                MainHero.draw()
                flip()
                ret = invertory.draw(user.screen, MainHero.back, cursor[0], cursor[1])
                if ret != -1:
                    if ret[1] == 1:
                        if type(MainHero.back[ret[0] - 1]) == items.Weapon:
                            MainHero.equip[0] = MainHero.back[ret[0] - 1]
                        elif type(MainHero.back[ret[0] - 1]) == items.Armor:
                            MainHero.equip[1] = MainHero.back[ret[0] - 1]

        # отрисовка всякой всячены(иницализированой в одном из прошлых комментариев)
        hud()
        MainHero.draw()
        health = [MainHero.health] # Передача в функцию user.AS.update ссылки на переменную
        user.AS.update(MainHero.x, MainHero.y, user.size, user.level.check, user.add, health)
        MainHero.health = ((MainHero.health if MainHero.equip[1].defend * len(user.S) > (MainHero.health - health[0])
                     else health[0] + MainHero.equip[1].defend * len(user.S)) if MainHero.equip[1] else health[0])
        health = None
        user.screen.blit(cursori, cursor)
        flip()
        clock.tick(user.fps)

        if MainHero.health < 0:
            MainLoop = False

        if MainHero.stamina < 1000:
            MainHero.stamina += 1
        if MainHero.health < 1000:
            MainHero.health += 1
        if MainHero.manna < 1000:
            MainHero.manna += 1

    # YOU DIED
    MainLoop = False
    font = pygame.font.Font('data/font.ttf', user.size[1] // 4)
    font2 = pygame.font.Font(None, 32)
    for i in range(255):
        text = font.render('YOU DIED', True, (i, 0, 0))
        text_rect = text.get_rect(center=(user.size[0] // 2, user.size[1] / 2))
        user.screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(0.01)
    while MainLoop:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                MainLoop = False
    pygame.quit()
    exit('Exit -> 01')
