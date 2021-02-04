import pygame

class Weapon:
    __image = pygame.image.load('data/sword.png')

    def __init__(self, damage, accu):
        self.damage = damage
        self.accuracy = accu
        self.cost = damage*accu

    def DrawEquip(self, SCREEN:pygame.surface, size:list, image=__image):
        SCREEN.blit(image, (size[0] - 32, 32))

    def draw(self, SCREEN:pygame.surface, x, y: int, image=__image):
        SCREEN.blit(image, (x, y))


class Armor:
    __image = pygame.image.load('data/armor.png')

    def __init__(self, defend, dod):
        self.defend = defend
        self.dodge = dod
        self.cost = defend*dod

    def DrawEquip(self, SCREEN: pygame.surface, size: list, image=__image):
        SCREEN.blit(image, (size[0] - 64, 32))

    def draw(self, SCREEN: pygame.surface, x, y: int, image=__image):
        SCREEN.blit(image, (x, y))

class WoodenStick(Weapon):
    __image = pygame.image.load('data/wooden_stick.png')
    def __init__(self):
        super().__init__(4, 0.1)

    def DrawEquip(self, SCREEN: pygame.surface, size: list):
        super().DrawEquip(SCREEN, size, WoodenStick.__image)

    def draw(self, SCREEN: pygame.surface, x, y: int):
        super().draw(SCREEN, x, y, WoodenStick.__image)