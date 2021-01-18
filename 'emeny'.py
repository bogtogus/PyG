import pygame, random


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