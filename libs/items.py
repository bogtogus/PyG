import pygame
import accessify

class Weapon:
    __image = pygame.image.load('data/sword.png')

    def __init__(self, damage, accu):
        self.damage = damage
        self.accuracy = accu

    def DrawEquip(self, SCREEN:pygame.surface, size:list):
        SCREEN.blit(Weapon.__image, (size[0] - 32, 32))

    def draw(self, SCREEN:pygame.surface, x, y: int):
        SCREEN.blit(Weapon.__image, (x, y))


class Armor:
    __image = pygame.image.load('data/armor.png')

    def __init__(self, defend, dod):
        self.defend = defend
        self.dodge = dod

    def DrawEquip(self, SCREEN: pygame.surface, size: list):
        SCREEN.blit(Armor.__image, (size[0] - 64, 32))

    def draw(self, SCREEN: pygame.surface, x, y: int):
        SCREEN.blit(Armor.__image, (x, y))