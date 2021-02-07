import pygame
from random import randint


def next_step(x1, y1, x2, y2: int, step=3):
    c = 0
    dx = x2 - x1
    dy = y2 - y1
    sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
    sign_y = 1 if dy > 0 else -1 if dy < 0 else 0
    if dx < 0:
        dx = -dx
    if dy < 0:
        dy = -dy
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

    def __init__(self, x, y: int, *group):
        super().__init__(*group)
        self.x = x
        self.y = y
        self.g = group
        self.sprite = 0
        self.health = 10

    def update(self, x, y, size, image1, image2):
        if self.sprite < 10:
            self.image = image1
            self.sprite += 1
        elif self.sprite < 20:
            self.image = image2
            self.sprite += 1
        else:
            self.sprite = 0
        self.rect.x = size[0] // 2 + self.x - x
        self.rect.y = size[1] // 2 + self.y - y

class Shark(Emeny):
    image = pygame.image.load('data/Снимок экрана 2021-01-30 в 12.52.32.png')
    image2 = pygame.image.load('data/Снимок экрана 2021-01-30 в 12.52.32.png')

    def __init__(self, x, y: int, size: list, *group):
        super().__init__(x, y, *group)
        self.image = Shark.image
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 2 + self.x - x
        self.rect.y = size[1] // 2 + self.y - y
        self.maxhp = 20
        self.health = self.maxhp
        self.func = 0

    def update(self, x, y, size, check, add, health):
        if abs(self.x - x) + abs(self.y - y) < 250:
            if self.x + 16 < x and check(self.x + 17, self.y + 16):
                self.x += 1
            elif self.x + 16 > x and check(self.x + 15, self.y + 16):
                self.x -= 1
            if self.y + 16 < y and check(self.x + 16, self.y + 17):
                self.y += 1
            elif self.y + 16 > y and check(self.x + 16, self.y + 15):
                self.y -= 1
        super().update(x, y, size, Shark.image, Shark.image2)
        if (self.x - 16 < x < self.x + 48) and (self.y - 16 < y < self.y + 48):
            health[0] -= 5
        pygame.draw.line(pygame.display.get_surface(), (255, 0, 0), (size[0] // 2 + self.x - x,
                size[1] // 2 + self.y - 18 - y),  (size[0] // 2 + self.x - x + int(self.health / self.maxhp * 32),
                                                  size[1] // 2 + self.y - 18 - y), width=3)


class Slime(Emeny):
    image = pygame.image.load('data/elf.png')
    image2 = pygame.image.load('data/elf2.png')

    def __init__(self, x, y: int, size: list, *group):
        super().__init__(x, y, *group)
        self.image = Slime.image
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 2 + self.x - x
        self.rect.y = size[1] // 2 + self.y - y
        self.maxhp = 20
        self.health = self.maxhp
        self.func = 0

    def update(self, x, y, size, check, add, health):
        if abs(self.x - x) + abs(self.y - y) < 250:
            if self.x + 16 < x and check(self.x + 17, self.y + 16):
                self.x += 1
            elif self.x + 16 > x and check(self.x + 15, self.y + 16):
                self.x -= 1
            if self.y + 16 < y and check(self.x + 16, self.y + 17):
                self.y += 1
            elif self.y + 16 > y and check(self.x + 16, self.y + 15):
                self.y -= 1
        super().update(x, y, size, Slime.image, Slime.image2)
        if (self.x - 16 < x < self.x + 48) and (self.y - 16 < y < self.y + 48):
            health[0] -= 5
        pygame.draw.line(pygame.display.get_surface(), (255, 0, 0), (size[0] // 2 + self.x - x,
                size[1] // 2 + self.y - 18 - y),  (size[0] // 2 + self.x - x + int(self.health / self.maxhp * 32),
                                                  size[1] // 2 + self.y - 18 - y), width=3)


class Elf(Emeny):
    image = pygame.image.load('data/elf.png')
    image2 = pygame.image.load('data/elf2.png')

    def __init__(self, x, y: int, size: list, *group):
        super().__init__(x, y, *group)
        self.image = Slime.image
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 2 + self.x - x
        self.rect.y = size[1] // 2 + self.y - y
        self.maxhp = 200
        self.health = self.maxhp

    def update(self, x, y, size, check, add, health):
        if abs(self.x - x) + abs(self.y - y) < 250:
            if self.x + 16 < x and check(self.x + 17, self.y + 16):
                self.x += 1
            elif self.x + 16 > x and check(self.x + 15, self.y + 16):
                self.x -= 1
            if self.y + 16 < y and check(self.x + 16, self.y + 17):
                self.y += 1
            elif self.y + 16 > y and check(self.x + 16, self.y + 15):
                self.y -= 1
        super().update(x, y, size, Elf.image, Elf.image2)
        if (self.x - 16 < x < self.x + 48) and (self.y - 16 < y < self.y + 48):
            health[0] -= 5
        if randint(0, 50) == 0:
            add(KatonFireBall(self.x, self.y, x, y, size, self.g))
        pygame.draw.line(pygame.display.get_surface(), (255, 0, 0), (size[0] // 2 + self.x - x,
                size[1] // 2 + self.y - 18 - y), (size[0] // 2 + self.x - x + int(self.health / self.maxhp * 32),
                size[1] // 2 + self.y - 18 - y), width=3)


class KatonFireBall(Emeny):
    image = pygame.image.load('data/fireball.png')
    image2 = pygame.image.load('data/fireball2.png')

    def __init__(self, x, y, mx, my: int, size: list, *group):
        super().__init__(x, y, *group)
        self.x = x
        self.y = y
        self.image = KatonFireBall.image
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 2 + self.x - mx
        self.rect.y = size[1] // 2 + self.y - my
        self.health = 1
        self.end = (mx - 16, my - 16)

    def update(self, x, y, size, check, add, health):
        self.x, self.y = next_step(self.x, self.y, self.end[0], self.end[1], 2)
        super().update(x, y, size, KatonFireBall.image, KatonFireBall.image2)
        if not check(self.x + 16, self.y + 16, 8):
            self.health = 0
        if (x - 16 < self.x + 16 < x + 16) and (y - 16 < self.y + 16 < y + 16):
            health[0] -= 80
            self.health = 0
        if abs(self.x - self.end[0]) < 3 and abs(self.y - self.end[1]) < 3:
            self.health = 0
        if self.x - 1 == self.end[0] - 1 and self.y - 1 == self.end[1] - 1:
            self.health = 0
        if self.health == 0:
            add(self, 1)


class Boss(pygame.sprite.Sprite):
    __sprite = [pygame.image.load('data/ricardo/ric (' + str(i) + ').png') for i in range(1, 10)]
    for i in __sprite:
        i.set_colorkey((0, 0, 0))
    def __init__(self, x, y, size: list, *group):
        super().__init__(*group)
        self.x = x
        self.y = y
        self.image = Boss.__sprite[0]
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 2 + self.x - x
        self.rect.y = size[1] // 2 + self.y - y
        self.fullhp = 200
        self.health = self.fullhp
        self.sprite = 0
        self.g = group

    def update(self, x, y, size, check, add, health):
        if self.x + 16 < x and check(self.x + 18, self.y + 16):
            self.x += 1
        elif self.x + 16 > x and check(self.x + 14, self.y + 16):
            self.x -= 1
        if self.y + 16 < y and check(self.x + 16, self.y + 18):
            self.y += 1
        elif self.y + 16 > y and check(self.x + 16, self.y + 14):
            self.y -= 1

        if self.sprite < 90:
            self.image = Boss.__sprite[self.sprite // 10]
        else:
            self.sprite = -1
        self.sprite += 1
        self.rect.x = size[0] // 2 + self.x - x
        self.rect.y = size[1] // 2 + self.y - y

        if (self.x < x < self.x + 32) and (self.y < y < self.y + 32):
            health[0] -= 7

        pygame.draw.line(pygame.display.get_surface(), (128, 0, 255), (100, 50),
                         (100 + int(self.health / self.fullhp * (size[0] - 100)) - 100, 50), width=20)

        if randint(0, 2) == 0:
            add(Naklz(randint(32, 1280), 32, x, y, size, self.g))
        if randint(0, 2) == 0:
            add(Naklz(randint(32, 1280), 704, x, y, size, self.g))
        if randint(0, 2) == 0:
            add(Naklz(32, randint(32, 704), x, y, size, self.g))
        if randint(0, 2) == 0:
            add(Naklz(1280, randint(32, 704), x, y, size, self.g))

class Naklz(Emeny):
    image = pygame.image.load('data/naklz.png')
    image2 = pygame.image.load('data/naklz2.png')

    def __init__(self, x, y, mx, my: int, size: list, *group):
        super().__init__(x, y, *group)
        self.x = x
        self.y = y
        self.image = Naklz.image
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 2 + self.x - mx
        self.rect.y = size[1] // 2 + self.y - my
        self.health = 1
        self.end = (mx - 16, my - 16)

    def update(self, x, y, size, check, add, health):
        self.x, self.y = next_step(self.x, self.y, x-16, y-16, randint(2, 3))

        super().update(x, y, size, Naklz.image, Naklz.image2)
        if not check(self.x + 16, self.y + 16, 8):
            self.health = 0
        if (x - 16 < self.x + 16 < x + 16) and (y - 16 < self.y + 16 < y + 16):
            health[0] -= 800
            self.health = 0
        if abs(self.x - x + 16) < 3 and abs(self.y - y + 16) < 3:
            self.health = 0
        if self.x - 1 == self.end[0] - 1 and self.y - 1 == self.end[1] - 1:
            self.health = 0
        if self.health == 0:
            add(self, 1)

class Prism(Emeny):
    image = pygame.image.load('data/prisma.png')
    image2 = pygame.image.load('data/prisma2.png')

    def __init__(self, x, y: int, size: list, *group):
        super().__init__(x, y, *group)
        self.image = Slime.image
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 2 + self.x - x
        self.rect.y = size[1] // 2 + self.y - y
        self.maxhp = 200
        self.health = self.maxhp
        self.func = 0

    def update(self, x, y, size, check, add, health):
        if abs(self.x - x) + abs(self.y - y) < 250:
            if self.x + 16 < x and check(self.x + 17, self.y + 16):
                self.x += 1
            elif self.x + 16 > x and check(self.x + 15, self.y + 16):
                self.x -= 1
            if self.y + 16 < y and check(self.x + 16, self.y + 17):
                self.y += 1
            elif self.y + 16 > y and check(self.x + 16, self.y + 15):
                self.y -= 1
        super().update(x, y, size, Prism.image, Prism.image2)
        if (self.x - 16 < x < self.x + 48) and (self.y - 16 < y < self.y + 48):
            health[0] -= 50