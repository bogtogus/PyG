# Подключение библиотек
import pygame, time, random, datetime
from math import cos, sin, pi

t1 = datetime.datetime.now()

def flip():
    global t1
    pygame.draw.rect(user.screen, 'black', (0, 0, 40, 20))
    user.screen.blit(font.render(str(1000 // ((datetime.datetime.now() - t1).microseconds / 1000)), True, 'yellow'), (0, 0))
    pygame.display.flip()
    t1 = datetime.datetime.now()


# define

class settings:
    def doc(self):
        r = 'fps(=60) -> int, size(=\'1280x720\') -> str, level(=\'level1.map\') -> str\n'
        r += 'fps - frames per second\n'
        r += 'size - size screen\n'
        r += 'level - map'
        return r

    def __init__(self, fps=60, size='1280x720', level=None, autosize=False):
        self.fps = fps
        self.KeyPressed = []
        if autosize:
            size = str(pygame.display.Info().current_w) + 'x' + str(pygame.display.Info().current_h)
        self.size = list(map(int, size.split('x')))
        self.level = level
        self.screen = None

def hud():
    user.screen.fill((0, 0, 0))
    level1.draw()
    pygame.draw.rect(user.screen, 'white', (user.size[0] - 64, 0, 32, 96), width=1)
    pygame.draw.rect(user.screen, 'white', (user.size[0] - 96, 32, 96, 32), width=1)


class Map:
    def __init__(self, map: list):
        self.map = map
        self.wall = pygame.image.load('data/wall.png')
        self.plintus = pygame.image.load('data/plintus.png')

    def draw(self):
        for j in range(len(self.map)):
            for i in range(len(self.map[j])):
                if self.map[j][i] == 1:
                    user.screen.blit(self.wall, (user.size[0] // 2 + i * 32 - MainHero.x,
                                            user.size[1] // 2 + j * 32 - MainHero.y))
                if self.map[j][i] == 0:
                    user.screen.blit(self.plintus, (user.size[0] // 2 + i * 32 - MainHero.x,
                                               user.size[1] // 2 + j * 32 - MainHero.y))

    def check(self, x, y: int):
        if self.map[(y - 15) // 32][(x - 15) // 32] == 0 and self.map[(y - 15) // 32][(x + 15) // 32] == 0 and \
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
        self.stamina = 1000
        self.manna = 1000
        self.health = 1000

    def draw(self):
        user.screen.blit(self.image, (user.size[0] // 2 - 16, user.size[1] // 2 - 16))
        if self.stamina < 100:
            pygame.draw.line(user.screen, 'red', (user.size[0] // 2 + 18, user.size[1] // 2 + 16),
                             (user.size[0] // 2 + 18, user.size[1] // 2 + 16 - (self.stamina // 32)), width=3)
        elif self.stamina < 400:
            pygame.draw.line(user.screen, 'yellow', (user.size[0] // 2 + 18, user.size[1] // 2 + 16),
                             (user.size[0] // 2 + 18, user.size[1] // 2 + 16 - (self.stamina // 32)), width=3)
        elif self.stamina != 1000:
            pygame.draw.line(user.screen, 'white', (user.size[0] // 2 + 18, user.size[1] // 2 + 16),
                             (user.size[0] // 2 + 18, user.size[1] // 2 + 16 - (self.stamina // 32)), width=3)
        if self.manna != 1000:
            pygame.draw.line(user.screen, 'blue', (user.size[0] // 2 - 18, user.size[1] // 2 + 16),
                             (user.size[0] // 2 - 18, user.size[1] // 2 + 16 - (self.manna // 30)), width=3)
        if self.health < 250:
            pygame.draw.line(user.screen, 'red', (user.size[0] // 2 - 16, user.size[1] // 2 - 18),
                             (user.size[0] // 2 - 16 + (self.health // 30), user.size[1] // 2 - 18), width=3)
        elif self.health < 500:
            pygame.draw.line(user.screen, 'yellow', (user.size[0] // 2 - 16, user.size[1] // 2 - 18),
                             (user.size[0] // 2 - 16 + (self.health // 30), user.size[1] // 2 - 18), width=3)
        elif self.health != 1000:
            pygame.draw.line(user.screen, 'green', (user.size[0] // 2 - 16, user.size[1] // 2 - 18),
                             (user.size[0] // 2 - 16 + (self.health // 30), user.size[1] // 2 - 18), width=3)

    def punch(self, pov):
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

    def igni(self, pov):
        if self.manna < 300:
            return 0
        self.manna -= 300
        for R in range(20, 60):
            x1 = user.size[0] // 2 + int(R * cos(pov * pi / 180))
            y1 = user.size[1] // 2 + int(R * sin(pov * pi / 180))
            x2 = x1
            y2 = y1
            time.sleep(0.006)
            for i in range(0, 100):
                rad = (i + pov) * pi / 180
                if random.randint(0, 5) == 1:
                    pygame.draw.line(user.screen, (255, 255 - (R - 20) * 6, 0), (x1, y1), (x2, y2), width=1)
                x2 = x1
                y2 = y1
                x1 = round(R * cos(rad)) + user.size[0] // 2
                y1 = round(R * sin(rad)) + user.size[1] // 2
            flip()


debug_kmin = 1000000  # fps_draw

if __name__ == '__main__':

    cursor = []
    cursori = pygame.image.load('data/cursor.png')
    with open('maps/level1.map') as data:
        level1 = Map([list(map(int, i.split())) for i in data.readlines()])
    pygame.init()
    user = settings(size='1280x720', level=level1)
    pygame.display.set_caption('PyG')
    pygame.mouse.set_visible(False)
    run_image = pygame.image.load('data/main_run.png')
    user.screen = pygame.display.set_mode(user.size, pygame.FULLSCREEN)
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
                user.KeyPressed.append(event.key)
            if event.type == pygame.KEYUP:
                del user.KeyPressed[user.KeyPressed.index(event.key)]
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
        if user.KeyPressed:
            if pygame.K_ESCAPE in user.KeyPressed:
                pygame.quit()
                exit('ESC')
            if pygame.K_w in user.KeyPressed:
                MainHero.pow = 3
                if level1.check(MainHero.x, MainHero.y - 2):
                    MainHero.y -= 2
            if pygame.K_s in user.KeyPressed:
                MainHero.pow = 1
                if level1.check(MainHero.x, MainHero.y + 2):
                    MainHero.y += 2

            if pygame.K_a in user.KeyPressed:
                MainHero.pow = 2
                if level1.check(MainHero.x - 2, MainHero.y):
                    MainHero.x -= 2
                if not MainHero.flipped:
                    MainHero.image = pygame.transform.flip(MainHero.image, True, False)
                    run_image = pygame.transform.flip(run_image, True, False)
                    MainHero.flipped = True
            if pygame.K_d in user.KeyPressed:
                MainHero.pow = 0
                if level1.check(MainHero.x + 2, MainHero.y):
                    MainHero.x += 2
                if MainHero.flipped:
                    MainHero.image = pygame.transform.flip(MainHero.image, True, False)
                    run_image = pygame.transform.flip(run_image, True, False)
                    MainHero.flipped = False

            if pygame.K_SPACE in user.KeyPressed:
                if MainHero.stamina > 300 and MainHero.x - 150 > 0 and MainHero.y - 150 > 0 and\
                        MainHero.y + 150 < len(level1.map) * 32 and MainHero.x + 150 < len(user.level.map[0]) * 32: # Надо пофиксить ссылку на длину карту на константу
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

            if pygame.K_q in user.KeyPressed:
                MainHero.igni(MainHero.pow * 90 - 50)

        t = datetime.datetime.now()  # fps_draw
        hud()
        MainHero.draw()
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

    MainLoop = False
    user.screen.fill('black')
    font = pygame.font.Font('data/font.ttf', user.size[1] // 4)
    font2 = pygame.font.Font(None, 32)
    for i in range(255):
        text = font.render('YOU DIED', True, (i, 0, 0))
        text_rect = text.get_rect(center=(user.size[0] // 2, user.size[1] / 2))
        user.screen.blit(text, text_rect)
        flip()
        user.screen.fill('black')
        time.sleep(0.01)
    while MainLoop:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                MainLoop = False
    pygame.quit()
