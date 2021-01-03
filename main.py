# Подключение библиотек
import pygame, time, random
from math import cos, sin, pi
# define
fps = 60
KeyPressed = []

class Map:
    def __init__(self, map):
        self.map = map

    def draw(self):
        global screen
        for j in range(len(self.map)):
            for i in range(len(self.map[j])):
                if self.map[j][i] == 1:
                    pygame.draw.rect(screen, 'green', (i*32, j*32, 32, 32))

class Hero:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('data/human.png')
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.pow = 0
        self.flipped = False

    def draw(self, x=-1, y=-1):
        global screen
        if x == -1 and y == -1:
            screen.blit(self.image, (self.x - 16, self.y - 16))
        else:
            screen.blit(self.image, (x, y))

    def kick(self, pov):
        R = 32
        x1 = self.x + int(R * cos(pov * pi / 180))
        y1 = self.y + int(R * sin(pov * pi / 180))
        x2 = x1
        y2 = y1
        for i in range(0, 100):
            rad = (i + pov) * pi / 180

            pygame.draw.line(screen, (255/100*i, 255/100*i, 255/100*i), (self.x, self.y), (x2, y2), width=1)
            pygame.draw.line(screen, 'white', (x1, y1), (x2, y2), width=1)
            x2 = x1
            y2 = y1
            x1 = int(R * cos(rad)) + self.x
            y1 = int(R * sin(rad)) + self.y
            self.draw()
            pygame.display.flip()
        time.sleep(0.5)

    def igni(self, pov):
        for R in range(20, 60):
            x1 = self.x + int(R * cos(pov * pi / 180))
            y1 = self.y + int(R * sin(pov * pi / 180))
            x2 = x1
            y2 = y1
            time.sleep(0.006)
            for i in range(0, 100):
                rad = (i + pov) * pi / 180
                if random.randint(0, 3) == 1:
                    pygame.draw.line(screen, (255, 255-(R-20)*6, 0), (x1, y1), (x2, y2), width=1)
                x2 = x1
                y2 = y1
                x1 = round(R * cos(rad)) + self.x
                y1 = round(R * sin(rad)) + self.y
            pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('PyG')
    screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
    MainLoop = True
    clock = pygame.time.Clock()
    MainHero = Hero(300, 100)
    MainHero.image.convert_alpha()
    Level01 = Map([[1, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1]])
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
                MainHero.y -= 2
                MainHero.pow = 3
            if pygame.K_s in KeyPressed:
                MainHero.y += 2
                MainHero.pow = 1
            if pygame.K_a in KeyPressed:
                MainHero.x -= 2
                MainHero.pow = 2
                if not MainHero.flipped:
                    MainHero.image = pygame.transform.flip(MainHero.image, True, False)
                    MainHero.flipped = True
            if pygame.K_d in KeyPressed:
                MainHero.x += 2
                MainHero.pow = 0
                if MainHero.flipped:
                    MainHero.image = pygame.transform.flip(MainHero.image, True, False)
                    MainHero.flipped = False
            if pygame.K_SPACE in KeyPressed:
                MainHero.kick(MainHero.pow * 90 - 50)
            if pygame.K_q in KeyPressed:
                MainHero.igni(MainHero.pow * 90 - 50)

        screen.fill((0, 0, 0))
        Level01.draw()
        pygame.draw.rect(screen, 'white', (1216, 0, 32, 96), width=1)
        pygame.draw.rect(screen, 'white', (1184, 32, 96, 32), width=1)
        MainHero.draw()
        clock.tick(fps)
        pygame.display.flip()



    pygame.quit()