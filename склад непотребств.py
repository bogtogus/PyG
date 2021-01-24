import pygame, random

import pygame, datetime, threading
class settings:
    def __init__(self):
        self.wall = [1]

user = settings()

ma = [[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 1, 1, 0, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]]

class wave:
    def __init__(self, start, end: list, m: list):
        self.map = m.copy()
        self.map = [[0 if self.map[i][j] == 0 else -1 for j in range(len(self.map[i]))] for i in range(len(self.map))]
        self.s = start
        self.e = end
        self.path = []

    def ripple(self, x, y, k):
        if k == 100:
            return 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (abs(i) == abs(j)) or self.map[x+i][y+j] == -1:
                    continue
                if self.map[x+i][y+j] == 0:
                    self.map[x+i][y+j] = self.map[x][y] + 1
                    self.ripple(x+i, y+j, k + 1)
                elif self.map[x+i][y+j] > self.map[x][y] + 1 and self.map[x+i][y+j] != 1:
                    self.map[x + i][y + j] = self.map[x][y] + 1
                    self.ripple(x+i, y+j, k + 1)


    def reverce_ripple(self, x, y):
        if x == self.s[1] and y == self.s[0]:
            self.path.append((x, y))
            return 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.map[x+i][y+j] + 1 == self.map[x][y]:
                    self.path.append((x, y))
                    self.reverce_ripple(x + i, y + j)
                    return 0

    def start(self):
        t1 = datetime.datetime.now()
        self.map[self.s[1]][self.s[0]] = 1
        self.ripple(self.s[1], self.s[0], 0)
        self.reverce_ripple(self.e[1], self.e[0])
        print(str((datetime.datetime.now() - t1).microseconds // 1000))

with open('maps/level1.map') as data:
    ma = [list(map(int, i.split())) for i in data.readlines()]



l = wave((2, 2), (30, 9), ma)
#t = threading.Thread(target=l.start)
l.start()

t2 = datetime.datetime.now()
pygame.init()
#pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((1280, 720))
MainLoop = True
clock = pygame.time.Clock()
font = pygame.font.Font(None, 15)

for j in range(len(l.map)):
    for i in range(len(l.map[j])):
        if l.map[j][i] > 0:
            pygame.draw.rect(screen, (255, 255 - l.map[j][i] * 3, 0), (i*20, j*20, 20, 20))
            screen.blit(font.render(str(l.map[j][i]), True, 'black'), (i*20, j*20))
        else:
            pygame.draw.rect(screen, (64, 64, 64), (i * 20, j * 20, 20, 20))
            screen.blit(font.render('wall', True, 'black'), (i * 20, j * 20))

pygame.display.flip()

for i in l.path:
    pygame.draw.rect(screen, (128, 255, 0), (i[1] * 20, i[0] * 20, 20, 20))
    screen.blit(font.render('path', True, 'black'), (i[1] * 20, i[0] * 20))

pygame.display.flip()

while MainLoop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            MainLoop = False


def next(x1, y1, x2, y2: int, step=3):
    dx = x2 - x1
    dy = y2 - y1
    sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
    sign_y = 1 if dy > 0 else -1 if dy < 0 else 0
    if dx < 0: dx = -dx
    if dy < 0: dy = -dy
    if dx > dy:
        pdx, pdy = sign_x, 0
        es, el = dy, dx
    else:
        pdx, pdy = 0, sign_y
        es, el = dx, dy
    x, y = x1, y1
    error, t = el / 2, 0
    for i in range(step):
        error -= es
        if error < 0:
                error += el
                x += sign_x
                y += sign_y
            else:
                x += pdx
                y += pdy
            t += 1
            c = (x, y)
    return c


class Emeny(pygame.sprite.Sprite):
    image = pygame.image.load('data/apple.png')
    def __init__(self, *group):
        super().__init__(*group)
        self.image = Emeny.image
        self.rect = self.image.get_rect()
        self.x = 346
        self.y = 346
        self.rect.x = user.size[0] // 2 - self.x
        self.rect.x = user.size[0] // 2 - self.y
        self.point = (random.randint(16, 704), random.randint(16, 704))
    def update(self):
        if self.rect.x + 16 < self.point[0]:
            self.rect = self.rect.move(1, 0)
        if self.rect.x + 16 > self.point[0]:
            self.rect = self.rect.move(-1, 0)
        if self.rect.y + 16 < self.point[1]:
            self.rect = self.rect.move(0, 1)
        if self.rect.y + 16 > self.point[1]:
            self.rect = self.rect.move(0, -1)
        pygame.draw.circle(screen, 'white', self.point, 3)
        if self.rect.x < MainHero.x < self.rect.x + 32 and self.rect.y < MainHero.x < self.rect.y + 32:



pygame.init()
pygame.display.set_caption('PyG')
pygame.mouse.set_visible(False)
print(pygame.display.Info().current_w, pygame.display.Info().current_h)
screen = pygame.display.set_mode((720, 720), pygame.FULLSCREEN)
MainLoop = True
clock = pygame.time.Clock()

AS = pygame.sprite.Group()
Emeny(AS)



while MainLoop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            MainLoop = False
    AS.update()
    AS.draw(screen)
    pygame.display.flip()
    clock.tick(150)