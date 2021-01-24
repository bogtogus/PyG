import pygame, main
from random import randint

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
    image = pygame.image.load('data/slime.png')
    image2 = pygame.image.load('data/slime2.png')

    def __init__(self, x, y: int, size: list, *group):
        super().__init__(*group)
        self.x = x
        self.y = y
        self.image = Emeny.image
        self.sprite = 0
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 2 + self.x - x
        self.rect.y = size[1] // 2 + self.y - y
        self.health = 10

    def update(self, x, y, size, check, health):
        if abs(self.x - x) + abs(self.y - y) < 250:
            if self.x + 16 < x and check(self.x + 17, self.y + 16):
                self.x += 1
            if self.x + 16 > x and check(self.x + 15, self.y + 16):
                self.x -= 1
            if self.y + 16 < y and check(self.x + 16, self.y + 17):
                self.y += 1
            if self.y + 16 > y and check(self.x + 16, self.y + 15):
                self.y -= 1
            if (self.x < x < self.x + 32) and (self.y < y < self.y + 32):
                health[0] -= 1
            if self.sprite < 10:
                self.image = Emeny.image2
                self.sprite += 1
            elif self.sprite < 20:
                self.image = Emeny.image
                self.sprite += 1
            else:
                self.sprite = 0
        self.rect.x = size[0] // 2 + self.x - x
        self.rect.y = size[1] // 2 + self.y - y


class Emeny(pygame.sprite.Sprite):

    def __init__(self, x, y: int, size: list, *group):
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


class Slime(Emeny):
    image = pygame.image.load('data/slime.png')
    image2 = pygame.image.load('data/slime2.png')

    def __init__(self, x, y: int, size: list, *group):
        super().__init__(x, y, size, *group)
        self.image = Slime.image
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 2 + self.x - x
        self.rect.y = size[1] // 2 + self.y - y
        self.health = 2

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
        if randint(0, 200) == 0:
            add(Katon_FireBall(self.x, self.y, x, y, size, self.g))

class Katon_FireBall(Emeny):
    image = pygame.image.load('data/fireball.png')
    image2 = pygame.image.load('data/fireball2.png')

    def __init__(self, x, y, mx, my: int, size: list, *group):
        super().__init__(x, y, size, *group)
        self.x = x
        self.y = y
        self.image = Katon_FireBall.image
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 2 + self.x - mx
        self.rect.y = size[1] // 2 + self.y - my
        self.health = 1


    def update(self, x, y, size, check, add, health):
        self.x, self.y = next(self.x, self.y, x-16, y-16, 2)
        super().update(x, y, size, Katon_FireBall.image, Katon_FireBall.image2)
        if not check(self.x+16, self.y+16):
            self.health = 0
        if (x - 16 < self.x + 16 < x + 16) and (y - 16 < self.y + 16 < y + 16):
            health[0] -= 200
            self.health = 0
        if self.health == 0:
            add(self, 1)