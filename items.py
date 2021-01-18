import pygame

class weapon:
    __image = pygame.image.load('C:/Users/MISA/Pictures/Pixel Studio/data/sword.png')

    def __init__(self, damage):
        self.damage = damage
        self.accuracy = 0.8

    def DrawEquip(self, SCREEN:pygame.surface, size:list):
        SCREEN.blit(weapon.__image, (size[0] - 64, 0))

    def draw(self, SCREEN:pygame.surface, x, y: int):
        SCREEN.blit(weapon.__image, (x, y))

