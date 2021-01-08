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
                    screen.blit(self.wall, (640+i*32-MainHero.x, 310+j*32-MainHero.y))
                if self.map[j][i] == 0:
                    screen.blit(self.plintus, (640+i*32-MainHero.x, 310+j*32-MainHero.y))

    def check(self, x, y: int):
        if self.map[(y - 15) // 32][(x - 15) // 32] == 0 and self.map[(y - 15) // 32][(x + 15) // 32] == 0 and\
            self.map[(y + 15) // 32][(x - 15) // 32] == 0 and self.map[(y + 15) // 32][(x + 15) // 32] == 0:
            return True
        return False


class Hero:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('data/main.png')
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.pow = 0
        self.flipped = False

    def draw(self, x=-1, y=-1):
        if x == -1 and y == -1:
            screen.blit(self.image, (640 - 16, 310 - 16))

    def punch(self, pov):
        R = 32
        x1 = 640 + int(R * cos(pov * pi / 180))
        y1 = 310 + int(R * sin(pov * pi / 180))
        x2 = x1
        y2 = y1
        for i in range(0, 100):
            rad = (i + pov) * pi / 180
            pygame.draw.line(screen, (50+i, 50+i, 50+i), (640, 310), (x2, y2), width=1)
            pygame.draw.line(screen, 'white', (x1, y1), (x2, y2), width=1)
            x2 = x1
            y2 = y1
            x1 = int(R * cos(rad)) + 640
            y1 = int(R * sin(rad)) + 310
            self.draw()
            pygame.display.flip()
        time.sleep(0.5)

    def igni(self, pov):
        for R in range(20, 60):
            x1 = 640 + int(R * cos(pov * pi / 180))
            y1 = 310 + int(R * sin(pov * pi / 180))
            x2 = x1
            y2 = y1
            time.sleep(0.006)
            for i in range(0, 100):
                rad = (i + pov) * pi / 180
                if random.randint(0, 3) == 1:
                    pygame.draw.line(screen, (255, 255-(R-20)*6, 0), (x1, y1), (x2, y2), width=1)
                x2 = x1
                y2 = y1
                x1 = round(R * cos(rad)) + 640
                y1 = round(R * sin(rad)) + 310
            pygame.display.flip()


if __name__ == '__main__':
    with open('maps/level1.map') as data:
        level1 = Map([list(map(int, i.split())) for i in data.readlines()])

    pygame.init()
    pygame.display.set_caption('PyG')
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
            if event.type == pygame.KEYDOWN:
                KeyPressed.append(event.key)
            if event.type == pygame.KEYUP:
                del KeyPressed[KeyPressed.index(event.key)]

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

        hud()
        MainHero.draw()
        flip()
        clock.tick(fps)

    pygame.quit()