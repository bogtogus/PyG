import pygame, time, random, datetime
from math import cos, sin, pi
import invertory, emeny, items

t1 = datetime.datetime.now()


# смена кадров и счёт fps
def flip():
    global t1
    pygame.draw.rect(user.screen, 'black', (0, 0, 40, 20))
    try:
        user.screen.blit(font.render(str(int(1000 / ((datetime.datetime.now() - t1).microseconds / 1000))), True, 'yellow'), (0, 0))
    except:
        user.screen.blit(font.render('err', True, 'red'), (0, 0))
    pygame.display.flip()
    t1 = datetime.datetime.now()

# отрисовка кода
def hud():
    user.screen.fill((0, 0, 0))
    user.level.draw()
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

    def load_guys(self, path):
        self.AS = pygame.sprite.Group()
        self.S = []
        with open('maps/level1.guys', 'r') as data:
            data2 = [i.replace('\n', '') for i in data.readlines()]
            MainHero.x = int(data2[0].split()[0])
            MainHero.y = int(data2[0].split()[1])
            for i in data2[1:]:
                if i.split()[0] == 'Slime':
                    user.S.append(emeny.Slime(int(i.split()[1]), int(i.split()[2]), user.size, user.AS))
            print(len(user.S))



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

    # функция проверки не вошёл ли объект (x, y (32x32px)) в текстуру
    def check(self, x, y: int):
        try:
            if self.map[(y - 16) // 32][(x - 16) // 32] == 0 and self.map[(y - 16) // 32][(x + 15) // 32] == 0 and\
                    self.map[(y + 15) // 32][(x - 16) // 32] == 0 and self.map[(y + 15) // 32][(x + 15) // 32] == 0:
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
        self.equip = [0 for i in range(5)]

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

        if self.equip[0] != 0:
            self.equip[0].DrawEquip(user.screen, user.size)

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
            if pov == 0 and MainHero.y - 32 <= user.S[i - k].y <= MainHero.y and MainHero.x - 16 <= user.S[i - k].x < MainHero.x + 16:
                user.S[i - k].health -= 1
                if user.S[i - k].health < 1:
                    user.AS.remove(user.S[i - k])
                    del user.S[i - k]
                    k += 1
            if pov == 1 and MainHero.y - 16 <= user.S[i - k].y <= MainHero.y + 16 and MainHero.x - 32 <= user.S[i - k].x < MainHero.x:
                user.S[i - k].health -= 1
                if user.S[i - k].health < 1:
                    user.AS.remove(user.S[i - k])
                    del user.S[i - k]
                    k += 1
            if pov == 2 and MainHero.y - 32 <= user.S[i - k].y <= MainHero.y and MainHero.x - 48 <= user.S[i - k].x < MainHero.x - 16:
                user.S[i - k].health -= 1
                if user.S[i - k].health < 1:
                    user.AS.remove(user.S[i - k])
                    del user.S[i - k]
                    k += 1
            if pov == 3 and MainHero.y - 48 <= user.S[i - k].y <= MainHero.y - 16 and MainHero.x - 32 <= user.S[i - k].x < MainHero.x :
                user.S[i - k].health -= 1
                if user.S[i - k].health < 1:
                    user.AS.remove(user.S[i - k])
                    del user.S[i - k]
                    k += 1

user = settings()

if __name__ == '__main__':

    # подгрузочка всякой всячены
    cursor = []
    cursori = pygame.image.load('data/cursor.png')
    pygame.init()
    with open('maps/level1.map') as data:
        user = settings(autosize=1, level=Map([list(map(int, i.split())) for i in data.readlines()]))
    pygame.display.set_caption('PyG')


    pygame.mouse.set_visible(False)
    run_image = pygame.image.load('data/main_run.png')
    user.screen = pygame.display.set_mode(user.size, pygame.FULLSCREEN)
    font = pygame.font.Font(None, 30)
    MainLoop = True
    clock = pygame.time.Clock()
    MainHero = Hero()
    MainHero.image.convert_alpha()
    MainHero.back.append(items.weapon(10))

    # создание Emeny
    user.load_guys('maps/level1.guys')

    while MainLoop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                MainLoop = False
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
                if user.size[0] // 2 - 20 < event.pos[0] < user.size[0] // 2 + 20 and\
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
                    if MainHero.pow == 0 and MainHero.x < len(user.level.map[0]) * 32 - 144 and\
                            user.level.check(MainHero.x + 128, MainHero.y) and MainHero.stamina > 300:
                        MainHero.stamina -= 300
                        MainHero.x += 128
                    elif MainHero.pow == 1 and MainHero.y < len(user.level.map) * 32 - 144 and\
                            user.level.check(MainHero.x, MainHero.y + 128) and MainHero.stamina > 300:
                        MainHero.stamina -= 300
                        MainHero.y += 128
                    elif MainHero.pow == 2 and MainHero.x > 144 and\
                            user.level.check(MainHero.x - 128, MainHero.y) and MainHero.stamina > 300:
                        MainHero.stamina -= 300
                        MainHero.x -= 128
                    elif MainHero.pow == 3 and MainHero.y > 144 and\
                            user.level.check(MainHero.x, MainHero.y - 128) and MainHero.stamina > 300:
                        MainHero.stamina -= 300
                        MainHero.y -= 128
                    else:
                        CanJump = False
                    hud()
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

            if pygame.K_e in user.KeyPressed:
                user.KeyPressed = []
                hud()
                MainHero.draw()
                user.AS.draw(user.screen)
                flip()
                ret = invertory.draw(user.screen, MainHero.back, cursor[0], cursor[1])
                if ret != -1:
                    if ret[1] == 1:
                        MainHero.equip[0] = MainHero.back[ret[0] - 1]


        for i in user.S:
            if i.health <= 0:
                del i

        # отрисовка всякой всячены(иницализированой в одном из прошлых комментариев)
        hud()
        MainHero.draw()
        health = [MainHero.health]
        user.AS.update(MainHero.x, MainHero.y, user.size, user.level.check, health)
        MainHero.health = health[0]
        health = None
        user.AS.draw(user.screen)
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
