import pygame, random, ctypes


class Emeny(pygame.sprite.Sprite):
    image = pygame.image.load('C:/Users/MISA/Pictures/Pixel Studio/data/slime.png')
    image2 = pygame.image.load('C:/Users/MISA/Pictures/Pixel Studio/data/slime2.png')

    def __init__(self, x, y:int, size:list, *group):
        super().__init__(*group)
        self.image = Emeny.image
        self.sprite = 0
        self.rect = self.image.get_rect()
        self.x = random.randint(32, 1000)
        self.y = random.randint(32, 1000)
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