# Подключение библиотек
import pygame, time, random, datetime
from math import cos, sin, pi

# define
fps = 60
KeyPressed = []
flip = pygame.display.flip


def hud():
    screen.fill((0, 0, 0))
    level1.draw()
    pygame.draw.rect(screen, 'white', (1216, 0, 32, 96), width=1)
    pygame.draw.rect(screen, 'white', (1184, 32, 96, 32), width=1)


class Map:
    def __init__(self, map: list):
        '''40x22'''
        self.map = map
        self.wall = pygame.image.load('data/wall.png')
        self.plintus = pygame.image.load('data/plintus.png')

    def draw(self):
        for j in range(len(self.map)):
            for i in range(len(self.map[j])):
                if self.map[j][i] == 1:
                    screen.blit(self.wall, (640 + i * 32 - MainHero.x, 310 + j * 32 - MainHero.y))
                if self.map[j][i] == 0:
                    screen.blit(self.plintus, (640 + i * 32 - MainHero.x, 310 + j * 32 - MainHero.y))

    def check(self, x, y: int):
        if self.map[(y - 15) // 32][(x - 15) // 32] == 0 and self.map[(y - 15) // 32][(x + 15) // 32] == 0 and \
                self.map[(y + 15) // 32][(x - 15) // 32] == 0 and self.map[(y + 15) // 32][(x + 15) // 32] == 0:
            return True
        return False


class Hero:
    __doc__ = 'pass'
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('data/main.png')
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.pow = 0
        self.flipped = False
        self.stamina = 1000
        self.manna = 1000
        self.health = 1000

    def draw(self):
        screen.blit(self.image, (640 - 16, 310 - 16))
        if self.stamina < 100:
            pygame.draw.line(screen, 'red', (660, 326), (660, 326 - (self.stamina // 30)), width=3)
        elif self.stamina < 400:
            pygame.draw.line(screen, 'yellow', (660, 326), (660, 326 - (self.stamina // 30)), width=3)
        elif self.stamina != 1000:
            pygame.draw.line(screen, 'white', (658, 326), (658, 326 - (self.stamina // 30)), width=3)
        if self.manna != 1000:
            pygame.draw.line(screen, 'blue', (622, 326), (622, 326 - (self.manna // 30)), width=3)
        if self.health < 250:
            pygame.draw.line(screen, 'red', (624, 290), (624 + (self.health // 30), 290), width=3)
        elif self.health < 500:
            pygame.draw.line(screen, 'yellow', (624, 290), (624 + (self.health // 30), 290), width=3)
        elif self.health != 1000:
            pygame.draw.line(screen, 'green', (624, 290), (624 + (self.health // 30), 290), width=3)

    def punch(self, pov):
        R = 32
        x1 = 640 + int(R * cos(pov * pi / 180))
        y1 = 310 + int(R * sin(pov * pi / 180))
        x2 = x1
        y2 = y1
        for i in range(0, 100):
            rad = (i + pov) * pi / 180
            pygame.draw.line(screen, (50 + i, 50 + i, 50 + i), (640, 310), (x2, y2), width=1)
            pygame.draw.line(screen, 'white', (x1, y1), (x2, y2), width=1)
            x2 = x1
            y2 = y1
            x1 = int(R * cos(rad)) + 640
            y1 = int(R * sin(rad)) + 310
            self.draw()
            pygame.display.flip()
        time.sleep(0.5)

    def igni(self, pov):
        if self.manna < 300:
            return 0
        self.manna -= 300
        for R in range(20, 60):
            x1 = 640 + int(R * cos(pov * pi / 180))
            y1 = 310 + int(R * sin(pov * pi / 180))
            x2 = x1
            y2 = y1
            time.sleep(0.006)
            for i in range(0, 100):
                rad = (i + pov) * pi / 180
                if random.randint(0, 3) == 1:
                    pygame.draw.line(screen, (255, 255 - (R - 20) * 6, 0), (x1, y1), (x2, y2), width=1)
                x2 = x1
                y2 = y1
                x1 = round(R * cos(rad)) + 640
                y1 = round(R * sin(rad)) + 310
            pygame.display.flip()


debug_kmin = 1000000  # fps_draw

if __name__ == '__main__':
    cursor = []
    cursori = pygame.image.load('data/cursor.png')
    with open('maps/level1.map') as data:
        level1 = Map([list(map(int, i.split())) for i in data.readlines()])
    pygame.init()
    pygame.display.set_caption('PyG')
    pygame.mouse.set_visible(False)
    run_image = pygame.image.load('data/main_run.png')
    screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
    font = pygame.font.Font(None, 30)
    MainLoop = True
    clock = pygame.time.Clock()

    MainHero = Hero(64, 64)
    MainHero.image.convert_alpha()

    while MainLoop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                MainLoop = False
            if event.type == pygame.MOUSEMOTION:
                cursor = event.pos
            if event.type == pygame.KEYDOWN:
                KeyPressed.append(event.key)
            if event.type == pygame.KEYUP:
                del KeyPressed[KeyPressed.index(event.key)]
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 620 < event.pos[0] < 660 and 290 < event.pos[1] < 330:
                    MainHero.health -= 300

        if KeyPressed:
            if pygame.K_ESCAPE in KeyPressed:
                MainLoop = False
            if pygame.K_w in KeyPressed:
                MainHero.pow = 3
                if level1.check(MainHero.x, MainHero.y - 2):
                    MainHero.y -= 2
            if pygame.K_s in KeyPressed:
                MainHero.pow = 1
                if level1.check(MainHero.x, MainHero.y + 2):
                    MainHero.y += 2

            if pygame.K_a in KeyPressed:
                MainHero.pow = 2
                if level1.check(MainHero.x - 2, MainHero.y):
                    MainHero.x -= 2
                if not MainHero.flipped:
                    MainHero.image = pygame.transform.flip(MainHero.image, True, False)
                    run_image = pygame.transform.flip(run_image, True, False)
                    MainHero.flipped = True
            if pygame.K_d in KeyPressed:
                MainHero.pow = 0
                if level1.check(MainHero.x + 2, MainHero.y):
                    MainHero.x += 2
                if MainHero.flipped:
                    MainHero.image = pygame.transform.flip(MainHero.image, True, False)
                    run_image = pygame.transform.flip(run_image, True, False)
                    MainHero.flipped = False

            if pygame.K_SPACE in KeyPressed:
                if MainHero.stamina > 300 and MainHero.x - 150 > 0 and MainHero.y - 150 > 0 and\
                        MainHero.y + 150 < len(level1.map) * 32 and MainHero.x + 150 < len(level1.map[0]) * 32: # Надо пофиксить ссылку на длину карту на константу
                    MainHero.stamina -= 300
                    hud()
                    if MainHero.pow == 0:
                        MainHero.x += 105
                    if MainHero.pow == 1:
                        MainHero.y += 105
                    if MainHero.pow == 2:
                        MainHero.x -= 105
                    if MainHero.pow == 3:
                        MainHero.y -= 105
                    hud()
                    tempx = 640
                    tempy = 310
                    for i in range(1, 15):
                        if MainHero.pow == 0:
                            tempx -= i
                        if MainHero.pow == 1:
                            tempy -= i
                        if MainHero.pow == 2:
                            tempx += i
                        if MainHero.pow == 3:
                            tempy += i
                        screen.blit(run_image, (tempx - 16, tempy - 16))
                        flip()
                        MainHero.draw()
                        time.sleep(0.01)
                    MainHero.punch(MainHero.pow * 90 - 50)
            if pygame.K_q in KeyPressed:
                MainHero.igni(MainHero.pow * 90 - 50)

        t = datetime.datetime.now()  # fps_draw
        hud()

        k = int(1000 / ((datetime.datetime.now() - t).microseconds / 1000))  # fps_draw
        if debug_kmin > k: debug_kmin = k  # fps_draw
        screen.blit(font.render(str(k) + ' | min: ' + str(debug_kmin), True, 'green'), (0, 0))  # fps_draw
        screen.blit(font.render(str(MainHero.stamina), True, 'green'), (0, 32))  # fps_draw
        MainHero.draw()
        screen.blit(cursori, cursor)
        flip()
        clock.tick(fps)

        if MainHero.health < 0:
            MainLoop = False

        if MainHero.stamina < 1000:
            MainHero.stamina += 1
        if MainHero.health < 1000:
            MainHero.health += 1
        if MainHero.manna < 1000:
            MainHero.manna += 1

    MainLoop = True
    screen.fill('black')
    font = pygame.font.Font('data/font.ttf', 128)
    font2 = pygame.font.Font(None, 32)
    for i in range(255):
        screen.blit(font.render('YOU DIED', True, (i, 0, 0)), (325, 250))
        pygame.display.flip()
        screen.fill('black')
        time.sleep(0.01)
    while MainLoop:
        screen.fill('black')
        screen.blit(font.render('YOU DIED', True, 'red'), (325, 250))
        screen.blit(font2.render('Нажмите любую кнопку для продолжения', True, 'red'), (425, 400))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                MainLoop = False
        pygame.display.flip()
    pygame.quit()
